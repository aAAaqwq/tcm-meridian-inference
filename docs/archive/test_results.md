# TCM Meridian Inference v2.0 — Agent (Hybrid) 模式测试结果

> 测试日期：2026-04-20
> 推理模式：agent (hybrid = 规则引擎 + DeepSeek)
> 端点：`POST /api/inference/meridian-diagnosis`

---

## 测试汇总

| Case | 模式 | 评分 | 等级 | LLM 延迟 | 组合命中 | 建议标签数 |
|------|------|------|------|----------|----------|-----------|
| case_stable | hybrid | 100 | 整体状态较好 | 23.28s | 0 | 0 |
| case_left_low | hybrid | 55.0 | 需重点关注 | 30.62s | 4 | 2 |
| case_right_low | hybrid | 55.0 | 需重点关注 | 27.45s | 4 | 6 |
| case_cross | hybrid | 34 | 需重点关注 | 22.44s | 4 | 4 |
| case_multi | hybrid | 55.0 | 需重点关注 | 25.91s | 3 | 3 |
| case_followup | hybrid | 82 | 轻度失衡 | 28.7s | 4 | 2 |

---

## case_stable

### 输入

```json
{
  "subject": {
    "id": "v2-stable-001",
    "name": "平稳场景"
  },
  "measurementSession": {
    "sessionId": "s001",
    "measuredAt": "2026-04-20T10:00:00",
    "isFollowup": false
  },
  "measurements": {
    "before": {
      "liver": {
        "left": 36.0,
        "right": 36.0
      },
      "spleen": {
        "left": 36.0,
        "right": 36.1
      },
      "kidney": {
        "left": 36.0,
        "right": 36.0
      },
      "stomach": {
        "left": 36.1,
        "right": 36.0
      },
      "gallbladder": {
        "left": 36.0,
        "right": 36.0
      },
      "bladder": {
        "left": 36.0,
        "right": 36.1
      }
    },
    "after": {
      "liver": {
        "left": 36.0,
        "right": 36.1
      },
      "spleen": {
        "left": 36.0,
        "right": 36.0
      },
      "kidney": {
        "left": 36.1,
        "right": 36.0
      },
      "stomach": {
        "left": 36.0,
        "right": 36.1
      },
      "gallbladder": {
        "left": 36.0,
        "right": 36.0
      },
      "bladder": {
        "left": 36.0,
        "right": 36.0
      }
    }
  }
}
```

### 输出摘要

- **引擎模式**：hybrid
- **LLM 模型**：deepseek-chat
- **LLM 延迟**：23.28s
- **综合评分**：100
- **等级**：整体状态较好
- **摘要**：当前整体状态较平稳，请继续保持。

### 评分上下文

- currentRawScore: 100
- displayedScore: 100
- scoreLevel: 整体状态较好
- adherenceFlag: False
- scoreAdjustedByPolicy: False

### 整体评估

- overallLevel: 整体相对平稳
- dominantPattern: 左右相对平衡
- focusMeridians: []
- stableMeridians: ['肝经', '脾经', '肾经', '胃经', '胆经', '膀胱经']

### 经络明细

| 经络 | 状态 | 严重度 | 交叉 | before | after | 风险点 |
|------|------|--------|------|--------|-------|--------|
| 肝经 | 相对平衡 | balanced | False | balanced | balanced | — |
| 脾经 | 相对平衡 | balanced | False | balanced | balanced | — |
| 肾经 | 相对平衡 | balanced | False | balanced | balanced | — |
| 胃经 | 相对平衡 | balanced | False | balanced | balanced | — |
| 胆经 | 相对平衡 | balanced | False | balanced | balanced | — |
| 膀胱经 | 相对平衡 | balanced | False | balanced | balanced | — |

### 组合命中

无组合命中

### 建议标签

无建议标签

### 完整输出

<details>
<summary>展开 case_stable 完整 JSON 输出</summary>

```json
{
  "engine": {
    "mode": "hybrid",
    "version": "2.0",
    "llmModel": "deepseek-chat",
    "llmLatency": 23.28
  },
  "subject": {
    "id": "v2-stable-001",
    "name": "平稳场景"
  },
  "engineInference": {
    "dominantPatternBefore": "mixed",
    "dominantPatternAfter": "mixed",
    "lowestMeridianBefore": {
      "meridian": "liver",
      "side": "left",
      "value": 36.0
    },
    "lowestMeridianAfter": {
      "meridian": "liver",
      "side": "left",
      "value": 36.0
    },
    "meridianStates": {
      "liver": {
        "beforeStatus": "balanced",
        "afterStatus": "balanced",
        "beforeLowSide": null,
        "afterLowSide": null,
        "beforeDiff": 0.0,
        "afterDiff": 0.1,
        "cross": false,
        "severity": "balanced"
      },
      "spleen": {
        "beforeStatus": "balanced",
        "afterStatus": "balanced",
        "beforeLowSide": null,
        "afterLowSide": null,
        "beforeDiff": 0.1,
        "afterDiff": 0.0,
        "cross": false,
        "severity": "balanced"
      },
      "kidney": {
        "beforeStatus": "balanced",
        "afterStatus": "balanced",
        "beforeLowSide": null,
        "afterLowSide": null,
        "beforeDiff": 0.0,
        "afterDiff": 0.1,
        "cross": false,
        "severity": "balanced"
      },
      "stomach": {
        "beforeStatus": "balanced",
        "afterStatus": "balanced",
        "beforeLowSide": null,
        "afterLowSide": null,
        "beforeDiff": 0.1,
        "afterDiff": 0.1,
        "cross": false,
        "severity": "balanced"
      },
      "gallbladder": {
        "beforeStatus": "balanced",
        "afterStatus": "balanced",
        "beforeLowSide": null,
        "afterLowSide": null,
        "beforeDiff": 0.0,
        "afterDiff": 0.0,
        "cross": false,
        "severity": "balanced"
      },
      "bladder": {
        "beforeStatus": "balanced",
        "afterStatus": "balanced",
        "beforeLowSide": null,
        "afterLowSide": null,
        "beforeDiff": 0.1,
        "afterDiff": 0.0,
        "cross": false,
        "severity": "balanced"
      }
    },
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
    "stableMeridians": [
      "肝经",
      "脾经",
      "肾经",
      "胃经",
      "胆经",
      "膀胱经"
    ]
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
      "riskPoints": [],
      "narrative": "肝经温度平衡，提示代谢和情绪状态较为稳定。"
    },
    {
      "meridian": "脾经",
      "meridianId": "spleen",
      "status": "相对平衡",
      "severity": "balanced",
      "cross": false,
      "beforeStatus": "balanced",
      "afterStatus": "balanced",
      "riskPoints": [],
      "narrative": "脾经温度平衡，反映运化和湿气代谢功能正常。"
    },
    {
      "meridian": "肾经",
      "meridianId": "kidney",
      "status": "相对平衡",
      "severity": "balanced",
      "cross": false,
      "beforeStatus": "balanced",
      "afterStatus": "balanced",
      "riskPoints": [],
      "narrative": "肾经温度平衡，表明肾阴肾阳和骨骼健康状态良好。"
    },
    {
      "meridian": "胃经",
      "meridianId": "stomach",
      "status": "相对平衡",
      "severity": "balanced",
      "cross": false,
      "beforeStatus": "balanced",
      "afterStatus": "balanced",
      "riskPoints": [],
      "narrative": "胃经温度平衡，显示消化功能和饮食规律较为协调。"
    },
    {
      "meridian": "胆经",
      "meridianId": "gallbladder",
      "status": "相对平衡",
      "severity": "balanced",
      "cross": false,
      "beforeStatus": "balanced",
      "afterStatus": "balanced",
      "riskPoints": [],
      "narrative": "胆经温度平衡，提示胆红素和胆固醇代谢无异常。"
    },
    {
      "meridian": "膀胱经",
      "meridianId": "bladder",
      "status": "相对平衡",
      "severity": "balanced",
      "cross": false,
      "beforeStatus": "balanced",
      "afterStatus": "balanced",
      "riskPoints": [],
      "narrative": "膀胱经温度平衡，反映肩颈腰和泌尿系统状态平稳。"
    }
  ],
  "combinationAnalysis": [],
  "adviceTags": [],
  "healthScoreValue": 100,
  "trace": {
    "scoreBreakdown": [],
    "improvementBonus": {
      "improvedCount": 2,
      "improvementBonus": 2,
      "improvementRule": "partial_improvement",
      "stableBonus": 3,
      "totalBonus": 5
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
  },
  "summary": "基于足部六条经络的温度测量数据，您的整体经络状态相对平稳，所有经络均处于相对平衡状态，健康评分为100分，表明当前身体状况较好。左右侧温度差异微小，无明显偏向，建议继续保持良好的生活习惯以维持这种健康状态。",
  "reportSummary": "基于足部六条经络的温度测量数据，您的整体经络状态相对平稳，所有经络均处于相对平衡状态，健康评分为100分，表明当前身体状况较好。左右侧温度差异微小，无明显偏向，建议继续保持良好的生活习惯以维持这种健康状态。",
  "storefront": {
    "focusHeadline": "经络平衡，健康状态良好",
    "clientExplanation": "本分析基于经络温度测量数据，提供健康趋势参考，不等同于医疗诊断。",
    "talkTrack": [
      "您的经络测量显示整体状态非常平稳，所有经络都处于平衡状态。",
      "这通常意味着身体机能协调良好，没有明显的失衡风险。",
      "建议您继续保持规律作息和健康饮食，以维护这种积极状态。"
    ],
    "retestPrompt": "建议定期复测，以持续监测经络状态变化。"
  },
  "recommendations": [
    "保持均衡饮食，避免过度油腻或生冷食物，以支持脾胃功能。",
    "适量运动，如散步或瑜伽，有助于促进气血循环和经络平衡。",
    "注意情绪管理，避免长期压力，以维护肝经的代谢和睡眠质量。"
  ]
}
```

