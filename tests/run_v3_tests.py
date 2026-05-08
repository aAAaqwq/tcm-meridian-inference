#!/usr/bin/env python3
"""
V3推理引擎测试脚本

用法:
  # 本地测试（根据环境变量自动选择模式）
  python3 tests/run_v3_tests.py

  # 强制本地规则引擎测试
  python3 tests/run_v3_tests.py --mode rule

  # 强制本地hybrid模式（需要DEEPSEEK_API_KEY）
  python3 tests/run_v3_tests.py --mode agent

  # 线上API测试
  python3 tests/run_v3_tests.py --url http://180.76.137.183:18790/api/inference/meridian-diagnosis
  python3 tests/run_v3_tests.py --port 18970
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from logger import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

# 尝试导入agent模式
try:
    from infer_agent import run_hybrid
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False

from infer_v3 import infer, load_rules

# 加载环境配置
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "").strip()

# 配置
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures/v3"
RESULTS_DIR = Path(__file__).parent.parent / "docs/v3/testing/actual-results"
MAX_WORKERS = 3  # 并发数（hybrid模式需要限制并发）

# 测试文件列表
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
    "test_33_retest_92_score.json",
    "test_34_retest_91_score.json",
    "test_35_retest_93_score.json",
    "test_36_retest_94_score.json",
    "case_01_first_test.json",
    "case_02_retest.json",
]


def extract_key_fields(response_data: dict) -> dict:
    """从API响应中提取关键字段"""
    result = response_data.get("result", response_data)
    return {
        "score": result.get("score_result", {}).get("score"),
        "problem_index": result.get("score_result", {}).get("problem_index"),
        "problem_index_detail": result.get("score_result", {}).get("problem_index_detail"),
        "lowest_points": result.get("lowest_points"),
        "side_bias_summary": result.get("side_bias_summary"),
        "cervical_lumbar_result": result.get("cervical_lumbar_result"),
        "trend_result": result.get("trend_result"),
        "retest_analysis": result.get("retest_analysis"),
    }


def run_inference_local(payload: dict, rules: dict, mode: str) -> dict:
    """使用本地规则引擎运行测试"""
    if mode == "agent" and AGENT_AVAILABLE:
        # 使用hybrid模式（规则引擎 + DeepSeek LLM）
        project_dir = Path(__file__).parent.parent
        return run_hybrid(payload, rules_dir=project_dir / "rules")
    else:
        # 使用纯规则引擎
        return infer(payload, rules)


def run_single_test_local(test_file: str, rules: dict, mode: str, test_data: dict, request_data: dict, expected_output: dict) -> dict:
    """使用本地规则引擎运行测试"""
    start_time = time.time()
    try:
        actual_output = run_inference_local(request_data, rules, mode)
        elapsed_ms = (time.time() - start_time) * 1000
        key_fields = extract_key_fields(actual_output)
        return {
            "test_file": test_file,
            "test_name": test_data.get("_comment", test_file),
            "status": "success",
            "response_time_ms": round(elapsed_ms, 2),
            "request": request_data,
            "expected": expected_output,
            "actual": actual_output,
            "key_fields": key_fields,
            "error": None
        }
    except Exception as e:
        return {
            "test_file": test_file,
            "test_name": test_data.get("_comment", test_file),
            "status": "error",
            "response_time_ms": round((time.time() - start_time) * 1000, 2),
            "request": request_data,
            "expected": expected_output,
            "actual": None,
            "key_fields": None,
            "error": str(e)
        }


def run_single_test_api(test_file: str, api_url: str, test_data: dict, request_data: dict, expected_output: dict) -> dict:
    """调用线上API运行测试"""
    import requests
    start_time = time.time()
    try:
        # 禁用代理
        session = requests.Session()
        session.trust_env = False

        response = session.post(
            api_url,
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        response.raise_for_status()
        actual_output = response.json()
        elapsed_ms = (time.time() - start_time) * 1000
        key_fields = extract_key_fields(actual_output)
        return {
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
    except Exception as e:
        return {
            "test_file": test_file,
            "test_name": test_data.get("_comment", test_file),
            "status": "error",
            "http_status": getattr(getattr(e, 'response', None), 'status_code', None),
            "response_time_ms": round((time.time() - start_time) * 1000, 2),
            "request": request_data,
            "expected": expected_output,
            "actual": None,
            "key_fields": None,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description="V3推理引擎测试")
    parser.add_argument("--mode", choices=["auto", "rule", "agent"], default="auto",
                        help="推理模式: auto(有KEY用agent)/rule(纯规则)/agent(hybrid)")
    parser.add_argument("--url", type=str, help="线上API地址")
    parser.add_argument("--port", type=int, help="服务器端口（替换默认端口18790）")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="服务器IP")
    parser.add_argument("--sequential", action="store_true", help="顺序执行而非并发")

    args = parser.parse_args()

    # 确定测试模式
    if args.url or args.port:
        mode = "api"
        api_url = args.url if args.url else f"http://{args.host}:{args.port}/api/inference/meridian-diagnosis"
    else:
        mode = "local"
        api_url = None
        # 根据环境变量和参数确定本地模式
        if args.mode == "agent" and not DEEPSEEK_API_KEY:
            print("⚠️ 警告: 强制agent模式但DEEPSEEK_API_KEY未配置，将使用rule模式")
        if args.mode == "rule":
            local_mode = "rule"
        elif args.mode == "agent" and DEEPSEEK_API_KEY and AGENT_AVAILABLE:
            local_mode = "agent"
        else:
            # auto模式: 有KEY用agent，否则用rule
            local_mode = "agent" if (DEEPSEEK_API_KEY and AGENT_AVAILABLE) else "rule"

    # 确保结果目录存在
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("V3 推理引擎测试")
    print("=" * 60)
    if mode == "api":
        print(f"模式: 线上API")
        print(f"API地址: {api_url}")
    else:
        print(f"模式: 本地 ({local_mode})")
        if local_mode == "agent":
            print(f"LLM: DeepSeek ({DEEPSEEK_API_KEY[:8]}...)")

    print(f"测试文件数: {len(TEST_FILES)}")
    if not args.sequential:
        print(f"并发数: {MAX_WORKERS}")
    print("=" * 60)
    print()

    # 预加载规则（本地模式）
    rules = None
    if mode == "local":
        rules = load_rules(Path(__file__).parent.parent / "rules")

    # 读取所有测试数据
    all_test_data = {}
    for test_file in TEST_FILES:
        test_path = FIXTURES_DIR / test_file
        if not test_path.exists():
            print(f"⚠️ 文件不存在: {test_file}")
            continue
        with open(test_path, "r", encoding="utf-8") as f:
            test_data = json.load(f)
        request_data = {k: v for k, v in test_data.items() if k not in ("expected", "_comment")}
        expected_output = test_data.get("expected", {})
        all_test_data[test_file] = {
            "test_data": test_data,
            "request_data": request_data,
            "expected_output": expected_output
        }

    results = []

    if args.sequential:
        # 顺序执行
        for test_file in TEST_FILES:
            if test_file not in all_test_data:
                continue
            data = all_test_data[test_file]
            if mode == "local":
                result = run_single_test_local(test_file, rules, local_mode, **data)
            else:
                result = run_single_test_api(test_file, api_url, **data)
            results.append(result)
            status = "✅" if result["status"] == "success" else "❌"
            print(f"{status} {test_file} ({result['response_time_ms']:.2f}ms)")
    else:
        # 并发执行
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {}
            for test_file in TEST_FILES:
                if test_file not in all_test_data:
                    continue
                data = all_test_data[test_file]
                if mode == "local":
                    future = executor.submit(run_single_test_local, test_file, rules, local_mode, **data)
                else:
                    future = executor.submit(run_single_test_api, test_file, api_url, **data)
                futures[future] = test_file

            for future in as_completed(futures):
                test_file = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                    status = "✅" if result["status"] == "success" else "❌"
                    print(f"{status} {test_file} ({result['response_time_ms']:.2f}ms)")
                except Exception as e:
                    print(f"❌ 异常: {test_file} - {e}")

    # 保存结果
    for result in results:
        result_file = RESULTS_DIR / f"{result['test_file'].replace('.json', '_result.json')}"
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    # 生成汇总
    total = len(results)
    success = sum(1 for r in results if r["status"] == "success")

    print()
    print("=" * 60)
    print("测试完成")
    print("=" * 60)
    print(f"成功: {success}/{total}")
    print(f"结果目录: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
