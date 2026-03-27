# TCM Meridian Inference MVP API 文档

面向：Daniel / 前端 / 调用方  
项目：`tcm-meridian-inference-mvp`  
当前版本：`0.4.0`

---

## 1. 文档目的

本文档基于项目当前**真实实现**整理，面向前端和调用方提供可直接对接的 API 说明。

> 重要边界：当前服务是**规则驱动的轻量推理服务**（`rule-based-mvp`），不是训练型医学诊断模型，也不应被表述为临床诊断结论。

---

## 2. 服务能力概览

当前主要暴露以下接口：

1. `GET /healthz`：服务健康检查
2. `POST /api/inference/meridian-diagnosis`：六条经络规则推理主接口
3. `POST /api/rules/load`：查看当前加载规则库（简版说明，便于联调）

---

## 3. 关键口径（调用方必须知道）

### 3.1 这不是训练型医学诊断模型

返回结果来自：
- 显式输入字段 `left / right / trendDelta`
- 固定阈值与规则库
- 规则匹配、风险标签聚合、摘要与建议生成

因此更适合理解为：
- **规则解释 / 风险提示 / 门店沟通辅助 / 复测追踪**

而不是：
- 临床诊断
- AI 黑盒诊断
- 医学结论输出

### 3.2 “6条经络评分” 与 “6个分析角度评分” 不是一回事

当前接口里真正稳定输出的是：
- `sixDimensionScores`：**按 6 条经络**输出的评分数组
- `scores`：同一批数据的 map 形式，key 为经络英文名

这 6 个维度分别是：
- `liver`
- `spleen`
- `kidney`
- `stomach`
- `gallbladder`
- `bladder`

这里的 “six dimension” 在当前实现中，**本质上就是六条经络维度**，不是另一个独立的“六个分析角度体系”。

### 3.3 推荐前端优先消费稳定字段，而不是深挖 trace

对前端/调用方，优先使用：
- `sixDimensionScores`
- `scores`
- `reportSummary`
- `advice`
- `storefront.focusHeadline`
- `storefront.clientExplanation`
- `storefront.retestPrompt`

`trace` 更适合：
- 调试
- 验证规则命中
- 内部解释

不建议前端首屏直接依赖 `trace` 的深层结构做核心展示。

---

## 4. 接口一：GET /healthz

### 4.1 用途

用于健康检查、部署探活、网关或前端联通性确认。

### 4.2 请求信息

- **URL**: `/healthz`
- **Method**: `GET`
- **Content-Type**: 无要求

### 4.3 请求示例

```bash
curl http://127.0.0.1:8000/healthz
```

### 4.4 响应示例

```json
{
  "status": "ok"
}
```

### 4.5 字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `status` | string | 固定为 `ok` 表示服务可用 |

---

## 5. 接口二：POST /api/inference/meridian-diagnosis

这是当前项目的**主推理接口**。

---

### 5.1 用途

输入六条经络的测量数据，返回：
- 六条经络逐条推理结果
- 六条经络评分
- 报告摘要
- 建议列表
- 门店讲解文案
- 规则命中 trace

---

### 5.2 请求信息

- **URL**: `/api/inference/meridian-diagnosis`
- **Method**: `POST`
- **Content-Type**: `application/json`

---

### 5.3 请求体结构

```json
{
  "subject": { "id": "string", "name": "string" },
  "measurements": {
    "liver": { "left": 0, "right": 0, "trendDelta": 0 },
    "spleen": { "left": 0, "right": 0, "trendDelta": 0 },
    "kidney": { "left": 0, "right": 0, "trendDelta": 0 },
    "stomach": { "left": 0, "right": 0, "trendDelta": 0 },
    "gallbladder": { "left": 0, "right": 0, "trendDelta": 0 },
    "bladder": { "left": 0, "right": 0, "trendDelta": 0 }
  },
  "context": {},
  "ruleConfigPath": "string",
  "thresholds": {}
}
```

---

### 5.4 请求体字段说明

#### 顶层字段

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `subject` | 是 | object | 受测对象信息 |
| `subject.id` | 是 | string | 受测对象唯一标识 |
| `subject.name` | 否 | string | 展示名 |
| `measurements` | 是 | object | 六条经络测量数据 |
| `context` | 否 | object | 业务上下文，如操作员、门店、场景等 |
| `ruleConfigPath` | 否 | string | 指定外部规则文件路径；不传则走默认规则库或环境变量 |
| `thresholds` | 否 | object | 覆盖默认阈值的配置项 |

#### `measurements` 字段

主路径要求为**脚上六经**：
- `liver`
- `spleen`
- `kidney`
- `stomach`
- `gallbladder`
- `bladder`

每条经络推荐使用显式结构：