</details>

---

## case_left_low

### 输入

```json
{
  "subject": {
    "id": "v2-left-low-001",
    "name": "左低场景"
  },
  "measurementSession": {
    "sessionId": "s002",
    "measuredAt": "2026-04-20T10:00:00",
    "isFollowup": false
  },
  "measurements": {
    "before": {
      "liver": {
        "left": 35.0,
        "right": 36.1
      },
      "spleen": {
        "left": 35.1,
        "right": 35.9
      },
      "kidney": {
        "left": 35.0,
        "right": 35.8
      },
      "stomach": {
        "left": 35.1,
        "right": 36.0
      },
      "gallbladder": {
        "left": 35.0,
        "right": 35.9
      },
      "bladder": {
        "left": 35.2,
        "right": 35.9
      }
    },
    "after": {
      "liver": {
        "left": 35.0,
        "right": 36.0
      },
      "spleen": {
        "left": 35.2,
        "right": 35.8
      },
      "kidney": {
        "left": 35.1,
        "right": 35.7
      },
      "stomach": {
        "left": 35.3,
        "right": 35.9
      },
      "gallbladder": {
        "left": 35.2,
        "right": 35.8
      },
      "bladder": {
        "left": 35.4,
        "right": 35.8
      }
    }
  }
}
```

### 输出摘要

- **引擎模式**：hybrid
- **LLM 模型**：deepseek-chat
- **LLM 延迟**：30.62s
- **综合评分**：55.0
- **等级**：需重点关注
- **摘要**：当前失衡较明显，建议尽早重视。

### 评分上下文

- currentRawScore: 55.0
- displayedScore: 55.0
- scoreLevel: 需重点关注
- adherenceFlag: False
- scoreAdjustedByPolicy: False

### 整体评估

- overallLevel: 失衡较明显
- dominantPattern: 整体偏左
- focusMeridians: ['肝经', '脾经', '肾经', '胃经', '胆经', '膀胱经']
- stableMeridians: []

### 经络明细

| 经络 | 状态 | 严重度 | 交叉 | before | after | 风险点 |
|------|------|--------|------|--------|-------|--------|
| 肝经 | 代谢偏弱 / 气虚倾向 | high | False | left_low | left_low | 三高风险需关注, 血稠倾向, 乳房结节或小叶增生风险, 温差较大时睡眠质量下降 |
| 脾经 | 脾气偏虚 | medium | False | left_low | left_low | 乏力, 思虑偏重, 血糖代谢需关注, 四肢风险, 膝盖风险 |
| 肾经 | 肾阴偏虚 | medium | False | left_low | left_low | 尿酸偏高风险, 耳鸣耳背, 偏热, 恢复偏慢 |
| 胃经 | 胃部津液偏少 | medium | False | left_low | left_low | 胃炎倾向, 反酸, 胃部刺激, 饮食不规律风险 |
| 胆经 | 胆经偏弱 | medium | False | left_low | left_low | 口干口苦, 偏头痛, 胆红素相关风险 |
| 膀胱经 | 肩颈腰与肠道方向需关注 | medium | False | left_low | left_low | 肩颈腰问题, 便秘, 痔疮, 大肠息肉风险, 肺左侧功能风险 |

### 组合命中

命中规则：combo_head_supply, combo_waist, combo_neck, combo_liver_gall

### 建议标签

标签：gallbladder_metabolism_pressure, head_supply_attention

### 扣分明细

| 规则 | 分值 | 说明 |
|------|------|------|
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| left_bias | -6 |  |
| head_supply_hit | -6 |  |
| neck_waist_reproductive_hit | -5 |  |
| multi_imbalance | -8 |  |
| 改善加分 | +4 | improved=6, stable=0 |

### 完整输出

<details>
<summary>展开 case_left_low 完整 JSON 输出</summary>

```json
{
  "engine": {
    "mode": "hybrid",
    "version": "2.0",
    "llmModel": "deepseek-chat",
    "llmLatency": 30.62
  },
  "subject": {
    "id": "v2-left-low-001",
    "name": "左低场景"
  },
  "engineInference": {
    "dominantPatternBefore": "left_low",
    "dominantPatternAfter": "left_low",
    "lowestMeridianBefore": {
      "meridian": "liver",
      "side": "left",
      "value": 35.0
    },
    "lowestMeridianAfter": {
      "meridian": "liver",
      "side": "left",
      "value": 35.0
    },
    "meridianStates": {
      "liver": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 1.1,
        "afterDiff": 1.0,
        "cross": false,
        "severity": "high"
      },
      "spleen": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.8,
        "afterDiff": 0.6,
        "cross": false,
        "severity": "medium"
      },
      "kidney": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.8,
        "afterDiff": 0.6,
        "cross": false,
        "severity": "medium"
      },
      "stomach": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.9,
        "afterDiff": 0.6,
        "cross": false,
        "severity": "medium"
      },
      "gallbladder": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.9,
        "afterDiff": 0.6,
        "cross": false,
        "severity": "medium"
      },
      "bladder": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.7,
        "afterDiff": 0.4,
        "cross": false,
        "severity": "medium"
      }
    },
    "combinationHits": [
      "combo_head_supply",
      "combo_waist",
      "combo_neck",
      "combo_liver_gall"
    ]
  },
  "scoreContext": {
    "currentRawScore": 55.0,
    "displayedScore": 55.0,
    "scoreLevel": "需重点关注",
    "scoreSummary": "当前失衡较明显，建议尽早重视。",
    "instrumentUsageDaysBetweenMeasurements": 0,
    "adherenceFlag": false,
    "scoreAdjustedByPolicy": false
  },
  "healthScore": {
    "score": 55.0,
    "level": "需重点关注",
    "summary": "当前失衡较明显，建议尽早重视。"
  },
  "overallAssessment": {
    "overallLevel": "失衡较明显",
    "dominantPattern": "整体偏左",
    "focusMeridians": [
      "肝经",
      "脾经",
      "肾经",
      "胃经",
      "胆经",
      "膀胱经"
    ],
    "stableMeridians": []
  },
  "meridianDetails": [
    {
      "meridian": "肝经",
      "meridianId": "liver",
      "status": "代谢偏弱 / 气虚倾向",
      "severity": "high",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "三高风险需关注",
        "血稠倾向",
        "乳房结节或小叶增生风险",
        "温差较大时睡眠质量下降"
      ],
      "narrative": "肝经显示代谢偏弱，提示三高风险和睡眠质量下降风险。"
    },
    {
      "meridian": "脾经",
      "meridianId": "spleen",
      "status": "脾气偏虚",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "乏力",
        "思虑偏重",
        "血糖代谢需关注",
        "四肢风险",
        "膝盖风险"
      ],
      "narrative": "脾经脾气偏虚，可能导致乏力和血糖代谢需关注。"
    },
    {
      "meridian": "肾经",
      "meridianId": "kidney",
      "status": "肾阴偏虚",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "尿酸偏高风险",
        "耳鸣耳背",
        "偏热",
        "恢复偏慢"
      ],
      "narrative": "肾经肾阴偏虚，有尿酸偏高和恢复偏慢的倾向。"
    },
    {
      "meridian": "胃经",
      "meridianId": "stomach",
      "status": "胃部津液偏少",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "胃炎倾向",
        "反酸",
        "胃部刺激",
        "饮食不规律风险"
      ],
      "narrative": "胃经津液偏少，提示胃炎倾向和饮食不规律风险。"
    },
    {
      "meridian": "胆经",
      "meridianId": "gallbladder",
      "status": "胆经偏弱",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "口干口苦",
        "偏头痛",
        "胆红素相关风险"
      ],
      "narrative": "胆经偏弱，可能伴随口干口苦和偏头痛。"
    },
    {
      "meridian": "膀胱经",
      "meridianId": "bladder",
      "status": "肩颈腰与肠道方向需关注",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "肩颈腰问题",
        "便秘",
        "痔疮",
        "大肠息肉风险",
        "肺左侧功能风险"
      ],
      "narrative": "膀胱经提示肩颈腰与肠道方向需关注，有便秘和肺左侧功能风险。"
    }
  ],
  "combinationAnalysis": [
    {
      "comboId": "combo_head_supply",
      "comboName": "头部供血需关注"
    },
    {
      "comboId": "combo_waist",
      "comboName": "腰椎相关问题需关注"
    },
    {
      "comboId": "combo_neck",
      "comboName": "颈椎相关问题需关注"
    },
    {
      "comboId": "combo_liver_gall",
      "comboName": "肝胆代谢压力需关注"
    }
  ],
  "adviceTags": [
    "gallbladder_metabolism_pressure",
    "head_supply_attention"
  ],
  "healthScoreValue": 55.0,
  "trace": {
    "scoreBreakdown": [
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "liver"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "spleen"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "kidney"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "stomach"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "gallbladder"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "bladder"
      },
      {
        "rule": "left_bias",
        "score": -6
      },
      {
        "rule": "head_supply_hit",
        "score": -6
      },
      {
        "rule": "neck_waist_reproductive_hit",
        "score": -5
      },
      {
        "rule": "multi_imbalance",
        "score": -8
      }
    ],
    "improvementBonus": {
      "improvedCount": 6,
      "improvementBonus": 4,
      "improvementRule": "multiple_meridians_improved",
      "stableBonus": 0,
      "totalBonus": 4
    },
    "globalPatterns": {
      "leftLowCountBefore": 6,
      "rightLowCountBefore": 0,
      "leftLowCountAfter": 6,
      "rightLowCountAfter": 0,
      "dominantPatternBefore": "left_low",
      "dominantPatternAfter": "left_low",
      "crossCount": 0
    }
  },
  "summary": "根据足部经络温度测量分析，您的整体健康评分为55.0分，需重点关注。主要发现为整体偏左失衡，提示头部供血方向需关注，同时肝经代谢偏弱、脾经脾气偏虚、肾经肾阴偏虚、胃经津液偏少、胆经偏弱和膀胱经肩颈腰与肠道方向异常，组合判症显示腰椎、颈椎和肝胆代谢压力需关注。建议从调节作息、饮食和运动入手，以改善经络平衡和整体健康状况。",
  "reportSummary": "根据足部经络温度测量分析，您的整体健康评分为55.0分，需重点关注。主要发现为整体偏左失衡，提示头部供血方向需关注，同时肝经代谢偏弱、脾经脾气偏虚、肾经肾阴偏虚、胃经津液偏少、胆经偏弱和膀胱经肩颈腰与肠道方向异常，组合判症显示腰椎、颈椎和肝胆代谢压力需关注。建议从调节作息、饮食和运动入手，以改善经络平衡和整体健康状况。",
  "storefront": {
    "focusHeadline": "经络失衡需关注，头部供血与代谢为重点",
    "clientExplanation": "本分析基于中医经络理论，通过温度测量评估身体状态，不等同于医疗诊断，建议结合专业医疗建议进行健康管理。",
    "talkTrack": [
      "您的测量结果显示整体经络状态有失衡倾向，特别是头部供血和代谢方向需要留意。",
      "肝经和胆经提示代谢压力，可能影响睡眠和消化，建议调整饮食规律。",
      "脾经和肾经的虚弱可能带来疲劳和恢复慢，日常中可加强温和运动来改善。"
    ],
    "retestPrompt": "建议在调整作息和饮食后，定期复测以跟踪经络状态变化。"
  },
  "recommendations": [
    "调整作息，确保充足睡眠，特别是凌晨1-3点肝经当令时段，以养肝血。",
    "饮食规律，避免生冷食物，增加温和易消化饮食，关注上午7-9点胃经当令时段促消化。",
    "进行适度运动如散步或瑜伽，以改善气血循环，缓解肩颈腰不适和代谢压力。"
  ]
}
```

