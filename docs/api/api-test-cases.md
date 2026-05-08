# TCM v3 API 测试用例文档

> **说明**: 本文档列出所有v3引擎测试用例索引
> **引擎版本**: hybrid v3.0 (规则引擎 + DeepSeek LLM)
> **测试用例总数**: 38个（首测26个 + 复测12个）
> **生成时间**: 2026-05-07

**测试输入文件**: [`fixtures/v3/*.json`](../../fixtures/v3/)
**测试结果记录**: [`docs/v3/testing/actual-results/*_result.json`](../../docs/v3/testing/actual-results/)

**运行测试**:
```bash
# 本地测试
python3 tests/run_v3_tests.py --mode rule        # 纯规则引擎
python3 tests/run_v3_tests.py --mode agent       # Hybrid模式

# 测试API服务
python3 tests/run_v3_tests.py --port 18790
```

---

## 测试用例索引

### 首测用例

| 编号 | 文件名 | 场景 | 分数 | 问题指数 |
|------|--------|------|------|----------|
| 1 | [case_01_first_test](case_01_first_test) | PRD标准示例 | 77 | 24.9 |
| 2 | [test_01_excellent_score](test_01_excellent_score) | 健康优秀 | 89 | 0.0 |
| 3 | [test_02_mild_imbalance](test_02_mild_imbalance) | 轻度失衡 | 89 | 1.5 |
| 4 | [test_03_moderate_imbalance](test_03_moderate_imbalance) | 中度失衡 | 76 | 26.0 |
| 5 | [test_04_significant_imbalance](test_04_significant_imbalance) | 明显失衡 | 75 | 28.0 |
| 6 | [test_05_trend_stable_left_low](test_05_trend_stable_left_low) | 趋势-左低 | 74 | 28.5 |
| 7 | [test_06_trend_stable_right_low](test_06_trend_stable_right_low) | 趋势-右低 | 74 | 28.5 |
| 8 | [test_07_trend_cross](test_07_trend_cross) | 趋势-交叉 | 77 | 25.0 |
| 9 | [test_08_trend_potential_symptom](test_08_trend_potential_symptom) | 趋势-潜在症状 | 89 | 3.3 |
| 10 | [test_09_trend_fast_response](test_09_trend_fast_response) | 趋势-快速恢复 | 89 | 0.3 |
| 11 | [test_10_diff_levels](test_10_diff_levels) | 温差等级 | 75 | 28.0 |
| 12 | [test_11_side_bias_4](test_11_side_bias_4) | 偏侧4条 | 84 | 14.5 |
| 13 | [test_12_side_bias_5](test_12_side_bias_5) | 偏侧5条 | 82 | 18.0 |
| 14 | [test_13_side_bias_6](test_13_side_bias_6) | 偏侧6条 | 80 | 21.5 |
| 15 | [test_14_cervical_opposite](test_14_cervical_opposite) | 颈椎-相反低 | 86 | 9.5 |
| 16 | [test_15_cervical_lumbar_cross](test_15_cervical_lumbar_cross) | 交叉=颈+腰 | 86 | 10.2 |
| 17 | [test_16_gender_male](test_16_gender_male) | 性别-男性 | 80 | 20.5 |
| 18 | [test_17_gender_female](test_17_gender_female) | 性别-女性 | 80 | 20.5 |
| 19 | [test_18_gender_unknown](test_18_gender_unknown) | 性别-未知 | 80 | 20.5 |
| 20 | [test_26_low_temp_index_max](test_26_low_temp_index_max) | 低温指数最大 | 88 | 6.0 |
| 21 | [test_27_diff_change_improved](test_27_diff_change_improved) | 温差改善 | 89 | 1.5 |
| 22 | [test_28_diff_change_worsened](test_28_diff_change_worsened) | 温差恶化 | 88 | 5.5 |
| 23 | [test_29_realistic_mild](test_29_realistic_mild) | 真实-轻度 | 89 | 1.5 |
| 24 | [test_30_realistic_moderate](test_30_realistic_moderate) | 真实-中度 | 76 | 26.5 |
| 25 | [test_31_bladder_lowest](test_31_bladder_lowest) | 膀胱最低 | 83 | 14.9 |
| 26 | [test_32_kidney_cross](test_32_kidney_cross) | 肾交叉 | 84 | 13.1 |

### 复测用例

