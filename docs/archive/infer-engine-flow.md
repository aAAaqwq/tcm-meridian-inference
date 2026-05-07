# 六条经络推理引擎流程说明（infer.py）

## 1. 整体执行顺序

推理引擎按以下 9 步执行：

1. 读取输入数据
2. 校验输入完整性
3. 计算单经状态
4. 计算整体偏侧与交叉情况
5. 计算组合规则命中
6. 计算原始综合评分 rawScore
7. 应用复测保护规则，得到 displayedScore
8. 生成建议标签与报告输入上下文
9. 输出标准化 JSON 结果

---

## 2. 输入输出关系

### 输入

来源于前端和后端规则层，包含：

- 用户信息
- 首测/复测标记
- 六经两组左右温度
- 两次测量之间使用仪器天数
- 上次展示分（复测时）

### 输出

输出给模型/前端的结构化数据，包含：

- 单经结果
- 组合规则
- 评分结果
- 建议标签
- 标准报告结构字段
- trace 调试信息

---

## 3. 详细计算步骤

### Step 1：读取输入数据

**目标：** 把接口输入统一解析成内部可用对象。

**输入重点字段：**

- `subject`
- `measurementSession`
- `measurements.before`
- `measurements.after`
- `scoreContext.previousDisplayedScore`（复测时）

**输出：** 内部对象 `subject`、`session`、`beforeMeasurements`、`afterMeasurements`、`previous_displayed_score`

```python
input_data = load_input()

subject = input_data["subject"]
session = input_data["measurementSession"]
before = input_data["measurements"]["before"]
after = input_data["measurements"]["after"]
previous_displayed_score = input_data.get("scoreContext", {}).get("previousDisplayedScore")
```

---

### Step 2：校验输入完整性

**目标：** 防止缺字段、错格式、缺经络导致后面规则失真。

**校验内容：**

- 是否包含 6 条经络
- 每条经络是否有 `left` / `right`
- `before` / `after` 是否都存在
- 若 `isFollowup == true`，是否填写 `instrumentUsageDaysBetweenMeasurements`

**失败处理：** 返回错误码，不进入后续推理。

```python
required_meridians = ["liver", "spleen", "kidney", "stomach", "gallbladder", "bladder"]

for m in required_meridians:
    assert m in before and m in after
    assert "left" in before[m] and "right" in before[m]
    assert "left" in after[m] and "right" in after[m]

if session["isFollowup"]:
    assert "instrumentUsageDaysBetweenMeasurements" in session
```

---

### Step 3：计算单经状态

**目标：** 先得到每条经络在两组数据中的基础状态。

**需要输出的内容（每条经络）：**

- `beforeStatus`
- `afterStatus`
- `cross`
- `beforeLowSide`
- `afterLowSide`
- `beforeDiff`
- `afterDiff`
- `severity`

**状态定义：**

| 状态 | 条件 |
|---|---|
| `balanced` | `abs(left - right) <= balanceThreshold` |
| `left_low` | `left < right` |
| `right_low` | `right < left` |

**交叉定义：** 第一组低侧 ≠ 第二组低侧，且两组都不是 `balanced` → `cross = true`

**平衡阈值：** `balanceThreshold = 0.2`

**严重程度分层：**

| 温差范围 | 程度 |
|---|---|
| 0 ~ 0.2 | balanced |
| 0.2 ~ 0.5 | mild |
| 0.5 ~ 1.0 | medium |
| > 1.0 | high |

```python
def get_side_status(left, right, balance_threshold=0.2):
    diff = abs(left - right)
    if diff <= balance_threshold:
        return "balanced", None, diff
    elif left < right:
        return "left_low", "left", diff
    else:
        return "right_low", "right", diff


def get_severity(diff):
    if diff <= 0.2:
        return "balanced"
    elif diff <= 0.5:
        return "mild"
    elif diff <= 1.0:
        return "medium"
    else:
        return "high"


meridian_states = {}

for meridian in required_meridians:
    before_status, before_side, before_diff = get_side_status(
        before[meridian]["left"], before[meridian]["right"]
    )
    after_status, after_side, after_diff = get_side_status(
        after[meridian]["left"], after[meridian]["right"]
    )

    cross = (
        before_status in ["left_low", "right_low"]
        and after_status in ["left_low", "right_low"]
        and before_side != after_side
    )

    severity = get_severity(max(before_diff, after_diff))

    meridian_states[meridian] = {
        "beforeStatus": before_status,
        "afterStatus": after_status,
        "beforeLowSide": before_side,
        "afterLowSide": after_side,
        "beforeDiff": before_diff,
        "afterDiff": after_diff,
        "cross": cross,
        "severity": severity
    }
```

