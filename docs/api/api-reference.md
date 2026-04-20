# TCM Meridian Inference API 文档

面向：前端 / 调用方 / 集成开发  
项目：`tcm-meridian-inference-mvp`  
当前版本：`0.4.0`  
更新日期：2026-04-16

---

## 1. 架构概述

```
用户 POST JSON
    ↓
tcm_api.py (HTTP Server)
    ↓ TCM_INFER_MODE
    ├─ rule  → infer.py 规则引擎（确定性，无需 API Key）
    ├─ agent → infer_agent.py 混合推理（规则引擎 + DeepSeek 自然语言）
    └─ auto  → 有 DEEPSEEK_API_KEY 时用 agent，否则 fallback 到 rule
```

**核心原则**：硬逻辑（分数、状态、症状、组合判症）始终由规则引擎决定，LLM 只负责生成可读的自然语言文案。LLM 失败时自动 fallback 到 rule 模式。

> 重要边界：本服务是**规则驱动 + LLM 辅助**的推理服务，不是训练型医学诊断模型，输出不应被表述为临床诊断结论。

---

## 2. 端点一览

| Method | Path | 说明 |
|--------|------|------|
| `GET` | `/` | 服务信息（版本、推理模式、端点列表） |
| `GET` | `/health` | 健康检查（legacy） |
| `GET` | `/healthz` | 健康检查 |
| `POST` | `/test` | 使用内置样例数据运行推理 |
| `POST` | `/` | 运行推理（legacy） |
| `POST` | `/api/inference/meridian-diagnosis` | **主推理接口** |

---

## 3. 请求规范

### 3.1 请求体结构

```json
{
  "subject": { "id": "张三", "name": "张三" },
  "measurements": {
    "liver":       { "left": 35.2, "right": 36.2 },
    "spleen":      { "left": 35.1, "right": 35.5 },
    "kidney":      { "left": 35.0, "right": 35.9 },
    "stomach":     { "left": 36.0, "right": 35.2 },
    "gallbladder": { "left": 35.1, "right": 36.0 },
    "bladder":     { "left": 36.1, "right": 35.2 }
  }
}
```

### 3.2 字段说明

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `subject` | 否 | object | 受测对象信息 |
| `subject.id` | 否 | string | 受测对象唯一标识 |
| `subject.name` | 否 | string | 展示名 |
| `measurements` | **是** | object | 六条经络测量数据 |
| `context` | 否 | object | 业务上下文（操作员、门店、场景等） |

### 3.3 measurements 字段

必须包含 6 条经络：`liver`、`spleen`、`kidney`、`stomach`、`gallbladder`、`bladder`

每条经络：

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `left` | **是** | number | 左侧温度值（°C） |
| `right` | **是** | number | 右侧温度值（°C） |
| `trendDelta` | 否 | number | 趋势值；不传则自动计算为 `right - left` |

兼容输入：也支持 `t1/t2` 格式（`left = t1`, `right = t2`）。

---

## 4. 响应规范

### 4.1 Rule 模式响应（`engine.mode = "rule-based-mvp"`）

纯规则引擎输出，确定性结果：

```json
{
  "engine": {
    "mode": "rule-based-mvp",
    "version": "0.2.0"
  },
  "subject": { "id": "张三", "name": "张三" },
  "context": {},
  "input": {
    "mode": "foot_six",
    "meridians": ["liver", "spleen", "kidney", "stomach", "gallbladder", "bladder"]
  },

  "healthScore": 46.0,

  "scores": {
    "liver": 46.0,
    "spleen": 46.0,
    "kidney": 46.0,
    "stomach": 46.0,
    "gallbladder": 46.0,
    "bladder": 46.0
  },

  "meridians": {
    "liver": {
      "status": "left_low",
      "score": 46.0,
      "symptoms": ["代谢差", "气虚", "乳房结节", "三高", "血稠", "难入睡"],
      "tags": ["left_low", "cross"]
    },
    "spleen": { "status": "left_low", "score": 46.0, "symptoms": ["..."], "tags": ["..."] },
    "kidney": { "status": "left_low", "score": 46.0, "symptoms": ["..."], "tags": ["..."] },
    "stomach": { "status": "left_low", "score": 46.0, "symptoms": ["..."], "tags": ["..."] },
    "gallbladder": { "status": "left_low", "score": 46.0, "symptoms": ["..."], "tags": ["..."] },
    "bladder": { "status": "left_low", "score": 46.0, "symptoms": ["..."], "tags": ["..."] }
  },

  "sixDimensionScores": [
    { "meridian": "liver", "score": 46.0, "tags": ["left_low", "cross"] },
    { "meridian": "spleen", "score": 46.0, "tags": ["left_low", "cross"] },
    { "meridian": "kidney", "score": 46.0, "tags": ["left_low", "cross"] },
    { "meridian": "stomach", "score": 46.0, "tags": ["left_low", "cross"] },
    { "meridian": "gallbladder", "score": 46.0, "tags": ["left_low", "cross"] },
    { "meridian": "bladder", "score": 46.0, "tags": ["left_low", "cross"] }
  ],

  "combinations": [
    {
      "id": "liver_gallbladder_left_low_transaminase",
      "name": "转氨酶偏高",
      "tags": ["transaminase", "liver_combo"],
      "summary": "肝左低 + 胆左低：提示转氨酶偏高/肝胆联动风险"
    },
    {
      "id": "kidney_bladder_same_side_low_lumbar",
      "name": "腰椎风险提示",
      "tags": ["lumbar"],
      "summary": "肾与膀胱同向低：提示腰椎相关问题倾向"
    },
    {
      "id": "left_side_four_plus_head_supply",
      "name": "头部供血注意",
      "tags": ["head_supply"],
      "summary": "六经中 4 条及以上偏左低：提示头部供血侧需关注"
    }
  ],

  "riskTags": ["left_low", "cross", "transaminase", "liver_combo", "lumbar", "head_supply"],

  "summary": "肝左低：代谢侧偏弱；脾左低：运化/思虑侧偏弱；...",
  "reportSummary": "（同 summary）",

  "advice": [
    "关注代谢与睡眠节律",
    "近期少油酒并观察眼干口苦是否持续",
    "..."
  ],

  "storefront": {
    "focusHeadline": "左侧偏低：重点关注 转氨酶偏高、腰椎风险提示",
    "clientExplanation": "...结果不等同于医疗诊断。",
    "talkTrack": [
      "这次主要看到的是经络侧的偏低/交叉信号，不等同于医疗诊断。",
      "更适合把它理解为体感、作息和左右差异的提示。",
      "建议结合近期状态，按 20-30 分钟间隔复测 2-3 次看趋势。"
    ],
    "retestPrompt": "建议间隔 20-30 分钟复测一次，连续 2-3 次趋势更可靠。"
  },

  "trace": {
    "perMeridian": { "liver": { "matchedRules": ["..."], "..." : "..." }, "...": {} },
    "thresholds": { "..." : "..." },
    "comboRulesMatched": ["..."]
  }
}
```

