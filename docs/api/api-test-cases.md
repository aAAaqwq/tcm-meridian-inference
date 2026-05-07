# TCM v3 API 测试用例文档（真实数据记录）

> **说明**: 本文档基于 v3 规则引擎实际运行输出记录，包含完整输入和关键输出字段。
> **引擎版本**: rule-based-v3 v3.0
> **测试用例总数**: 38 个（首测26个 + 复测12个）
> **生成时间**: 2026-05-07

---

## 测试用例索引

### 首测用例

| 编号 | 文件名 | 场景 | 分数 | 问题指数 |
|------|--------|------|------|----------|
| 1 | case_01_first_test | PRD标准示例 | 77 | 24.9 |
| 2 | test_01_excellent_score | 健康优秀 | 89 | 0.0 |
| 3 | test_02_mild_imbalance | 轻度失衡 | 89 | 1.5 |
| 4 | test_03_moderate_imbalance | 中度失衡 | 76 | 26.0 |
| 5 | test_04_significant_imbalance | 明显失衡 | 75 | 28.0 |
| 6 | test_05_trend_stable_left_low | 趋势-左低 | 74 | 28.5 |
| 7 | test_06_trend_stable_right_low | 趋势-右低 | 74 | 28.5 |
| 8 | test_07_trend_cross | 趋势-交叉 | 77 | 25.0 |
| 9 | test_08_trend_potential_symptom | 趋势-潜在症状 | 89 | 3.3 |
| 10 | test_09_trend_fast_response | 趋势-快速恢复 | 89 | 0.3 |
| 11 | test_10_diff_levels | 温差等级 | 75 | 28.0 |
| 12 | test_11_side_bias_4 | 偏侧4条 | 84 | 14.5 |
| 13 | test_12_side_bias_5 | 偏侧5条 | 82 | 18.0 |
| 14 | test_13_side_bias_6 | 偏侧6条 | 80 | 21.5 |
| 15 | test_14_cervical_opposite | 颈椎-相反低 | 86 | 9.5 |
| 16 | test_15_cervical_lumbar_cross | 交叉=颈+腰 | 86 | 10.2 |
| 17 | test_16_gender_male | 性别-男性 | 80 | 20.5 |
| 18 | test_17_gender_female | 性别-女性 | 80 | 20.5 |
| 19 | test_18_gender_unknown | 性别-未知 | 80 | 20.5 |
| 20 | test_26_low_temp_index_max | 低温指数最大 | 88 | 6.0 |
| 21 | test_27_diff_change_improved | 温差改善 | 89 | 1.5 |
| 22 | test_28_diff_change_worsened | 温差恶化 | 88 | 5.5 |
| 23 | test_29_realistic_mild | 真实-轻度 | 89 | 1.5 |
| 24 | test_30_realistic_moderate | 真实-中度 | 76 | 26.5 |
| 25 | test_31_bladder_lowest | 膀胱最低 | 83 | 14.9 |
| 26 | test_32_kidney_cross | 肾交叉 | 84 | 13.1 |

### 复测用例

| 编号 | 文件名 | 场景 | 分数 | 问题指数 |
|------|--------|------|------|----------|
| 1 | case_02_retest | PRD复测示例 | 89 | 14.7 |
| 2 | test_19_retest_0_2_days | 0-2天 | 77 | 26.0 |
| 3 | test_20_retest_3_6_days | 3-6天 | 78 | 26.0 |
| 4 | test_21_retest_7_13_days | 7-13天 | 79 | 26.0 |
| 5 | test_22_retest_14_29_days_low | 14-29天(<88) | 80 | 26.0 |
| 6 | test_23_retest_14_29_days_high | 14-29天(≥88)→95分 | 95 | 0.0 |
| 7 | test_24_retest_30_plus_days | 30天+ | 81 | 26.0 |
| 8 | test_25_retest_improvement | 数据改善→95分 | 95 | 0.0 |
| 9 | test_33_retest_92_score | 92分-中等高分 | 93 | 1.8 |
| 10 | test_34_retest_91_score | 91分-高分起步 | 94 | 1.8 |
| 11 | test_35_retest_93_score | 93分-接近封顶 | 95 | 1.8 |
| 12 | test_36_retest_94_score | 94分-保护机制 | 94 | 1.8 |

---

## 1. case_01_first_test (PRD标准示例)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 39.5,
      "group1_right": 40.5,
      "group2_left": 42.4,
      "group2_right": 42.5
    },
    "gallbladder": {
      "group1_left": 36.7,
      "group1_right": 36.7,
      "group2_left": 42.1,
      "group2_right": 42.1
    },
    "bladder": {
      "group1_left": 36.2,
      "group1_right": 36.5,
      "group2_left": 37.9,
      "group2_right": 41.1
    },
    "liver": {
      "group1_left": 36.7,
      "group1_right": 36.4,
      "group2_left": 39.6,
      "group2_right": 39.9
    },
    "spleen": {
      "group1_left": 36.6,
      "group1_right": 36.5,
      "group2_left": 39.1,
      "group2_right": 40.6
    },
    "kidney": {
      "group1_left": 36.6,
      "group1_right": 36.7,
      "group2_left": 40.5,
      "group2_right": 41.6
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 77,
    "score_raw": 77.08,
    "problem_index": 24.9,
    "problem_index_detail": {
      "low_temperature_index": 5.0,
      "temperature_difference_index": 8.5,
      "side_bias_index": 5.0,
      "trend_index": 3.9000000000000004,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "bladder",
        "side": "left",
        "value": 37.9,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "spleen",
        "side": "left",
        "value": 39.1,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "spleen",
      "meridian_name": "脾经",
      "side": "left",
      "title": "脾经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 5,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "膀胱经、脾经需重点关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的检测结果显示，膀胱经、脾经问题比较突出，这可能影响相关脏腑功能。",
      "整体健康分77分，属于中度失衡，需要通过系统调理来改善。"
    ],
    "retestPrompt": "建议调理2-4周后复测，观察改善情况。"
  }
}
```

### 验证点

- **预期分数**: 77, **实际分数**: 77
- **预期问题指数**: 24.9, **实际问题指数**: 24.9

---

## 2. case_02_retest (PRD复测示例)

**类型**: 复测

### 输入

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 77,
  "previous_problem_index": 24.9,
  "usage_days_between_tests": 14,
  "meridians": {
    "stomach": {
      "group1_left": 40.0,
      "group1_right": 40.5,
      "group2_left": 42.5,
      "group2_right": 42.6
    },
    "gallbladder": {
      "group1_left": 37.0,
      "group1_right": 37.0,
      "group2_left": 42.2,
      "group2_right": 42.2
    },
    "bladder": {
      "group1_left": 37.0,
      "group1_right": 37.2,
      "group2_left": 40.0,
      "group2_right": 41.0
    },
    "liver": {
      "group1_left": 37.0,
      "group1_right": 36.8,
      "group2_left": 40.0,
      "group2_right": 40.2
    },
    "spleen": {
      "group1_left": 37.0,
      "group1_right": 36.8,
      "group2_left": 40.0,
      "group2_right": 40.8
    },
    "kidney": {
      "group1_left": 37.0,
      "group1_right": 37.0,
      "group2_left": 41.0,
      "group2_right": 41.5
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 89,
    "score_raw": 83.42,
    "problem_index": 14.7,
    "problem_index_detail": {
      "low_temperature_index": 1.0,
      "temperature_difference_index": 5.0,
      "side_bias_index": 5.0,
      "trend_index": 3.7,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "bladder",
        "side": "left",
        "value": 40.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "liver",
        "side": "right",
        "value": 40.2,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 5,
    "right_low_count": 0,
    "balanced_count": 1,
    "result": "head_blood_supply_attention"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "potential_symptom",
    "bladder_trend": "stable_left_low"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "liver",
      "meridian_name": "肝经",
      "side": "right",
      "title": "肝经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 5,
      "reason_codes": [
        "left_bias_count_high"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "调理见效，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "太好了！您的健康分从77分提升到了89分，调理效果非常明显。",
      "这说明我们的调理方向是对的，您的配合也很好，建议继续坚持。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  },
  "retest_detail": {
    "usage_days": 14,
    "usage_bonus": 3.0,
    "delta_I": 10.2,
    "improvement_bonus": 3.0,
    "retest_score_base": 89.415,
    "protected_score": 89.415,
    "previous_score": 77,
    "previous_problem_index": 24.9,
    "current_problem_index": 14.7
  }
}
```

