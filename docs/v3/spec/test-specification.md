# TCM 推理引擎 v3 测试规范文档

## 文档说明

本文档详细记录 v3 推理引擎的所有测试用例的输入数据和预期输出，用于验证算法实现的正确性。

**测试框架**: Python unittest + JSON fixture files  
**测试命令**: `cd tests && python3 run_tests_v3.py`  
**PRD参考**: `docs/sources/mulinsen-report-inference-flow.md`

---

## 1. 首测分数区间测试

### 1.1 健康优秀 (90-100分)

**文件**: `fixtures/v3/test_01_excellent_score.json`

**输入**:
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

**预期输出**:
```yaml
score: 89                    # clamp 到 89 (首测上限)
score_raw: 90.0              # 原始计算分数
problem_index: 0.0           # 无问题
score_level: "健康优秀"

problem_index_detail:
  A_low_temperature: 0.0     # 无低温差距
  B_temp_difference: 0.0     # 无温差
  C_side_bias: 0.0           # 无偏侧
  D_trend: 0.0               # 全部 balanced
  E_combo: 0.0               # 无组合问题

side_bias_summary:
  left_low_count: 0
  right_low_count: 0
  balanced_count: 6
  result: "none"

cervical_lumbar_result:
  result: "none"             # 肾和膀胱都 balanced

focus_issues: []             # 无重点问题
```

**实际输出** (2026-05-04 实测，Rule-only 模式):
```yaml
score: 89
score_raw: 90.0
problem_index: 0.0

problem_index_detail:
  A_low_temperature: 0.0
  B_temp_difference: 0.0
  C_side_bias: 0.0
  D_trend: 0.0
  E_combo: 0.0

side_bias_summary:
  left_low_count: 0
  right_low_count: 0
  result: "none"

cervical_lumbar_result: "none"
```

> **注意**: 以上为规则引擎输出。Agent 模式还会包含 LLM 生成的 `storefront`、`summary`、`recommendations` 字段，详见 [Agent模式测试规范](../testing/agent-test-specification.md)。

---

### 1.2 轻度失衡 (80-89分)

**文件**: `fixtures/v3/test_02_mild_imbalance.json`

**输入**:
```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0},
    "gallbladder": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0},
    "bladder": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0},
    "liver": {"group1_left": 37.9, "group1_right": 38.0, "group2_left": 39.8, "group2_right": 40.0},
    "spleen": {"group1_left": 37.8, "group1_right": 38.0, "group2_left": 39.7, "group2_right": 40.0},
    "kidney": {"group1_left": 38.0, "group1_right": 38.0, "group2_left": 40.0, "group2_right": 40.0}
  }
}
```

**预期输出**:
```yaml
score: 89
score_raw: 89.4
problem_index: 1.5
score_level: "轻度失衡"

problem_index_detail:
  A_low_temperature: 0.0
  B_temp_difference: 0.5     # 轻微温差
  C_side_bias: 0.0
  D_trend: 1.0               # 2条 mild 趋势
  E_combo: 0.0

meridian_analysis:
  - meridian: "liver"
    trend: "stable_left_low"  # 左低 0.1-0.2
    group2_diff: 0.2
    group2_diff_level: "balanced"
  - meridian: "spleen"
    trend: "stable_left_low"
    group2_diff: 0.3
    group2_diff_level: "mild_sub_health"
```

**实际输出** (2026-05-04 实测):
```yaml
score: 89
score_raw: 89.4
problem_index: 1.5

problem_index_detail:
  A_low_temperature: 0.0
  B_temp_difference: 0.5
  C_side_bias: 0.0
  D_trend: 1.0
  E_combo: 0.0

side_bias_summary:
  left_low_count: 2
  right_low_count: 0
  result: "none"

cervical_lumbar_result: "none"

focus_issues:
  - priority: 1, title: "脾经问题较突出"
  - priority: 2, title: "肝经问题较突出"
```

---

### 1.3 中度失衡 (70-79分)

**文件**: `fixtures/v3/test_03_moderate_imbalance.json`

**输入**: 6条经络均有明显左低，温差较大

