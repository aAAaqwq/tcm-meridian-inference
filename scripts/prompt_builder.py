#!/usr/bin/env python3
"""Build system and user prompts for the DeepSeek agent - v3 Mulinsen Edition.

Supports the new v3 inference engine output format based on PRD:
docs/sources/mulinsen-report-inference-flow.md
"""

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

TREND_NAMES_ZH = {
    "stable_left_low": "两组均左低",
    "stable_right_low": "两组均右低",
    "cross": "两组左右方向相反（交叉）",
    "stable_balanced": "两组均平衡",
    "potential_symptom": "潜在症状问题（第一组平衡，第二组异常）",
    "fast_response": "调理反应较快（第一组异常，第二组恢复平衡）",
}

DIFF_LEVEL_NAMES_ZH = {
    "balanced": "平衡",
    "mild_sub_health": "有一定亚健康",
    "health_problem": "有健康问题",
    "serious_problem": "有比较严重的问题",
}


def build_system_prompt() -> str:
    """Read the system prompt template."""
    template = (PROMPTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
    return template


def build_user_prompt(
    payload: dict[str, Any],
    rule_engine_result: dict[str, Any],
) -> str:
    """Build the user prompt with v3 inference engine result.

    The v3 format follows the PRD structure with:
    - score_result (score, score_raw, problem_index, problem_index_detail)
    - lowest_points (selected lowest 2 points from group2)
    - side_bias_summary (left_low_count, right_low_count, result)
    - cervical_lumbar_result (kidney_trend, bladder_trend, result)
    - meridian_analysis (detailed per-meridian analysis)
    - focus_issues (prioritized focus issues, 3-4 items)
    """
    measurement_type = payload.get("measurement_type", "first_test")
    gender = payload.get("gender", "unknown")
    meridians = payload.get("meridians", {})

    lines = [
        "请基于以下经络测量数据和规则引擎推理结果，生成自然语言分析报告。",
        "",
        "## 基础信息",
        f"- 检测类型: {'首次检测' if measurement_type == 'first_test' else '复测'}",
        f"- 性别: {'女性' if gender == 'female' else '男性' if gender == 'male' else '未知'}",
        "",
    ]

    # 原始测量数据 (v3: group1/group2 format)
    lines.append("## 原始测量数据")
    for group_name, group_label in [("group1", "第一组（使用仪器5分钟时测量）"), ("group2", "第二组（使用仪器20分钟时测量）")]:
        lines.append(f"### {group_label}")
        for meridian in ["stomach", "gallbladder", "bladder", "liver", "spleen", "kidney"]:
            if meridian in meridians:
                vals = meridians[meridian]
                name = MERIDIAN_NAMES_ZH.get(meridian, meridian)
                left = vals.get(f"{group_name}_left", "?")
                right = vals.get(f"{group_name}_right", "?")
                lines.append(f"- {name}: 左 {left}°C, 右 {right}°C")
        lines.append("")

    # 规则引擎推理结果
    lines.append("## 规则引擎推理结果（已确定，请基于此生成文案）")
    lines.append("")

    # 评分结果
    score_result = rule_engine_result.get("score_result", {})
    score = score_result.get("score", "?")
    problem_index = score_result.get("problem_index", "?")
    lines.append(f"### 综合健康分")
    lines.append(f"- 展示分数: {score}")
    lines.append(f"- 内部问题指数 I: {problem_index}")
    lines.append("")

    # 问题指数详情
    detail = score_result.get("problem_index_detail", {})
    lines.append(f"### 问题指数 breakdown")
    lines.append(f"- A 低温指数: {detail.get('low_temperature_index', '?')}")
    lines.append(f"- B 温差指数: {detail.get('temperature_difference_index', '?')}")
    lines.append(f"- C 偏侧指数: {detail.get('side_bias_index', '?')}")
    lines.append(f"- D 趋势指数: {detail.get('trend_index', '?')}")
    lines.append(f"- E 组合指数: {detail.get('combo_index', '?')}")
    lines.append("")

    # 第二组最低两点
    lowest_points = rule_engine_result.get("lowest_points", {})
    selected = lowest_points.get("selected", [])
    if selected:
        lines.append(f"### 第二组温度最低的两个点（必讲项）")
        for lp in selected:
            m_name = MERIDIAN_NAMES_ZH.get(lp.get("meridian"), lp.get("meridian", "?"))
            lines.append(f"- 排名 {lp.get('rank')}: {m_name} {lp.get('side') == 'left' and '左侧' or '右侧'} {lp.get('value')}°C")
        lines.append("")

    # 左右偏向统计
    side_bias = rule_engine_result.get("side_bias_summary", {})
    lines.append(f"### 第二组左右偏向统计")
    lines.append(f"- 左低经络数: {side_bias.get('left_low_count', '?')}")
    lines.append(f"- 右低经络数: {side_bias.get('right_low_count', '?')}")
    lines.append(f"- 平衡经络数: {side_bias.get('balanced_count', '?')}")
    if side_bias.get("result") == "head_blood_supply_attention":
        lines.append(f"- 偏向判断: 整体偏左较明显，提示头部供血方向需关注")
    elif side_bias.get("result") == "heart_attention":
        lines.append(f"- 偏向判断: 整体偏右较明显，提示循环及心脏供血方向需关注")
    lines.append("")

    # 颈椎/腰椎判断
    cervical_lumbar = rule_engine_result.get("cervical_lumbar_result", {})
    if cervical_lumbar.get("result") != "none":
        lines.append(f"### 颈椎/腰椎判断（基于肾经+膀胱经趋势）")
        lines.append(f"- 肾经趋势: {TREND_NAMES_ZH.get(cervical_lumbar.get('kidney_trend'), cervical_lumbar.get('kidney_trend', '?'))}")
        lines.append(f"- 膀胱经趋势: {TREND_NAMES_ZH.get(cervical_lumbar.get('bladder_trend'), cervical_lumbar.get('bladder_trend', '?'))}")
        result_map = {
            "cervical": "颈椎问题",
            "lumbar": "腰椎问题",
            "cervical_and_lumbar": "颈椎和腰椎问题同时存在",
        }
        lines.append(f"- 判断结果: {result_map.get(cervical_lumbar.get('result'), '?')}")
        lines.append("")

    # 经络详细分析
    meridian_analysis = rule_engine_result.get("meridian_analysis", [])
    if meridian_analysis:
        lines.append(f"### 六条经络详细分析")
        for ma in meridian_analysis:
            name = ma.get("meridian_name", "?")
            trend = ma.get("trend", "?")
            g2_diff = ma.get("group2_diff", "?")
            g2_level = ma.get("group2_diff_level", "?")
            is_focus = ma.get("is_focus", False)

            lines.append(f"\n**{name}** {'[重点关注]' if is_focus else ''}")
            lines.append(f"- 趋势: {TREND_NAMES_ZH.get(trend, trend)}")
            lines.append(f"- 第二组温差: {g2_diff}°C ({DIFF_LEVEL_NAMES_ZH.get(g2_level, g2_level)})")

            if ma.get("diff_change") == "worsened":
                lines.append(f"- 温差变化: 问题更突出 / 左右差异变大")
            elif ma.get("diff_change") == "improved":
                lines.append(f"- 温差变化: 问题有所好转 / 左右差异缩小")

            matched_rules = ma.get("matched_rules", [])
            if matched_rules:
                lines.append(f"- 匹配到的问题: {', '.join(matched_rules)}")

            focus_reason = ma.get("focus_reason", [])
            if focus_reason:
                reason_map = {
                    "second_group_lowest_point": "是第二组最低点之一",
                    "group2_diff_health_problem": "第二组温差有健康问题",
                    "group2_diff_serious_problem": "第二组温差有严重问题",
                    "diff_worsened": "温差恶化",
                    "side_bias_participant": "参与整体偏侧统计",
                }
                reasons = [reason_map.get(r, r) for r in focus_reason]
                lines.append(f"- 重点关注原因: {'; '.join(reasons)}")
        lines.append("")

    # 本次重点关注的问题
    focus_issues = rule_engine_result.get("focus_issues", [])
    if focus_issues:
        lines.append(f"### 本次重点关注的问题（已按优先级排序）")
        for issue in focus_issues:
            priority = issue.get("priority", "?")
            title = issue.get("title", "?")
            lines.append(f"\n{priority}. {title}")

            if issue.get("type") == "lowest_point":
                m_name = issue.get("meridian_name", "?")
                lines.append(f"   - 相关经络: {m_name}")

            if issue.get("left_low_count"):
                lines.append(f"   - 左低经络数: {issue.get('left_low_count')}")
            if issue.get("right_low_count"):
                lines.append(f"   - 右低经络数: {issue.get('right_low_count')}")
        lines.append("")

    # 复测详情
    if measurement_type == "retest":
        retest_detail = rule_engine_result.get("retest_detail", {})
        if retest_detail:
            lines.append(f"### 复测评分详情")
            lines.append(f"- 测试次数: 第{retest_detail.get('test_number', '?')}次检测")
            lines.append(f"- 测试次数加分: +{retest_detail.get('test_bonus', '?')}")
            lines.append(f"- 使用天数: {retest_detail.get('usage_days', '?')}")
            lines.append(f"- 问题指数变化 (ΔI): {retest_detail.get('delta_I', '?')}")
            lines.append(f"- 数据改善加分: +{retest_detail.get('improvement_bonus', '?')}")
            lines.append(f"- 上次数值: 分数 {retest_detail.get('previous_score', '?')}, 问题指数 {retest_detail.get('previous_problem_index', '?')}")
            lines.append("")

    # AI 生成约束
    lines.extend([
        "## AI 生成约束",
        "",
        "### 你可以做的",
        "- 合并重复问题，调整语言顺序",
        "- 把规则结果改写成用户能看懂的话",
        "- 根据已判定问题生成调理建议",
        "- 适度弱化疾病诊断感",
        "",
        "### 你不能做的",
        "- 不能新增规则库中没有的问题",
        "- 不能新增未被数据触发的问题",
        "- 不能输出药物建议",
        "- 不能替代医生诊断",
    ])

    if gender == "male":
        lines.append("- 不能输出女性专属表达（宫寒、子宫、例假、人流、剖腹产、子宫肌瘤等）")
    elif gender == "female":
        lines.append("- 不能输出男性专属表达（前列腺、前列腺炎、前列腺钙化等）")
    else:
        lines.append("- 性别未知，只保留中性表达（生殖系统、泌尿系统、腹部手术史等），不出现男/女专属疾病")

    lines.append("- 不能把平衡经络强行说成有问题")
    lines.append("")
    lines.append("请输出纯 JSON，不要包含 markdown 代码块标记。")

    return "\n".join(lines)