### 验证点

- **预期分数**: 89, **实际分数**: 89
- **预期问题指数**: 14.7, **实际问题指数**: 14.7

---

## 3. test_01_excellent_score (健康优秀)

**类型**: 首测

### 输入

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
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
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
      {
        "meridian": "stomach",
        "side": "left",
        "value": 40.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 0,
    "balanced_count": 6,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_balanced"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体状态良好，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的六条经络温度平衡，气血运行顺畅，这是一个非常好的状态。",
      "建议继续保持当前的作息和饮食习惯，定期复测以维护健康。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  }
}
```

### 验证点

- **预期分数**: 89, **实际分数**: 89
- **预期问题指数**: 0.0, **实际问题指数**: 0.0

---

## 4. test_02_mild_imbalance (轻度失衡)

**类型**: 首测

### 输入

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
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 37.9,
      "group1_right": 38.0,
      "group2_left": 39.8,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 37.8,
      "group1_right": 38.0,
      "group2_left": 39.7,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 89,
    "score_raw": 89.4,
    "problem_index": 1.5,
    "problem_index_detail": {
      "low_temperature_index": 0.0,
      "temperature_difference_index": 0.5,
      "side_bias_index": 0.0,
      "trend_index": 1.0,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "spleen",
        "side": "left",
        "value": 39.7,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "liver",
        "side": "left",
        "value": 39.8,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 2,
    "right_low_count": 0,
    "balanced_count": 4,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_balanced"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "spleen",
      "meridian_name": "脾经",
      "side": "left",
      "title": "脾经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "liver",
      "meridian_name": "肝经",
      "side": "left",
      "title": "肝经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体状态良好，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的六条经络温度平衡，气血运行顺畅，这是一个非常好的状态。",
      "建议继续保持当前的作息和饮食习惯，定期复测以维护健康。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  }
}
```

### 验证点

- **预期分数**: 89, **实际分数**: 89
- **预期问题指数**: 1.5, **实际问题指数**: 1.5

---

## 5. test_03_moderate_imbalance (中度失衡)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 36.5,
      "group1_right": 38.0,
      "group2_left": 39.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.5,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 35.0,
      "group1_right": 37.0,
      "group2_left": 37.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 37.5,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 35.5,
      "group1_right": 37.0,
      "group2_left": 38.0,
      "group2_right": 39.5
    },
    "kidney": {
      "group1_left": 35.0,
      "group1_right": 36.0,
      "group2_left": 37.0,
      "group2_right": 39.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
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
      {
        "meridian": "bladder",
        "side": "left",
        "value": 37.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "liver",
        "side": "left",
        "value": 38.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "liver",
      "meridian_name": "肝经",
      "side": "left",
      "title": "肝经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 6,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "膀胱经、肝经需重点关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的检测结果显示，膀胱经、肝经问题比较突出，这可能影响相关脏腑功能。",
      "整体健康分76分，属于中度失衡，需要通过系统调理来改善。"
    ],
    "retestPrompt": "建议调理2-4周后复测，观察改善情况。"
  }
}
```

### 验证点

- **预期分数**: 76, **实际分数**: 76
- **预期问题指数**: 26.0, **实际问题指数**: 26.0

---

## 6. test_04_significant_imbalance (明显失衡)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 28.0,
      "group1_right": 38.0,
      "group2_left": 42.0,
      "group2_right": 32.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 28.0,
      "group2_left": 32.0,
      "group2_right": 42.0
    },
    "bladder": {
      "group1_left": 26.0,
      "group1_right": 34.0,
      "group2_left": 44.0,
      "group2_right": 30.0
    },
    "liver": {
      "group1_left": 28.0,
      "group1_right": 36.0,
      "group2_left": 42.0,
      "group2_right": 32.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 28.0,
      "group2_left": 32.0,
      "group2_right": 42.0
    },
    "kidney": {
      "group1_left": 26.0,
      "group1_right": 35.0,
      "group2_left": 43.0,
      "group2_right": 30.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 75,
    "score_raw": 74.6,
    "problem_index": 28.0,
    "problem_index_detail": {
      "low_temperature_index": 6.0,
      "temperature_difference_index": 12.0,
      "side_bias_index": 3.5,
      "trend_index": 4.0,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "bladder",
        "side": "right",
        "value": 30.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 32.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 2,
    "right_low_count": 4,
    "balanced_count": 0,
    "result": "heart_attention"
  },
  "cervical_lumbar_result": {
    "result": "cervical_and_lumbar",
    "kidney_trend": "cross",
    "bladder_trend": "cross"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "right",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "心脏方向需关注",
      "right_low_count": 4,
      "reason_codes": [
        "right_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "颈椎和腰椎问题同时存在",
      "reason_codes": [
        "cervical_and_lumbar_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "膀胱经、胃经需重点关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的检测结果显示，膀胱经、胃经问题比较突出，这可能影响相关脏腑功能。",
      "整体健康分75分，属于中度失衡，需要通过系统调理来改善。"
    ],
    "retestPrompt": "建议调理2-4周后复测，观察改善情况。"
  }
}
```

### 验证点

- **预期分数**: 75, **实际分数**: 75
- **预期问题指数**: 28.0, **实际问题指数**: 28.0

---