### 4.2 Hybrid 模式响应（`engine.mode = "hybrid"`）

在 rule 模式基础上，DeepSeek 生成自然语言替换/丰富以下字段：

```json
{
  "engine": {
    "mode": "hybrid",
    "version": "0.2.0",
    "llmModel": "deepseek-reasoner",
    "llmLatency": 12.35
  },

  // ---- 以下字段与 rule 模式完全一致（硬逻辑不变） ----
  "healthScore": 46.0,
  "scores": { "..." : "..." },
  "meridians": {
    "liver": {
      "status": "left_low",
      "score": 46.0,
      "symptoms": ["代谢差", "气虚", "..."],
      "tags": ["left_low", "cross"],
      "narrative": "肝经左侧温度偏低，提示代谢功能和气的运行可能偏弱..."
    },
    "...": {}
  },
  "combinations": ["..."],
  "riskTags": ["..."],
  "sixDimensionScores": ["..."],

  // ---- 以下字段由 DeepSeek 生成自然语言 ----
  "summary": "您的肝经和胆经左侧信号偏低，提示近期代谢和肝胆系统可能承受较大压力...",
  "reportSummary": "（同 summary）",

  "storefront": {
    "focusHeadline": "肝胆经络信号偏弱，建议重点关注",
    "clientExplanation": "本次检测发现肝经和胆经左侧温度偏低...结果不等同于医疗诊断。",
    "talkTrack": [
      "这次主要看到肝经和胆经信号偏低，可能跟近期作息有关。",
      "这个结果更像是身体状态的一个参考，不等同于医疗诊断。",
      "建议7到14天复测一次，看看趋势有没有变化。"
    ],
    "retestPrompt": "建议间隔一到两周复测..."
  },

  "recommendations": [
    "保证凌晨1-3点处于深睡状态，这是肝经修复的关键时段",
    "近期减少油腻饮食和酒精，减轻肝胆负担",
    "7-14天后复测观察趋势"
  ]
}
```

### 4.3 Fallback 模式（`engine.mode = "rule-fallback"`）

当 DeepSeek API 调用失败时，自动退回 rule 模式输出，并附加错误信息：

```json
{
  "engine": {
    "mode": "rule-fallback",
    "version": "0.2.0",
    "llmError": "DeepSeek API timed out after 60s (attempt 3)"
  },
  "...": "（其余字段与 rule 模式完全一致）"
}
```

---

## 5. 响应字段速查

### 5.1 顶层字段

| 字段 | 类型 | 说明 | 前端建议 |
|------|------|------|----------|
| `engine` | object | 引擎信息（模式、版本、LLM 延迟） | 调试 |
| `healthScore` | number | 综合健康评分（0-100） | **首屏展示** |
| `scores` | object | 各经络评分 map | **首屏展示** |
| `meridians` | object | 各经络详情（status、score、symptoms、tags） | **核心展示** |
| `sixDimensionScores` | array | 六经评分数组（同 scores，数组形式） | **雷达图** |
| `combinations` | array | 组合判症命中结果 | 展示 |
| `riskTags` | string[] | 全局风险标签 | 可选 |
| `summary` | string | 报告摘要 | 展示 |
| `reportSummary` | string | summary 的别名 | **推荐优先** |
| `advice` | string[] | 调理建议列表 | **展示** |
| `storefront` | object | 门店讲解层 | **门店展示** |
| `trace` | object | 调试信息（规则命中、阈值） | 仅调试 |

