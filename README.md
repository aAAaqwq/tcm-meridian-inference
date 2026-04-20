# TCM Meridian Inference MVP — 中医经络推理 Agent

基于 **规则引擎 + DeepSeek LLM** 的六经络推理服务：输入 6 条经络的左右测量值，输出健康评分、经络状态、组合判症、自然语言解读与调理建议。

默认使用 **Hybrid 模式**（规则引擎 + DeepSeek 自然语言生成），DeepSeek 不可用时自动降级到纯规则模式。

---

## 架构

```text
用户 POST JSON
    ↓
tcm_api.py (HTTP Server, port 18790)
    ↓ TCM_INFER_MODE
    ├─ agent → infer_agent.py 混合推理（规则 + DeepSeek）← 默认
    ├─ rule  → infer.py 纯规则引擎（确定性，无需 API Key）
    └─ auto  → 有 DEEPSEEK_API_KEY 用 agent，否则 fallback rule
```

核心原则：硬逻辑（分数、状态、症状、组合判症）始终由规则引擎决定，LLM 只负责生成自然语言文案。LLM 失败时自动降级到 rule 模式。

### 组件

| 文件 | 说明 |
|------|------|
| `scripts/tcm_api.py` | HTTP API 服务 |
| `scripts/infer.py` | 纯规则引擎 |
| `scripts/infer_agent.py` | Hybrid 混合推理 |
| `scripts/deepseek_client.py` | DeepSeek API 客户端 |
| `scripts/prompt_builder.py` | LLM prompt 构建 |
| `scripts/output_validator.py` | LLM 输出校验 |
| `scripts/logger.py` | 日志 + 共享工具（MERIDIANS、load_dotenv） |
| `rules/` | 规则库 JSON |
| `prompts/` | DeepSeek 系统提示词 |
| `fixtures/` | 5 个 demo case |

---

## 快速开始

```bash
# 安装依赖
pip install httpx

# 配置 DeepSeek（Hybrid 模式需要）
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY

# 启动服务（默认 auto 模式）
python3 scripts/tcm_api.py

# 调用推理接口
curl -s -X POST http://127.0.0.1:18790/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  --data @fixtures/case_left_low.json | python3 -c "import sys,json;print(json.dumps(json.load(sys.stdin),ensure_ascii=False,indent=2))"
```

### 命令行推理（不走 HTTP）

```bash
python3 scripts/infer_agent.py fixtures/case_left_low.json        # Hybrid
python3 scripts/infer_agent.py fixtures/case_left_low.json --rule-only  # 纯规则
python3 scripts/infer.py fixtures/case_left_low.json               # 纯规则引擎
```

---

## 推理模式

| 模式 | engine.mode | 说明 | 外部依赖 |
|------|-------------|------|----------|
| **Hybrid**（默认） | `hybrid` | 规则引擎 + DeepSeek | `DEEPSEEK_API_KEY` |
| Rule | `rule-based-mvp` | 纯规则引擎 | 无 |
| Fallback | `rule-fallback` | DeepSeek 失败时自动降级 | 无 |

---

## 输入格式

```json
{
  "subject": { "id": "case-001", "name": "张三" },
  "measurements": {
    "liver":       { "left": 35.0, "right": 36.1 },
    "spleen":      { "left": 35.1, "right": 35.9 },
    "kidney":      { "left": 35.0, "right": 35.8 },
    "stomach":     { "left": 35.1, "right": 36.0 },
    "gallbladder": { "left": 35.0, "right": 35.9 },
    "bladder":     { "left": 35.2, "right": 35.9 }
  }
}
```

必填：`measurements`（含 6 条经络的 `left` + `right`）。
可选：`subject`、`context`、`trendDelta`。

---

## 输出概览

| 字段 | 说明 |
|------|------|
| `healthScore` | 综合健康评分（0-100） |
| `meridians` | 各经络详情（status、score、symptoms、narrative） |
| `sixDimensionScores` | 六经评分数组（雷达图） |
| `combinations` | 组合判症命中结果 |
| `storefront` | 门店讲解层（focusHeadline、talkTrack） |
| `summary` | 报告摘要 |

完整字段说明见 [API 文档](docs/api/api-reference.md)。

---

## 健康评分算法

- **单经评分**：基础分 100，`left_low`/`right_low` 扣 16，`cross` 扣 20，可叠加
- **组合扣分**：组合规则命中时，只对参与的经络扣 6 分
- **综合评分**：`healthScore = 六经单经评分的平均值`

| 等级 | 分数范围 |
|------|----------|
| 优秀 | 85-100 |
| 良好 | 70-84 |
| 注意 | 55-69 |
| 预警 | <55 |

详见 [评分算法文档](docs/design/scoring-algorithm.md)。

---

## 测试

```bash
python3 scripts/test_infer.py            # 规则引擎单元测试（12 个）
python3 scripts/test_infer_agent.py      # Hybrid 集成测试（h1-h7）
bash scripts/test_api_remote.sh          # 远程 API 冒烟测试
```

---

## 日志

- 输出：stdout + `logs/tcm.log`（每日轮转，保留 30 天）
- DEBUG 模式：`TCM_LOG_LEVEL=DEBUG python3 scripts/tcm_api.py`
- 日志内容：启动/关闭、每次推理的 mode/score/latency、DeepSeek 调用/重试/降级

---

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `TCM_API_PORT` | `18790` | 服务端口 |
| `TCM_INFER_MODE` | `auto` | `rule` / `agent` / `auto` |
| `DEEPSEEK_API_KEY` | （空） | DeepSeek API 密钥 |
| `DEEPSEEK_MODEL` | `deepseek-chat` | DeepSeek 模型 |
| `TCM_LOG_LEVEL` | `INFO` | 日志级别 |

---

## 文档索引

| 文档 | 说明 |
|------|------|
| [API 参考](docs/api/api-reference.md) | 端点、请求/响应规范、字段速查 |
| [评分算法](docs/design/scoring-algorithm.md) | 评分原理、扣分规则、计算示例 |
| [规则库设计](docs/design/rule-library.md) | 规则文件结构、状态判定、数据规避 |
| [路线图](docs/roadmap.md) | 里程碑、当前进度、后续计划 |

---

## 路线图

**当前阶段**：打包部署上线

详见 [docs/roadmap.md](docs/roadmap.md)。

---

## 已知约束

- 本服务是**规则驱动 + LLM 辅助**的推理服务，不是临床诊断系统
- 输出不应被表述为医疗诊断结论
- Hybrid 模式依赖 DeepSeek API，调用失败时自动降级到 rule 模式
- 某些 case 可能同时命中多个组合规则，这是当前设计允许的行为