## 7. test_05_trend_stable_left_low (趋势-左低)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 36.5,
      "group1_right": 38.0,
      "group2_left": 38.5,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 35.0,
      "group1_right": 37.0,
      "group2_left": 37.0,
      "group2_right": 39.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 37.5,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 35.5,
      "group1_right": 37.0,
      "group2_left": 38.0,
      "group2_right": 39.5
    },
    "kidney": {
      "group1_left": 34.0,
      "group1_right": 36.0,
      "group2_left": 36.0,
      "group2_right": 39.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 74,
    "score_raw": 74.2,
    "problem_index": 28.5,
    "problem_index_detail": {
      "low_temperature_index": 5.0,
      "temperature_difference_index": 12.0,
      "side_bias_index": 6.0,
      "trend_index": 3.0,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "kidney",
        "side": "left",
        "value": 36.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "bladder",
        "side": "left",
        "value": 37.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "kidney",
      "meridian_name": "肾经",
      "side": "left",
      "title": "肾经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 6,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "肾经、膀胱经需重点关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的检测结果显示，肾经、膀胱经问题比较突出，这可能影响相关脏腑功能。",
      "整体健康分74分，属于中度失衡，需要通过系统调理来改善。"
    ],
    "retestPrompt": "建议调理2-4周后复测，观察改善情况。"
  }
}
```

### 验证点

- **预期分数**: 74, **实际分数**: 74
- **预期问题指数**: 28.5, **实际问题指数**: 28.5

---

## 8. test_06_trend_stable_right_low (趋势-右低)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 38.0,
      "group1_right": 36.0,
      "group2_left": 40.0,
      "group2_right": 38.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 36.5,
      "group2_left": 40.0,
      "group2_right": 38.5
    },
    "bladder": {
      "group1_left": 37.0,
      "group1_right": 35.0,
      "group2_left": 39.0,
      "group2_right": 37.0
    },
    "liver": {
      "group1_left": 37.5,
      "group1_right": 36.0,
      "group2_left": 40.0,
      "group2_right": 38.0
    },
    "spleen": {
      "group1_left": 37.0,
      "group1_right": 35.5,
      "group2_left": 39.5,
      "group2_right": 38.0
    },
    "kidney": {
      "group1_left": 36.0,
      "group1_right": 34.0,
      "group2_left": 39.0,
      "group2_right": 36.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 74,
    "score_raw": 74.2,
    "problem_index": 28.5,
    "problem_index_detail": {
      "low_temperature_index": 5.0,
      "temperature_difference_index": 12.0,
      "side_bias_index": 6.0,
      "trend_index": 3.0,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "kidney",
        "side": "right",
        "value": 36.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "bladder",
        "side": "right",
        "value": 37.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 6,
    "balanced_count": 0,
    "result": "heart_attention"
  },
  "cervical_lumbar_result": {
    "result": "lumbar",
    "kidney_trend": "stable_right_low",
    "bladder_trend": "stable_right_low"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "kidney",
      "meridian_name": "肾经",
      "side": "right",
      "title": "肾经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "right",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "心脏方向需关注",
      "right_low_count": 6,
      "reason_codes": [
        "right_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "肾经、膀胱经需重点关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的检测结果显示，肾经、膀胱经问题比较突出，这可能影响相关脏腑功能。",
      "整体健康分74分，属于中度失衡，需要通过系统调理来改善。"
    ],
    "retestPrompt": "建议调理2-4周后复测，观察改善情况。"
  }
}
```

### 验证点

- **预期分数**: 74, **实际分数**: 74
- **预期问题指数**: 28.5, **实际问题指数**: 28.5

---

