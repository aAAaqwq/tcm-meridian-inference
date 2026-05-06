# TCM v3 API 完整测试用例示例

本文档提供全部34个测试用例的完整请求/响应示例，用于API开发和测试参考。

**测试用例位置**: `fixtures/v3/`  
**实际输出位置**: `docs/v3/testing/actual-results/` (Rule-only 模式)  
**Agent输出位置**: `docs/v3/testing/agent-results/` (Hybrid 模式，包含LLM生成文案)

---

## 模式说明

| 模式 | 说明 | 输出字段 |
|------|------|----------|
| `rule` | 纯规则引擎 + 模板化建议 | `engine`, `score_result`, `meridian_analysis`, `focus_issues`, `summary`, `storefront`, `recommendations` |
| `hybrid` (默认) | 规则引擎 + LLM生成文案 | 所有rule字段，但文案由LLM生成，更自然个性化 |

### 两种模式的区别

| 字段 | `rule` 模式 | `hybrid` 模式 |
|------|-------------|---------------|
| `summary` | 模板化生成，基于分数等级和重点问题 | LLM生成，更自然流畅 |
| `storefront.talkTrack` | 固定模板话术 | LLM根据具体情况生成 |
| `recommendations` | 模板化建议列表 | LLM生成的个性化建议 |
| 生成速度 | 快（本地计算） | 慢（需调用LLM API） |
| 依赖 | 无需API Key | 需要 DeepSeek API Key |

**建议**:
- 生产环境默认使用 `hybrid` 模式（有API Key时自动启用）
- 网络不稳定或无需LLM时，使用 `rule` 模式也有完整的建议输出

---

## 测试用例索引

| 编号 | 测试文件 | 场景 | 预期分数 | 关键验证点 |
|------|----------|------|----------|------------|
| 1 | test_01_excellent_score | 健康优秀 | 89 | 全部平衡 |
| 2 | test_02_mild_imbalance | 轻度失衡 | 89 | 肝/脾轻微异常 |
| 3 | test_03_moderate_imbalance | 中度失衡 | 76 | 6条左低 |
| 4 | test_04_significant_imbalance | 明显失衡 | 75 | 交叉+严重温差 |
| 5 | test_05_trend_stable_left_low | stable_left_low | 74 | 肾+膀胱左低=腰椎 |
| 6 | test_06_trend_stable_right_low | stable_right_low | 74 | 肾+膀胱右低=腰椎 |
| 7 | test_07_trend_cross | cross | 77 | 交叉=颈椎+腰椎 |
| 8 | test_08_trend_potential_symptom | potential_symptom | 89 | 潜在症状 |
| 9 | test_09_trend_fast_response | fast_response | 89 | 调理反应快 |
| 10 | test_10_diff_levels | 温差等级 | 75 | 4种温差等级 |
| 11 | test_11_side_bias_4 | 偏侧4条 | 84 | C=3.5 |
| 12 | test_12_side_bias_5 | 偏侧5条 | 82 | C=5 |
| 13 | test_13_side_bias_6 | 偏侧6条 | 80 | C=6 |
| 14 | test_14_cervical_opposite | 相反低 | 86 | 颈椎 |
| 15 | test_15_cervical_lumbar_cross | 膀胱交叉 | 86 | 颈椎+腰椎 |
| 16 | test_16_gender_male | 男性过滤 | 80 | 男性专属词 |
| 17 | test_17_gender_female | 女性过滤 | 80 | 女性专属词 |
| 18 | test_18_gender_unknown | 未知性别 | 80 | 中性词 |
| 19 | test_19_retest_0_2_days | 复测0-2天 | 77 | usage_bonus=0 |
| 20 | test_20_retest_3_6_days | 复测3-6天 | 78 | usage_bonus=1 |
| 21 | test_21_retest_7_13_days | 复测7-13天 | 79 | usage_bonus=2 |
| 22 | test_22_retest_14_29_low | 复测14-29天(<88) | 80 | usage_bonus=3 |
| 23 | test_23_retest_14_29_high | 复测14-29天(≥88) | 95 | usage_bonus=3 |
| 24 | test_24_retest_30_plus | 复测30天+ | 81 | usage_bonus=4 |
| 25 | test_25_retest_improvement | 数据改善 | 95 | improvement_bonus=3 |
| 26 | test_26_low_temp_index | A=6最大档 | 88 | 低温差距>3℃ |
| 27 | test_27_diff_improved | 温差改善 | 89 | diff改善-0.5 |
| 28 | test_28_diff_worsened | 温差恶化 | 88 | diff恶化+0.5 |
| 29 | test_29_realistic_mild | 真实轻度 | 89 | 真实数据 |
| 30 | test_30_realistic_moderate | 真实中度 | 76 | 真实数据 |
| 31 | test_31_bladder_lowest | 膀胱最低 | 83 | 膀胱问题 |
| 32 | test_32_kidney_cross | 肾交叉 | 84 | 肾交叉=颈椎+腰椎 |
| 33 | case_01_first_test | PRD首测示例 | 77 | 标准示例 |
| 34 | case_02_retest | PRD复测示例 | 89 | 复测改善 |

---

## 1. 首测 - 健康优秀 (test_01_excellent_score)

