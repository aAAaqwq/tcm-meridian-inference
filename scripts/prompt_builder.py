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
        name = MERIDIAN_NAMES_ZH.get(rule["meridian"], rule["meridian"])
        rules_lines.append(
            f"- **{name} {rule['status']}**: {rule.get('summary', '')}"
            f"  症状: {', '.join(rule.get('symptoms', []))}"
        )
    meridian_ctx = "### 单经判症规则\n" + "\n".join(rules_lines)

    combo_lines = []
    for rule in combo_rules.get("rules", []):
        combo_lines.append(
            f"- **{rule.get('name', '')}**: {rule.get('summary', '')}"
        )
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

    lines.append("## 原始测量数据")
    for meridian, vals in measurements.items():
        name = MERIDIAN_NAMES_ZH.get(meridian, meridian)
        left = vals.get("left", "?")
        right = vals.get("right", "?")
        lines.append(f"- {name}: 左 {left}°C, 右 {right}°C")
    lines.append("")

    lines.append("## 规则引擎推理结果（已确定，请基于此生成文案）")
    lines.append(f"- 健康评分: {rule_engine_result.get('healthScore', '?')}")

    meridians = rule_engine_result.get("meridians", {})
    for m, info in meridians.items():
        name = MERIDIAN_NAMES_ZH.get(m, m)
        status = info.get("status", "stable")
        score = info.get("score", "?")
        symptoms = ", ".join(info.get("symptoms", []))
        lines.append(f"- {name}: status={status}, score={score}, symptoms=[{symptoms}]")

    combos = rule_engine_result.get("combinations", [])
    if combos:
        lines.append("- 组合判症:")
        for c in combos:
            lines.append(f"  - {c.get('name', '')}: {c.get('summary', '')}")

    risk_tags = rule_engine_result.get("riskTags", [])
    if risk_tags:
        lines.append(f"- 风险标签: {', '.join(risk_tags)}")

    if subject:
        lines.append(f"\nsubject: {json.dumps(subject, ensure_ascii=False)}")

    lines.append("")
    lines.append("请输出纯 JSON，不要包含 markdown 代码块标记。")

    return "\n".join(lines)