## 9. test_07_trend_cross (趋势-交叉)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 38.0
    },
    "gallbladder": {
      "group1_left": 36.5,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 38.5
    },
    "bladder": {
      "group1_left": 35.0,
      "group1_right": 37.0,
      "group2_left": 39.0,
      "group2_right": 37.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 37.5,
      "group2_left": 40.0,
      "group2_right": 38.0
    },
    "spleen": {
      "group1_left": 35.5,
      "group1_right": 37.0,
      "group2_left": 39.5,
      "group2_right": 38.0
    },
    "kidney": {
      "group1_left": 34.0,
      "group1_right": 36.0,
      "group2_left": 39.0,
      "group2_right": 37.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
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
  "lowest_points": {
    "selected": [
      {
        "meridian": "bladder",
        "side": "right",
        "value": 37.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 38.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 6,
    "balanced_count": 0,
    "result": "heart_attention"
  },
  "cervical_lumbar_result": {
    "result": "cervical_and_lumbar",
    "kidney_trend": "cross",
    "bladder_trend": "cross"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "right",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "心脏方向需关注",
      "right_low_count": 6,
      "reason_codes": [
        "right_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "颈椎和腰椎问题同时存在",
      "reason_codes": [
        "cervical_and_lumbar_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "膀胱经、胃经需重点关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的检测结果显示，膀胱经、胃经问题比较突出，这可能影响相关脏腑功能。",
      "整体健康分77分，属于中度失衡，需要通过系统调理来改善。"
    ],
    "retestPrompt": "建议调理2-4周后复测，观察改善情况。"
  }
}
```

### 验证点

- **预期分数**: 77, **实际分数**: 77
- **预期问题指数**: 25.0, **实际问题指数**: 25.0

---

## 10. test_08_trend_potential_symptom (趋势-潜在症状)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 89,
    "score_raw": 88.68,
    "problem_index": 3.3,
    "problem_index_detail": {
      "low_temperature_index": 1.0,
      "temperature_difference_index": 2.0,
      "side_bias_index": 0.0,
      "trend_index": 0.3,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 38.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 1,
    "right_low_count": 0,
    "balanced_count": 5,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_balanced"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体状态良好，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的六条经络温度平衡，气血运行顺畅，这是一个非常好的状态。",
      "建议继续保持当前的作息和饮食习惯，定期复测以维护健康。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  }
}
```

### 验证点

- **预期分数**: 89, **实际分数**: 89
- **预期问题指数**: 3.3, **实际问题指数**: 3.3

---

## 11. test_09_trend_fast_response (趋势-快速恢复)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 89,
    "score_raw": 89.88,
    "problem_index": 0.3,
    "problem_index_detail": {
      "low_temperature_index": 0.0,
      "temperature_difference_index": 0.0,
      "side_bias_index": 0.0,
      "trend_index": 0.3,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 40.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 0,
    "balanced_count": 6,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_balanced"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体状态良好，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的六条经络温度平衡，气血运行顺畅，这是一个非常好的状态。",
      "建议继续保持当前的作息和饮食习惯，定期复测以维护健康。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  }
}
```

### 验证点

- **预期分数**: 89, **实际分数**: 89
- **预期问题指数**: 0.3, **实际问题指数**: 0.3

---

## 12. test_10_diff_levels (温差等级)

**类型**: 首测

### 输入

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
    "gallbladder": {
      "group1_left": 37.8,
      "group1_right": 38.0,
      "group2_left": 39.8,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 37.5,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 36.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 35.0,
      "group1_right": 38.0,
      "group2_left": 35.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 34.0,
      "group1_right": 38.0,
      "group2_left": 34.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 75,
    "score_raw": 74.6,
    "problem_index": 28.0,
    "problem_index_detail": {
      "low_temperature_index": 6.0,
      "temperature_difference_index": 12.0,
      "side_bias_index": 5.0,
      "trend_index": 2.5,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "kidney",
        "side": "left",
        "value": 34.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "spleen",
        "side": "left",
        "value": 35.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "kidney",
      "meridian_name": "肾经",
      "side": "left",
      "title": "肾经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "spleen",
      "meridian_name": "脾经",
      "side": "left",
      "title": "脾经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 5,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "肾经、脾经需重点关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的检测结果显示，肾经、脾经问题比较突出，这可能影响相关脏腑功能。",
      "整体健康分75分，属于中度失衡，需要通过系统调理来改善。"
    ],
    "retestPrompt": "建议调理2-4周后复测，观察改善情况。"
  }
}
```

### 验证点

- **预期分数**: 75, **实际分数**: 75
- **预期问题指数**: 28.0, **实际问题指数**: 28.0

---

## 13. test_11_side_bias_4 (偏侧4条)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 84,
    "score_raw": 83.53,
    "problem_index": 14.5,
    "problem_index_detail": {
      "low_temperature_index": 3.0,
      "temperature_difference_index": 6.0,
      "side_bias_index": 3.5,
      "trend_index": 2.0,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 38.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 4,
    "right_low_count": 0,
    "balanced_count": 2,
    "result": "head_blood_supply_attention"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_left_low"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 4,
      "reason_codes": [
        "left_bias_count_high"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体良好，注意调理",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的经络整体状态不错，大部分经络都处于平衡状态。",
      "只是有轻微的不平衡，通过简单的饮食和作息调整就能改善。"
    ],
    "retestPrompt": "建议1-2个月后复测，观察调理效果。"
  }
}
```

### 验证点

- **预期分数**: 84, **实际分数**: 84
- **预期问题指数**: 14.5, **实际问题指数**: 14.5

---

## 14. test_12_side_bias_5 (偏侧5条)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 38.0,
      "group1_right": 36.0,
      "group2_left": 40.0,
      "group2_right": 38.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 36.0,
      "group2_left": 40.0,
      "group2_right": 38.0
    },
    "bladder": {
      "group1_left": 38.0,
      "group1_right": 36.0,
      "group2_left": 40.0,
      "group2_right": 38.0
    },
    "liver": {
      "group1_left": 38.0,
      "group1_right": 36.0,
      "group2_left": 40.0,
      "group2_right": 38.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 36.0,
      "group2_left": 40.0,
      "group2_right": 38.0
    },
    "kidney": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 82,
    "score_raw": 81.6,
    "problem_index": 18.0,
    "problem_index_detail": {
      "low_temperature_index": 3.0,
      "temperature_difference_index": 7.5,
      "side_bias_index": 5.0,
      "trend_index": 2.5,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "right",
        "value": 38.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "left",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 5,
    "balanced_count": 1,
    "result": "heart_attention"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_right_low"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "心脏方向需关注",
      "right_low_count": 5,
      "reason_codes": [
        "right_bias_count_high"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体良好，注意调理",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的经络整体状态不错，大部分经络都处于平衡状态。",
      "只是有轻微的不平衡，通过简单的饮食和作息调整就能改善。"
    ],
    "retestPrompt": "建议1-2个月后复测，观察调理效果。"
  }
}
```

### 验证点

- **预期分数**: 82, **实际分数**: 82
- **预期问题指数**: 18.0, **实际问题指数**: 18.0

---

## 15. test_13_side_bias_6 (偏侧6条)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 80,
    "score_raw": 79.67,
    "problem_index": 21.5,
    "problem_index_detail": {
      "low_temperature_index": 1.0,
      "temperature_difference_index": 9.0,
      "side_bias_index": 6.0,
      "trend_index": 3.0,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 38.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 6,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体良好，注意调理",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的经络整体状态不错，大部分经络都处于平衡状态。",
      "只是有轻微的不平衡，通过简单的饮食和作息调整就能改善。"
    ],
    "retestPrompt": "建议1-2个月后复测，观察调理效果。"
  }
}
```

### 验证点

- **预期分数**: 80, **实际分数**: 80
- **预期问题指数**: 21.5, **实际问题指数**: 21.5

---

## 16. test_14_cervical_opposite (颈椎-相反低)

**类型**: 首测

### 输入

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
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 38.0,
      "group1_right": 36.0,
      "group2_left": 40.0,
      "group2_right": 38.0
    },
    "liver": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 86,
    "score_raw": 86.2,
    "problem_index": 9.5,
    "problem_index_detail": {
      "low_temperature_index": 3.0,
      "temperature_difference_index": 3.0,
      "side_bias_index": 0.0,
      "trend_index": 1.0,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "bladder",
        "side": "right",
        "value": 38.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "left",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 1,
    "right_low_count": 1,
    "balanced_count": 4,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "cervical",
    "kidney_trend": "stable_left_low",
    "bladder_trend": "stable_right_low"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "right",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 3,
      "type": "cervical_lumbar",
      "title": "颈椎相关问题需关注",
      "reason_codes": [
        "cervical_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体状态良好，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的六条经络温度平衡，气血运行顺畅，这是一个非常好的状态。",
      "建议继续保持当前的作息和饮食习惯，定期复测以维护健康。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  }
}
```

### 验证点

- **预期分数**: 86, **实际分数**: 86
- **预期问题指数**: 9.5, **实际问题指数**: 9.5

---

## 17. test_15_cervical_lumbar_cross (交叉=颈+腰)

**类型**: 首测

### 输入

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
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 38.0
    },
    "liver": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 86,
    "score_raw": 85.89,
    "problem_index": 10.2,
    "problem_index_detail": {
      "low_temperature_index": 3.0,
      "temperature_difference_index": 3.0,
      "side_bias_index": 0.0,
      "trend_index": 1.7,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "bladder",
        "side": "right",
        "value": 38.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "left",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 1,
    "right_low_count": 1,
    "balanced_count": 4,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "cervical_and_lumbar",
    "kidney_trend": "stable_left_low",
    "bladder_trend": "cross"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "right",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 3,
      "type": "cervical_lumbar",
      "title": "颈椎和腰椎问题同时存在",
      "reason_codes": [
        "cervical_and_lumbar_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体状态良好，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的六条经络温度平衡，气血运行顺畅，这是一个非常好的状态。",
      "建议继续保持当前的作息和饮食习惯，定期复测以维护健康。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  }
}
```

### 验证点

- **预期分数**: 86, **实际分数**: 86
- **预期问题指数**: 10.2, **实际问题指数**: 10.2

---

## 18. test_16_gender_male (性别-男性)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "male",
  "meridians": {
    "stomach": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 80,
    "score_raw": 80.22,
    "problem_index": 20.5,
    "problem_index_detail": {
      "low_temperature_index": 3.0,
      "temperature_difference_index": 7.5,
      "side_bias_index": 5.0,
      "trend_index": 2.5,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 38.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 5,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体良好，注意调理",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的经络整体状态不错，大部分经络都处于平衡状态。",
      "只是有轻微的不平衡，通过简单的饮食和作息调整就能改善。"
    ],
    "retestPrompt": "建议1-2个月后复测，观察调理效果。"
  }
}
```

### 验证点

- **预期分数**: 80, **实际分数**: 80
- **预期问题指数**: 20.5, **实际问题指数**: 20.5

---

## 19. test_17_gender_female (性别-女性)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 80,
    "score_raw": 80.22,
    "problem_index": 20.5,
    "problem_index_detail": {
      "low_temperature_index": 3.0,
      "temperature_difference_index": 7.5,
      "side_bias_index": 5.0,
      "trend_index": 2.5,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 38.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 5,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体良好，注意调理",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的经络整体状态不错，大部分经络都处于平衡状态。",
      "只是有轻微的不平衡，通过简单的饮食和作息调整就能改善。"
    ],
    "retestPrompt": "建议1-2个月后复测，观察调理效果。"
  }
}
```

### 验证点

- **预期分数**: 80, **实际分数**: 80
- **预期问题指数**: 20.5, **实际问题指数**: 20.5

---

## 20. test_18_gender_unknown (性别-未知)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "unknown",
  "meridians": {
    "stomach": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 80,
    "score_raw": 80.22,
    "problem_index": 20.5,
    "problem_index_detail": {
      "low_temperature_index": 3.0,
      "temperature_difference_index": 7.5,
      "side_bias_index": 5.0,
      "trend_index": 2.5,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 38.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 5,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体良好，注意调理",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的经络整体状态不错，大部分经络都处于平衡状态。",
      "只是有轻微的不平衡，通过简单的饮食和作息调整就能改善。"
    ],
    "retestPrompt": "建议1-2个月后复测，观察调理效果。"
  }
}
```