| 字段 | 必填 | 类型 | 说明 |
|---|---|---|---|
| `left` | 是 | number | 左侧测量值 |
| `right` | 是 | number | 右侧测量值 |
| `trendDelta` | 是 | number | 趋势值，由上游提供；当前服务直接消费，不在接口内二次推导 |

---

### 5.5 兼容输入说明

当前实现除推荐主路径外，还兼容两种旧格式：

#### 兼容模式 A：脚上六经 + `t1/t2`

当每条经络提供：
- `t1`
- `t2`

系统会按当前实现解释为：
- `left = t1`
- `right = t2`
- `trendDelta = t2 - t1`

输出中会标记：
- `input.mode = foot_six_legacy_pair`
- `input.compatibility.usedLegacyT1T2Proxy = true`

#### 兼容模式 B：旧六键 legacy payload

仍兼容以下旧键：
- `lung`
- `pericardium`
- `heart`
- `spleen`
- `liver`
- `kidney`

当前实现中的映射关系：
- `lung -> stomach`
- `pericardium -> gallbladder`
- `heart -> bladder`

输出中会标记：
- `input.mode = legacy_mapped`
- `input.compatibility.usedCompatibilityMapping = true`

> 注意：该映射仅用于旧 demo / 旧 API 兼容，不代表真实医学等价。

---

### 5.6 完整示例请求 JSON

以下示例来自项目真实 fixture：`fixtures/demo_case_01.json`

```json
{
  "subject": {
    "id": "demo-left-low-001",
    "name": "久坐加班型"
  },
  "context": {
    "intervalMinutes": 20,
    "operator": "store-demo",
    "scene": "连续加班、睡眠不足，演示左侧偏低型"
  },
  "measurements": {
    "liver": { "left": 35.0, "right": 36.1, "trendDelta": -0.2 },
    "spleen": { "left": 35.1, "right": 35.8, "trendDelta": -0.1 },
    "kidney": { "left": 35.0, "right": 35.9, "trendDelta": -0.7 },
    "stomach": { "left": 35.2, "right": 35.9, "trendDelta": -0.2 },
    "gallbladder": { "left": 35.1, "right": 36.0, "trendDelta": -0.1 },
    "bladder": { "left": 36.0, "right": 35.2, "trendDelta": -0.5 }
  }
}
```

---

### 5.7 完整示例响应 JSON

> 说明：下面示例基于当前项目真实实现运行结果整理，重点完整覆盖：
> - 6 条经络评分
> - 报告摘要
> - 建议
> - 前端常用字段
> - 每条经络的核心结果结构
>
> `trace` 在真实响应中还会包含更长的规则命中详情；这里保留当前对接最关键的真实字段结构。

