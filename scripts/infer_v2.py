#!/usr/bin/env python3
"""TCM Meridian Inference Engine v3.0 - Mulinsen Report Edition

Implements the scoring algorithm defined in docs/sources/mulinsen-report-inference-flow.md.
Based on group1(5min)/group2(20min) measurement model with problem index calculation.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MERIDIANS = ["stomach", "gallbladder", "bladder", "liver", "spleen", "kidney"]

MERIDIAN_NAMES = {
    "stomach": "胃经",
    "gallbladder": "胆经",
    "bladder": "膀胱经",
    "liver": "肝经",
    "spleen": "脾经",
    "kidney": "肾经",
}

TREND_TYPES = {
    "stable_left_low": "两组均左低",
    "stable_right_low": "两组均右低",
    "cross": "两组左右方向相反",
    "stable_balanced": "两组均平衡",
    "potential_symptom": "潜在症状问题",
    "fast_response": "调理反应较快",
}

DIFF_LEVELS = {
    "balanced": "平衡",
    "mild_sub_health": "有一定亚健康",
    "health_problem": "有健康问题",
    "serious_problem": "有比较严重的问题",
}

# ============================================================================
# 模板化建议 (Rule模式)
# ============================================================================

# 分数等级对应的话术
SCORE_LEVEL_TEMPLATES = {
    "excellent": {
        "summary": "恭喜！本次检测显示您的综合健康分{score}分，属于健康优秀水平。六条经络温度平衡，无明显失衡点，整体气血运行良好。建议继续保持规律作息和健康饮食，定期复测维护健康状态。",
        "headline": "整体状态良好，继续保持",
        "talk_track": [
            "您的六条经络温度平衡，气血运行顺畅，这是一个非常好的状态。",
            "建议继续保持当前的作息和饮食习惯，定期复测以维护健康。"
        ],
        "retest_prompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
    },
    "good": {
        "summary": "本次检测显示您的综合健康分{score}分，属于轻度失衡状态。整体经络状态良好，但存在轻微不平衡。建议通过调整饮食和作息来改善。",
        "headline": "整体良好，注意调理",
        "talk_track": [
            "您的经络整体状态不错，大部分经络都处于平衡状态。",
            "只是有轻微的不平衡，通过简单的饮食和作息调整就能改善。"
        ],
        "retest_prompt": "建议1-2个月后复测，观察调理效果。"
    },
    "moderate": {
        "summary": "本次检测显示您的综合健康分{score}分，属于中度失衡状态。主要问题集中在{focus_meridians}，提示相关脏腑功能需要关注。建议系统调理，改善亚健康状态。",
        "headline": "{focus_meridians}需重点关注",
        "talk_track": [
            "您的检测结果显示，{focus_meridians}问题比较突出，这可能影响相关脏腑功能。",
            "整体健康分{score}分，属于中度失衡，需要通过系统调理来改善。"
        ],
        "retest_prompt": "建议调理2-4周后复测，观察改善情况。"
    },
    "significant": {
        "summary": "本次检测显示您的综合健康分{score}分，属于明显失衡状态。{focus_meridians}等多个经络存在明显问题，提示身体处于亚健康状态。建议重点关注，及时进行系统调理。",
        "headline": "{focus_meridians}问题需紧急关注",
        "talk_track": [
            "您的检测结果显示，{focus_meridians}等多个经络问题比较突出。",
            "整体健康分{score}分，属于明显失衡状态，需要重点关注和调理。"
        ],
        "retest_prompt": "建议坚持调理2-3周后复测，密切观察改善情况。"
    }
}

# 经络对应的建议
MERIDIAN_ADVICE = {
    "stomach": {
        "title": "胃经",
        "issues": ["消化", "食欲", "胃部不适"],
        "recommendations": [
            "饮食规律，三餐定时，避免暴饮暴食和生冷食物。",
            "多吃易消化食物如小米粥、山药、南瓜等。",
            "避免辛辣刺激食物，减少咖啡、浓茶摄入。"
        ]
    },
    "gallbladder": {
        "title": "胆经",
        "issues": ["胆囊", "决断力", "偏头痛"],
        "recommendations": [
            "避免油腻和高胆固醇食物，多吃蔬菜水果。",
            "保持心情舒畅，避免过度思虑和压力。",
            "适当进行头部按摩，缓解偏头痛症状。"
        ]
    },
    "bladder": {
        "title": "膀胱经",
        "issues": ["腰背", "排尿", "排毒"],
        "recommendations": [
            "注意腰部保暖，避免久坐，适当进行腰背拉伸。",
            "多饮水，保持正常排尿，促进代谢废物排出。",
            "可进行膀胱经穴位按摩或温敷。"
        ]
    },
    "liver": {
        "title": "肝经",
        "issues": ["代谢", "情绪", "眼睛"],
        "recommendations": [
            "保持规律作息，尽量在23点前入睡，利于肝脏代谢。",
            "保持情绪舒畅，避免过度愤怒和压力。",
            "多吃绿色蔬菜，适当饮用菊花枸杞茶。"
        ]
    },
    "spleen": {
        "title": "脾经",
        "issues": ["消化", "湿气", "四肢乏力"],
        "recommendations": [
            "少吃生冷油腻食物，多吃健脾祛湿食材如薏米、山药、红豆。",
            "适当进行有氧运动，促进气血运行。",
            "避免过度思虑，保持心情舒畅。"
        ]
    },
    "kidney": {
        "title": "肾经",
        "issues": ["精力", "腰膝", "听力"],
        "recommendations": [
            "注意腰部和脚部保暖，避免受寒。",
            "多吃黑色食物如黑芝麻、黑豆、枸杞等补肾食材。",
            "避免过度劳累和熬夜，保证充足睡眠。"
        ]
    }
}

# 偏侧问题建议
SIDE_BIAS_ADVICE = {
    "head_blood_supply_attention": {
        "title": "头部供血需关注",
        "recommendations": [
            "注意头部保暖，避免冷风直吹。",
            "适当进行颈部按摩和热敷。",
            "保持充足睡眠，避免过度劳累。"
        ]
    },
    "heart_attention": {
        "title": "心脏方向需关注",
        "recommendations": [
            "保持情绪平稳，避免过度激动。",
            "适当进行有氧运动，增强心肺功能。",
            "避免剧烈运动和过度劳累。"
        ]
    }
}

# 颈椎/腰椎建议
CERVICAL_LUMBAR_ADVICE = {
    "cervical": {
        "title": "颈椎问题",
        "recommendations": [
            "保持正确坐姿，避免长时间低头。",
            "每小时起身活动，做颈部放松运动。",
            "可使用热敷或理疗缓解颈部不适。"
        ]
    },
    "lumbar": {
        "title": "腰椎问题",
        "recommendations": [
            "注意腰部保暖，避免久坐久站。",
            "适当进行腰背肌肉锻炼。",
            "避免提重物和腰部受凉。"
        ]
    },
    "cervical_and_lumbar": {
        "title": "颈椎+腰椎问题",
        "recommendations": [
            "保持正确姿势，避免长时间保持同一姿势。",
            "适当进行脊柱伸展运动。",
            "注意颈腰部保暖，可配合理疗调理。"
        ]
    }
}

# 复测建议模板
RETEST_TEMPLATES = {
    "improved": {
        "summary": "恭喜！本次复测显示您的健康状况有明显改善，综合健康分从{previous_score}提升至{score}分。说明之前的调理方向正确，建议继续坚持。",
        "headline": "调理见效，继续保持",
        "talk_track": [
            "太好了！您的健康分从{previous_score}分提升到了{score}分，调理效果非常明显。",
            "这说明我们的调理方向是对的，您的配合也很好，建议继续坚持。"
        ]
    },
    "stable": {
        "summary": "本次复测显示您的健康状况保持稳定，综合健康分{score}分。虽然变化不大，但也没有恶化，建议继续调理。",
        "headline": "状态稳定，持续调理",
        "talk_track": [
            "您的健康分保持在{score}分，状态比较稳定。",
            "调理需要时间，建议继续当前的方案，耐心等待改善。"
        ]
    },
    "worsened": {
        "summary": "本次复测显示您的健康状况需要加强关注，综合健康分{score}分。建议调整调理方案，加强针对性的调理措施。",
        "headline": "需要加强调理",
        "talk_track": [
            "本次检测显示您的健康分有所下降，需要加强关注。",
            "建议我们调整一下调理方案，加强针对性的措施。"
        ]
    }
}

def generate_rule_based_recommendations(
    display_score: int,
    focus_issues: list,
    side_bias: dict,
    cervical_lumbar_result: dict,
    measurement_type: str,
    previous_score: int = None,
) -> dict:
    """生成模板化的建议 (Rule模式)。"""

    # 确定分数等级
    if display_score >= 85:
        level = "excellent"
    elif display_score >= 80:
        level = "good"
    elif display_score >= 70:
        level = "moderate"
    else:
        level = "significant"

    # 提取重点经络
    focus_meridians = []
    for issue in focus_issues:
        if issue.get("type") == "lowest_point":
            meridian = issue.get("meridian")
            if meridian and meridian not in focus_meridians:
                focus_meridians.append(meridian)

    focus_meridian_names = "、".join([MERIDIAN_ADVICE[m]["title"] for m in focus_meridians[:2] if m in MERIDIAN_ADVICE])
    if not focus_meridian_names:
        focus_meridian_names = "多条经络"

    # 获取基础模板
    templates = SCORE_LEVEL_TEMPLATES[level]

    # 构建summary
    summary = templates["summary"].format(score=display_score, focus_meridians=focus_meridian_names)

    # 构建storefront
    storefront = {
        "focusHeadline": templates["headline"].format(focus_meridians=focus_meridian_names),
        "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
        "talkTrack": [t.format(score=display_score, focus_meridians=focus_meridian_names) for t in templates["talk_track"]],
        "retestPrompt": templates["retest_prompt"]
    }

    # 构建recommendations
    recommendations = []

    # 1. 添加重点经络建议
    for m in focus_meridians[:2]:
        if m in MERIDIAN_ADVICE:
            advice = MERIDIAN_ADVICE[m]
            recommendations.append(f"【{advice['title']}】{advice['recommendations'][0]}")

    # 2. 添加偏侧建议
    side_bias_result = side_bias.get("result")
    if side_bias_result in SIDE_BIAS_ADVICE:
        advice = SIDE_BIAS_ADVICE[side_bias_result]
        recommendations.append(f"【{advice['title']}】{advice['recommendations'][0]}")

    # 3. 添加颈椎/腰椎建议
    cl_result = cervical_lumbar_result.get("result")
    if cl_result in CERVICAL_LUMBAR_ADVICE:
        advice = CERVICAL_LUMBAR_ADVICE[cl_result]
        recommendations.append(f"【{advice['title']}】{advice['recommendations'][0]}")

    # 4. 添加通用建议
    recommendations.append("保持规律作息，避免熬夜，保证充足睡眠。")
    recommendations.append("适度运动，如散步、太极、瑜伽等，促进气血流通。")

    # 复测特殊处理
    if measurement_type == "retest" and previous_score is not None:
        diff = display_score - previous_score
        if diff >= 3:
            retest_template = RETEST_TEMPLATES["improved"]
        elif diff <= -3:
            retest_template = RETEST_TEMPLATES["worsened"]
        else:
            retest_template = RETEST_TEMPLATES["stable"]

        summary = retest_template["summary"].format(score=display_score, previous_score=previous_score)
        storefront["focusHeadline"] = retest_template["headline"]
        storefront["talkTrack"] = [t.format(score=display_score, previous_score=previous_score) for t in retest_template["talk_track"]]

    return {
        "summary": summary,
        "reportSummary": summary[:150] + "..." if len(summary) > 150 else summary,
        "storefront": storefront,
        "recommendations": recommendations[:6]  # 最多6条建议
    }


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_rules(rules_dir: Path) -> dict:
    """Load all rule configuration files."""
    meridian_rules = _load_json(rules_dir / "meridian_rules.json")
    return {"meridian_rules": meridian_rules}


# ============================================================================
# Step 1: 数据精度处理
# ============================================================================

def round_to_1dp(value: float) -> float:
    """所有温度值统一保留1位小数。"""
    return round(value, 1)


# ============================================================================
# Step 2: 基础计算规则
# ============================================================================

def get_side_status(left: float, right: float) -> Tuple[str, Optional[str], float]:
    """
    左右状态判断。
    只有左右数值完全相等才算平衡。只要相差0.1，也按低的一侧判断。

    Returns: (status, low_side, diff)
    - status: "left_low" | "right_low" | "balanced"
    - low_side: "left" | "right" | None
    - diff: 温差（保留1位小数）
    """
    left = round_to_1dp(left)
    right = round_to_1dp(right)

    if left == right:
        return "balanced", None, 0.0
    elif left < right:
        return "left_low", "left", round_to_1dp(right - left)
    else:
        return "right_low", "right", round_to_1dp(left - right)


def get_diff_level(diff: float) -> str:
    """
    温差等级判断。

    diff <= 0.2           → balanced
    0.2 < diff <= 0.5     → mild_sub_health
    0.5 < diff <= 2       → health_problem
    diff > 2              → serious_problem
    """
    if diff <= 0.2:
        return "balanced"
    elif diff <= 0.5:
        return "mild_sub_health"
    elif diff <= 2.0:
        return "health_problem"
    else:
        return "serious_problem"


def get_diff_change(group1_diff: float, group2_diff: float) -> str:
    """
    前后温差变化判断。

    group2_diff - group1_diff > 0.2   → worsened
    group1_diff - group2_diff > 0.2   → improved
    其他                               → unchanged
    """
    diff_delta = round_to_1dp(group2_diff - group1_diff)
    if diff_delta > 0.2:
        return "worsened"
    elif diff_delta < -0.2:
        return "improved"
    else:
        return "unchanged"


# ============================================================================
# Step 3: 经络趋势分析
# ============================================================================

def analyze_trend(
    group1_status: str, group2_status: str
) -> str:
    """
    分析经络整体趋势。

    stable_left_low:   两组均左低
    stable_right_low:  两组均右低
    cross:             两组左右方向相反
    stable_balanced:   两组均平衡
    potential_symptom: 第一组平衡，第二组左低/右低
    fast_response:     第一组左低/右低，第二组平衡
    """
    # 交叉判断
    if (group1_status in ("left_low", "right_low") and
        group2_status in ("left_low", "right_low") and
        group1_status != group2_status):
        return "cross"

    # 稳定左低
    if group1_status == "left_low" and group2_status == "left_low":
        return "stable_left_low"

    # 稳定右低
    if group1_status == "right_low" and group2_status == "right_low":
        return "stable_right_low"

    # 均平衡
    if group1_status == "balanced" and group2_status == "balanced":
        return "stable_balanced"

    # 潜在症状：第一组平衡，第二组异常
    if group1_status == "balanced" and group2_status in ("left_low", "right_low"):
        return "potential_symptom"

    # 快速恢复：第一组异常，第二组平衡
    if group1_status in ("left_low", "right_low") and group2_status == "balanced":
        return "fast_response"

    # 其他情况（理论上不应出现）
    return "stable_balanced"


# ============================================================================
# Step 4: 第二组最低两点分析
# ============================================================================

def find_lowest_two_points(group2_data: dict) -> Tuple[List[dict], List[dict]]:
    """
    从第二组12个温度值中找出最低的两个点。

    Returns:
    - selected: 最终选中的最低两点（每个点包含 meridian, side, value, rank, must_report）
    - tie_candidates: 并列候选点
    """
    # 收集所有点
    all_points = []
    for m in MERIDIANS:
        vals = group2_data[m]
        for side in ("left", "right"):
            value = round_to_1dp(vals[side])
            all_points.append({
                "meridian": m,
                "side": side,
                "value": value,
            })

    # 按温度排序
    all_points.sort(key=lambda x: x["value"])

    # 找到最低值和第二低值
    if len(all_points) < 2:
        return [], []

    lowest_value = all_points[0]["value"]
    second_lowest_value = None

    # 找出第二低的值（不同于最低值）
    for p in all_points[1:]:
        if p["value"] > lowest_value:
            second_lowest_value = p["value"]
            break

    # 如果没有第二低的值（所有值都相同），取第二个点
    if second_lowest_value is None:
        second_lowest_value = all_points[1]["value"]

    # 收集最低值的候选点
    lowest_candidates = [p for p in all_points if p["value"] == lowest_value]

    # 收集第二低值的候选点
    second_candidates = [p for p in all_points if p["value"] == second_lowest_value]

    selected = []
    tie_candidates = []

    # 处理最低点
    if len(lowest_candidates) == 1:
        selected.append({
            **lowest_candidates[0],
            "rank": 1,
            "must_report": True,
        })
    else:
        # 有并列，需要进一步筛选（暂时取第一个，后面结合其他规则筛选）
        selected.append({
            **lowest_candidates[0],
            "rank": 1,
            "must_report": True,
        })
        tie_candidates.extend(lowest_candidates[1:])

    # 处理第二低点
    if len(second_candidates) == 1:
        selected.append({
            **second_candidates[0],
            "rank": 2,
            "must_report": True,
        })
    else:
        # 有并列，需要进一步筛选
        # 排除已经在selected中的点
        remaining = [p for p in second_candidates
                     if not any(s["meridian"] == p["meridian"] and s["side"] == p["side"]
                               for s in selected)]
        if remaining:
            selected.append({
                **remaining[0],
                "rank": 2,
                "must_report": True,
            })
            tie_candidates.extend(remaining[1:])

    return selected, tie_candidates


# ============================================================================
# Step 5: 第二组左右偏向统计
# ============================================================================

def analyze_side_bias(group2_data: dict) -> dict:
    """
    统计第二组6条经络的左右偏向。

    Returns:
    - left_low_count: 左低经络数
    - right_low_count: 右低经络数
    - balanced_count: 平衡经络数
    - result: 判断结果（head_blood_supply_attention / heart_attention / none）
    """
    left_low_count = 0
    right_low_count = 0
    balanced_count = 0

    for m in MERIDIANS:
        vals = group2_data[m]
        status, _, _ = get_side_status(vals["left"], vals["right"])
        if status == "left_low":
            left_low_count += 1
        elif status == "right_low":
            right_low_count += 1
        else:
            balanced_count += 1

    # 判定结果
    result = "none"
    if left_low_count >= 4:
        result = "head_blood_supply_attention"
    elif right_low_count >= 4:
        result = "heart_attention"

    return {
        "left_low_count": left_low_count,
        "right_low_count": right_low_count,
        "balanced_count": balanced_count,
        "result": result,
    }


# ============================================================================
# Step 6: 肾经+膀胱经颈椎/腰椎判断
# ============================================================================

def analyze_cervical_lumbar(kidney_trend: str, bladder_trend: str) -> dict:
    """
    根据肾经和膀胱经的趋势判断颈椎/腰椎问题。

    规则：
    1. 相同低 → 腰椎问题
    2. 相反低 → 颈椎问题
    3. 任意一条整体平衡 → 不输出颈椎/腰椎问题
    4. 任意一条交叉 → 颈椎和腰椎问题同时存在
    5. potential_symptom / fast_response 暂不进入强颈椎/腰椎判断
    """
    # 任意一条平衡 → 不输出
    if kidney_trend == "stable_balanced" or bladder_trend == "stable_balanced":
        return {"result": "none", "kidney_trend": kidney_trend, "bladder_trend": bladder_trend}

    # 任意一条交叉 → 颈椎和腰椎同时存在
    if kidney_trend == "cross" or bladder_trend == "cross":
        return {"result": "cervical_and_lumbar", "kidney_trend": kidney_trend, "bladder_trend": bladder_trend}

    # potential_symptom / fast_response 暂不进入强判断
    if kidney_trend in ("potential_symptom", "fast_response") or \
       bladder_trend in ("potential_symptom", "fast_response"):
        return {"result": "none", "kidney_trend": kidney_trend, "bladder_trend": bladder_trend}

    # 相同低 → 腰椎问题
    if (kidney_trend == "stable_left_low" and bladder_trend == "stable_left_low") or \
       (kidney_trend == "stable_right_low" and bladder_trend == "stable_right_low"):
        return {"result": "lumbar", "kidney_trend": kidney_trend, "bladder_trend": bladder_trend}

    # 相反低 → 颈椎问题
    if (kidney_trend == "stable_left_low" and bladder_trend == "stable_right_low") or \
       (kidney_trend == "stable_right_low" and bladder_trend == "stable_left_low"):
        return {"result": "cervical", "kidney_trend": kidney_trend, "bladder_trend": bladder_trend}

    return {"result": "none", "kidney_trend": kidney_trend, "bladder_trend": bladder_trend}


# ============================================================================
# Step 7: 综合健康分算法 - 问题指数计算
# ============================================================================

def calculate_low_temperature_index(group2_data: dict) -> Tuple[float, dict]:
    """
    A: 低温指数

    计算：
    M = 第二组12个数据的中位数
    L = 第二组最低两个温度值的平均值
    低温差距 = M - L

    A取值：
    低温差距 <= 0.5℃        A = 0
    0.5℃ < 低温差距 <= 1℃   A = 1
    1℃ < 低温差距 <= 2℃     A = 3
    2℃ < 低温差距 <= 3℃     A = 5
    低温差距 > 3℃           A = 6
    """
    # 收集第二组所有12个温度值
    all_temps = []
    for m in MERIDIANS:
        vals = group2_data[m]
        all_temps.append(round_to_1dp(vals["left"]))
        all_temps.append(round_to_1dp(vals["right"]))

    # 计算中位数M
    M = round_to_1dp(statistics.median(all_temps))

    # 找出最低两个值的平均L
    sorted_temps = sorted(all_temps)
    L = round_to_1dp(sum(sorted_temps[:2]) / 2)

    # 低温差距
    gap = round_to_1dp(M - L)
    if gap < 0:
        gap = 0.0

    # 计算A
    if gap <= 0.5:
        A = 0.0
    elif gap <= 1.0:
        A = 1.0
    elif gap <= 2.0:
        A = 3.0
    elif gap <= 3.0:
        A = 5.0
    else:
        A = 6.0

    return A, {
        "median": M,
        "lowest_two_avg": L,
        "gap": gap,
        "value": A,
    }


def calculate_temperature_difference_index(
    meridian_analysis: List[dict]
) -> Tuple[float, dict]:
    """
    B: 温差指数

    每条经络根据第二组温差计算基础指数：
    第二组温差 <= 0.2℃         0
    0.2℃ < 第二组温差 <= 0.5℃  0.5
    0.5℃ < 第二组温差 <= 2℃    1.5
    第二组温差 > 2℃            3.5

    前后温差变化修正：
    第二组温差 - 第一组温差 > 0.2℃   +0.5
    第一组温差 - 第二组温差 > 0.2℃   -0.5
    其他                              0

    单经温差指数 = max(0, 基础指数 + 修正值)
    B = min(六条经络单经温差指数之和, 12)
    """
    per_meridian = []
    total = 0.0

    for m in meridian_analysis:
        group2_diff = m["group2_diff"]
        diff_change = m["diff_change"]

        # 基础指数
        if group2_diff <= 0.2:
            base = 0.0
        elif group2_diff <= 0.5:
            base = 0.5
        elif group2_diff <= 2.0:
            base = 1.5
        else:
            base = 3.5

        # 修正值
        if diff_change == "worsened":
            adjustment = 0.5
        elif diff_change == "improved":
            adjustment = -0.5
        else:
            adjustment = 0.0

        # 单经温差指数
        single_index = max(0.0, base + adjustment)

        per_meridian.append({
            "meridian": m["meridian"],
            "base": base,
            "adjustment": adjustment,
            "single_index": single_index,
        })

        total += single_index

    # 封顶
    B = min(total, 12.0)

    return B, {
        "per_meridian": per_meridian,
        "total_before_cap": total,
        "value": B,
    }


def calculate_side_bias_index(side_bias: dict) -> Tuple[float, dict]:
    """
    C: 偏侧指数

    max_count = max(left_low_count, right_low_count)

    max_count < 4    C = 0
    max_count = 4    C = 3.5
    max_count = 5    C = 5
    max_count = 6    C = 6
    """
    max_count = max(side_bias["left_low_count"], side_bias["right_low_count"])

    if max_count < 4:
        C = 0.0
    elif max_count == 4:
        C = 3.5
    elif max_count == 5:
        C = 5.0
    else:  # max_count == 6
        C = 6.0

    return C, {"max_count": max_count, "value": C}


def calculate_trend_index(meridian_analysis: List[dict]) -> Tuple[float, dict]:
    """
    D: 经络趋势指数

    每条经络根据整体趋势计分：
    stable_balanced       0
    potential_symptom     0.3
    fast_response         0.3
    stable_left_low       0.5
    stable_right_low      0.5
    cross                 1.2

    D = min(六条经络趋势指数之和, 4)
    """
    trend_scores = {
        "stable_balanced": 0.0,
        "potential_symptom": 0.3,
        "fast_response": 0.3,
        "stable_left_low": 0.5,
        "stable_right_low": 0.5,
        "cross": 1.2,
    }

    per_meridian = []
    total = 0.0

    for m in meridian_analysis:
        trend = m["trend"]
        score = trend_scores.get(trend, 0.0)
        per_meridian.append({
            "meridian": m["meridian"],
            "trend": trend,
            "score": score,
        })
        total += score

    # 封顶
    D = min(total, 4.0)

    return D, {
        "per_meridian": per_meridian,
        "total_before_cap": total,
        "value": D,
    }


def calculate_combo_index(cervical_lumbar_result: dict) -> Tuple[float, dict]:
    """
    E: 组合问题指数

    未触发颈椎/腰椎问题      E = 0
    触发 cervical           E = 2.5
    触发 lumbar             E = 2.5
    触发 cervical_and_lumbar  E = 2.5

    说明：即使同时出现颈椎和腰椎问题，E也不叠加
    """
    result = cervical_lumbar_result["result"]

    if result == "none":
        E = 0.0
    else:
        E = 2.5

    return E, {"cervical_lumbar_result": result, "value": E}


def calculate_problem_index(
    group2_data: dict,
    meridian_analysis: List[dict],
    side_bias: dict,
    cervical_lumbar_result: dict,
) -> Tuple[float, dict]:
    """
    计算总问题指数 I = A + B + C + D + E
    """
    A, A_detail = calculate_low_temperature_index(group2_data)
    B, B_detail = calculate_temperature_difference_index(meridian_analysis)
    C, C_detail = calculate_side_bias_index(side_bias)
    D, D_detail = calculate_trend_index(meridian_analysis)
    E, E_detail = calculate_combo_index(cervical_lumbar_result)

    I = A + B + C + D + E

    return I, {
        "A_low_temperature": A_detail,
        "B_temp_difference": B_detail,
        "C_side_bias": C_detail,
        "D_trend": D_detail,
        "E_combo": E_detail,
        "total": I,
    }


# ============================================================================
# Step 8: 问题指数映射为健康分
# ============================================================================

def map_index_to_score(I: float) -> Tuple[float, str]:
    """
    将问题指数 I 映射为健康分。

    如果 I <= 10：
        score_raw = 90 - 0.4 * I

    如果 10 < I <= 22：
        score_raw = 86 - 0.55 * (I - 10)

    如果 22 < I <= 32：
        score_raw = 79.4 - 0.8 * (I - 22)

    如果 I > 32：
        score_raw = 71.4 - 1.0 * (I - 32)
    """
    if I <= 10:
        score_raw = 90 - 0.4 * I
    elif I <= 22:
        score_raw = 86 - 0.55 * (I - 10)
    elif I <= 32:
        score_raw = 79.4 - 0.8 * (I - 22)
    else:
        score_raw = 71.4 - 1.0 * (I - 32)

    return score_raw, ""


def clamp_first_test_score(score_raw: float) -> Tuple[int, float]:
    """
    首测展示分：
    first_test_score = clamp(score_raw, 65, 89)
    display_score = round(first_test_score)
    """
    clamped = max(65.0, min(89.0, score_raw))
    return round(clamped), clamped


# ============================================================================
# Step 9: 复测评分规则
# ============================================================================

def calculate_retest_score(
    score_raw: float,
    previous_score: float,
    previous_problem_index: float,
    current_problem_index: float,
    usage_days: int,
) -> Tuple[int, float, dict]:
    """
    复测评分计算。

    1. 使用天数加分
    2. 数据改善加分
    3. 复测保护
    """
    # 使用天数加分
    if usage_days <= 2:
        usage_bonus = 0.0
    elif usage_days <= 6:
        usage_bonus = 1.0
    elif usage_days <= 13:
        usage_bonus = 2.0
    elif usage_days <= 29:
        usage_bonus = 3.0
    else:
        usage_bonus = 4.0

    # 数据改善加分
    delta_I = previous_problem_index - current_problem_index
    if delta_I > 0:
        improvement_bonus = min(3.0, 0.3 * delta_I)
    else:
        improvement_bonus = 0.0

    # 复测基础修正分
    retest_score_base = score_raw + usage_bonus + improvement_bonus

    # 复测保护
    if usage_days <= 2:
        protected_score = retest_score_base
    elif usage_days <= 6:
        protected_score = max(retest_score_base, previous_score - 2)
    elif usage_days <= 13:
        protected_score = max(retest_score_base, previous_score)
    elif usage_days <= 29:
        if previous_score < 88:
            protected_score = max(retest_score_base, previous_score + 1)
        else:
            protected_score = max(retest_score_base, previous_score)
    else:  # >= 30
        if previous_score < 90:
            protected_score = max(retest_score_base, previous_score + 2)
        else:
            protected_score = max(retest_score_base, previous_score)

    # 最终展示分（clamp到65-95）
    retest_final_score = max(65.0, min(95.0, protected_score))
    display_score = round(retest_final_score)

    detail = {
        "usage_days": usage_days,
        "usage_bonus": usage_bonus,
        "delta_I": delta_I,
        "improvement_bonus": improvement_bonus,
        "retest_score_base": retest_score_base,
        "protected_score": protected_score,
        "previous_score": previous_score,
        "previous_problem_index": previous_problem_index,
        "current_problem_index": current_problem_index,
    }

    return display_score, retest_final_score, detail


# ============================================================================
# Step 10: 重点问题排序
# ============================================================================

def build_focus_issues(
    lowest_points: List[dict],
    side_bias: dict,
    cervical_lumbar_result: dict,
    meridian_analysis: List[dict],
) -> List[dict]:
    """
    构建本次重点关注的问题列表（控制在3-4个）。

    优先级：
    1. 第二组最低两个点
    2. 温差严重或加重问题
    3. 第二组整体左右偏向问题
    4. 颈椎/腰椎组合问题
    5. 交叉问题中同时伴随温差明显或最低点候选的问题
    """
    issues = []
    priority = 1

    # 1. 最低两点问题
    for lp in lowest_points:
        m = lp["meridian"]
        side = lp["side"]
        m_analysis = next((ma for ma in meridian_analysis if ma["meridian"] == m), None)

        issue = {
            "priority": priority,
            "type": "lowest_point",
            "meridian": m,
            "meridian_name": MERIDIAN_NAMES[m],
            "side": side,
            "title": f"{MERIDIAN_NAMES[m]}问题较突出",
            "reason_codes": ["second_group_lowest_point"],
        }

        # 添加温差相关信息
        if m_analysis:
            if m_analysis["group2_diff_level"] in ("health_problem", "serious_problem"):
                issue["reason_codes"].append(f"group2_diff_{m_analysis['group2_diff_level']}")
            if m_analysis["diff_change"] == "worsened":
                issue["reason_codes"].append("diff_worsened")

        issues.append(issue)
        priority += 1

    # 2. 左右偏向问题
    if side_bias["result"] == "head_blood_supply_attention":
        issues.append({
            "priority": priority,
            "type": "side_bias",
            "title": "头部供血需关注",
            "left_low_count": side_bias["left_low_count"],
            "reason_codes": ["left_bias_count_high"],
        })
        priority += 1
    elif side_bias["result"] == "heart_attention":
        issues.append({
            "priority": priority,
            "type": "side_bias",
            "title": "心脏方向需关注",
            "right_low_count": side_bias["right_low_count"],
            "reason_codes": ["right_bias_count_high"],
        })
        priority += 1

    # 3. 颈椎/腰椎问题
    if cervical_lumbar_result["result"] == "cervical":
        issues.append({
            "priority": priority,
            "type": "cervical_lumbar",
            "title": "颈椎相关问题需关注",
            "reason_codes": ["cervical_issue_detected"],
        })
        priority += 1
    elif cervical_lumbar_result["result"] == "lumbar":
        issues.append({
            "priority": priority,
            "type": "cervical_lumbar",
            "title": "腰椎相关问题需关注",
            "reason_codes": ["lumbar_issue_detected"],
        })
        priority += 1
    elif cervical_lumbar_result["result"] == "cervical_and_lumbar":
        issues.append({
            "priority": priority,
            "type": "cervical_lumbar",
            "title": "颈椎和腰椎问题同时存在",
            "reason_codes": ["cervical_and_lumbar_detected"],
        })
        priority += 1

    # 限制在3-4个重点问题
    return issues[:4]


# ============================================================================
# Step 11: 输入验证
# ============================================================================

def validate_input(payload: dict) -> None:
    """Validate input completeness. Raises ValueError on failure."""
    measurement_type = payload.get("measurement_type")
    if measurement_type not in ("first_test", "retest"):
        raise ValueError("measurement_type must be 'first_test' or 'retest'")

    gender = payload.get("gender")
    if gender not in ("male", "female", "unknown"):
        raise ValueError("gender must be 'male', 'female', or 'unknown'")

    meridians = payload.get("meridians")
    if not isinstance(meridians, dict):
        raise ValueError("meridians must be an object")

    for m in MERIDIANS:
        if m not in meridians:
            raise ValueError(f"Missing meridian: {m}")
        vals = meridians[m]
        required = ["group1_left", "group1_right", "group2_left", "group2_right"]
        for key in required:
            if key not in vals:
                raise ValueError(f"meridians.{m} must contain {key}")

    # 复测额外验证
    if measurement_type == "retest":
        if "previous_score" not in payload:
            raise ValueError("previous_score required for retest")
        if "previous_problem_index" not in payload:
            raise ValueError("previous_problem_index required for retest")
        if "usage_days_between_tests" not in payload:
            raise ValueError("usage_days_between_tests required for retest")


# ============================================================================
# Step 12: 构建完整输出
# ============================================================================

def get_matched_rules(meridian: str, trend: str, group1_status: str, group2_status: str) -> List[str]:
    """根据经络和趋势匹配规则库中的问题描述。"""
    rules_map = {
        "liver": {
            "stable_left_low": ["气虚", "血液流速不够", "血液循环推动不足", "垃圾容易沉积在血管中", "血稠、血脂、高血压方向", "代谢差", "口臭", "放屁多", "解毒功能变弱", "皮肤易过敏", "湿疹", "容易长斑"],
            "stable_right_low": ["藏血功能变弱", "血虚", "心脏供血功能不足", "心慌", "胸闷", "心悸", "心律不齐", "容易做梦", "结合肾右低，容易掉发", "温度特别低时，血虚严重，容易抽筋"],
            "cross": ["是否熬夜", "气血两虚", "脂肪肝", "酒精肝", "肝囊肿"],
        },
        "spleen": {
            "stable_left_low": ["过滤能力弱", "温差大时，容易出现血糖高方向问题", "思虑重", "容易操心"],
            "stable_right_low": ["湿气重", "阳少湿气重", "湿气下注到大肠，结合肝右低、肾右低，容易便溏", "湿气下注到子宫，可能例假长", "湿气下注到小腿，容易腿沉"],
            "cross": ["血糖", "思虑重", "湿气", "四肢乏力", "肌肉松弛", "腿沉"],
        },
        "kidney": {
            "stable_left_low": ["耳鸣，尤其是嗡鸣声", "阴虚", "阴虚生内热", "手心脚心热", "体内像有一把火", "容易缺水", "五心烦躁", "尿黄", "尿短"],
            "stable_right_low": ["耳背", "阳虚", "夜尿", "尿长", "怕冷", "宫寒", "结合肝右低，容易掉发"],
            "cross": ["结石", "囊肿", "腹部手术史", "女性：剖腹产、人流、子宫肌瘤", "男性：前列腺炎、前列腺钙化"],
        },
        "stomach": {
            "stable_left_low": ["阴虚生内热", "消化快", "容易饿"],
            "stable_right_low": ["胃阳不足", "胃胀", "温度特别低时，可能吃什么拉什么"],
            "cross": ["饮食不规律", "胃炎", "胃溃疡", "消化不良"],
        },
        "gallbladder": {
            "stable_left_low": ["胆红素高", "皮肤黄", "眼白黄", "偏头痛"],
            "stable_right_low": ["胆固醇", "脂肪瘤", "优柔寡断", "决断力不够"],
            "cross": ["温度上不去时，容易胆结石、胆囊炎", "不按时吃早餐"],
        },
        "bladder": {
            "stable_left_low": ["肩颈腰与肠道方向需关注", "便秘", "痔疮", "大肠息肉风险", "肺左侧功能风险"],
            "stable_right_low": ["湿下注与腰部方向需关注", "大便不成形", "湿气下注大肠", "肺右侧功能风险"],
            "cross": ["肠道问题需关注", "生殖系统问题需关注", "腰部及循环问题需关注"],
        },
    }

    return rules_map.get(meridian, {}).get(trend, [])


def build_meridian_analysis(
    payload: dict,
    lowest_points: List[dict],
    side_bias: dict,
) -> List[dict]:
    """构建6条经络的详细分析。"""
    meridians = payload["meridians"]
    analysis = []

    lowest_meridian_sides = [(lp["meridian"], lp["side"]) for lp in lowest_points]

    for m in MERIDIANS:
        vals = meridians[m]

        # 获取各组左右状态
        group1_status, group1_low_side, group1_diff = get_side_status(
            vals["group1_left"], vals["group1_right"]
        )
        group2_status, group2_low_side, group2_diff = get_side_status(
            vals["group2_left"], vals["group2_right"]
        )

        # 趋势分析
        trend = analyze_trend(group1_status, group2_status)

        # 温差等级
        group1_diff_level = get_diff_level(group1_diff)
        group2_diff_level = get_diff_level(group2_diff)

        # 温差变化
        diff_change = get_diff_change(group1_diff, group2_diff)

        # 匹配规则
        matched_rules = get_matched_rules(m, trend, group1_status, group2_status)

        # 是否属于重点
        is_focus = False
        focus_reason = []

        # 是最低点之一
        if any(lm[0] == m for lm in lowest_meridian_sides):
            is_focus = True
            focus_reason.append("second_group_lowest_point")

        # 温差严重
        if group2_diff_level in ("health_problem", "serious_problem"):
            is_focus = True
            focus_reason.append(f"group2_diff_{group2_diff_level}")

        # 温差恶化
        if diff_change == "worsened":
            is_focus = True
            focus_reason.append("diff_worsened")

        # 参与偏侧统计
        if side_bias["result"] != "none":
            if (side_bias["result"] == "head_blood_supply_attention" and group2_status == "left_low") or \
               (side_bias["result"] == "heart_attention" and group2_status == "right_low"):
                is_focus = True
                focus_reason.append("side_bias_participant")

        analysis.append({
            "meridian": m,
            "meridian_name": MERIDIAN_NAMES[m],
            "group1_status": group1_status,
            "group2_status": group2_status,
            "trend": trend,
            "group1_diff": group1_diff,
            "group2_diff": group2_diff,
            "group1_diff_level": group1_diff_level,
            "group2_diff_level": group2_diff_level,
            "diff_change": diff_change,
            "matched_rules": matched_rules,
            "is_focus": is_focus,
            "focus_reason": focus_reason,
        })

    return analysis


def get_score_level(score: int) -> Tuple[str, str]:
    """根据分数获取等级和说明。"""
    if score >= 90:
        return "健康优秀", "当前整体状态优秀，请继续保持。"
    elif score >= 80:
        return "轻度失衡", "整体状态尚可，局部仍需关注。"
    elif score >= 70:
        return "中度失衡", "存在较明确失衡，建议持续调理。"
    elif score >= 65:
        return "明显失衡", "当前失衡较明显，建议持续调理并复测。"
    else:
        return "严重失衡", "当前失衡较明显，建议尽早重视。"


def build_final_output(
    payload: dict,
    lowest_points: List[dict],
    side_bias: dict,
    cervical_lumbar_result: dict,
    meridian_analysis: List[dict],
    problem_index: float,
    problem_index_detail: dict,
    score_raw: float,
    display_score: int,
    score_detail: dict,
) -> dict:
    """构建最终输出结构。"""
    measurement_type = payload["measurement_type"]
    gender = payload["gender"]

    # 分数等级
    score_level, score_summary = get_score_level(display_score)

    # 重点问题
    focus_issues = build_focus_issues(
        lowest_points, side_bias, cervical_lumbar_result, meridian_analysis
    )

    # 构建输出
    output = {
        "engine": {
            "mode": "rule-based-v3",
            "version": "3.0",
        },
        "score_result": {
            "score": display_score,
            "score_raw": round(score_raw, 2),
            "problem_index": round(problem_index, 1),
            "problem_index_detail": {
                "low_temperature_index": problem_index_detail["A_low_temperature"]["value"],
                "temperature_difference_index": problem_index_detail["B_temp_difference"]["value"],
                "side_bias_index": problem_index_detail["C_side_bias"]["value"],
                "trend_index": problem_index_detail["D_trend"]["value"],
                "combo_index": problem_index_detail["E_combo"]["value"],
            },
        },
        "lowest_points": {
            "selected": lowest_points,
            "tie_candidates": [],  # 简化为空列表
        },
        "side_bias_summary": side_bias,
        "cervical_lumbar_result": cervical_lumbar_result,
        "meridian_analysis": meridian_analysis,
        "focus_issues": focus_issues,
        "gender": gender,
        "measurement_type": measurement_type,
    }

    # 添加复测相关信息
    if measurement_type == "retest":
        output["retest_detail"] = score_detail

    # 添加模板化建议 (Rule模式)
    previous_score = score_detail.get("previous_score") if score_detail else None
    recommendations = generate_rule_based_recommendations(
        display_score=display_score,
        focus_issues=focus_issues,
        side_bias=side_bias,
        cervical_lumbar_result=cervical_lumbar_result,
        measurement_type=measurement_type,
        previous_score=previous_score,
    )
    output["summary"] = recommendations["summary"]
    output["reportSummary"] = recommendations["reportSummary"]
    output["storefront"] = recommendations["storefront"]
    output["recommendations"] = recommendations["recommendations"]

    return output


# ============================================================================
# Main Inference Function
# ============================================================================

def infer(payload: dict, rules: dict) -> dict:
    """Run the full inference pipeline."""
    # Step 1: 验证输入
    validate_input(payload)

    meridians = payload["meridians"]
    measurement_type = payload["measurement_type"]

    # 构建 group2 数据
    group2_data = {m: {"left": meridians[m]["group2_left"], "right": meridians[m]["group2_right"]} for m in MERIDIANS}

    # Step 2: 第二组最低两点分析
    lowest_points, tie_candidates = find_lowest_two_points(group2_data)

    # Step 3: 第二组左右偏向统计
    side_bias = analyze_side_bias(group2_data)

    # Step 4: 六条经络趋势分析
    meridian_analysis = build_meridian_analysis(payload, lowest_points, side_bias)

    # Step 5: 肾经+膀胱经颈椎/腰椎判断
    kidney_analysis = next((m for m in meridian_analysis if m["meridian"] == "kidney"), None)
    bladder_analysis = next((m for m in meridian_analysis if m["meridian"] == "bladder"), None)
    cervical_lumbar_result = analyze_cervical_lumbar(
        kidney_analysis["trend"], bladder_analysis["trend"]
    )

    # Step 6: 计算问题指数 I = A + B + C + D + E
    problem_index, problem_index_detail = calculate_problem_index(
        group2_data, meridian_analysis, side_bias, cervical_lumbar_result
    )

    # Step 7: 映射为原始分数
    score_raw, _ = map_index_to_score(problem_index)

    # Step 8: 首测或复测分数计算
    score_detail = {}
    if measurement_type == "first_test":
        display_score, clamped_score = clamp_first_test_score(score_raw)
    else:  # retest
        display_score, clamped_score, score_detail = calculate_retest_score(
            score_raw,
            payload["previous_score"],
            payload["previous_problem_index"],
            problem_index,
            payload["usage_days_between_tests"],
        )

    # Step 9: 构建最终输出
    return build_final_output(
        payload=payload,
        lowest_points=lowest_points,
        side_bias=side_bias,
        cervical_lumbar_result=cervical_lumbar_result,
        meridian_analysis=meridian_analysis,
        problem_index=problem_index,
        problem_index_detail=problem_index_detail,
        score_raw=score_raw,
        display_score=display_score,
        score_detail=score_detail,
    )


# ============================================================================
# CLI
# ============================================================================

def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="infer_v2.py", description="TCM Meridian Inference Engine v3.0 - Mulinsen Report Edition")
    ap.add_argument("input", nargs="?", help="Input JSON file")
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
    rules = load_rules(rules_dir)
    result = infer(payload, rules)

    text = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)
    if args.out:
        out_path = (project_root / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
        print(f"Output written to: {out_path}")
    else:
        try:
            print(text)
        except BrokenPipeError:
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