### 验证点

- **预期分数**: 80, **实际分数**: 80
- **预期问题指数**: 20.5, **实际问题指数**: 20.5

---

## 21. test_19_retest_0_2_days (0-2天)

**类型**: 复测

### 输入

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 75,
  "previous_problem_index": 28.0,
  "usage_days_between_tests": 2,
  "meridians": {
    "stomach": {
      "group1_left": 36.5,
      "group1_right": 38.0,
      "group2_left": 39.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.5,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 35.0,
      "group1_right": 37.0,
      "group2_left": 37.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 37.5,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 35.5,
      "group1_right": 37.0,
      "group2_left": 38.0,
      "group2_right": 39.5
    },
    "kidney": {
      "group1_left": 35.0,
      "group1_right": 36.0,
      "group2_left": 37.0,
      "group2_right": 39.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 77,
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
      {
        "meridian": "bladder",
        "side": "left",
        "value": 37.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "liver",
        "side": "left",
        "value": 38.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "liver",
      "meridian_name": "肝经",
      "side": "left",
      "title": "肝经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 6,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "状态稳定，持续调理",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的健康分保持在77分，状态比较稳定。",
      "调理需要时间，建议继续当前的方案，耐心等待改善。"
    ],
    "retestPrompt": "建议调理2-4周后复测，观察改善情况。"
  },
  "retest_detail": {
    "usage_days": 2,
    "usage_bonus": 0.0,
    "delta_I": 2.0,
    "improvement_bonus": 0.6,
    "retest_score_base": 76.8,
    "protected_score": 76.8,
    "previous_score": 75,
    "previous_problem_index": 28.0,
    "current_problem_index": 26.0
  }
}
```

### 验证点

- **预期分数**: 77, **实际分数**: 77
- **预期问题指数**: 26.0, **实际问题指数**: 26.0

---

## 22. test_20_retest_3_6_days (3-6天)

**类型**: 复测

### 输入

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 75,
  "previous_problem_index": 28.0,
  "usage_days_between_tests": 5,
  "meridians": {
    "stomach": {
      "group1_left": 36.5,
      "group1_right": 38.0,
      "group2_left": 39.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.5,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 35.0,
      "group1_right": 37.0,
      "group2_left": 37.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 37.5,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 35.5,
      "group1_right": 37.0,
      "group2_left": 38.0,
      "group2_right": 39.5
    },
    "kidney": {
      "group1_left": 35.0,
      "group1_right": 36.0,
      "group2_left": 37.0,
      "group2_right": 39.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 78,
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
      {
        "meridian": "bladder",
        "side": "left",
        "value": 37.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "liver",
        "side": "left",
        "value": 38.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "liver",
      "meridian_name": "肝经",
      "side": "left",
      "title": "肝经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 6,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "调理见效，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "太好了！您的健康分从75分提升到了78分，调理效果非常明显。",
      "这说明我们的调理方向是对的，您的配合也很好，建议继续坚持。"
    ],
    "retestPrompt": "建议调理2-4周后复测，观察改善情况。"
  },
  "retest_detail": {
    "usage_days": 5,
    "usage_bonus": 1.0,
    "delta_I": 2.0,
    "improvement_bonus": 0.6,
    "retest_score_base": 77.8,
    "protected_score": 77.8,
    "previous_score": 75,
    "previous_problem_index": 28.0,
    "current_problem_index": 26.0
  }
}
```

### 验证点

- **预期分数**: 78, **实际分数**: 78
- **预期问题指数**: 26.0, **实际问题指数**: 26.0

---

## 23. test_21_retest_7_13_days (7-13天)

**类型**: 复测

### 输入

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 75,
  "previous_problem_index": 28.0,
  "usage_days_between_tests": 10,
  "meridians": {
    "stomach": {
      "group1_left": 36.5,
      "group1_right": 38.0,
      "group2_left": 39.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.5,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 35.0,
      "group1_right": 37.0,
      "group2_left": 37.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 37.5,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 35.5,
      "group1_right": 37.0,
      "group2_left": 38.0,
      "group2_right": 39.5
    },
    "kidney": {
      "group1_left": 35.0,
      "group1_right": 36.0,
      "group2_left": 37.0,
      "group2_right": 39.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 79,
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
      {
        "meridian": "bladder",
        "side": "left",
        "value": 37.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "liver",
        "side": "left",
        "value": 38.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "liver",
      "meridian_name": "肝经",
      "side": "left",
      "title": "肝经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 6,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "调理见效，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "太好了！您的健康分从75分提升到了79分，调理效果非常明显。",
      "这说明我们的调理方向是对的，您的配合也很好，建议继续坚持。"
    ],
    "retestPrompt": "建议调理2-4周后复测，观察改善情况。"
  },
  "retest_detail": {
    "usage_days": 10,
    "usage_bonus": 2.0,
    "delta_I": 2.0,
    "improvement_bonus": 0.6,
    "retest_score_base": 78.8,
    "protected_score": 78.8,
    "previous_score": 75,
    "previous_problem_index": 28.0,
    "current_problem_index": 26.0
  }
}
```

### 验证点

- **预期分数**: 79, **实际分数**: 79
- **预期问题指数**: 26.0, **实际问题指数**: 26.0

---

## 24. test_22_retest_14_29_days_low (14-29天(<88))

**类型**: 复测

### 输入

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 75,
  "previous_problem_index": 28.0,
  "usage_days_between_tests": 20,
  "meridians": {
    "stomach": {
      "group1_left": 36.5,
      "group1_right": 38.0,
      "group2_left": 39.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.5,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 35.0,
      "group1_right": 37.0,
      "group2_left": 37.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 37.5,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 35.5,
      "group1_right": 37.0,
      "group2_left": 38.0,
      "group2_right": 39.5
    },
    "kidney": {
      "group1_left": 35.0,
      "group1_right": 36.0,
      "group2_left": 37.0,
      "group2_right": 39.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 80,
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
      {
        "meridian": "bladder",
        "side": "left",
        "value": 37.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "liver",
        "side": "left",
        "value": 38.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "liver",
      "meridian_name": "肝经",
      "side": "left",
      "title": "肝经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 6,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "调理见效，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "太好了！您的健康分从75分提升到了80分，调理效果非常明显。",
      "这说明我们的调理方向是对的，您的配合也很好，建议继续坚持。"
    ],
    "retestPrompt": "建议1-2个月后复测，观察调理效果。"
  },
  "retest_detail": {
    "usage_days": 20,
    "usage_bonus": 3.0,
    "delta_I": 2.0,
    "improvement_bonus": 0.6,
    "retest_score_base": 79.8,
    "protected_score": 79.8,
    "previous_score": 75,
    "previous_problem_index": 28.0,
    "current_problem_index": 26.0
  }
}
```

