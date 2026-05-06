# V3 API 测试结果汇总

**测试时间**: 2026-05-05 06:00:19
**API地址**: http://localhost:18790/api/inference/meridian-diagnosis

## 统计概览

- **测试总数**: 34
- **成功数**: 0
- **失败数**: 34
- **成功率**: 0.0%

## 详细结果

| 序号 | 测试文件 | 状态 | 响应时间(ms) | Score | Problem Index | Side Bias | Cervical/Lumbar | 错误 |
|------|----------|------|--------------|-------|---------------|-----------|-----------------|------|
| 1 | test_01_excellent_score.json | ❌ | 11.11 | - | - | - | - | 400 Client Error: Bad Request ... |
| 2 | test_02_mild_imbalance.json | ❌ | 12.46 | - | - | - | - | 400 Client Error: Bad Request ... |
| 3 | test_03_moderate_imbalance.json | ❌ | 20.04 | - | - | - | - | 400 Client Error: Bad Request ... |
| 4 | test_04_significant_imbalance.json | ❌ | 13.72 | - | - | - | - | 400 Client Error: Bad Request ... |
| 5 | test_05_trend_stable_left_low.json | ❌ | 19.80 | - | - | - | - | 400 Client Error: Bad Request ... |
| 6 | test_06_trend_stable_right_low.json | ❌ | 9.65 | - | - | - | - | 400 Client Error: Bad Request ... |
| 7 | test_07_trend_cross.json | ❌ | 21.65 | - | - | - | - | 400 Client Error: Bad Request ... |
| 8 | test_08_trend_potential_symptom.json | ❌ | 7.75 | - | - | - | - | 400 Client Error: Bad Request ... |
| 9 | test_09_trend_fast_response.json | ❌ | 5.95 | - | - | - | - | 400 Client Error: Bad Request ... |
| 10 | test_10_diff_levels.json | ❌ | 11.48 | - | - | - | - | 400 Client Error: Bad Request ... |
| 11 | test_11_side_bias_4.json | ❌ | 7.25 | - | - | - | - | 400 Client Error: Bad Request ... |
| 12 | test_12_side_bias_5.json | ❌ | 5.70 | - | - | - | - | 400 Client Error: Bad Request ... |
| 13 | test_13_side_bias_6.json | ❌ | 5.29 | - | - | - | - | 400 Client Error: Bad Request ... |
| 14 | test_14_cervical_opposite.json | ❌ | 10.50 | - | - | - | - | 400 Client Error: Bad Request ... |
| 15 | test_15_cervical_lumbar_cross.json | ❌ | 11.37 | - | - | - | - | 400 Client Error: Bad Request ... |
| 16 | test_16_gender_male.json | ❌ | 8.06 | - | - | - | - | 400 Client Error: Bad Request ... |
| 17 | test_17_gender_female.json | ❌ | 9.27 | - | - | - | - | 400 Client Error: Bad Request ... |
| 18 | test_18_gender_unknown.json | ❌ | 10.77 | - | - | - | - | 400 Client Error: Bad Request ... |
| 19 | test_19_retest_0_2_days.json | ❌ | 8.28 | - | - | - | - | 400 Client Error: Bad Request ... |
| 20 | test_20_retest_3_6_days.json | ❌ | 5.18 | - | - | - | - | 400 Client Error: Bad Request ... |
| 21 | test_21_retest_7_13_days.json | ❌ | 8.76 | - | - | - | - | 400 Client Error: Bad Request ... |
| 22 | test_22_retest_14_29_days_low.json | ❌ | 7.51 | - | - | - | - | 400 Client Error: Bad Request ... |
| 23 | test_23_retest_14_29_days_high.json | ❌ | 1007.42 | - | - | - | - | 400 Client Error: Bad Request ... |
| 24 | test_24_retest_30_plus_days.json | ❌ | 9.56 | - | - | - | - | 400 Client Error: Bad Request ... |
| 25 | test_25_retest_improvement.json | ❌ | 15.48 | - | - | - | - | 400 Client Error: Bad Request ... |
| 26 | test_26_low_temp_index_max.json | ❌ | 6.10 | - | - | - | - | 400 Client Error: Bad Request ... |
| 27 | test_27_diff_change_improved.json | ❌ | 11.73 | - | - | - | - | 400 Client Error: Bad Request ... |
| 28 | test_28_diff_change_worsened.json | ❌ | 9.10 | - | - | - | - | 400 Client Error: Bad Request ... |
| 29 | test_29_realistic_mild.json | ❌ | 7.70 | - | - | - | - | 400 Client Error: Bad Request ... |
| 30 | test_30_realistic_moderate.json | ❌ | 6.92 | - | - | - | - | 400 Client Error: Bad Request ... |
| 31 | test_31_bladder_lowest.json | ❌ | 8.61 | - | - | - | - | 400 Client Error: Bad Request ... |
| 32 | test_32_kidney_cross.json | ❌ | 6.84 | - | - | - | - | 400 Client Error: Bad Request ... |
| 33 | case_01_first_test.json | ❌ | 5.11 | - | - | - | - | 400 Client Error: Bad Request ... |
| 34 | case_02_retest.json | ❌ | 2.96 | - | - | - | - | 400 Client Error: Bad Request ... |

