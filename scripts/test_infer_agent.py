#!/usr/bin/env python3
"""Acceptance tests for the hybrid inference agent (rule engine + DeepSeek).

These tests call DeepSeek API and require DEEPSEEK_API_KEY in .env or environment.
Run with: python3 scripts/test_infer_agent.py

Test coverage:
  - h1: hybrid mode activates and returns correct engine metadata
  - h2: rule engine hard logic preserved (scores, statuses, symptoms unchanged)
  - h3: LLM generates narrative for each meridian
  - h4: storefront meets acceptance criteria (talkTrack=3, 不等同, stable tone)
  - h5: all 5 demo cases pass hybrid mode
  - h6: rule-only fallback works without API key
  - h7: API server integration (rule mode, no DeepSeek dependency)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AGENT_SCRIPT = ROOT / "scripts" / "infer_agent.py"
API_SCRIPT = ROOT / "scripts" / "tcm_api.py"

CASES = [
    "fixtures/case_left_low.json",
    "fixtures/case_right_low.json",
    "fixtures/case_cross.json",
    "fixtures/case_multi.json",
    "fixtures/case_stable.json",
]


def run_agent(case_path: str, *, rule_only: bool = False) -> dict[str, Any]:
    cmd = ["python3", str(AGENT_SCRIPT), case_path]
    if rule_only:
        cmd.append("--rule-only")
    out = subprocess.check_output(cmd, cwd=ROOT, text=True, timeout=180)
    return json.loads(out)


def _has_api_key() -> bool:
    """Check if DeepSeek API key is available."""
    env_path = ROOT / ".env"
    if os.environ.get("DEEPSEEK_API_KEY", "").strip():
        return True
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("DEEPSEEK_API_KEY=") and len(line.split("=", 1)[1].strip()) > 5:
                return True
    return False


# ---------------------------------------------------------------------------
# h1: hybrid mode engine metadata
# ---------------------------------------------------------------------------

def test_h1_hybrid_mode_engine_metadata() -> None:
    data = run_agent("fixtures/case_left_low.json")
    engine = data["engine"]
    assert engine["mode"] == "hybrid", engine
    assert "llmLatency" in engine, engine
    assert isinstance(engine["llmLatency"], (int, float)), engine
    assert engine["llmLatency"] > 0, engine
    assert "llmModel" in engine, engine
    assert engine["version"] == "0.2.0", engine


# ---------------------------------------------------------------------------
# h2: rule engine hard logic preserved in hybrid mode
# ---------------------------------------------------------------------------

def test_h2_hard_logic_preserved() -> None:
    hybrid = run_agent("fixtures/case_left_low.json")
    rule = run_agent("fixtures/case_left_low.json", rule_only=True)

    # Scores must be identical
    assert hybrid["healthScore"] == rule["healthScore"], (
        hybrid["healthScore"], rule["healthScore"]
    )
    assert hybrid["scores"] == rule["scores"]

    # Statuses and symptoms must be identical
    for m in ["liver", "spleen", "kidney", "stomach", "gallbladder", "bladder"]:
        assert hybrid["meridians"][m]["status"] == rule["meridians"][m]["status"], m
        assert hybrid["meridians"][m]["score"] == rule["meridians"][m]["score"], m
        assert hybrid["meridians"][m]["symptoms"] == rule["meridians"][m]["symptoms"], m
        assert hybrid["meridians"][m]["tags"] == rule["meridians"][m]["tags"], m

    # Combinations must be identical
    hybrid_combo_ids = [c["id"] for c in hybrid["combinations"]]
    rule_combo_ids = [c["id"] for c in rule["combinations"]]
    assert hybrid_combo_ids == rule_combo_ids, (hybrid_combo_ids, rule_combo_ids)

    # Risk tags must be identical
    assert hybrid["riskTags"] == rule["riskTags"]


# ---------------------------------------------------------------------------
# h3: LLM generates narrative for each meridian
# ---------------------------------------------------------------------------

def test_h3_meridian_narratives() -> None:
    data = run_agent("fixtures/case_left_low.json")
    for m in ["liver", "spleen", "kidney", "stomach", "gallbladder", "bladder"]:
        narrative = data["meridians"][m].get("narrative", "")
        assert isinstance(narrative, str) and len(narrative) > 5, (m, narrative)


# ---------------------------------------------------------------------------
# h4: storefront acceptance criteria in hybrid mode
# ---------------------------------------------------------------------------

def test_h4_storefront_hybrid() -> None:
    # Non-stable case
    data = run_agent("fixtures/case_left_low.json")
    sf = data["storefront"]
    assert isinstance(sf["talkTrack"], list) and len(sf["talkTrack"]) == 3, sf
    assert "不等同" in sf.get("clientExplanation", ""), sf

    # Stable case: no alarming language
    stable = run_agent("fixtures/case_stable.json")
    sf_s = stable["storefront"]
    assert isinstance(sf_s["talkTrack"], list) and len(sf_s["talkTrack"]) == 3, sf_s
    assert "不等同" in sf_s.get("clientExplanation", ""), sf_s

    blob = " ".join([
        sf_s.get("focusHeadline", ""),
        sf_s.get("clientExplanation", ""),
        *sf_s.get("talkTrack", []),
        sf_s.get("retestPrompt", ""),
    ])
    for bad in ["预警", "严重", "危险", "紧急"]:
        assert bad not in blob, f"stable case contains alarming word '{bad}': {blob}"


# ---------------------------------------------------------------------------
# h5: all 5 demo cases pass hybrid
# ---------------------------------------------------------------------------

def test_h5_all_cases_hybrid() -> None:
    expected_statuses = {
        "fixtures/case_left_low.json": {"liver": "left_low"},
        "fixtures/case_right_low.json": {"liver": "right_low"},
        "fixtures/case_cross.json": {},  # mixed statuses
        "fixtures/case_multi.json": {},  # mixed statuses
        "fixtures/case_stable.json": {"liver": "stable"},
    }

    for case_path in CASES:
        data = run_agent(case_path)
        assert data["engine"]["mode"] == "hybrid", (case_path, data["engine"])

        # Basic structure
        for key in ["healthScore", "meridians", "storefront", "summary"]:
            assert key in data, (case_path, key)

        # Storefront shape
        sf = data["storefront"]
        assert isinstance(sf.get("talkTrack"), list) and len(sf["talkTrack"]) == 3, (
            case_path, sf
        )
        assert "不等同" in sf.get("clientExplanation", ""), (case_path, sf)

        # Narrative for every meridian
        for m in ["liver", "spleen", "kidney", "stomach", "gallbladder", "bladder"]:
            assert data["meridians"][m].get("narrative"), (case_path, m)

        # Check expected statuses
        for m, expected in expected_statuses.get(case_path, {}).items():
            assert data["meridians"][m]["status"] == expected, (
                case_path, m, data["meridians"][m]["status"], expected
            )


# ---------------------------------------------------------------------------
# h6: rule-only fallback (no API key needed)
# ---------------------------------------------------------------------------

def test_h6_rule_only_fallback() -> None:
    data = run_agent("fixtures/case_left_low.json", rule_only=True)
    assert data["engine"]["mode"] == "rule-only", data["engine"]
    assert "llmLatency" not in data["engine"]
    assert data["healthScore"] == 54.0
    assert data["meridians"]["liver"]["status"] == "left_low"
    # Scores should differ across meridians (not all the same)
    score_values = list(data["scores"].values())
    assert len(set(score_values)) > 1, f"all scores identical: {data['scores']}"
    # No narrative in rule-only mode
    assert "narrative" not in data["meridians"]["liver"]


# ---------------------------------------------------------------------------
# h7: API server integration
# ---------------------------------------------------------------------------

def test_h7_api_server_rule_mode() -> None:
    """Start API in rule mode and verify inference endpoint."""
    port = 18798
    env = os.environ.copy()
    env["TCM_INFER_MODE"] = "rule"
    env["TCM_API_PORT"] = str(port)
    # Remove API key to force rule mode
    env.pop("DEEPSEEK_API_KEY", None)

    proc = subprocess.Popen(
        ["python3", str(API_SCRIPT)],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        time.sleep(1.5)

        # Health check
        import urllib.request
        health = urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz")
        assert health.status == 200

        # Root info
        info_resp = urllib.request.urlopen(f"http://127.0.0.1:{port}/")
        info = json.loads(info_resp.read())
        assert info["inferMode"] == "rule", info

        # Inference
        payload = json.dumps({
            "measurements": {
                "liver": {"left": 35.0, "right": 36.1},
                "spleen": {"left": 35.1, "right": 35.8},
                "kidney": {"left": 35.0, "right": 35.9},
                "stomach": {"left": 35.2, "right": 35.9},
                "gallbladder": {"left": 35.1, "right": 36.0},
                "bladder": {"left": 36.0, "right": 35.2},
            }
        }).encode()
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/api/inference/meridian-diagnosis",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        assert "healthScore" in result
        assert "meridians" in result
        assert result["meridians"]["liver"]["status"] == "left_low"
    finally:
        proc.kill()
        proc.wait(timeout=3)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    has_key = _has_api_key()

    # Tests that need DeepSeek API
    hybrid_tests = [
        test_h1_hybrid_mode_engine_metadata,
        test_h2_hard_logic_preserved,
        test_h3_meridian_narratives,
        test_h4_storefront_hybrid,
        test_h5_all_cases_hybrid,
    ]

    # Tests that don't need API
    local_tests = [
        test_h6_rule_only_fallback,
        test_h7_api_server_rule_mode,
    ]

    passed = 0
    failed = 0
    skipped = 0

    for test in hybrid_tests:
        if not has_key:
            print(f"SKIP {test.__name__} (no DEEPSEEK_API_KEY)")
            skipped += 1
            continue
        try:
            test()
            print(f"PASS {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"FAIL {test.__name__}: {e}")
            failed += 1

    for test in local_tests:
        try:
            test()
            print(f"PASS {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"FAIL {test.__name__}: {e}")
            failed += 1

    print(f"\nRESULT: passed={passed} failed={failed} skipped={skipped}")
    sys.exit(1 if failed else 0)
