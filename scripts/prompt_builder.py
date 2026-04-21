#!/usr/bin/env python3
"""Build system and user prompts for the DeepSeek agent."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"

MERIDIAN_NAMES_ZH = {
    "liver": "肝经",
    "spleen": "脾经",
    "kidney": "肾经",
    "stomach": "胃经",
    "gallbladder": "胆经",
    "bladder": "膀胱经",
}


def build_system_prompt(
    thresholds: dict[str, Any],
    meridian_rules: dict[str, Any],
    combo_rules: dict[str, Any],
) -> str:
    """Read the system prompt template and inject rule context."""
    template = (PROMPTS_DIR / "system_prompt.md").read_text(encoding="utf-8")

    thresholds_ctx = (
        "### 阈值参数\n```json\n"
        + json.dumps(thresholds["temperature"], ensure_ascii=False, indent=2)
        + "\n```"
    )

    rules_lines = []
    for rule in meridian_rules.get("rules", []):
        mid = rule.get("meridian_id") or rule.get("meridian", "")
        name = MERIDIAN_NAMES_ZH.get(mid, mid)
        mname = rule.get("meridian_name", name)
        # v2 structure: per-meridian with left_low/right_low/cross sub-objects
        for status_key in ("left_low", "right_low", "cross"):
            sub = rule.get(status_key, {})
            if sub:
                label = sub.get("label", status_key)
                points = ", ".join(sub.get("points", []))
                rules_lines.append(f"- **{mname} {label}**: 风险点: [{points}]")
    meridian_ctx = "### 单经判症规则\n" + "\n".join(rules_lines)

    combo_lines = []
    for rule in combo_rules.get("rules", []):
        output = rule.get("output", {})
        title = output.get("title", rule.get("rule_name", ""))
        desc = output.get("description", "")
        combo_lines.append(f"- **{title}**: {desc}")
    combo_ctx = "### 组合判症规则\n" + "\n".join(combo_lines)

    return (
        template
        .replace("{thresholds_context}", thresholds_ctx)
        .replace("{meridian_rules_context}", meridian_ctx)
        .replace("{combination_rules_context}", combo_ctx)
    )


def build_user_prompt(
    payload: dict[str, Any],
    rule_engine_result: dict[str, Any],
) -> str:
    """Build the user prompt with pre-computed features and rule engine result.

    The hybrid approach sends the rule engine's deterministic output so that
    DeepSeek only needs to generate natural language, not re-do calculations.
    """
    subject = payload.get("subject", {})
    measurements = payload.get("measurements", {})

    lines = ["请基于以下经络测量数据和规则引擎推理结果，生成自然语言分析报告。", ""]

    # Raw measurements (v2: before/after format)
    lines.append("## 原始测量数据")
    if "before" in measurements and "after" in measurements:
        for phase in ("before", "after"):
            label = "第一组" if phase == "before" else "第二组"
            lines.append(f"### {label}")
            for meridian, vals in measurements[phase].items():
                name = MERIDIAN_NAMES_ZH.get(meridian, meridian)
                left = vals.get("left", "?")
                right = vals.get("right", "?")
                lines.append(f"- {name}: 左 {left}°C, 右 {right}°C")
    else:
        for meridian, vals in measurements.items():
            name = MERIDIAN_NAMES_ZH.get(meridian, meridian)
            left = vals.get("left", "?")
            right = vals.get("right", "?")
            lines.append(f"- {name}: 左 {left}°C, 右 {right}°C")
    lines.append("")

    # Engine results (v2 structure)
    lines.append("## 规则引擎推理结果（已确定，请基于此生成文案）")
    hs = rule_engine_result.get("healthScore", {})
    score = hs.get("score", "?") if isinstance(hs, dict) else hs
    level = hs.get("level", "?") if isinstance(hs, dict) else ""
    lines.append(f"- 健康评分: {score} ({level})")

    # Meridian details (v2: meridianDetails array)
    meridian_details = rule_engine_result.get("meridianDetails", [])
    if meridian_details:
        for md in meridian_details:
            name = md.get("meridian", "?")
            status = md.get("status", "?")
            severity = md.get("severity", "?")
            cross = md.get("cross", False)
            cross_str = ", 交叉" if cross else ""
            risk_pts = ", ".join(md.get("riskPoints", []))
            lines.append(f"- {name}: {status} (severity={severity}{cross_str}), 风险: [{risk_pts}]")

    # Combination analysis
    combos = rule_engine_result.get("combinationAnalysis", [])
    if combos:
        lines.append("- 组合判症:")
        for c in combos:
            lines.append(f"  - {c.get('comboName', '')}")

    # Overall assessment
    oa = rule_engine_result.get("overallAssessment", {})
    if oa:
        lines.append(f"- 整体判断: {oa.get('overallLevel', '')}")
        lines.append(f"- 偏向: {oa.get('dominantPattern', '')}")
        focus = oa.get("focusMeridians", [])
        if focus:
            lines.append(f"- 重点经络: {', '.join(focus)}")
        stable = oa.get("stableMeridians", [])
        if stable:
            lines.append(f"- 平衡经络: {', '.join(stable)}")

    # Advice tags
    advice_tags = rule_engine_result.get("adviceTags", [])
    if advice_tags:
        lines.append(f"- 建议标签: {', '.join(advice_tags)}")

    if subject:
        lines.append(f"\nsubject: {json.dumps(subject, ensure_ascii=False)}")

    lines.append("")
    lines.append("请输出纯 JSON，不要包含 markdown 代码块标记。")

    return "\n".join(lines)