```json
{
  "meridianResults": {
    "liver": {
      "label": "肝经",
      "status": "warning",
      "riskLevel": "high",
      "trend": "stable",
      "sideState": "left_low",
      "riskScore": 72,
      "measurements": {
        "left": 35.0,
        "right": 36.1,
        "trendDelta": -0.2,
        "t1": 35.0,
        "t2": 36.1,
        "delta": -0.2
      },
      "signals": [
        "transaminase_attention",
        "hepatic_biliary_linkage",
        "metabolism_attention",
        "stress_heat_pattern",
        "sleep_disturbance_attention",
        "low_temp_signal",
        "left_right_asymmetry",
        "side_state:left_low"
      ],
      "ruleHits": [
        {
          "ruleId": "FSM-COMBO-LIVER-L-GB-L-022",
          "category": "combination",
          "riskLevel": "high",
          "explanation": "肝经与胆经同时左低，属于 Excel 明确给出的组合规则，应优先提示肝胆同向失衡。"
        },
        {
          "ruleId": "FSM-LIVER-LEFT-LOW-001",
          "category": "single_meridian",
          "riskLevel": "medium",
          "explanation": "肝经左侧偏低时，优先提示疏泄/代谢侧负担偏大。"
        }
      ],
      "recommendations": [
        "肝经出现左右偏低/失衡信号，建议结合复测与问询确认。",
        "建议结合近期作息、情绪压力和饮酒情况做问询。"
      ],
      "storefront": {
        "focus": "肝经是本次优先关注项之一。",
        "simpleExplanation": "肝经与胆经同时左低，属于 Excel 明确给出的组合规则，应优先提示肝胆同向失衡。",
        "careHint": "肝经出现左右偏低/失衡信号，建议结合复测与问询确认。"
      }
    },
    "spleen": {
      "label": "脾经",
      "status": "watch",
      "riskLevel": "medium",
      "trend": "stable",
      "sideState": "left_low",
      "riskScore": 72,
      "measurements": {
        "left": 35.1,
        "right": 35.8,
        "trendDelta": -0.1,
        "t1": 35.1,
        "t2": 35.8,
        "delta": -0.1
      },
      "signals": [
        "limb_fatigue_attention",
        "overthinking_attention",
        "glucose_attention",
        "low_temp_signal",
        "side_state:left_low"
      ],
      "ruleHits": [
        {
          "ruleId": "FSM-SPLEEN-LEFT-LOW-004",
          "category": "single_meridian",
          "riskLevel": "medium",
          "explanation": "脾经左低优先指向运化与四肢支持侧偏弱。"
        }
      ],
      "recommendations": [
        "脾经出现左右偏低/失衡信号，建议结合复测与问询确认。",
        "建议关注饮食规律，减少过甜、过冷饮食。"
      ],
      "storefront": {
        "focus": "脾经是本次优先关注项之一。",
        "simpleExplanation": "脾经左低优先指向运化与四肢支持侧偏弱。",
        "careHint": "脾经出现左右偏低/失衡信号，建议结合复测与问询确认。"
      }
    },
    "kidney": {
      "label": "肾经",
      "status": "warning",
      "riskLevel": "high",
      "trend": "down_strong",
      "sideState": "left_low",
      "riskScore": 85,
      "measurements": {
        "left": 35.0,
        "right": 35.9,
        "trendDelta": -0.7,
        "t1": 35.0,
        "t2": 35.9,
        "delta": -0.7
      },
      "signals": [
        "cervical_attention",
        "kidney_bladder_cross_linkage",
        "uric_acid_attention",
        "hearing_attention",
        "kidney_yin_deficiency_attention",
        "kidney_decline_trend",
        "fatigue_recovery_attention",
        "low_temp_signal",
        "left_right_asymmetry",
        "trend:down_strong",
        "side_state:left_low"
      ],
      "ruleHits": [
        {
          "ruleId": "FSM-COMBO-KIDNEY-L-BLADDER-R-023",
          "category": "combination",
          "riskLevel": "high",
          "explanation": "左肾低叠加右膀胱低，属于肾膀胱交叉组合。"
        },
        {
          "ruleId": "FSM-KIDNEY-LEFT-LOW-007",
          "category": "single_meridian",
          "riskLevel": "high",
          "explanation": "肾经左低是首批规则中的高优先级项。"
        },
        {
          "ruleId": "FSM-KIDNEY-DOWN-STRONG-020",
          "category": "trend",
          "riskLevel": "high",
          "explanation": "肾经在短时复测中明显下降。"
        }
      ],
      "recommendations": [
        "肾经出现左右偏低/失衡信号，建议结合复测与问询确认。",
        "建议结合夜尿、耳鸣、腰膝酸软、尿酸指标做复核。"
      ],
      "storefront": {
        "focus": "肾经是本次优先关注项之一。",
        "simpleExplanation": "左肾低叠加右膀胱低，属于肾膀胱交叉组合。",
        "careHint": "肾经出现左右偏低/失衡信号，建议结合复测与问询确认。"
      }
    },
    "stomach": {
      "label": "胃经",
      "status": "observe",
      "riskLevel": "low",
      "trend": "stable",
      "sideState": "left_low",
      "riskScore": 72,
      "measurements": {
        "left": 35.2,
        "right": 35.9,
        "trendDelta": -0.2,
        "t1": 35.2,
        "t2": 35.9,
        "delta": -0.2
      },
      "signals": [
        "fluid_deficiency_attention",
        "chronic_gastritis_attention",
        "low_temp_signal",
        "side_state:left_low"
      ],
      "ruleHits": [
        {
          "ruleId": "FSM-STOMACH-LEFT-LOW-010",
          "category": "single_meridian",
          "riskLevel": "low",
          "explanation": "胃经左低当前作为低优先级辅助规则保留。"
        }
      ],
      "recommendations": [
        "胃经出现左右偏低/失衡信号，建议结合复测与问询确认。",
        "建议结合早餐规律、胃胀、反酸、口渴等信息判断。"
      ],
      "storefront": {
        "focus": "胃经是本次优先关注项之一。",
        "simpleExplanation": "胃经左低当前作为低优先级辅助规则保留。",
        "careHint": "胃经出现左右偏低/失衡信号，建议结合复测与问询确认。"
      }
    },
    "gallbladder": {
      "label": "胆经",
      "status": "warning",
      "riskLevel": "high",
      "trend": "stable",
      "sideState": "left_low",
      "riskScore": 72,
      "measurements": {
        "left": 35.1,
        "right": 36.0,
        "trendDelta": -0.1,
        "t1": 35.1,
        "t2": 36.0,
        "delta": -0.1
      },
      "signals": [
        "transaminase_attention",
        "hepatic_biliary_linkage",
        "bilirubin_attention",
        "migraine_attention",
        "bitter_mouth_attention",
        "low_temp_signal",
        "left_right_asymmetry",
        "side_state:left_low"
      ],
      "ruleHits": [
        {
          "ruleId": "FSM-COMBO-LIVER-L-GB-L-022",
          "category": "combination",
          "riskLevel": "high",
          "explanation": "肝经与胆经同时左低，属于组合规则。"
        },
        {
          "ruleId": "FSM-GALLBLADDER-LEFT-LOW-013",
          "category": "single_meridian",
          "riskLevel": "medium",
          "explanation": "胆经左低优先提示胆红素方向、口苦、偏头痛等关注点。"
        }
      ],
      "recommendations": [
        "胆经出现左右偏低/失衡信号，建议结合复测与问询确认。",
        "建议结合口苦、叹气、偏头痛、睡眠质量等情况复核。"
      ],
      "storefront": {
        "focus": "胆经是本次优先关注项之一。",
        "simpleExplanation": "肝经与胆经同时左低，属于组合规则。",
        "careHint": "胆经出现左右偏低/失衡信号，建议结合复测与问询确认。"
      }
    },
    "bladder": {
      "label": "膀胱经",
      "status": "warning",
      "riskLevel": "high",
      "trend": "down_mild",
      "sideState": "right_low",
      "riskScore": 72,
      "measurements": {
        "left": 36.0,
        "right": 35.2,
        "trendDelta": -0.5,
        "t1": 36.0,
        "t2": 35.2,
        "delta": -0.5
      },
      "signals": [
        "cervical_attention",
        "kidney_bladder_cross_linkage",
        "neck_shoulder_waist_attention",
        "lung_attention",
        "low_temp_signal",
        "trend:down_mild",
        "side_state:right_low"
      ],
      "ruleHits": [
        {
          "ruleId": "FSM-COMBO-KIDNEY-L-BLADDER-R-023",
          "category": "combination",
          "riskLevel": "high",
          "explanation": "左肾低叠加右膀胱低，属于肾膀胱交叉组合。"
        },
        {
          "ruleId": "FSM-BLADDER-RIGHT-LOW-017",
          "category": "single_meridian",
          "riskLevel": "medium",
          "explanation": "膀胱经右低适合作为肩颈腰与肺部/泌尿系统联动关注提示。"
        }
      ],
      "recommendations": [
        "膀胱经出现左右偏低/失衡信号，建议结合复测与问询确认。",
        "建议结合久坐、颈肩僵硬、腰痛和泌尿系统情况复核。"
      ],
      "storefront": {
        "focus": "膀胱经是本次优先关注项之一。",
        "simpleExplanation": "左肾低叠加右膀胱低，属于肾膀胱交叉组合。",
        "careHint": "膀胱经出现左右偏低/失衡信号，建议结合复测与问询确认。"
      }
    }
  },
  "sixDimensionScores": [
    {
      "meridian": "liver",
      "label": "肝经",
      "score": 28,
      "riskScore": 72,
      "riskLevel": "high",
      "status": "warning",
      "sideState": "left_low",
      "trend": "stable"
    },
    {
      "meridian": "spleen",
      "label": "脾经",
      "score": 28,
      "riskScore": 72,
      "riskLevel": "medium",
      "status": "watch",
      "sideState": "left_low",
      "trend": "stable"
    },
    {
      "meridian": "kidney",
      "label": "肾经",
      "score": 15,
      "riskScore": 85,
      "riskLevel": "high",
      "status": "warning",
      "sideState": "left_low",
      "trend": "down_strong"
    },
    {
      "meridian": "stomach",
      "label": "胃经",
      "score": 28,
      "riskScore": 72,
      "riskLevel": "low",
      "status": "observe",
      "sideState": "left_low",
      "trend": "stable"
    },
    {
      "meridian": "gallbladder",
      "label": "胆经",
      "score": 28,
      "riskScore": 72,
      "riskLevel": "high",
      "status": "warning",
      "sideState": "left_low",
      "trend": "stable"
    },
    {
      "meridian": "bladder",
      "label": "膀胱经",
      "score": 28,
      "riskScore": 72,
      "riskLevel": "high",
      "status": "warning",
      "sideState": "right_low",
      "trend": "down_mild"
    }
  ],
  "scores": {
    "liver": { "meridian": "liver", "label": "肝经", "score": 28, "riskScore": 72, "riskLevel": "high", "status": "warning", "sideState": "left_low", "trend": "stable" },
    "spleen": { "meridian": "spleen", "label": "脾经", "score": 28, "riskScore": 72, "riskLevel": "medium", "status": "watch", "sideState": "left_low", "trend": "stable" },
    "kidney": { "meridian": "kidney", "label": "肾经", "score": 15, "riskScore": 85, "riskLevel": "high", "status": "warning", "sideState": "left_low", "trend": "down_strong" },
    "stomach": { "meridian": "stomach", "label": "胃经", "score": 28, "riskScore": 72, "riskLevel": "low", "status": "observe", "sideState": "left_low", "trend": "stable" },
    "gallbladder": { "meridian": "gallbladder", "label": "胆经", "score": 28, "riskScore": 72, "riskLevel": "high", "status": "warning", "sideState": "left_low", "trend": "stable" },
    "bladder": { "meridian": "bladder", "label": "膀胱经", "score": 28, "riskScore": 72, "riskLevel": "high", "status": "warning", "sideState": "right_low", "trend": "down_mild" }
  },
  "riskTags": [
    "head_blood_supply_attention",
    "left_side_bias_pattern",
    "multi_meridian_imbalance",
    "cold_or_deficiency_pattern"
  ],
  "recommendations": [
    "建议作为全局 riskTag 输出，并提示复测确认。",
    "建议结合头晕、头痛、睡眠和颈肩状态复核。",
    "肝经与胆经同时左低，属于 Excel 明确给出的组合规则，应优先提示肝胆同向失衡。",
    "左肾低叠加右膀胱低，属于肾膀胱交叉组合，Excel 明确提示与颈椎问题关联。",
    "存在多经络联动失衡，建议门店复测并结合问诊确认。",
    "部分经络呈明显下降/偏低，建议优先保暖、休息、规律饮食。"
  ],
  "advice": [
    "建议作为全局 riskTag 输出，并提示复测确认。",
    "建议结合头晕、头痛、睡眠和颈肩状态复核。",
    "肝经与胆经同时左低，属于 Excel 明确给出的组合规则，应优先提示肝胆同向失衡。",
    "左肾低叠加右膀胱低，属于肾膀胱交叉组合，Excel 明确提示与颈椎问题关联。",
    "存在多经络联动失衡，建议门店复测并结合问诊确认。",
    "部分经络呈明显下降/偏低，建议优先保暖、休息、规律饮食。"
  ],
  "summary": "本次推理共评估6条经络，重点关注：肾经、肝经、胆经。全局风险标签为：head_blood_supply_attention、left_side_bias_pattern、multi_meridian_imbalance、cold_or_deficiency_pattern。",
  "reportSummary": "本次推理共评估6条经络，重点关注：肾经、肝经、胆经。全局风险标签为：head_blood_supply_attention、left_side_bias_pattern、multi_meridian_imbalance、cold_or_deficiency_pattern。",
  "storefront": {
    "focusItems": [
      {
        "meridian": "kidney",
        "label": "肾经",
        "riskLevel": "high",
        "sideState": "left_low",
        "trend": "down_strong",
        "reason": "左肾低叠加右膀胱低，属于肾膀胱交叉组合，Excel 明确提示与颈椎问题关联。"
      },
      {
        "meridian": "liver",
        "label": "肝经",
        "riskLevel": "high",
        "sideState": "left_low",
        "trend": "stable",
        "reason": "肝经与胆经同时左低，属于 Excel 明确给出的组合规则，应优先提示肝胆同向失衡。"
      },
      {
        "meridian": "gallbladder",
        "label": "胆经",
        "riskLevel": "high",
        "sideState": "left_low",
        "trend": "stable",
        "reason": "肝经与胆经同时左低，属于 Excel 明确给出的组合规则，应优先提示肝胆同向失衡。"
      }
    ],
    "focusHeadline": "本次重点关注：肾经、肝经、胆经。",
    "clientExplanation": "从本次脚上六经结果看，主要是肾经、肝经、胆经出现了更明显的左右偏低或波动信号。这更适合解读为当前身体节律与负担分配需要关注，不等同于医疗诊断。",
    "retestPrompt": "建议结合最近作息、压力、饮食和身体感受，7-14 天内复测一次，看看这些信号是不是持续。",
    "conditioningPrompt": "现阶段建议先从肾经、肝经相关的作息恢复、保暖和饮食节律入手，先做轻调整，再看复测变化。",
    "talkTrack": [
      "本次重点关注：肾经、肝经、胆经。",
      "这次更像是头颈循环信号需要关注，必要时再结合问询把重点缩到 1-2 个方向。",
      "建议结合最近作息、压力、饮食和身体感受，7-14 天内复测一次，看看这些信号是不是持续。"
    ]
  },
  "trace": {
    "thresholds": {
      "significant_drop": -0.6,
      "mild_drop": -0.3,
      "significant_rise": 0.6,
      "mild_rise": 0.3,
      "low_temp": 35.3,
      "high_temp": 37.0,
      "high_abs_delta": 0.8,
      "multi_meridian_risk_count": 2,
      "cross_low_delta": 0.8,
      "cross_low_upper_temp": 35.8
    },
    "flaggedMeridians": ["liver", "spleen", "kidney", "gallbladder", "bladder"],
    "globalRuleHits": [
      { "ruleId": "FSM-AGG-LEFT-LOW-COUNT-028", "category": "aggregate", "riskLevel": "high" },
      { "ruleId": "FSM-COMBO-LIVER-L-GB-L-022", "category": "combination", "riskLevel": "high" },
      { "ruleId": "FSM-COMBO-KIDNEY-L-BLADDER-R-023", "category": "combination", "riskLevel": "high" }
    ],
    "assumptions": [
      "Excel 内容更像门店解读话术和经验规则，不等同于医学诊断标准。",
      "新主路径使用显式 left/right/trendDelta；仅兼容模式下才允许 t1/t2 代理 left/right 与趋势。",
      "cross_low 运行假设：当左右绝对差 >= cross_low_delta 且较低侧 <= cross_low_upper_temp 时，判定为交叉性偏低/显著失衡。"
    ]
  },
  "subject": {
    "id": "demo-left-low-001",
    "name": "久坐加班型"
  },
  "context": {
    "intervalMinutes": 20,
    "operator": "store-demo",
    "scene": "连续加班、睡眠不足，演示左侧偏低型"
  },
  "input": {
    "mode": "foot_six_explicit",
    "compatibility": {
      "usedCompatibilityMapping": false,
      "usedLegacyT1T2Proxy": false,
      "inputContract": {
        "primaryMode": "foot_six_explicit",
        "activeMode": "foot_six_explicit",
        "measurementSpec": {
          "explicit": { "required": ["left", "right", "trendDelta"] },
          "legacyPair": { "supported": true, "fields": ["t1", "t2"] }
        },
        "semantics": {
          "left_low": "左侧值偏低",
          "right_low": "右侧值偏低",
          "cross_low": "左右差异显著且较低侧落入偏低区间",
          "trend": "使用显式 trendDelta 解释变化趋势；仅兼容模式下允许由 t2-t1 代理"
        },
        "compatibilityFlags": {
          "usedCompatibilityMapping": false,
          "usedLegacyT1T2Proxy": false
        }
      }
    },
    "meridians": ["liver", "spleen", "kidney", "stomach", "gallbladder", "bladder"],
    "measurementSemantics": {
      "primary": ["left", "right", "trendDelta"],
      "compatibility": ["t1", "t2"]
    }
  },
  "engine": {
    "name": "tcm-meridian-inference-mvp",
    "mode": "rule-based-mvp",
    "version": "0.4.0",
    "ruleConfigSource": "/home/aa/clawd/projects/tcm-meridian-inference-mvp/knowledge/expert_rules/foot_six_meridian.rule_set.core.json",
    "ruleSetId": "foot-six-meridian-core-v1",
    "ruleSetStatus": "draft-core-usable"
  }
}
```

