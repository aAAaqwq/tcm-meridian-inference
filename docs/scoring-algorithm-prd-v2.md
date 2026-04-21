# 六条经络推理引擎与评分算法 PRD v2.0

> 版本：v2.0 | 日期：2026-04-20
>
> 本文档严格基于以下三份源文档，统一定义推理引擎的数据模型、计算流程、评分算法和输出结构：
> - `docs/sources/ai-report-prd.md`（报告系统 PRD v1.2）
> - `docs/sources/infer-engine-flow.md`（推理引擎流程说明）
> - `docs/sources/report-structure-overview.md`（报告结构梳理）
> - `docs/sources/rule-library-prd.md`（规则库 PRD v1.0）

---

## 1. 数据模型

### 1.1 输入结构

严格按 ai-report-prd 第 5 节定义，采用 **before/after 两组测量**模型：

```json
{
  "reportContext": {
    "reportType": "initial_or_followup",
    "language": "zh-CN",
    "tone": "professional_clear_warm"
  },
  "subject": {
    "id": "case_001",
    "name": "张三",
    "gender": "female",
    "age": 42
  },
  "measurementSession": {
    "sessionId": "session_20260418_001",
    "measuredAt": "2026-04-18 10:30:00",
    "isFollowup": true,
    "daysSinceLastMeasurement": 30,
    "instrumentUsageDaysBetweenMeasurements": 25
  },
  "measurements": {
    "before": {
      "liver":       { "left": 38.2, "right": 37.6 },
      "spleen":      { "left": 38.4, "right": 37.8 },
      "kidney":      { "left": 37.9, "right": 37.1 },
      "stomach":     { "left": 38.5, "right": 38.0 },
      "gallbladder": { "left": 37.4, "right": 38.2 },
      "bladder":     { "left": 37.2, "right": 36.9 }
    },
    "after": {
      "liver":       { "left": 38.0, "right": 37.9 },
      "spleen":      { "left": 38.3, "right": 38.0 },
      "kidney":      { "left": 37.4, "right": 37.8 },
      "stomach":     { "left": 38.4, "right": 38.2 },
      "gallbladder": { "left": 37.8, "right": 38.0 },
      "bladder":     { "left": 37.5, "right": 37.6 }
    }
  },
  "scoreContext": {
    "previousDisplayedScore": 72
  }
}
```

### 1.2 六条经络

肝经(liver)、脾经(spleen)、肾经(kidney)、胃经(stomach)、胆经(gallbladder)、膀胱经(bladder)

### 1.3 优先级

| 优先级 | 经络 |
|--------|------|
| A | 肝、脾、肾、膀胱 |
| B | 胆 |
| C | 胃（次要项，除非异常明显否则不前置） |

---

## 2. 引擎执行流程

严格按 infer-engine-flow 的 12 步执行：

```
输入数据
    │
    ▼
Step 1:  load_input()              读取输入数据
    │
    ▼
Step 2:  validate_input()          校验输入完整性
    │                              → 失败则返回错误码
    ▼
Step 3:  compute_meridian_states() 计算单经状态
    │
    ▼
Step 4:  compute_global_patterns() 计算整体偏侧与交叉情况
    │
    ▼
Step 5:  find_lowest_meridian()    查找最低温经络
    │    apply_combination_rules() 计算组合规则命中
    │
    ▼
Step 6:  calculate_raw_score()     计算原始综合评分（扣分）
    │
    ▼
Step 7:  apply_improvement_bonus() 计算改善加分
    │
    ▼
Step 8:  apply_followup_policy()   应用复测保护规则
    │
    ▼
Step 9:  map_score_level()         计算评分等级与摘要
    │
    ▼
Step 10: collect_advice_tags()     生成建议标签
    │
    ▼
Step 11: build_model_payload()     组装模型输入上下文
    │
    ▼
Step 12: build_final_output()      组装最终输出结构
```

---

## 3. Step 2：输入校验

| 校验项 | 规则 |
|--------|------|
| 经络完整性 | before 和 after 各必须包含 6 条经络 |
| 字段完整性 | 每条经络必须有 left 和 right |
| 复测字段 | isFollowup=true 时必须填写 instrumentUsageDaysBetweenMeasurements |
| 取值范围 | instrumentUsageDaysBetweenMeasurements: 0~365 |

