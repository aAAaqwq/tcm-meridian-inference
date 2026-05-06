# TCM v3 实际输出结果记录

**生成时间**: 2026-05-04

**后端版本**: v3.0

---

## 测试结果摘要

- 总测试数: 34
- 成功: 34
- 失败: 0

## 详细结果

| 测试文件 | 分数 | 问题指数 | A | B | C | D | E | 偏侧结果 | 颈椎/腰椎 |
|----------|------|----------|---|---|---|---|---|----------|----------|
| case_01_first_test.json | 77 | 24.9 | 5.0 | 8.5 | 5.0 | 3.9000000000000004 | 2.5 | head_blood_supply_attention | lumbar |
| case_02_retest.json | 89 | 14.7 | 1.0 | 5.0 | 5.0 | 3.7 | 0.0 | head_blood_supply_attention | none |
| test_01_excellent_score.json | 89 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | none | none |
| test_02_mild_imbalance.json | 89 | 1.5 | 0.0 | 0.5 | 0.0 | 1.0 | 0.0 | none | none |
| test_03_moderate_imbalance.jso | 76 | 26.0 | 3.0 | 11.5 | 6.0 | 3.0 | 2.5 | head_blood_supply_attention | lumbar |
| test_04_significant_imbalance. | 75 | 28.0 | 6.0 | 12.0 | 3.5 | 4.0 | 2.5 | heart_attention | cervical_and_lumbar |
| test_05_trend_stable_left_low. | 74 | 28.5 | 5.0 | 12.0 | 6.0 | 3.0 | 2.5 | head_blood_supply_attention | lumbar |
| test_06_trend_stable_right_low | 74 | 28.5 | 5.0 | 12.0 | 6.0 | 3.0 | 2.5 | heart_attention | lumbar |
| test_07_trend_cross.json | 77 | 25.0 | 3.0 | 9.5 | 6.0 | 4.0 | 2.5 | heart_attention | cervical_and_lumbar |
| test_08_trend_potential_sympto | 89 | 3.3 | 1.0 | 2.0 | 0.0 | 0.3 | 0.0 | none | none |
| test_09_trend_fast_response.js | 89 | 0.3 | 0.0 | 0.0 | 0.0 | 0.3 | 0.0 | none | none |
| test_10_diff_levels.json | 75 | 28.0 | 6.0 | 12.0 | 5.0 | 2.5 | 2.5 | head_blood_supply_attention | lumbar |
| test_11_side_bias_4.json | 84 | 14.5 | 3.0 | 6.0 | 3.5 | 2.0 | 0.0 | head_blood_supply_attention | none |
| test_12_side_bias_5.json | 82 | 18.0 | 3.0 | 7.5 | 5.0 | 2.5 | 0.0 | heart_attention | none |
| test_13_side_bias_6.json | 80 | 21.5 | 1.0 | 9.0 | 6.0 | 3.0 | 2.5 | head_blood_supply_attention | lumbar |
| test_14_cervical_opposite.json | 86 | 9.5 | 3.0 | 3.0 | 0.0 | 1.0 | 2.5 | none | cervical |
| test_15_cervical_lumbar_cross. | 86 | 10.2 | 3.0 | 3.0 | 0.0 | 1.7 | 2.5 | none | cervical_and_lumbar |
| test_16_gender_male.json | 80 | 20.5 | 3.0 | 7.5 | 5.0 | 2.5 | 2.5 | head_blood_supply_attention | lumbar |
| test_17_gender_female.json | 80 | 20.5 | 3.0 | 7.5 | 5.0 | 2.5 | 2.5 | head_blood_supply_attention | lumbar |
| test_18_gender_unknown.json | 80 | 20.5 | 3.0 | 7.5 | 5.0 | 2.5 | 2.5 | head_blood_supply_attention | lumbar |
| test_19_retest_0_2_days.json | 77 | 26.0 | 3.0 | 11.5 | 6.0 | 3.0 | 2.5 | head_blood_supply_attention | lumbar |
| test_20_retest_3_6_days.json | 78 | 26.0 | 3.0 | 11.5 | 6.0 | 3.0 | 2.5 | head_blood_supply_attention | lumbar |
| test_21_retest_7_13_days.json | 79 | 26.0 | 3.0 | 11.5 | 6.0 | 3.0 | 2.5 | head_blood_supply_attention | lumbar |
| test_22_retest_14_29_days_low. | 80 | 26.0 | 3.0 | 11.5 | 6.0 | 3.0 | 2.5 | head_blood_supply_attention | lumbar |
| test_23_retest_14_29_days_high | 95 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | none | none |
| test_24_retest_30_plus_days.js | 81 | 26.0 | 3.0 | 11.5 | 6.0 | 3.0 | 2.5 | head_blood_supply_attention | lumbar |
| test_25_retest_improvement.jso | 95 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | none | none |
| test_26_low_temp_index_max.jso | 88 | 6.0 | 6.0 | 0.0 | 0.0 | 0.0 | 0.0 | none | none |
| test_27_diff_change_improved.j | 89 | 1.5 | 0.0 | 1.0 | 0.0 | 0.5 | 0.0 | none | none |
| test_28_diff_change_worsened.j | 88 | 5.5 | 1.0 | 4.0 | 0.0 | 0.5 | 0.0 | none | none |
| test_29_realistic_mild.json | 89 | 1.5 | 0.0 | 0.5 | 0.0 | 1.0 | 0.0 | none | none |
| test_30_realistic_moderate.jso | 76 | 26.5 | 5.0 | 10.0 | 6.0 | 3.0 | 2.5 | head_blood_supply_attention | lumbar |
| test_31_bladder_lowest.json | 83 | 14.9 | 5.0 | 5.0 | 0.0 | 2.4000000000000004 | 2.5 | none | lumbar |
| test_32_kidney_cross.json | 84 | 13.1 | 3.0 | 4.5 | 0.0 | 3.1 | 2.5 | none | cervical_and_lumbar |