### 1.1 请求

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0},
    "gallbladder": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0},
    "bladder": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0},
    "liver": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0},
    "spleen": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0},
    "kidney": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0}
  }
}
```

### 1.2 Rule-only 响应

```json
{
  "engine": {"mode": "rule-based-v3", "version": "3.0"},
  "score_result": {
    "score": 89,
    "score_raw": 90.0,
    "problem_index": 0.0,
    "problem_index_detail": {
      "low_temperature_index": 0.0,
      "temperature_difference_index": 0.0,
      "side_bias_index": 0.0,
      "trend_index": 0.0,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {"meridian": "stomach", "side": "left", "value": 40.0, "rank": 1, "must_report": true},
      {"meridian": "stomach", "side": "right", "value": 40.0, "rank": 2, "must_report": true}
    ]
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 0,
    "balanced_count": 6,
    "result": "none"
  },
  "cervical_lumbar_result": {"result": "none"},
  "focus_issues": [
    {"priority": 1, "type": "lowest_point", "title": "胃经问题较突出", "meridian": "stomach"}
  ]
}
```

### 1.3 Hybrid (Agent) 响应

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 5.23},
  "score_result": {"score": 89, "score_raw": 90.0, "problem_index": 0.0},
  "side_bias_summary": {"left_low_count": 0, "right_low_count": 0, "result": "none"},
  "cervical_lumbar_result": {"result": "none"},
  "meridian_analysis": [...],
  "focus_issues": [...],
  
  "// --- 以下为LLM生成字段 ---": "",
  
  "summary": "恭喜！本次检测显示您的综合健康分89分，属于健康优秀水平。六条经络温度平衡，无明显失衡点，整体气血运行良好。建议继续保持规律作息和健康饮食，定期复测维护健康状态。",
  "reportSummary": "恭喜！本次检测显示您的综合健康分89分，属于健康优秀水平...",
  
  "storefront": {
    "focusHeadline": "整体状态良好，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。您的综合健康分89分，处于健康优秀水平。",
    "talkTrack": [
      "您的六条经络温度平衡，气血运行顺畅，这是一个非常好的状态。",
      "建议继续保持当前的作息和饮食习惯，定期复测以维护健康。",
      "如果有任何不适，请及时就医咨询专业医生。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  },
  
  "recommendations": [
    "保持规律作息，早睡早起，保证充足睡眠。",
    "均衡饮食，多摄入新鲜蔬果和优质蛋白。",
    "适度运动，如散步、瑜伽、太极等，促进气血流通。",
    "保持心情愉悦，减少压力，定期放松身心。"
  ]
}
```

### 1.3 Hybrid (Agent) 响应

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 7.92},
  "score_result": {"score": 89, "score_raw": 89.4, "problem_index": 1.5},
  "lowest_points": {
    "selected": [
      {"meridian": "spleen", "side": "left", "value": 39.7, "rank": 1},
      {"meridian": "liver", "side": "left", "value": 39.8, "rank": 2}
    ]
  },
  "side_bias_summary": {"left_low_count": 2, "right_low_count": 0, "result": "none"},
  "cervical_lumbar_result": {"result": "none"},

  "// --- LLM生成字段 ---": "",

  "summary": "您的检测结果显示整体状态良好，经络温度都在正常范围。但脾经和肝经存在轻微不平衡。脾经与消化、思虑相关，略低提示过滤功能和气血方面需稍加关注；肝经与代谢、解毒相关，左侧略低提示血液循环和代谢有提升空间。建议在饮食、作息上做相应调理，保持良好状态。",
  "reportSummary": "您的检测结果显示整体状态良好，经络温度都在正常范围。但脾经和肝经存在轻微不平衡...",

  "storefront": {
    "focusHeadline": "脾经肝经需温和调理",
    "clientExplanation": "本次检测基于中医经络理论，结果仅反映当前状态，不等同于医疗诊断。",
    "talkTrack": [
      "您这次的检测结果整体不错，脏腑功能基本平衡。",
      "不过脾经和肝经有一点小提示，可能与消化、思虑或代谢有关。",
      "通过一些生活习惯的小调整，可以帮助改善这些方面，让身体状态更好。"
    ],
    "retestPrompt": "建议一个月后复测，观察调理效果。"
  },

  "recommendations": [
    "饮食上可适当增加山药、茯苓、薏米等健脾祛湿的食物，少吃油腻甜食，减轻脾的负担。",
    "保持规律作息，尽量在晚上11点前入睡，以利于肝的代谢解毒功能。",
    "推荐每天进行30分钟有氧运动，如快走、瑜伽，促进血液循环和气血运行。"
  ]
}
```

---

## 2. 首测 - 中度失衡 (test_03_moderate_imbalance)

### 请求

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {"group1_left": 36.5, "group1_right": 38.0, "group2_left": 39.0, "group2_right": 40.0},
    "gallbladder": {"group1_left": 36.0, "group1_right": 38.0, "group2_left": 38.5, "group2_right": 40.0},
    "bladder": {"group1_left": 35.0, "group1_right": 37.0, "group2_left": 37.0, "group2_right": 40.0},
    "liver": {"group1_left": 36.0, "group1_right": 37.5, "group2_left": 38.0, "group2_right": 40.0},
    "spleen": {"group1_left": 35.5, "group1_right": 37.0, "group2_left": 38.0, "group2_right": 39.5},
    "kidney": {"group1_left": 35.0, "group1_right": 36.0, "group2_left": 37.0, "group2_right": 39.0}
  }
}
```

### 响应

```json
{
  "engine": {"mode": "rule-based-v3", "version": "3.0"},
  "score_result": {
    "score": 76,
    "score_raw": 76.2,
    "problem_index": 26.0,
    "problem_index_detail": {
      "low_temperature_index": 3.0,
      "temperature_difference_index": 11.5,
      "side_bias_index": 6.0,
      "trend_index": 3.0,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {"meridian": "bladder", "side": "left", "value": 37.0, "rank": 1, "must_report": true},
      {"meridian": "liver", "side": "left", "value": 38.0, "rank": 2, "must_report": true}
    ]
  },
  "side_bias_summary": {
    "left_low_count": 6,
    "right_low_count": 0,
    "balanced_count": 0,
    "result": "head_blood_supply_attention"
  },
  "cervical_lumbar_result": {
    "result": "lumbar",
    "kidney_trend": "stable_left_low",
    "bladder_trend": "stable_left_low"
  },
  "focus_issues": [
    {"priority": 1, "title": "膀胱经问题较突出"},
    {"priority": 2, "title": "肝经问题较突出"},
    {"priority": 3, "title": "头部供血需关注"},
    {"priority": 4, "title": "腰椎相关问题需关注"}
  ]
}
```

