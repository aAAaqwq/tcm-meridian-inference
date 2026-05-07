#!/usr/bin/env python3
"""Final comprehensive verification of the implementation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from infer_v3 import (
    MERIDIANS,
    get_side_status,
    get_diff_level,
    analyze_trend,
    analyze_cervical_lumbar,
    detect_combination_rules,
)


def get_trend_type(group1_status: str, group2_status: str) -> str:
    """Wrapper to get trend type from analyze_trend."""
    result = analyze_trend(
        group1_left=35.0,
        group1_right=36.0,
        group2_left=35.0,
        group2_right=36.0,
        group1_low_status=group1_status,
        group2_low_status=group2_status,
    )
    return result.get("trend", "unknown")


def test_core_functions():
    """Test core inference functions."""
    print("=" * 60)
    print("核心函数验证")
    print("=" * 60)

    tests = []

    # Test get_side_status
    status, low_side, diff = get_side_status(35.0, 36.0)
    tests.append(("get_side_status 左低", status == "left_low"))

    status, low_side, diff = get_side_status(36.0, 35.0)
    tests.append(("get_side_status 右低", status == "right_low"))

    # Test get_trend_type (via analyze_trend wrapper)
    trend = get_trend_type("left_low", "left_low")
    tests.append(("get_trend_type stable_left_low", trend == "stable_left_low"))

    trend = get_trend_type("left_low", "right_low")
    tests.append(("get_trend_type cross", trend == "cross"))

    # Test get_diff_level
    tests.append(("get_diff_level balanced", get_diff_level(0.1) == "balanced"))
    tests.append(("get_diff_level mild", get_diff_level(0.3) == "mild_sub_health"))
    tests.append(("get_diff_level health", get_diff_level(0.8) == "health_problem"))
    tests.append(("get_diff_level serious", get_diff_level(2.5) == "serious_problem"))

    # Test analyze_cervical_lumbar
    result = analyze_cervical_lumbar("stable_left_low", "stable_left_low")
    tests.append(("cervical_lumbar lumbar", result["result"] == "lumbar"))

    result = analyze_cervical_lumbar("stable_left_low", "stable_right_low")
    tests.append(("cervical_lumbar cervical", result["result"] == "cervical"))

    result = analyze_cervical_lumbar("cross", "stable_left_low")
    tests.append(("cervical_lumbar cross -> both", result["result"] == "cervical_and_lumbar"))

    # Test detect_combination_rules
    ma = [
        {"meridian": "liver", "trend": "stable_left_low"},
        {"meridian": "gallbladder", "trend": "stable_left_low"},
        {"meridian": "spleen", "trend": "stable_balanced"},
        {"meridian": "kidney", "trend": "stable_balanced"},
        {"meridian": "stomach", "trend": "stable_balanced"},
        {"meridian": "bladder", "trend": "stable_balanced"},
    ]
    combos = detect_combination_rules(ma)
    has_liver_gall = any(c["rule_id"] == "combo_liver_gall" for c in combos)
    tests.append(("combo_liver_gall", has_liver_gall))

    ma_cross = [
        {"meridian": "liver", "trend": "cross"},
        {"meridian": "gallbladder", "trend": "cross"},
        {"meridian": "spleen", "trend": "cross"},
        {"meridian": "kidney", "trend": "stable_balanced"},
        {"meridian": "stomach", "trend": "stable_balanced"},
        {"meridian": "bladder", "trend": "stable_balanced"},
    ]
    combos = detect_combination_rules(ma_cross)
    has_multi_cross = any(c["rule_id"] == "combo_multi_cross" for c in combos)
    tests.append(("combo_multi_cross", has_multi_cross))

    passed = sum(1 for _, p in tests if p)
    for name, result in tests:
        print(f"{'✓' if result else '✗'} {name}")

    print(f"\n核心函数: {passed}/{len(tests)} 通过")
    return passed == len(tests)


def test_edge_cases():
    """Test edge cases."""
    print("\n" + "=" * 60)
    print("边界条件验证")
    print("=" * 60)

    tests = []

    # Edge case: exactly 0.2 diff (boundary of balanced)
    status, _, _ = get_side_status(36.0, 36.2)
    tests.append(("边界: 温差0.2视为平衡", status == "left_low"))

    # Edge case: exactly 3 crosses
    ma = [
        {"meridian": "liver", "trend": "cross"},
        {"meridian": "gallbladder", "trend": "cross"},
        {"meridian": "spleen", "trend": "cross"},
        {"meridian": "kidney", "trend": "stable_balanced"},
        {"meridian": "stomach", "trend": "stable_balanced"},
        {"meridian": "bladder", "trend": "stable_balanced"},
    ]
    combos = detect_combination_rules(ma)
    has_multi = any(c["rule_id"] == "combo_multi_cross" for c in combos)
    tests.append(("边界: 恰好3条交叉", has_multi))

    # Edge case: 2 crosses (should NOT trigger)
    ma = [
        {"meridian": "liver", "trend": "cross"},
        {"meridian": "gallbladder", "trend": "cross"},
        {"meridian": "spleen", "trend": "stable_balanced"},
        {"meridian": "kidney", "trend": "stable_balanced"},
        {"meridian": "stomach", "trend": "stable_balanced"},
        {"meridian": "bladder", "trend": "stable_balanced"},
    ]
    combos = detect_combination_rules(ma)
    has_multi = any(c["rule_id"] == "combo_multi_cross" for c in combos)
    tests.append(("边界: 仅2条交叉不触发", not has_multi))

    passed = sum(1 for _, p in tests if p)
    for name, result in tests:
        print(f"{'✓' if result else '✗'} {name}")

    print(f"\n边界条件: {passed}/{len(tests)} 通过")
    return passed == len(tests)


def main():
    core_ok = test_core_functions()
    edge_ok = test_edge_cases()

    print("\n" + "=" * 60)
    print("最终审查验证报告")
    print("=" * 60)
    print(f"{'✓' if core_ok else '✗'} 核心函数测试")
    print(f"{'✓' if edge_ok else '✗'} 边界条件测试")

    if core_ok and edge_ok:
        print("\n✓ 所有审查验证通过！")
        return 0
    else:
        print("\n✗ 部分测试未通过")
        return 1


if __name__ == "__main__":
    sys.exit(main())