## 关键字段详细对比

### test_01_excellent_score.json

**测试名称**: 首测 - 健康优秀分数区间(90-100): 所有经络平衡,温差小,问题指数<=10
**状态**: 失败
**响应时间**: 11.11 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_02_mild_imbalance.json

**测试名称**: 首测 - 轻度失衡分数区间(80-89): 轻微温差,1-2条经络轻度异常
**状态**: 失败
**响应时间**: 12.46 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_03_moderate_imbalance.json

**测试名称**: 首测 - 中度失衡分数区间(70-79): 多条经络有温差,偏侧明显
**状态**: 失败
**响应时间**: 20.04 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_04_significant_imbalance.json

**测试名称**: 首测 - 严重失衡: 极端温差,多交叉,最高问题指数~30.5,分数~73
**状态**: 失败
**响应时间**: 13.72 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_05_trend_stable_left_low.json

**测试名称**: 趋势测试 - stable_left_low: 两组均左低,肾经和膀胱经同左低→腰椎问题
**状态**: 失败
**响应时间**: 19.80 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_06_trend_stable_right_low.json

**测试名称**: 趋势测试 - stable_right_low: 两组均右低,肾经和膀胱经同右低→腰椎问题
**状态**: 失败
**响应时间**: 9.65 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_07_trend_cross.json

**测试名称**: 趋势测试 - cross: 两组左右方向相反,肾经左低+膀胱经右低→颈椎问题
**状态**: 失败
**响应时间**: 21.65 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_08_trend_potential_symptom.json

**测试名称**: 趋势测试 - potential_symptom: 第一组平衡,第二组左低,表示潜在症状
**状态**: 失败
**响应时间**: 7.75 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_09_trend_fast_response.json

**测试名称**: 趋势测试 - fast_response: 第一组左低,第二组平衡,表示调理反应较快
**状态**: 失败
**响应时间**: 5.95 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_10_diff_levels.json

**测试名称**: 温差等级测试: 覆盖balanced/mild/health_problem/serious_problem四种等级
**状态**: 失败
**响应时间**: 11.48 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_11_side_bias_4.json

**测试名称**: 左右偏向测试 - 4条经络左低: 触发头部供血关注, C=3.5
**状态**: 失败
**响应时间**: 7.25 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_12_side_bias_5.json

**测试名称**: 左右偏向测试 - 5条经络右低: 触发心脏方向关注, C=5
**状态**: 失败
**响应时间**: 5.70 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_13_side_bias_6.json

**测试名称**: 左右偏向测试 - 6条经络全部左低: C=6,严重偏侧
**状态**: 失败
**响应时间**: 5.29 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_14_cervical_opposite.json

