# TCM 经络推理引擎 v3 - 测试套件

本目录包含 v3 推理引擎的所有测试相关脚本。

## 测试脚本说明

| 脚本 | 用途 | 运行方式 |
|------|------|----------|
| `run_tests_v3.py` | 运行所有测试用例，生成测试报告 | `python3 run_tests_v3.py` |
| `validate_backend.py` | 后端算法验证，确保与 PRD 一致 | `python3 validate_backend.py` |
| `record_actual_outputs.py` | 记录 Rule-only 模式的实际输出 | `python3 record_actual_outputs.py` |
| `record_agent_outputs.py` | 记录 Agent 模式的实际输出（需要 DeepSeek API Key） | `python3 record_agent_outputs.py` |
| `run_v3_api_tests.py` | 通过 HTTP API 并发测试 | `python3 run_v3_api_tests.py` |

## 快速开始

```bash
# 进入测试目录
cd tests

# 运行主测试套件
python3 run_tests_v3.py

# 验证后端算法
python3 validate_backend.py
```

## 测试用例位置

测试用例（fixtures）位于：`../fixtures/v3/`

实际输出结果位于：`../docs/v3/testing/`

## 环境要求

- Python 3.12+
- 依赖：`pip install -r ../requirements.txt`
- Agent 模式测试需要设置 `DEEPSEEK_API_KEY`

## 输出文件

测试运行后会生成：
- `test_report_v3.json` - 详细测试报告
- `../docs/v3/testing/actual-results/` - Rule-only 实际输出
- `../docs/v3/testing/agent-results/` - Agent 模式实际输出