---

### Step 4：计算整体偏侧与交叉情况

**目标：** 为整体概况、组合规则、评分做准备。

**需要输出的内容：**

- `leftLowCountBefore`
- `rightLowCountBefore`
- `leftLowCountAfter`
- `rightLowCountAfter`
- `dominantPatternBefore`
- `dominantPatternAfter`
- `crossCount`

**偏侧定义：**

| 条件 | 结果 |
|---|---|
| 左低数量 > 右低数量 | `left_low` |
| 右低数量 > 左低数量 | `right_low` |
| 相等或差异不明显 | `mixed` |

```python
left_before = 0
right_before = 0
left_after = 0
right_after = 0
cross_count = 0

for m, s in meridian_states.items():
    if s["beforeStatus"] == "left_low":
        left_before += 1
    elif s["beforeStatus"] == "right_low":
        right_before += 1

    if s["afterStatus"] == "left_low":
        left_after += 1
    elif s["afterStatus"] == "right_low":
        right_after += 1

    if s["cross"]:
        cross_count += 1


def dominant_pattern(left_count, right_count):
    if left_count > right_count:
        return "left_low"
    elif right_count > left_count:
        return "right_low"
    else:
        return "mixed"


dominant_before = dominant_pattern(left_before, right_before)
dominant_after = dominant_pattern(left_after, right_after)
```

---

### Step 5：计算最低温与组合规则命中

#### 5.1 先算最低温

分别计算：

- `lowestMeridianBefore`
- `lowestMeridianAfter`

```python
def find_lowest_meridian(measurements):
    lowest = None
    for meridian, vals in measurements.items():
        for side in ["left", "right"]:
            value = vals[side]
            if lowest is None or value < lowest["value"]:
                lowest = {
                    "meridian": meridian,
                    "side": side,
                    "value": value
                }
    return lowest


lowest_before = find_lowest_meridian(before)
lowest_after = find_lowest_meridian(after)
```

#### 5.2 再算组合规则命中

按 `combination_rules.json` 逐条跑。

**输出：**

- `combinationHits[]` — 每条命中的 `rule_id`
- 每条命中的 `title`、`description`、`evidence`

**优先实现的 8 条核心规则：**

| 规则 | 触发条件 |
|---|---|
| `combo_heart_supply` | 第一组或整体统计中，4条及以上经络偏右 |
| `combo_head_supply` | 第一组或整体统计中，4条及以上经络偏左 |
| `combo_waist` | 肾经与膀胱经同侧异常 |
| `combo_neck` | 肾经、膀胱经、脾经共同异常 |
| `combo_reproductive` | 肾经交叉 + 膀胱经交叉 |
| `combo_liver_gall` | 肝经异常 + 胆经异常 |
| `combo_liver_gall_spleen_mass` | 胆经左低 + 肝经交叉/异常 + 脾经右低 |
| `combo_multi_cross` | 交叉经络数量 >= 3 |

```python
combination_hits = []

# 心脏供血
if right_before >= 4 or right_after >= 4:
    combination_hits.append("combo_heart_supply")

# 头部供血
if left_before >= 4 or left_after >= 4:
    combination_hits.append("combo_head_supply")

kidney = meridian_states["kidney"]
bladder = meridian_states["bladder"]
spleen = meridian_states["spleen"]
liver = meridian_states["liver"]
gall = meridian_states["gallbladder"]

# 腰椎：肾与膀胱同侧异常
if kidney["beforeLowSide"] is not None and kidney["beforeLowSide"] == bladder["beforeLowSide"]:
    combination_hits.append("combo_waist")

# 颈椎：肾、膀胱、脾共同异常
if (kidney["beforeStatus"] != "balanced"
        and bladder["beforeStatus"] != "balanced"
        and spleen["beforeStatus"] != "balanced"):
    combination_hits.append("combo_neck")

# 生殖系统：肾+膀胱双交叉
if kidney["cross"] and bladder["cross"]:
    combination_hits.append("combo_reproductive")

# 肝胆联动
if liver["beforeStatus"] != "balanced" and gall["beforeStatus"] != "balanced":
    combination_hits.append("combo_liver_gall")

# 肝胆脾结节风险
if (gall["beforeStatus"] == "left_low"
        and liver["cross"]
        and spleen["beforeStatus"] == "right_low"):
    combination_hits.append("combo_liver_gall_spleen_mass")

# 多经络交叉
if cross_count >= 3:
    combination_hits.append("combo_multi_cross")
```