## 完整输出文件

- [case_01_first_test.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/case_01_first_test-actual.json)
- [case_02_retest.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/case_02_retest-actual.json)
- [test_01_excellent_score.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_01_excellent_score-actual.json)
- [test_02_mild_imbalance.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_02_mild_imbalance-actual.json)
- [test_03_moderate_imbalance.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_03_moderate_imbalance-actual.json)
- [test_04_significant_imbalance.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_04_significant_imbalance-actual.json)
- [test_05_trend_stable_left_low.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_05_trend_stable_left_low-actual.json)
- [test_06_trend_stable_right_low.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_06_trend_stable_right_low-actual.json)
- [test_07_trend_cross.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_07_trend_cross-actual.json)
- [test_08_trend_potential_symptom.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_08_trend_potential_symptom-actual.json)
- [test_09_trend_fast_response.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_09_trend_fast_response-actual.json)
- [test_10_diff_levels.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_10_diff_levels-actual.json)
- [test_11_side_bias_4.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_11_side_bias_4-actual.json)
- [test_12_side_bias_5.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_12_side_bias_5-actual.json)
- [test_13_side_bias_6.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_13_side_bias_6-actual.json)
- [test_14_cervical_opposite.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_14_cervical_opposite-actual.json)
- [test_15_cervical_lumbar_cross.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_15_cervical_lumbar_cross-actual.json)
- [test_16_gender_male.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_16_gender_male-actual.json)
- [test_17_gender_female.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_17_gender_female-actual.json)
- [test_18_gender_unknown.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_18_gender_unknown-actual.json)
- [test_19_retest_0_2_days.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_19_retest_0_2_days-actual.json)
- [test_20_retest_3_6_days.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_20_retest_3_6_days-actual.json)
- [test_21_retest_7_13_days.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_21_retest_7_13_days-actual.json)
- [test_22_retest_14_29_days_low.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_22_retest_14_29_days_low-actual.json)
- [test_23_retest_14_29_days_high.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_23_retest_14_29_days_high-actual.json)
- [test_24_retest_30_plus_days.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_24_retest_30_plus_days-actual.json)
- [test_25_retest_improvement.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_25_retest_improvement-actual.json)
- [test_26_low_temp_index_max.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_26_low_temp_index_max-actual.json)
- [test_27_diff_change_improved.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_27_diff_change_improved-actual.json)
- [test_28_diff_change_worsened.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_28_diff_change_worsened-actual.json)
- [test_29_realistic_mild.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_29_realistic_mild-actual.json)
- [test_30_realistic_moderate.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_30_realistic_moderate-actual.json)
- [test_31_bladder_lowest.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_31_bladder_lowest-actual.json)
- [test_32_kidney_cross.json](/home/aa/clawd/projects/tcm-meridian-inference-mvp/docs/v3/testing/actual-results/test_32_kidney_cross-actual.json)