校验失败返回错误码，不进入后续推理。

---

## 4. Step 3：计算单经状态

### 4.1 状态定义

| 状态 | 条件 |
|------|------|
| `balanced` | `abs(left - right) <= 0.2` |
| `left_low` | `left < right`（且差值 > 0.2） |
| `right_low` | `right < left`（且差值 > 0.2） |

**平衡阈值：** `balanceThreshold = 0.2`

### 4.2 交叉定义

```
cross = (beforeStatus 为 left_low 或 right_low)
    AND (afterStatus 为 left_low 或 right_low)
    AND (beforeLowSide ≠ afterLowSide)
```

即：两组都有偏侧，且偏的方向相反。

### 4.3 严重程度（severity）

基于左右温差绝对值 `diffAbs = abs(left - right)`，取 before 和 after 中较大值：

| 温差范围 | 程度 |
|----------|------|
| 0 ~ 0.2 | balanced |
| 0.2 ~ 0.5 | mild |
| 0.5 ~ 1.0 | medium |
| > 1.0 | high |

```python
severity = get_severity(max(beforeDiff, afterDiff))
```

### 4.4 每条经络输出字段

| 字段 | 说明 |
|------|------|
| `beforeStatus` | 第一组状态：balanced / left_low / right_low |
| `afterStatus` | 第二组状态：balanced / left_low / right_low |
| `beforeLowSide` | 第一组低侧：left / right / None |
| `afterLowSide` | 第二组低侧：left / right / None |
| `beforeDiff` | 第一组左右温差绝对值 |
| `afterDiff` | 第二组左右温差绝对值 |
| `cross` | 是否交叉 |
| `severity` | balanced / mild / medium / high |

---

## 5. Step 4：计算整体偏侧与交叉情况

### 5.1 输出字段

| 字段 | 说明 |
|------|------|
| `leftLowCountBefore` | 第一组偏左经络数 |
| `rightLowCountBefore` | 第一组偏右经络数 |
| `leftLowCountAfter` | 第二组偏左经络数 |
| `rightLowCountAfter` | 第二组偏右经络数 |
| `dominantPatternBefore` | 第一组主偏向：left_low / right_low / mixed |
| `dominantPatternAfter` | 第二组主偏向：left_low / right_low / mixed |
| `crossCount` | 交叉经络总数 |

### 5.2 偏向判定

| 条件 | 结果 |
|------|------|
| 左低数 > 右低数 | `left_low` |
| 右低数 > 左低数 | `right_low` |
| 相等或差异不明显 | `mixed` |

**重要：** 第一组和第二组的偏向分别记录，支持"第一组偏右、第二组偏左"这类动态描述（来自 report-structure-overview 案例要求）。

---

## 6. Step 5：最低温与组合规则

### 6.1 最低温

分别计算 `lowestMeridianBefore` 和 `lowestMeridianAfter`，输出 `{meridian, side, value}`。

### 6.2 组合规则（8 条核心规则）

严格按 rule-library-prd 第 4 节和 infer-engine-flow Step 5 定义：

| 规则 ID | 规则名 | 触发条件 |
|---------|--------|---------|
| `combo_heart_supply` | 心脏供血关注 | 第一组或第二组中 >= 4 条经络偏右 |
| `combo_head_supply` | 头部供血关注 | 第一组或第二组中 >= 4 条经络偏左 |
| `combo_waist` | 腰椎风险提示 | 肾经与膀胱经同侧异常（beforeLowSide 相同且非 None） |
| `combo_neck` | 颈椎风险提示 | 肾经、膀胱经、脾经三条 beforeStatus 均非 balanced |
| `combo_reproductive` | 生殖系统关注 | 肾经 cross + 膀胱经 cross |
| `combo_liver_gall` | 肝胆代谢关注 | 肝经 beforeStatus 非 balanced + 胆经 beforeStatus 非 balanced |
| `combo_liver_gall_spleen_mass` | 结节/囊肿/息肉风险 | 胆经 beforeStatus=left_low + 肝经 cross + 脾经 beforeStatus=right_low |
| `combo_multi_cross` | 多经络交叉失衡 | crossCount >= 3 |

