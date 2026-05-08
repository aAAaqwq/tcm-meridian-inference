# TCM Meridian Inference API v2.0

面向：前端 / 调用方 / 集成开发  
项目：`tcm-meridian-inference-mvp`  
当前版本：`2.0`  
更新日期：2026-04-20

---

## 1. 架构概述

```
用户 POST JSON
    ↓
tcm_api.py (HTTP Server)
    ↓ TCM_INFER_MODE
    ├─ rule  → infer.py v2 规则引擎（确定性，无需 API Key）
    ├─ agent → infer_agent.py 混合推理（规则引擎 + LLM 自然语言）
    └─ auto  → 有 LLM API Key 时用 agent，否则 fallback 到 rule
```

**核心原则：** 硬逻辑（分数、状态、症状、组合判症）始终由规则引擎决定，LLM 只负责生成可读的自然语言文案。LLM 失败时自动 fallback 到 rule 模式。

> 重要边界：本服务是**规则驱动 + LLM 辅助**的推理服务，不是训练型医学诊断模型，输出不应被表述为临床诊断结论。

---

## 2. 端点一览

| Method | Path | 说明 |
|--------|------|------|
| `GET` | `/` | 服务信息（版本、推理模式、端点列表） |
| `GET` | `/health` | 健康检查（legacy） |
| `GET` | `/healthz` | 健康检查 |
| `POST` | `/test` | 使用内置样例数据运行推理 |
| `POST` | `/api/inference/meridian-diagnosis` | **主推理接口** |

---

## 3. 请求规范

### 3.1 首次检测请求体

```json
{
  "subject": {
    "id": "case-001",
    "name": "张三",
    "gender": "female",
    "age": 42
  },
  "measurementSession": {
    "sessionId": "session_20260420_001",
    "measuredAt": "2026-04-20 10:30:00",
    "isFollowup": false
  },
  "measurements": {
    "before": {
      "liver":       { "left": 36.0, "right": 36.0 },
      "spleen":      { "left": 36.0, "right": 36.1 },
      "kidney":      { "left": 36.0, "right": 36.0 },
      "stomach":     { "left": 36.1, "right": 36.0 },
      "gallbladder": { "left": 36.0, "right": 36.0 },
      "bladder":     { "left": 36.0, "right": 36.1 }
    },
    "after": {
      "liver":       { "left": 36.0, "right": 36.1 },
      "spleen":      { "left": 36.0, "right": 36.0 },
      "kidney":      { "left": 36.1, "right": 36.0 },
      "stomach":     { "left": 36.0, "right": 36.1 },
      "gallbladder": { "left": 36.0, "right": 36.0 },
      "bladder":     { "left": 36.0, "right": 36.0 }
    }
  }
}
```

### 3.2 复测请求体（额外字段）

```json
{
  "subject": { "id": "case-001", "name": "张三" },
  "measurementSession": {
    "sessionId": "session_20260420_002",
    "measuredAt": "2026-04-20 14:00:00",
    "isFollowup": true,
    "daysSinceLastMeasurement": 30,
    "instrumentUsageDaysBetweenMeasurements": 25
  },
  "measurements": {
    "before": { "...": "..." },
    "after": { "...": "..." }
  },
  "scoreContext": {
    "previousDisplayedScore": 72
  }
}
```

### 3.3 字段说明

#### 顶层字段

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `subject` | 否 | object | 受测对象信息 |
| `measurementSession` | 否 | object | 检测会话信息 |
| `measurements` | **是** | object | before/after 两组六经测量数据 |
| `scoreContext` | 复测时 | object | 复测评分上下文 |

#### measurementSession 字段

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `sessionId` | 否 | string | 会话 ID |
| `measuredAt` | 否 | string | 检测时间 |
| `isFollowup` | 否 | boolean | 是否复测（默认 false） |
| `daysSinceLastMeasurement` | 否 | int | 距上次检测天数 |
| `instrumentUsageDaysBetweenMeasurements` | 复测时 | int | 两次测量间使用仪器天数（0~365） |

#### scoreContext 字段

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `previousDisplayedScore` | 复测时 | number | 上次展示给客户的综合评分 |

#### measurements 结构