| 编号 | 文件名 | 场景 | 分数 | 问题指数 |
|------|--------|------|------|----------|
| 1 | [case_02_retest](case_02_retest) | PRD复测示例 | 89 | 14.7 |
| 2 | [test_19_retest_0_2_days](test_19_retest_0_2_days) | 0-2天 | 77 | 26.0 |
| 3 | [test_20_retest_3_6_days](test_20_retest_3_6_days) | 3-6天 | 78 | 26.0 |
| 4 | [test_21_retest_7_13_days](test_21_retest_7_13_days) | 7-13天 | 79 | 26.0 |
| 5 | [test_22_retest_14_29_days_low](test_22_retest_14_29_days_low) | 14-29天(<88) | 80 | 26.0 |
| 6 | [test_23_retest_14_29_days_high](test_23_retest_14_29_days_high) | 14-29天(≥88)→95分 | 95 | 0.0 |
| 7 | [test_24_retest_30_plus_days](test_24_retest_30_plus_days) | 30天+ | 81 | 26.0 |
| 8 | [test_25_retest_improvement](test_25_retest_improvement) | 数据改善→95分 | 95 | 0.0 |
| 9 | [test_33_retest_92_score](test_33_retest_92_score) | 92分-中等高分 | 93 | 1.8 |
| 10 | [test_34_retest_91_score](test_34_retest_91_score) | 91分-高分起步 | 94 | 1.8 |
| 11 | [test_35_retest_93_score](test_35_retest_93_score) | 93分-接近封顶 | 95 | 1.8 |
| 12 | [test_36_retest_94_score](test_36_retest_94_score) | 94分-保护机制 | 94 | 1.8 |

---

## 文件引用

### 首测用例