### 6.3 组合规则优先级

| 优先级 | 规则 |
|--------|------|
| A | combo_heart_supply, combo_head_supply, combo_waist, combo_neck, combo_reproductive, combo_liver_gall_spleen_mass, combo_multi_cross |
| B | combo_liver_gall, combo_intestine_lung |

---

## 7. Step 6 + 7：综合评分算法

### 7.1 评分原则

- 综合评分范围：**0–100**，分数越高表示整体状态越好
- 采用"**基础分 100 − 扣分 + 小幅加分**"的逻辑
- 评分由两层组成：`rawScore`（真实计算）和 `displayedScore`（复测保护后）
- **这是一个整体综合分，不是每条经络独立打分再取平均**

### 7.2 评分维度参考权重

| 维度 | 权重 | 考虑因素 |
|------|------|---------|
| 整体平衡度 | 30 分 | 左右温差、偏左/偏右经络数量、整体偏侧情况 |
| 交叉失衡程度 | 20 分 | 是否交叉、交叉数量、是否存在关键双交叉（如肾+膀胱） |
| 重点经络状态 | 20 分 | 重点关注肝、脾、肾、膀胱；胃、胆次一级 |
| 组合风险程度 | 20 分 | 命中心脏供血、头部供血、颈椎、腰椎、生殖系统、肠道/肺、结节风险 |
| 调理响应度 | 10 分 | 第二组是否更趋于平衡、多条经络是否改善 |

> 以上权重为设计参考，实际通过下方扣分/加分规则实现。

### 7.3 扣分规则

从 100 分开始，按以下规则逐项扣除：

**单经扣分（遍历 6 条经络）：**

| 条件 | 扣分 | 说明 |
|------|------|------|
| severity = mild | -2 | 轻度异常 |
| severity = medium 或 high | -4 | 明显异常 |
| cross = true | -4 | 该经络存在交叉 |

**全局扣分（跨经络联动）：**

| 条件 | 扣分 | 说明 |
|------|------|------|
| 肾经 cross + 膀胱经 cross | -8 | 肾膀胱双交叉 |
| crossCount >= 3 | -8 | 多经络交叉失衡 |
| rightLowCount(before 或 after) >= 4 | -6 | 4 条及以上偏右 |
| leftLowCount(before 或 after) >= 4 | -6 | 4 条及以上偏左 |
| 命中 combo_heart_supply | -6 | 心脏供血 |
| 命中 combo_head_supply | -6 | 头部供血 |
| 命中 combo_neck/combo_waist/combo_reproductive 任一 | -5 | 颈椎/腰椎/生殖系统 |
| 命中 combo_liver_gall_spleen_mass | -6 | 结节/囊肿/息肉风险 |
| 异常经络数（beforeStatus 或 afterStatus 非 balanced）>= 4 | -8 | 多经络失衡 |

### 7.4 加分规则

| 条件 | 加分 | 说明 |
|------|------|------|
| >= 3 条经络 afterDiff < beforeDiff | +4 | 多条经络改善 |
| >= 1 条经络 afterDiff < beforeDiff（不满足 3 条时） | +2 | 部分改善 |
| 无交叉且整体平衡较好 | +3 | 整体稳定 |

### 7.5 分值边界

```
rawScore = max(30, min(100, rawScore))
```

- 上限：100
- 下限：30（避免极端低分造成用户恐慌）

### 7.6 评分计算伪代码

```python
raw_score = 100

# 单经扣分
for m, s in meridian_states.items():
    if s["severity"] == "mild":
        raw_score -= 2
    elif s["severity"] in ["medium", "high"]:
        raw_score -= 4
    if s["cross"]:
        raw_score -= 4

# 肾膀胱双交叉
if kidney["cross"] and bladder["cross"]:
    raw_score -= 8

# 多经络交叉
if cross_count >= 3:
    raw_score -= 8

# 偏侧扣分
if right_before >= 4 or right_after >= 4:
    raw_score -= 6
if left_before >= 4 or left_after >= 4:
    raw_score -= 6

# 组合命中扣分
if "combo_heart_supply" in combination_hits:
    raw_score -= 6
if "combo_head_supply" in combination_hits:
    raw_score -= 6
if any(c in combination_hits for c in ["combo_neck", "combo_waist", "combo_reproductive"]):
    raw_score -= 5
if "combo_liver_gall_spleen_mass" in combination_hits:
    raw_score -= 6

# 多经络失衡
abnormal_count = sum(
    1 for s in meridian_states.values()
    if s["beforeStatus"] != "balanced" or s["afterStatus"] != "balanced"
)
if abnormal_count >= 4:
    raw_score -= 8

# 上下界
raw_score = max(30, min(100, raw_score))

# 改善加分
improved_count = sum(
    1 for s in meridian_states.values()
    if s["afterDiff"] < s["beforeDiff"]
)
if improved_count >= 3:
    raw_score += 4
elif improved_count >= 1:
    raw_score += 2

# 再次上下界
raw_score = max(30, min(100, raw_score))
```

