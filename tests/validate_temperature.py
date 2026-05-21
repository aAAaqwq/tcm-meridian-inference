#!/usr/bin/env python3
"""
温度设计验证工具
验证测试用例的温度分布是否与目标分数匹配

用法:
  python validate_temperature.py fixtures/v3/test_01_excellent_score.json
"""

import json
import statistics
import sys
from pathlib import Path

def analyze_temperature(data):
    """分析温度数据，计算各指标"""
    meridians = data.get("meridians", {})

    # 收集数据
    group2_temps = []
    meridian_data = []

    for name, m in meridians.items():
        g1_left = round(m["group1_left"], 1)
        g1_right = round(m["group1_right"], 1)
        g2_left = round(m["group2_left"], 1)
        g2_right = round(m["group2_right"], 1)

        group2_temps.extend([g2_left, g2_right])

        # 左右状态
        g1_status = "balanced" if g1_left == g1_right else ("left_low" if g1_left < g1_right else "right_low")
        g2_status = "balanced" if g2_left == g2_right else ("left_low" if g2_left < g2_right else "right_low")

        # 温差
        g1_diff = abs(g1_left - g1_right)
        g2_diff = abs(g2_left - g2_right)

        meridian_data.append({
            "name": name,
            "g1_status": g1_status,
            "g2_status": g2_status,
            "g1_diff": g1_diff,
            "g2_diff": g2_diff
        })

    # 计算低温指数A
    median = statistics.median(group2_temps)
    lowest_2 = sorted(group2_temps)[:2]
    lowest_avg = sum(lowest_2) / len(lowest_2)
    low_temp_gap = median - lowest_avg

    if low_temp_gap <= 0.5:
        A = 0
    elif low_temp_gap <= 1.0:
        A = 2
    elif low_temp_gap <= 2.0:
        A = 4
    elif low_temp_gap <= 3.0:
        A = 6
    else:
        A = 8

    # 计算温差指数B
    B = 0
    for m in meridian_data:
        base = 0
        if m["g2_diff"] > 2.0:
            base = 5
        elif m["g2_diff"] > 0.5:
            base = 2.5
        elif m["g2_diff"] > 0.2:
            base = 1

        # 温差变化修正
        diff_delta = m["g2_diff"] - m["g1_diff"]
        if diff_delta > 0.2:
            base += 0.5
        elif diff_delta < -0.2:
            base -= 0.5

        B += max(0, base)
    B = min(B, 16)

    # 计算偏侧指数C
    left_low = sum(1 for m in meridian_data if m["g2_status"] == "left_low")
    right_low = sum(1 for m in meridian_data if m["g2_status"] == "right_low")
    max_bias = max(left_low, right_low)

    if max_bias < 4:
        C = 0
    elif max_bias == 4:
        C = 4
    elif max_bias == 5:
        C = 6
    else:
        C = 8

    # 计算趋势指数D
    D = 0
    for m in meridian_data:
        if m["g1_status"] in ["left_low", "right_low"] and m["g2_status"] in ["left_low", "right_low"]:
            if m["g1_status"] != m["g2_status"]:
                D += 2  # cross
            else:
                D += 1  # stable
        elif m["g1_status"] == "balanced" and m["g2_status"] in ["left_low", "right_low"]:
            D += 0.5  # potential_symptom
        elif m["g1_status"] in ["left_low", "right_low"] and m["g2_status"] == "balanced":
            D += 0.5  # fast_response
    D = min(D, 8)

    # 计算组合问题E (简化版)
    E = 0
    cross_count = sum(1 for m in meridian_data if m["g1_status"] in ["left_low", "right_low"] and m["g2_status"] in ["left_low", "right_low"] and m["g1_status"] != m["g2_status"])

    # 检查肾经+膀胱经组合
    kidney_data = next((m for m in meridian_data if m["name"] == "kidney"), None)
    bladder_data = next((m for m in meridian_data if m["name"] == "bladder"), None)

    if kidney_data and bladder_data:
        k_trend = "cross" if (kidney_data["g1_status"] in ["left_low", "right_low"] and kidney_data["g2_status"] in ["left_low", "right_low"] and kidney_data["g1_status"] != kidney_data["g2_status"]) else "stable"
        b_trend = "cross" if (bladder_data["g1_status"] in ["left_low", "right_low"] and bladder_data["g2_status"] in ["left_low", "right_low"] and bladder_data["g1_status"] != bladder_data["g2_status"]) else "stable"

        if k_trend == "cross" or b_trend == "cross":
            E = 4  # cervical_and_lumbar
        elif kidney_data["g2_status"] == bladder_data["g2_status"] and kidney_data["g2_status"] != "balanced":
            E = 3  # lumbar
        elif kidney_data["g2_status"] != "balanced" and bladder_data["g2_status"] != "balanced":
            E = 3  # cervical

    # 检查肝经最低
    liver_idx = next((i for i, m in enumerate(meridian_data) if m["name"] == "liver"), -1)
    if liver_idx >= 0:
        g2_temps_by_meridian = {}
        for m in meridian_data:
            g2_left = meridians[m["name"]]["group2_left"]
            g2_right = meridians[m["name"]]["group2_right"]
            g2_temps_by_meridian[m["name"]] = min(g2_left, g2_right)

        if g2_temps_by_meridian.get("liver", 999) == min(g2_temps_by_meridian.values()):
            E += 3

    PI = int(A + B + C + D + E)

    # 计算预期分数
    if PI <= 5:
        score = 88 - 1.6 * PI
    elif PI <= 12:
        score = 80 - 0.71 * (PI - 5)
    elif PI <= 20:
        score = 75 - 0.625 * (PI - 12)
    elif PI <= 30:
        score = 70 - 0.7 * (PI - 20)
    else:
        score = 63

    return {
        "A": A,
        "B": round(B, 1),
        "C": C,
        "D": round(D, 1),
        "E": E,
        "PI": PI,
        "score": round(score, 1),
        "temp_range": (min(group2_temps), max(group2_temps)),
        "low_temp_gap": round(low_temp_gap, 1),
        "max_bias": max_bias,
        "cross_count": cross_count
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"错误: 文件不存在: {filepath}")
        sys.exit(1)

    data = json.loads(filepath.read_text())
    expected = data.get("expected", {})
    target_score = expected.get("target_score", expected.get("score", 0))

    result = analyze_temperature(data)

    print(f"\n文件: {filepath.name}")
    print(f"注释: {data.get('_comment', 'N/A')}")
    print(f"\n{'='*60}")
    print("温度分析结果")
    print(f"{'='*60}")
    print(f"\n温度范围: {result['temp_range'][0]:.1f} - {result['temp_range'][1]:.1f}℃")
    print(f"低温差距: {result['low_temp_gap']:.1f}℃ (中位数 - 最低点平均)")
    print(f"最大偏侧: {result['max_bias']}条经络")
    print(f"交叉数: {result['cross_count']}条")

    print(f"\n问题指数 (PI = A + B + C + D + E):")
    print(f"  A (低温指数): {result['A']}")
    print(f"  B (温差指数): {result['B']}")
    print(f"  C (偏侧指数): {result['C']}")
    print(f"  D (趋势指数): {result['D']}")
    print(f"  E (组合问题): {result['E']}")
    print(f"  ─────────────────")
    print(f"  PI 总计: {result['PI']}")

    print(f"\n{'='*60}")
    print("分数验证")
    print(f"{'='*60}")
    print(f"估算分数: {result['score']}")

    if target_score > 0:
        print(f"目标分数: {target_score}")
        diff = result['score'] - target_score
        if abs(diff) <= 2:
            print(f"✅ 匹配 (偏差: {diff:+.1f})")
        else:
            print(f"❌ 不匹配 (偏差: {diff:+.1f})")

            # 给出建议
            print(f"\n修正建议:")
            if result['PI'] > 30:
                print(f"  - PI过高(>30)，会被限制为63分")
                print(f"  - 建议降低温度差距到2.5-3.0℃")
                print(f"  - 减少交叉趋势")
            elif result['score'] > target_score + 5:
                print(f"  - PI偏低，需要增加温度差距或偏侧数")
                print(f"  - 当前PI={result['PI']}，目标PI≈{int((88-target_score)/1.6) if target_score>=80 else int(5+(80-target_score)/0.71) if target_score>=75 else int(12+(75-target_score)/0.625) if target_score>=70 else int(20+(70-target_score)/0.7)}")
            elif result['score'] < target_score - 5:
                print(f"  - PI偏高，需要降低温度差距")
                print(f"  - 当前PI={result['PI']}，目标PI≈{int((88-target_score)/1.6) if target_score>=80 else int(5+(80-target_score)/0.71) if target_score>=75 else int(12+(75-target_score)/0.625) if target_score>=70 else int(20+(70-target_score)/0.7)}")
    else:
        print("目标分数: 未指定")

    print(f"\n{'='*60}")


if __name__ == "__main__":
    main()
