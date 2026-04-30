#!/usr/bin/env python3
"""Tests for TCM Meridian Inference Engine v2.0.

Validates the scoring algorithm defined in docs/scoring-algorithm-prd-v2.md.
"""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_case(rel_path: str) -> dict:
    out = subprocess.check_output([
        "python3",
        str(ROOT / "scripts" / "infer.py"),
        rel_path,
    ], cwd=ROOT, text=True)
    return json.loads(out)


# ---------------------------------------------------------------------------
# Step 2: Input validation
# ---------------------------------------------------------------------------

def test_validate_rejects_missing_before_after():
    """Input without before/after structure should fail."""
    import tempfile, os
    bad = {"subject": {"id": "x"}, "measurements": {"liver": {"left": 36, "right": 36}}}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, dir="/tmp") as f:
        json.dump(bad, f)
        f.flush()
        try:
            result = subprocess.run(
                ["python3", str(ROOT / "scripts" / "infer.py"), f.name],
                capture_output=True, text=True, cwd=ROOT,
            )
            assert result.returncode != 0, "Should fail on bad input"
        finally:
            os.unlink(f.name)


# ---------------------------------------------------------------------------
# Step 3: Meridian states
# ---------------------------------------------------------------------------

def test_stable_case_all_balanced():
    data = run_case("fixtures/v2/case_stable.json")
    states = data["engineInference"]["meridianStates"]
    for m in ["liver", "spleen", "kidney", "stomach", "gallbladder", "bladder"]:
        assert states[m]["beforeStatus"] == "balanced", f"{m}: {states[m]}"
        assert states[m]["afterStatus"] == "balanced", f"{m}: {states[m]}"
        assert states[m]["cross"] is False, f"{m}"
        assert states[m]["severity"] == "balanced", f"{m}: {states[m]}"


def test_left_low_case_before_status():
    data = run_case("fixtures/v2/case_left_low.json")
    states = data["engineInference"]["meridianStates"]
    for m in ["liver", "spleen", "kidney", "gallbladder"]:
        assert states[m]["beforeStatus"] == "left_low", f"{m}: {states[m]}"
    assert states[m]["severity"] in ("medium", "high", "mild"), f"unexpected severity"


def test_cross_case_cross_detected():
    data = run_case("fixtures/v2/case_cross.json")
    states = data["engineInference"]["meridianStates"]
    cross_count = sum(1 for s in states.values() if s["cross"])
    assert cross_count >= 3, f"Expected >= 3 crosses, got {cross_count}"


def test_severity_mild_medium_high():
    data = run_case("fixtures/v2/case_left_low.json")
    states = data["engineInference"]["meridianStates"]
    severities = [s["severity"] for s in states.values()]
    assert "high" in severities, f"Expected high severity, got {severities}"


# ---------------------------------------------------------------------------
# Step 4: Global patterns
# ---------------------------------------------------------------------------

def test_global_patterns_left_low():
    data = run_case("fixtures/v2/case_left_low.json")
    gp = data["trace"]["globalPatterns"]
    assert gp["leftLowCountBefore"] >= 4, gp
    assert gp["dominantPatternBefore"] == "left_low", gp


def test_global_patterns_right_low():
    data = run_case("fixtures/v2/case_right_low.json")
    gp = data["trace"]["globalPatterns"]
    assert gp["rightLowCountBefore"] >= 4, gp
    assert gp["dominantPatternBefore"] == "right_low", gp


def test_global_patterns_cross():
    data = run_case("fixtures/v2/case_cross.json")
    gp = data["trace"]["globalPatterns"]
    assert gp["crossCount"] >= 3, gp


def test_global_patterns_stable():
    data = run_case("fixtures/v2/case_stable.json")
    gp = data["trace"]["globalPatterns"]
    assert gp["crossCount"] == 0, gp
    assert gp["leftLowCountBefore"] == 0, gp
    assert gp["rightLowCountBefore"] == 0, gp


# ---------------------------------------------------------------------------
# Step 5: Combination rules
# ---------------------------------------------------------------------------

def test_combo_heart_supply():
    data = run_case("fixtures/v2/case_right_low.json")
    hits = data["engineInference"]["combinationHits"]
    assert "combo_heart_supply" in hits, hits


def test_combo_head_supply():
    data = run_case("fixtures/v2/case_left_low.json")
    hits = data["engineInference"]["combinationHits"]
    assert "combo_head_supply" in hits, hits