---

### 5.8 响应字段说明（前端重点版）

#### A. 顶层核心字段

| 字段 | 类型 | 说明 | 前端建议 |
|---|---|---|---|
| `sixDimensionScores` | array | 六条经络评分数组，顺序固定 | **强烈推荐直接使用** |
| `scores` | object | 六条经络评分 map，按经络名索引 | **强烈推荐直接使用** |
| `summary` | string | 报告摘要 | 可用 |
| `reportSummary` | string | `summary` 的稳定别名 | **推荐优先使用** |
| `recommendations` | string[] | 建议列表 | 可用 |
| `advice` | string[] | `recommendations` 的稳定别名 | **推荐优先使用** |
| `riskTags` | string[] | 全局风险标签 | 可选展示 / 内部使用 |
| `storefront` | object | 更适合门店或前端展示的话术层 | **推荐使用** |
| `meridianResults` | object | 每条经络的详细解释结果 | 二级详情页适合 |
| `trace` | object | 规则命中、阈值、假设、调试信息 | 调试优先 |
| `input` | object | 输入模式与兼容标记 | 调试 / 排查 |
| `engine` | object | 引擎版本、模式、规则库来源 | 调试 / 追踪 |

#### B. `sixDimensionScores[]` 字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `meridian` | string | 经络英文 key |
| `label` | string | 经络中文名 |
| `score` | number | 展示分数，当前实现为 `100 - riskScore` |
| `riskScore` | number | 风险分 |
| `riskLevel` | string | 风险等级：`low / medium / high` |
| `status` | string | 当前状态：如 `observe / watch / warning / balanced` |
| `sideState` | string | 左右侧状态，如 `left_low / right_low / cross_low / balanced` |
| `trend` | string | 趋势，如 `stable / down_mild / down_strong / up_mild / up_strong` |