---

### Step 6：计算原始综合评分 rawScore

**目标：** 根据单经异常、交叉、组合命中等规则计算原始分。

**建议顺序：**

1. 从 100 分开始
2. 遍历单经扣分
3. 遍历交叉扣分
4. 遍历组合命中扣分
5. 计算改善情况加分
6. 限制上下界

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
abnormal_meridian_count = sum(
    1 for s in meridian_states.values()
    if s["beforeStatus"] != "balanced" or s["afterStatus"] != "balanced"
)
if abnormal_meridian_count >= 4:
    raw_score -= 8

# 上下界限制
raw_score = max(30, min(100, raw_score))
```

---

### Step 7：计算改善加分

**目标：** 体现第二组趋于平衡的正向变化。

```python
improved_count = 0

for m, s in meridian_states.items():
    if s["afterDiff"] < s["beforeDiff"]:
        improved_count += 1

if improved_count >= 3:
    raw_score += 4
elif improved_count >= 1:
    raw_score += 2

# 再次上下界限制
raw_score = max(30, min(100, raw_score))
```

---

### Step 8：应用复测保护规则，得到 displayedScore

**目标：** 满足业务要求——如果客户持续使用仪器，复测展示分不能下降。

**关键字段：**

- `isFollowup`
- `instrumentUsageDaysBetweenMeasurements`
- `previousDisplayedScore`

```python
displayed_score = raw_score
score_adjusted_by_policy = False

usage_days = session.get("instrumentUsageDaysBetweenMeasurements", 0)
is_followup = session.get("isFollowup", False)

adherence_flag = usage_days >= 7

if (
    is_followup
    and previous_displayed_score is not None
    and adherence_flag
    and raw_score < previous_displayed_score
):
    displayed_score = previous_displayed_score
    score_adjusted_by_policy = True
```

---

### Step 9：计算评分等级与摘要

```python
def score_level_and_summary(score):
    if score >= 90:
        return "整体状态较好", "当前整体状态较平稳，请继续保持。"
    elif score >= 75:
        return "轻度失衡", "整体状态尚可，局部仍需关注。"
    elif score >= 60:
        return "中度失衡", "存在较明确失衡，建议持续调理。"
    else:
        return "需重点关注", "当前失衡较明显，建议尽早重视。"


score_level, score_summary = score_level_and_summary(displayed_score)
```

---

### Step 10：生成建议标签

**目标：** 把单经和组合命中转成建议系统可识别的 `tags`。

**标签映射：**

| 触发条件 | 标签 |
|---|---|
| 胃右低 | `stomach_cold` |
| 脾右低 | `spleen_damp` |
| 肾右低 | `kidney_yang_weak` |
| 肝右低 | `liver_blood_weak` |
| 胆异常 | `gallbladder_metabolism_pressure` |
| 心脏供血命中 | `heart_supply_attention` |
| 头部供血命中 | `head_supply_attention` |
| 生殖系统命中 | `reproductive_system_attention` |

```python
advice_tags = set()

if meridian_states["stomach"]["beforeStatus"] == "right_low":
    advice_tags.add("stomach_cold")

if meridian_states["spleen"]["beforeStatus"] == "right_low":
    advice_tags.add("spleen_damp")

if meridian_states["kidney"]["beforeStatus"] == "right_low":
    advice_tags.add("kidney_yang_weak")

if meridian_states["liver"]["beforeStatus"] == "right_low":
    advice_tags.add("liver_blood_weak")

if meridian_states["gallbladder"]["beforeStatus"] != "balanced":
    advice_tags.add("gallbladder_metabolism_pressure")

if "combo_heart_supply" in combination_hits:
    advice_tags.add("heart_supply_attention")

if "combo_head_supply" in combination_hits:
    advice_tags.add("head_supply_attention")

if "combo_reproductive" in combination_hits:
    advice_tags.add("reproductive_system_attention")