</details>

---

## case_right_low

### 输入

```json
{
  "subject": {
    "id": "v2-right-low-001",
    "name": "右低场景"
  },
  "measurementSession": {
    "sessionId": "s003",
    "measuredAt": "2026-04-20T10:00:00",
    "isFollowup": false
  },
  "measurements": {
    "before": {
      "liver": {
        "left": 36.0,
        "right": 35.1
      },
      "spleen": {
        "left": 35.9,
        "right": 35.0
      },
      "kidney": {
        "left": 35.8,
        "right": 35.1
      },
      "stomach": {
        "left": 36.0,
        "right": 35.2
      },
      "gallbladder": {
        "left": 36.1,
        "right": 35.2
      },
      "bladder": {
        "left": 35.9,
        "right": 35.1
      }
    },
    "after": {
      "liver": {
        "left": 36.0,
        "right": 35.2
      },
      "spleen": {
        "left": 35.8,
        "right": 35.1
      },
      "kidney": {
        "left": 35.7,
        "right": 35.2
      },
      "stomach": {
        "left": 35.9,
        "right": 35.3
      },
      "gallbladder": {
        "left": 36.0,
        "right": 35.3
      },
      "bladder": {
        "left": 35.8,
        "right": 35.2
      }
    }
  }
}
```

### 输出摘要

- **引擎模式**：hybrid
- **LLM 模型**：deepseek-chat
- **LLM 延迟**：27.45s
- **综合评分**：55.0
- **等级**：需重点关注
- **摘要**：当前失衡较明显，建议尽早重视。

### 评分上下文

- currentRawScore: 55.0
- displayedScore: 55.0
- scoreLevel: 需重点关注
- adherenceFlag: False
- scoreAdjustedByPolicy: False

### 整体评估

- overallLevel: 失衡较明显
- dominantPattern: 整体偏右
- focusMeridians: ['肝经', '脾经', '肾经', '胃经', '胆经', '膀胱经']
- stableMeridians: []

### 经络明细

| 经络 | 状态 | 严重度 | 交叉 | before | after | 风险点 |
|------|------|--------|------|--------|-------|--------|
| 肝经 | 血虚 / 藏血不足 | medium | False | right_low | right_low | 贫血倾向, 头晕乏力, 掉发, 心脏供血不足, 心慌, 低血压, 睡眠浅 |
| 脾经 | 湿气偏重 | medium | False | right_low | right_low | 大便异常, 粘马桶, 子宫相关风险, 经期延长或量多, 四肢疼痛, 膝盖问题 |
| 肾经 | 肾阳偏虚 | medium | False | right_low | right_low | 怕冷, 四肢发凉, 夜尿偏多, 体力恢复慢 |
| 胃经 | 胃阳不足 / 胃寒 | medium | False | right_low | right_low | 胃寒, 消化偏弱, 胃胀, 饮食后不适 |
| 胆经 | 胆脂代谢需关注 | medium | False | right_low | right_low | 胆固醇风险, 甘油三酯风险, 脂肪瘤风险, 精神状态或决策效率可能受身体状态影响 |
| 膀胱经 | 湿下注与腰部方向需关注 | medium | False | right_low | right_low | 大便不成形, 湿气下注大肠, 肺右侧功能风险 |

### 组合命中

命中规则：combo_heart_supply, combo_waist, combo_neck, combo_liver_gall

### 建议标签

标签：stomach_cold, spleen_damp, kidney_yang_weak, liver_blood_weak, gallbladder_metabolism_pressure, heart_supply_attention

### 扣分明细

| 规则 | 分值 | 说明 |
|------|------|------|
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| right_bias | -6 |  |
| heart_supply_hit | -6 |  |
| neck_waist_reproductive_hit | -5 |  |
| multi_imbalance | -8 |  |
| 改善加分 | +4 | improved=6, stable=0 |

### 完整输出

<details>
<summary>展开 case_right_low 完整 JSON 输出</summary>