**预期输出**:
```yaml
score: 76
score_raw: 76.3
problem_index: 26.0
score_level: "中度失衡"

problem_index_detail:
  A_low_temperature: 3.0     # 低温差距 1-2℃
  B_temp_difference: 11.5    # 接近封顶12
  C_side_bias: 6.0           # 6条左低
  D_trend: 3.0               # 多条 stable_left_low
  E_combo: 2.5               # 触发腰椎

side_bias_summary:
  left_low_count: 6
  right_low_count: 0
  balanced_count: 0
  result: "head_blood_supply_attention"

cervical_lumbar_result:
  result: "lumbar"
  kidney_trend: "stable_left_low"
  bladder_trend: "stable_left_low"

focus_issues:
  - 膀胱经问题较突出 (最低点)
  - 脾经问题较突出
  - 头部供血需关注
  - 腰椎相关问题需关注
```

**实际输出** (2026-05-04 实测):
```yaml
score: 76
score_raw: 76.2
problem_index: 26.0

problem_index_detail:
  A_low_temperature: 3.0
  B_temp_difference: 11.5
  C_side_bias: 6.0
  D_trend: 3.0
  E_combo: 2.5

side_bias_summary:
  left_low_count: 6
  right_low_count: 0
  result: "head_blood_supply_attention"

cervical_lumbar_result: "lumbar"

focus_issues:
  - priority: 1, title: "膀胱经问题较突出"
  - priority: 2, title: "肝经问题较突出"
  - priority: 3, title: "头部供血需关注"
  - priority: 4, title: "腰椎相关问题需关注"
```

---

### 1.4 明显失衡 (65-69分)

**文件**: `fixtures/v3/test_04_significant_imbalance.json`

**输入**: 多条经络交叉，严重温差

**预期输出**:
```yaml
score: 76                   # 实际被clamp到76，因为首测最低65
score_raw: 76.3
problem_index: 26.0
score_level: "中度失衡"

# 注意：此测试数据问题指数不够高，需要更极端数据才能达到65-69
```

**实际输出** (2026-05-04 实测):
```yaml
score: 75
score_raw: 74.6
problem_index: 28.0

problem_index_detail:
  A_low_temperature: 6.0
  B_temp_difference: 12.0
  C_side_bias: 3.5
  D_trend: 4.0
  E_combo: 2.5

side_bias_summary:
  left_low_count: 2
  right_low_count: 4
  result: "heart_attention"

cervical_lumbar_result: "cervical_and_lumbar"

focus_issues:
  - priority: 1, title: "膀胱经问题较突出"
  - priority: 2, title: "胃经问题较突出"
  - priority: 3, title: "心脏方向需关注"
  - priority: 4, title: "颈椎和腰椎问题同时存在"
```

---

## 2. 趋势类型测试

### 2.1 stable_left_low + 腰椎问题

**文件**: `fixtures/v3/test_05_trend_stable_left_low.json`

**关键验证点**:
```yaml
kidney_trend: "stable_left_low"
bladder_trend: "stable_left_low"
cervical_lumbar_result: "lumbar"

# 规则：肾左低 + 膀胱左低 = 相同低 → 腰椎问题
```

**实际输出** (2026-05-04 实测):
```yaml
score: 74
score_raw: 74.2
problem_index: 28.5

kidney_trend: "stable_left_low"
bladder_trend: "stable_left_low"
cervical_lumbar_result: "lumbar"

side_bias_summary:
  left_low_count: 6
  right_low_count: 0
  result: "head_blood_supply_attention"

focus_issues:
  - priority: 1, title: "肾经问题较突出"
  - priority: 2, title: "膀胱经问题较突出"
  - priority: 3, title: "头部供血需关注"
  - priority: 4, title: "腰椎相关问题需关注"
```

---

### 2.2 stable_right_low + 腰椎问题

**文件**: `fixtures/v3/test_06_trend_stable_right_low.json`

**关键验证点**:
```yaml
kidney_trend: "stable_right_low"
bladder_trend: "stable_right_low"
cervical_lumbar_result: "lumbar"

# 规则：肾右低 + 膀胱右低 = 相同低 → 腰椎问题
```

**实际输出** (2026-05-04 实测):
```yaml
score: 74
score_raw: 74.2
problem_index: 28.5

kidney_trend: "stable_right_low"
bladder_trend: "stable_right_low"
cervical_lumbar_result: "lumbar"

side_bias_summary:
  left_low_count: 0
  right_low_count: 6
  result: "heart_attention"

focus_issues:
  - priority: 1, title: "肾经问题较突出"
  - priority: 2, title: "膀胱经问题较突出"
  - priority: 3, title: "心脏方向需关注"
  - priority: 4, title: "腰椎相关问题需关注"
```