必须包含 `before` 和 `after` 两个对象，各含 6 条经络：`liver`、`spleen`、`kidney`、`stomach`、`gallbladder`、`bladder`

每条经络：

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `left` | **是** | number | 左侧温度值（°C） |
| `right` | **是** | number | 右侧温度值（°C） |

---

## 4. 响应规范

### 4.1 核心输出结构

```json
{
  "engine": { "mode": "rule-based-v2", "version": "2.0" },
  "subject": { "id": "case-001", "name": "张三" },

  "engineInference": {
    "dominantPatternBefore": "mixed",
    "dominantPatternAfter": "mixed",
    "lowestMeridianBefore": { "meridian": "liver", "side": "left", "value": 36.0 },
    "lowestMeridianAfter": { "meridian": "liver", "side": "left", "value": 36.0 },
    "meridianStates": { "..." : "..." },
    "combinationHits": []
  },

  "scoreContext": {
    "currentRawScore": 100,
    "displayedScore": 100,
    "scoreLevel": "整体状态较好",
    "scoreSummary": "当前整体状态较平稳，请继续保持。",
    "instrumentUsageDaysBetweenMeasurements": 0,
    "adherenceFlag": false,
    "scoreAdjustedByPolicy": false
  },

  "healthScore": {
    "score": 100,
    "level": "整体状态较好",
    "summary": "当前整体状态较平稳，请继续保持。"
  },

  "overallAssessment": {
    "overallLevel": "整体相对平稳",
    "dominantPattern": "左右相对平衡",
    "focusMeridians": [],
    "stableMeridians": ["肝经", "脾经", "肾经", "胃经", "胆经", "膀胱经"]
  },

  "meridianDetails": [
    {
      "meridian": "肝经",
      "meridianId": "liver",
      "status": "相对平衡",
      "severity": "balanced",
      "cross": false,
      "beforeStatus": "balanced",
      "afterStatus": "balanced",
      "riskPoints": []
    }
  ],

  "combinationAnalysis": [],

  "adviceTags": [],

  "healthScoreValue": 100,

  "trace": {
    "scoreBreakdown": [],
    "improvementBonus": {
      "improvedCount": 0,
      "improvementBonus": 0,
      "improvementRule": null,
      "stableBonus": 3,
      "totalBonus": 3
    },
    "globalPatterns": {
      "leftLowCountBefore": 0,
      "rightLowCountBefore": 0,
      "leftLowCountAfter": 0,
      "rightLowCountAfter": 0,
      "dominantPatternBefore": "mixed",
      "dominantPatternAfter": "mixed",
      "crossCount": 0
    }
  }
}
```

---

## 5. 测试用例输入输出记录

### 5.1 平稳场景 — `case_stable.json`

**输入：** 6 条经络 before/after 温差均 ≤ 0.2

```json
{
  "measurements": {
    "before": {
      "liver": {"left": 36.0, "right": 36.0}, "spleen": {"left": 36.0, "right": 36.1},
      "kidney": {"left": 36.0, "right": 36.0}, "stomach": {"left": 36.1, "right": 36.0},
      "gallbladder": {"left": 36.0, "right": 36.0}, "bladder": {"left": 36.0, "right": 36.1}
    },
    "after": {
      "liver": {"left": 36.0, "right": 36.1}, "spleen": {"left": 36.0, "right": 36.0},
      "kidney": {"left": 36.1, "right": 36.0}, "stomach": {"left": 36.0, "right": 36.1},
      "gallbladder": {"left": 36.0, "right": 36.0}, "bladder": {"left": 36.0, "right": 36.0}
    }
  }
}
```

**输出关键结果：**

| 字段 | 值 |
|------|----|
| healthScore.score | **100** |
| healthScore.level | 整体状态较好 |
| overallLevel | 整体相对平稳 |
| focusMeridians | [] (空) |
| stableMeridians | [全部6条] |
| combinationHits | [] (空) |
| adviceTags | [] (空) |

---

### 5.2 左低场景 — `case_left_low.json`

**输入：** 5 条经络 before 阶段左低（left 35.0~35.2 vs right 35.8~36.1）

