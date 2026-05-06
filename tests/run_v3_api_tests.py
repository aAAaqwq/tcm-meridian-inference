#!/usr/bin/env python3
"""
并发测试所有v3测试用例，调用后端API记录实际输出结果
"""

import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import requests

# 配置
API_URL = "http://localhost:18790/api/inference/meridian-diagnosis"
FIXTURES_DIR = Path("../fixtures/v3")
RESULTS_DIR = Path("../docs/v3/testing/actual-results")
MAX_WORKERS = 10  # 并发数

# 确保结果目录存在
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# 测试文件列表（按顺序）
TEST_FILES = [
    "test_01_excellent_score.json",
    "test_02_mild_imbalance.json",
    "test_03_moderate_imbalance.json",
    "test_04_significant_imbalance.json",
    "test_05_trend_stable_left_low.json",
    "test_06_trend_stable_right_low.json",
    "test_07_trend_cross.json",
    "test_08_trend_potential_symptom.json",
    "test_09_trend_fast_response.json",
    "test_10_diff_levels.json",
    "test_11_side_bias_4.json",
    "test_12_side_bias_5.json",
    "test_13_side_bias_6.json",
    "test_14_cervical_opposite.json",
    "test_15_cervical_lumbar_cross.json",
    "test_16_gender_male.json",
    "test_17_gender_female.json",
    "test_18_gender_unknown.json",
    "test_19_retest_0_2_days.json",
    "test_20_retest_3_6_days.json",
    "test_21_retest_7_13_days.json",
    "test_22_retest_14_29_days_low.json",
    "test_23_retest_14_29_days_high.json",
    "test_24_retest_30_plus_days.json",
    "test_25_retest_improvement.json",
    "test_26_low_temp_index_max.json",
    "test_27_diff_change_improved.json",
    "test_28_diff_change_worsened.json",
    "test_29_realistic_mild.json",
    "test_30_realistic_moderate.json",
    "test_31_bladder_lowest.json",
    "test_32_kidney_cross.json",
    "case_01_first_test.json",
    "case_02_retest.json",
]


def extract_key_fields(response_data: dict) -> dict:
    """从API响应中提取关键字段"""
    result = response_data.get("result", {})

    # 提取关键字段
    key_fields = {
        "score": result.get("score"),
        "problem_index": result.get("problem_index"),
        "problem_index_detail": result.get("problem_index_detail"),
        "lowest_points": result.get("lowest_points"),
        "side_bias_summary": result.get("side_bias_summary"),
        "cervical_lumbar_result": result.get("cervical_lumbar_result"),
        "trend_result": result.get("trend_result"),
        "retest_analysis": result.get("retest_analysis"),
    }

    return key_fields