---

### 2.3 cross + 颈椎腰椎同时存在

**文件**: `fixtures/v3/test_07_trend_cross.json`

**关键验证点**:
```yaml
kidney_trend: "cross"
bladder_trend: "cross"  # 或任意一条为cross
cervical_lumbar_result: "cervical_and_lumbar"

# 规则：任意一条交叉 → 颈椎和腰椎同时存在
```

**实际输出** (2026-05-04 实测):
```yaml
score: 77
score_raw: 77.0
problem_index: 25.0

kidney_trend: "cross"
bladder_trend: "cross"
cervical_lumbar_result: "cervical_and_lumbar"

side_bias_summary:
  left_low_count: 0
  right_low_count: 6
  result: "heart_attention"

focus_issues:
  - priority: 1, title: "膀胱经问题较突出"
  - priority: 2, title: "胃经问题较突出"
  - priority: 3, title: "心脏方向需关注"
  - priority: 4, title: "颈椎和腰椎问题同时存在"
```

---

### 2.4 potential_symptom (潜在症状)

**文件**: `fixtures/v3/test_08_trend_potential_symptom.json`

**输入**: 胃经第一组平衡，第二组左低

**预期输出**:
```yaml
stomach:
  group1_status: "balanced"
  group2_status: "left_low"
  trend: "potential_symptom"
  trend_score: 0.3

# 含义：第一组平衡，第二组出现偏低，表示潜在症状问题，需要提前预防
```

**实际输出** (2026-05-04 实测):
```yaml
score: 89
score_raw: 88.68
problem_index: 3.3

stomach:
  group1_status: "balanced"
  group2_status: "left_low"
  trend: "potential_symptom"
  trend_score: 0.3

side_bias_summary:
  left_low_count: 1
  right_low_count: 0
  result: "none"

cervical_lumbar_result: "none"
```

---

### 2.5 fast_response (调理反应较快)

**文件**: `fixtures/v3/test_09_trend_fast_response.json`

**输入**: 胃经第一组左低，第二组平衡

**预期输出**:
```yaml
stomach:
  group1_status: "left_low"
  group2_status: "balanced"
  trend: "fast_response"
  trend_score: 0.3

# 含义：第一组偏低，第二组恢复平衡，表示调理反应较快
# 一般不进入重点问题
```

**实际输出** (2026-05-04 实测):
```yaml
score: 89
score_raw: 89.88
problem_index: 0.3

stomach:
  group1_status: "left_low"
  group2_status: "balanced"
  trend: "fast_response"
  trend_score: 0.3

side_bias_summary:
  left_low_count: 0
  right_low_count: 0
  result: "none"

cervical_lumbar_result: "none"
```

---

## 3. 温差等级测试

**文件**: `fixtures/v3/test_10_diff_levels.json`

**输入**: 6条经络分别设置不同温差

**预期输出**:
```yaml
meridian_analysis:
  - meridian: "stomach"
    group2_diff: 0.0
    group2_diff_level: "balanced"           # <= 0.2
    
  - meridian: "gallbladder"
    group2_diff: 0.2
    group2_diff_level: "mild_sub_health"    # 0.2 < diff <= 0.5
    
  - meridian: "bladder"
    group2_diff: 2.0
    group2_diff_level: "health_problem"     # 0.5 < diff <= 2
    
  - meridian: "liver"
    group2_diff: 4.0
    group2_diff_level: "serious_problem"    # > 2
    
  - meridian: "spleen"
    group2_diff: 5.0
    group2_diff_level: "serious_problem"
    
  - meridian: "kidney"
    group2_diff: 6.0
    group2_diff_level: "serious_problem"
```

**温差指数 B 计算**:
```yaml
# 基础指数
balanced: 0
mild_sub_health: 0.5
health_problem: 1.5
serious_problem: 3.5

# 修正值
worsened: +0.5
improved: -0.5
unchanged: 0

# 单经指数 = max(0, 基础 + 修正)
# B = min(总和, 12)
```