---

## 8. Step 8：复测保护规则

### 8.1 规则目的

若客户在两次测量之间持续使用仪器，则复测展示给客户的综合评分不应低于上次展示分。

### 8.2 核心字段

| 字段 | 说明 |
|------|------|
| `isFollowup` | 是否复测 |
| `previousDisplayedScore` | 上次展示给客户的分数 |
| `instrumentUsageDaysBetweenMeasurements` | 两次检测之间使用仪器的天数 |
| `minUsageDaysForProtection` | 触发保护的最小天数阈值（初版 = 7） |
| `adherenceFlag` | 是否达到持续使用条件 |
| `scoreAdjustedByPolicy` | 是否触发保护规则 |

### 8.3 触发条件（全部同时满足）

1. `isFollowup == true`
2. `previousDisplayedScore` 存在
3. `instrumentUsageDaysBetweenMeasurements >= 7`
4. `currentRawScore < previousDisplayedScore`

### 8.4 处理逻辑

```
if isFollowup == true
   AND previousDisplayedScore exists
   AND instrumentUsageDaysBetweenMeasurements >= 7
   AND currentRawScore < previousDisplayedScore
then:
   displayedScore = previousDisplayedScore
   scoreAdjustedByPolicy = true
else:
   displayedScore = currentRawScore
   scoreAdjustedByPolicy = false
```

### 8.5 异常与边界处理

| 场景 | 处理方式 |
|------|---------|
| 首次检测 | 不输入 instrumentUsageDays，不应用保护规则 |
| 复测但未使用仪器 | instrumentUsageDays=0，不触发保护，按 rawScore 展示 |
| 复测但缺少上次分数 | 不触发保护，按 rawScore 展示 |
| 复测使用天数 < 0 | 前端拦截 |
| 复测使用天数 > 365 | 前端提示重新确认 |

---

## 9. Step 9：评分分级映射

| 分数 | 等级 | 展示语 |
|------|------|--------|
| 90–100 | 整体状态较好 | 当前整体状态较平稳，请继续保持。 |
| 75–89 | 轻度失衡 | 整体状态尚可，局部仍需关注。 |
| 60–74 | 中度失衡 | 存在较明确失衡，建议持续调理。 |
| 0–59 | 需重点关注 | 当前失衡较明显，建议尽早重视。 |

---

## 10. Step 10：建议标签映射

| 触发条件 | 标签 |
|----------|------|
| 胃经 beforeStatus=right_low | `stomach_cold` |
| 脾经 beforeStatus=right_low | `spleen_damp` |
| 肾经 beforeStatus=right_low | `kidney_yang_weak` |
| 肝经 beforeStatus=right_low | `liver_blood_weak` |
| 胆经 beforeStatus 非 balanced | `gallbladder_metabolism_pressure` |
| 命中 combo_heart_supply | `heart_supply_attention` |
| 命中 combo_head_supply | `head_supply_attention` |
| 命中 combo_reproductive | `reproductive_system_attention` |

---

## 11. 报告输出结构

### 11.1 双层输出

严格按 infer-engine-flow Step 12 定义，同时输出两层：

**A. 引擎层（供调试/复盘，前端不展示）：**
- `engineInference`
- `scoreContext`
- `trace`

**B. 报告层（供前端展示）：**
- `healthScore`
- `overallAssessment`
- `keyFindings`
- `meridianDetails`
- `combinationAnalysis`
- `advice`
- `encouragementBanner`
- `disclaimer`

