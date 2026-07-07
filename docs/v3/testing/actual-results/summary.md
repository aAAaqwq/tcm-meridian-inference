# V3 API 测试结果汇总

**测试时间**: 2026-05-07 19:50:43
**API地址**: http://8.163.126.86:18790/api/inference/meridian-diagnosis

## 统计概览

- **测试总数**: 34
- **成功数**: 34
- **失败数**: 0
- **成功率**: 100.0%

## 详细结果

| 序号 | 测试文件 | 状态 | 响应时间(ms) | Score | Problem Index | Side Bias | Cervical/Lumbar | 错误 |
|------|----------|------|--------------|-------|---------------|-----------|-----------------|------|
| 1 | test_01_excellent_score.json | ✅ | 0.16 | 89 | 0.0 | {'left_low_coun | {'result': 'non | - |
| 2 | test_02_mild_imbalance.json | ✅ | 0.20 | 89 | 1.5 | {'left_low_coun | {'result': 'non | - |
| 3 | test_03_moderate_imbalance.json | ✅ | 0.23 | 76 | 26.0 | {'left_low_coun | {'result': 'lum | - |
| 4 | test_04_significant_imbalance.json | ✅ | 0.22 | 75 | 28.0 | {'left_low_coun | {'result': 'cer | - |
| 5 | test_05_trend_stable_left_low.json | ✅ | 0.23 | 74 | 28.5 | {'left_low_coun | {'result': 'lum | - |
| 6 | test_06_trend_stable_right_low.json | ✅ | 0.20 | 74 | 28.5 | {'left_low_coun | {'result': 'lum | - |
| 7 | test_07_trend_cross.json | ✅ | 0.20 | 77 | 25.0 | {'left_low_coun | {'result': 'cer | - |
| 8 | test_08_trend_potential_symptom.json | ✅ | 0.28 | 89 | 3.3 | {'left_low_coun | {'result': 'non | - |
| 9 | test_09_trend_fast_response.json | ✅ | 0.19 | 89 | 0.3 | {'left_low_coun | {'result': 'non | - |
| 10 | test_10_diff_levels.json | ✅ | 0.16 | 75 | 28.0 | {'left_low_coun | {'result': 'lum | - |
| 11 | test_11_side_bias_4.json | ✅ | 0.34 | 84 | 14.5 | {'left_low_coun | {'result': 'non | - |
| 12 | test_12_side_bias_5.json | ✅ | 0.21 | 82 | 18.0 | {'left_low_coun | {'result': 'non | - |
| 13 | test_13_side_bias_6.json | ✅ | 0.15 | 80 | 21.5 | {'left_low_coun | {'result': 'lum | - |
| 14 | test_14_cervical_opposite.json | ✅ | 0.19 | 86 | 9.5 | {'left_low_coun | {'result': 'cer | - |
| 15 | test_15_cervical_lumbar_cross.json | ✅ | 0.92 | 86 | 10.2 | {'left_low_coun | {'result': 'cer | - |
| 16 | test_16_gender_male.json | ✅ | 0.71 | 80 | 20.5 | {'left_low_coun | {'result': 'lum | - |
| 17 | test_17_gender_female.json | ✅ | 1.45 | 80 | 20.5 | {'left_low_coun | {'result': 'lum | - |
| 18 | test_18_gender_unknown.json | ✅ | 0.15 | 80 | 20.5 | {'left_low_coun | {'result': 'lum | - |
| 19 | test_19_retest_0_2_days.json | ✅ | 0.18 | 77 | 26.0 | {'left_low_coun | {'result': 'lum | - |
| 20 | test_20_retest_3_6_days.json | ✅ | 0.12 | 78 | 26.0 | {'left_low_coun | {'result': 'lum | - |
| 21 | test_21_retest_7_13_days.json | ✅ | 0.17 | 79 | 26.0 | {'left_low_coun | {'result': 'lum | - |
| 22 | test_22_retest_14_29_days_low.json | ✅ | 0.15 | 80 | 26.0 | {'left_low_coun | {'result': 'lum | - |
| 23 | test_23_retest_14_29_days_high.json | ✅ | 0.22 | 95 | 0.0 | {'left_low_coun | {'result': 'non | - |
| 24 | test_24_retest_30_plus_days.json | ✅ | 0.17 | 81 | 26.0 | {'left_low_coun | {'result': 'lum | - |
| 25 | test_25_retest_improvement.json | ✅ | 0.17 | 95 | 0.0 | {'left_low_coun | {'result': 'non | - |
| 26 | test_26_low_temp_index_max.json | ✅ | 0.15 | 88 | 6.0 | {'left_low_coun | {'result': 'non | - |
| 27 | test_27_diff_change_improved.json | ✅ | 0.12 | 89 | 1.5 | {'left_low_coun | {'result': 'non | - |
| 28 | test_28_diff_change_worsened.json | ✅ | 0.16 | 88 | 5.5 | {'left_low_coun | {'result': 'non | - |
| 29 | test_29_realistic_mild.json | ✅ | 0.15 | 89 | 1.5 | {'left_low_coun | {'result': 'non | - |
| 30 | test_30_realistic_moderate.json | ✅ | 0.20 | 76 | 26.5 | {'left_low_coun | {'result': 'lum | - |
| 31 | test_31_bladder_lowest.json | ✅ | 0.16 | 83 | 14.9 | {'left_low_coun | {'result': 'lum | - |
| 32 | test_32_kidney_cross.json | ✅ | 0.16 | 84 | 13.1 | {'left_low_coun | {'result': 'cer | - |
| 33 | case_01_first_test.json | ✅ | 0.18 | 77 | 24.9 | {'left_low_coun | {'result': 'lum | - |
| 34 | case_02_retest.json | ✅ | 0.23 | 89 | 14.7 | {'left_low_coun | {'result': 'non | - |

## 关键字段详细对比

### test_01_excellent_score.json

**测试名称**: 首测 - 健康优秀分数区间(90-100): 所有经络平衡,温差小,问题指数<=10
**状态**: 成功
**响应时间**: 0.16 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 89 | 89 ✅ |
| problem_index | 0.0 | 0.0 ✅ |
| problem_index_detail | {'low_temperature_index': 0.0, 'temperature_difference_index': 0.0, 'side_bias_index': 0.0, 'trend_index': 0.0, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 0, 'right_low_count': 0, 'balanced_count': 6, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'stable_balanced', 'bladder_trend': 'stable_balanced'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "left", "value": 40.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_02_mild_imbalance.json

**测试名称**: 首测 - 轻度失衡分数区间(80-89): 轻微温差,1-2条经络轻度异常
**状态**: 成功
**响应时间**: 0.20 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 89 | None ⚠️ |
| problem_index | 1.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 0.0, 'temperature_difference_index': 0.5, 'side_bias_index': 0.0, 'trend_index': 1.0, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 2, 'right_low_count': 0, 'balanced_count': 4, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'stable_balanced', 'bladder_trend': 'stable_balanced'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "spleen", "side": "left", "value": 39.7, "rank": 1, "must_report": true}, {"meridian": "liver", "side": "left", "value": 39.8, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_03_moderate_imbalance.json

**测试名称**: 首测 - 中度失衡分数区间(70-79): 多条经络有温差,偏侧明显
**状态**: 成功
**响应时间**: 0.23 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 76 | None ⚠️ |
| problem_index | 26.0 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 11.5, 'side_bias_index': 6.0, 'trend_index': 3.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 6, 'right_low_count': 0, 'balanced_count': 0, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "left", "value": 37.0, "rank": 1, "must_report": true}, {"meridian": "liver", "side": "left", "value": 38.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_04_significant_imbalance.json

**测试名称**: 首测 - 严重失衡: 极端温差,多交叉,最高问题指数~30.5,分数~73
**状态**: 成功
**响应时间**: 0.22 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 75 | 73 ⚠️ |
| problem_index | 28.0 | 28.0 ✅ |
| problem_index_detail | {'low_temperature_index': 6.0, 'temperature_difference_index': 12.0, 'side_bias_index': 3.5, 'trend_index': 4.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 2, 'right_low_count': 4, 'balanced_count': 0, 'result': 'heart_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'cervical_and_lumbar', 'kidney_trend': 'cross', 'bladder_trend': 'cross'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "right", "value": 30.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 32.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_05_trend_stable_left_low.json

**测试名称**: 趋势测试 - stable_left_low: 两组均左低,肾经和膀胱经同左低→腰椎问题
**状态**: 成功
**响应时间**: 0.23 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 74 | None ⚠️ |
| problem_index | 28.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 5.0, 'temperature_difference_index': 12.0, 'side_bias_index': 6.0, 'trend_index': 3.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 6, 'right_low_count': 0, 'balanced_count': 0, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "kidney", "side": "left", "value": 36.0, "rank": 1, "must_report": true}, {"meridian": "bladder", "side": "left", "value": 37.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_06_trend_stable_right_low.json

**测试名称**: 趋势测试 - stable_right_low: 两组均右低,肾经和膀胱经同右低→腰椎问题
**状态**: 成功
**响应时间**: 0.20 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 74 | None ⚠️ |
| problem_index | 28.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 5.0, 'temperature_difference_index': 12.0, 'side_bias_index': 6.0, 'trend_index': 3.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 0, 'right_low_count': 6, 'balanced_count': 0, 'result': 'heart_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_right_low', 'bladder_trend': 'stable_right_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "kidney", "side": "right", "value": 36.0, "rank": 1, "must_report": true}, {"meridian": "bladder", "side": "right", "value": 37.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_07_trend_cross.json

**测试名称**: 趋势测试 - cross: 两组左右方向相反,肾经左低+膀胱经右低→颈椎问题
**状态**: 成功
**响应时间**: 0.20 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 77 | None ⚠️ |
| problem_index | 25.0 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 9.5, 'side_bias_index': 6.0, 'trend_index': 4.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 0, 'right_low_count': 6, 'balanced_count': 0, 'result': 'heart_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'cervical_and_lumbar', 'kidney_trend': 'cross', 'bladder_trend': 'cross'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "right", "value": 37.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 38.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_08_trend_potential_symptom.json

**测试名称**: 趋势测试 - potential_symptom: 第一组平衡,第二组左低,表示潜在症状
**状态**: 成功
**响应时间**: 0.28 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 89 | None ⚠️ |
| problem_index | 3.3 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 1.0, 'temperature_difference_index': 2.0, 'side_bias_index': 0.0, 'trend_index': 0.3, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 1, 'right_low_count': 0, 'balanced_count': 5, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'stable_balanced', 'bladder_trend': 'stable_balanced'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "left", "value": 38.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_09_trend_fast_response.json

**测试名称**: 趋势测试 - fast_response: 第一组左低,第二组平衡,表示调理反应较快
**状态**: 成功
**响应时间**: 0.19 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 89 | None ⚠️ |
| problem_index | 0.3 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 0.0, 'temperature_difference_index': 0.0, 'side_bias_index': 0.0, 'trend_index': 0.3, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 0, 'right_low_count': 0, 'balanced_count': 6, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'stable_balanced', 'bladder_trend': 'stable_balanced'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "left", "value": 40.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_10_diff_levels.json

**测试名称**: 温差等级测试: 覆盖balanced/mild/health_problem/serious_problem四种等级
**状态**: 成功
**响应时间**: 0.16 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 75 | None ⚠️ |
| problem_index | 28.0 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 6.0, 'temperature_difference_index': 12.0, 'side_bias_index': 5.0, 'trend_index': 2.5, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 5, 'right_low_count': 0, 'balanced_count': 1, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "kidney", "side": "left", "value": 34.0, "rank": 1, "must_report": true}, {"meridian": "spleen", "side": "left", "value": 35.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_11_side_bias_4.json

**测试名称**: 左右偏向测试 - 4条经络左低: 触发头部供血关注, C=3.5
**状态**: 成功
**响应时间**: 0.34 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 84 | None ⚠️ |
| problem_index | 14.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 6.0, 'side_bias_index': 3.5, 'trend_index': 2.0, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 4, 'right_low_count': 0, 'balanced_count': 2, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'stable_balanced', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "left", "value": 38.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_12_side_bias_5.json

**测试名称**: 左右偏向测试 - 5条经络右低: 触发心脏方向关注, C=5
**状态**: 成功
**响应时间**: 0.21 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 82 | None ⚠️ |
| problem_index | 18.0 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 7.5, 'side_bias_index': 5.0, 'trend_index': 2.5, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 0, 'right_low_count': 5, 'balanced_count': 1, 'result': 'heart_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'stable_balanced', 'bladder_trend': 'stable_right_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "right", "value": 38.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "left", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_13_side_bias_6.json

**测试名称**: 左右偏向测试 - 6条经络全部左低: C=6,严重偏侧
**状态**: 成功
**响应时间**: 0.15 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 80 | None ⚠️ |
| problem_index | 21.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 1.0, 'temperature_difference_index': 9.0, 'side_bias_index': 6.0, 'trend_index': 3.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 6, 'right_low_count': 0, 'balanced_count': 0, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "left", "value": 38.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_14_cervical_opposite.json

**测试名称**: 颈椎判断测试 - 肾左低+膀胱右低: 相反低→颈椎问题
**状态**: 成功
**响应时间**: 0.19 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 86 | None ⚠️ |
| problem_index | 9.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 3.0, 'side_bias_index': 0.0, 'trend_index': 1.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 1, 'right_low_count': 1, 'balanced_count': 4, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'cervical', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_right_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "right", "value": 38.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "left", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_15_cervical_lumbar_cross.json

**测试名称**: 颈椎腰椎测试 - 肾交叉+膀胱任意: 任意一条交叉→颈椎和腰椎同时存在
**状态**: 成功
**响应时间**: 0.92 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 86 | None ⚠️ |
| problem_index | 10.2 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 3.0, 'side_bias_index': 0.0, 'trend_index': 1.7, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 1, 'right_low_count': 1, 'balanced_count': 4, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'cervical_and_lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'cross'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "right", "value": 38.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "left", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_16_gender_male.json

**测试名称**: 性别过滤测试 - 男性: 不能出现女性专属表达
**状态**: 成功
**响应时间**: 0.71 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 80 | None ⚠️ |
| problem_index | 20.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 7.5, 'side_bias_index': 5.0, 'trend_index': 2.5, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 5, 'right_low_count': 0, 'balanced_count': 1, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "left", "value": 38.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_17_gender_female.json

**测试名称**: 性别过滤测试 - 女性: 不能出现男性专属表达
**状态**: 成功
**响应时间**: 1.45 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 80 | None ⚠️ |
| problem_index | 20.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 7.5, 'side_bias_index': 5.0, 'trend_index': 2.5, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 5, 'right_low_count': 0, 'balanced_count': 1, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "left", "value": 38.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_18_gender_unknown.json

**测试名称**: 性别过滤测试 - 未知: 只保留中性表达
**状态**: 成功
**响应时间**: 0.15 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 80 | None ⚠️ |
| problem_index | 20.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 7.5, 'side_bias_index': 5.0, 'trend_index': 2.5, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 5, 'right_low_count': 0, 'balanced_count': 1, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "left", "value": 38.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_19_retest_0_2_days.json

**测试名称**: 复测测试 - 使用0-2天: 无使用天数加分,无保护
**状态**: 成功
**响应时间**: 0.18 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 77 | None ⚠️ |
| problem_index | 26.0 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 11.5, 'side_bias_index': 6.0, 'trend_index': 3.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 6, 'right_low_count': 0, 'balanced_count': 0, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "left", "value": 37.0, "rank": 1, "must_report": true}, {"meridian": "liver", "side": "left", "value": 38.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_20_retest_3_6_days.json

**测试名称**: 复测测试 - 使用3-6天: usage_bonus=1,保护为max(本次,上次-2)
**状态**: 成功
**响应时间**: 0.12 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 78 | None ⚠️ |
| problem_index | 26.0 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 11.5, 'side_bias_index': 6.0, 'trend_index': 3.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 6, 'right_low_count': 0, 'balanced_count': 0, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "left", "value": 37.0, "rank": 1, "must_report": true}, {"meridian": "liver", "side": "left", "value": 38.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_21_retest_7_13_days.json

**测试名称**: 复测测试 - 使用7-13天: usage_bonus=2,保护为max(本次,上次)
**状态**: 成功
**响应时间**: 0.17 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 79 | None ⚠️ |
| problem_index | 26.0 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 11.5, 'side_bias_index': 6.0, 'trend_index': 3.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 6, 'right_low_count': 0, 'balanced_count': 0, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "left", "value": 37.0, "rank": 1, "must_report": true}, {"meridian": "liver", "side": "left", "value": 38.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_22_retest_14_29_days_low.json

**测试名称**: 复测测试 - 使用14-29天且上次<88: usage_bonus=3,保护为max(本次,上次+1)
**状态**: 成功
**响应时间**: 0.15 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 80 | None ⚠️ |
| problem_index | 26.0 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 11.5, 'side_bias_index': 6.0, 'trend_index': 3.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 6, 'right_low_count': 0, 'balanced_count': 0, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "left", "value": 37.0, "rank": 1, "must_report": true}, {"meridian": "liver", "side": "left", "value": 38.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_23_retest_14_29_days_high.json

**测试名称**: 复测测试 - 使用14-29天且上次>=88: usage_bonus=3,保护为max(本次,上次)
**状态**: 成功
**响应时间**: 0.22 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 95 | None ⚠️ |
| problem_index | 0.0 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 0.0, 'temperature_difference_index': 0.0, 'side_bias_index': 0.0, 'trend_index': 0.0, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 0, 'right_low_count': 0, 'balanced_count': 6, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'stable_balanced', 'bladder_trend': 'stable_balanced'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "left", "value": 40.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_24_retest_30_plus_days.json

**测试名称**: 复测测试 - 使用30天及以上且上次<90: usage_bonus=4,保护为max(本次,上次+2)
**状态**: 成功
**响应时间**: 0.17 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 81 | None ⚠️ |
| problem_index | 26.0 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 11.5, 'side_bias_index': 6.0, 'trend_index': 3.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 6, 'right_low_count': 0, 'balanced_count': 0, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "left", "value": 37.0, "rank": 1, "must_report": true}, {"meridian": "liver", "side": "left", "value": 38.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_25_retest_improvement.json

**测试名称**: 复测测试 - 数据改善: ΔI>0时improvement_bonus=min(3, 0.3*ΔI)
**状态**: 成功
**响应时间**: 0.17 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 95 | None ⚠️ |
| problem_index | 0.0 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 0.0, 'temperature_difference_index': 0.0, 'side_bias_index': 0.0, 'trend_index': 0.0, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 0, 'right_low_count': 0, 'balanced_count': 6, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'stable_balanced', 'bladder_trend': 'stable_balanced'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "left", "value": 40.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_26_low_temp_index_max.json

**测试名称**: 低温指数测试 - 低温差距>3℃: A=6,最高档
**状态**: 成功
**响应时间**: 0.15 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 88 | None ⚠️ |
| problem_index | 6.0 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 6.0, 'temperature_difference_index': 0.0, 'side_bias_index': 0.0, 'trend_index': 0.0, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 0, 'right_low_count': 0, 'balanced_count': 6, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'stable_balanced', 'bladder_trend': 'stable_balanced'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "left", "value": 40.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "left", "value": 44.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_27_diff_change_improved.json

**测试名称**: 温差变化测试 - improved: 温差缩小>0.2℃
**状态**: 成功
**响应时间**: 0.12 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 89 | None ⚠️ |
| problem_index | 1.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 0.0, 'temperature_difference_index': 1.0, 'side_bias_index': 0.0, 'trend_index': 0.5, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 1, 'right_low_count': 0, 'balanced_count': 5, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'stable_balanced', 'bladder_trend': 'stable_balanced'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "left", "value": 39.0, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "right", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_28_diff_change_worsened.json

**测试名称**: 温差变化测试 - worsened: 温差变大>0.2℃
**状态**: 成功
**响应时间**: 0.16 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 88 | None ⚠️ |
| problem_index | 5.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 1.0, 'temperature_difference_index': 4.0, 'side_bias_index': 0.0, 'trend_index': 0.5, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 1, 'right_low_count': 0, 'balanced_count': 5, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'stable_balanced', 'bladder_trend': 'stable_balanced'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "stomach", "side": "left", "value": 38.0, "rank": 1, "must_report": true}, {"meridian": "gallbladder", "side": "left", "value": 40.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_29_realistic_mild.json

**测试名称**: 真实场景 - 轻度亚健康: 1-2条经络轻度异常，温差0.3-0.5
**状态**: 成功
**响应时间**: 0.15 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 89 | None ⚠️ |
| problem_index | 1.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 0.0, 'temperature_difference_index': 0.5, 'side_bias_index': 0.0, 'trend_index': 1.0, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 2, 'right_low_count': 0, 'balanced_count': 4, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'stable_balanced', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "left", "value": 39.5, "rank": 1, "must_report": true}, {"meridian": "stomach", "side": "left", "value": 39.8, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_30_realistic_moderate.json

**测试名称**: 真实场景 - 中度失衡: 4-5条经络异常，有明显低温点和温差
**状态**: 成功
**响应时间**: 0.20 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 76 | None ⚠️ |
| problem_index | 26.5 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 5.0, 'temperature_difference_index': 10.0, 'side_bias_index': 6.0, 'trend_index': 3.0, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 6, 'right_low_count': 0, 'balanced_count': 0, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "left", "value": 37.0, "rank": 1, "must_report": true}, {"meridian": "spleen", "side": "left", "value": 38.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_31_bladder_lowest.json

**测试名称**: 膀胱经最低点场景: 膀胱经温度最低，需结合肾经分析
**状态**: 成功
**响应时间**: 0.16 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 83 | None ⚠️ |
| problem_index | 14.9 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 5.0, 'temperature_difference_index': 5.0, 'side_bias_index': 0.0, 'trend_index': 2.4000000000000004, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 3, 'right_low_count': 0, 'balanced_count': 3, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "left", "value": 37.0, "rank": 1, "must_report": true}, {"meridian": "kidney", "side": "left", "value": 38.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### test_32_kidney_cross.json

**测试名称**: 肾经交叉场景: 肾经交叉提示结石/囊肿/手术史风险
**状态**: 成功
**响应时间**: 0.16 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 84 | None ⚠️ |
| problem_index | 13.1 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 3.0, 'temperature_difference_index': 4.5, 'side_bias_index': 0.0, 'trend_index': 3.1, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 2, 'right_low_count': 1, 'balanced_count': 3, 'result': 'none'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'cervical_and_lumbar', 'kidney_trend': 'cross', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "kidney", "side": "right", "value": 38.0, "rank": 1, "must_report": true}, {"meridian": "bladder", "side": "left", "value": 39.0, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### case_01_first_test.json

**测试名称**: case_01_first_test.json
**状态**: 成功
**响应时间**: 0.18 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 77 | None ⚠️ |
| problem_index | 24.9 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 5.0, 'temperature_difference_index': 8.5, 'side_bias_index': 5.0, 'trend_index': 3.9000000000000004, 'combo_index': 2.5} | None ⚠️ |
| side_bias_summary | {'left_low_count': 5, 'right_low_count': 0, 'balanced_count': 1, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'lumbar', 'kidney_trend': 'stable_left_low', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "left", "value": 37.9, "rank": 1, "must_report": true}, {"meridian": "spleen", "side": "left", "value": 39.1, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---

### case_02_retest.json

**测试名称**: case_02_retest.json
**状态**: 成功
**响应时间**: 0.23 ms

**关键字段**:

| 字段 | 实际值 | 期望值 |
|------|--------|--------|
| score | 89 | None ⚠️ |
| problem_index | 14.7 | None ⚠️ |
| problem_index_detail | {'low_temperature_index': 1.0, 'temperature_difference_index': 5.0, 'side_bias_index': 5.0, 'trend_index': 3.7, 'combo_index': 0.0} | None ⚠️ |
| side_bias_summary | {'left_low_count': 5, 'right_low_count': 0, 'balanced_count': 1, 'result': 'head_blood_supply_attention'} | None ⚠️ |
| cervical_lumbar_result | {'result': 'none', 'kidney_trend': 'potential_symptom', 'bladder_trend': 'stable_left_low'} | None ⚠️ |
| lowest_points | {"selected": [{"meridian": "bladder", "side": "left", "value": 40.0, "rank": 1, "must_report": true}, {"meridian": "liver", "side": "right", "value": 40.2, "rank": 2, "must_report": true}], "tie_candidates": []} | - |

---