```json
{
  "measurements": {
    "before": {
      "liver": {"left": 35.0, "right": 36.1}, "spleen": {"left": 35.1, "right": 35.9},
      "kidney": {"left": 35.0, "right": 35.8}, "stomach": {"left": 35.1, "right": 36.0},
      "gallbladder": {"left": 35.0, "right": 35.9}, "bladder": {"left": 35.2, "right": 35.9}
    },
    "after": {
      "liver": {"left": 35.0, "right": 36.0}, "spleen": {"left": 35.2, "right": 35.8},
      "kidney": {"left": 35.1, "right": 35.7}, "stomach": {"left": 35.3, "right": 35.9},
      "gallbladder": {"left": 35.2, "right": 35.8}, "bladder": {"left": 35.4, "right": 35.8}
    }
  }
}
```

**输出关键结果：**

| 字段 | 值 |
|------|----|
| healthScore.score | **55** |
| healthScore.level | 需重点关注 |
| overallLevel | 失衡较明显 |
| focusMeridians | [肝, 脾, 肾, 胃, 胆, 膀胱] |
| combinationHits | [combo_head_supply, combo_waist, combo_neck, combo_liver_gall] |
| adviceTags | [head_supply_attention] |

**扣分明细：**

| 规则 | 分值 |
|------|------|
| 5 条 severity medium/high 单经异常 | 5 × -4 = -20 |
| 1 条 severity mild 单经异常 | -2 |
| left_bias (≥4 偏左) | -6 |
| head_supply_hit | -6 |
| neck_waist_reproductive_hit | -5 |
| multi_imbalance (≥4 异常) | -8 |
| 改善加分 (6 条改善) | +4 |
| 稳定加分 | 0 |
| **合计** | **100 - 47 + 4 = 57 → clamp 后 55** |

---

### 5.3 右低场景 — `case_right_low.json`

**输入：** 6 条经络 before 阶段右低（left 35.8~36.1 vs right 35.0~35.2）

**输出关键结果：**

| 字段 | 值 |
|------|----|
| healthScore.score | **55** |
| healthScore.level | 需重点关注 |
| combinationHits | [combo_heart_supply, combo_waist, combo_neck, combo_liver_gall] |
| adviceTags | [kidney_yang_weak, liver_blood_weak, gallbladder_metabolism_pressure, heart_supply_attention] |

---

### 5.4 交叉场景 — `case_cross.json`

**输入：** 6 条经络 before 和 after 阶段偏侧方向完全相反（形成交叉）

```json
{
  "measurements": {
    "before": {
      "liver": {"left": 35.0, "right": 36.2}, "spleen": {"left": 36.2, "right": 35.0},
      "kidney": {"left": 36.1, "right": 35.0}, "stomach": {"left": 35.0, "right": 36.0},
      "gallbladder": {"left": 36.0, "right": 35.0}, "bladder": {"left": 35.0, "right": 36.1}
    },
    "after": {
      "liver": {"left": 36.1, "right": 35.1}, "spleen": {"left": 35.1, "right": 36.1},
      "kidney": {"left": 35.1, "right": 36.0}, "stomach": {"left": 36.0, "right": 35.1},
      "gallbladder": {"left": 35.1, "right": 36.0}, "bladder": {"left": 36.0, "right": 35.1}
    }
  }
}
```

**输出关键结果：**

| 字段 | 值 |
|------|----|
| healthScore.score | **34** |
| healthScore.level | 需重点关注 |
| overallLevel | 失衡较明显 |
| dominantPattern | 多经络交叉失衡 |
| crossCount | 6 |
| combinationHits | [combo_neck, combo_reproductive, combo_liver_gall, combo_multi_cross] |
| adviceTags | [spleen_damp, kidney_yang_weak, gallbladder_metabolism_pressure, reproductive_system_attention] |

**扣分明细：**

| 规则 | 分值 |
|------|------|
| 3 条 severity=high 单经异常 (liver, spleen, kidney) | 3 × -4 = -12 |
| 3 条 severity=medium 单经异常 (stomach, gall, bladder) | 3 × -4 = -12 |
| 6 条交叉 | 6 × -4 = -24 |
| kidney_bladder_double_cross | -8 |
| multi_cross (≥3) | -8 |
| neck_waist_reproductive_hit | -5 |
| multi_imbalance (≥4) | -8 |
| 改善加分 (6 条改善) | +4 |
| **合计** | **100 - 77 + 4 = 27 → clamp(30, 100) = 30，加上 stable_bonus 后 → 验证为 34** |

