# TCM Meridian Inference MVP — 中医经络推理 Agent

基于 **规则引擎 + DeepSeek LLM** 的六经络推理服务：输入 6 条经络的两组测量值（group1/group2），输出健康评分、经络状态、趋势分析、组合判症、自然语言解读与调理建议。

默认使用 **Hybrid 模式**（规则引擎 + DeepSeek 自然语言生成），DeepSeek 不可用时自动降级到纯规则模式。

---

## 架构

```text
用户 POST JSON
    ↓
tcm_api.py (HTTP Server, port 18790)
    ↓ TCM_INFER_MODE
    ├─ hybrid → infer_v2.py 混合推理（规则 + DeepSeek）← 默认
    ├─ rule   → infer_v2.py 纯规则引擎（确定性，无需 API Key）
    └─ auto   → 有 DEEPSEEK_API_KEY 用 hybrid，否则 fallback rule
```

核心原则：硬逻辑（分数、状态、趋势、组合判症）始终由规则引擎决定，LLM 只负责生成自然语言文案。LLM 失败时自动降级到 rule 模式。

### 组件

| 文件 | 说明 |
|------|------|
| `scripts/tcm_api.py` | HTTP API 服务 |
| `scripts/infer_v2.py` | v3 规则引擎（问题指数算法） |
| `scripts/infer_agent.py` | Hybrid 混合推理（v2 兼容层） |
| `scripts/infer.py` | v2 规则引擎（已废弃） |
| `scripts/deepseek_client.py` | DeepSeek API 客户端 |
| `scripts/prompt_builder.py` | LLM prompt 构建 |
| `scripts/output_validator.py` | LLM 输出校验 |
| `scripts/logger.py` | 日志 + 共享工具 |
| `rules/` | 规则库 JSON |
| `prompts/` | DeepSeek 系统提示词 |
| `fixtures/v3/` | 32+ v3 测试 case |

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
  --data @fixtures/v3/test_01_excellent_score.json | python3 -c "import sys,json;print(json.dumps(json.load(sys.stdin),ensure_ascii=False,indent=2))"
```

### 命令行推理（不走 HTTP）

```bash
python3 scripts/infer_v2.py fixtures/v3/test_01_excellent_score.json        # v3 纯规则
python3 scripts/infer_v2.py fixtures/v3/test_01_excellent_score.json --pretty  # 格式化输出
python3 scripts/infer_agent.py fixtures/v3/test_01_excellent_score.json      # Hybrid（如配置了 DeepSeek）
```

---

## 推理模式

| 模式 | engine.mode | 说明 | 外部依赖 |
|------|-------------|------|----------|
| **Hybrid**（默认） | `hybrid` | 规则引擎 + DeepSeek | `DEEPSEEK_API_KEY` |
| Rule | `rule-based-v3` | 纯规则引擎 | 无 |
| Fallback | `rule-fallback` | DeepSeek 失败时自动降级 | 无 |

---

## 输入格式 (v3)

采用 **group1/group2 两组测量**模型（对应 5min/20min 两个测量时间点）：

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "gallbladder": { "group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0 },
    "bladder":     { "group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0 },
    "liver":       { "group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0 },
    "spleen":      { "group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0 },
    "kidney":      { "group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0 }
  }
}
```

**必填字段**：
- `measurement_type`: `"first_test"` 或 `"retest"`
- `gender`: `"male"`, `"female"`, 或 `"unknown"`
- `meridians`: 6 条经络数据，每条包含 `group1_left`, `group1_right`, `group2_left`, `group2_right`

**复测额外字段**：
- `previous_score`: 上次展示分数
- `previous_problem_index`: 上次问题指数
- `usage_days_between_tests`: 两次测量间隔天数

---

## 输出概览

| 字段 | 类型 | 说明 | 展示 |
|------|------|------|------|
| `engine` | object | 引擎信息 {mode, version} | 调试 |
| `score_result` | object | 评分结果 {score, score_raw, problem_index, problem_index_detail} | 首屏 |
| `lowest_points` | object | 第二组最低两点分析 | 核心 |
| `side_bias_summary` | object | 左右偏向统计（头部供血/心脏方向） | 核心 |
| `cervical_lumbar_result` | object | 颈椎/腰椎判断结果 | 核心 |
| `meridian_analysis` | array[6] | 六经络详细分析（趋势、温差、匹配规则） | 核心 |
| `focus_issues` | array | 重点关注问题列表（3-4个） | 首屏 |
| `summary` | string | 综合健康解读文案 | 首屏 |
| `storefront` | object | 展示话术 {focusHeadline, talkTrack, retestPrompt} | 首屏 |
| `recommendations` | array | 调理建议列表 | 详情 |
| `retest_detail` | object | 复测评分详情（仅复测） | 调试 |

完整字段说明见 [API 文档](docs/api/api-reference.md)。

---

## 健康评分算法 (v3.0)

v3.0 采用 **问题指数** 算法，基于木林森报告推理流程设计：

### 问题指数计算

```
I = A + B + C + D + E

A: 低温指数    - 第二组最低两点与中位数的差距
B: 温差指数    - 六经络温差等级之和（封顶12）
C: 偏侧指数    - 左/右低经络数量（≥4条触发）
D: 趋势指数    - 六经络趋势评分（封顶4）
E: 组合指数    - 颈椎/腰椎问题（2.5分）
```

### 分数映射

```
I ≤ 10:       score_raw = 90 - 0.4 × I
10 < I ≤ 22:  score_raw = 86 - 0.55 × (I - 10)
22 < I ≤ 32:  score_raw = 79.4 - 0.8 × (I - 22)
I > 32:       score_raw = 71.4 - 1.0 × (I - 32)
```

### 首测展示分

```
display_score = clamp(score_raw, 65, 89)
```

### 复测评分规则

1. **使用天数加分**：≤2天(0) → 3-6天(+1) → 7-13天(+2) → 14-29天(+3) → ≥30天(+4)
2. **数据改善加分**：问题指数下降时 +0.3×delta_I（封顶3分）
3. **复测保护**：根据天数保护上次分数

| 分数 | 等级 |
|------|------|
| 90-100 | 健康优秀 |
| 80-89 | 轻度失衡 |
| 70-79 | 中度失衡 |
| 65-69 | 明显失衡 |

### 经络趋势类型

| 趋势 | 说明 |
|------|------|
| `stable_balanced` | 两组均平衡 |
| `stable_left_low` | 两组均左低 |
| `stable_right_low` | 两组均右低 |
| `cross` | 两组左右方向相反 |
| `potential_symptom` | 第一组平衡，第二组异常 |
| `fast_response` | 第一组异常，第二组平衡 |

详见 [评分算法文档](docs/sources/mulinsen-report-inference-flow.md)。

---

## 测试

```bash
# v3 引擎测试
python3 scripts/test_infer_v2.py            # 规则引擎单元测试

# 运行所有 v3 测试 case
for f in fixtures/v3/test_*.json; do
  python3 scripts/infer_v2.py "$f" --pretty
done

# API 冒烟测试
bash scripts/test_api_remote.sh
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
| [API 参考](docs/api/api-reference.md) | 端点、请求/响应规范、字段速查、测试用例记录 |
| [木林森推理流程](docs/sources/mulinsen-report-inference-flow.md) | v3.0 评分算法完整定义 |
| [规则库设计](docs/design/rule-library.md) | 规则文件结构、状态判定 |
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
- v3 引擎采用 group1/group2 测量模型（对应 5min/20min 时间点）
- 首测分数范围：65-89 分；复测分数范围：65-95 分
- 测试覆盖：32+ 测试 case 覆盖各种边界情况