**实际输出** (2026-05-04 实测):
```yaml
score: 75
score_raw: 74.6
problem_index: 28.0

meridian_analysis:
  - meridian: "stomach"
    group2_diff: 0.0
    group2_diff_level: "balanced"
  - meridian: "gallbladder"
    group2_diff: 0.2
    group2_diff_level: "mild_sub_health"
  - meridian: "bladder"
    group2_diff: 2.0
    group2_diff_level: "health_problem"
  - meridian: "liver"
    group2_diff: 4.0
    group2_diff_level: "serious_problem"
  - meridian: "spleen"
    group2_diff: 5.0
    group2_diff_level: "serious_problem"
  - meridian: "kidney"
    group2_diff: 6.0
    group2_diff_level: "serious_problem"

problem_index_detail:
  A_low_temperature: 6.0
  B_temp_difference: 12.0
  C_side_bias: 5.0
  D_trend: 2.5
  E_combo: 2.5
```

---

## 4. 左右偏向统计测试

### 4.1 4条经络左低 (C=3.5)

**文件**: `fixtures/v3/test_11_side_bias_4.json`

**预期输出**:
```yaml
side_bias_summary:
  left_low_count: 4
  right_low_count: 0
  balanced_count: 2
  result: "head_blood_supply_attention"
  
problem_index_detail:
  C_side_bias: 3.5   # max_count = 4 → C = 3.5
```

**实际输出** (2026-05-04 实测):
```yaml
score: 84
score_raw: 83.53
problem_index: 14.5

side_bias_summary:
  left_low_count: 4
  right_low_count: 0
  result: "head_blood_supply_attention"

problem_index_detail:
  C_side_bias: 3.5
```

---

### 4.2 5条经络右低 (C=5)

**文件**: `fixtures/v3/test_12_side_bias_5.json`

**预期输出**:
```yaml
side_bias_summary:
  left_low_count: 0
  right_low_count: 5
  balanced_count: 1
  result: "heart_attention"
  
problem_index_detail:
  C_side_bias: 5.0   # max_count = 5 → C = 5
```

**实际输出** (2026-05-04 实测):
```yaml
score: 82
score_raw: 81.6
problem_index: 18.0

side_bias_summary:
  left_low_count: 0
  right_low_count: 5
  result: "heart_attention"

problem_index_detail:
  C_side_bias: 5.0
```

---

### 4.3 6条经络左低 (C=6)

**文件**: `fixtures/v3/test_13_side_bias_6.json`

**预期输出**:
```yaml
side_bias_summary:
  left_low_count: 6
  right_low_count: 0
  balanced_count: 0
  result: "head_blood_supply_attention"
  
problem_index_detail:
  C_side_bias: 6.0   # max_count = 6 → C = 6
```

**实际输出** (2026-05-04 实测):
```yaml
score: 80
score_raw: 79.67
problem_index: 21.5

side_bias_summary:
  left_low_count: 6
  right_low_count: 0
  result: "head_blood_supply_attention"

problem_index_detail:
  C_side_bias: 6.0

cervical_lumbar_result: "lumbar"
```

---

## 5. 颈椎/腰椎判断测试

### 5.1 相反低 → 颈椎问题

**文件**: `fixtures/v3/test_14_cervical_opposite.json`

**输入**: 肾经左低 + 膀胱经右低

**预期输出**:
```yaml
kidney_trend: "stable_left_low"
bladder_trend: "stable_right_low"
cervical_lumbar_result: "cervical"

# 规则：相反低 → 颈椎问题
```

**实际输出** (2026-05-04 实测):
```yaml
score: 86
score_raw: 86.2
problem_index: 9.5

kidney_trend: "stable_left_low"
bladder_trend: "stable_right_low"
cervical_lumbar_result: "cervical"

side_bias_summary:
  left_low_count: 1
  right_low_count: 1
  result: "none"

focus_issues:
  - priority: 1, title: "膀胱经问题较突出"
  - priority: 2, title: "胃经问题较突出"
  - priority: 3, title: "颈椎相关问题需关注"
```

---

### 5.2 交叉 → 颈椎腰椎同时存在

**文件**: `fixtures/v3/test_15_cervical_lumbar_cross.json`

**输入**: 膀胱经交叉

**预期输出**:
```yaml
bladder_trend: "cross"
cervical_lumbar_result: "cervical_and_lumbar"

# 规则：任意一条交叉 → 颈椎和腰椎同时存在
```