### 验证点

- **预期分数**: 80, **实际分数**: 80
- **预期问题指数**: 26.0, **实际问题指数**: 26.0

---

## 25. test_23_retest_14_29_days_high (14-29天(≥88)→95分)

**类型**: 复测

### 输入

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 90,
  "previous_problem_index": 15.0,
  "usage_days_between_tests": 20,
  "meridians": {
    "stomach": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 95,
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
      {
        "meridian": "stomach",
        "side": "left",
        "value": 40.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 0,
    "balanced_count": 6,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_balanced"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "调理见效，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "太好了！您的健康分从90分提升到了95分，调理效果非常明显。",
      "这说明我们的调理方向是对的，您的配合也很好，建议继续坚持。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  },
  "retest_detail": {
    "usage_days": 20,
    "usage_bonus": 3.0,
    "delta_I": 15.0,
    "improvement_bonus": 3.0,
    "retest_score_base": 96.0,
    "protected_score": 96.0,
    "previous_score": 90,
    "previous_problem_index": 15.0,
    "current_problem_index": 0.0
  }
}
```

### 验证点

- **预期分数**: 95, **实际分数**: 95
- **预期问题指数**: 0.0, **实际问题指数**: 0.0

---

## 26. test_24_retest_30_plus_days (30天+)

**类型**: 复测

### 输入

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 75,
  "previous_problem_index": 28.0,
  "usage_days_between_tests": 35,
  "meridians": {
    "stomach": {
      "group1_left": 36.5,
      "group1_right": 38.0,
      "group2_left": 39.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.5,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 35.0,
      "group1_right": 37.0,
      "group2_left": 37.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 37.5,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 35.5,
      "group1_right": 37.0,
      "group2_left": 38.0,
      "group2_right": 39.5
    },
    "kidney": {
      "group1_left": 35.0,
      "group1_right": 36.0,
      "group2_left": 37.0,
      "group2_right": 39.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 81,
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
      {
        "meridian": "bladder",
        "side": "left",
        "value": 37.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "liver",
        "side": "left",
        "value": 38.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "liver",
      "meridian_name": "肝经",
      "side": "left",
      "title": "肝经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 6,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "调理见效，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "太好了！您的健康分从75分提升到了81分，调理效果非常明显。",
      "这说明我们的调理方向是对的，您的配合也很好，建议继续坚持。"
    ],
    "retestPrompt": "建议1-2个月后复测，观察调理效果。"
  },
  "retest_detail": {
    "usage_days": 35,
    "usage_bonus": 4.0,
    "delta_I": 2.0,
    "improvement_bonus": 0.6,
    "retest_score_base": 80.8,
    "protected_score": 80.8,
    "previous_score": 75,
    "previous_problem_index": 28.0,
    "current_problem_index": 26.0
  }
}
```

### 验证点

- **预期分数**: 81, **实际分数**: 81
- **预期问题指数**: 26.0, **实际问题指数**: 26.0

---

## 27. test_25_retest_improvement (数据改善→95分)

**类型**: 复测

### 输入

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 70,
  "previous_problem_index": 30.0,
  "usage_days_between_tests": 14,
  "meridians": {
    "stomach": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 95,
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
      {
        "meridian": "stomach",
        "side": "left",
        "value": 40.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 0,
    "balanced_count": 6,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_balanced"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "调理见效，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "太好了！您的健康分从70分提升到了95分，调理效果非常明显。",
      "这说明我们的调理方向是对的，您的配合也很好，建议继续坚持。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  },
  "retest_detail": {
    "usage_days": 14,
    "usage_bonus": 3.0,
    "delta_I": 30.0,
    "improvement_bonus": 3.0,
    "retest_score_base": 96.0,
    "protected_score": 96.0,
    "previous_score": 70,
    "previous_problem_index": 30.0,
    "current_problem_index": 0.0
  }
}
```

### 验证点

- **预期分数**: 95, **实际分数**: 95
- **预期问题指数**: 0.0, **实际问题指数**: 0.0

---

## 28. test_26_low_temp_index_max (低温指数最大)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 44.0,
      "group2_right": 44.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 44.0,
      "group2_right": 44.0
    },
    "bladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 44.0,
      "group2_right": 44.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 44.0,
      "group2_right": 44.0
    },
    "kidney": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 44.0,
      "group2_right": 44.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 88,
    "score_raw": 87.6,
    "problem_index": 6.0,
    "problem_index_detail": {
      "low_temperature_index": 6.0,
      "temperature_difference_index": 0.0,
      "side_bias_index": 0.0,
      "trend_index": 0.0,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "bladder",
        "side": "left",
        "value": 40.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "left",
        "value": 44.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 0,
    "balanced_count": 6,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_balanced"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体状态良好，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的六条经络温度平衡，气血运行顺畅，这是一个非常好的状态。",
      "建议继续保持当前的作息和饮食习惯，定期复测以维护健康。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  }
}
```

### 验证点

- **预期分数**: 88, **实际分数**: 88
- **预期问题指数**: 6.0, **实际问题指数**: 6.0

---

## 29. test_27_diff_change_improved (温差改善)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 34.0,
      "group1_right": 38.0,
      "group2_left": 39.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 89,
    "score_raw": 89.4,
    "problem_index": 1.5,
    "problem_index_detail": {
      "low_temperature_index": 0.0,
      "temperature_difference_index": 1.0,
      "side_bias_index": 0.0,
      "trend_index": 0.5,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 39.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 1,
    "right_low_count": 0,
    "balanced_count": 5,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_balanced"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体状态良好，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的六条经络温度平衡，气血运行顺畅，这是一个非常好的状态。",
      "建议继续保持当前的作息和饮食习惯，定期复测以维护健康。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  }
}
```

### 验证点

- **预期分数**: 89, **实际分数**: 89
- **预期问题指数**: 1.5, **实际问题指数**: 1.5

---

## 30. test_28_diff_change_worsened (温差恶化)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.0,
      "group2_right": 42.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 88,
    "score_raw": 87.8,
    "problem_index": 5.5,
    "problem_index_detail": {
      "low_temperature_index": 1.0,
      "temperature_difference_index": 4.0,
      "side_bias_index": 0.0,
      "trend_index": 0.5,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 38.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "gallbladder",
        "side": "left",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 1,
    "right_low_count": 0,
    "balanced_count": 5,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_balanced"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "gallbladder",
      "meridian_name": "胆经",
      "side": "left",
      "title": "胆经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体状态良好，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的六条经络温度平衡，气血运行顺畅，这是一个非常好的状态。",
      "建议继续保持当前的作息和饮食习惯，定期复测以维护健康。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  }
}
```

### 验证点

- **预期分数**: 88, **实际分数**: 88
- **预期问题指数**: 5.5, **实际问题指数**: 5.5

---

## 31. test_29_realistic_mild (真实-轻度)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 37.8,
      "group1_right": 38.0,
      "group2_left": 39.8,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 37.5,
      "group1_right": 38.0,
      "group2_left": 39.5,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 38.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 89,
    "score_raw": 89.4,
    "problem_index": 1.5,
    "problem_index_detail": {
      "low_temperature_index": 0.0,
      "temperature_difference_index": 0.5,
      "side_bias_index": 0.0,
      "trend_index": 1.0,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "bladder",
        "side": "left",
        "value": 39.5,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "left",
        "value": 39.8,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 2,
    "right_low_count": 0,
    "balanced_count": 4,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_left_low"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体状态良好，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的六条经络温度平衡，气血运行顺畅，这是一个非常好的状态。",
      "建议继续保持当前的作息和饮食习惯，定期复测以维护健康。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  }
}
```

### 验证点

- **预期分数**: 89, **实际分数**: 89
- **预期问题指数**: 1.5, **实际问题指数**: 1.5

---

## 32. test_30_realistic_moderate (真实-中度)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 36.5,
      "group1_right": 38.0,
      "group2_left": 39.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 39.5,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 35.0,
      "group1_right": 37.0,
      "group2_left": 37.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 36.0,
      "group1_right": 38.0,
      "group2_left": 38.5,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 35.5,
      "group1_right": 37.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 36.0,
      "group1_right": 37.0,
      "group2_left": 38.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 76,
    "score_raw": 75.8,
    "problem_index": 26.5,
    "problem_index_detail": {
      "low_temperature_index": 5.0,
      "temperature_difference_index": 10.0,
      "side_bias_index": 6.0,
      "trend_index": 3.0,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "bladder",
        "side": "left",
        "value": 37.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "spleen",
        "side": "left",
        "value": 38.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
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
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "spleen",
      "meridian_name": "脾经",
      "side": "left",
      "title": "脾经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 3,
      "type": "side_bias",
      "title": "头部供血需关注",
      "left_low_count": 6,
      "reason_codes": [
        "left_bias_count_high"
      ]
    },
    {
      "priority": 4,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "膀胱经、脾经需重点关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的检测结果显示，膀胱经、脾经问题比较突出，这可能影响相关脏腑功能。",
      "整体健康分76分，属于中度失衡，需要通过系统调理来改善。"
    ],
    "retestPrompt": "建议调理2-4周后复测，观察改善情况。"
  }
}
```

### 验证点

- **预期分数**: 76, **实际分数**: 76
- **预期问题指数**: 26.5, **实际问题指数**: 26.5

---

## 33. test_31_bladder_lowest (膀胱最低)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 37.5,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 35.0,
      "group1_right": 36.0,
      "group2_left": 37.0,
      "group2_right": 39.0
    },
    "liver": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 36.5,
      "group1_right": 37.5,
      "group2_left": 39.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 35.5,
      "group1_right": 36.5,
      "group2_left": 38.0,
      "group2_right": 39.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 83,
    "score_raw": 83.31,
    "problem_index": 14.9,
    "problem_index_detail": {
      "low_temperature_index": 5.0,
      "temperature_difference_index": 5.0,
      "side_bias_index": 0.0,
      "trend_index": 2.4000000000000004,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "bladder",
        "side": "left",
        "value": 37.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "kidney",
        "side": "left",
        "value": 38.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 3,
    "right_low_count": 0,
    "balanced_count": 3,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "lumbar",
    "kidney_trend": "stable_left_low",
    "bladder_trend": "stable_left_low"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "kidney",
      "meridian_name": "肾经",
      "side": "left",
      "title": "肾经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 3,
      "type": "cervical_lumbar",
      "title": "腰椎相关问题需关注",
      "reason_codes": [
        "lumbar_issue_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体良好，注意调理",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的经络整体状态不错，大部分经络都处于平衡状态。",
      "只是有轻微的不平衡，通过简单的饮食和作息调整就能改善。"
    ],
    "retestPrompt": "建议1-2个月后复测，观察调理效果。"
  }
}
```

### 验证点

- **预期分数**: 83, **实际分数**: 83
- **预期问题指数**: 14.9, **实际问题指数**: 14.9

---

## 34. test_32_kidney_cross (肾交叉)

**类型**: 首测

### 输入

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 37.5,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 36.0,
      "group1_right": 37.0,
      "group2_left": 39.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 36.5,
      "group1_right": 37.5,
      "group2_left": 39.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 35.0,
      "group1_right": 37.0,
      "group2_left": 40.0,
      "group2_right": 38.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 84,
    "score_raw": 84.3,
    "problem_index": 13.1,
    "problem_index_detail": {
      "low_temperature_index": 3.0,
      "temperature_difference_index": 4.5,
      "side_bias_index": 0.0,
      "trend_index": 3.1,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "kidney",
        "side": "right",
        "value": 38.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "bladder",
        "side": "left",
        "value": 39.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 2,
    "right_low_count": 1,
    "balanced_count": 3,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "cervical_and_lumbar",
    "kidney_trend": "cross",
    "bladder_trend": "stable_left_low"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "kidney",
      "meridian_name": "肾经",
      "side": "right",
      "title": "肾经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "bladder",
      "meridian_name": "膀胱经",
      "side": "left",
      "title": "膀胱经问题较突出",
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_health_problem"
      ]
    },
    {
      "priority": 3,
      "type": "cervical_lumbar",
      "title": "颈椎和腰椎问题同时存在",
      "reason_codes": [
        "cervical_and_lumbar_detected"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "整体良好，注意调理",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "您的经络整体状态不错，大部分经络都处于平衡状态。",
      "只是有轻微的不平衡，通过简单的饮食和作息调整就能改善。"
    ],
    "retestPrompt": "建议1-2个月后复测，观察调理效果。"
  }
}
```