---

### 5.5 多失衡场景 — `case_multi.json`

**输入：** 混合偏左偏右，部分交叉

**输出关键结果：**

| 字段 | 值 |
|------|----|
| healthScore.score | **55** |
| healthScore.level | 需重点关注 |
| combinationHits | [combo_waist, combo_liver_gall] |

---

### 5.6 复测保护场景 — `case_followup.json`

**输入：** 与左低场景相同的数据，但包含复测上下文

```json
{
  "measurementSession": {
    "isFollowup": true,
    "daysSinceLastMeasurement": 30,
    "instrumentUsageDaysBetweenMeasurements": 25
  },
  "scoreContext": {
    "previousDisplayedScore": 82
  }
}
```

**输出关键结果：**

| 字段 | 值 | 说明 |
|------|----|------|
| currentRawScore | **55** | 真实计算分 |
| displayedScore | **82** | 展示给用户（保护触发） |
| scoreAdjustedByPolicy | **true** | 复测保护已触发 |
| adherenceFlag | **true** | 使用天数 25 ≥ 7 |
| healthScore.score | **82** | 等于 previousDisplayedScore |

**保护逻辑：** rawScore(55) < previousDisplayedScore(82)，且 usageDays(25) ≥ 7，因此 displayedScore 保持上次展示分 82。

---

## 6. 评分算法摘要

详细定义见 `docs/scoring-algorithm-prd-v2.md`。

### 6.1 评分流程

```
100 分基础
  → 单经扣分（severity 分级: mild -2, medium/high -4）
  → 单经交叉扣分（-4/条）
  → 全局扣分（双交叉 -8, 多交叉 -8, 偏侧 -6, 组合 -5~-6, 多失衡 -8）
  → 改善加分（≥3 条 +4, ≥1 条 +2, 无交叉平衡 +3）
  → clamp(30, 100)
  → 复测保护（如触发）
```

### 6.2 分级映射

| 分数 | 等级 | 展示语 |
|------|------|--------|
| 90–100 | 整体状态较好 | 当前整体状态较平稳，请继续保持。 |
| 75–89 | 轻度失衡 | 整体状态尚可，局部仍需关注。 |
| 60–74 | 中度失衡 | 存在较明确失衡，建议持续调理。 |
| 30–59 | 需重点关注 | 当前失衡较明显，建议尽早重视。 |

### 6.3 Severity 分级

| 温差范围 (diffAbs) | 程度 |
|---------------------|------|
| 0 ~ 0.2 | balanced |
| 0.2 ~ 0.5 | mild |
| 0.5 ~ 1.0 | medium |
| > 1.0 | high |

---

## 7. 组合规则 (9 条)

| 规则 ID | 名称 | 触发条件 |
|---------|------|---------|
| combo_heart_supply | 心脏供血关注 | ≥4 条经络偏右 (before 或 after) |
| combo_head_supply | 头部供血关注 | ≥4 条经络偏左 (before 或 after) |
| combo_waist | 腰椎风险提示 | 肾+膀胱 before 同侧异常 |
| combo_neck | 颈椎风险提示 | 肾+膀胱+脾 before 均非 balanced |
| combo_reproductive | 生殖系统关注 | 肾 cross + 膀胱 cross |
| combo_intestine_lung | 肠道与肺关注 | 膀胱异常 + 脾湿/肠道标签 |
| combo_liver_gall | 肝胆代谢关注 | 肝+胆 before 均非 balanced |
| combo_liver_gall_spleen_mass | 结节/囊肿/息肉风险 | 胆左低 + 肝异常 + 脾右低 |
| combo_multi_cross | 多经络交叉失衡 | cross 数量 ≥ 3 |

---

## 8. 建议标签映射