```json
{
  "engine": {
    "mode": "hybrid",
    "version": "2.0",
    "llmModel": "deepseek-chat",
    "llmLatency": 27.45
  },
  "subject": {
    "id": "v2-right-low-001",
    "name": "右低场景"
  },
  "engineInference": {
    "dominantPatternBefore": "right_low",
    "dominantPatternAfter": "right_low",
    "lowestMeridianBefore": {
      "meridian": "spleen",
      "side": "right",
      "value": 35.0
    },
    "lowestMeridianAfter": {
      "meridian": "spleen",
      "side": "right",
      "value": 35.1
    },
    "meridianStates": {
      "liver": {
        "beforeStatus": "right_low",
        "afterStatus": "right_low",
        "beforeLowSide": "right",
        "afterLowSide": "right",
        "beforeDiff": 0.9,
        "afterDiff": 0.8,
        "cross": false,
        "severity": "medium"
      },
      "spleen": {
        "beforeStatus": "right_low",
        "afterStatus": "right_low",
        "beforeLowSide": "right",
        "afterLowSide": "right",
        "beforeDiff": 0.9,
        "afterDiff": 0.7,
        "cross": false,
        "severity": "medium"
      },
      "kidney": {
        "beforeStatus": "right_low",
        "afterStatus": "right_low",
        "beforeLowSide": "right",
        "afterLowSide": "right",
        "beforeDiff": 0.7,
        "afterDiff": 0.5,
        "cross": false,
        "severity": "medium"
      },
      "stomach": {
        "beforeStatus": "right_low",
        "afterStatus": "right_low",
        "beforeLowSide": "right",
        "afterLowSide": "right",
        "beforeDiff": 0.8,
        "afterDiff": 0.6,
        "cross": false,
        "severity": "medium"
      },
      "gallbladder": {
        "beforeStatus": "right_low",
        "afterStatus": "right_low",
        "beforeLowSide": "right",
        "afterLowSide": "right",
        "beforeDiff": 0.9,
        "afterDiff": 0.7,
        "cross": false,
        "severity": "medium"
      },
      "bladder": {
        "beforeStatus": "right_low",
        "afterStatus": "right_low",
        "beforeLowSide": "right",
        "afterLowSide": "right",
        "beforeDiff": 0.8,
        "afterDiff": 0.6,
        "cross": false,
        "severity": "medium"
      }
    },
    "combinationHits": [
      "combo_heart_supply",
      "combo_waist",
      "combo_neck",
      "combo_liver_gall"
    ]
  },
  "scoreContext": {
    "currentRawScore": 55.0,
    "displayedScore": 55.0,
    "scoreLevel": "需重点关注",
    "scoreSummary": "当前失衡较明显，建议尽早重视。",
    "instrumentUsageDaysBetweenMeasurements": 0,
    "adherenceFlag": false,
    "scoreAdjustedByPolicy": false
  },
  "healthScore": {
    "score": 55.0,
    "level": "需重点关注",
    "summary": "当前失衡较明显，建议尽早重视。"
  },
  "overallAssessment": {
    "overallLevel": "失衡较明显",
    "dominantPattern": "整体偏右",
    "focusMeridians": [
      "肝经",
      "脾经",
      "肾经",
      "胃经",
      "胆经",
      "膀胱经"
    ],
    "stableMeridians": []
  },
  "meridianDetails": [
    {
      "meridian": "肝经",
      "meridianId": "liver",
      "status": "血虚 / 藏血不足",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "right_low",
      "afterStatus": "right_low",
      "riskPoints": [
        "贫血倾向",
        "头晕乏力",
        "掉发",
        "心脏供血不足",
        "心慌",
        "低血压",
        "睡眠浅"
      ],
      "narrative": "肝经温度显示血虚倾向，可能影响情绪和睡眠质量。"
    },
    {
      "meridian": "脾经",
      "meridianId": "spleen",
      "status": "湿气偏重",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "right_low",
      "afterStatus": "right_low",
      "riskPoints": [
        "大便异常",
        "粘马桶",
        "子宫相关风险",
        "经期延长或量多",
        "四肢疼痛",
        "膝盖问题"
      ],
      "narrative": "脾经湿气偏重，提示运化功能需加强，可能伴有大便异常。"
    },
    {
      "meridian": "肾经",
      "meridianId": "kidney",
      "status": "肾阳偏虚",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "right_low",
      "afterStatus": "right_low",
      "riskPoints": [
        "怕冷",
        "四肢发凉",
        "夜尿偏多",
        "体力恢复慢"
      ],
      "narrative": "肾经肾阳偏虚，表现为怕冷和体力恢复慢。"
    },
    {
      "meridian": "胃经",
      "meridianId": "stomach",
      "status": "胃阳不足 / 胃寒",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "right_low",
      "afterStatus": "right_low",
      "riskPoints": [
        "胃寒",
        "消化偏弱",
        "胃胀",
        "饮食后不适"
      ],
      "narrative": "胃经胃阳不足，可能导致胃寒和消化偏弱。"
    },
    {
      "meridian": "胆经",
      "meridianId": "gallbladder",
      "status": "胆脂代谢需关注",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "right_low",
      "afterStatus": "right_low",
      "riskPoints": [
        "胆固醇风险",
        "甘油三酯风险",
        "脂肪瘤风险",
        "精神状态或决策效率可能受身体状态影响"
      ],
      "narrative": "胆经胆脂代谢需关注，与胆固醇和决策效率相关。"
    },
    {
      "meridian": "膀胱经",
      "meridianId": "bladder",
      "status": "湿下注与腰部方向需关注",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "right_low",
      "afterStatus": "right_low",
      "riskPoints": [
        "大便不成形",
        "湿气下注大肠",
        "肺右侧功能风险"
      ],
      "narrative": "膀胱经湿下注，需关注腰部和肠道健康。"
    }
  ],
  "combinationAnalysis": [
    {
      "comboId": "combo_heart_supply",
      "comboName": "心脏供血需关注"
    },
    {
      "comboId": "combo_waist",
      "comboName": "腰椎相关问题需关注"
    },
    {
      "comboId": "combo_neck",
      "comboName": "颈椎相关问题需关注"
    },
    {
      "comboId": "combo_liver_gall",
      "comboName": "肝胆代谢压力需关注"
    }
  ],
  "adviceTags": [
    "stomach_cold",
    "spleen_damp",
    "kidney_yang_weak",
    "liver_blood_weak",
    "gallbladder_metabolism_pressure",
    "heart_supply_attention"
  ],
  "healthScoreValue": 55.0,
  "trace": {
    "scoreBreakdown": [
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "liver"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "spleen"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "kidney"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "stomach"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "gallbladder"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "bladder"
      },
      {
        "rule": "right_bias",
        "score": -6
      },
      {
        "rule": "heart_supply_hit",
        "score": -6
      },
      {
        "rule": "neck_waist_reproductive_hit",
        "score": -5
      },
      {
        "rule": "multi_imbalance",
        "score": -8
      }
    ],
    "improvementBonus": {
      "improvedCount": 6,
      "improvementBonus": 4,
      "improvementRule": "multiple_meridians_improved",
      "stableBonus": 0,
      "totalBonus": 4
    },
    "globalPatterns": {
      "leftLowCountBefore": 0,
      "rightLowCountBefore": 6,
      "leftLowCountAfter": 0,
      "rightLowCountAfter": 6,
      "dominantPatternBefore": "right_low",
      "dominantPatternAfter": "right_low",
      "crossCount": 0
    }
  },
  "summary": "根据足部经络温度测量数据，您的整体健康评分为55.0，需重点关注。分析显示，您存在整体偏右的失衡趋势，提示循环及心脏供血方向需关注。主要经络问题包括肝经血虚、脾经湿气偏重、肾经肾阳偏虚、胃经胃阳不足、胆经胆脂代谢需关注和膀胱经湿下注，这可能与贫血、消化弱、怕冷、代谢压力等症状相关。建议从温补阳气、祛湿健脾、改善循环等方面入手调理。",
  "reportSummary": "根据足部经络温度测量数据，您的整体健康评分为55.0，需重点关注。分析显示，您存在整体偏右的失衡趋势，提示循环及心脏供血方向需关注。主要经络问题包括肝经血虚、脾经湿气偏重、肾经肾阳偏虚、胃经胃阳不足、胆经胆脂代谢需关注和膀胱经湿下注，这可能与贫血、消化弱、怕冷、代谢压力等症状相关。建议从温补阳气、祛湿健脾、改善循环等方面入手调理。",
  "storefront": {
    "focusHeadline": "整体失衡需关注，重点调理肝脾肾胃胆膀胱",
    "clientExplanation": "本分析基于中医经络理论，通过温度测量评估身体状态，不等同于医疗诊断，建议结合专业医疗意见。",
    "talkTrack": [
      "您的测量结果显示整体经络状态有失衡，特别是右侧偏低，这可能影响循环和心脏供血。",
      "肝经和脾经的问题提示您可能有贫血、湿气重的情况，建议注意饮食和作息。",
      "肾经和胃经的偏虚可能让您感到怕冷或消化不适，日常可多温补调理。"
    ],
    "retestPrompt": "建议定期复测以跟踪调理效果，尤其在季节变化或作息调整后。"
  },
  "recommendations": [
    "建议加强温补，如适量食用姜、桂圆等温性食物，以改善胃寒和肾阳不足。",
    "注重祛湿健脾，通过薏米、山药等食材调理，帮助缓解湿气和大便问题。",
    "保持规律作息和适度运动，促进肝胆代谢和整体循环，减少贫血和疲劳风险。"
  ]
}
```

</details>

---

## case_cross

### 输入

```json
{
  "subject": {
    "id": "v2-cross-001",
    "name": "交叉场景"
  },
  "measurementSession": {
    "sessionId": "s004",
    "measuredAt": "2026-04-20T10:00:00",
    "isFollowup": false
  },
  "measurements": {
    "before": {
      "liver": {
        "left": 35.0,
        "right": 36.2
      },
      "spleen": {
        "left": 36.2,
        "right": 35.0
      },
      "kidney": {
        "left": 36.1,
        "right": 35.0
      },
      "stomach": {
        "left": 35.0,
        "right": 36.0
      },
      "gallbladder": {
        "left": 36.0,
        "right": 35.0
      },
      "bladder": {
        "left": 35.0,
        "right": 36.1
      }
    },
    "after": {
      "liver": {
        "left": 36.1,
        "right": 35.1
      },
      "spleen": {
        "left": 35.1,
        "right": 36.1
      },
      "kidney": {
        "left": 35.1,
        "right": 36.0
      },
      "stomach": {
        "left": 36.0,
        "right": 35.1
      },
      "gallbladder": {
        "left": 35.1,
        "right": 36.0
      },
      "bladder": {
        "left": 36.0,
        "right": 35.1
      }
    }
  }
}
```

### 输出摘要

- **引擎模式**：hybrid
- **LLM 模型**：deepseek-chat
- **LLM 延迟**：22.44s
- **综合评分**：34
- **等级**：需重点关注
- **摘要**：当前失衡较明显，建议尽早重视。

### 评分上下文

- currentRawScore: 34
- displayedScore: 34
- scoreLevel: 需重点关注
- adherenceFlag: False
- scoreAdjustedByPolicy: False

### 整体评估

- overallLevel: 失衡较明显
- dominantPattern: 多经络交叉失衡
- focusMeridians: ['肝经', '脾经', '肾经', '胃经', '胆经', '膀胱经']
- stableMeridians: []

### 经络明细