### 11.2 引擎层输出结构

```json
{
  "engineInference": {
    "dominantPatternBefore": "right_low",
    "dominantPatternAfter": "left_low",
    "lowestMeridianBefore": { "meridian": "gallbladder", "side": "left", "value": 37.4 },
    "lowestMeridianAfter": { "meridian": "kidney", "side": "left", "value": 37.4 },
    "meridianStates": {
      "liver": {
        "beforeStatus": "left_low", "afterStatus": "balanced",
        "beforeLowSide": "left", "afterLowSide": null,
        "beforeDiff": 0.6, "afterDiff": 0.1,
        "cross": false, "severity": "medium"
      }
    },
    "combinationHits": ["combo_reproductive", "combo_heart_supply"]
  },
  "scoreContext": {
    "currentRawScore": 68,
    "displayedScore": 72,
    "scoreLevel": "轻度失衡",
    "scoreSummary": "整体状态尚可，局部仍需关注。",
    "instrumentUsageDaysBetweenMeasurements": 25,
    "adherenceFlag": true,
    "scoreAdjustedByPolicy": true
  },
  "trace": {
    "meridianDiffs": {
      "liver": { "beforeDiff": 0.6, "afterDiff": 0.1, "cross": false, "severity": "medium" }
    },
    "combinationHits": ["combo_reproductive", "combo_heart_supply"],
    "scoreBreakdown": [
      { "rule": "single_meridian_obvious_abnormal", "score": -4, "target": "kidney" },
      { "rule": "single_meridian_cross", "score": -4, "target": "kidney" },
      { "rule": "kidney_bladder_double_cross", "score": -8 },
      { "rule": "combo_heart_supply", "score": -6 }
    ],
    "improvementBonus": { "improvedCount": 3, "bonus": 4 },
    "followupPolicy": {
      "triggered": true,
      "rawScore": 68,
      "previousDisplayedScore": 72,
      "displayedScore": 72
    }
  }
}
```

### 11.3 报告层输出结构

严格按 ai-report-prd 第 6 节定义的 8 个模块：

```json
{
  "healthScore": {
    "score": 72,
    "level": "轻度失衡",
    "summary": "整体状态尚可，局部仍需关注。"
  },
  "overallAssessment": {
    "overallLevel": "整体存在一定失衡",
    "dominantPattern": "前后两组左右偏向变化较明显",
    "focusMeridians": ["肾经", "膀胱经", "肝经"],
    "stableMeridians": ["胃经"],
    "summaryText": "..."
  },
  "keyFindings": [
    {
      "title": "生殖系统相关风险需重点关注",
      "level": "高",
      "description": "肾经与膀胱经同时出现交叉变化...",
      "evidence": ["肾经交叉", "膀胱经交叉"]
    }
  ],
  "meridianDetails": [
    {
      "meridian": "肝经",
      "status": "交叉",
      "mainLabel": "先藏血不足，后代谢偏弱",
      "riskPoints": ["贫血倾向", "结节风险"],
      "description": "..."
    }
  ],
  "combinationAnalysis": [
    {
      "comboName": "肾膀胱交叉联动",
      "description": "肾经与膀胱经共同异常时..."
    }
  ],
  "advice": {
    "priorityDirections": ["优先关注肾经与膀胱经相关调理"],
    "lifestyleAdvice": ["注意休息，避免长期劳累和透支"],
    "wellnessAdvice": ["保持规律作息，尽量减少熬夜"],
    "retestAdvice": "后续复测时，重点观察肾经、膀胱经的变化。"
  },
  "encouragementBanner": {
    "text": "每天坚持踩生物能量仪+喝健康安全好水：即可越来越健康美丽哦"
  },
  "disclaimer": {
    "text": "本报告基于经络温度数据生成，用于日常健康管理参考，不等同于医疗诊断结论。如有长期不适，建议结合专业检查进一步评估。"
  }
}
```

### 11.4 前端模块与字段映射

