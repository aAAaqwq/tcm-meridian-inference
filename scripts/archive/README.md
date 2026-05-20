# Scripts 归档目录

此目录存放旧版本的脚本文件，保留以备查阅但不再_active使用。

## 归档文件列表

| 文件名 | 原位置 | 归档原因 | 原始日期 |
|--------|--------|----------|----------|
| `infer_v2_legacy.py` | `scripts/infer.py` | v2旧版本推理引擎，已被 `infer_v3.py` 替代 | 2025-04-29 |
| `test_infer_v2_legacy.py` | `scripts/test_infer.py` | v2配套测试脚本，已被 `tests/run_v3_tests.py` 替代 | 2025-04-29 |
| `run_v3_api_tests_legacy.py` | `scripts/run_v3_api_tests.py` | 早期API测试脚本，功能已合并至 `tests/run_v3_tests.py` | 2025-05-12 |

## 当前使用的核心文件

主目录 (`scripts/`) 中保留的活跃文件：

- `infer_v3.py` - v3新算法主推理引擎（核心）
- `prompt_builder.py` - AI提示词构建器
- `infer_agent.py` - Agent模式（规则引擎 + DeepSeek LLM）
- `deepseek_client.py` - DeepSeek API客户端
- `tcm_api.py` - HTTP API接口
- `logger.py` - 日志工具
- `benchmark.py` - 性能基准测试
- `output_validator.py` - 输出验证器
- `test_api_remote.sh` - 远程API测试脚本