### 2.2 Hybrid (Agent) 响应

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 10.43},
  "score_result": {
    "score": 76,
    "score_raw": 76.2,
    "problem_index": 26.0
  },
  "lowest_points": {
    "selected": [
      {"meridian": "bladder", "side": "left", "value": 37.0, "rank": 1},
      {"meridian": "liver", "side": "left", "value": 38.0, "rank": 2}
    ]
  },
  "side_bias_summary": {
    "left_low_count": 6,
    "right_low_count": 0,
    "result": "head_blood_supply_attention"
  },
  "cervical_lumbar_result": {
    "result": "lumbar",
    "kidney_trend": "stable_left_low",
    "bladder_trend": "stable_left_low"
  },
  
  "// --- LLM生成字段 ---": "",
  
  "summary": "本次检测显示您的综合健康分为76分，属于中度失衡状态。膀胱经和肝经问题较为突出，同时存在整体偏左的趋势，提示头部供血和腰椎方面需要关注。建议从调理经络平衡入手，改善血液循环和代谢功能。",
  "reportSummary": "本次检测显示您的综合健康分为76分，属于中度失衡状态...",
  
  "storefront": {
    "focusHeadline": "经络失衡，关注腰背与代谢",
    "clientExplanation": "本次检测基于足部经络温度分析，结果仅反映当前经络状态，不等同于医疗诊断。建议结合自身感受，如有不适请及时就医。",
    "talkTrack": [
      "您的检测结果显示，膀胱经和肝经的温差比较明显，提示腰背部和代谢方面需要多关注。",
      "整体来看，身体左侧温度偏低，可能影响头部供血，平时有没有感觉头晕或注意力不集中？",
      "建议您注意保暖，尤其是腰背和脚部，同时调整饮食和作息，帮助身体恢复平衡。"
    ],
    "retestPrompt": "建议在调理2-4周后进行复测，观察经络变化情况。"
  },
  
  "recommendations": [
    "饮食建议：多吃黑色食物（黑豆、黑芝麻）补肾，绿色蔬菜（菠菜、西兰花）养肝，避免油腻和甜食。",
    "作息建议：晚上11点前入睡，保证7-8小时睡眠，有助于肝胆排毒和肾精恢复。",
    "运动建议：每天练习八段锦或瑜伽，重点拉伸腰背和腿部经络，促进气血循环。",
    "保暖建议：注意腰背和脚部保暖，可用热水泡脚或艾灸膀胱经穴位（如委中、承山）。",
    "情绪管理：减少思虑，可通过冥想或深呼吸放松，避免过度操心。"
  ]
}
```

**关键验证**:
- 6条经络全部左低 → C=6 (偏侧指数)
- 肾+膀胱都 stable_left_low → 腰椎问题
- 低温差距 3℃ (40-37) → A=3

---

## 3. 趋势 - Cross (test_07_trend_cross)

### 请求

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {"group1_left": 38.0, "group1_right": 36.0, "group2_left": 36.0, "group2_right": 38.0},
    "gallbladder": {"group1_left": 38.0, "group1_right": 36.0, "group2_left": 36.0, "group2_right": 38.0},
    "bladder": {"group1_left": 36.0, "group1_right": 38.0, "group2_left": 38.0, "group2_right": 37.0},
    "liver": {"group1_left": 38.0, "group1_right": 36.0, "group2_left": 36.0, "group2_right": 38.0},
    "spleen": {"group1_left": 38.0, "group1_right": 36.0, "group2_left": 36.0, "group2_right": 38.0},
    "kidney": {"group1_left": 36.0, "group1_right": 38.0, "group2_left": 38.0, "group2_right": 37.0}
  }
}
```

### 响应

```json
{
  "engine": {"mode": "rule-based-v3", "version": "3.0"},
  "score_result": {
    "score": 77,
    "score_raw": 77.0,
    "problem_index": 25.0,
    "problem_index_detail": {
      "low_temperature_index": 3.0,
      "temperature_difference_index": 9.5,
      "side_bias_index": 6.0,
      "trend_index": 4.0,
      "combo_index": 2.5
    }
  },
  "cervical_lumbar_result": {
    "result": "cervical_and_lumbar",
    "kidney_trend": "cross",
    "bladder_trend": "cross"
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 6,
    "result": "heart_attention"
  }
}
```

**关键验证**:
- 肾/膀胱交叉 → 颈椎+腰椎同时存在
- D趋势封顶=4 (cross=1.2×6=7.2, 封顶4)

### 3.1 Hybrid (Agent) 响应

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 8.32},
  "score_result": {"score": 77, "score_raw": 77.0, "problem_index": 25.0},
  "cervical_lumbar_result": {"result": "cervical_and_lumbar", "kidney_trend": "cross", "bladder_trend": "cross"},
  "side_bias_summary": {"left_low_count": 0, "right_low_count": 6, "result": "heart_attention"},

  "// --- LLM生成字段 ---": "",

  "summary": "本次检测显示您的经络存在明显的交叉失衡模式，六条经络均呈现交叉趋势，导致颈椎和腰椎问题同时被提示。整体偏向右侧低温，提示心脏供血方向需要关注。综合健康分77分，处于中度失衡状态，建议通过系统性的经络调理来改善身体平衡。",
  "reportSummary": "本次检测显示您的经络存在明显的交叉失衡模式，六条经络均呈现交叉趋势...",

  "storefront": {
    "focusHeadline": "经络交叉失衡，颈椎腰椎需关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。您的经络呈现特殊的交叉失衡模式，提示颈椎和腰椎区域需要同时关注。",
    "talkTrack": [
      "您的检测结果显示一个比较特殊的模式，六条经络都呈现交叉状态，这意味着身体左右能量流动存在失衡。",
      "这种模式同时提示颈椎和腰椎问题，可能和长期姿势不良或脊柱压力有关。",
      "另外整体偏向右侧温度偏低，也需要关注心脏供血方面的调理。",
      "建议您从改善日常姿势开始，配合经络调理，逐步恢复身体平衡。"
    ],
    "retestPrompt": "建议坚持调理3-4周后复测，观察交叉失衡模式的改善情况。"
  },

  "recommendations": [
    "注意保持正确坐姿，避免长时间低头或弯腰，每小时起身活动5-10分钟。",
    "可进行颈椎和腰椎的温和拉伸运动，如猫牛式、颈部环绕等，每天15分钟。",
    "建议使用经络调理仪同时关注颈椎和腰椎区域，促进局部气血循环。",
    "保持规律作息，避免熬夜，有助于整体经络平衡的恢复。"
  ]
}
```

---

## 4. 复测 - 改善 (case_02_retest)

### 请求

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 77,
  "previous_problem_index": 24.9,
  "usage_days_between_tests": 14,
  "meridians": {
    "stomach": {"group1_left": 40.0, "group1_right": 40.5, "group2_left": 42.5, "group2_right": 42.6},
    "gallbladder": {"group1_left": 37.0, "group1_right": 37.0, "group2_left": 42.2, "group2_right": 42.2},
    "bladder": {"group1_left": 37.0, "group1_right": 37.2, "group2_left": 40.0, "group2_right": 41.0},
    "liver": {"group1_left": 37.0, "group1_right": 36.8, "group2_left": 40.0, "group2_right": 40.2},
    "spleen": {"group1_left": 37.0, "group1_right": 36.8, "group2_left": 40.0, "group2_right": 40.8},
    "kidney": {"group1_left": 37.0, "group1_right": 37.0, "group2_left": 41.0, "group2_right": 41.5}
  }
}
```

