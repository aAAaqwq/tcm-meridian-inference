#!/usr/bin/env python3
"""Record actual backend outputs for all test cases.

This script directly calls the inference engine (same as backend) to record
actual outputs for comparison with expected values.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from infer_v3 import infer, load_rules

RESULTS_DIR = Path(__file__).parent.parent / "docs" / "v3" / "testing" / "actual-results"
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures" / "v3"


def extract_summary(result: dict, test_file: str) -> dict:
    """Extract key fields for comparison."""
    score_result = result.get("score_result", {})
    pi_detail = score_result.get("problem_index_detail", {})

    return {
        "test_file": test_file,
        "score": score_result.get("score"),
        "score_raw": score_result.get("score_raw"),
        "problem_index": score_result.get("problem_index"),
        "A_low_temperature": pi_detail.get("low_temperature_index"),
        "B_temp_difference": pi_detail.get("temperature_difference_index"),
        "C_side_bias": pi_detail.get("side_bias_index"),
        "D_trend": pi_detail.get("trend_index"),
        "E_combo": pi_detail.get("combo_index"),
        "side_bias_result": result.get("side_bias_summary", {}).get("result"),
        "left_low_count": result.get("side_bias_summary", {}).get("left_low_count"),
        "right_low_count": result.get("side_bias_summary", {}).get("right_low_count"),
        "cervical_lumbar": result.get("cervical_lumbar_result", {}).get("result"),
        "lowest_points": [
            {"meridian": p["meridian"], "side": p["side"], "value": p["value"]}
            for p in result.get("lowest_points", {}).get("selected", [])
        ],
        "focus_issues": [
            {"priority": i["priority"], "title": i["title"]}
            for i in result.get("focus_issues", [])
        ],
    }


def main():
    """Run all tests and record actual outputs."""
    print("=" * 70)
    print("TCM v3 - Recording Actual Backend Outputs")
    print("=" * 70)
    print()

    # Ensure results directory exists
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load rules
    project_root = Path(__file__).parent.parent
    rules = load_rules(project_root / "rules")

    # Get all test files
    test_files = sorted(FIXTURES_DIR.glob("*.json"))
    print(f"Found {len(test_files)} test files")
    print()

    results = []
    summaries = []

    for test_file in test_files:
        print(f"Processing: {test_file.name}...", end=" ")

        try:
            with open(test_file) as f:
                payload = json.load(f)

            # Remove comment and expected fields
            payload.pop("_comment", None)
            payload.pop("expected", None)

            # Run inference
            result = infer(payload, rules)

            # Save full result
            output_file = RESULTS_DIR / f"{test_file.stem}-actual.json"
            with open(output_file, "w") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            # Extract summary
            summary = extract_summary(result, test_file.name)
            summaries.append(summary)
            results.append({
                "test_file": test_file.name,
                "status": "success",
                "output_file": str(output_file),
            })

            print(f"✓ Score: {summary['score']}, PI: {summary['problem_index']}")

        except Exception as e:
            print(f"✗ Error: {e}")
            results.append({
                "test_file": test_file.name,
                "status": "error",
                "error": str(e),
            })

    # Save summary
    summary_file = RESULTS_DIR / "summary.json"
    with open(summary_file, "w") as f:
        json.dump({
            "total": len(test_files),
            "success": sum(1 for r in results if r["status"] == "success"),
            "errors": sum(1 for r in results if r["status"] == "error"),
            "summaries": summaries,
            "results": results,
        }, f, ensure_ascii=False, indent=2)

    # Generate markdown report
    report_file = RESULTS_DIR / "comparison-report.md"
    with open(report_file, "w") as f:
        f.write("# TCM v3 实际输出结果记录\n\n")
        f.write("**生成时间**: 2026-05-04\n\n")
        f.write("**后端版本**: v3.0\n\n")
        f.write("---\n\n")

        f.write("## 测试结果摘要\n\n")
        f.write(f"- 总测试数: {len(test_files)}\n")
        f.write(f"- 成功: {sum(1 for r in results if r['status'] == 'success')}\n")
        f.write(f"- 失败: {sum(1 for r in results if r['status'] == 'error')}\n\n")

        f.write("## 详细结果\n\n")
        f.write("| 测试文件 | 分数 | 问题指数 | A | B | C | D | E | 偏侧结果 | 颈椎/腰椎 |\n")
        f.write("|----------|------|----------|---|---|---|---|---|----------|----------|\n")

        for s in summaries:
            f.write(f"| {s['test_file'][:30]} | {s['score']} | {s['problem_index']} | ")
            f.write(f"{s['A_low_temperature']} | {s['B_temp_difference']} | ")
            f.write(f"{s['C_side_bias']} | {s['D_trend']} | {s['E_combo']} | ")
            f.write(f"{s['side_bias_result'] or '-'} | {s['cervical_lumbar'] or '-'} |\n")

        f.write("\n## 完整输出文件\n\n")
        for r in results:
            if r["status"] == "success":
                f.write(f"- [{r['test_file']}]({r['output_file']})\n")

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total: {len(test_files)}")
    print(f"Success: {sum(1 for r in results if r['status'] == 'success')}")
    print(f"Errors: {sum(1 for r in results if r['status'] == 'error')}")
    print()
    print(f"Results saved to: {RESULTS_DIR}")
    print(f"Summary: {summary_file}")
    print(f"Report: {report_file}")

    return 0


if __name__ == "__main__":
    exit(main())