### 验证点

- **预期分数**: 84, **实际分数**: 84
- **预期问题指数**: 13.1, **实际问题指数**: 13.1

---

## 35. test_33_retest_92_score (92分-中等高分)

**类型**: 复测

### 输入

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 85,
  "previous_problem_index": 18.0,
  "usage_days_between_tests": 5,
  "meridians": {
    "stomach": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 93,
    "score_raw": 89.28,
    "problem_index": 1.8,
    "problem_index_detail": {
      "low_temperature_index": 0.0,
      "temperature_difference_index": 0.0,
      "side_bias_index": 0.0,
      "trend_index": 1.8,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 40.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 0,
    "balanced_count": 6,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "fast_response",
    "bladder_trend": "fast_response"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "调理见效，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "太好了！您的健康分从85分提升到了93分，调理效果非常明显。",
      "这说明我们的调理方向是对的，您的配合也很好，建议继续坚持。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  },
  "retest_detail": {
    "usage_days": 5,
    "usage_bonus": 1.0,
    "delta_I": 16.2,
    "improvement_bonus": 3.0,
    "retest_score_base": 93.28,
    "protected_score": 93.28,
    "previous_score": 85,
    "previous_problem_index": 18.0,
    "current_problem_index": 1.8
  }
}
```

### 验证点

- **预期分数**: 93, **实际分数**: 93
- **预期问题指数**: 1.8, **实际问题指数**: 1.8

---

## 36. test_34_retest_91_score (91分-高分起步)

**类型**: 复测

### 输入

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 82,
  "previous_problem_index": 20.0,
  "usage_days_between_tests": 10,
  "meridians": {
    "stomach": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 94,
    "score_raw": 89.28,
    "problem_index": 1.8,
    "problem_index_detail": {
      "low_temperature_index": 0.0,
      "temperature_difference_index": 0.0,
      "side_bias_index": 0.0,
      "trend_index": 1.8,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 40.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 0,
    "balanced_count": 6,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "fast_response",
    "bladder_trend": "fast_response"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "调理见效，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "太好了！您的健康分从82分提升到了94分，调理效果非常明显。",
      "这说明我们的调理方向是对的，您的配合也很好，建议继续坚持。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  },
  "retest_detail": {
    "usage_days": 10,
    "usage_bonus": 2.0,
    "delta_I": 18.2,
    "improvement_bonus": 3.0,
    "retest_score_base": 94.28,
    "protected_score": 94.28,
    "previous_score": 82,
    "previous_problem_index": 20.0,
    "current_problem_index": 1.8
  }
}
```

### 验证点

- **预期分数**: 94, **实际分数**: 94
- **预期问题指数**: 1.8, **实际问题指数**: 1.8

---

## 37. test_35_retest_93_score (93分-接近封顶)

**类型**: 复测

### 输入

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 88,
  "previous_problem_index": 15.0,
  "usage_days_between_tests": 21,
  "meridians": {
    "stomach": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 95,
    "score_raw": 89.28,
    "problem_index": 1.8,
    "problem_index_detail": {
      "low_temperature_index": 0.0,
      "temperature_difference_index": 0.0,
      "side_bias_index": 0.0,
      "trend_index": 1.8,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 40.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 0,
    "balanced_count": 6,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "fast_response",
    "bladder_trend": "fast_response"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "调理见效，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "太好了！您的健康分从88分提升到了95分，调理效果非常明显。",
      "这说明我们的调理方向是对的，您的配合也很好，建议继续坚持。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  },
  "retest_detail": {
    "usage_days": 21,
    "usage_bonus": 3.0,
    "delta_I": 13.2,
    "improvement_bonus": 3.0,
    "retest_score_base": 95.28,
    "protected_score": 95.28,
    "previous_score": 88,
    "previous_problem_index": 15.0,
    "current_problem_index": 1.8
  }
}
```

### 验证点

- **预期分数**: 95, **实际分数**: 95
- **预期问题指数**: 1.8, **实际问题指数**: 1.8

---

## 38. test_36_retest_94_score (94分-保护机制)

**类型**: 复测

### 输入

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 90,
  "previous_problem_index": 12.0,
  "usage_days_between_tests": 10,
  "meridians": {
    "stomach": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "gallbladder": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "bladder": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "liver": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "spleen": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    },
    "kidney": {
      "group1_left": 37.0,
      "group1_right": 38.0,
      "group2_left": 40.0,
      "group2_right": 40.0
    }
  }
}
```

### 输出（实际运行结果）

```json
{
  "engine": {
    "mode": "rule-based-v3",
    "version": "3.0"
  },
  "score_result": {
    "score": 94,
    "score_raw": 89.28,
    "problem_index": 1.8,
    "problem_index_detail": {
      "low_temperature_index": 0.0,
      "temperature_difference_index": 0.0,
      "side_bias_index": 0.0,
      "trend_index": 1.8,
      "combo_index": 0.0
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 40.0,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "stomach",
        "side": "right",
        "value": 40.0,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 0,
    "balanced_count": 6,
    "result": "none"
  },
  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "fast_response",
    "bladder_trend": "fast_response"
  },
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    },
    {
      "priority": 2,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "right",
      "title": "胃经问题较突出",
      "reason_codes": [
        "second_group_lowest_point"
      ]
    }
  ],
  "storefront": {
    "focusHeadline": "调理见效，继续保持",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。如有不适请及时就医。",
    "talkTrack": [
      "太好了！您的健康分从90分提升到了94分，调理效果非常明显。",
      "这说明我们的调理方向是对的，您的配合也很好，建议继续坚持。"
    ],
    "retestPrompt": "建议3-6个月后定期复测，持续跟踪健康状态。"
  },
  "retest_detail": {
    "usage_days": 10,
    "usage_bonus": 2.0,
    "delta_I": 10.2,
    "improvement_bonus": 3.0,
    "retest_score_base": 94.28,
    "protected_score": 94.28,
    "previous_score": 90,
    "previous_problem_index": 12.0,
    "current_problem_index": 1.8
  }
}
```

### 验证点

- **预期分数**: 94, **实际分数**: 94
- **预期问题指数**: 1.8, **实际问题指数**: 1.8

---

## 附录：复测评分规则取值范围分析

### 各分量取值范围

| 分量 | 范围 | 说明 |
|------|------|------|
| usage_bonus | [0, 1, 2, 3, 4] | 0-2天, 3-6天, 7-13天, 14-29天, 30天+ |
| improvement_bonus | [0, 3] | min(3, 0.3×ΔI), delta_I≥10封顶 |
| score_raw | [65, 90] | 首测原始分范围 |
| retest_score_base | [65, 97] | score_raw + usage_bonus + improvement_bonus |
| protected_score | 动态 | 基于上次分数的保护 |
| **最终分数** | **[65, 95]** | clamp(protected_score, 65, 95) |

### 复测分数覆盖范围

| 分数段 | 测试用例 | 说明 |
|--------|----------|------|
| 77 | test_19 | 0-2天无保护，可能下降 |
| 78 | test_20 | 3-6天保护-2 |
| 79 | test_21 | 7-13天保护=上次 |
| 80 | test_22 | 14-29天保护+1 |
| 81 | test_24 | 30天+保护+2 |
| 89 | case_02 | PRD标准复测示例 |
| 93 | test_33 | 中等高分区间 |
| 94 | test_34 | 高分起步区间 |
| 94 | test_36 | 保护机制高分 |
| 95 | test_23 | 14-29天高分封顶 |
| 95 | test_25 | 数据改善封顶 |
| 95 | test_35 | 接近封顶区间 |

### 极端情况

**最高分 (95分):**
- 首测原始分 90 + usage_bonus 4 + improvement_bonus 3 = 97
- clamp(97, 65, 95) = 95

**最低分 (65分):**
- 首测原始分 65 + usage_bonus 0 + improvement_bonus 0 = 65
- clamp(65, 65, 95) = 65

### 保护机制效果

| 天数 | 上次<88 | 上次≥88 |
|------|---------|---------|
| 0-2天 | 无保护 | 无保护 |
| 3-6天 | 上次-2 | 上次-2 |
| 7-13天 | 上次 | 上次 |
| 14-29天 | 上次+1 | 上次 |
| 30天+ | 上次+2 | 上次 |

---

## 快速测试命令

```bash
# 运行所有测试
python3 tests/run_tests_v3.py

# 单个测试
python3 scripts/infer_v3.py fixtures/v3/case_01_first_test.json --pretty

# HTTP API 测试
curl -X POST http://localhost:18790/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  -d @fixtures/v3/case_01_first_test.json
```

---

*文档版本: v3.0*  
*最后更新: 2026-05-07*