### 响应

```json
{
  "engine": {"mode": "rule-based-v3", "version": "3.0"},
  "score_result": {
    "score": 89,
    "score_raw": 89.42,
    "problem_index": 14.7
  },
  "retest_detail": {
    "usage_days": 14,
    "usage_bonus": 3.0,
    "delta_I": 10.2,
    "improvement_bonus": 3.0,
    "previous_score": 77,
    "previous_problem_index": 24.9,
    "current_problem_index": 14.7,
    "retest_score_base": 83.42,
    "protected_score": 86.42
  },
  "side_bias_summary": {
    "left_low_count": 5,
    "right_low_count": 0,
    "result": "head_blood_supply_attention"
  }
}
```

### 4.2 Hybrid (Agent) 响应

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 9.79},
  "score_result": {"score": 89, "score_raw": 83.42, "problem_index": 14.7},
  "retest_detail": {
    "usage_days": 14,
    "usage_bonus": 3.0,
    "delta_I": 10.2,
    "improvement_bonus": 3.0,
    "previous_score": 77,
    "previous_problem_index": 24.9,
    "current_problem_index": 14.7,
    "retest_score_base": 83.42,
    "protected_score": 86.42
  },
  "side_bias_summary": {"left_low_count": 5, "right_low_count": 0, "result": "head_blood_supply_attention"},
  
  "// --- LLM生成字段 ---": "",
  
  "summary": "本次复测显示您整体健康状况有所改善，综合健康分从77提升至89，说明调理见效。但仍有几个经络需要关注，尤其是膀胱经、肝经和脾经，提示肩颈腰、内分泌和代谢方面可能需要持续调理。头部供血方向偏左也需留意。",
  "reportSummary": "本次复测显示您整体健康状况有所改善，综合健康分从77提升至89...",
  
  "storefront": {
    "focusHeadline": "膀胱与肝经需关注",
    "clientExplanation": "本次检测结果显示您身体有多处失衡，尤其是膀胱经和肝经，需结合日常调理改善。请注意，本报告基于经络温度分析，不等同于医疗诊断。",
    "talkTrack": [
      "您的整体健康分从77分提升到了89分，说明我们之前做的调理方向是对的，您也配合得非常好。",
      "不过这次数据显示，膀胱经和肝经的温度差异比较明显，这可能和您肩颈腰的不适、消化代谢有关。",
      "另外脾经也有波动，提示湿气和思虑可能还在影响您。我们需要根据这些调整一下后续的调理方案。"
    ],
    "retestPrompt": "建议继续按照调理方案执行，14天后再次检测，观察改善情况。"
  },
  
  "recommendations": [
    "膀胱经方面：建议多做肩颈和腰背部疏通，如热敷、轻柔拉伸，避免久坐；饮食上多吃富含纤维的蔬菜水果，如芹菜、香蕉，促进肠道蠕动。",
    "肝经方面：建议保持规律作息，尽量在23点前入睡；减少油腻食物和酒精摄入，可适当喝菊花枸杞茶疏肝明目。",
    "脾经方面：建议少吃生冷甜腻食物，多吃薏米、山药、红豆等健脾祛湿食材；适当进行有氧运动如快走、瑜伽，帮助排湿。"
  ]
}
```

**关键验证**:
- 14天使用 → usage_bonus=3
- 问题指数改善 10.2 → improvement_bonus=3 (封顶)
- 保护分数: max(83.42, 77+1=78) = 83.42 → 实际89 (加上improvement_bonus)

---

## 5. 复测 - 30天+ (test_24_retest_30_plus_days)

### 请求

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 75,
  "previous_problem_index": 28.0,
  "usage_days_between_tests": 35,
  "meridians": {
    "stomach": {"group1_left": 36.5, "group1_right": 38.0, "group2_left": 39.0, "group2_right": 40.0},
    "gallbladder": {"group1_left": 36.0, "group1_right": 38.0, "group2_left": 38.5, "group2_right": 40.0},
    "bladder": {"group1_left": 35.0, "group1_right": 37.0, "group2_left": 37.0, "group2_right": 40.0},
    "liver": {"group1_left": 36.0, "group1_right": 37.5, "group2_left": 38.0, "group2_right": 40.0},
    "spleen": {"group1_left": 35.5, "group1_right": 37.0, "group2_left": 38.0, "group2_right": 39.5},
    "kidney": {"group1_left": 35.0, "group1_right": 36.0, "group2_left": 37.0, "group2_right": 39.0}
  }
}
```

### 响应

```json
{
  "score_result": {"score": 81, "problem_index": 26.0},
  "retest_detail": {
    "usage_days": 35,
    "usage_bonus": 4.0,
    "improvement_bonus": 0.6,
    "protected_score": 77.2
  }
}
```

**关键验证**:
- 30天+ → usage_bonus=4
- 保护规则: max(本次, 上次+2) = max(76.2, 77) = 77.2