#### C. `storefront` 字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `focusItems` | array | 本次重点关注的前 3 个经络 |
| `focusHeadline` | string | 一句话重点关注 |
| `clientExplanation` | string | 面向客户/用户的解释，明确保留“非诊断”边界 |
| `retestPrompt` | string | 复测建议 |
| `conditioningPrompt` | string | 调理建议（轻建议） |
| `talkTrack` | string[] | 3 句可直接口播的话术 |

#### D. `meridianResults.<meridian>` 字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `label` | string | 经络中文名 |
| `status` | string | 该经络状态 |
| `riskLevel` | string | 风险等级 |
| `trend` | string | 趋势判断 |
| `sideState` | string | 左右状态判断 |
| `riskScore` | number | 风险分 |
| `measurements` | object | 该经络的测量值及兼容字段 |
| `signals` | string[] | 命中信号标签 |
| `ruleHits` | array | 命中规则列表 |
| `recommendations` | string[] | 该经络局部建议 |
| `storefront` | object | 该经络的轻解释字段 |

---

### 5.9 前端最应消费的字段清单

如果前端只做一版稳定接入，建议优先消费以下字段：

#### 首屏推荐
- `reportSummary`
- `advice`
- `sixDimensionScores`
- `storefront.focusHeadline`
- `storefront.clientExplanation`
- `storefront.retestPrompt`
- `storefront.conditioningPrompt`