### 5.2 meridians.\<meridian\> 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | 主状态：`left_low` / `right_low` / `cross` / `stable` |
| `score` | number | 该经络评分（0-100） |
| `symptoms` | string[] | 匹配到的症状列表 |
| `tags` | string[] | 匹配到的标签 |
| `narrative` | string | （仅 hybrid）LLM 生成的自然语言描述 |

### 5.3 storefront 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `focusHeadline` | string | 一句话焦点标题，可直接展示 |
| `clientExplanation` | string | 面向客户的解释，必含"不等同于医疗诊断" |
| `talkTrack` | string[3] | 恰好 3 句口语化话术，可直接念给客户 |
| `retestPrompt` | string | 复测建议 |

### 5.4 combinations[] 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 规则 ID |
| `name` | string | 组合名称（如"转氨酶偏高"） |
| `tags` | string[] | 组合标签 |
| `summary` | string | 组合说明 |

### 5.5 健康评分算法

详细算法说明和计算示例见 [评分算法文档](../design/scoring-algorithm.md)。

简要规则：

- **单经评分**：基础分 100，`left_low`/`right_low` 扣 16，`cross` 扣 20，可叠加
- **组合扣分**：组合规则命中时，只对参与的经络扣 6 分
- **综合评分**：`healthScore = 六经单经评分的平均值`
- **范围**：0-100

| 等级 | 分数范围 |
|------|----------|
| 优秀 | 85-100 |
| 良好 | 70-84 |
| 注意 | 55-69 |
| 预警 | <55 |

---

## 6. 推理模式对比

| 维度 | rule 模式 | hybrid 模式 |
|------|-----------|-------------|
| 分数/状态/症状 | 规则引擎确定 | 规则引擎确定（不变） |
| summary | 规则拼接模板 | DeepSeek 自然语言 |
| storefront | 规则模板 | DeepSeek 自然语言 |
| recommendations | 规则模板 | DeepSeek 自然语言 |
| meridian narrative | 无 | DeepSeek 逐经描述 |
| 依赖 | 无外部依赖 | 需要 DEEPSEEK_API_KEY |
| 延迟 | <100ms | 10-30s（含 DeepSeek 调用） |
| 失败处理 | N/A | 自动 fallback 到 rule |

---

## 7. 调用示例

### 7.1 curl 基础调用

```bash
curl -X POST http://127.0.0.1:18790/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  -d '{
    "subject": {"id": "demo-001", "name": "张三"},
    "measurements": {
      "liver":       {"left": 35.2, "right": 36.2},
      "spleen":      {"left": 35.1, "right": 35.5},
      "kidney":      {"left": 35.0, "right": 35.9},
      "stomach":     {"left": 36.0, "right": 35.2},
      "gallbladder": {"left": 35.1, "right": 36.0},
      "bladder":     {"left": 36.1, "right": 35.2}
    }
  }'
```

### 7.2 使用 fixture 文件

```bash
curl -X POST http://127.0.0.1:18790/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  --data @fixtures/case_left_low.json
```

### 7.3 健康检查

```bash
curl http://127.0.0.1:18790/healthz
# {"status": "ok", "service": "tcm-meridian-api", "python": "3.12.x"}
```

### 7.4 服务信息

```bash
curl http://127.0.0.1:18790/
# {"service": "TCM Meridian Inference API", "version": "0.4.0", "inferMode": "rule", ...}
```

---

## 8. 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `TCM_API_PORT` | `18790` | 服务端口 |
| `TCM_INFER_MODE` | `auto` | 推理模式：`rule` / `agent` / `auto` |
| `DEEPSEEK_API_KEY` | （空） | DeepSeek API 密钥，hybrid 模式必需 |
| `DEEPSEEK_MODEL` | `deepseek-reasoner` | 使用的 DeepSeek 模型 |

---

## 9. 错误响应

| HTTP 状态码 | 场景 | 响应示例 |
|-------------|------|----------|
| 400 | 请求体 JSON 解析失败 | `{"error": "invalid JSON: ..."}` |
| 404 | 路由不存在 | `{"error": "not found"}` |
| 500 | 服务器内部错误 | `{"error": "..."}` |

---

## 10. 前端接入建议

### 首屏优先消费

- `healthScore` — 综合健康评分
- `reportSummary` — 报告摘要
- `sixDimensionScores` — 六经雷达图数据
- `storefront.focusHeadline` — 焦点标题
- `storefront.clientExplanation` — 客户解释
- `storefront.talkTrack` — 3 句话术

### 二级详情

- `meridians` — 各经络 status / symptoms / narrative
- `combinations` — 组合判症
- `advice` — 调理建议

### 仅调试

- `trace` — 规则命中详情、阈值参数
- `engine` — 引擎版本和模式信息