### 5.1 Hybrid (Agent) 响应

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 9.85},
  "score_result": {"score": 81, "score_raw": 76.2, "problem_index": 26.0},
  "retest_detail": {
    "usage_days": 35,
    "usage_bonus": 4.0,
    "improvement_bonus": 0.6,
    "protected_score": 77.2,
    "previous_score": 75,
    "previous_problem_index": 28.0
  },
  "side_bias_summary": {"left_low_count": 6, "right_low_count": 0, "result": "head_blood_supply_attention"},
  "cervical_lumbar_result": {"result": "lumbar", "kidney_trend": "stable_left_low", "bladder_trend": "stable_left_low"},

  "// --- LLM生成字段 ---": "",

  "summary": "本次复测显示整体经络状态较上次有所改善，综合健康分81分，处于轻度失衡范围。主要问题集中在膀胱经、肝经的左侧低温及温差偏大，提示腰部、代谢、循环方面需重点关注；同时六条经络均表现为左侧偏低，提示头部供血方向需关注。肾经与膀胱经趋势组合提示腰椎问题。建议继续调理，注重腰部保养、疏肝养血和改善头部供血。",
  "reportSummary": "本次复测显示整体经络状态较上次有所改善，综合健康分81分...",

  "storefront": {
    "focusHeadline": "腰部与代谢需重点关注",
    "clientExplanation": "本次分析基于足部经络热成像数据，反映身体的功能性倾向，不等同于医疗诊断，仅供参考。",
    "talkTrack": [
      "您的检测结果整体不错，比上次有进步，健康分81分，属于轻度失衡的常见状态。",
      "主要发现是膀胱经和肝经的温度差异比较明显，这两个跟腰部和代谢循环有关联，提示需要重点留意。",
      "另外六条经络都是左侧偏低，可能跟头部供血有关，平时可以多注意休息，配合调理来改善。"
    ],
    "retestPrompt": "建议继续坚持调理，35天后再来复测，观察改善情况。"
  },

  "recommendations": [
    "膀胱经调理：多饮水，适度拉伸背部，避免久坐，可尝试温敷腰部。",
    "肝经调理：保持情绪舒畅，多做扩胸运动，可饮用菊花枸杞茶，避免过度饮酒。",
    "整体偏左低：增加有氧运动如快走或瑜伽，促进全身血液循环，改善头部供血。",
    "腰椎保养：注意腰部保暖，避免提重物，可配合艾灸或理疗。"
  ]
}
```

---

## 6. 性别过滤 - 男性 (test_16_gender_male)

### 请求

```json
{
  "measurement_type": "first_test",
  "gender": "male",
  "meridians": {
    "stomach": {"group1_left": 36.5, "group1_right": 38.5, "group2_left": 38.0, "group2_right": 40.0},
    "gallbladder": {"group1_left": 36.0, "group1_right": 38.0, "group2_left": 38.5, "group2_right": 40.0},
    "bladder": {"group1_left": 35.0, "group1_right": 37.0, "group2_left": 37.0, "group2_right": 40.0},
    "liver": {"group1_left": 36.0, "group1_right": 37.5, "group2_left": 38.0, "group2_right": 40.0},
    "spleen": {"group1_left": 35.5, "group1_right": 37.5, "group2_left": 38.0, "group2_right": 39.5},
    "kidney": {"group1_left": 35.0, "group1_right": 36.0, "group2_left": 37.0, "group2_right": 39.0}
  }
}
```

### 响应

```json
{
  "score_result": {"score": 80, "problem_index": 20.5}
}
```

**关键验证** (Agent模式):
- 允许词汇: 前列腺、前列腺炎
- 禁止词汇: 宫寒、子宫、例假

### 6.1 Hybrid (Agent) 响应

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 10.43},
  "score_result": {"score": 80, "score_raw": 80.22, "problem_index": 20.5},
  "side_bias_summary": {"left_low_count": 5, "right_low_count": 0, "result": "head_blood_supply_attention"},
  "cervical_lumbar_result": {"result": "lumbar", "kidney_trend": "stable_left_low", "bladder_trend": "stable_left_low"},
  "gender": "male",

  "// --- LLM生成字段 ---": "",

  "summary": "您的足部经络测量显示整体偏向左侧温度偏低，提示头部供血方向需要关注。胃经是本次的最低点，结合温差较大，提示消化系统可能存在阴虚内热、消化偏快的情况。此外，膀胱经、肝经、脾经、肾经均存在明显温差，反映腰椎、代谢、过滤及肾阴方面需要留意。综合健康分80分，处于轻度失衡状态，建议通过饮食、作息和适当调理来改善。",
  "reportSummary": "您的足部经络测量显示整体偏向左侧温度偏低，提示头部供血方向需要关注...",

  "storefront": {
    "focusHeadline": "胃经与整体偏左需关注",
    "clientExplanation": "该报告基于足部经络温度测量分析，仅供参考，不等同于医疗诊断。建议结合个人感受咨询专业医师。",
    "talkTrack": [
      "您的检测结果显示，胃经是温度最低的经络，且左右温差较大，可能反映消化系统有阴虚内热的倾向。",
      "另外，整体左边经络温度偏低，可能提示头部供血方面需要多加关注。",
      "多个经络如肝、脾、肾经也有明显温差，建议在调理中重点疏肝健脾、滋补肾阴。"
    ],
    "retestPrompt": "建议在调理2-4周后复测，观察经络平衡变化。"
  },

  "recommendations": [
    "饮食上避免辛辣燥热食物，多食滋阴润燥之品，如银耳、百合、黑芝麻。",
    "作息规律，尽量在23点前入睡，减少熬夜，以助肾阴恢复。",
    "适度进行温和运动，如散步、瑜伽，促进血液循环，但避免过度出汗耗阴。",
    "可考虑使用足部温灸或经络调理仪器，重点刺激胃经、肝经、肾经的穴位。"
  ]
}
```

---

## 7. 温差改善 (test_27_diff_change_improved)

### 请求

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {"group1_left": 34.0, "group1_right": 38.0, "group2_left": 39.0, "group2_right": 40.0},
    "gallbladder": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0},
    "bladder": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0},
    "liver": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0},
    "spleen": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0},
    "kidney": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0}
  }
}
```

### 响应

```json
{
  "score_result": {"score": 89, "problem_index": 1.5},
  "meridian_analysis": [
    {
      "meridian": "stomach",
      "group1_diff": 4.0,
      "group2_diff": 1.0,
      "diff_change": "improved",
      "diff_adjustment": -0.5
    }
  ]
}
```

**关键验证**:
- group1_diff=4.0, group2_diff=1.0
- 改善 3.0 > 0.2 → diff_change="improved"
- B指数修正: -0.5

### 7.1 Hybrid (Agent) 响应

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 8.15},
  "score_result": {"score": 89, "score_raw": 89.5, "problem_index": 1.5},
  "meridian_analysis": [
    {
      "meridian": "stomach",
      "group1_diff": 4.0,
      "group2_diff": 1.0,
      "diff_change": "improved",
      "diff_adjustment": -0.5
    }
  ],

  "// --- LLM生成字段 ---": "",

  "summary": "您的整体健康得分为89分，属于轻度失衡状态，整体状态良好。本次检测发现胃经存在明显的左右温差改善趋势，从第一组的4.0°C改善到第二组的1.0°C，提示消化系统功能正在自我调整。其他五条经络表现平衡，说明整体经络运行较为协调。建议您从饮食和生活习惯入手，维持消化功能的健康。",
  "reportSummary": "您的整体健康得分为89分，属于轻度失衡状态，整体状态良好...",

  "storefront": {
    "focusHeadline": "胃经改善明显",
    "clientExplanation": "本次检测结果基于足部经络温度分析，不等同于医疗诊断，仅供参考。您的健康得分较高，胃经温差有明显改善趋势。",
    "talkTrack": [
      "您的整体经络状态不错，大部分经络都很平衡，健康评分有89分呢。",
      "而且我们发现胃经的温差在检测过程中有明显改善，从4度降到了1度，这是一个很好的信号。",
      "建议您继续保持良好的饮食习惯，少食生冷刺激的食物，可以适当进行腹部按摩，帮助巩固胃经的改善。"
    ],
    "retestPrompt": "建议2-4周后复测，观察胃经的长期稳定性，同时保持健康的生活习惯。"
  },

  "recommendations": [
    "继续保持规律饮食，避免暴饮暴食，多吃温热易消化的食物如小米粥、山药。",
    "可适当进行腹部按摩或艾灸足三里、中脘等穴位，帮助巩固胃经改善。",
    "保持良好作息，避免过度思虑，饮食后适当散步促进消化。"
  ]
}
```