| 前端模块 | 数据字段 |
|----------|---------|
| 1. 亚健康综合评分 | `healthScore` |
| 2. 整体概况 | `overallAssessment` |
| 3. 核心关注结论 | `keyFindings`（固定 2~3 条，优先输出组合判断） |
| 4. 六经络明细 | `meridianDetails`（6 条全要，含平衡项，胃经次要） |
| 5. 综合分析 | `combinationAnalysis`（组合规则层，不重复六经络明细） |
| 6. 生活方式与养生建议 | `advice` |
| 7. 信心提醒 | `encouragementBanner`（固定文案，不由模型生成） |
| 8. 报告说明 | `disclaimer`（固定文案） |

### 11.5 前端展示原则

**只展示：**
- `displayedScore`（通过 `healthScore.score`）
- 标准报告八模块内容

**不展示：**
- `rawScore`
- `trace`
- `scoreAdjustedByPolicy` 等调试字段

---

## 12. 经络主规则

严格按 rule-library-prd 第 3 节定义。每条经络的三种状态（left_low / right_low / cross）对应不同的标签和提示点：

| 经络 | left_low 标签 | right_low 标签 | cross 标签 |
|------|-------------|---------------|-----------|
| 肝经 | 代谢偏弱/气虚倾向 | 血虚/藏血不足 | 气血两虚 |
| 脾经 | 脾气偏虚 | 湿气偏重 | 血糖/代谢紊乱 |
| 肾经 | 肾阴偏虚 | 肾阳偏虚 | 阴阳两虚 |
| 胃经 | 胃部津液偏少 | 胃阳不足/胃寒 | 胃经功能失衡 |
| 胆经 | 胆经偏弱 | 胆脂代谢需关注 | 胆经交叉失衡 |
| 膀胱经 | 肩颈腰与肠道方向 | 湿下注与腰部方向 | 膀胱经交叉失衡 |

> 详细提示点见 rule-library-prd 第 3.2 节，此处不重复。

---

## 13. 养生建议映射

严格按 rule-library-prd 第 7 节定义。tag → 建议的映射关系：

| tag | 优先调理方向 | 生活方式建议 | 具体养生建议 |
|-----|-------------|-------------|-------------|
| `stomach_cold` | 温胃、调理胃部功能 | 饮食规律，少食寒凉 | 三餐规律，少空腹，减少冰凉刺激 |
| `spleen_damp` | 健脾、祛湿 | 少甜少油少黏腻 | 适量活动，关注排湿和大便状态 |
| `kidney_yang_weak` | 温养肾阳 | 腰腹四肢保暖，避免过劳 | 作息规律，减少熬夜 |
| `liver_blood_weak` | 养肝、补血、改善循环 | 注意休息，减少熬夜 | 规律作息，重视气血调养 |
| `gallbladder_metabolism_pressure` | 关注肝胆代谢 | 饮食清淡，少高脂 | 规律作息，减轻代谢负担 |
| `heart_supply_attention` | 关注循环与供血状态 | 避免劳累 | 关注心悸乏力，保持节律稳定 |
| `head_supply_attention` | 关注头部循环状态 | 避免熬夜，减少脑力透支 | 注意睡眠，关注精神状态 |
| `reproductive_system_attention` | 关注生殖系统方向 | 注意休息保暖 | 关注腰腹及周期性不适 |

---

## 14. 边界与禁用规则

严格按 rule-library-prd 第 8 节定义：

**全部剔除：** 风水、男女/生育判断、体质偏父母、梦境、现场问询、成交话术、过度主观评价、明确疾病诊断

**需模糊化：** 肺部结节 → "肺部情况需关注"；决断力弱 → "精神状态可能受身体状态影响"；结节/囊肿 → "相关方向风险需关注"

---

## 15. 代码模块划分

严格按 infer-engine-flow 第 4 节建议：

| 函数 | 职责 |
|------|------|
| `load_input()` | 读取输入数据 |
| `validate_input()` | 校验输入完整性 |
| `compute_meridian_states()` | 计算单经状态（status, cross, severity） |
| `compute_global_patterns()` | 计算整体偏侧与交叉情况 |
| `find_lowest_meridian()` | 查找最低温经络 |
| `apply_combination_rules()` | 计算组合规则命中 |
| `calculate_raw_score()` | 计算原始综合评分 |
| `apply_improvement_bonus()` | 计算改善加分 |
| `apply_followup_policy()` | 应用复测保护规则 |
| `map_score_level()` | 计算评分等级与摘要 |
| `collect_advice_tags()` | 生成建议标签 |
| `build_model_payload()` | 组装模型输入上下文 |
| `build_final_output()` | 组装最终输出结构 |