| 经络 | 状态 | 严重度 | 交叉 | before | after | 风险点 |
|------|------|--------|------|--------|-------|--------|
| 肝经 | 交叉 | high | True | left_low | right_low | 三高风险需关注, 血稠倾向, 乳房结节或小叶增生风险, 温差较大时睡眠质量下降 |
| 脾经 | 交叉 | high | True | right_low | left_low | 大便异常, 粘马桶, 子宫相关风险, 经期延长或量多, 四肢疼痛, 膝盖问题 |
| 肾经 | 交叉 | high | True | right_low | left_low | 怕冷, 四肢发凉, 夜尿偏多, 体力恢复慢 |
| 胃经 | 交叉 | medium | True | left_low | right_low | 胃炎倾向, 反酸, 胃部刺激, 饮食不规律风险 |
| 胆经 | 交叉 | medium | True | right_low | left_low | 胆固醇风险, 甘油三酯风险, 脂肪瘤风险, 精神状态或决策效率可能受身体状态影响 |
| 膀胱经 | 交叉 | high | True | left_low | right_low | 肩颈腰问题, 便秘, 痔疮, 大肠息肉风险, 肺左侧功能风险 |

### 组合命中

命中规则：combo_neck, combo_reproductive, combo_liver_gall, combo_multi_cross

### 建议标签

标签：spleen_damp, kidney_yang_weak, gallbladder_metabolism_pressure, reproductive_system_attention

### 扣分明细

| 规则 | 分值 | 说明 |
|------|------|------|
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_cross | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_cross | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_cross | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_cross | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_cross | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_cross | -4 |  |
| kidney_bladder_double_cross | -8 |  |
| multi_cross | -8 |  |
| neck_waist_reproductive_hit | -5 |  |
| multi_imbalance | -8 |  |
| 改善加分 | +4 | improved=6, stable=0 |

### 完整输出

<details>
<summary>展开 case_cross 完整 JSON 输出</summary>

```json
{
  "engine": {
    "mode": "hybrid",
    "version": "2.0",
    "llmModel": "deepseek-chat",
    "llmLatency": 22.44
  },
  "subject": {
    "id": "v2-cross-001",
    "name": "交叉场景"
  },
  "engineInference": {
    "dominantPatternBefore": "mixed",
    "dominantPatternAfter": "mixed",
    "lowestMeridianBefore": {
      "meridian": "liver",
      "side": "left",
      "value": 35.0
    },
    "lowestMeridianAfter": {
      "meridian": "liver",
      "side": "right",
      "value": 35.1
    },
    "meridianStates": {
      "liver": {
        "beforeStatus": "left_low",
        "afterStatus": "right_low",
        "beforeLowSide": "left",
        "afterLowSide": "right",
        "beforeDiff": 1.2,
        "afterDiff": 1.0,
        "cross": true,
        "severity": "high"
      },
      "spleen": {
        "beforeStatus": "right_low",
        "afterStatus": "left_low",
        "beforeLowSide": "right",
        "afterLowSide": "left",
        "beforeDiff": 1.2,
        "afterDiff": 1.0,
        "cross": true,
        "severity": "high"
      },
      "kidney": {
        "beforeStatus": "right_low",
        "afterStatus": "left_low",
        "beforeLowSide": "right",
        "afterLowSide": "left",
        "beforeDiff": 1.1,
        "afterDiff": 0.9,
        "cross": true,
        "severity": "high"
      },
      "stomach": {
        "beforeStatus": "left_low",
        "afterStatus": "right_low",
        "beforeLowSide": "left",
        "afterLowSide": "right",
        "beforeDiff": 1.0,
        "afterDiff": 0.9,
        "cross": true,
        "severity": "medium"
      },
      "gallbladder": {
        "beforeStatus": "right_low",
        "afterStatus": "left_low",
        "beforeLowSide": "right",
        "afterLowSide": "left",
        "beforeDiff": 1.0,
        "afterDiff": 0.9,
        "cross": true,
        "severity": "medium"
      },
      "bladder": {
        "beforeStatus": "left_low",
        "afterStatus": "right_low",
        "beforeLowSide": "left",
        "afterLowSide": "right",
        "beforeDiff": 1.1,
        "afterDiff": 0.9,
        "cross": true,
        "severity": "high"
      }
    },
    "combinationHits": [
      "combo_neck",
      "combo_reproductive",
      "combo_liver_gall",
      "combo_multi_cross"
    ]
  },
  "scoreContext": {
    "currentRawScore": 34,
    "displayedScore": 34,
    "scoreLevel": "需重点关注",
    "scoreSummary": "当前失衡较明显，建议尽早重视。",
    "instrumentUsageDaysBetweenMeasurements": 0,
    "adherenceFlag": false,
    "scoreAdjustedByPolicy": false
  },
  "healthScore": {
    "score": 34,
    "level": "需重点关注",
    "summary": "当前失衡较明显，建议尽早重视。"
  },
  "overallAssessment": {
    "overallLevel": "失衡较明显",
    "dominantPattern": "多经络交叉失衡",
    "focusMeridians": [
      "肝经",
      "脾经",
      "肾经",
      "胃经",
      "胆经",
      "膀胱经"
    ],
    "stableMeridians": []
  },
  "meridianDetails": [
    {
      "meridian": "肝经",
      "meridianId": "liver",
      "status": "交叉",
      "severity": "high",
      "cross": true,
      "beforeStatus": "left_low",
      "afterStatus": "right_low",
      "riskPoints": [
        "三高风险需关注",
        "血稠倾向",
        "乳房结节或小叶增生风险",
        "温差较大时睡眠质量下降"
      ],
      "narrative": "肝经交叉异常，提示代谢偏弱，需关注三高和睡眠质量。"
    },
    {
      "meridian": "脾经",
      "meridianId": "spleen",
      "status": "交叉",
      "severity": "high",
      "cross": true,
      "beforeStatus": "right_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "大便异常",
        "粘马桶",
        "子宫相关风险",
        "经期延长或量多",
        "四肢疼痛",
        "膝盖问题"
      ],
      "narrative": "脾经交叉异常，提示湿气偏重，可能影响消化和四肢。"
    },
    {
      "meridian": "肾经",
      "meridianId": "kidney",
      "status": "交叉",
      "severity": "high",
      "cross": true,
      "beforeStatus": "right_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "怕冷",
        "四肢发凉",
        "夜尿偏多",
        "体力恢复慢"
      ],
      "narrative": "肾经交叉异常，提示肾阳偏虚，表现为怕冷和体力恢复慢。"
    },
    {
      "meridian": "胃经",
      "meridianId": "stomach",
      "status": "交叉",
      "severity": "medium",
      "cross": true,
      "beforeStatus": "left_low",
      "afterStatus": "right_low",
      "riskPoints": [
        "胃炎倾向",
        "反酸",
        "胃部刺激",
        "饮食不规律风险"
      ],
      "narrative": "胃经交叉异常，提示胃部津液偏少，需注意饮食规律和胃部不适。"
    },
    {
      "meridian": "胆经",
      "meridianId": "gallbladder",
      "status": "交叉",
      "severity": "medium",
      "cross": true,
      "beforeStatus": "right_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "胆固醇风险",
        "甘油三酯风险",
        "脂肪瘤风险",
        "精神状态或决策效率可能受身体状态影响"
      ],
      "narrative": "胆经交叉异常，提示胆脂代谢需关注，可能影响胆固醇和精神状态。"
    },
    {
      "meridian": "膀胱经",
      "meridianId": "bladder",
      "status": "交叉",
      "severity": "high",
      "cross": true,
      "beforeStatus": "left_low",
      "afterStatus": "right_low",
      "riskPoints": [
        "肩颈腰问题",
        "便秘",
        "痔疮",
        "大肠息肉风险",
        "肺左侧功能风险"
      ],
      "narrative": "膀胱经交叉异常，提示肩颈腰与肠道方向需关注，可能有便秘或腰酸风险。"
    }
  ],
  "combinationAnalysis": [
    {
      "comboId": "combo_neck",
      "comboName": "颈椎相关问题需关注"
    },
    {
      "comboId": "combo_reproductive",
      "comboName": "生殖系统相关风险需重点关注"
    },
    {
      "comboId": "combo_liver_gall",
      "comboName": "肝胆代谢压力需关注"
    },
    {
      "comboId": "combo_multi_cross",
      "comboName": "多经络交叉失衡需重点关注"
    }
  ],
  "adviceTags": [
    "spleen_damp",
    "kidney_yang_weak",
    "gallbladder_metabolism_pressure",
    "reproductive_system_attention"
  ],
  "healthScoreValue": 34,
  "trace": {
    "scoreBreakdown": [
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "liver"
      },
      {
        "rule": "single_meridian_cross",
        "score": -4,
        "target": "liver"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "spleen"
      },
      {
        "rule": "single_meridian_cross",
        "score": -4,
        "target": "spleen"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "kidney"
      },
      {
        "rule": "single_meridian_cross",
        "score": -4,
        "target": "kidney"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "stomach"
      },
      {
        "rule": "single_meridian_cross",
        "score": -4,
        "target": "stomach"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "gallbladder"
      },
      {
        "rule": "single_meridian_cross",
        "score": -4,
        "target": "gallbladder"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "bladder"
      },
      {
        "rule": "single_meridian_cross",
        "score": -4,
        "target": "bladder"
      },
      {
        "rule": "kidney_bladder_double_cross",
        "score": -8
      },
      {
        "rule": "multi_cross",
        "score": -8
      },
      {
        "rule": "neck_waist_reproductive_hit",
        "score": -5
      },
      {
        "rule": "multi_imbalance",
        "score": -8
      }
    ],
    "improvementBonus": {
      "improvedCount": 6,
      "improvementBonus": 4,
      "improvementRule": "multiple_meridians_improved",
      "stableBonus": 0,
      "totalBonus": 4
    },
    "globalPatterns": {
      "leftLowCountBefore": 3,
      "rightLowCountBefore": 3,
      "leftLowCountAfter": 3,
      "rightLowCountAfter": 3,
      "dominantPatternBefore": "mixed",
      "dominantPatternAfter": "mixed",
      "crossCount": 6
    }
  },
  "summary": "根据足部六条经络的温度测量分析，您的经络状态显示多经络交叉失衡，整体健康评分为34分，需重点关注。主要发现包括肝经、脾经、肾经和膀胱经交叉异常，提示代谢、湿气、肾阳和肩颈腰方向存在风险，同时组合判症指出颈椎、生殖系统、肝胆代谢压力需关注。建议从饮食、作息和运动方面进行温和调理，以改善整体经络平衡。",
  "reportSummary": "根据足部六条经络的温度测量分析，您的经络状态显示多经络交叉失衡，整体健康评分为34分，需重点关注。主要发现包括肝经、脾经、肾经和膀胱经交叉异常，提示代谢、湿气、肾阳和肩颈腰方向存在风险，同时组合判症指出颈椎、生殖系统、肝胆代谢压力需关注。建议从饮食、作息和运动方面进行温和调理，以改善整体经络平衡。",
  "storefront": {
    "focusHeadline": "经络交叉失衡，多方向需关注",
    "clientExplanation": "本分析基于中医经络理论，通过温度测量评估身体状态，不等同于医疗诊断，建议结合专业医疗建议进行综合调理。",
    "talkTrack": [
      "您的经络测量显示多经络交叉失衡，提示整体调节状态较不稳定。",
      "肝经和脾经交叉异常可能影响代谢和湿气，需注意饮食和作息。",
      "肾经和膀胱经交叉提示肾阳偏虚和肩颈腰风险，建议加强保暖和适度运动。"
    ],
    "retestPrompt": "建议定期复测以跟踪经络变化，结合生活方式调整观察改善情况。"
  },
  "recommendations": [
    "调整饮食结构，减少油腻食物，增加蔬菜摄入以改善代谢和湿气。",
    "保持规律作息，避免熬夜，尤其在凌晨1-3点肝经当令时注意休息。",
    "适度进行温和运动如散步或瑜伽，以增强肾阳和缓解肩颈腰不适。"
  ]
}
```