---

## 8. PRD首测示例 (case_01_first_test)

### 8.1 请求

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {"group1_left": 39.5, "group1_right": 40.5, "group2_left": 42.4, "group2_right": 42.5},
    "gallbladder": {"group1_left": 36.7, "group1_right": 36.7, "group2_left": 42.1, "group2_right": 42.1},
    "bladder": {"group1_left": 36.2, "group1_right": 36.5, "group2_left": 37.9, "group2_right": 41.1},
    "liver": {"group1_left": 36.7, "group1_right": 36.4, "group2_left": 39.6, "group2_right": 39.9},
    "spleen": {"group1_left": 36.6, "group1_right": 36.5, "group2_left": 39.1, "group2_right": 40.6},
    "kidney": {"group1_left": 36.6, "group1_right": 36.7, "group2_left": 40.5, "group2_right": 41.6}
  }
}
```

### 8.2 Hybrid (Agent) 响应

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 8.12},
  "score_result": {
    "score": 77,
    "score_raw": 77.08,
    "problem_index": 24.9,
    "problem_index_detail": {
      "low_temperature_index": 5.0,
      "temperature_difference_index": 8.5,
      "side_bias_index": 5.0,
      "trend_index": 3.9,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {"meridian": "bladder", "side": "left", "value": 37.9, "rank": 1, "must_report": true},
      {"meridian": "spleen", "side": "left", "value": 39.1, "rank": 2, "must_report": true}
    ]
  },
  "side_bias_summary": {
    "left_low_count": 5,
    "right_low_count": 0,
    "balanced_count": 1,
    "result": "head_blood_supply_attention"
  },
  "cervical_lumbar_result": {
    "result": "lumbar",
    "kidney_trend": "stable_left_low",
    "bladder_trend": "stable_left_low"
  },
  
  "// --- LLM生成字段 ---": "",
  
  "summary": "本次检测显示综合健康分为77分，属于中度失衡状态。主要问题集中在膀胱经、脾经和肾经，其中膀胱经和脾经温差显著，且整体经络偏左明显，提示头部供血和腰椎方向需重点关注。建议持续调理，改善亚健康状态。",
  "reportSummary": "本次检测显示综合健康分为77分，属于中度失衡状态。主要问题集中在膀胱经、脾经和肾经...",
  
  "storefront": {
    "focusHeadline": "膀胱经与脾经需重点关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。您的综合健康分77分，提示身体存在一些需要关注的失衡点。",
    "talkTrack": [
      "您的膀胱经和脾经温度差异较大，可能与肩颈腰部和消化代谢有关。",
      "同时整体经络偏左侧较低，提示头部供血方面需要留意。",
      "结合肾经与膀胱经的趋势，腰椎区域也需要关注，建议配合调理改善。"
    ],
    "retestPrompt": "建议经过一段时间的调理后复测，观察改善情况。"
  },
  
  "recommendations": [
    "注意腰部保暖，避免久坐，可适当进行腰椎伸展运动。",
    "饮食上减少生冷油腻，增加薏米、山药等健脾祛湿食材。",
    "保持规律作息，避免熬夜，多饮水，可食用枸杞、黑芝麻等补肾滋阴食物。"
  ]
}
```

**关键验证**:
- 分数 77 → 中度失衡 (70-79)
- 问题指数 24.9 = 100-77.08+2
- 5条左低 (胃经、膀胱经、肝经、脾经、肾经) → 头部供血需关注

---

## 9. 其他测试用例 Hybrid 输出汇总

### 9.1 快速参考表

| 编号 | 测试用例 | 分数 | Hybrid 核心摘要 |
|------|----------|------|-----------------|
| 2 | test_02_mild_imbalance | 89 | 脾经肝经轻微不平衡，建议饮食调理 |
| 4 | test_04_significant_imbalance | 75 | 经络全面交叉失衡，颈椎腰椎同时存在 |
| 5 | test_05_trend_stable_left_low | 74 | 肾+膀胱左低=腰椎，头部供血需关注 |
| 6 | test_06_trend_stable_right_low | 74 | 肾+膀胱右低=腰椎，心脏方向需关注 |
| 8 | test_08_trend_potential_symptom | 89 | 胃经潜在症状，第二组温差增大 |
| 9 | test_09_trend_fast_response | 89 | 胃经改善明显，调理反应快 |
| 10 | test_10_diff_levels | 75 | 4种温差等级，肾经脾经严重问题 |
| 11 | test_11_side_bias_4 | 84 | 偏侧4条，C=3.5，头部供血需关注 |
| 12 | test_12_side_bias_5 | 82 | 右侧5条偏低，心脏方向需关注 |
| 13 | test_13_side_bias_6 | 80 | 左侧6条偏低，头部供血+腰椎 |
| 14 | test_14_cervical_opposite | 86 | 肾左低+膀胱右低=颈椎问题 |
| 15 | test_15_cervical_lumbar_cross | 86 | 膀胱交叉=颈椎+腰椎 |
| 17 | test_17_gender_female | 80 | 女性文案，允许多囊、宫寒等词汇 |
| 18 | test_18_gender_unknown | 80 | 中性文案，性别中性表述 |
| 19 | test_19_retest_0_2_days | 77 | 复测0-2天，usage_bonus=0 |
| 20 | test_20_retest_3_6_days | 78 | 复测3-6天，usage_bonus=1 |
| 21 | test_21_retest_7_13_days | 79 | 复测7-13天，usage_bonus=2 |
| 22 | test_22_retest_14_29_low | 80 | 复测14-29天，低分，usage_bonus=3 |
| 23 | test_23_retest_14_29_high | 95 | 复测14-29天，高分，usage_bonus=3 |
| 25 | test_25_retest_improvement | 95 | 数据改善，improvement_bonus=3 |
| 26 | test_26_low_temp_index_max | 88 | 低温指数最大档，A=6 |
| 28 | test_28_diff_change_worsened | 88 | 温差恶化，diff恶化+0.5 |
| 29 | test_29_realistic_mild | 89 | 真实轻度数据验证 |
| 30 | test_30_realistic_moderate | 76 | 真实中度数据验证 |
| 31 | test_31_bladder_lowest | 83 | 膀胱经最低点验证 |
| 32 | test_32_kidney_cross | 84 | 肾经交叉=颈椎+腰椎 |