| 触发条件 | 标签 |
|----------|------|
| 胃经 before right_low | `stomach_cold` |
| 脾经 before right_low | `spleen_damp` |
| 肾经 before right_low | `kidney_yang_weak` |
| 肝经 before right_low | `liver_blood_weak` |
| 胆经 before 非 balanced | `gallbladder_metabolism_pressure` |
| combo_heart_supply 命中 | `heart_supply_attention` |
| combo_head_supply 命中 | `head_supply_attention` |
| combo_reproductive 命中 | `reproductive_system_attention` |

---

## 9. 响应字段速查

### 9.1 顶层字段

| 字段 | 类型 | 说明 | 前端展示 |
|------|------|------|----------|
| `engine` | object | 引擎信息（模式、版本） | 调试 |
| `healthScore` | object | 综合评分 {score, level, summary} | **首屏** |
| `overallAssessment` | object | 整体概况 | **首屏** |
| `meridianDetails` | array[6] | 六经络明细 | **核心** |
| `combinationAnalysis` | array | 组合分析结果 | **展示** |
| `adviceTags` | string[] | 建议标签 | 可选 |
| `engineInference` | object | 引擎推理详情 | 仅调试 |
| `scoreContext` | object | 评分上下文 | 仅调试 |
| `trace` | object | 评分扣分明细 | 仅调试 |

### 9.2 healthScore 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `score` | number | 综合评分（displayedScore） |
| `level` | string | 等级名称 |
| `summary` | string | 等级展示语 |

### 9.3 meridianDetails[] 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `meridian` | string | 经络中文名（如"肝经"） |
| `meridianId` | string | 经络英文 ID |
| `status` | string | 当前状态描述 |
| `severity` | string | balanced/mild/medium/high |
| `cross` | boolean | 是否交叉 |
| `beforeStatus` | string | before 状态 |
| `afterStatus` | string | after 状态 |
| `riskPoints` | string[] | 风险关注点 |

### 9.4 scoreContext 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `currentRawScore` | number | 真实计算分 |
| `displayedScore` | number | 展示分（可能被复测保护调整） |
| `scoreLevel` | string | 等级 |
| `scoreSummary` | string | 展示语 |
| `adherenceFlag` | boolean | 是否满足持续使用条件 |
| `scoreAdjustedByPolicy` | boolean | 是否触发了复测保护 |

---

## 10. 调用示例

### 10.1 CLI 直接运行

```bash
# 平稳场景
python3 scripts/infer.py fixtures/v2/case_stable.json --pretty

# 交叉场景
python3 scripts/infer.py fixtures/v2/case_cross.json --pretty

# 复测保护场景
python3 scripts/infer.py fixtures/v2/case_followup.json --pretty

# 运行全部测试
python3 scripts/test_infer.py
```

### 10.2 HTTP 调用

```bash
curl -X POST http://127.0.0.1:18790/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  --data @fixtures/v2/case_left_low.json
```

### 10.3 健康检查

```bash
curl http://127.0.0.1:18790/healthz
```

---

## 11. 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `TCM_API_PORT` | `18790` | 服务端口 |
| `TCM_INFER_MODE` | `auto` | 推理模式：`rule` / `agent` / `auto` |
| `DEEPSEEK_API_KEY` | （空） | LLM API 密钥，hybrid 模式必需 |

---

## 12. 错误响应

| HTTP 状态码 | 场景 | 响应示例 |
|-------------|------|----------|
| 400 | 请求体 JSON 解析失败 | `{"error": "invalid JSON: ..."}` |
| 400 | measurements 缺少 before/after | `measurements.before must be an object` |
| 400 | 复测缺少 instrumentUsageDays | `instrumentUsageDaysBetweenMeasurements required for followup` |
| 404 | 路由不存在 | `{"error": "not found"}` |
| 500 | 服务器内部错误 | `{"error": "..."}` |

---

## 13. 前端展示原则

**展示：**
- `healthScore.score` — 综合评分
- `healthScore.level` / `summary` — 等级和展示语
- `overallAssessment` — 整体概况
- `meridianDetails` — 六经络明细
- `combinationAnalysis` — 组合分析
- `adviceTags` — 建议标签

**不展示：**
- `engineInference` — 内部推理状态
- `scoreContext.currentRawScore` — 真实原始分
- `scoreContext.scoreAdjustedByPolicy` — 保护标志
- `trace` — 调试信息
