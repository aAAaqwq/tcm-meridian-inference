# 六条经络报告系统 PRD（v1.2）

## 1. 产品目标

本版本目标不是做"更像专家"的自由发挥报告，而是做一套：

- 用户能看懂
- 门店可稳定展示
- 后端可计算
- 模型可稳定生成
- 前端可模块化呈现

的标准化报告系统。

## 2. 适用范围

本版本适用于两类场景：

### 2.1 首次检测

输入本次两组测量数据，输出标准报告与综合评分。

### 2.2 复测

输入本次两组测量数据、上次评分、两次检测之间使用仪器天数等信息，输出标准报告与综合评分，并应用复测评分保护规则。

## 3. 核心业务规则

### 3.1 报告展示结构

前端报告统一按以下 8 个模块展示：

1. 亚健康综合评分
2. 整体概况
3. 核心关注结论
4. 六经络明细
5. 综合分析
6. 生活方式与养生建议
7. 信心提醒
8. 报告说明

### 3.2 模块说明

#### 模块1：亚健康综合评分

展示本次综合评分及评分等级。

**展示内容：**
- 综合评分（0–100）
- 评分等级
- 简短说明

**字段：**
- `healthScore.score`
- `healthScore.level`
- `healthScore.summary`

**分级建议：**
| 分数 | 等级 |
|---|---|
| 90–100 | 整体状态较好 |
| 75–89 | 轻度失衡 |
| 60–74 | 中度失衡 |
| 0–59 | 需重点关注 |

#### 模块2：整体概况

展示本次检测的整体状态。

**展示内容：**
- 整体状态
- 主要失衡方向
- 重点异常经络
- 相对平衡经络
- 总体说明

**字段：**
- `overallAssessment.overallLevel`
- `overallAssessment.dominantPattern`
- `overallAssessment.focusMeridians`
- `overallAssessment.stableMeridians`
- `overallAssessment.summaryText`

**补充说明：** 这里要支持"第一组偏右、第二组偏左"这类动态偏向描述，不能只写单一偏左/偏右。

#### 模块3：核心关注结论

提炼本次最需要优先关注的 2~3 个问题。

**展示内容：**
- 标题
- 关注程度
- 通俗说明
- 触发依据（可折叠）

**字段：** `keyFindings[]`

**要求：**
- 固定输出 2~3 条
- 不平均罗列六条经络
- 优先输出组合判断或最关键单经异常

#### 模块4：六经络明细

逐条呈现六经络当前状态。

**展示内容：**
- 经络名称
- 当前状态
- 主要提示
- 风险关注
- 简短说明

**字段：** `meridianDetails[]`

**经络包括：** 肝经、脾经、肾经、胃经、胆经、膀胱经

**要求：**
- 六条经络都要有
- 平衡项也要写
- 胃经保留为次要项

#### 模块5：综合分析

承接多经络联动产生的判断。

**展示内容包括但不限于：**
- 心脏供血
- 头部供血
- 颈椎
- 腰椎
- 生殖系统
- 肠道/肺
- 多经络交叉失衡

**字段：** `combinationAnalysis[]`

**要求：**
- 这里是组合规则层，不重复六经络明细
- 交叉失衡信息优先在本模块承接

#### 模块6：生活方式与养生建议

**展示内容：**
- 优先调理方向
- 生活方式建议
- 具体养生建议
- 复测建议

**字段：**
- `advice.priorityDirections[]`
- `advice.lifestyleAdvice[]`
- `advice.wellnessAdvice[]`
- `advice.retestAdvice`

**要求：**
- 养生建议要具体
- 不写成交话术
- 语言风格要专业、易懂、带适度关怀感

#### 模块7：信心提醒

**位置：** 在"报告说明"之前，固定文案，不由模型自由生成

**字段：** `encouragementBanner.text`

**固定文案：** 每天坚持踩生物能量仪+喝健康安全好水：即可越来越健康美丽哦

#### 模块8：报告说明

**字段：** `disclaimer.text`

**固定文案：** 本报告是根据经络温度数据做出的健康分析，主要用于日常健康管理和提前预防，不等同于医院的疾病诊断。如需进一步咨询和解读，请联系门店专业老师。

## 4. 前端录入需求

