#!/usr/bin/env python3
"""TCM Meridian Inference Engine v2.0

Implements the scoring algorithm defined in docs/scoring-algorithm-prd-v2.md.
Uses before/after measurement model, severity-based state calculation,
whole-score evaluation, improvement bonuses, and follow-up protection.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MERIDIANS = ["liver", "spleen", "kidney", "stomach", "gallbladder", "bladder"]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_rules(rules_dir: Path) -> Tuple[dict, dict, dict, dict, dict]:
    """Load all rule configuration files."""
    thresholds = _load_json(rules_dir / "thresholds.json")
    meridian_rules = _load_json(rules_dir / "meridian_rules.json")
    combo_rules = _load_json(rules_dir / "combination_rules.json")
    score_rules = _load_json(rules_dir / "score_rules.json")
    followup_policy = _load_json(rules_dir / "followup_policy_rules.json")
    return thresholds, meridian_rules, combo_rules, score_rules, followup_policy


# ---------------------------------------------------------------------------
# Step 1: load_input  (handled by CLI, payload passed to infer())
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Step 2: validate_input
# ---------------------------------------------------------------------------

def validate_input(payload: dict) -> None:
    """Validate input completeness. Raises ValueError on failure."""
    ms = payload.get("measurements")
    if not isinstance(ms, dict):
        raise ValueError("payload.measurements must be an object")
    for phase in ("before", "after"):
        phase_data = ms.get(phase)
        if not isinstance(phase_data, dict):
            raise ValueError(f"measurements.{phase} must be an object")
        for m in MERIDIANS:
            v = phase_data.get(m)
            if not isinstance(v, dict):
                raise ValueError(f"measurements.{phase}.{m} must be an object")
            if "left" not in v or "right" not in v:
                raise ValueError(f"measurements.{phase}.{m} must contain left and right")

    session = payload.get("measurementSession") or {}
    if session.get("isFollowup"):
        if "instrumentUsageDaysBetweenMeasurements" not in session:
            raise ValueError("instrumentUsageDaysBetweenMeasurements required for followup")


# ---------------------------------------------------------------------------
# Step 3: compute_meridian_states
# ---------------------------------------------------------------------------

def get_side_status(left: float, right: float, balance_threshold: float = 0.2) -> Tuple[str, Optional[str], float]:
    """Returns (status, low_side, diffAbs)."""
    diff = abs(left - right)
    if diff <= balance_threshold:
        return "balanced", None, diff
    elif left < right:
        return "left_low", "left", diff
    else:
        return "right_low", "right", diff


def get_severity(diff: float, thresholds: dict) -> str:
    """Return severity level based on diffAbs."""
    mild_max = thresholds.get("mild_max", 0.5)
    medium_max = thresholds.get("medium_max", 1.0)
    if diff <= 0.2:
        return "balanced"
    elif diff <= mild_max:
        return "mild"
    elif diff <= medium_max:
        return "medium"
    else:
        return "high"


def compute_meridian_states(payload: dict, score_rules: dict) -> Dict[str, dict]:
    """Step 3: compute per-meridian states from before/after measurements."""
    ms = payload["measurements"]
    before = ms["before"]
    after = ms["after"]
    severity_thresholds = score_rules.get("severity_thresholds", {})

    meridian_states: Dict[str, dict] = {}
    for m in MERIDIANS:
        b = before[m]
        a = after[m]

        before_status, before_low_side, before_diff = get_side_status(b["left"], b["right"])
        after_status, after_low_side, after_diff = get_side_status(a["left"], a["right"])

        cross = (
            before_status in ("left_low", "right_low")
            and after_status in ("left_low", "right_low")
            and before_low_side is not None
            and after_low_side is not None
            and before_low_side != after_low_side
        )

        severity = get_severity(max(before_diff, after_diff), severity_thresholds)

        meridian_states[m] = {
            "beforeStatus": before_status,
            "afterStatus": after_status,
            "beforeLowSide": before_low_side,
            "afterLowSide": after_low_side,
            "beforeDiff": round(before_diff, 4),
            "afterDiff": round(after_diff, 4),
            "cross": cross,
            "severity": severity,
        }

    return meridian_states


# ---------------------------------------------------------------------------
# Step 4: compute_global_patterns
# ---------------------------------------------------------------------------

def compute_global_patterns(meridian_states: Dict[str, dict]) -> dict:
    """Step 4: compute overall bias and cross counts."""
    left_before = right_before = left_after = right_after = cross_count = 0

    for s in meridian_states.values():
        if s["beforeStatus"] == "left_low":
            left_before += 1
        elif s["beforeStatus"] == "right_low":
            right_before += 1
        if s["afterStatus"] == "left_low":
            left_after += 1
        elif s["afterStatus"] == "right_low":
            right_after += 1
        if s["cross"]:
            cross_count += 1

    def _dominant(lc: int, rc: int) -> str:
        if lc > rc:
            return "left_low"
        elif rc > lc:
            return "right_low"
        return "mixed"

    return {
        "leftLowCountBefore": left_before,
        "rightLowCountBefore": right_before,
        "leftLowCountAfter": left_after,
        "rightLowCountAfter": right_after,
        "dominantPatternBefore": _dominant(left_before, right_before),
        "dominantPatternAfter": _dominant(left_after, right_after),
        "crossCount": cross_count,
    }


# ---------------------------------------------------------------------------
# Step 5a: find_lowest_meridian
# ---------------------------------------------------------------------------

def find_lowest_meridian(phase_data: dict) -> dict:
    """Find the lowest temperature meridian+side in a phase."""
    lowest: Optional[dict] = None
    for m in MERIDIANS:
        vals = phase_data[m]
        for side in ("left", "right"):
            value = float(vals[side])
            if lowest is None or value < lowest["value"]:
                lowest = {"meridian": m, "side": side, "value": value}
    return lowest or {}


# ---------------------------------------------------------------------------
# Step 5b: apply_combination_rules
# ---------------------------------------------------------------------------

def apply_combination_rules(
    meridian_states: Dict[str, dict],
    global_patterns: dict,
    combo_rules: dict,
) -> List[str]:
    """Step 5b: determine which combination rules hit. Returns list of rule_ids."""
    hits: List[str] = []

    gp = global_patterns
    kidney = meridian_states["kidney"]
    bladder = meridian_states["bladder"]
    spleen = meridian_states["spleen"]
    liver = meridian_states["liver"]
    gall = meridian_states["gallbladder"]

    # combo_heart_supply: >=4 right_low in before or after
    if gp["rightLowCountBefore"] >= 4 or gp["rightLowCountAfter"] >= 4:
        hits.append("combo_heart_supply")

    # combo_head_supply: >=4 left_low in before or after
    if gp["leftLowCountBefore"] >= 4 or gp["leftLowCountAfter"] >= 4:
        hits.append("combo_head_supply")

    # combo_waist: kidney + bladder same side abnormal (before)
    if (kidney["beforeLowSide"] is not None
            and kidney["beforeLowSide"] == bladder["beforeLowSide"]):
        hits.append("combo_waist")

    # combo_neck: kidney + bladder + spleen all non-balanced (before)
    if (kidney["beforeStatus"] != "balanced"
            and bladder["beforeStatus"] != "balanced"
            and spleen["beforeStatus"] != "balanced"):
        hits.append("combo_neck")

    # combo_reproductive: kidney cross + bladder cross
    if kidney["cross"] and bladder["cross"]:
        hits.append("combo_reproductive")

    # combo_liver_gall: liver + gallbladder both non-balanced (before)
    if (liver["beforeStatus"] != "balanced"
            and gall["beforeStatus"] != "balanced"):
        hits.append("combo_liver_gall")

    # combo_liver_gall_spleen_mass: gallbladder left_low + liver abnormal + spleen right_low
    if (gall["beforeStatus"] == "left_low"
            and liver["beforeStatus"] != "balanced"
            and spleen["beforeStatus"] == "right_low"):
        hits.append("combo_liver_gall_spleen_mass")

    # combo_multi_cross: cross count >= 3
    if gp["crossCount"] >= 3:
        hits.append("combo_multi_cross")

    return hits


# ---------------------------------------------------------------------------
# Step 6: calculate_raw_score  (deductions)
# ---------------------------------------------------------------------------

def _get_deduction(score_rules: dict, rule_id: str, default: float) -> float:
    """从 score_rules 获取扣减分值，如果不存在则使用默认值。"""
    for d in score_rules.get("deductions", []):
        if d.get("rule_id") == rule_id:
            return d.get("score", default)
    return default


def calculate_raw_score(
    meridian_states: Dict[str, dict],
    global_patterns: dict,
    combination_hits: List[str],
    score_rules: dict,
) -> Tuple[float, List[dict]]:
    """Step 6: compute raw score from 100 with deductions. Returns (score, breakdown)."""
    raw_score = 100.0
    breakdown: List[dict] = []

    # 从配置读取扣减分值（兼容旧配置）
    mild_deduction = _get_deduction(score_rules, "single_meridian_mild_abnormal", -2)
    obvious_deduction = _get_deduction(score_rules, "single_meridian_obvious_abnormal", -4)
    cross_deduction = _get_deduction(score_rules, "single_meridian_cross", -4)
    kidney_bladder_deduction = _get_deduction(score_rules, "kidney_bladder_double_cross", -8)
    multi_cross_deduction = _get_deduction(score_rules, "multi_cross", -8)
    right_bias_deduction = _get_deduction(score_rules, "right_bias", -6)
    left_bias_deduction = _get_deduction(score_rules, "left_bias", -6)
    heart_supply_deduction = _get_deduction(score_rules, "heart_supply_hit", -6)
    head_supply_deduction = _get_deduction(score_rules, "head_supply_hit", -6)
    neck_waist_deduction = _get_deduction(score_rules, "neck_waist_reproductive_hit", -5)
    mass_risk_deduction = _get_deduction(score_rules, "mass_risk_hit", -6)
    multi_imbalance_deduction = _get_deduction(score_rules, "multi_imbalance", -8)

    # Single meridian deductions
    for m, s in meridian_states.items():
        sev = s["severity"]
        if sev == "mild":
            raw_score += mild_deduction  # 加上负数等于减去
            breakdown.append({"rule": "single_meridian_mild_abnormal", "score": mild_deduction, "target": m})
        elif sev in ("medium", "high"):
            raw_score += obvious_deduction
            breakdown.append({"rule": "single_meridian_obvious_abnormal", "score": obvious_deduction, "target": m})
        if s["cross"]:
            raw_score += cross_deduction
            breakdown.append({"rule": "single_meridian_cross", "score": cross_deduction, "target": m})

    gp = global_patterns

    # Kidney + bladder double cross
    if meridian_states["kidney"]["cross"] and meridian_states["bladder"]["cross"]:
        raw_score += kidney_bladder_deduction
        breakdown.append({"rule": "kidney_bladder_double_cross", "score": kidney_bladder_deduction})

    # Multi cross
    if gp["crossCount"] >= 3:
        raw_score += multi_cross_deduction
        breakdown.append({"rule": "multi_cross", "score": multi_cross_deduction})

    # Right bias
    if gp["rightLowCountBefore"] >= 4 or gp["rightLowCountAfter"] >= 4:
        raw_score += right_bias_deduction
        breakdown.append({"rule": "right_bias", "score": right_bias_deduction})

    # Left bias
    if gp["leftLowCountBefore"] >= 4 or gp["leftLowCountAfter"] >= 4:
        raw_score += left_bias_deduction
        breakdown.append({"rule": "left_bias", "score": left_bias_deduction})

    # Combination hits
    if "combo_heart_supply" in combination_hits:
        raw_score += heart_supply_deduction
        breakdown.append({"rule": "heart_supply_hit", "score": heart_supply_deduction})

    if "combo_head_supply" in combination_hits:
        raw_score += head_supply_deduction
        breakdown.append({"rule": "head_supply_hit", "score": head_supply_deduction})

    if any(c in combination_hits for c in ("combo_neck", "combo_waist", "combo_reproductive")):
        raw_score += neck_waist_deduction
        breakdown.append({"rule": "neck_waist_reproductive_hit", "score": neck_waist_deduction})

    if "combo_liver_gall_spleen_mass" in combination_hits:
        raw_score += mass_risk_deduction
        breakdown.append({"rule": "mass_risk_hit", "score": mass_risk_deduction})

    # Multi imbalance: >= 4 meridians abnormal
    abnormal_count = sum(
        1 for s in meridian_states.values()
        if s["beforeStatus"] != "balanced" or s["afterStatus"] != "balanced"
    )
    if abnormal_count >= 4:
        raw_score += multi_imbalance_deduction
        breakdown.append({"rule": "multi_imbalance", "score": multi_imbalance_deduction})

    # Clamp
    min_score = score_rules.get("min_score", 30)
    max_score = score_rules.get("max_score", 100)
    raw_score = max(min_score, min(max_score, raw_score))

    return round(raw_score, 1), breakdown


# ---------------------------------------------------------------------------
# Step 7: apply_improvement_bonus
# ---------------------------------------------------------------------------

def _get_bonus(score_rules: dict, rule_id: str, default: float) -> float:
    """从 score_rules 获取加分值，如果不存在则使用默认值。"""
    for b in score_rules.get("bonuses", []):
        if b.get("rule_id") == rule_id:
            return b.get("score", default)
    return default


def apply_improvement_bonus(
    raw_score: float,
    meridian_states: Dict[str, dict],
    score_rules: dict,
) -> Tuple[float, dict]:
    """Step 7: add improvement bonuses. Returns (score, bonus_info)."""
    improved_count = sum(
        1 for s in meridian_states.values()
        if s["afterDiff"] < s["beforeDiff"]
    )

    # 从配置读取加分值（兼容旧配置）
    multi_improve_bonus = _get_bonus(score_rules, "multiple_meridians_improved", 4)
    partial_improve_bonus = _get_bonus(score_rules, "partial_improvement", 2)
    stable_bonus_value = _get_bonus(score_rules, "overall_stable", 3)

    bonus = 0
    rule_id = None
    if improved_count >= 3:
        bonus = multi_improve_bonus
        rule_id = "multiple_meridians_improved"
    elif improved_count >= 1:
        bonus = partial_improve_bonus
        rule_id = "partial_improvement"

    # Overall stable bonus
    cross_count = sum(1 for s in meridian_states.values() if s["cross"])
    abnormal_count = sum(
        1 for s in meridian_states.values()
        if s["beforeStatus"] != "balanced" or s["afterStatus"] != "balanced"
    )
    stable_bonus = 0
    if cross_count == 0 and abnormal_count <= 2:
        stable_bonus = stable_bonus_value

    total_bonus = bonus + stable_bonus
    new_score = raw_score + total_bonus

    min_score = score_rules.get("min_score", 30)
    max_score = score_rules.get("max_score", 100)
    new_score = max(min_score, min(max_score, new_score))

    bonus_info = {
        "improvedCount": improved_count,
        "improvementBonus": bonus,
        "improvementRule": rule_id,
        "stableBonus": stable_bonus,
        "totalBonus": total_bonus,
    }

    return round(new_score, 1), bonus_info


# ---------------------------------------------------------------------------
# Step 8: apply_followup_policy
# ---------------------------------------------------------------------------

def apply_followup_policy(
    raw_score: float,
    payload: dict,
    followup_policy: dict,
) -> Tuple[float, bool, bool]:
    """Step 8: apply follow-up score protection. Returns (displayedScore, scoreAdjustedByPolicy, adherenceFlag)."""
    session = payload.get("measurementSession") or {}
    score_ctx = payload.get("scoreContext") or {}

    is_followup = session.get("isFollowup", False)
    usage_days = session.get("instrumentUsageDaysBetweenMeasurements", 0)
    previous_score = score_ctx.get("previousDisplayedScore")

    min_days = followup_policy.get("minUsageDaysForProtection", 7)
    adherence_flag = usage_days >= min_days

    displayed_score = raw_score
    adjusted = False

    if (is_followup
            and previous_score is not None
            and adherence_flag
            and raw_score < previous_score):
        displayed_score = previous_score
        adjusted = True

    return round(displayed_score, 1), adjusted, adherence_flag


# ---------------------------------------------------------------------------
# Step 9: map_score_level
# ---------------------------------------------------------------------------

def map_score_level(score: float, score_rules: dict) -> Tuple[str, str]:
    """Step 9: map score to level and summary. Returns (level, summary)."""
    for level_def in score_rules.get("score_levels", []):
        if level_def["min"] <= score <= level_def["max"]:
            return level_def["level"], level_def["summary"]
    return "需重点关注", "当前失衡较明显，建议尽早重视。"


# ---------------------------------------------------------------------------
# Step 10: collect_advice_tags
# ---------------------------------------------------------------------------

def collect_advice_tags(meridian_states: Dict[str, dict], combination_hits: List[str]) -> List[str]:
    """Step 10: generate advice tags from meridian states and combination hits."""
    tags: List[str] = []

    if meridian_states["stomach"]["beforeStatus"] == "right_low":
        tags.append("stomach_cold")
    if meridian_states["spleen"]["beforeStatus"] == "right_low":
        tags.append("spleen_damp")
    if meridian_states["kidney"]["beforeStatus"] == "right_low":
        tags.append("kidney_yang_weak")
    if meridian_states["liver"]["beforeStatus"] == "right_low":
        tags.append("liver_blood_weak")
    if meridian_states["gallbladder"]["beforeStatus"] != "balanced":
        tags.append("gallbladder_metabolism_pressure")
    if "combo_heart_supply" in combination_hits:
        tags.append("heart_supply_attention")
    if "combo_head_supply" in combination_hits:
        tags.append("head_supply_attention")
    if "combo_reproductive" in combination_hits:
        tags.append("reproductive_system_attention")

    return tags


# ---------------------------------------------------------------------------
# Step 11-12: build output
# ---------------------------------------------------------------------------

def build_meridian_label(state: str, meridian_config: dict) -> str:
    """Get the label for a meridian state from meridian_rules config."""
    if state == "balanced":
        return "相对平衡"
    mapping = meridian_config.get(state, {})
    return mapping.get("label", state)


def get_meridian_points(state: str, meridian_config: dict) -> List[str]:
    """Get the risk points for a meridian state."""
    if state == "balanced":
        return []
    mapping = meridian_config.get(state, {})
    return mapping.get("points", [])


def build_final_output(
    payload: dict,
    meridian_states: Dict[str, dict],
    global_patterns: dict,
    combination_hits: List[str],
    raw_score: float,
    displayed_score: float,
    score_level: str,
    score_summary: str,
    score_adjusted: bool,
    adherence_flag: bool,
    advice_tags: List[str],
    score_breakdown: List[dict],
    bonus_info: dict,
    meridian_rules_config: dict,
    score_rules: dict,
) -> dict:
    """Steps 11-12: assemble final output structure."""
    session = payload.get("measurementSession") or {}
    subject = payload.get("subject") or {}
    ms = payload["measurements"]

    # Lowest meridians
    lowest_before = find_lowest_meridian(ms["before"])
    lowest_after = find_lowest_meridian(ms["after"])

    # Build meridian details for report
    meridian_details = []
    meridian_names = {
        "liver": "肝经", "spleen": "脾经", "kidney": "肾经",
        "stomach": "胃经", "gallbladder": "胆经", "bladder": "膀胱经",
    }
    for m in MERIDIANS:
        s = meridian_states[m]
        m_config = {}
        for rule in meridian_rules_config.get("rules", []):
            if rule.get("meridian_id") == m or rule.get("meridian") == m:
                m_config = rule
                break

        status_label = s["beforeStatus"]
        if s["cross"]:
            status_label = "交叉"
        elif s["beforeStatus"] == "balanced" and s["afterStatus"] == "balanced":
            status_label = "相对平衡"
        elif s["beforeStatus"] != "balanced":
            status_label = build_meridian_label(s["beforeStatus"], m_config)

        meridian_details.append({
            "meridian": meridian_names[m],
            "meridianId": m,
            "status": status_label,
            "severity": s["severity"],
            "cross": s["cross"],
            "beforeStatus": s["beforeStatus"],
            "afterStatus": s["afterStatus"],
            "riskPoints": get_meridian_points(s["beforeStatus"], m_config),
        })

    # Combination analysis for report
    combo_map = {
        "combo_heart_supply": "心脏供血需关注",
        "combo_head_supply": "头部供血需关注",
        "combo_waist": "腰椎相关问题需关注",
        "combo_neck": "颈椎相关问题需关注",
        "combo_reproductive": "生殖系统相关风险需重点关注",
        "combo_liver_gall": "肝胆代谢压力需关注",
        "combo_liver_gall_spleen_mass": "结节、囊肿、息肉方向需关注",
        "combo_multi_cross": "多经络交叉失衡需重点关注",
    }
    combination_analysis = [
        {"comboId": hit, "comboName": combo_map.get(hit, hit)}
        for hit in combination_hits
    ]

    # Focus meridians & stable meridians
    focus_meridians = [
        meridian_names[m] for m in MERIDIANS
        if meridian_states[m]["beforeStatus"] != "balanced" or meridian_states[m]["cross"]
    ]
    stable_meridians = [
        meridian_names[m] for m in MERIDIANS
        if meridian_states[m]["beforeStatus"] == "balanced"
        and meridian_states[m]["afterStatus"] == "balanced"
        and not meridian_states[m]["cross"]
    ]

    # Dominant pattern description
    dpb = global_patterns["dominantPatternBefore"]
    dpa = global_patterns["dominantPatternAfter"]
    cross_count = global_patterns["crossCount"]

    if cross_count >= 3:
        dominant_desc = "多经络交叉失衡"
    elif dpb == dpa:
        if dpb == "left_low":
            dominant_desc = "整体偏左"
        elif dpb == "right_low":
            dominant_desc = "整体偏右"
        else:
            dominant_desc = "左右相对平衡"
    else:
        dominant_desc = f"前后两组左右偏向变化较明显（第一组{dpb}，第二组{dpa}）"

    # Build overall assessment
    if score_level == "整体状态较好":
        overall_level = "整体相对平稳"
    elif score_level == "轻度失衡":
        overall_level = "整体存在一定失衡"
    elif score_level == "中度失衡":
        overall_level = "存在较明确失衡"
    else:
        overall_level = "失衡较明显"

    return {
        "engine": {"mode": "rule-based-v2", "version": "2.0"},
        "subject": subject,

        # Engine layer (for debug/review)
        "engineInference": {
            "dominantPatternBefore": dpb,
            "dominantPatternAfter": dpa,
            "lowestMeridianBefore": lowest_before,
            "lowestMeridianAfter": lowest_after,
            "meridianStates": meridian_states,
            "combinationHits": combination_hits,
        },

        # Score context
        "scoreContext": {
            "currentRawScore": raw_score,
            "displayedScore": displayed_score,
            "scoreLevel": score_level,
            "scoreSummary": score_summary,
            "instrumentUsageDaysBetweenMeasurements": session.get("instrumentUsageDaysBetweenMeasurements", 0),
            "adherenceFlag": adherence_flag,
            "scoreAdjustedByPolicy": score_adjusted,
        },

        # Report payload (for frontend display)
        "healthScore": {
            "score": displayed_score,
            "level": score_level,
            "summary": score_summary,
        },
        "overallAssessment": {
            "overallLevel": overall_level,
            "dominantPattern": dominant_desc,
            "focusMeridians": focus_meridians,
            "stableMeridians": stable_meridians,
        },
        "meridianDetails": meridian_details,
        "combinationAnalysis": combination_analysis,
        "adviceTags": advice_tags,

        # Backward-compatible fields
        "healthScoreValue": displayed_score,

        # Trace (debug only)
        "trace": {
            "scoreBreakdown": score_breakdown,
            "improvementBonus": bonus_info,
            "globalPatterns": global_patterns,
        },
    }


# ---------------------------------------------------------------------------
# Main infer function
# ---------------------------------------------------------------------------

def infer(payload: dict, thresholds: dict, meridian_rules: dict,
          combo_rules: dict, score_rules: dict, followup_policy: dict) -> dict:
    """Run the full inference pipeline (Steps 1-12)."""
    # Step 2
    validate_input(payload)

    # Step 3
    meridian_states = compute_meridian_states(payload, score_rules)

    # Step 4
    global_patterns = compute_global_patterns(meridian_states)

    # Step 5
    combination_hits = apply_combination_rules(meridian_states, global_patterns, combo_rules)

    # Step 6
    raw_score, score_breakdown = calculate_raw_score(
        meridian_states, global_patterns, combination_hits, score_rules,
    )

    # Step 7
    raw_score, bonus_info = apply_improvement_bonus(raw_score, meridian_states, score_rules)

    # Step 8
    displayed_score, score_adjusted, adherence_flag = apply_followup_policy(
        raw_score, payload, followup_policy,
    )

    # Step 9
    score_level, score_summary = map_score_level(displayed_score, score_rules)

    # Step 10
    advice_tags = collect_advice_tags(meridian_states, combination_hits)

    # Steps 11-12
    return build_final_output(
        payload=payload,
        meridian_states=meridian_states,
        global_patterns=global_patterns,
        combination_hits=combination_hits,
        raw_score=raw_score,
        displayed_score=displayed_score,
        score_level=score_level,
        score_summary=score_summary,
        score_adjusted=score_adjusted,
        adherence_flag=adherence_flag,
        advice_tags=advice_tags,
        score_breakdown=score_breakdown,
        bonus_info=bonus_info,
        meridian_rules_config=meridian_rules,
        score_rules=score_rules,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="infer.py", description="TCM Meridian Inference Engine v2.0")
    ap.add_argument("input", nargs="?", help="Input JSON file (see fixtures/v2/*.json)")
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
    thresholds, meridian_rules, combo_rules, score_rules, followup_policy = load_rules(rules_dir)
    result = infer(payload, thresholds, meridian_rules, combo_rules, score_rules, followup_policy)

    text = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)
    if args.out:
        out_path = (project_root / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
    else:
        try:
            print(text)
        except BrokenPipeError:
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
