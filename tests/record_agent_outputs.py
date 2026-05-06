#!/usr/bin/env python3
"""Record actual backend outputs with Agent/LLM enrichment.

This script calls the hybrid inference agent (rule engine + DeepSeek LLM)
to record actual outputs including LLM-generated fields:
- storefront (focusHeadline, clientExplanation, talkTrack, retestPrompt)
- summary / reportSummary
- recommendations
- meridianNarrative
"""

import json
import sys
import os
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from infer_agent import run_hybrid
from logger import load_dotenv

# Load environment variables (including DEEPSEEK_API_KEY)
load_dotenv()

RESULTS_DIR = Path("../docs/v3/testing/agent-results")
FIXTURES_DIR = Path("../fixtures/v3")


def extract_summary(result: dict, test_file: str) -> dict:
    """Extract key fields for comparison including LLM fields."""
    score_result = result.get("score_result", {})
    pi_detail = score_result.get("problem_index_detail", {})

    summary = {
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
        # LLM-generated fields
        "has_storefront": "storefront" in result,
        "has_summary": "summary" in result or "reportSummary" in result,
        "has_recommendations": "recommendations" in result,
        "storefront": result.get("storefront", {}),
        "summary": result.get("summary", result.get("reportSummary", "")),
        "recommendations": result.get("recommendations", [])[:3],  # First 3 only
    }

    return summary


def main():
    """Run all tests and record agent outputs."""
    print("=" * 70)
    print("TCM v3 - Recording Agent Mode Outputs (with LLM enrichment)")
    print("=" * 70)
    print()

    # Ensure results directory exists
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load rules
    rules_dir = Path("../rules")

    # Get all test files
    test_files = sorted(FIXTURES_DIR.glob("*.json"))
    print(f"Found {len(test_files)} test files")
    print()

    results = []
    summaries = []

    for test_file in test_files:
        print(f"Processing: {test_file.name}...", end=" ", flush=True)

        try:
            with open(test_file) as f:
                payload = json.load(f)

            # Remove comment and expected fields
            payload.pop("_comment", None)
            payload.pop("expected", None)

            # Run hybrid inference (rule engine + LLM)
            result = run_hybrid(payload, rules_dir=rules_dir, skip_llm=False)

            # Save full result
            output_file = RESULTS_DIR / f"{test_file.stem}-agent.json"
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

            # Print summary info
            storefront = result.get("storefront", {})
            has_llm_fields = bool(storefront or result.get("summary"))
            print(f"✓ Score: {summary['score']}, PI: {summary['problem_index']}, "
                  f"LLM: {'✓' if has_llm_fields else '✗'}")

            # Print storefront headline if available
            if storefront.get("focusHeadline"):
                print(f"  Headline: {storefront['focusHeadline'][:50]}...")

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
        f.write("# TCM v3 Agent 模式实际输出结果\n\n")
        f.write("**生成时间**: 2026-05-05\n\n")
        f.write("**后端版本**: v3.0 (Agent 模式 - 规则引擎 + DeepSeek LLM)\n\n")
        f.write("---\n\n")

        f.write("## 测试结果摘要\n\n")
        f.write(f"- 总测试数: {len(test_files)}\n")
        f.write(f"- 成功: {sum(1 for r in results if r['status'] == 'success')}\n")
        f.write(f"- 失败: {sum(1 for r in results if r['status'] == 'error')}\n\n")

        f.write("## 详细结果\n\n")
        f.write("| 测试文件 | 分数 | 问题指数 | 偏侧结果 | 颈椎/腰椎 | LLM摘要 |\n")
        f.write("|----------|------|----------|----------|----------|----------|\n")

        for s in summaries:
            storefront = s.get("storefront", {})
            headline = storefront.get("focusHeadline", "-")
            if len(headline) > 20:
                headline = headline[:17] + "..."
            f.write(f"| {s['test_file'][:25]} | {s['score']} | {s['problem_index']} | ")
            f.write(f"{s['side_bias_result'] or '-'} | {s['cervical_lumbar'] or '-'} | ")
            f.write(f"{headline} |\n")

        f.write("\n## Storefront 示例\n\n")
        for s in summaries[:3]:  # Show first 3 as examples
            storefront = s.get("storefront", {})
            if storefront:
                f.write(f"### {s['test_file']}\n\n")
                f.write(f"**Headline**: {storefront.get('focusHeadline', '-')}\n\n")
                f.write(f"**Explanation**: {storefront.get('clientExplanation', '-')[:100]}...\n\n")
                talk_track = storefront.get('talkTrack', [])
                if talk_track:
                    f.write(f"**Talk Track**: {talk_track[0][:80]}...\n\n")
                f.write("---\n\n")

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
