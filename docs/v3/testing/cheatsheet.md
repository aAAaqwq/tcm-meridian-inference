# TCM v3 测试用例速查表

## 快速运行

```bash
# 运行所有测试
python3 run_tests_v3.py

# 运行单个测试
python3 scripts/infer_v3.py fixtures/v3/case_01_first_test.json --pretty
```

---

## 测试用例索引

### 首测分数区间

| 文件 | 描述 | 期望分数 | 关键特征 |
|------|------|----------|----------|
| `test_01_excellent_score.json` | 健康优秀 | 89 (clamp) | 全部平衡，无问题 |
| `test_02_mild_imbalance.json` | 轻度失衡 | 89 | 轻微温差，2条轻度异常 |
| `test_03_moderate_imbalance.json` | 中度失衡 | 76 | 6条左低，头部供血，腰椎 |
| `test_04_significant_imbalance.json` | 明显失衡 | 76 | 多条交叉，严重温差 |

### 趋势类型

| 文件 | 趋势 | 颈椎/腰椎 | 验证点 |
|------|------|-----------|--------|
| `test_05_trend_stable_left_low.json` | stable_left_low | lumbar | 肾左低+膀胱左低 |
| `test_06_trend_stable_right_low.json` | stable_right_low | lumbar | 肾右低+膀胱右低 |
| `test_07_trend_cross.json` | cross | cervical_and_lumbar | 任意交叉 |
| `test_08_trend_potential_symptom.json` | potential_symptom | - | 第一组平衡→第二组异常 |
| `test_09_trend_fast_response.json` | fast_response | - | 第一组异常→第二组平衡 |

### 温差等级

| 文件 | 覆盖等级 |
|------|----------|
| `test_10_diff_levels.json` | balanced/mild/health/serious |

### 左右偏向 (C指数)

| 文件 | 左低 | 右低 | C值 | 结果 |
|------|------|------|-----|------|
| `test_11_side_bias_4.json` | 4 | 0 | 3.5 | 头部供血 |
| `test_12_side_bias_5.json` | 0 | 5 | 5.0 | 心脏关注 |
| `test_13_side_bias_6.json` | 6 | 0 | 6.0 | 头部供血 |

### 颈椎/腰椎

| 文件 | 肾经 | 膀胱经 | 结果 |
|------|------|--------|------|
| `test_14_cervical_opposite.json` | 左低 | 右低 | cervical |
| `test_15_cervical_lumbar_cross.json` | - | cross | cervical_and_lumbar |

### 性别过滤

| 文件 | 性别 | 禁用词 |
|------|------|--------|
| `test_16_gender_male.json` | male | 宫寒/子宫/例假/人流/剖腹产/子宫肌瘤 |
| `test_17_gender_female.json` | female | 前列腺/前列腺炎/前列腺钙化 |
| `test_18_gender_unknown.json` | unknown | 所有性别专属词 |

### 复测保护

| 文件 | 天数 | bonus | 保护规则 |
|------|------|-------|----------|
| `test_19_retest_0_2_days.json` | 2 | 0 | 无保护 |
| `test_20_retest_3_6_days.json` | 5 | 1 | max(本次,上次-2) |
| `test_21_retest_7_13_days.json` | 10 | 2 | max(本次,上次) |
| `test_22_retest_14_29_days_low.json` | 20 | 3 | max(本次,上次+1) |
| `test_23_retest_14_29_days_high.json` | 20 | 3 | max(本次,上次) |
| `test_24_retest_30_plus_days.json` | 35 | 4 | max(本次,上次+2) |
| `test_25_retest_improvement.json` | 14 | 3 | +improvement_bonus |

### 其他

| 文件 | 描述 |
|------|------|
| `test_26_low_temp_index_max.json` | A=6 (低温差距>3℃) |
| `test_27_diff_change_improved.json` | 温差改善 (-0.5修正) |
| `test_28_diff_change_worsened.json` | 温差恶化 (+0.5修正) |

### PRD示例

| 文件 | 描述 | 分数 | 问题指数 |
|------|------|------|----------|
| `case_01_first_test.json` | PRD首测示例 | 77 | 24.9 |
| `case_02_retest.json` | PRD复测示例 | 89 | 14.7 |

---

## 输出字段说明

### score_result

```json
{
  "score": 77,                    // 展示分数 (int)
  "score_raw": 77.08,             // 原始分数 (float)
  "problem_index": 24.9,          // 问题指数 I
  "problem_index_detail": {
    "low_temperature_index": 5.0,      // A
    "temperature_difference_index": 8.5, // B
    "side_bias_index": 5.0,            // C
    "trend_index": 3.9,                // D
    "combo_index": 2.5                 // E
  }
}
```

### lowest_points

```json
{
  "selected": [
    {
      "rank": 1,
      "meridian": "bladder",
      "side": "left",
      "value": 37.9,
      "must_report": true
    }
  ],
  "tie_candidates": []
}
```

### side_bias_summary

```json
{
  "left_low_count": 5,
  "right_low_count": 0,
  "balanced_count": 1,
  "result": "head_blood_supply_attention"  // 或 heart_attention/none
}
```

### cervical_lumbar_result

```json
{
  "result": "lumbar",           // cervical/lumbar/cervical_and_lumbar/none
  "kidney_trend": "stable_left_low",
  "bladder_trend": "stable_left_low"
}
```

### meridian_analysis (单条经络)

```json
{
  "meridian": "spleen",
  "meridian_name": "脾经",
  "group1_status": "right_low",
  "group2_status": "left_low",
  "trend": "cross",
  "group1_diff": 0.1,
  "group2_diff": 1.5,
  "group1_diff_level": "balanced",
  "group2_diff_level": "health_problem",
  "diff_change": "worsened",
  "matched_rules": ["血糖", "思虑重", "湿气"],
  "is_focus": true,
  "focus_reason": ["second_group_lowest_point", "group2_diff_health_problem"]
}
```

### focus_issues

```json
[
  {
    "priority": 1,
    "type": "lowest_point",     // lowest_point/side_bias/cervical_lumbar
    "title": "膀胱经问题较突出",
    "meridian": "bladder",
    "reason_codes": ["second_group_lowest_point"]
  }
]
```

### retest_detail (仅复测)

```json
{
  "usage_days": 14,
  "usage_bonus": 3.0,
  "delta_I": 10.2,
  "improvement_bonus": 3.0,
  "retest_score_base": 83.4,
  "protected_score": 83.4,
  "previous_score": 77,
  "previous_problem_index": 24.9
}
```

---

## 验证清单

运行测试后检查：

- [ ] 首测分数在 65-89 之间
- [ ] 复测分数在 65-95 之间
- [ ] 问题指数 I = A+B+C+D+E
- [ ] B指数封顶12，D指数封顶4
- [ ] 左右偏向 >=4 时触发 head/heart attention
- [ ] 肾+膀胱同侧低 → lumbar
- [ ] 肾+膀胱异侧低 → cervical
- [ ] 肾或膀胱交叉 → cervical_and_lumbar
- [ ] 复测保护规则按天数正确应用
- [ ] 数据改善 bonus = min(3, 0.3*ΔI)

---

*生成时间: 2026-05-04*