**测试名称**: 颈椎判断测试 - 肾左低+膀胱右低: 相反低→颈椎问题
**状态**: 失败
**响应时间**: 10.50 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_15_cervical_lumbar_cross.json

**测试名称**: 颈椎腰椎测试 - 肾交叉+膀胱任意: 任意一条交叉→颈椎和腰椎同时存在
**状态**: 失败
**响应时间**: 11.37 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_16_gender_male.json

**测试名称**: 性别过滤测试 - 男性: 不能出现女性专属表达
**状态**: 失败
**响应时间**: 8.06 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_17_gender_female.json

**测试名称**: 性别过滤测试 - 女性: 不能出现男性专属表达
**状态**: 失败
**响应时间**: 9.27 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_18_gender_unknown.json

**测试名称**: 性别过滤测试 - 未知: 只保留中性表达
**状态**: 失败
**响应时间**: 10.77 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_19_retest_0_2_days.json

**测试名称**: 复测测试 - 使用0-2天: 无使用天数加分,无保护
**状态**: 失败
**响应时间**: 8.28 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_20_retest_3_6_days.json

**测试名称**: 复测测试 - 使用3-6天: usage_bonus=1,保护为max(本次,上次-2)
**状态**: 失败
**响应时间**: 5.18 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_21_retest_7_13_days.json

**测试名称**: 复测测试 - 使用7-13天: usage_bonus=2,保护为max(本次,上次)
**状态**: 失败
**响应时间**: 8.76 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_22_retest_14_29_days_low.json

**测试名称**: 复测测试 - 使用14-29天且上次<88: usage_bonus=3,保护为max(本次,上次+1)
**状态**: 失败
**响应时间**: 7.51 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_23_retest_14_29_days_high.json

**测试名称**: 复测测试 - 使用14-29天且上次>=88: usage_bonus=3,保护为max(本次,上次)
**状态**: 失败
**响应时间**: 1007.42 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_24_retest_30_plus_days.json

**测试名称**: 复测测试 - 使用30天及以上且上次<90: usage_bonus=4,保护为max(本次,上次+2)
**状态**: 失败
**响应时间**: 9.56 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_25_retest_improvement.json

**测试名称**: 复测测试 - 数据改善: ΔI>0时improvement_bonus=min(3, 0.3*ΔI)
**状态**: 失败
**响应时间**: 15.48 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_26_low_temp_index_max.json

**测试名称**: 低温指数测试 - 低温差距>3℃: A=6,最高档
**状态**: 失败
**响应时间**: 6.10 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_27_diff_change_improved.json

**测试名称**: 温差变化测试 - improved: 温差缩小>0.2℃
**状态**: 失败
**响应时间**: 11.73 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_28_diff_change_worsened.json

**测试名称**: 温差变化测试 - worsened: 温差变大>0.2℃
**状态**: 失败
**响应时间**: 9.10 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_29_realistic_mild.json

**测试名称**: 真实场景 - 轻度亚健康: 1-2条经络轻度异常，温差0.3-0.5
**状态**: 失败
**响应时间**: 7.70 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_30_realistic_moderate.json

**测试名称**: 真实场景 - 中度失衡: 4-5条经络异常，有明显低温点和温差
**状态**: 失败
**响应时间**: 6.92 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_31_bladder_lowest.json

**测试名称**: 膀胱经最低点场景: 膀胱经温度最低，需结合肾经分析
**状态**: 失败
**响应时间**: 8.61 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### test_32_kidney_cross.json

**测试名称**: 肾经交叉场景: 肾经交叉提示结石/囊肿/手术史风险
**状态**: 失败
**响应时间**: 6.84 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### case_01_first_test.json

**测试名称**: case_01_first_test.json
**状态**: 失败
**响应时间**: 5.11 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---

### case_02_retest.json

**测试名称**: case_02_retest.json
**状态**: 失败
**响应时间**: 2.96 ms

**错误**: 400 Client Error: Bad Request for url: http://localhost:18790/api/inference/meridian-diagnosis

---
