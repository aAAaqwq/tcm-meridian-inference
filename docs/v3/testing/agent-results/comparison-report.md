# TCM v3 Agent 模式实际输出结果

**生成时间**: 2026-05-05

**后端版本**: v3.0 (Agent 模式 - 规则引擎 + DeepSeek LLM)

---

## 测试结果摘要

- 总测试数: 34
- 成功: 34
- 失败: 0

## 详细结果

| 测试文件 | 分数 | 问题指数 | 偏侧结果 | 颈椎/腰椎 | LLM摘要 |
|----------|------|----------|----------|----------|----------|
| case_01_first_test.json | 77 | 24.9 | head_blood_supply_attention | lumbar | 膀胱经与脾经需重点关注 |
| case_02_retest.json | 89 | 14.7 | head_blood_supply_attention | none | 膀胱与肝经需关注 |
| test_01_excellent_score.j | 89 | 0.0 | none | none | 胃经状态需关注 |
| test_02_mild_imbalance.js | 89 | 1.5 | none | none | 脾经肝经需温和调理 |
| test_03_moderate_imbalanc | 76 | 26.0 | head_blood_supply_attention | lumbar | 经络失衡，关注腰背与代谢 |
| test_04_significant_imbal | 75 | 28.0 | heart_attention | cervical_and_lumbar | 经络全面失衡，需重点调理 |
| test_05_trend_stable_left | 74 | 28.5 | head_blood_supply_attention | lumbar | 经络失衡，肾经膀胱经需重点关注 |
| test_06_trend_stable_righ | 74 | 28.5 | heart_attention | lumbar | 整体偏右失衡，肾与膀胱需关注 |
| test_07_trend_cross.json | 77 | 25.0 | heart_attention | cervical_and_lumbar | 气血失衡，关注脾胃与膀胱 |
| test_08_trend_potential_s | 89 | 3.3 | none | none | 胃经需关注，其他均平衡 |
| test_09_trend_fast_respon | 89 | 0.3 | none | none | 胃经改善明显 |
| test_10_diff_levels.json | 75 | 28.0 | head_blood_supply_attention | lumbar | 肾脾失衡，腰椎需关注 |
| test_11_side_bias_4.json | 84 | 14.5 | head_blood_supply_attention | none | 脾胃与代谢需关注 |
| test_12_side_bias_5.json | 82 | 18.0 | heart_attention | none | 右侧经络偏弱需关注 |
| test_13_side_bias_6.json | 80 | 21.5 | head_blood_supply_attention | lumbar | 整体偏左，关注头部与腰椎 |
| test_14_cervical_opposite | 86 | 9.5 | none | cervical | 颈椎与膀胱经需关注 |
| test_15_cervical_lumbar_c | 86 | 10.2 | none | cervical_and_lumbar | 膀胱经与肾经失衡需注意 |
| test_16_gender_male.json | 80 | 20.5 | head_blood_supply_attention | lumbar | 胃经与整体偏左需关注 |
| test_17_gender_female.jso | 80 | 20.5 | head_blood_supply_attention | lumbar | 胃经与多经络失衡需关注 |
| test_18_gender_unknown.js | 80 | 20.5 | head_blood_supply_attention | lumbar | 脾胃与腰部需重点关注 |
| test_19_retest_0_2_days.j | 77 | 26.0 | head_blood_supply_attention | lumbar | 关注膀胱与肝经，腰椎需重视 |
| test_20_retest_3_6_days.j | 78 | 26.0 | head_blood_supply_attention | lumbar | 膀胱经与肝经需重点调理 |
| test_21_retest_7_13_days. | 79 | 26.0 | head_blood_supply_attention | lumbar | 膀胱与肝经需重点关注 |
| test_22_retest_14_29_days | 80 | 26.0 | head_blood_supply_attention | lumbar | 膀胱经与肝经需重点关注 |
| test_23_retest_14_29_days | 95 | 0.0 | none | none | 胃经需关注，整体平衡 |
| test_24_retest_30_plus_da | 81 | 26.0 | head_blood_supply_attention | lumbar | 腰部与代谢需重点关注 |
| test_25_retest_improvemen | 95 | 0.0 | none | none | 消化系统需持续关注 |
| test_26_low_temp_index_ma | 88 | 6.0 | none | none | 膀胱经与胃经需留意 |
| test_27_diff_change_impro | 89 | 1.5 | none | none | 胃经需关注 |
| test_28_diff_change_worse | 88 | 5.5 | none | none | 胃经胆经需关注 |
| test_29_realistic_mild.js | 89 | 1.5 | none | none | 膀胱与胃经需关注 |
| test_30_realistic_moderat | 76 | 26.5 | head_blood_supply_attention | lumbar | 消化与脊柱健康需关注 |
| test_31_bladder_lowest.js | 83 | 14.9 | none | lumbar | 需关注腰部与代谢平衡 |
| test_32_kidney_cross.json | 84 | 13.1 | none | cervical_and_lumbar | 肾与膀胱功能需关注 |

## Storefront 示例

### case_01_first_test.json

**Headline**: 膀胱经与脾经需重点关注

