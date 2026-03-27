#!/usr/bin/env python3
"""TCM Meridian Inference MVP CLI

Goal for c1: project structure readiness.
- Provide a working CLI entrypoint: `python3 scripts/infer.py --help`
- Provide rule/threshold JSON files under ./rules/

This CLI is intentionally lightweight (stdlib-only) and outputs a stable JSON structure
that matches the API doc's recommended consumer fields.

Usage examples:
  python3 scripts/infer.py fixtures/demo_case_01.json
  python3 scripts/infer.py fixtures/demo_case_01.json --pretty
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple

MERIDIANS = ["liver", "spleen", "kidney", "stomach", "gallbladder", "bladder"]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _get_by_path(obj: dict, dotted: str) -> Any:
    cur: Any = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(dotted)
        cur = cur[part]
    return cur


def load_rules(rules_dir: Path) -> Tuple[dict, dict, dict]:
    thresholds = _load_json(rules_dir / "thresholds.json")
    meridian_rules = _load_json(rules_dir / "meridian_rules.json")
    combo_rules = _load_json(rules_dir / "combination_rules.json")
    return thresholds, meridian_rules, combo_rules


def normalize_measurements(payload: dict) -> Dict[str, dict]:
    ms = payload.get("measurements")
    if not isinstance(ms, dict):
        raise ValueError("payload.measurements must be an object")

    out: Dict[str, dict] = {}
    for m in MERIDIANS:
        v = ms.get(m)
        if not isinstance(v, dict):
            raise ValueError(f"measurements.{m} must be an object")

        # Recommended format: left/right/trendDelta
        if "left" in v and "right" in v:
            left = float(v["left"])
            right = float(v["right"])
            trend = float(v.get("trendDelta", right - left))
        # Legacy compatibility: t1/t2
        elif "t1" in v and "t2" in v:
            left = float(v["t1"])
            right = float(v["t2"])
            trend = right - left
        else:
            raise ValueError(f"measurements.{m} must contain left/right or t1/t2")

        out[m] = {
            "left": left,
            "right": right,
            "trendDelta": trend,
        }

    return out


def eval_conditions(fields: dict, thresholds: dict, conditions: list[dict]) -> bool:
    for c in conditions:
        field = c["field"]
        op = c["op"]

        if "valueFrom" in c:
            rhs = _get_by_path({"thresholds": thresholds}, c["valueFrom"])
        else:
            rhs = c["value"]

        lhs = fields.get(field)
        if lhs is None:
            return False

        if op == "<":
            ok = lhs < rhs
        elif op == "<=":
            ok = lhs <= rhs
        elif op == ">":
            ok = lhs > rhs
        elif op == ">=":
            ok = lhs >= rhs
        elif op == "==":
            ok = lhs == rhs
        else:
            raise ValueError(f"Unsupported op: {op}")

        if not ok:
            return False

    return True


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def infer(payload: dict, thresholds: dict, meridian_rules: dict, combo_rules: dict) -> dict:
    subject = payload.get("subject") or {}
    context = payload.get("context") or {}
    measurements = normalize_measurements(payload)

    scoring = thresholds["scoring"]
    base = float(scoring["base"])
    floor = float(scoring["floor"])
    ceiling = float(scoring["ceiling"])
    penalties = scoring["penalty"]

    per_meridian: Dict[str, dict] = {}
    risk_tags: List[str] = []
    advice: List[str] = []
    summaries: List[str] = []

    for m, v in measurements.items():
        left = v["left"]
        right = v["right"]
        avg = (left + right) / 2.0
        diff_abs = abs(left - right)
        trend = v["trendDelta"]
        trend_abs = abs(trend)

        fields = {
            "left": left,
            "right": right,
            "avg": avg,
            "diffAbs": diff_abs,
            "trendDelta": trend,
            "trendAbs": trend_abs,
        }

        score = base
        matched: List[dict] = []
        tags_here: List[str] = []

        for rule in meridian_rules.get("rules", []):
            if rule.get("meridian") not in ("*", m):
                continue
            if eval_conditions(fields, thresholds, rule.get("conditions", [])):
                matched.append({
                    "id": rule.get("id"),
                    "tag": rule.get("tag"),
                    "summary": rule.get("summary"),
                })
                tag = rule.get("tag")
                if tag:
                    tags_here.append(tag)
                pk = rule.get("penaltyKey")
                if pk in penalties:
                    score -= float(penalties[pk])
                if rule.get("summary"):
                    summaries.append(f"{m}:{rule['summary']}")
                for a in rule.get("advice", []) or []:
                    advice.append(a)

        score = clamp(score, floor, ceiling)

        per_meridian[m] = {
            "left": left,
            "right": right,
            "trendDelta": trend,
            "avg": avg,
            "diffAbs": diff_abs,
            "score": round(score, 1),
            "tags": sorted(set(tags_here)),
            "matchedRules": matched,
        }

        risk_tags.extend(tags_here)

    # Combination rules
    unique_tags = sorted(set(risk_tags))
    tag_to_meridians: Dict[str, set] = {}
    for m, d in per_meridian.items():
        for t in d["tags"]:
            tag_to_meridians.setdefault(t, set()).add(m)

    for rule in combo_rules.get("rules", []):
        when = rule.get("when") or {}
        mm = when.get("minMeridiansWithAnyTag")
        ok = True
        if mm:
            tags = mm.get("tags", [])
            need = int(mm.get("count", 0))
            meridians_hit = set()
            for t in tags:
                meridians_hit |= tag_to_meridians.get(t, set())
            ok = len(meridians_hit) >= need

        if ok:
            for t in rule.get("addTags", []) or []:
                unique_tags.append(t)
            if rule.get("summaryAppend"):
                summaries.append(rule["summaryAppend"])
            for a in rule.get("adviceAppend", []) or []:
                advice.append(a)

    unique_tags = sorted(set(unique_tags))
    advice = list(dict.fromkeys(advice))  # de-dup keep order

    # Build stable outputs
    scores_map = {m: per_meridian[m]["score"] for m in MERIDIANS}
    six_dimension_scores = [
        {"meridian": m, "score": scores_map[m], "tags": per_meridian[m]["tags"]}
        for m in MERIDIANS
    ]

    # Simple report summary
    if not unique_tags:
        report_summary = "整体相对平稳，建议保持作息并按周期复测。"
        focus = "整体相对平稳"
    else:
        report_summary = "；".join(summaries[:8]) if summaries else "检测到需要关注的信号，建议结合近期状态复测确认。"
        focus = "需要重点关注：" + ", ".join(unique_tags[:5])

    storefront = {
        "focusHeadline": focus,
        "clientExplanation": report_summary,
        "retestPrompt": "建议间隔 20-30 分钟复测一次，连续 2-3 次趋势更可靠。",
    }

    return {
        "engine": {"mode": "rule-based-mvp", "version": "0.1.0"},
        "subject": subject,
        "context": context,
        "input": {
            "mode": "foot_six",
            "meridians": MERIDIANS,
        },
        "scores": scores_map,
        "sixDimensionScores": six_dimension_scores,
        "riskTags": unique_tags,
        "reportSummary": report_summary,
        "advice": advice,
        "storefront": storefront,
        "trace": {
            "perMeridian": per_meridian,
            "thresholds": thresholds,
        },
    }


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="infer.py",
        description="TCM meridian inference MVP (rule-based) CLI",
    )
    ap.add_argument("input", nargs="?", help="Input JSON file (see fixtures/*.json)")
    ap.add_argument("--rules-dir", default="rules", help="Rules directory (default: ./rules)")
    ap.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    ap.add_argument("--out", help="Write output JSON to file")
    return ap


def main() -> int:
    ap = build_argparser()
    args = ap.parse_args()

    if not args.input:
        ap.print_help()
        return 0

    project_root = Path(__file__).resolve().parents[1]
    in_path = (project_root / args.input).resolve() if not Path(args.input).is_absolute() else Path(args.input)
    rules_dir = (project_root / args.rules_dir).resolve()

    if not in_path.exists():
        raise SystemExit(f"Input not found: {in_path}")
    if not rules_dir.exists():
        raise SystemExit(f"Rules dir not found: {rules_dir}")

    payload = _load_json(in_path)
    thresholds, meridian_rules, combo_rules = load_rules(rules_dir)
    result = infer(payload, thresholds, meridian_rules, combo_rules)

    text = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)

    if args.out:
        out_path = (project_root / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