### 9.2 代表性 Hybrid 输出示例

#### test_04_significant_imbalance (分数 75)

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 10.46},
  "score_result": {"score": 75, "score_raw": 74.6, "problem_index": 28.0},
  "summary": "本次检测显示您的经络存在多处左右交叉失衡，以膀胱经、胃经、肝经、脾经、肾经、胆经的温度差较为突出，提示消化、代谢、泌尿生殖及脊柱相关系统功能需要关注。整体偏向右侧低温，可能影响循环和心脏供血。颈椎和腰椎问题同时存在。",
  "storefront": {
    "focusHeadline": "经络全面失衡，需重点调理",
    "clientExplanation": "这份报告是基于足部经络温度测量的分析，不等同于医疗诊断。",
    "talkTrack": [
      "您的经络检测结果显示，六条经络都有不同程度的左右温度差，属于比较全面的失衡状态。",
      "其中膀胱经、胃经、肾经的问题相对更突出，可能影响到您的消化、腰背、睡眠和精力。"
    ],
    "retestPrompt": "建议您先按调理方案尝试2-4周，然后进行复测。"
  },
  "recommendations": [
    "饮食方面：规律三餐，避免暴饮暴食，少吃生冷油腻；",
    "作息方面：尽量在23点前入睡，避免熬夜；",
    "运动方面：每天适度有氧运动如快走30分钟；",
    "经络调理：可使用经络仪重点调理膀胱经、胃经和肾经。"
  ]
}
```

#### test_12_side_bias_5 (分数 82)

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 8.72},
  "score_result": {"score": 82, "score_raw": 81.8, "problem_index": 18.0},
  "side_bias_summary": {"left_low_count": 0, "right_low_count": 5, "result": "heart_attention"},
  "summary": "您的整体健康评分为82分，处于轻度失衡状态。数据显示身体右侧多条经络温度偏低，尤其胃经、胆经、膀胱经、肝经、脾经的右侧温度明显低于左侧，提示消化系统、代谢功能及循环系统需要关注。",
  "storefront": {
    "focusHeadline": "右侧经络偏弱需关注",
    "clientExplanation": "本次检测结果反映了您身体当前的能量状态，不等同于医疗诊断。",
    "talkTrack": [
      "从数据看，您身体右侧的经络温度普遍偏低，尤其是胃经和脾经，说明消化吸收和代谢方面可能需要多加关注。",
      "这种情况可能和日常饮食习惯、压力或循环有关，但不用太担心，我们有针对性的调理方案可以帮助改善。"
    ],
    "retestPrompt": "建议在坚持调理2-4周后进行复测，以评估调理效果。"
  },
  "recommendations": [
    "饮食上注意三餐规律，减少油腻和甜食摄入，多吃易消化的食物。",
    "保持适度运动，如散步或瑜伽，促进全身血液循环。",
    "建议定期使用经络调理设备，重点刺激右侧胃经、脾经穴位。"
  ]
}
```

#### test_17_gender_female (分数 80)

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 9.24},
  "score_result": {"score": 80, "score_raw": 80.22, "problem_index": 20.5},
  "gender": "female",
  "summary": "您的整体健康评分为80分，处于轻度失衡状态。本次检测发现，胃经问题最为突出，同时脾、肝、肾、膀胱等多条经络存在偏侧温差，提示身体代谢、消化、血液循环和排毒功能需要关注。此外，整体左侧温度偏低，可能影响头部供血。",
  "storefront": {
    "focusHeadline": "胃经与多经络失衡需关注",
    "clientExplanation": "本报告基于足部经络温度测量，通过数据分析提供健康参考，不等同于医疗诊断。",
    "talkTrack": [
      "从测量结果看，您目前胃经问题比较突出，温差较大，可能跟消化功能有关。",
      "另外，多条经络左侧温度偏低，提示身体代谢、血液循环和排毒方面需要加强。"
    ],
    "retestPrompt": "建议坚持调理1-2周后复测，观察经络平衡度的变化。"
  },
  "recommendations": [
    "饮食上减少生冷油腻，增加薏米、山药等健脾祛湿食材。",
    "注意子宫和卵巢保暖，避免久坐，可配合艾灸。",
    "例假期间避免剧烈运动和寒凉食物。"
  ]
}
```

**性别过滤验证**:
- 女性文案允许使用: 宫寒、子宫、例假、月经、多囊、卵巢
- 不会出现男性专属词汇: 前列腺、前列腺炎、肾阳

#### test_23_retest_14_29_high (分数 95)

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat", "llmLatency": 8.92},
  "score_result": {"score": 95, "score_raw": 92.0, "problem_index": 5.0},
  "retest_detail": {
    "usage_days": 21,
    "usage_bonus": 3.0,
    "improvement_bonus": 0,
    "previous_score": 90,
    "current_problem_index": 5.0
  },
  "summary": "本次复测结果显示，您的综合健康评分达到95分，较上次显著提升，整体经络状态趋于平衡。所有经络在两次测量中均保持对称，仅在胃经上观察到温度升高表现，提示消化系统可能成为当前需要关注的焦点。",
  "storefront": {
    "focusHeadline": "胃经需关注，整体平衡",
    "clientExplanation": "本次复测结果显示您的经络整体平衡，健康评分较高，仅胃经温度有所升高。",
    "talkTrack": [
      "您的复测结果非常不错，整体经络都很平衡，健康评分从上次的90分提升到了95分。",
      "我们注意到在胃经区域温度有所上升，这可能与近期的饮食习惯或消化负担有关。"
    ],
    "retestPrompt": "建议您继续保持当前调理方案，并在1-2周后复测。"
  },
  "recommendations": [
    "继续保持规律饮食，避免暴饮暴食。",
    "适当控制辛辣刺激食物摄入，保护胃黏膜。",
    "坚持适度运动，维持当前良好的身体状态。"
  ]
}
```