```

---

### Step 11：组装模型输入上下文

**目标：** 模型不负责算规则，只负责把规则结果组织成自然语言报告。

**模型输入建议包含：**

- `healthScore`
- `overallAssessment`
- `meridianStates`
- `combinationHits`
- `adviceTags`
- `encouragementBanner`
- `disclaimer`

> ⚠️ **注意：** 不要让模型自行重新判断评分、组合规则是否命中、是否触发复测保护。

---

### Step 12：输出标准 JSON 结果

**同时输出两层：**

**A. 引擎层结果（供调试/复盘）：**

- `engineInference`
- `scoreContext`
- `trace`

**B. 报告层结果（供前端展示）：**

- `healthScore`
- `overallAssessment`
- `keyFindings`
- `meridianDetails`
- `combinationAnalysis`
- `advice`
- `encouragementBanner`
- `disclaimer`

```python
result = {
    "engineInference": {
        "dominantPatternBefore": dominant_before,
        "dominantPatternAfter": dominant_after,
        "lowestMeridianBefore": lowest_before,
        "lowestMeridianAfter": lowest_after,
        "meridianStates": meridian_states,
        "combinationHits": combination_hits
    },
    "scoreContext": {
        "currentRawScore": raw_score,
        "displayedScore": displayed_score,
        "scoreLevel": score_level,
        "instrumentUsageDaysBetweenMeasurements": usage_days,
        "adherenceFlag": adherence_flag,
        "scoreAdjustedByPolicy": score_adjusted_by_policy
    },
    "reportPayload": {
        "healthScore": {
            "score": displayed_score,
            "level": score_level,
            "summary": score_summary
        },
        "adviceTags": list(advice_tags)
    }
}
```

---

## 4. 代码模块划分

建议 `infer.py` 拆分为以下函数，避免所有逻辑堆在一起：

| 函数 | 职责 |
|---|---|
| `load_input()` | 读取输入数据 |
| `validate_input()` | 校验输入完整性 |
| `compute_meridian_states()` | 计算单经状态 |
| `compute_global_patterns()` | 计算整体偏侧与交叉情况 |
| `find_lowest_meridian()` | 查找最低温经络 |
| `apply_combination_rules()` | 计算组合规则命中 |
| `calculate_raw_score()` | 计算原始综合评分 |
| `apply_followup_policy()` | 应用复测保护规则 |
| `map_score_level()` | 计算评分等级与摘要 |
| `collect_advice_tags()` | 生成建议标签 |
| `build_model_payload()` | 组装模型输入上下文 |
| `build_final_output()` | 组装最终输出结构 |

---

## 5. 调试与 Trace 建议

引擎应保留一层 `trace`，至少记录：

- 每条经络 `before` / `after` 状态
- 哪些组合规则命中
- `rawScore` 扣分明细
- 是否触发复测保护
- `displayedScore` 与 `rawScore` 的差异原因

**trace 示例：**

```json
{
  "trace": {
    "meridianDiffs": {
      "liver": { "beforeDiff": 0.6, "afterDiff": 0.1, "cross": true }
    },
    "combinationHits": ["combo_reproductive", "combo_heart_supply"],
    "scoreBreakdown": [
      { "rule": "single_meridian_cross", "score": -4, "target": "kidney" },
      { "rule": "kidney_bladder_double_cross", "score": -8, "target": "kidney+bladder" }
    ],
    "followupPolicy": {
      "triggered": true,
      "rawScore": 68,
      "previousDisplayedScore": 72,
      "displayedScore": 72
    }
  }
}
```

> ⚠️ 前端不展示 `trace`，仅供开发、产品、调规则时使用。

---

## 6. 执行流程总图

```
输入数据
    │
    ▼
Step 1: load_input()
    │
    ▼
Step 2: validate_input() ──→ 失败 → 返回错误码
    │
    ▼
Step 3: compute_meridian_states()
    │
    ▼
Step 4: compute_global_patterns()
    │
    ▼
Step 5: find_lowest_meridian() + apply_combination_rules()
    │
    ▼
Step 6: calculate_raw_score()
    │
    ▼
Step 7: 计算改善加分
    │
    ▼
Step 8: apply_followup_policy() ──→ displayedScore
    │
    ▼
Step 9: map_score_level()
    │
    ▼
Step 10: collect_advice_tags()
    │
    ▼
Step 11: build_model_payload()
    │
    ▼
Step 12: build_final_output()
    │
    ▼
  输出
  ├── engineInference（调试用）
  ├── scoreContext（调试用）
  └── reportPayload（前端展示用）
```