#### 二级详情推荐
- `scores`
- `meridianResults`
- `storefront.focusItems`

#### 调试或内部面板
- `riskTags`
- `trace.globalRuleHits`
- `trace.thresholds`
- `input.mode`
- `input.compatibility`
- `engine.ruleSetId`
- `engine.ruleConfigSource`

---

### 5.10 curl 调用示例

#### 基础调用

```bash
curl -X POST http://127.0.0.1:8000/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  --data @fixtures/demo_case_01.json
```

#### 内联 JSON 调用

```bash
curl -X POST http://127.0.0.1:8000/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  -d '{
    "subject": {"id": "demo-left-low-001", "name": "久坐加班型"},
    "context": {"intervalMinutes": 20, "operator": "store-demo"},
    "measurements": {
      "liver": {"left": 35.0, "right": 36.1, "trendDelta": -0.2},
      "spleen": {"left": 35.1, "right": 35.8, "trendDelta": -0.1},
      "kidney": {"left": 35.0, "right": 35.9, "trendDelta": -0.7},
      "stomach": {"left": 35.2, "right": 35.9, "trendDelta": -0.2},
      "gallbladder": {"left": 35.1, "right": 36.0, "trendDelta": -0.1},
      "bladder": {"left": 36.0, "right": 35.2, "trendDelta": -0.5}
    }
  }'
```