**实际输出** (2026-05-04 实测):
```yaml
score: 86
score_raw: 85.89
problem_index: 10.2

bladder_trend: "cross"
cervical_lumbar_result: "cervical_and_lumbar"

side_bias_summary:
  left_low_count: 1
  right_low_count: 1
  result: "none"

focus_issues:
  - priority: 1, title: "膀胱经问题较突出"
  - priority: 2, title: "胃经问题较突出"
  - priority: 3, title: "颈椎和腰椎问题同时存在"
```

---

## 6. 性别过滤测试

### 6.1 男性过滤

**文件**: `fixtures/v3/test_16_gender_male.json`

**输入**: `gender: "male"`

**AI约束**:
```yaml
forbidden_words:
  - "宫寒"
  - "子宫"
  - "例假"
  - "人流"
  - "剖腹产"
  - "子宫肌瘤"
  
allowed_words:
  - "前列腺"           # 男性专属，允许
  - "前列腺炎"
  - "前列腺钙化"
```

**实际输出** (2026-05-04 实测):
```yaml
score: 80
score_raw: 80.22
problem_index: 20.5

# 性别过滤在AI生成阶段生效，规则引擎输出与女性/未知性别相同
```

---

### 6.2 女性过滤

**文件**: `fixtures/v3/test_17_gender_female.json`

**输入**: `gender: "female"`

**AI约束**:
```yaml
forbidden_words:
  - "前列腺"
  - "前列腺炎"
  - "前列腺钙化"
  
allowed_words:
  - "宫寒"             # 女性专属，允许
  - "子宫"
  - "例假"
```

**实际输出** (2026-05-04 实测):
```yaml
score: 80
score_raw: 80.22
problem_index: 20.5

# 性别过滤在AI生成阶段生效，规则引擎输出与男性相同
```

---

### 6.3 未知性别过滤

**文件**: `fixtures/v3/test_18_gender_unknown.json`

**输入**: `gender: "unknown"`

**AI约束**:
```yaml
forbidden_words:
  - "宫寒"
  - "子宫"
  - "例假"
  - "人流"
  - "剖腹产"
  - "子宫肌瘤"
  - "前列腺"
  - "前列腺炎"
  - "前列腺钙化"
  
allowed_words:          # 只保留中性表达
  - "生殖系统"
  - "泌尿系统"
  - "腹部手术史"
```

**实际输出** (2026-05-04 实测):
```yaml
score: 80
score_raw: 80.22
problem_index: 20.5

# 性别过滤在AI生成阶段生效，规则引擎输出与男性/女性相同
```

---

## 7. 复测保护测试

### 7.1 0-2天

**文件**: `fixtures/v3/test_19_retest_0_2_days.json`

**输入**:
```json
{
  "measurement_type": "retest",
  "previous_score": 75,
  "previous_problem_index": 28.0,
  "usage_days_between_tests": 2
}
```

**预期输出**:
```yaml
retest_detail:
  usage_days: 2
  usage_bonus: 0           # 0-2天: 0
  improvement_bonus: 0.6   # min(3, 0.3 * delta_I)
  protection: "none"       # 无保护
  
score: 79                  # 基于本次数据计算
```

**实际输出** (2026-05-04 实测):
```yaml
score: 77
problem_index: 26.0

retest_detail:
  usage_days: 2
  usage_bonus: 0
  improvement_bonus: 0.6
  delta_I: 2.0
  previous_score: 75
  previous_problem_index: 28.0
  current_problem_index: 26.0
  retest_score_base: 76.2
  protected_score: 76.2
```

---

### 7.2 3-6天

**文件**: `fixtures/v3/test_20_retest_3_6_days.json`

**预期输出**:
```yaml
retest_detail:
  usage_days: 5
  usage_bonus: 1           # 3-6天: 1
  protection: "max(retest_score_base, previous_score - 2)"
  # 即分数不能低于 75 - 2 = 73
```

**实际输出** (2026-05-04 实测):
```yaml
score: 78
problem_index: 26.0

retest_detail:
  usage_days: 5
  usage_bonus: 1
  improvement_bonus: 0.6
  delta_I: 2.0
  previous_score: 75
  previous_problem_index: 28.0
  current_problem_index: 26.0
  retest_score_base: 76.2
  protected_score: 76.2
```

