#!/usr/bin/env python3
"""Test runner for v3 inference engine.

Runs all test cases in fixtures/v3/ and generates a report.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from infer_v2 import infer, load_rules

# Test cases to run
TEST_CASES = [
    # Score range tests
    ("test_01_excellent_score.json", "首测-健康优秀(90-100)"),
    ("test_02_mild_imbalance.json", "首测-轻度失衡(80-89)"),
    ("test_03_moderate_imbalance.json", "首测-中度失衡(70-79)"),
    ("test_04_significant_imbalance.json", "首测-明显失衡(65-69)"),

    # Trend tests
    ("test_05_trend_stable_left_low.json", "趋势-stable_left_low+腰椎"),
    ("test_06_trend_stable_right_low.json", "趋势-stable_right_low+腰椎"),
    ("test_07_trend_cross.json", "趋势-cross+颈椎腰椎同时"),
    ("test_08_trend_potential_symptom.json", "趋势-potential_symptom"),
    ("test_09_trend_fast_response.json", "趋势-fast_response"),

    # Diff level tests
    ("test_10_diff_levels.json", "温差等级-四种等级"),

    # Side bias tests
    ("test_11_side_bias_4.json", "偏侧-4条左低(C=3.5)"),
    ("test_12_side_bias_5.json", "偏侧-5条右低(C=5)"),
    ("test_13_side_bias_6.json", "偏侧-6条左低(C=6)"),

    # Cervical/Lumbar tests
    ("test_14_cervical_opposite.json", "颈椎-相反低"),
    ("test_15_cervical_lumbar_cross.json", "颈椎腰椎-交叉"),

    # Gender tests
    ("test_16_gender_male.json", "性别-男性过滤"),
    ("test_17_gender_female.json", "性别-女性过滤"),
    ("test_18_gender_unknown.json", "性别-未知过滤"),

    # Retest tests
    ("test_19_retest_0_2_days.json", "复测-0-2天"),
    ("test_20_retest_3_6_days.json", "复测-3-6天"),
    ("test_21_retest_7_13_days.json", "复测-7-13天"),
    ("test_22_retest_14_29_days_low.json", "复测-14-29天上次<88"),
    ("test_23_retest_14_29_days_high.json", "复测-14-29天上次>=88"),
    ("test_24_retest_30_plus_days.json", "复测-30天+"),
    ("test_25_retest_improvement.json", "复测-数据改善加分"),

    # Low temperature index
    ("test_26_low_temp_index_max.json", "低温指数-A=6"),

    # Diff change tests
    ("test_27_diff_change_improved.json", "温差变化-改善"),
    ("test_28_diff_change_worsened.json", "温差变化-恶化"),

    # Original cases
    ("case_01_first_test.json", "PRD示例-首测"),
    ("case_02_retest.json", "PRD示例-复测"),
]


def run_test(test_file: str, description: str, rules: dict) -> Tuple[bool, dict]:
    """Run a single test case and return success status and results."""
    test_path = Path("fixtures/v3") / test_file

    try:
        with open(test_path) as f:
            payload = json.load(f)

        # Remove _comment and expected fields
        payload.pop("_comment", None)
        payload.pop("expected", None)

        result = infer(payload, rules)

        return True, result

    except Exception as e:
        return False, {"error": str(e)}


def print_result(test_file: str, description: str, success: bool, result: dict):
    """Print test result in a formatted way."""
    status = "✓ PASS" if success else "✗ FAIL"

    print(f"\n{'=' * 60}")
    print(f"{status} | {description}")
    print(f"File: {test_file}")
    print("-" * 60)

    if not success:
        print(f"Error: {result.get('error', 'Unknown error')}")
        return

    # Print key results
    score_result = result.get("score_result", {})
    print(f"Score: {score_result.get('score')} | Problem Index: {score_result.get('problem_index')}")

    # Print problem index breakdown
    detail = score_result.get("problem_index_detail", {})
    print(f"  A(低温): {detail.get('low_temperature_index')} | "
          f"B(温差): {detail.get('temperature_difference_index')} | "
          f"C(偏侧): {detail.get('side_bias_index')}")
    print(f"  D(趋势): {detail.get('trend_index')} | "
          f"E(组合): {detail.get('combo_index')}")

    # Print side bias
    side_bias = result.get("side_bias_summary", {})
    if side_bias.get("result") != "none":
        print(f"Side Bias: {side_bias.get('result')} (L:{side_bias.get('left_low_count')} R:{side_bias.get('right_low_count')})")

    # Print cervical/lumbar
    cl = result.get("cervical_lumbar_result", {})
    if cl.get("result") != "none":
        print(f"Cervical/Lumbar: {cl.get('result')}")

    # Print retest details if applicable
    retest = result.get("retest_detail", {})
    if retest:
        print(f"Retest: +{retest.get('usage_bonus')} days | +{retest.get('improvement_bonus'):.1f} improvement")


def main():
    """Run all tests and generate report."""
    print("=" * 60)
    print("TCM Inference Engine v3 - Test Suite")
    print("=" * 60)

    # Load rules (from project root)
    project_root = Path(__file__).parent.parent
    rules = load_rules(project_root / "rules")

    passed = 0
    failed = 0
    results = []

    for test_file, description in TEST_CASES:
        success, result = run_test(test_file, description, rules)
        print_result(test_file, description, success, result)

        if success:
            passed += 1
        else:
            failed += 1

        results.append({
            "file": test_file,
            "description": description,
            "success": success,
            "result": result
        })

    # Summary
    print(f"\n{'=' * 60}")
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total:  {len(TEST_CASES)}")
    print(f"Passed: {passed} ✓")
    print(f"Failed: {failed} ✗")
    print(f"Rate:   {passed/len(TEST_CASES)*100:.1f}%")
    print("=" * 60)

    # Save detailed report
    report = {
        "summary": {
            "total": len(TEST_CASES),
            "passed": passed,
            "failed": failed,
            "rate": passed / len(TEST_CASES) * 100
        },
        "results": results
    }

    report_path = Path("test_report_v3.json")
    with open(report_path, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nDetailed report saved to: {report_path}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