#### 覆盖阈值示例

```bash
curl -X POST http://127.0.0.1:8000/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  -d '{
    "subject": {"id": "demo-override-001"},
    "measurements": {
      "liver": {"left": 35.0, "right": 36.1, "trendDelta": -0.2},
      "spleen": {"left": 35.1, "right": 35.8, "trendDelta": -0.1},
      "kidney": {"left": 35.0, "right": 35.9, "trendDelta": -0.7},
      "stomach": {"left": 35.2, "right": 35.9, "trendDelta": -0.2},
      "gallbladder": {"left": 35.1, "right": 36.0, "trendDelta": -0.1},
      "bladder": {"left": 36.0, "right": 35.2, "trendDelta": -0.5}
    },
    "thresholds": {
      "low_temp": 35.4,
      "cross_low_delta": 0.9
    }
  }'
```

---

### 5.11 错误响应说明

当前实现里常见错误分三类：

#### 1）请求体结构错误 / 字段缺失 / 类型不对

来源：
- Pydantic 请求体验证
- 自定义 `ValidationError`

HTTP 状态码通常为：`422`

##### 示例：缺少 `subject.id`

```json
{
  "detail": "subject.id is required"
}
```

##### 示例：缺少某条经络

```json
{
  "detail": "measurements must provide foot six meridians ['liver', 'spleen', 'kidney', 'stomach', 'gallbladder', 'bladder']; missing: ['bladder']"
}
```

##### 示例：显式模式缺少 `trendDelta`

```json
{
  "detail": "measurements.liver.trendDelta is required when using explicit left/right input"
}
```

#### 2）规则文件加载失败

来源：
- `ruleConfigPath` 无效
- 外部规则文件格式错误

HTTP 状态码：`400`

```json
{
  "detail": "<具体规则配置错误信息>"
}
```

#### 3）路由不存在

HTTP 状态码：`404`

```json
{
  "detail": "Not Found"
}
```

---

## 6. 接口三：POST /api/rules/load（简版）

这个接口不是主业务推理接口，但对联调非常有帮助，可以查看当前规则库是否加载成功。

### 6.1 用途

返回当前规则配置来源、规则集 ID、阈值、规则 ID 清单、经络列表等。

### 6.2 请求信息

- **URL**: `/api/rules/load`
- **Method**: `POST`
- **Content-Type**: `application/json`

### 6.3 请求体

```json
{
  "path": "string"
}
```

- `path` 可选；不传则使用默认规则库或环境变量 `TCM_RULE_CONFIG`

### 6.4 curl 示例