**Explanation**: 本次检测基于足部经络温度分析，不等同于医疗诊断。您的综合健康分77分，提示身体存在一些需要关注的失衡点。...

**Talk Track**: 您的膀胱经和脾经温度差异较大，可能与肩颈腰部和消化代谢有关。...

---

### case_02_retest.json

**Headline**: 膀胱与肝经需关注

**Explanation**: 本次检测结果显示您身体有多处失衡，尤其是膀胱经和肝经，需结合日常调理改善。请注意，本报告基于经络温度分析，不等同于医疗诊断。...

**Talk Track**: 您的整体健康分从77分提升到了89分，说明我们之前做的调理方向是对的，您也配合得非常好。...

---

### test_01_excellent_score.json

**Headline**: 胃经状态需关注

**Explanation**: 本次检测基于足部经络温度分析，不等同于医疗诊断，旨在提供健康参考。您目前整体经络平衡，但胃经相对较低，提示消化系统可能需要调理。...

**Talk Track**: 您看，这次检测您的综合健康分是89分，非常不错，说明整体状态良好。...

---


## 完整输出文件

- [case_01_first_test.json](docs/v3/testing/agent-results/case_01_first_test-agent.json)
- [case_02_retest.json](docs/v3/testing/agent-results/case_02_retest-agent.json)
- [test_01_excellent_score.json](docs/v3/testing/agent-results/test_01_excellent_score-agent.json)
- [test_02_mild_imbalance.json](docs/v3/testing/agent-results/test_02_mild_imbalance-agent.json)
- [test_03_moderate_imbalance.json](docs/v3/testing/agent-results/test_03_moderate_imbalance-agent.json)
- [test_04_significant_imbalance.json](docs/v3/testing/agent-results/test_04_significant_imbalance-agent.json)
- [test_05_trend_stable_left_low.json](docs/v3/testing/agent-results/test_05_trend_stable_left_low-agent.json)
- [test_06_trend_stable_right_low.json](docs/v3/testing/agent-results/test_06_trend_stable_right_low-agent.json)
- [test_07_trend_cross.json](docs/v3/testing/agent-results/test_07_trend_cross-agent.json)
- [test_08_trend_potential_symptom.json](docs/v3/testing/agent-results/test_08_trend_potential_symptom-agent.json)
- [test_09_trend_fast_response.json](docs/v3/testing/agent-results/test_09_trend_fast_response-agent.json)
- [test_10_diff_levels.json](docs/v3/testing/agent-results/test_10_diff_levels-agent.json)
- [test_11_side_bias_4.json](docs/v3/testing/agent-results/test_11_side_bias_4-agent.json)
- [test_12_side_bias_5.json](docs/v3/testing/agent-results/test_12_side_bias_5-agent.json)
- [test_13_side_bias_6.json](docs/v3/testing/agent-results/test_13_side_bias_6-agent.json)
- [test_14_cervical_opposite.json](docs/v3/testing/agent-results/test_14_cervical_opposite-agent.json)
- [test_15_cervical_lumbar_cross.json](docs/v3/testing/agent-results/test_15_cervical_lumbar_cross-agent.json)
- [test_16_gender_male.json](docs/v3/testing/agent-results/test_16_gender_male-agent.json)
- [test_17_gender_female.json](docs/v3/testing/agent-results/test_17_gender_female-agent.json)
- [test_18_gender_unknown.json](docs/v3/testing/agent-results/test_18_gender_unknown-agent.json)
- [test_19_retest_0_2_days.json](docs/v3/testing/agent-results/test_19_retest_0_2_days-agent.json)
- [test_20_retest_3_6_days.json](docs/v3/testing/agent-results/test_20_retest_3_6_days-agent.json)
- [test_21_retest_7_13_days.json](docs/v3/testing/agent-results/test_21_retest_7_13_days-agent.json)
- [test_22_retest_14_29_days_low.json](docs/v3/testing/agent-results/test_22_retest_14_29_days_low-agent.json)
- [test_23_retest_14_29_days_high.json](docs/v3/testing/agent-results/test_23_retest_14_29_days_high-agent.json)
- [test_24_retest_30_plus_days.json](docs/v3/testing/agent-results/test_24_retest_30_plus_days-agent.json)
- [test_25_retest_improvement.json](docs/v3/testing/agent-results/test_25_retest_improvement-agent.json)
- [test_26_low_temp_index_max.json](docs/v3/testing/agent-results/test_26_low_temp_index_max-agent.json)
- [test_27_diff_change_improved.json](docs/v3/testing/agent-results/test_27_diff_change_improved-agent.json)
- [test_28_diff_change_worsened.json](docs/v3/testing/agent-results/test_28_diff_change_worsened-agent.json)
- [test_29_realistic_mild.json](docs/v3/testing/agent-results/test_29_realistic_mild-agent.json)
- [test_30_realistic_moderate.json](docs/v3/testing/agent-results/test_30_realistic_moderate-agent.json)
- [test_31_bladder_lowest.json](docs/v3/testing/agent-results/test_31_bladder_lowest-agent.json)
- [test_32_kidney_cross.json](docs/v3/testing/agent-results/test_32_kidney_cross-agent.json)