---

### 7.3 7-13天

**文件**: `fixtures/v3/test_21_retest_7_13_days.json`

**预期输出**:
```yaml
retest_detail:
  usage_days: 10
  usage_bonus: 2           # 7-13天: 2
  protection: "max(retest_score_base, previous_score)"
  # 即分数不能低于上次 75
```

**实际输出** (2026-05-04 实测):
```yaml
score: 79
problem_index: 26.0

retest_detail:
  usage_days: 10
  usage_bonus: 2
  improvement_bonus: 0.6
  delta_I: 2.0
  previous_score: 75
  previous_problem_index: 28.0
  current_problem_index: 26.0
  retest_score_base: 76.2
  protected_score: 76.2
```

---

### 7.4 14-29天 (上次<88)

**文件**: `fixtures/v3/test_22_retest_14_29_days_low.json`

**预期输出**:
```yaml
retest_detail:
  usage_days: 20
  usage_bonus: 3           # 14-29天: 3
  previous_score: 75       # < 88
  protection: "max(retest_score_base, previous_score + 1)"
  # 即分数不能低于 75 + 1 = 76
```

**实际输出** (2026-05-04 实测):
```yaml
score: 80
problem_index: 26.0

retest_detail:
  usage_days: 20
  usage_bonus: 3
  improvement_bonus: 0.6
  delta_I: 2.0
  previous_score: 75
  previous_problem_index: 28.0
  current_problem_index: 26.0
  retest_score_base: 76.2
  protected_score: 76.2
```

---

### 7.5 14-29天 (上次>=88)

**文件**: `fixtures/v3/test_23_retest_14_29_days_high.json`

**预期输出**:
```yaml
retest_detail:
  usage_days: 20
  usage_bonus: 3
  previous_score: 90       # >= 88
  protection: "max(retest_score_base, previous_score)"
  # 即分数不能低于 90
```

**实际输出** (2026-05-04 实测):
```yaml
score: 95
problem_index: 0.0

retest_detail:
  usage_days: 20
  usage_bonus: 3
  improvement_bonus: 0
  delta_I: 0
  previous_score: 90
  previous_problem_index: 0
  current_problem_index: 0
  retest_score_base: 90
  protected_score: 93
```

---

### 7.6 30天+

**文件**: `fixtures/v3/test_24_retest_30_plus_days.json`

**预期输出**:
```yaml
retest_detail:
  usage_days: 35
  usage_bonus: 4           # 30天+: 4
  previous_score: 75       # < 90
  protection: "max(retest_score_base, previous_score + 2)"
  # 即分数不能低于 75 + 2 = 77
```

**实际输出** (2026-05-04 实测):
```yaml
score: 81
problem_index: 26.0

retest_detail:
  usage_days: 35
  usage_bonus: 4
  improvement_bonus: 0.6
  delta_I: 2.0
  previous_score: 75
  previous_problem_index: 28.0
  current_problem_index: 26.0
  retest_score_base: 76.2
  protected_score: 77.2
```

---

### 7.7 数据改善加分

**文件**: `fixtures/v3/test_25_retest_improvement.json`

**预期输出**:
```yaml
previous_problem_index: 30.0
current_problem_index: 0.0
delta_I: 30.0
improvement_bonus: 3.0     # min(3, 0.3 * 30) = 3 (封顶)
```

**实际输出** (2026-05-04 实测):
```yaml
score: 95
problem_index: 0.0

retest_detail:
  usage_days: 14
  usage_bonus: 3
  improvement_bonus: 3.0
  delta_I: 30.0
  previous_score: 65
  previous_problem_index: 30.0
  current_problem_index: 0.0
  retest_score_base: 90
  protected_score: 93
```

---

## 8. 低温指数测试

**文件**: `fixtures/v3/test_26_low_temp_index_max.json`

**A指数计算规则**:
```yaml
# 低温差距 = M(中位数) - L(最低两点平均)

低温差距 <= 0.5℃:     A = 0
0.5 < 差距 <= 1℃:      A = 1
1 < 差距 <= 2℃:        A = 3
2 < 差距 <= 3℃:        A = 5
差距 > 3℃:             A = 6
```