</details>

---

## case_multi

### 输入

```json
{
  "subject": {
    "id": "v2-multi-001",
    "name": "多失衡场景"
  },
  "measurementSession": {
    "sessionId": "s005",
    "measuredAt": "2026-04-20T10:00:00",
    "isFollowup": false
  },
  "measurements": {
    "before": {
      "liver": {
        "left": 35.0,
        "right": 35.8
      },
      "spleen": {
        "left": 35.1,
        "right": 35.7
      },
      "kidney": {
        "left": 35.0,
        "right": 35.8
      },
      "stomach": {
        "left": 36.2,
        "right": 35.0
      },
      "gallbladder": {
        "left": 35.0,
        "right": 35.9
      },
      "bladder": {
        "left": 36.0,
        "right": 35.1
      }
    },
    "after": {
      "liver": {
        "left": 35.1,
        "right": 35.7
      },
      "spleen": {
        "left": 35.2,
        "right": 35.6
      },
      "kidney": {
        "left": 35.1,
        "right": 35.7
      },
      "stomach": {
        "left": 36.1,
        "right": 35.1
      },
      "gallbladder": {
        "left": 35.1,
        "right": 35.8
      },
      "bladder": {
        "left": 35.9,
        "right": 35.2
      }
    }
  }
}
```

### 输出摘要

- **引擎模式**：hybrid
- **LLM 模型**：deepseek-chat
- **LLM 延迟**：25.91s
- **综合评分**：55.0
- **等级**：需重点关注
- **摘要**：当前失衡较明显，建议尽早重视。

### 评分上下文

- currentRawScore: 55.0
- displayedScore: 55.0
- scoreLevel: 需重点关注
- adherenceFlag: False
- scoreAdjustedByPolicy: False

### 整体评估

- overallLevel: 失衡较明显
- dominantPattern: 整体偏左
- focusMeridians: ['肝经', '脾经', '肾经', '胃经', '胆经', '膀胱经']
- stableMeridians: []

### 经络明细

| 经络 | 状态 | 严重度 | 交叉 | before | after | 风险点 |
|------|------|--------|------|--------|-------|--------|
| 肝经 | 代谢偏弱 / 气虚倾向 | medium | False | left_low | left_low | 三高风险需关注, 血稠倾向, 乳房结节或小叶增生风险, 温差较大时睡眠质量下降 |
| 脾经 | 脾气偏虚 | medium | False | left_low | left_low | 乏力, 思虑偏重, 血糖代谢需关注, 四肢风险, 膝盖风险 |
| 肾经 | 肾阴偏虚 | medium | False | left_low | left_low | 尿酸偏高风险, 耳鸣耳背, 偏热, 恢复偏慢 |
| 胃经 | 胃阳不足 / 胃寒 | high | False | right_low | right_low | 胃寒, 消化偏弱, 胃胀, 饮食后不适 |
| 胆经 | 胆经偏弱 | medium | False | left_low | left_low | 口干口苦, 偏头痛, 胆红素相关风险 |
| 膀胱经 | 湿下注与腰部方向需关注 | medium | False | right_low | right_low | 大便不成形, 湿气下注大肠, 肺右侧功能风险 |

### 组合命中

命中规则：combo_head_supply, combo_neck, combo_liver_gall

### 建议标签

标签：stomach_cold, gallbladder_metabolism_pressure, head_supply_attention

### 扣分明细

| 规则 | 分值 | 说明 |
|------|------|------|
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| left_bias | -6 |  |
| head_supply_hit | -6 |  |
| neck_waist_reproductive_hit | -5 |  |
| multi_imbalance | -8 |  |
| 改善加分 | +4 | improved=6, stable=0 |

### 完整输出

<details>
<summary>展开 case_multi 完整 JSON 输出</summary>