def run_single_test(test_file: str) -> dict:
    """运行单个测试用例"""
    test_path = FIXTURES_DIR / test_file

    # 读取测试文件
    with open(test_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # 准备请求数据 - V3测试文件使用扁平结构
    # 提取除expected和_comment外的字段作为请求数据
    request_data = {k: v for k, v in test_data.items() if k not in ("expected", "_comment")}
    expected_output = test_data.get("expected", {})

    start_time = time.time()

    try:
        # 调用API
        response = requests.post(
            API_URL,
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()

        actual_output = response.json()
        elapsed_ms = (time.time() - start_time) * 1000

        # 提取关键字段
        key_fields = extract_key_fields(actual_output)

        # 构建结果
        result = {
            "test_file": test_file,
            "test_name": test_data.get("_comment", test_file),
            "status": "success",
            "http_status": response.status_code,
            "response_time_ms": round(elapsed_ms, 2),
            "request": request_data,
            "expected": expected_output,
            "actual": actual_output,
            "key_fields": key_fields,
            "error": None
        }

    except requests.exceptions.RequestException as e:
        elapsed_ms = (time.time() - start_time) * 1000
        result = {
            "test_file": test_file,
            "test_name": test_data.get("_comment", test_file),
            "status": "error",
            "http_status": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
            "response_time_ms": round(elapsed_ms, 2),
            "request": request_data,
            "expected": expected_output,
            "actual": None,
            "key_fields": None,
            "error": str(e)
        }

    # 保存单个测试结果
    result_file = RESULTS_DIR / f"{test_file.replace('.json', '_result.json')}"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result


def generate_summary(results: list) -> str:
    """生成汇总报告"""
    total = len(results)
    success = sum(1 for r in results if r["status"] == "success")
    failed = total - success

    lines = [
        "# V3 API 测试结果汇总",
        "",
        f"**测试时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"**API地址**: {API_URL}",
        "",
        "## 统计概览",
        "",
        f"- **测试总数**: {total}",
        f"- **成功数**: {success}",
        f"- **失败数**: {failed}",
        f"- **成功率**: {success/total*100:.1f}%",
        "",
        "## 详细结果",
        "",
        "| 序号 | 测试文件 | 状态 | 响应时间(ms) | Score | Problem Index | Side Bias | Cervical/Lumbar | 错误 |",
        "|------|----------|------|--------------|-------|---------------|-----------|-----------------|------|",
    ]

    for i, r in enumerate(results, 1):
        status_emoji = "✅" if r["status"] == "success" else "❌"
        key_fields = r.get("key_fields") or {}

        score = key_fields.get("score", "-") if key_fields else "-"
        problem_index = key_fields.get("problem_index", "-") if key_fields else "-"
        side_bias = key_fields.get("side_bias_summary", "-") if key_fields else "-"
        cervical_lumbar = key_fields.get("cervical_lumbar_result", "-") if key_fields else "-"

        # 截断长字符串
        side_bias_str = str(side_bias)[:15] if side_bias != "-" else "-"
        cervical_str = str(cervical_lumbar)[:15] if cervical_lumbar != "-" else "-"

        error = r.get("error", "-") or "-"
        error_short = error[:30] + "..." if len(str(error)) > 30 else error

        lines.append(
            f"| {i} | {r['test_file']} | {status_emoji} | {r['response_time_ms']:.2f} | {score} | {problem_index} | {side_bias_str} | {cervical_str} | {error_short} |"
        )

    lines.extend([
        "",
        "## 关键字段详细对比",
        "",
    ])

    for r in results:
        lines.append(f"### {r['test_file']}")
        lines.append("")
        lines.append(f"**测试名称**: {r['test_name']}")
        lines.append(f"**状态**: {'成功' if r['status'] == 'success' else '失败'}")
        lines.append(f"**响应时间**: {r['response_time_ms']:.2f} ms")
        lines.append("")

        if r["status"] == "success" and r.get("key_fields"):
            key_fields = r["key_fields"]
            lines.append("**关键字段**:")
            lines.append("")
            lines.append("| 字段 | 实际值 | 期望值 |")
            lines.append("|------|--------|--------|")

            expected = r.get("expected", {})

            # Score
            actual_score = key_fields.get("score")
            expected_score = expected.get("score")
            match = "✅" if actual_score == expected_score else "⚠️"
            lines.append(f"| score | {actual_score} | {expected_score} {match} |")

            # Problem Index
            actual_pi = key_fields.get("problem_index")
            expected_pi = expected.get("problem_index")
            match = "✅" if actual_pi == expected_pi else "⚠️"
            lines.append(f"| problem_index | {actual_pi} | {expected_pi} {match} |")

            # Problem Index Detail
            actual_pid = key_fields.get("problem_index_detail")
            expected_pid = expected.get("problem_index_detail")
            match = "✅" if actual_pid == expected_pid else "⚠️"
            lines.append(f"| problem_index_detail | {actual_pid} | {expected_pid} {match} |")

            # Side Bias
            actual_sb = key_fields.get("side_bias_summary")
            expected_sb = expected.get("side_bias_summary")
            match = "✅" if actual_sb == expected_sb else "⚠️"
            lines.append(f"| side_bias_summary | {actual_sb} | {expected_sb} {match} |")

            # Cervical Lumbar
            actual_cl = key_fields.get("cervical_lumbar_result")
            expected_cl = expected.get("cervical_lumbar_result")
            match = "✅" if actual_cl == expected_cl else "⚠️"
            lines.append(f"| cervical_lumbar_result | {actual_cl} | {expected_cl} {match} |")

            # Trend Result
            actual_tr = key_fields.get("trend_result")
            expected_tr = expected.get("trend_result")
            if actual_tr or expected_tr:
                match = "✅" if actual_tr == expected_tr else "⚠️"
                lines.append(f"| trend_result | {actual_tr} | {expected_tr} {match} |")

            # Retest Analysis
            actual_ra = key_fields.get("retest_analysis")
            expected_ra = expected.get("retest_analysis")
            if actual_ra or expected_ra:
                match = "✅" if actual_ra == expected_ra else "⚠️"
                lines.append(f"| retest_analysis | {actual_ra} | {expected_ra} {match} |")

            # Lowest Points
            actual_lp = key_fields.get("lowest_points")
            if actual_lp:
                lines.append(f"| lowest_points | {json.dumps(actual_lp, ensure_ascii=False)} | - |")

        elif r["error"]:
            lines.append(f"**错误**: {r['error']}")

        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    """主函数"""
    print("=" * 60)
    print("V3 API 并发测试")
    print("=" * 60)
    print(f"API地址: {API_URL}")
    print(f"测试文件数: {len(TEST_FILES)}")
    print(f"并发数: {MAX_WORKERS}")
    print("=" * 60)
    print()

    results = []

    # 并发执行测试
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_file = {
            executor.submit(run_single_test, test_file): test_file
            for test_file in TEST_FILES
        }

        for future in as_completed(future_to_file):
            test_file = future_to_file[future]
            try:
                result = future.result()
                results.append(result)
                status = "✅ 成功" if result["status"] == "success" else "❌ 失败"
                print(f"{status}: {test_file} ({result['response_time_ms']:.2f}ms)")
            except Exception as e:
                print(f"❌ 异常: {test_file} - {e}")
                results.append({
                    "test_file": test_file,
                    "status": "exception",
                    "error": str(e)
                })

    # 按测试文件顺序排序结果
    results.sort(key=lambda x: TEST_FILES.index(x["test_file"]) if x["test_file"] in TEST_FILES else 999)

    # 生成汇总报告
    summary = generate_summary(results)
    summary_path = RESULTS_DIR / "summary.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    # 打印汇总
    print()
    print("=" * 60)
    print("测试完成")
    print("=" * 60)
    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = len(results) - success_count
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")
    print(f"结果保存目录: {RESULTS_DIR}")
    print(f"汇总报告: {summary_path}")


if __name__ == "__main__":
    main()