def test_combo_reproductive():
    data = run_case("fixtures/v2/case_cross.json")
    hits = data["engineInference"]["combinationHits"]
    assert "combo_reproductive" in hits, hits


def test_combo_multi_cross():
    data = run_case("fixtures/v2/case_cross.json")
    hits = data["engineInference"]["combinationHits"]
    assert "combo_multi_cross" in hits, hits


def test_combo_liver_gall():
    data = run_case("fixtures/v2/case_left_low.json")
    hits = data["engineInference"]["combinationHits"]
    assert "combo_liver_gall" in hits, hits


def test_combo_waist():
    data = run_case("fixtures/v2/case_left_low.json")
    hits = data["engineInference"]["combinationHits"]
    assert "combo_waist" in hits, hits


def test_combo_neck():
    data = run_case("fixtures/v2/case_left_low.json")
    hits = data["engineInference"]["combinationHits"]
    assert "combo_neck" in hits, hits


# ---------------------------------------------------------------------------
# Step 6-7: Scoring
# ---------------------------------------------------------------------------

def test_stable_score_100():
    data = run_case("fixtures/v2/case_stable.json")
    assert data["healthScore"]["score"] == 100, data["healthScore"]
    assert data["healthScore"]["level"] == "健康优秀", data["healthScore"]


def test_stable_score_level_mapping():
    data = run_case("fixtures/v2/case_stable.json")
    assert data["scoreContext"]["scoreLevel"] == "健康优秀"
    assert "优秀" in data["scoreContext"]["scoreSummary"]


def test_left_low_score_below_100():
    data = run_case("fixtures/v2/case_left_low.json")
    assert data["healthScore"]["score"] < 100, data["healthScore"]
    assert data["healthScore"]["score"] >= 30, data["healthScore"]  # floor


def test_cross_score_lower_than_left_low():
    cross = run_case("fixtures/v2/case_cross.json")
    left_low = run_case("fixtures/v2/case_left_low.json")
    assert cross["healthScore"]["score"] < left_low["healthScore"]["score"], \
        f"cross={cross['healthScore']['score']}, left_low={left_low['healthScore']['score']}"


def test_score_floor_30():
    """Score should never go below 30."""
    data = run_case("fixtures/v2/case_cross.json")
    assert data["scoreContext"]["currentRawScore"] >= 30, data["scoreContext"]


def test_score_breakdown_exists():
    data = run_case("fixtures/v2/case_left_low.json")
    breakdown = data["trace"]["scoreBreakdown"]
    assert isinstance(breakdown, list), breakdown
    assert len(breakdown) > 0, "Should have deductions"
    rules = [b["rule"] for b in breakdown]
    assert "single_meridian_high_abnormal" in rules, rules


def test_improvement_bonus():
    data = run_case("fixtures/v2/case_left_low.json")
    bonus_info = data["trace"]["improvementBonus"]
    assert "improvedCount" in bonus_info
    assert "totalBonus" in bonus_info


# ---------------------------------------------------------------------------
# Step 8: Follow-up protection
# ---------------------------------------------------------------------------

def test_followup_protection_triggered():
    data = run_case("fixtures/v2/case_followup.json")
    ctx = data["scoreContext"]
    assert ctx["scoreAdjustedByPolicy"] is True, ctx
    assert ctx["displayedScore"] == 82, ctx  # previousDisplayedScore
    assert ctx["currentRawScore"] < ctx["displayedScore"], ctx


def test_followup_adherence_flag():
    data = run_case("fixtures/v2/case_followup.json")
    assert data["scoreContext"]["adherenceFlag"] is True


# ---------------------------------------------------------------------------
# Step 9: Score level mapping
# ---------------------------------------------------------------------------

def test_score_levels_all_valid():
    cases = [
        "fixtures/v2/case_stable.json",
        "fixtures/v2/case_left_low.json",
        "fixtures/v2/case_right_low.json",
        "fixtures/v2/case_cross.json",
        "fixtures/v2/case_multi.json",
    ]
    valid_levels = {"健康优秀", "轻度失衡", "中度失衡", "严重问题"}
    for path in cases:
        data = run_case(path)
        level = data["healthScore"]["level"]
        assert level in valid_levels, f"{path}: {level}"


# ---------------------------------------------------------------------------
# Step 10: Advice tags
# ---------------------------------------------------------------------------

def test_advice_tags_left_low():
    data = run_case("fixtures/v2/case_left_low.json")
    tags = data["adviceTags"]
    assert "head_supply_attention" in tags, tags