### 4.1 首次检测录入字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `subject.id` | string | 是 | 用户ID |
| `subject.name` | string | 否 | 用户姓名/昵称 |
| `subject.gender` | enum | 否 | male/female |
| `subject.age` | int | 否 | 年龄 |
| `measuredAt` | datetime | 是 | 检测时间 |
| 六经两组左右温度 | float | 是 | 六经两组左右温度 |

### 4.2 复测新增录入字段

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `isFollowup` | boolean | 是 | 是否复测 |
| `daysSinceLastMeasurement` | int | 否 | 距离上次检测间隔天数 |
| `instrumentUsageDaysBetweenMeasurements` | int | 复测时必填 | 两次测量之间使用该仪器的天数 |
| `previousDisplayedScore` | int | 复测时必填 | 上次展示给客户的综合评分 |

**字段说明：** `instrumentUsageDaysBetweenMeasurements` 是本次新增的正式业务字段，用于：
- 判断客户是否属于持续使用场景
- 决定复测评分保护规则是否生效

**前端校验要求：**
- 首次检测：不显示或不必填
- 复测：必须填写
- 取值范围：0–365
- 不能为空、不能为负数

## 5. 后端接口输入结构

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
      "liver": { "left": 38.2, "right": 37.6 },
      "spleen": { "left": 38.4, "right": 37.8 },
      "kidney": { "left": 37.9, "right": 37.1 },
      "stomach": { "left": 38.5, "right": 38.0 },
      "gallbladder": { "left": 37.4, "right": 38.2 },
      "bladder": { "left": 37.2, "right": 36.9 }
    },
    "after": {
      "liver": { "left": 38.0, "right": 37.9 },
      "spleen": { "left": 38.3, "right": 38.0 },
      "kidney": { "left": 37.4, "right": 37.8 },
      "stomach": { "left": 38.4, "right": 38.2 },
      "gallbladder": { "left": 37.8, "right": 38.0 },
      "bladder": { "left": 37.5, "right": 37.6 }
    }
  },
  "engineInference": {
    "overallLevel": "moderate_imbalance",
    "dominantPatternBefore": "right_low",
    "dominantPatternAfter": "left_low",
    "lowestMeridianBefore": { "meridian": "gallbladder", "side": "left", "value": 37.4 },
    "lowestMeridianAfter": { "meridian": "kidney", "side": "left", "value": 37.4 },
    "meridianStates": [],
    "combinationHits": [],
    "riskTags": []
  },
  "scoreContext": {
    "previousDisplayedScore": 72,
    "currentRawScore": 76,
    "displayedScore": 76,
    "scoreLevel": "轻度失衡",
    "instrumentUsageDaysBetweenMeasurements": 25,
    "minUsageDaysForProtection": 7,
    "adherenceFlag": true,
    "scoreAdjustedByPolicy": false
  }
}
```

## 6. 模型返回的数据结构

```json
{
  "healthScore": {
    "score": 78,
    "level": "轻度失衡",
    "summary": "整体状态尚可，局部存在失衡，建议持续调理和观察。"
  },
  "overallAssessment": {
    "overallLevel": "整体存在一定失衡",
    "dominantPattern": "前后两组左右偏向变化较明显",
    "focusMeridians": ["肾经", "膀胱经", "肝经", "胆经", "脾经"],
    "stableMeridians": ["胃经"],
    "summaryText": "本次检测显示，身体整体平衡状态仍需加强，重点关注肾膀胱、肝胆及脾相关变化。"
  },
  "keyFindings": [
    {
      "title": "生殖系统相关风险需重点关注",
      "level": "高",
      "description": "肾经与膀胱经同时出现交叉变化，提示这一方向需要尽早关注和调理。",
      "evidence": ["肾经交叉", "膀胱经交叉"]
    }
  ],
  "meridianDetails": [
    {
      "meridian": "肝经",
      "status": "交叉",
      "mainLabel": "先藏血不足，后代谢偏弱",
      "riskPoints": ["贫血倾向", "结节风险"],
      "description": "肝经前后变化较明显，提示气血与代谢两方面都需要关注。"
    }
  ],
  "combinationAnalysis": [
    {
      "comboName": "肾膀胱交叉联动",
      "description": "肾经与膀胱经共同异常时，常提示生殖系统和腰部方向需重点预防。"
    }
  ],
  "advice": {
    "priorityDirections": [
      "优先关注肾经与膀胱经相关调理",
      "同时重视肝胆代谢与祛湿"
    ],
    "lifestyleAdvice": [
      "注意休息，避免长期劳累和透支",
      "注意腰腹及四肢保暖",
      "少食寒凉、生冷、过甜食物"
    ],
    "wellnessAdvice": [
      "保持规律作息，尽量减少熬夜",
      "适量活动，避免久坐久站",
      "日常多关注身体循环、睡眠和排湿状态"
    ],
    "retestAdvice": "后续复测时，重点观察肾经、膀胱经、肝经和胆经的变化。"
  },
  "encouragementBanner": {
    "text": "每天坚持踩生物能量仪+喝健康安全好水：即可越来越健康美丽哦"
  },
  "disclaimer": {
    "text": "本报告基于经络温度数据生成，用于日常健康管理参考，不等同于医疗诊断结论。如有长期不适，建议结合专业检查进一步评估。"
  }
}
```

## 7. 前端模块与返回字段映射

| 前端模块 | 数据字段 |
|---|---|
| 亚健康综合评分 | `healthScore` |
| 整体概况 | `overallAssessment` |
| 核心关注结论 | `keyFindings` |
| 六经络明细 | `meridianDetails` |
| 综合分析 | `combinationAnalysis` |
| 生活方式与养生建议 | `advice` |
| 信心提醒 | `encouragementBanner` |
| 报告说明 | `disclaimer` |

## 8. 规则库更新需求

### 8.1 新增评分规则层

**建议新增规则文件：** `rules/score_rules.json`

**作用：**
- 计算原始综合评分
- 管理加分扣分逻辑
- 管理评分等级映射

### 8.2 新增养生建议规则层

**建议新增规则文件：** `rules/wellness_advice_rules.json`

**作用：** 将经络异常与具体养生建议做映射。

**示例映射：**
| 经络异常 | 养生建议 |
|---|---|
| 胃寒 | 少食寒凉、生冷，饮食规律 |
| 脾湿 | 少甜少油，适量活动，注意排湿 |
| 肾阳虚 | 注意保暖，避免过劳 |
| 肝血虚 | 规律作息，减少熬夜，关注气血恢复 |
| 胆经异常 | 饮食清淡，少高脂食物，注意休息 |

### 8.3 新增复测策略规则层

**建议新增规则文件：** `rules/followup_policy_rules.json`

```json
{
  "minUsageDaysForProtection": 7,
  "preventScoreDecreaseWhenAdherent": true,
  "allowStableOrImprovedFollowupMessaging": true
}
```

**作用：**
- 管理复测评分保护规则
- 管理复测文案策略
- 管理最小有效使用天数阈值

## 9. 新案例带来的规则补充

### 9.1 交叉分层

不能只记录"是否交叉"，建议增加：
- 单经交叉
- 双经交叉
- 多经络交叉失衡

**原因：** 新增案例中，肾经和膀胱经双交叉会被优先解释成重点风险。

### 9.2 第一组与第二组偏侧都要记录

**新增字段：**
- `dominantPatternBefore`
- `dominantPatternAfter`

**原因：** 新增案例中，第一组偏右、第二组偏左本身就是重要结论。

### 9.3 生殖系统组合规则强化

**新增规则：** `kidney_cross + bladder_cross → reproductive_system_attention`

**原因：** 新增案例中，肾膀胱双交叉优先被解释为生殖系统相关风险。

### 9.4 肝胆脾联动强化

**新增规则：** `gallbladder_left_low + liver_cross + spleen_right_low → mass_risk_attention`

**原因：** 新增案例中，胆、肝、脾共同异常被收束为结节、囊肿、息肉风险方向。

## 10. 亚健康综合评分逻辑

### 10.1 评分目标

综合评分用于健康管理感知，不是医疗评分。其目标是：
- 反映当前整体状态
- 让用户易理解
- 与复测场景衔接
- 不与业务目标冲突

### 10.2 分值范围

- 0–100 分

### 10.3 评分构成

| 维度 | 权重 | 考虑因素 |
|---|---|---|
| 整体平衡度 | 30分 | 左右温差、偏左/偏右经络数量、整体偏侧情况 |
| 交叉失衡程度 | 20分 | 是否交叉、交叉数量、是否存在关键双交叉（如肾+膀胱） |
| 重点经络状态 | 20分 | 重点关注肝、脾、肾、膀胱；胃、胆次一级 |
| 组合风险程度 | 20分 | 命中心脏供血、头部供血、颈椎、腰椎、生殖系统、肠道/肺、结节/囊肿风险 |
| 调理响应度 | 10分 | 第二组是否更趋于平衡、多条经络是否改善 |

### 10.4 初版评分算法

采用"基础分100 - 扣分 + 小幅加分"的逻辑。

**扣分项：**
| 扣分场景 | 分值 |
|---|---|
| 单条经络轻度异常 | -2 |
| 单条经络明显异常 | -4 |
| 单经交叉 | -4 |
| 肾膀胱双交叉 | -8 |
| 4条以上偏左/偏右 | -6 |
| 命中心脏供血/头部供血 | -6 |
| 命中颈椎/腰椎/生殖系统等组合风险 | -4 ~ -6 |
| 多经络失衡 | -8 |

**加分项：**
| 加分场景 | 分值 |
|---|---|
| 第二组明显趋于平衡 | +2 ~ +5 |
| 多条经络改善 | +2 ~ +5 |

**分值边界：**
- 上限：100
- 建议下限：30

### 10.5 评分分级映射

| 分数 | 等级 | 展示语 |
|---|---|---|
| 90–100 | 整体状态较好 | 当前整体状态较平稳，请继续保持 |
| 75–89 | 轻度失衡 | 整体状态尚可，局部仍需关注 |
| 60–74 | 中度失衡 | 存在较明确失衡，建议持续调理 |
| 0–59 | 需重点关注 | 当前失衡较明显，建议尽早重视 |

## 11. 复测评分保护规则

### 11.1 规则名称

复测评分保护规则

### 11.2 规则目的

若客户在两次测量之间持续使用仪器，则复测展示给客户的综合评分不应低于上次展示分。

### 11.3 触发条件

同时满足以下条件时生效：
1. `isFollowup == true`
2. 存在 `previousDisplayedScore`
3. `instrumentUsageDaysBetweenMeasurements >= minUsageDaysForProtection`
4. `currentRawScore < previousDisplayedScore`

### 11.4 处理逻辑

```
if isFollowup == true
and previousDisplayedScore exists
and instrumentUsageDaysBetweenMeasurements >= minUsageDaysForProtection
and currentRawScore < previousDisplayedScore
then displayedScore = previousDisplayedScore
else displayedScore = currentRawScore
```

### 11.5 最小有效使用天数

建议初版设定：`minUsageDaysForProtection = 7`

- 小于7天，不触发保护规则
- 大于等于7天，可视为持续使用

### 11.6 评分字段说明

| 字段 | 说明 |
|---|---|
| `currentRawScore` | 规则真实算出的分 |
| `displayedScore` | 最终展示给客户的分 |
| `scoreAdjustedByPolicy` | 是否触发保护规则 |
| `adherenceFlag` | 是否达到持续使用条件 |

## 12. 异常与边界处理

| 场景 | 处理方式 |
|---|---|
| 首次检测 | 不需要输入 `instrumentUsageDaysBetweenMeasurements`，不应用复测评分保护规则 |
| 复测但未使用仪器 | `instrumentUsageDaysBetweenMeasurements = 0`，不触发保护规则，分数按原始计算结果展示 |
| 复测但缺少上次分数 | 不触发保护规则，分数按原始计算结果展示 |
| 复测使用天数 < 0 | 前端拦截 |
| 复测使用天数 > 365 | 前端提示重新确认 |

## 13. 开发实施顺序建议

### 第一阶段：前端模块搭建

先完成页面模块：评分 → 整体概况 → 核心关注结论 → 六经络明细 → 综合分析 → 建议 → 信心提醒 → 说明

### 第二阶段：后端规则扩展

补齐：评分规则、养生建议规则、复测保护规则、新案例补充规则

### 第三阶段：模型文案优化

确保输出风格统一为：专业、通俗、易懂、不生硬、不广告化

## 14. 版本结论

本版本新增需求已形成完整的开发说明，重点包括：

- 报告展示结构升级为 8 个模块
- 复测场景新增必填字段：两次测量之间使用仪器的天数
- 评分逻辑独立成层
- 复测评分保护规则明确
- 新案例带来的交叉、偏侧、生殖系统、肝胆脾联动规则已纳入更新范围

**下一步可按本 PRD 进入：** 前端模块设计、后端规则实现、模型输出结构调整