| 用例 | 输入文件 | 结果文件 |
|------|----------|----------|
| case_01_first_test | [`fixtures/v3/case_01_first_test.json`](../../fixtures/v3/case_01_first_test.json) | [`actual-results/case_01_first_test_result.json`](../../docs/v3/testing/actual-results/case_01_first_test_result.json) |
| test_01_excellent_score | [`fixtures/v3/test_01_excellent_score.json`](../../fixtures/v3/test_01_excellent_score.json) | [`actual-results/test_01_excellent_score_result.json`](../../docs/v3/testing/actual-results/test_01_excellent_score_result.json) |
| test_02_mild_imbalance | [`fixtures/v3/test_02_mild_imbalance.json`](../../fixtures/v3/test_02_mild_imbalance.json) | [`actual-results/test_02_mild_imbalance_result.json`](../../docs/v3/testing/actual-results/test_02_mild_imbalance_result.json) |
| test_03_moderate_imbalance | [`fixtures/v3/test_03_moderate_imbalance.json`](../../fixtures/v3/test_03_moderate_imbalance.json) | [`actual-results/test_03_moderate_imbalance_result.json`](../../docs/v3/testing/actual-results/test_03_moderate_imbalance_result.json) |
| test_04_significant_imbalance | [`fixtures/v3/test_04_significant_imbalance.json`](../../fixtures/v3/test_04_significant_imbalance.json) | [`actual-results/test_04_significant_imbalance_result.json`](../../docs/v3/testing/actual-results/test_04_significant_imbalance_result.json) |
| test_05_trend_stable_left_low | [`fixtures/v3/test_05_trend_stable_left_low.json`](../../fixtures/v3/test_05_trend_stable_left_low.json) | [`actual-results/test_05_trend_stable_left_low_result.json`](../../docs/v3/testing/actual-results/test_05_trend_stable_left_low_result.json) |
| test_06_trend_stable_right_low | [`fixtures/v3/test_06_trend_stable_right_low.json`](../../fixtures/v3/test_06_trend_stable_right_low.json) | [`actual-results/test_06_trend_stable_right_low_result.json`](../../docs/v3/testing/actual-results/test_06_trend_stable_right_low_result.json) |
| test_07_trend_cross | [`fixtures/v3/test_07_trend_cross.json`](../../fixtures/v3/test_07_trend_cross.json) | [`actual-results/test_07_trend_cross_result.json`](../../docs/v3/testing/actual-results/test_07_trend_cross_result.json) |
| test_08_trend_potential_symptom | [`fixtures/v3/test_08_trend_potential_symptom.json`](../../fixtures/v3/test_08_trend_potential_symptom.json) | [`actual-results/test_08_trend_potential_symptom_result.json`](../../docs/v3/testing/actual-results/test_08_trend_potential_symptom_result.json) |
| test_09_trend_fast_response | [`fixtures/v3/test_09_trend_fast_response.json`](../../fixtures/v3/test_09_trend_fast_response.json) | [`actual-results/test_09_trend_fast_response_result.json`](../../docs/v3/testing/actual-results/test_09_trend_fast_response_result.json) |
| test_10_diff_levels | [`fixtures/v3/test_10_diff_levels.json`](../../fixtures/v3/test_10_diff_levels.json) | [`actual-results/test_10_diff_levels_result.json`](../../docs/v3/testing/actual-results/test_10_diff_levels_result.json) |
| test_11_side_bias_4 | [`fixtures/v3/test_11_side_bias_4.json`](../../fixtures/v3/test_11_side_bias_4.json) | [`actual-results/test_11_side_bias_4_result.json`](../../docs/v3/testing/actual-results/test_11_side_bias_4_result.json) |
| test_12_side_bias_5 | [`fixtures/v3/test_12_side_bias_5.json`](../../fixtures/v3/test_12_side_bias_5.json) | [`actual-results/test_12_side_bias_5_result.json`](../../docs/v3/testing/actual-results/test_12_side_bias_5_result.json) |
| test_13_side_bias_6 | [`fixtures/v3/test_13_side_bias_6.json`](../../fixtures/v3/test_13_side_bias_6.json) | [`actual-results/test_13_side_bias_6_result.json`](../../docs/v3/testing/actual-results/test_13_side_bias_6_result.json) |
| test_14_cervical_opposite | [`fixtures/v3/test_14_cervical_opposite.json`](../../fixtures/v3/test_14_cervical_opposite.json) | [`actual-results/test_14_cervical_opposite_result.json`](../../docs/v3/testing/actual-results/test_14_cervical_opposite_result.json) |
| test_15_cervical_lumbar_cross | [`fixtures/v3/test_15_cervical_lumbar_cross.json`](../../fixtures/v3/test_15_cervical_lumbar_cross.json) | [`actual-results/test_15_cervical_lumbar_cross_result.json`](../../docs/v3/testing/actual-results/test_15_cervical_lumbar_cross_result.json) |
| test_16_gender_male | [`fixtures/v3/test_16_gender_male.json`](../../fixtures/v3/test_16_gender_male.json) | [`actual-results/test_16_gender_male_result.json`](../../docs/v3/testing/actual-results/test_16_gender_male_result.json) |
| test_17_gender_female | [`fixtures/v3/test_17_gender_female.json`](../../fixtures/v3/test_17_gender_female.json) | [`actual-results/test_17_gender_female_result.json`](../../docs/v3/testing/actual-results/test_17_gender_female_result.json) |
| test_18_gender_unknown | [`fixtures/v3/test_18_gender_unknown.json`](../../fixtures/v3/test_18_gender_unknown.json) | [`actual-results/test_18_gender_unknown_result.json`](../../docs/v3/testing/actual-results/test_18_gender_unknown_result.json) |
| test_26_low_temp_index_max | [`fixtures/v3/test_26_low_temp_index_max.json`](../../fixtures/v3/test_26_low_temp_index_max.json) | [`actual-results/test_26_low_temp_index_max_result.json`](../../docs/v3/testing/actual-results/test_26_low_temp_index_max_result.json) |
| test_27_diff_change_improved | [`fixtures/v3/test_27_diff_change_improved.json`](../../fixtures/v3/test_27_diff_change_improved.json) | [`actual-results/test_27_diff_change_improved_result.json`](../../docs/v3/testing/actual-results/test_27_diff_change_improved_result.json) |
| test_28_diff_change_worsened | [`fixtures/v3/test_28_diff_change_worsened.json`](../../fixtures/v3/test_28_diff_change_worsened.json) | [`actual-results/test_28_diff_change_worsened_result.json`](../../docs/v3/testing/actual-results/test_28_diff_change_worsened_result.json) |
| test_29_realistic_mild | [`fixtures/v3/test_29_realistic_mild.json`](../../fixtures/v3/test_29_realistic_mild.json) | [`actual-results/test_29_realistic_mild_result.json`](../../docs/v3/testing/actual-results/test_29_realistic_mild_result.json) |
| test_30_realistic_moderate | [`fixtures/v3/test_30_realistic_moderate.json`](../../fixtures/v3/test_30_realistic_moderate.json) | [`actual-results/test_30_realistic_moderate_result.json`](../../docs/v3/testing/actual-results/test_30_realistic_moderate_result.json) |
| test_31_bladder_lowest | [`fixtures/v3/test_31_bladder_lowest.json`](../../fixtures/v3/test_31_bladder_lowest.json) | [`actual-results/test_31_bladder_lowest_result.json`](../../docs/v3/testing/actual-results/test_31_bladder_lowest_result.json) |
| test_32_kidney_cross | [`fixtures/v3/test_32_kidney_cross.json`](../../fixtures/v3/test_32_kidney_cross.json) | [`actual-results/test_32_kidney_cross_result.json`](../../docs/v3/testing/actual-results/test_32_kidney_cross_result.json) |