def test_advice_tags_right_low():
    data = run_case("fixtures/v2/case_right_low.json")
    tags = data["adviceTags"]
    assert "heart_supply_attention" in tags, tags


def test_advice_tags_cross():
    data = run_case("fixtures/v2/case_cross.json")
    tags = data["adviceTags"]
    assert "reproductive_system_attention" in tags, tags


# ---------------------------------------------------------------------------
# Output structure
# ---------------------------------------------------------------------------

def test_output_has_required_fields():
    required = {
        "engine", "subject", "engineInference", "scoreContext",
        "healthScore", "overallAssessment", "meridianDetails",
        "combinationAnalysis", "adviceTags", "trace",
    }
    for path in ["fixtures/v2/case_stable.json", "fixtures/v2/case_cross.json"]:
        data = run_case(path)
        missing = required - set(data.keys())
        assert not missing, f"{path}: missing {sorted(missing)}"


def test_health_score_structure():
    for path in ["fixtures/v2/case_stable.json", "fixtures/v2/case_left_low.json"]:
        data = run_case(path)
        hs = data["healthScore"]
        assert "score" in hs, hs
        assert "level" in hs, hs
        assert "summary" in hs, hs


def test_meridian_details_six_meridians():
    data = run_case("fixtures/v2/case_stable.json")
    details = data["meridianDetails"]
    assert len(details) == 6, f"Expected 6 meridian details, got {len(details)}"
    names = {d["meridian"] for d in details}
    assert names == {"肝经", "脾经", "肾经", "胃经", "胆经", "膀胱经"}, names


def test_meridian_details_have_severity():
    data = run_case("fixtures/v2/case_left_low.json")
    for d in data["meridianDetails"]:
        assert "severity" in d, d
        assert d["severity"] in ("balanced", "mild", "medium", "high"), d


def test_overall_assessment_structure():
    data = run_case("fixtures/v2/case_left_low.json")
    oa = data["overallAssessment"]
    assert "overallLevel" in oa
    assert "dominantPattern" in oa
    assert "focusMeridians" in oa
    assert "stableMeridians" in oa


# ---------------------------------------------------------------------------
# All demo cases produce valid output
# ---------------------------------------------------------------------------

def test_all_v2_cases_run():
    cases = [
        "fixtures/v2/case_stable.json",
        "fixtures/v2/case_left_low.json",
        "fixtures/v2/case_right_low.json",
        "fixtures/v2/case_cross.json",
        "fixtures/v2/case_multi.json",
        "fixtures/v2/case_followup.json",
    ]
    for path in cases:
        data = run_case(path)
        assert "healthScore" in data, f"{path}: missing healthScore"
        assert isinstance(data["healthScore"]["score"], (int, float)), f"{path}: bad score type"
        assert data["healthScore"]["score"] >= 30, f"{path}: score below floor"
        print(f"  {path}: score={data['healthScore']['score']} level={data['healthScore']['level']}")


if __name__ == "__main__":
    tests = [
        test_validate_rejects_missing_before_after,
        test_stable_case_all_balanced,
        test_left_low_case_before_status,
        test_cross_case_cross_detected,
        test_severity_mild_medium_high,
        test_global_patterns_left_low,
        test_global_patterns_right_low,
        test_global_patterns_cross,
        test_global_patterns_stable,
        test_combo_heart_supply,
        test_combo_head_supply,
        test_combo_reproductive,
        test_combo_multi_cross,
        test_combo_liver_gall,
        test_combo_waist,
        test_combo_neck,
        test_stable_score_100,
        test_stable_score_level_mapping,
        test_left_low_score_below_100,
        test_cross_score_lower_than_left_low,
        test_score_floor_30,
        test_score_breakdown_exists,
        test_improvement_bonus,
        test_followup_protection_triggered,
        test_followup_adherence_flag,
        test_score_levels_all_valid,
        test_advice_tags_left_low,
        test_advice_tags_right_low,
        test_advice_tags_cross,
        test_output_has_required_fields,
        test_health_score_structure,
        test_meridian_details_six_meridians,
        test_meridian_details_have_severity,
        test_overall_assessment_structure,
        test_all_v2_cases_run,
    ]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as e:
            print(f"FAIL {test.__name__}: {e}")
            failed += 1

    print(f"\n{len(tests) - failed}/{len(tests)} passed, {failed} failed")
    if failed:
        raise SystemExit(1)