---

## 16. 配置文件结构

### 16.1 JSON 文件清单

| 文件 | 对应规则层 |
|------|-----------|
| `rules/meridian_rules.json` | 单经判断（标签、提示点） |
| `rules/combination_rules.json` | 组合判断（8 条核心规则） |
| `rules/score_rules.json` | 综合评分（扣分/加分/分级） |
| `rules/wellness_advice_rules.json` | 建议生成（tag → 建议映射） |
| `rules/followup_policy_rules.json` | 复测保护策略 |

### 16.2 score_rules.json

```json
{
  "version": "2.0",
  "base_score": 100,
  "min_score": 30,
  "max_score": 100,
  "balance_threshold": 0.2,
  "severity_thresholds": {
    "mild_max": 0.5,
    "medium_max": 1.0
  },
  "deductions": [
    { "rule_id": "single_meridian_mild_abnormal", "condition": "severity == mild", "per_meridian": true, "score": -2 },
    { "rule_id": "single_meridian_obvious_abnormal", "condition": "severity in [medium, high]", "per_meridian": true, "score": -4 },
    { "rule_id": "single_meridian_cross", "condition": "cross == true", "per_meridian": true, "score": -4 },
    { "rule_id": "kidney_bladder_double_cross", "condition": "kidney.cross AND bladder.cross", "score": -8 },
    { "rule_id": "multi_cross", "condition": "cross_count >= 3", "score": -8 },
    { "rule_id": "right_bias", "condition": "right_low_count >= 4 (before or after)", "score": -6 },
    { "rule_id": "left_bias", "condition": "left_low_count >= 4 (before or after)", "score": -6 },
    { "rule_id": "heart_supply_hit", "condition": "combo_heart_supply in hits", "score": -6 },
    { "rule_id": "head_supply_hit", "condition": "combo_head_supply in hits", "score": -6 },
    { "rule_id": "neck_waist_reproductive_hit", "condition": "combo_neck/waist/reproductive in hits", "score": -5 },
    { "rule_id": "mass_risk_hit", "condition": "combo_liver_gall_spleen_mass in hits", "score": -6 },
    { "rule_id": "multi_imbalance", "condition": "abnormal_meridian_count >= 4", "score": -8 }
  ],
  "bonuses": [
    { "rule_id": "multiple_meridians_improved", "condition": "improved_count >= 3", "score": 4 },
    { "rule_id": "partial_improvement", "condition": "improved_count >= 1", "score": 2 },
    { "rule_id": "overall_stable", "condition": "no_cross AND good_balance", "score": 3 }
  ],
  "score_levels": [
    { "min": 90, "max": 100, "level": "整体状态较好", "summary": "当前整体状态较平稳，请继续保持。" },
    { "min": 75, "max": 89, "level": "轻度失衡", "summary": "整体状态尚可，局部仍需关注。" },
    { "min": 60, "max": 74, "level": "中度失衡", "summary": "存在较明确失衡，建议持续调理。" },
    { "min": 30, "max": 59, "level": "需重点关注", "summary": "当前失衡较明显，建议尽早重视。" }
  ]
}
```

### 16.3 followup_policy_rules.json

```json
{
  "version": "1.0",
  "minUsageDaysForProtection": 7,
  "preventScoreDecreaseWhenAdherent": true,
  "allowStableOrImprovedFollowupMessaging": true,
  "rules": [
    {
      "rule_id": "followup_score_protection",
      "enabled": true,
      "condition": {
        "isFollowup": true,
        "requiresPreviousDisplayedScore": true,
        "minUsageDays": 7,
        "whenCurrentRawScoreLowerThanPreviousDisplayedScore": true
      },
      "action": {
        "displayedScore": "use_previousDisplayedScore",
        "scoreAdjustedByPolicy": true
      }
    }
  ]
}
```

---

## 17. 与当前实现的差异与改造要点

### 17.1 数据模型改造