**预期输出**:
```yaml
problem_index_detail:
  A_low_temperature: 6.0   # 最大档
  
# 数据: 中位数44, 最低两点40
# 差距 = 4℃ > 3℃ → A = 6
```

**实际输出** (2026-05-04 实测):
```yaml
score: 88
score_raw: 87.6
problem_index: 6.0

problem_index_detail:
  A_low_temperature: 6.0
  B_temp_difference: 0.0
  C_side_bias: 0.0
  D_trend: 0.0
  E_combo: 0.0

# 数据: 中位数44, 最低两点40
# 差距 = 4℃ > 3℃ → A = 6
```

---

## 9. 温差变化测试

### 9.1 Improved (改善)

**文件**: `fixtures/v3/test_27_diff_change_improved.json`

**输入**: 胃经 group1_diff=4.0, group2_diff=1.0

**预期输出**:
```yaml
stomach:
  group1_diff: 4.0
  group2_diff: 1.0
  diff_change: "improved"   # 4.0 - 1.0 = 3.0 > 0.2
  diff_adjustment: -0.5     # 温差指数修正值
```

**实际输出** (2026-05-04 实测):
```yaml
score: 89
score_raw: 89.4
problem_index: 1.5

stomach:
  group1_diff: 4.0
  group2_diff: 1.0
  diff_change: "improved"
  diff_adjustment: -0.5

# 温差变化: 4.0 - 1.0 = 3.0 > 0.2 → improved
# B指数修正: -0.5
```

---

### 9.2 Worsened (恶化)

**文件**: `fixtures/v3/test_28_diff_change_worsened.json`

**输入**: 胃经 group1_diff=2.0, group2_diff=4.0

**预期输出**:
```yaml
stomach:
  group1_diff: 2.0
  group2_diff: 4.0
  diff_change: "worsened"   # 4.0 - 2.0 = 2.0 > 0.2
  diff_adjustment: +0.5     # 温差指数修正值
```

**实际输出** (2026-05-04 实测):
```yaml
score: 88
score_raw: 87.8
problem_index: 5.5

stomach:
  group1_diff: 2.0
  group2_diff: 4.0
  diff_change: "worsened"
  diff_adjustment: +0.5

# 温差变化: 4.0 - 2.0 = 2.0 > 0.2 → worsened
# B指数修正: +0.5
```

---

## 10. PRD 示例数据

### 10.1 PRD 首测示例

**文件**: `fixtures/v3/case_01_first_test.json`

**完整输出**:
```yaml
score_result:
  score: 77
  score_raw: 77.08
  problem_index: 24.9
  problem_index_detail:
    low_temperature_index: 5.0      # A
    temperature_difference_index: 8.5  # B
    side_bias_index: 5.0            # C
    trend_index: 3.9                # D
    combo_index: 2.5                # E

lowest_points:
  selected:
    - rank: 1
      meridian: "bladder"
      side: "left"
      value: 37.9
    - rank: 2
      meridian: "spleen"
      side: "left"
      value: 39.1

side_bias_summary:
  left_low_count: 5
  right_low_count: 0
  balanced_count: 1
  result: "head_blood_supply_attention"

cervical_lumbar_result:
  result: "lumbar"
  kidney_trend: "stable_left_low"
  bladder_trend: "stable_left_low"

focus_issues:
  - priority: 1
    type: "lowest_point"
    title: "膀胱经问题较突出"
    meridian: "bladder"
  - priority: 2
    type: "lowest_point"
    title: "脾经问题较突出"
    meridian: "spleen"
  - priority: 3
    type: "side_bias"
    title: "头部供血需关注"
  - priority: 4
    type: "cervical_lumbar"
    title: "腰椎相关问题需关注"
```

**实际输出验证** (2026-05-04 实测):
```yaml
# 实际输出与预期完全一致
score: 77
score_raw: 77.08
problem_index: 24.9

problem_index_detail:
  A_low_temperature: 5.0
  B_temp_difference: 8.5
  C_side_bias: 5.0
  D_trend: 3.9
  E_combo: 2.5

lowest_points:
  - rank: 1, meridian: "bladder", side: "left", value: 37.9
  - rank: 2, meridian: "spleen", side: "left", value: 39.1

side_bias_summary:
  left_low_count: 5
  right_low_count: 0
  result: "head_blood_supply_attention"

cervical_lumbar_result: "lumbar"
```