### 复测用例

| 用例 | 输入文件 | 结果文件 |
|------|----------|----------|
| case_02_retest | [`fixtures/v3/case_02_retest.json`](../../fixtures/v3/case_02_retest.json) | [`actual-results/case_02_retest_result.json`](../../docs/v3/testing/actual-results/case_02_retest_result.json) |
| test_19_retest_0_2_days | [`fixtures/v3/test_19_retest_0_2_days.json`](../../fixtures/v3/test_19_retest_0_2_days.json) | [`actual-results/test_19_retest_0_2_days_result.json`](../../docs/v3/testing/actual-results/test_19_retest_0_2_days_result.json) |
| test_20_retest_3_6_days | [`fixtures/v3/test_20_retest_3_6_days.json`](../../fixtures/v3/test_20_retest_3_6_days.json) | [`actual-results/test_20_retest_3_6_days_result.json`](../../docs/v3/testing/actual-results/test_20_retest_3_6_days_result.json) |
| test_21_retest_7_13_days | [`fixtures/v3/test_21_retest_7_13_days.json`](../../fixtures/v3/test_21_retest_7_13_days.json) | [`actual-results/test_21_retest_7_13_days_result.json`](../../docs/v3/testing/actual-results/test_21_retest_7_13_days_result.json) |
| test_22_retest_14_29_days_low | [`fixtures/v3/test_22_retest_14_29_days_low.json`](../../fixtures/v3/test_22_retest_14_29_days_low.json) | [`actual-results/test_22_retest_14_29_days_low_result.json`](../../docs/v3/testing/actual-results/test_22_retest_14_29_days_low_result.json) |
| test_23_retest_14_29_days_high | [`fixtures/v3/test_23_retest_14_29_days_high.json`](../../fixtures/v3/test_23_retest_14_29_days_high.json) | [`actual-results/test_23_retest_14_29_days_high_result.json`](../../docs/v3/testing/actual-results/test_23_retest_14_29_days_high_result.json) |
| test_24_retest_30_plus_days | [`fixtures/v3/test_24_retest_30_plus_days.json`](../../fixtures/v3/test_24_retest_30_plus_days.json) | [`actual-results/test_24_retest_30_plus_days_result.json`](../../docs/v3/testing/actual-results/test_24_retest_30_plus_days_result.json) |
| test_25_retest_improvement | [`fixtures/v3/test_25_retest_improvement.json`](../../fixtures/v3/test_25_retest_improvement.json) | [`actual-results/test_25_retest_improvement_result.json`](../../docs/v3/testing/actual-results/test_25_retest_improvement_result.json) |
| test_33_retest_92_score | [`fixtures/v3/test_33_retest_92_score.json`](../../fixtures/v3/test_33_retest_92_score.json) | [`actual-results/test_33_retest_92_score_result.json`](../../docs/v3/testing/actual-results/test_33_retest_92_score_result.json) |
| test_34_retest_91_score | [`fixtures/v3/test_34_retest_91_score.json`](../../fixtures/v3/test_34_retest_91_score.json) | [`actual-results/test_34_retest_91_score_result.json`](../../docs/v3/testing/actual-results/test_34_retest_91_score_result.json) |
| test_35_retest_93_score | [`fixtures/v3/test_35_retest_93_score.json`](../../fixtures/v3/test_35_retest_93_score.json) | [`actual-results/test_35_retest_93_score_result.json`](../../docs/v3/testing/actual-results/test_35_retest_93_score_result.json) |
| test_36_retest_94_score | [`fixtures/v3/test_36_retest_94_score.json`](../../fixtures/v3/test_36_retest_94_score.json) | [`actual-results/test_36_retest_94_score_result.json`](../../docs/v3/testing/actual-results/test_36_retest_94_score_result.json) |

---

## 结果汇总

完整汇总见: [`docs/v3/testing/actual-results/summary.md`](../../docs/v3/testing/actual-results/summary.md)

---

*最后更新: 2026-05-07*