| 当前实现 | PRD v2.0 | 改造要点 |
|----------|----------|---------|
| 单组数据 left/right + trendDelta | before/after 两组数据 | 输入结构重构 |
| 温度绝对值阈值（lowMin=35.3, highMax=36.9） | 左右温差 diffAbs + balanceThreshold=0.2 | 状态判定逻辑重写 |
| cross 基于温差超阈值 | cross 基于 before/after 偏侧方向相反 | 交叉定义重写 |
| severity 不存在 | severity 基于 diffAbs: 0.2/0.5/1.0 | 新增 |

### 17.2 评分模型改造

| 当前实现 | PRD v2.0 | 改造要点 |
|----------|----------|---------|
| 每条经络独立 100 分，取平均 | 整体综合分 100 分 | 评分架构重写 |
| 固定扣分（left_low -16, cross -20） | 按 severity 分级扣分（mild -2, medium/high -4） | 扣分逻辑重写 |
| 无加分 | 改善加分 +2/+4，稳定加分 +3 | 新增 |
| combo 统一 -6 对涉及经络 | 组合规则对综合分扣 -5/-6 | 改为全局扣分 |
| 分级 85/70/55 | 分级 90/75/60 | 调整 |
| 下限 0 | 下限 30 | 调整 |
| 无复测保护 | rawScore / displayedScore 双分数 | 新增 |

### 17.3 输出结构改造

| 当前实现 | PRD v2.0 | 改造要点 |
|----------|----------|---------|
| healthScore 为数字 | healthScore 为对象 {score, level, summary} | 结构变更 |
| 无 overallAssessment | 新增 dominantPattern before/after | 新增 |
| 无 keyFindings | 新增 2~3 条核心关注结论 | 新增 |
| 无 combinationAnalysis | 新增组合分析模块 | 新增 |
| advice 为数组 | advice 为结构化对象 | 结构变更 |
| 无 encouragementBanner | 固定文案 | 新增 |
| 无 disclaimer | 固定文案 | 新增 |
| 无 scoreContext | 新增 rawScore/displayedScore/adherenceFlag | 新增 |

### 17.4 需要修改的文件

| 文件 | 改动要点 |
|------|---------|
| `scripts/infer.py` | 核心重写：before/after 数据模型、severity、整体综合分、加分、复测保护、新输出结构 |
| `rules/thresholds.json` | 移除 scoring.penalty，仅保留温度基础阈值 |
| `rules/meridian_rules.json` | 重构为 rule-library-prd 第 10.1 节结构（按 left_low/right_low/cross 组织标签和提示点） |
| `rules/combination_rules.json` | 重构为 rule-library-prd 第 10.2 节结构（8 条核心规则，含 trigger 定义） |
| `scripts/test_infer.py` | 全面重写测试用例 |

### 17.5 需要新建的文件

| 文件 | 用途 |
|------|------|
| `rules/score_rules.json` | 综合评分规则 |
| `rules/wellness_advice_rules.json` | 养生建议映射 |
| `rules/followup_policy_rules.json` | 复测保护策略 |

---

## 18. 实施阶段

| 阶段 | 内容 | 优先级 |
|------|------|--------|
| Phase 1 | 输入结构改造（before/after 模型）+ 输入校验 | P0 |
| Phase 2 | 单经状态计算（status, cross, severity）+ 整体偏侧 | P0 |
| Phase 3 | 组合规则（8 条核心规则）+ 最低温 | P0 |
| Phase 4 | 综合评分算法（扣分 + 加分）+ 分级映射 | P0 |
| Phase 5 | 复测保护机制 | P1 |
| Phase 6 | 输出结构改造（engineInference + scoreContext + reportPayload） | P0 |
| Phase 7 | 建议标签 + 养生建议映射 | P1 |
| Phase 8 | 规则配置文件落地（5 个 JSON） | P0 |
| Phase 9 | 测试用例全面重写 + 回归验证 | P0 |

---

## 19. 模型职责边界

> ⚠️ **核心原则：** 模型不负责算规则，只负责把规则结果组织成自然语言报告。

引擎负责：
- 所有状态判定
- 所有评分计算
- 所有组合规则匹配
- 所有建议标签收集
- 复测保护

模型负责：
- 基于引擎输出生成 8 个模块的自然语言文本
- 保持风格统一：专业、通俗、易懂、不生硬、不广告化