```bash
curl -X POST http://127.0.0.1:8000/api/rules/load \
  -H 'Content-Type: application/json' \
  -d '{}'
```

### 6.5 响应示例

```json
{
  "source": "/home/aa/clawd/projects/tcm-meridian-inference-mvp/knowledge/expert_rules/foot_six_meridian.rule_set.core.json",
  "ruleSetId": "foot-six-meridian-core-v1",
  "status": "draft-core-usable",
  "thresholds": {
    "significant_drop": -0.6,
    "mild_drop": -0.3,
    "significant_rise": 0.6,
    "mild_rise": 0.3,
    "low_temp": 35.3,
    "high_temp": 37.0,
    "high_abs_delta": 0.8,
    "multi_meridian_risk_count": 2,
    "cross_low_delta": 0.8,
    "cross_low_upper_temp": 35.8
  },
  "ruleIds": ["..."],
  "meridians": ["bladder", "gallbladder", "kidney", "liver", "spleen", "stomach"],
  "assumptions": ["..."]
}
```

### 6.6 字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `source` | string | 当前规则库来源路径 |
| `ruleSetId` | string | 规则集 ID |
| `status` | string | 规则集状态 |
| `thresholds` | object | 当前生效阈值 |
| `ruleIds` | string[] | 当前可用规则 ID 列表 |
| `meridians` | string[] | 当前规则覆盖的经络 |
| `assumptions` | string[] | 当前规则库假设/限制 |

---

## 7. 字段语义补充

### 7.1 `score` 与 `riskScore`

当前实现：
- `riskScore` 越高，风险越高
- `score = 100 - riskScore`

因此：
- `score` 更适合展示为“健康分/稳定分”
- `riskScore` 更适合规则计算和排序

### 7.2 `status` 与 `riskLevel`

两者不是同一个字段：

- `riskLevel`: `low / medium / high`
- `status`: `balanced / observe / watch / warning`

可以理解为：
- `riskLevel` 更像等级
- `status` 更像前端展示态

### 7.3 `sideState`

当前实现可能值包括：
- `balanced`
- `left_low`
- `right_low`
- `cross_low`
- `bilateral_low`
- `left_high`
- `right_high`

### 7.4 `trend`

当前实现可能值包括：
- `stable`
- `down_mild`
- `down_strong`
- `up_mild`
- `up_strong`

---

## 8. 已知约束 / 注意事项

以下内容来自当前真实实现，建议调用方明确知晓：

1. **当前是规则驱动 MVP，不是训练型医学诊断模型。**
   - `engine.mode` 当前固定为 `rule-based-mvp`
   - 输出只能理解为规则提示、风险提示、复测辅助

2. **推荐主输入是脚上六经 + 显式 `left/right/trendDelta`。**
   - 当前实现已经把它作为主路径
   - `trendDelta` 需要上游明确提供

3. **`t1/t2` 仍可兼容，但只是过渡口径。**
   - 当前兼容逻辑会将 `t1/t2` 代理为 `left/right`
   - 不建议新接入方继续使用该模式

4. **旧六键 `lung / pericardium / heart ...` 的兼容映射不代表真实医学等价。**
   - 仅用于旧 demo / 旧 API 平滑过渡
   - 新接入不要基于这个映射做业务固化

5. **`cross_low` 当前仍带实现假设。**
   - 当前逻辑是：`abs(left-right) >= cross_low_delta` 且较低侧 `<= cross_low_upper_temp`
   - 若后续业务方对“交叉”的定义变化，结果会受影响

6. **胃经规则当前存在弱化口径。**
   - 规则库里胃经保留，但有 `pendingConfirmation`
   - 当前优先级低于肝/脾/肾/胆/膀胱

7. **`trace` 可用于调试，但不建议前端把它当成稳定展示 contract。**
   - `trace.featureSnapshot` / `trace.globalRuleHits` 对内部很有用
   - 但其深层细节更容易随规则库演进而变化

8. **建议前端优先消费别名字段 `reportSummary` 和 `advice`。**
   - 它们分别对应 `summary` 和 `recommendations`
   - 当前测试也明确覆盖了这两个别名字段

---

## 9. 推荐联调顺序

建议联调方按以下顺序：

1. `GET /healthz` 确认服务可用
2. `POST /api/rules/load` 确认规则库已正常加载
3. 用 `fixtures/demo_case_01.json` 调 `POST /api/inference/meridian-diagnosis`
4. 前端先对接：
   - `sixDimensionScores`
   - `reportSummary`
   - `advice`
   - `storefront.*`
5. 如需解释细节，再接 `meridianResults` 与 `trace`

---

## 10. 一句话结论

对接时把这个服务理解为：

> **一个基于六条经络输入、输出评分 + 摘要 + 建议 + 规则解释的规则型推理 API，而不是医学诊断模型接口。**