---

## 附录

### A. Rule vs Hybrid 模式对比示例

以 `case_01_first_test.json` (分数77) 为例：

#### Rule 模式输出（模板化）

```json
{
  "engine": {"mode": "rule-based-v3", "version": "3.0"},
  "score": 77,
  "summary": "本次检测显示您的综合健康分77分，属于中度失衡状态。主要问题集中在膀胱经、脾经，提示相关脏腑功能需要关注。建议系统调理，改善亚健康状态。",
  "storefront": {
    "focusHeadline": "膀胱经、脾经需重点关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。",
    "talkTrack": [
      "您的检测结果显示，膀胱经、脾经问题比较突出，这可能影响相关脏腑功能。",
      "整体健康分77分，属于中度失衡，需要通过系统调理来改善。"
    ],
    "retestPrompt": "建议调理2-4周后复测，观察改善情况。"
  },
  "recommendations": [
    "【膀胱经】注意腰部保暖，避免久坐，适当进行腰背拉伸。",
    "【脾经】少吃生冷油腻食物，多吃健脾祛湿食材如薏米、山药、红豆。",
    "【头部供血需关注】注意头部保暖，避免冷风直吹。",
    "【腰椎问题】注意腰部保暖，避免久坐久站。",
    "保持规律作息，避免熬夜，保证充足睡眠。",
    "适度运动，如散步、太极、瑜伽等，促进气血流通。"
  ]
}
```

#### Hybrid 模式输出（LLM生成）

```json
{
  "engine": {"mode": "hybrid", "version": "3.0", "llmModel": "deepseek-chat"},
  "score": 77,
  "summary": "本次检测显示综合健康分为77分，属于中度失衡状态。主要问题集中在膀胱经、脾经和肾经，其中膀胱经和脾经温差显著，且整体经络偏左明显，提示头部供血和腰椎方向需重点关注。",
  "storefront": {
    "focusHeadline": "膀胱经与脾经需重点关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。",
    "talkTrack": [
      "您的膀胱经和脾经温度差异较大，可能与肩颈腰部和消化代谢有关。",
      "同时整体经络偏左侧较低，提示头部供血方面需要留意。",
      "结合肾经与膀胱经的趋势，腰椎区域也需要关注，建议配合调理改善。"
    ],
    "retestPrompt": "建议经过一段时间的调理后复测，观察改善情况。"
  },
  "recommendations": [
    "注意腰部保暖，避免久坐，可适当进行腰椎伸展运动。",
    "饮食上减少生冷油腻，增加薏米、山药等健脾祛湿食材。",
    "保持规律作息，避免熬夜，多饮水，可食用枸杞、黑芝麻等补肾滋阴食物。"
  ]
}
```

**对比总结**:
- Rule: 模板固定，快速生成，结构统一
- Hybrid: 文案自然，更具个性化，但需要LLM调用

---

### A. 批量测试命令

```bash
# 运行所有测试
cd tests && python3 run_tests_v3.py

# 记录 Rule-only 输出
cd tests && python3 record_actual_outputs.py

# 记录 Agent 输出（需要 DEEPSEEK_API_KEY）
cd tests && python3 record_agent_outputs.py

# 运行特定测试用例
python3 scripts/infer_v2.py fixtures/v3/test_01_excellent_score.json --pretty

# HTTP API 测试
curl -X POST http://localhost:18790/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  -d @fixtures/v3/test_01_excellent_score.json
```

### B. 模式切换

| 环境变量 | 说明 |
|----------|------|
| `TCM_INFER_MODE=rule` | 纯规则引擎，无LLM调用 |
| `TCM_INFER_MODE=hybrid` (默认) | 规则+LLM，生成自然语言文案 |
| `TCM_INFER_MODE=auto` | 有API Key时用hybrid，否则fallback到rule |

### C. Agent 结果文件位置

所有 34 个测试用例的完整 Agent 输出位于:
```
docs/v3/testing/agent-results/
├── case_01_first_test-agent.json
├── case_02_retest-agent.json
├── test_01_excellent_score-agent.json
├── test_02_mild_imbalance-agent.json
├── test_03_moderate_imbalance-agent.json
├── test_04_significant_imbalance-agent.json
├── test_05_trend_stable_left_low-agent.json
├── test_06_trend_stable_right_low-agent.json
├── test_07_trend_cross-agent.json
├── test_08_trend_potential_symptom-agent.json
├── test_09_trend_fast_response-agent.json
├── test_10_diff_levels-agent.json
├── test_11_side_bias_4-agent.json
├── test_12_side_bias_5-agent.json
├── test_13_side_bias_6-agent.json
├── test_14_cervical_opposite-agent.json
├── test_15_cervical_lumbar_cross-agent.json
├── test_16_gender_male-agent.json
├── test_17_gender_female-agent.json
├── test_18_gender_unknown-agent.json
├── test_19_retest_0_2_days-agent.json
├── test_20_retest_3_6_days-agent.json
├── test_21_retest_7_13_days-agent.json
├── test_22_retest_14_29_days_low-agent.json
├── test_23_retest_14_29_days_high-agent.json
├── test_24_retest_30_plus_days-agent.json
├── test_25_retest_improvement-agent.json
├── test_26_low_temp_index_max-agent.json
├── test_27_diff_change_improved-agent.json
├── test_28_diff_change_worsened-agent.json
├── test_29_realistic_mild-agent.json
├── test_30_realistic_moderate-agent.json
├── test_31_bladder_lowest-agent.json
└── test_32_kidney_cross-agent.json
```

---

*文档版本: v1.2*  
*最后更新: 2026-05-05*