```json
{
  "engine": {
    "mode": "hybrid",
    "version": "2.0",
    "llmModel": "deepseek-chat",
    "llmLatency": 25.91
  },
  "subject": {
    "id": "v2-multi-001",
    "name": "多失衡场景"
  },
  "engineInference": {
    "dominantPatternBefore": "left_low",
    "dominantPatternAfter": "left_low",
    "lowestMeridianBefore": {
      "meridian": "liver",
      "side": "left",
      "value": 35.0
    },
    "lowestMeridianAfter": {
      "meridian": "liver",
      "side": "left",
      "value": 35.1
    },
    "meridianStates": {
      "liver": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.8,
        "afterDiff": 0.6,
        "cross": false,
        "severity": "medium"
      },
      "spleen": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.6,
        "afterDiff": 0.4,
        "cross": false,
        "severity": "medium"
      },
      "kidney": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.8,
        "afterDiff": 0.6,
        "cross": false,
        "severity": "medium"
      },
      "stomach": {
        "beforeStatus": "right_low",
        "afterStatus": "right_low",
        "beforeLowSide": "right",
        "afterLowSide": "right",
        "beforeDiff": 1.2,
        "afterDiff": 1.0,
        "cross": false,
        "severity": "high"
      },
      "gallbladder": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.9,
        "afterDiff": 0.7,
        "cross": false,
        "severity": "medium"
      },
      "bladder": {
        "beforeStatus": "right_low",
        "afterStatus": "right_low",
        "beforeLowSide": "right",
        "afterLowSide": "right",
        "beforeDiff": 0.9,
        "afterDiff": 0.7,
        "cross": false,
        "severity": "medium"
      }
    },
    "combinationHits": [
      "combo_head_supply",
      "combo_neck",
      "combo_liver_gall"
    ]
  },
  "scoreContext": {
    "currentRawScore": 55.0,
    "displayedScore": 55.0,
    "scoreLevel": "需重点关注",
    "scoreSummary": "当前失衡较明显，建议尽早重视。",
    "instrumentUsageDaysBetweenMeasurements": 0,
    "adherenceFlag": false,
    "scoreAdjustedByPolicy": false
  },
  "healthScore": {
    "score": 55.0,
    "level": "需重点关注",
    "summary": "当前失衡较明显，建议尽早重视。"
  },
  "overallAssessment": {
    "overallLevel": "失衡较明显",
    "dominantPattern": "整体偏左",
    "focusMeridians": [
      "肝经",
      "脾经",
      "肾经",
      "胃经",
      "胆经",
      "膀胱经"
    ],
    "stableMeridians": []
  },
  "meridianDetails": [
    {
      "meridian": "肝经",
      "meridianId": "liver",
      "status": "代谢偏弱 / 气虚倾向",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "三高风险需关注",
        "血稠倾向",
        "乳房结节或小叶增生风险",
        "温差较大时睡眠质量下降"
      ],
      "narrative": "肝经温度偏低，提示代谢偏弱，可能有气虚倾向，影响情绪和睡眠。"
    },
    {
      "meridian": "脾经",
      "meridianId": "spleen",
      "status": "脾气偏虚",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "乏力",
        "思虑偏重",
        "血糖代谢需关注",
        "四肢风险",
        "膝盖风险"
      ],
      "narrative": "脾经温度异常，显示脾气偏虚，可能导致运化不足和湿气问题。"
    },
    {
      "meridian": "肾经",
      "meridianId": "kidney",
      "status": "肾阴偏虚",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "尿酸偏高风险",
        "耳鸣耳背",
        "偏热",
        "恢复偏慢"
      ],
      "narrative": "肾经温度偏低，提示肾阴偏虚，可能伴有尿酸偏高和恢复偏慢。"
    },
    {
      "meridian": "胃经",
      "meridianId": "stomach",
      "status": "胃阳不足 / 胃寒",
      "severity": "high",
      "cross": false,
      "beforeStatus": "right_low",
      "afterStatus": "right_low",
      "riskPoints": [
        "胃寒",
        "消化偏弱",
        "胃胀",
        "饮食后不适"
      ],
      "narrative": "胃经温度失衡，显示胃阳不足，可能有胃寒和消化功能减弱。"
    },
    {
      "meridian": "胆经",
      "meridianId": "gallbladder",
      "status": "胆经偏弱",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "口干口苦",
        "偏头痛",
        "胆红素相关风险"
      ],
      "narrative": "胆经温度偏低，提示胆经偏弱，可能涉及口干口苦和偏头痛风险。"
    },
    {
      "meridian": "膀胱经",
      "meridianId": "bladder",
      "status": "湿下注与腰部方向需关注",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "right_low",
      "afterStatus": "right_low",
      "riskPoints": [
        "大便不成形",
        "湿气下注大肠",
        "肺右侧功能风险"
      ],
      "narrative": "膀胱经温度异常，提示湿下注，需关注腰部和大肠功能。"
    }
  ],
  "combinationAnalysis": [
    {
      "comboId": "combo_head_supply",
      "comboName": "头部供血需关注"
    },
    {
      "comboId": "combo_neck",
      "comboName": "颈椎相关问题需关注"
    },
    {
      "comboId": "combo_liver_gall",
      "comboName": "肝胆代谢压力需关注"
    }
  ],
  "adviceTags": [
    "stomach_cold",
    "gallbladder_metabolism_pressure",
    "head_supply_attention"
  ],
  "healthScoreValue": 55.0,
  "trace": {
    "scoreBreakdown": [
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "liver"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "spleen"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "kidney"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "stomach"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "gallbladder"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "bladder"
      },
      {
        "rule": "left_bias",
        "score": -6
      },
      {
        "rule": "head_supply_hit",
        "score": -6
      },
      {
        "rule": "neck_waist_reproductive_hit",
        "score": -5
      },
      {
        "rule": "multi_imbalance",
        "score": -8
      }
    ],
    "improvementBonus": {
      "improvedCount": 6,
      "improvementBonus": 4,
      "improvementRule": "multiple_meridians_improved",
      "stableBonus": 0,
      "totalBonus": 4
    },
    "globalPatterns": {
      "leftLowCountBefore": 4,
      "rightLowCountBefore": 2,
      "leftLowCountAfter": 4,
      "rightLowCountAfter": 2,
      "dominantPatternBefore": "left_low",
      "dominantPatternAfter": "left_low",
      "crossCount": 0
    }
  },
  "summary": "根据足部经络温度测量分析，您的健康评分为55.0，显示失衡较明显，需重点关注。主要发现包括：胃经胃阳不足，提示胃寒和消化偏弱；肝经代谢偏弱，有气虚倾向；脾经脾气偏虚，影响运化功能；肾经肾阴偏虚，可能伴有尿酸偏高风险；胆经偏弱，涉及胆红素代谢；膀胱经湿下注，提示腰部和大肠方向需关注。组合判症显示头部供血、颈椎问题和肝胆代谢压力需留意。建议方向：加强胃部保暖，调整饮食规律，关注肝胆代谢，并注意颈椎和头部循环。",
  "reportSummary": "根据足部经络温度测量分析，您的健康评分为55.0，显示失衡较明显，需重点关注。主要发现包括：胃经胃阳不足，提示胃寒和消化偏弱；肝经代谢偏弱，有气虚倾向；脾经脾气偏虚，影响运化功能；肾经肾阴偏虚，可能伴有尿酸偏高风险；胆经偏弱，涉及胆红素代谢；膀胱经湿下注，提示腰部和大肠方向需关注。组合判症显示头部供血、颈椎问题和肝胆代谢压力需留意。建议方向：加强胃部保暖，调整饮食规律，关注肝胆代谢，并注意颈椎和头部循环。",
  "storefront": {
    "focusHeadline": "胃寒与代谢失衡需调理",
    "clientExplanation": "本分析基于中医经络理论，通过温度测量评估身体状态，不等同于医疗诊断，建议结合专业医疗意见。",
    "talkTrack": [
      "您的测量结果显示胃经功能偏弱，可能有胃寒和消化不适的情况。",
      "肝经和胆经提示代谢压力，需关注胆固醇和睡眠质量。",
      "整体偏向左侧，建议注意头部供血和颈椎健康，通过饮食和作息调整来改善。"
    ],
    "retestPrompt": "建议定期复测以跟踪调理效果，尤其是在调整饮食或生活习惯后。"
  },
  "recommendations": [
    "加强胃部保暖，避免生冷食物，规律饮食以改善胃寒。",
    "关注肝胆代谢，减少油腻饮食，适当运动以缓解代谢压力。",
    "注意颈椎保健，避免长时间低头，并结合中医调理如艾灸或按摩。"
  ]
}
```

</details>

---

## case_followup

### 输入

```json
{
  "subject": {
    "id": "v2-followup-001",
    "name": "复测保护场景"
  },
  "measurementSession": {
    "sessionId": "s006",
    "measuredAt": "2026-04-20T10:00:00",
    "isFollowup": true,
    "daysSinceLastMeasurement": 30,
    "instrumentUsageDaysBetweenMeasurements": 25
  },
  "measurements": {
    "before": {
      "liver": {
        "left": 35.0,
        "right": 36.1
      },
      "spleen": {
        "left": 35.1,
        "right": 35.9
      },
      "kidney": {
        "left": 35.0,
        "right": 35.8
      },
      "stomach": {
        "left": 35.1,
        "right": 36.0
      },
      "gallbladder": {
        "left": 35.0,
        "right": 35.9
      },
      "bladder": {
        "left": 35.2,
        "right": 35.9
      }
    },
    "after": {
      "liver": {
        "left": 35.0,
        "right": 36.0
      },
      "spleen": {
        "left": 35.2,
        "right": 35.8
      },
      "kidney": {
        "left": 35.1,
        "right": 35.7
      },
      "stomach": {
        "left": 35.3,
        "right": 35.9
      },
      "gallbladder": {
        "left": 35.2,
        "right": 35.8
      },
      "bladder": {
        "left": 35.4,
        "right": 35.8
      }
    }
  },
  "scoreContext": {
    "previousDisplayedScore": 82
  }
}
```

### 输出摘要

- **引擎模式**：hybrid
- **LLM 模型**：deepseek-chat
- **LLM 延迟**：28.7s
- **综合评分**：82
- **等级**：轻度失衡
- **摘要**：整体状态尚可，局部仍需关注。

### 评分上下文

- currentRawScore: 55.0
- displayedScore: 82
- scoreLevel: 轻度失衡
- adherenceFlag: True
- scoreAdjustedByPolicy: True

### 整体评估

- overallLevel: 整体存在一定失衡
- dominantPattern: 整体偏左
- focusMeridians: ['肝经', '脾经', '肾经', '胃经', '胆经', '膀胱经']
- stableMeridians: []

### 经络明细

| 经络 | 状态 | 严重度 | 交叉 | before | after | 风险点 |
|------|------|--------|------|--------|-------|--------|
| 肝经 | 代谢偏弱 / 气虚倾向 | high | False | left_low | left_low | 三高风险需关注, 血稠倾向, 乳房结节或小叶增生风险, 温差较大时睡眠质量下降 |
| 脾经 | 脾气偏虚 | medium | False | left_low | left_low | 乏力, 思虑偏重, 血糖代谢需关注, 四肢风险, 膝盖风险 |
| 肾经 | 肾阴偏虚 | medium | False | left_low | left_low | 尿酸偏高风险, 耳鸣耳背, 偏热, 恢复偏慢 |
| 胃经 | 胃部津液偏少 | medium | False | left_low | left_low | 胃炎倾向, 反酸, 胃部刺激, 饮食不规律风险 |
| 胆经 | 胆经偏弱 | medium | False | left_low | left_low | 口干口苦, 偏头痛, 胆红素相关风险 |
| 膀胱经 | 肩颈腰与肠道方向需关注 | medium | False | left_low | left_low | 肩颈腰问题, 便秘, 痔疮, 大肠息肉风险, 肺左侧功能风险 |

### 组合命中

命中规则：combo_head_supply, combo_waist, combo_neck, combo_liver_gall

### 建议标签