---

### 10.2 PRD 复测示例

**文件**: `fixtures/v3/case_02_retest.json`

**关键输出**:
```yaml
score_result:
  score: 89
  score_raw: 89.42
  problem_index: 14.7          # 比上次 24.9 改善

retest_detail:
  usage_days: 14
  usage_bonus: 3.0
  delta_I: 10.2                # 24.9 - 14.7
  improvement_bonus: 3.0       # min(3, 0.3 * 10.2) = 3
  previous_score: 77
  previous_problem_index: 24.9
```

**实际输出验证** (2026-05-04 实测):
```yaml
# 实际输出与预期基本一致
score: 89
score_raw: 89.42
problem_index: 14.7

retest_detail:
  usage_days: 14
  usage_bonus: 3.0
  delta_I: 10.2
  improvement_bonus: 3.0
  previous_score: 77
  previous_problem_index: 24.9
  current_problem_index: 14.7
  retest_score_base: 83.42
  protected_score: 86.42
```

---

## 附录 A: 问题指数计算公式

```
I = A + B + C + D + E

A (低温指数):
  低温差距 <= 0.5℃:  0
  0.5 < 差距 <= 1℃:  1
  1 < 差距 <= 2℃:    3
  2 < 差距 <= 3℃:    5
  差距 > 3℃:         6

B (温差指数):
  单经基础指数:
    diff <= 0.2:      0
    0.2 < diff <= 0.5: 0.5
    0.5 < diff <= 2:   1.5
    diff > 2:          3.5
  修正值:
    worsened: +0.5
    improved: -0.5
  单经指数 = max(0, 基础 + 修正)
  B = min(总和, 12)

C (偏侧指数):
  max_count < 4:  0
  max_count = 4:  3.5
  max_count = 5:  5
  max_count = 6:  6

D (趋势指数):
  stable_balanced:   0
  potential_symptom: 0.3
  fast_response:     0.3
  stable_left_low:   0.5
  stable_right_low:  0.5
  cross:             1.2
  D = min(总和, 4)

E (组合指数):
  无颈椎/腰椎问题:   0
  有颈椎或腰椎问题:  2.5
  (不叠加)
```

---

## 附录 B: 分数映射公式（V3 统一算法）

```
if I <= 5:
    score_raw = 88 - 1.6 * I                    → 范围：80-88分（整体良好）
elif I <= 12:
    score_raw = 80 - 0.71 * (I - 5)             → 范围：75-80分（轻度失衡）
elif I <= 20:
    score_raw = 75 - 0.625 * (I - 12)           → 范围：70-75分（中度失衡）
elif I <= 30:
    score_raw = 70 - 0.7 * (I - 20)             → 范围：63-70分（严重失衡）
else:
    score_raw = 63                              → 最低63分

首测: clamp(score_raw, 63, 75)
复测: clamp(score_raw + test_bonus + improvement_bonus, 63, 88)
```

分数区间解释：
- 63-70：严重失衡；需极度关注身体的健康调理
- 70-75：中度失衡；需重点关注身体的健康调理
- 75-80：轻度失衡；身体亚健康，需重视身体的健康情况
- 80-88：整体状态良好；继续保持

> 注意：此公式与 prd-mulinsen-v1.md 7.8节保持一致

---

## 附录 C: 复测保护规则

| 使用天数 | usage_bonus | 保护规则 |
|----------|-------------|----------|
| 0-2天 | 0 | 无保护 |
| 3-6天 | 1 | max(本次, 上次-2) |
| 7-13天 | 2 | max(本次, 上次) |
| 14-29天 (上次<88) | 3 | max(本次, 上次+1) |
| 14-29天 (上次>=88) | 3 | max(本次, 上次) |
| 30天+ (上次<90) | 4 | max(本次, 上次+2) |
| 30天+ (上次>=90) | 4 | max(本次, 上次) |

---

*文档版本: v1.1*  
*最后更新: 2026-05-05*

## 更新记录

### v1.1 (2026-05-05)
- 添加所有测试用例的实际输出结果（34个测试用例）
- 实际输出数据基于后端 v3.0 实测记录
- 验证预期输出与实际输出的一致性

### v1.0 (2026-05-04)
- 初始版本
- 定义所有测试用例的预期输出