标签：gallbladder_metabolism_pressure, head_supply_attention

### 扣分明细

| 规则 | 分值 | 说明 |
|------|------|------|
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| single_meridian_obvious_abnormal | -4 |  |
| left_bias | -6 |  |
| head_supply_hit | -6 |  |
| neck_waist_reproductive_hit | -5 |  |
| multi_imbalance | -8 |  |
| 改善加分 | +4 | improved=6, stable=0 |

### 完整输出

<details>
<summary>展开 case_followup 完整 JSON 输出</summary>

```json
{
  "engine": {
    "mode": "hybrid",
    "version": "2.0",
    "llmModel": "deepseek-chat",
    "llmLatency": 28.7
  },
  "subject": {
    "id": "v2-followup-001",
    "name": "复测保护场景"
  },
  "engineInference": {
    "dominantPatternBefore": "left_low",
    "dominantPatternAfter": "left_low",
    "lowestMeridianBefore": {
      "meridian": "liver",
      "side": "left",
      "value": 35.0
    },
    "lowestMeridianAfter": {
      "meridian": "liver",
      "side": "left",
      "value": 35.0
    },
    "meridianStates": {
      "liver": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 1.1,
        "afterDiff": 1.0,
        "cross": false,
        "severity": "high"
      },
      "spleen": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.8,
        "afterDiff": 0.6,
        "cross": false,
        "severity": "medium"
      },
      "kidney": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.8,
        "afterDiff": 0.6,
        "cross": false,
        "severity": "medium"
      },
      "stomach": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.9,
        "afterDiff": 0.6,
        "cross": false,
        "severity": "medium"
      },
      "gallbladder": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.9,
        "afterDiff": 0.6,
        "cross": false,
        "severity": "medium"
      },
      "bladder": {
        "beforeStatus": "left_low",
        "afterStatus": "left_low",
        "beforeLowSide": "left",
        "afterLowSide": "left",
        "beforeDiff": 0.7,
        "afterDiff": 0.4,
        "cross": false,
        "severity": "medium"
      }
    },
    "combinationHits": [
      "combo_head_supply",
      "combo_waist",
      "combo_neck",
      "combo_liver_gall"
    ]
  },
  "scoreContext": {
    "currentRawScore": 55.0,
    "displayedScore": 82,
    "scoreLevel": "轻度失衡",
    "scoreSummary": "整体状态尚可，局部仍需关注。",
    "instrumentUsageDaysBetweenMeasurements": 25,
    "adherenceFlag": true,
    "scoreAdjustedByPolicy": true
  },
  "healthScore": {
    "score": 82,
    "level": "轻度失衡",
    "summary": "整体状态尚可，局部仍需关注。"
  },
  "overallAssessment": {
    "overallLevel": "整体存在一定失衡",
    "dominantPattern": "整体偏左",
    "focusMeridians": [
      "肝经",
      "脾经",
      "肾经",
      "胃经",
      "胆经",
      "膀胱经"
    ],
    "stableMeridians": []
  },
  "meridianDetails": [
    {
      "meridian": "肝经",
      "meridianId": "liver",
      "status": "代谢偏弱 / 气虚倾向",
      "severity": "high",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "三高风险需关注",
        "血稠倾向",
        "乳房结节或小叶增生风险",
        "温差较大时睡眠质量下降"
      ],
      "narrative": "肝经数据显示代谢偏弱，提示气虚倾向，可能影响情绪和睡眠。"
    },
    {
      "meridian": "脾经",
      "meridianId": "spleen",
      "status": "脾气偏虚",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "乏力",
        "思虑偏重",
        "血糖代谢需关注",
        "四肢风险",
        "膝盖风险"
      ],
      "narrative": "脾经脾气偏虚，可能导致运化功能减弱，需关注湿气和血糖代谢。"
    },
    {
      "meridian": "肾经",
      "meridianId": "kidney",
      "status": "肾阴偏虚",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "尿酸偏高风险",
        "耳鸣耳背",
        "偏热",
        "恢复偏慢"
      ],
      "narrative": "肾经肾阴偏虚，提示肾阴不足，可能影响骨骼和听力健康。"
    },
    {
      "meridian": "胃经",
      "meridianId": "stomach",
      "status": "胃部津液偏少",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "胃炎倾向",
        "反酸",
        "胃部刺激",
        "饮食不规律风险"
      ],
      "narrative": "胃经津液偏少，提示胃部功能需关注，可能伴有消化不适。"
    },
    {
      "meridian": "胆经",
      "meridianId": "gallbladder",
      "status": "胆经偏弱",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "口干口苦",
        "偏头痛",
        "胆红素相关风险"
      ],
      "narrative": "胆经偏弱，提示胆经功能需加强，可能影响代谢和偏头痛。"
    },
    {
      "meridian": "膀胱经",
      "meridianId": "bladder",
      "status": "肩颈腰与肠道方向需关注",
      "severity": "medium",
      "cross": false,
      "beforeStatus": "left_low",
      "afterStatus": "left_low",
      "riskPoints": [
        "肩颈腰问题",
        "便秘",
        "痔疮",
        "大肠息肉风险",
        "肺左侧功能风险"
      ],
      "narrative": "膀胱经数据显示肩颈腰与肠道方向需关注，提示相关部位可能存在问题。"
    }
  ],
  "combinationAnalysis": [
    {
      "comboId": "combo_head_supply",
      "comboName": "头部供血需关注"
    },
    {
      "comboId": "combo_waist",
      "comboName": "腰椎相关问题需关注"
    },
    {
      "comboId": "combo_neck",
      "comboName": "颈椎相关问题需关注"
    },
    {
      "comboId": "combo_liver_gall",
      "comboName": "肝胆代谢压力需关注"
    }
  ],
  "adviceTags": [
    "gallbladder_metabolism_pressure",
    "head_supply_attention"
  ],
  "healthScoreValue": 82,
  "trace": {
    "scoreBreakdown": [
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "liver"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "spleen"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "kidney"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "stomach"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "gallbladder"
      },
      {
        "rule": "single_meridian_obvious_abnormal",
        "score": -4,
        "target": "bladder"
      },
      {
        "rule": "left_bias",
        "score": -6
      },
      {
        "rule": "head_supply_hit",
        "score": -6
      },
      {
        "rule": "neck_waist_reproductive_hit",
        "score": -5
      },
      {
        "rule": "multi_imbalance",
        "score": -8
      }
    ],
    "improvementBonus": {
      "improvedCount": 6,
      "improvementBonus": 4,
      "improvementRule": "multiple_meridians_improved",
      "stableBonus": 0,
      "totalBonus": 4
    },
    "globalPatterns": {
      "leftLowCountBefore": 6,
      "rightLowCountBefore": 0,
      "leftLowCountAfter": 6,
      "rightLowCountAfter": 0,
      "dominantPatternBefore": "left_low",
      "dominantPatternAfter": "left_low",
      "crossCount": 0
    }
  },
  "summary": "根据足部六条经络的温度测量数据，您的健康评分为82分，属于轻度失衡状态。整体分析显示，经络系统存在一定失衡，偏向左侧，提示头部供血方向需关注。主要发现包括肝经代谢偏弱、脾经脾气偏虚、肾经肾阴偏虚、胃经津液偏少、胆经偏弱以及膀胱经肩颈腰与肠道方向需关注。组合判症提示腰椎、颈椎相关问题及肝胆代谢压力需重点关注。建议从调整作息、饮食和适度运动入手，以促进经络平衡和整体健康。",
  "reportSummary": "根据足部六条经络的温度测量数据，您的健康评分为82分，属于轻度失衡状态。整体分析显示，经络系统存在一定失衡，偏向左侧，提示头部供血方向需关注。主要发现包括肝经代谢偏弱、脾经脾气偏虚、肾经肾阴偏虚、胃经津液偏少、胆经偏弱以及膀胱经肩颈腰与肠道方向需关注。组合判症提示腰椎、颈椎相关问题及肝胆代谢压力需重点关注。建议从调整作息、饮食和适度运动入手，以促进经络平衡和整体健康。",
  "storefront": {
    "focusHeadline": "经络轻度失衡，重点关注头部供血与肝胆代谢",
    "clientExplanation": "基于中医经络理论，本次分析显示您的经络状态存在轻度失衡，不等同于医疗诊断，建议结合生活习惯调整以改善健康。",
    "talkTrack": [
      "您好，根据您的经络测量数据，整体评分82分，属于轻度失衡状态。",
      "数据显示，您的肝经代谢偏弱，脾经脾气偏虚，肾经肾阴偏虚，胃经津液偏少，胆经偏弱，膀胱经肩颈腰与肠道方向需关注。",
      "组合分析提示头部供血、腰椎、颈椎及肝胆代谢方向需重点关注，建议从日常作息和饮食入手进行调整。"
    ],
    "retestPrompt": "建议在调整生活习惯后1-2周进行复测，以观察经络状态变化。"
  },
  "recommendations": [
    "建议调整作息，确保充足睡眠，特别是凌晨1-3点肝经当令时段，以养肝血。",
    "注意饮食规律，避免生冷食物，增加温和易消化食物，以改善胃经和脾经功能。",
    "适度进行肩颈腰部的伸展运动，并关注肝胆代谢，减少高脂肪食物摄入，以缓解代谢压力。"
  ]
}
```

</details>

---
