# 六条经络规则库 PRD（v1.0）

## 1. 文档目的

本文档用于配合《六条经络报告系统 PRD v1.2》落地开发。

- **PRD v1.2** 解决的是"报告怎么展示、接口怎么设计、评分怎么处理"
- **本规则库 PRD** 解决的是"系统按什么规则进行判断"

本规则库覆盖以下内容：

- 经络主规则
- 组合规则
- 综合评分规则
- 养生建议映射规则
- 复测保护规则
- 边界与禁用规则

---

## 2. 使用原则

### 2.1 定位

- 健康管理参考规则
- 标准报告生成规则
- 非医疗诊断规则

### 2.2 当前版本支持

- 标准报告输出
- 固定规则判断
- 固定建议映射
- 复测评分保护

### 2.3 当前版本不支持

- 风水
- 男女、生育
- 现场问询式验证
- 成交话术
- 专家自由发挥层

---

## 3. 经络主规则表

### 3.1 字段说明

| 字段 | 说明 |
|---|---|
| `meridian_id` | 经络唯一标识 |
| `meridian_name` | 经络名称 |
| `priority_level` | 优先级：A/B/C |
| `enabled_in_standard_report` | 是否进入标准报告 |
| `left_low_label` | 左低时的主标签 |
| `left_low_points` | 左低时主要提示点 |
| `right_low_label` | 右低时的主标签 |
| `right_low_points` | 右低时主要提示点 |
| `cross_label` | 交叉时主标签 |
| `cross_points` | 交叉时主要提示点 |
| `notes` | 备注说明 |

### 3.2 经络主规则清单

#### 肝经

| 字段 | 内容 |
|---|---|
| `meridian_id` | liver |
| `meridian_name` | 肝经 |
| `priority_level` | A |
| `enabled_in_standard_report` | true |
| `left_low_label` | 代谢偏弱 / 气虚倾向 |
| `left_low_points` | 三高风险需关注、血稠倾向、乳房结节或小叶增生风险、温差较大时睡眠质量下降 |
| `right_low_label` | 血虚 / 藏血不足 |
| `right_low_points` | 贫血倾向、头晕乏力、掉发、心脏供血不足、心慌、低血压、睡眠浅 |
| `cross_label` | 气血两虚 |
| `cross_points` | 脂肪肝风险需关注、肝囊肿风险需关注 |
| `notes` | 梦境相关内容不进入标准报告 |

#### 脾经

| 字段 | 内容 |
|---|---|
| `meridian_id` | spleen |
| `meridian_name` | 脾经 |
| `priority_level` | A |
| `enabled_in_standard_report` | true |
| `left_low_label` | 脾气偏虚 |
| `left_low_points` | 乏力、思虑偏重、血糖代谢需关注、四肢风险、膝盖风险 |
| `right_low_label` | 湿气偏重 |
| `right_low_points` | 大便异常、粘马桶、子宫相关风险、经期延长或量多、四肢疼痛、膝盖问题 |
| `cross_label` | 血糖 / 代谢紊乱提示 |
| `cross_points` | 血糖相关风险需重点关注 |
| `notes` | 思虑相关表述用中性语言，不做性格判断 |

#### 肾经

| 字段 | 内容 |
|---|---|
| `meridian_id` | kidney |
| `meridian_name` | 肾经 |
| `priority_level` | A |
| `enabled_in_standard_report` | true |
| `left_low_label` | 肾阴偏虚 |
| `left_low_points` | 尿酸偏高风险、耳鸣耳背、偏热、恢复偏慢 |
| `right_low_label` | 肾阳偏虚 |
| `right_low_points` | 怕冷、四肢发凉、夜尿偏多、体力恢复慢 |
| `cross_label` | 阴阳两虚 |
| `cross_points` | 结石风险需关注、囊肿风险需关注、生殖系统相关风险需关注 |
| `notes` | 男女、生育相关内容全部剔除 |

#### 胃经

| 字段 | 内容 |
|---|---|
| `meridian_id` | stomach |
| `meridian_name` | 胃经 |
| `priority_level` | C |
| `enabled_in_standard_report` | true |
| `left_low_label` | 胃部津液偏少 |
| `left_low_points` | 胃炎倾向、反酸、胃部刺激、饮食不规律风险 |
| `right_low_label` | 胃阳不足 / 胃寒 |
| `right_low_points` | 胃寒、消化偏弱、胃胀、饮食后不适 |
| `cross_label` | 胃经功能失衡 |
| `cross_points` | 胃功能状态需持续关注 |
| `notes` | 作为次要项保留，除非异常明显，否则不前置 |

#### 胆经

| 字段 | 内容 |
|---|---|
| `meridian_id` | gallbladder |
| `meridian_name` | 胆经 |
| `priority_level` | B |
| `enabled_in_standard_report` | true |
| `left_low_label` | 胆经偏弱 |
| `left_low_points` | 口干口苦、偏头痛、胆红素相关风险 |
| `right_low_label` | 胆脂代谢需关注 |
| `right_low_points` | 胆固醇风险、甘油三酯风险、脂肪瘤风险、精神状态或决策效率可能受身体状态影响 |
| `cross_label` | 胆经交叉失衡 |
| `cross_points` | 结石风险需关注、囊肿风险需关注、息肉风险需关注、表面粗糙等风险需关注 |
| `notes` | 决断力弱、叹气等改写为中性偏身体状态表达 |

#### 膀胱经

| 字段 | 内容 |
|---|---|
| `meridian_id` | bladder |
| `meridian_name` | 膀胱经 |
| `priority_level` | A |
| `enabled_in_standard_report` | true |
| `left_low_label` | 肩颈腰与肠道方向需关注 |
| `left_low_points` | 肩颈腰问题、便秘、痔疮、大肠息肉风险、肺左侧功能风险 |
| `right_low_label` | 湿下注与腰部方向需关注 |
| `right_low_points` | 大便不成形、湿气下注大肠、肺右侧功能风险 |
| `cross_label` | 膀胱经交叉失衡 |
| `cross_points` | 肠道问题需关注、生殖系统问题需关注、腰部及循环问题需关注 |
| `notes` | 肺部只写功能或风险关注，不做明确诊断 |

---

## 4. 组合规则表

### 4.1 字段说明

| 字段 | 说明 |
|---|---|
| `rule_id` | 规则ID |
| `rule_name` | 规则名称 |
| `trigger` | 触发条件 |
| `output.title` | 输出标题 |
| `output.desc` | 输出说明 |
| `priority` | 优先级 |
| `enabled` | 是否启用 |

### 4.2 组合规则清单

#### combo_heart_supply — 心脏供血关注

| 字段 | 内容 |
|---|---|
| `rule_id` | combo_heart_supply |
| `rule_name` | 心脏供血关注 |
| `enabled` | true |
| `priority` | A |
| `trigger.type` | count_by_side |
| `trigger.phase` | before_or_overall |
| `trigger.side` | right |
| `trigger.min_count` | 4 |
| `output.title` | 心脏供血需关注 |
| `output.desc` | 整体偏右较明显时，提示循环及心脏供血方向需重点关注。 |

#### combo_head_supply — 头部供血关注

| 字段 | 内容 |
|---|---|
| `rule_id` | combo_head_supply |
| `rule_name` | 头部供血关注 |
| `enabled` | true |
| `priority` | A |
| `trigger.type` | count_by_side |
| `trigger.phase` | before_or_overall |
| `trigger.side` | left |
| `trigger.min_count` | 4 |
| `output.title` | 头部供血需关注 |
| `output.desc` | 整体偏左较明显时，提示头部供血方向需重点关注。 |

#### combo_waist — 腰椎风险提示

| 字段 | 内容 |
|---|---|
| `rule_id` | combo_waist |
| `rule_name` | 腰椎风险提示 |
| `enabled` | true |
| `priority` | A |
| `trigger.type` | same_side_abnormal |
| `trigger.meridians` | kidney, bladder |
| `output.title` | 腰椎相关问题需关注 |
| `output.desc` | 肾主骨，膀胱管肩颈腰，同向异常时优先看腰椎方向。 |

#### combo_neck — 颈椎风险提示

| 字段 | 内容 |
|---|---|
| `rule_id` | combo_neck |
| `rule_name` | 颈椎风险提示 |
| `enabled` | true |
| `priority` | A |
| `trigger.type` | joint_abnormal |
| `trigger.meridians` | kidney, bladder, spleen |
| `output.title` | 颈椎相关问题需关注 |
| `output.desc` | 采用膀胱定位、脾定侧、肾定骨的逻辑综合判断颈椎方向风险。 |

#### combo_reproductive — 生殖系统关注

| 字段 | 内容 |
|---|---|
| `rule_id` | combo_reproductive |
| `rule_name` | 生殖系统关注 |
| `enabled` | true |
| `priority` | A |
| `trigger.type` | cross_pair |
| `trigger.pairs` | kidney, bladder |
| `output.title` | 生殖系统相关风险需重点关注 |
| `output.desc` | 肾经与膀胱经同时交叉时，优先提示生殖系统方向需提前预防。 |

#### combo_intestine_lung — 肠道与肺方向关注

| 字段 | 内容 |
|---|---|
| `rule_id` | combo_intestine_lung |
| `rule_name` | 肠道与肺方向关注 |
| `enabled` | true |
| `priority` | B |
| `trigger.type` | compound |
| `trigger.conditions[0].meridian` | bladder |
| `trigger.conditions[0].status_in` | left_low, right_low, cross |
| `trigger.conditions[1].tags_any` | spleen_damp, bowel_abnormal |
| `output.title` | 肠道及肺部情况需关注 |
| `output.desc` | 优先提示肠道，再提示肺部功能或相关风险。 |

#### combo_liver_gall — 肝胆代谢关注

| 字段 | 内容 |
|---|---|
| `rule_id` | combo_liver_gall |
| `rule_name` | 肝胆代谢关注 |
| `enabled` | true |
| `priority` | B |
| `trigger.type` | joint_abnormal |
| `trigger.meridians` | liver, gallbladder |
| `output.title` | 肝胆代谢压力需关注 |
| `output.desc` | 肝胆联动异常时，提示代谢、解毒及相关风险需关注。 |

#### combo_liver_gall_spleen_mass — 结节/囊肿/息肉风险关注

| 字段 | 内容 |
|---|---|
| `rule_id` | combo_liver_gall_spleen_mass |
| `rule_name` | 结节/囊肿/息肉风险关注 |
| `enabled` | true |
| `priority` | A |
| `trigger.type` | specific_combo |
| `trigger.conditions[0]` | gallbladder status=left_low |
| `trigger.conditions[1]` | liver status_in=cross, left_low, right_low |
| `trigger.conditions[2]` | spleen status=right_low |
| `output.title` | 结节、囊肿、息肉方向需关注 |
| `output.desc` | 肝胆代谢与湿气问题叠加时，此方向风险更高。 |

#### combo_multi_cross — 多经络交叉失衡

| 字段 | 内容 |
|---|---|
| `rule_id` | combo_multi_cross |
| `rule_name` | 多经络交叉失衡 |
| `enabled` | true |
| `priority` | A |
| `trigger.type` | cross_count |
| `trigger.min_count` | 3 |
| `output.title` | 多经络交叉失衡需重点关注 |
| `output.desc` | 当前不是单一经络问题，而是整体经络调节状态较不稳定。 |

---

## 5. 综合评分规则表

### 5.1 评分原则

- 综合评分范围：**0–100**，分数越高表示整体状态越好
- 评分由两层组成：
  - **rawScore**：根据规则真实计算
  - **displayedScore**：应用复测保护规则后的对外分数

### 5.2 扣分规则

| 规则 | 扣分 |
|---|---|
| 单条经络轻度异常 | -2 |
| 单条经络明显异常 | -4 |
| 单经交叉 | -4 |
| 肾膀胱双交叉 | -8 |
| 交叉经络数量 >= 3 | -8 |
| 4条及以上偏右 | -6 |
| 4条及以上偏左 | -6 |
| 命中心脏供血规则 | -6 |
| 命中头部供血规则 | -6 |
| 命中腰椎/颈椎/生殖系统规则 | -4 ~ -6 |
| 命中肝胆脾结节风险规则 | -6 |
| 多经络失衡（>=4条异常） | -8 |

### 5.3 加分规则

| 规则 | 加分 |
|---|---|
| 第二组较第一组明显趋于平衡 | +2 ~ +5 |
| 多条经络改善 | +2 ~ +5 |
| 无明显交叉且整体平衡较好 | +3 |

### 5.4 分级映射

| 分数 | 等级 | 展示语 |
|---|---|---|
| 90–100 | 整体状态较好 | 当前整体状态较平稳，请继续保持 |
| 75–89 | 轻度失衡 | 整体状态尚可，局部仍需关注 |
| 60–74 | 中度失衡 | 存在较明确失衡，建议持续调理 |
| 0–59 | 需重点关注 | 当前失衡较明显，建议尽早重视 |

### 5.5 分值边界

- 上限：100
- 下限：30

---

## 6. 复测保护规则表

### 6.1 核心字段

| 字段 | 含义 |
|---|---|
| `isFollowup` | 是否复测 |
| `previousDisplayedScore` | 上次展示给客户的分数 |
| `instrumentUsageDaysBetweenMeasurements` | 两次检测之间使用仪器的天数 |
| `minUsageDaysForProtection` | 触发保护的最小天数阈值 |
| `adherenceFlag` | 是否达到持续使用条件 |
| `scoreAdjustedByPolicy` | 是否触发保护规则 |

### 6.2 规则定义

**最小有效使用天数：** `minUsageDaysForProtection = 7`

**触发条件（同时满足）：**
1. `isFollowup == true`
2. 存在 `previousDisplayedScore`
3. `instrumentUsageDaysBetweenMeasurements >= 7`
4. `currentRawScore < previousDisplayedScore`

**处理逻辑：**

```
if isFollowup == true
and previousDisplayedScore exists
and instrumentUsageDaysBetweenMeasurements >= 7
and currentRawScore < previousDisplayedScore
then displayedScore = previousDisplayedScore
else displayedScore = currentRawScore
```

**补充要求：**
- 后台必须保留 `rawScore`
- 前端对客户展示 `displayedScore`
- 若触发保护规则，需保留 `scoreAdjustedByPolicy = true`

---

## 7. 养生建议映射规则表

### 7.1 字段说明

| 字段 | 说明 |
|---|---|
| `tag` | 异常标签 |
| `priorityDirections` | 优先调理方向 |
| `lifestyleAdvice` | 生活方式建议 |
| `wellnessAdvice` | 具体养生建议 |

### 7.2 规则清单

#### stomach_cold — 胃寒 / 胃阳不足

| 字段 | 内容 |
|---|---|
| `tag` | stomach_cold |
| `priorityDirections` | 温胃、调理胃部功能 |
| `lifestyleAdvice` | 饮食规律，少食寒凉、生冷食物 |
| `wellnessAdvice` | 三餐尽量规律，少空腹，避免长期节食，减少冰凉刺激 |

#### spleen_damp — 脾湿 / 湿气重

| 字段 | 内容 |
|---|---|
| `tag` | spleen_damp |
| `priorityDirections` | 健脾、祛湿 |
| `lifestyleAdvice` | 少甜、少油、少黏腻，注意活动 |
| `wellnessAdvice` | 适量活动，避免久坐，关注排湿和大便状态，注意膝盖和四肢的保养 |

#### kidney_yang_weak — 肾阳偏虚 / 怕冷

| 字段 | 内容 |
|---|---|
| `tag` | kidney_yang_weak |
| `priorityDirections` | 温养肾阳 |
| `lifestyleAdvice` | 注意腰腹和四肢保暖，避免过劳 |
| `wellnessAdvice` | 作息规律，减少熬夜，避免长期身体透支 |

#### liver_blood_weak — 肝血不足 / 气血偏弱

| 字段 | 内容 |
|---|---|
| `tag` | liver_blood_weak |
| `priorityDirections` | 养肝、补血、改善循环 |
| `lifestyleAdvice` | 注意休息，减少熬夜，关注睡眠质量 |
| `wellnessAdvice` | 保持规律作息，避免情绪过度紧张，重视身体恢复和气血调养 |

#### gallbladder_metabolism_pressure — 胆经异常 / 胆脂代谢问题

| 字段 | 内容 |
|---|---|
| `tag` | gallbladder_metabolism_pressure |
| `priorityDirections` | 关注肝胆代谢 |
| `lifestyleAdvice` | 饮食清淡，少高脂、高油食物 |
| `wellnessAdvice` | 规律作息，适量活动，减轻身体代谢负担 |

#### heart_supply_attention — 心脏供血关注

| 字段 | 内容 |
|---|---|
| `tag` | heart_supply_attention |
| `priorityDirections` | 优先关注循环与供血状态 |
| `lifestyleAdvice` | 避免劳累，注意休息与睡眠 |
| `wellnessAdvice` | 日常关注心悸、乏力等表现，保持节律稳定，避免情绪和体力过度消耗 |

#### head_supply_attention — 头部供血关注

| 字段 | 内容 |
|---|---|
| `tag` | head_supply_attention |
| `priorityDirections` | 优先关注头部循环状态 |
| `lifestyleAdvice` | 避免熬夜，减少脑力透支 |
| `wellnessAdvice` | 注意睡眠，关注精神状态和记忆力变化，避免长期紧张和疲劳 |

#### reproductive_system_attention — 生殖系统风险关注

| 字段 | 内容 |
|---|---|
| `tag` | reproductive_system_attention |
| `priorityDirections` | 优先关注生殖系统方向 |
| `lifestyleAdvice` | 注意休息，注意保暖，避免过度劳累 |
| `wellnessAdvice` | 关注腰腹、生殖系统及周期性不适情况，避免长期受凉，出现持续不适时及时检查 |

---

## 8. 边界与禁用规则表

### 8.1 全部剔除内容

| 类型 | 处理规则 |
|---|---|
| 风水、方位、绿植 | 全部剔除 |
| 男女、生育判断 | 全部剔除 |
| 体质偏父/偏母 | 不写入标准报告 |
| 梦境解释 | 不写入标准报告 |
| 现场问询式验证 | 不写入标准报告 |
| 成交话术 | 不写入标准报告 |
| 过度主观评价 | 不写入标准报告 |
| 明确疾病诊断 | 不写入标准报告 |

### 8.2 需模糊化表达内容

| 内容 | 标准写法 |
|---|---|
| 肺部结节 | "肺部情况需关注" / "可能存在相关风险" |
| 决断力弱、叹气 | "精神状态或决策效率可能受身体状态影响" |
| 结节/囊肿/息肉 | "相关方向风险需关注" |

---

## 9. 开发实施建议

### 9.1 后端执行顺序

1. 读取测量数据
2. 计算单经状态
3. 计算组合规则命中
4. 计算 rawScore
5. 判断是否触发复测保护规则，得到 displayedScore
6. 收集建议标签
7. 组装模型输入
8. 生成标准报告结构输出

### 9.2 前端展示原则

**只展示：**
- `displayedScore`
- 标准报告八模块内容

**不要直接展示：**
- `rawScore`
- 内部 trace
- 调整策略标志位

---

## 10. JSON 规则文件草案

### 10.1 meridian_rules.json

```json
{
  "version": "1.0",
  "rules": [
    {
      "meridian_id": "liver",
      "meridian_name": "肝经",
      "priority_level": "A",
      "enabled_in_standard_report": true,
      "left_low": {
        "label": "代谢偏弱 / 气虚倾向",
        "points": [
          "三高风险需关注",
          "血稠倾向",
          "乳房结节或小叶增生风险",
          "温差较大时睡眠质量下降"
        ]
      },
      "right_low": {
        "label": "血虚 / 藏血不足",
        "points": [
          "贫血倾向",
          "头晕乏力",
          "掉发",
          "心脏供血不足",
          "心慌",
          "低血压",
          "睡眠浅"
        ]
      },
      "cross": {
        "label": "气血两虚",
        "points": [
          "脂肪肝风险需关注",
          "肝囊肿风险需关注"
        ]
      },
      "notes": [
        "梦境相关内容不进入标准报告"
      ]
    },
    {
      "meridian_id": "spleen",
      "meridian_name": "脾经",
      "priority_level": "A",
      "enabled_in_standard_report": true,
      "left_low": {
        "label": "脾气偏虚",
        "points": [
          "乏力",
          "思虑偏重",
          "血糖代谢需关注",
          "四肢风险",
          "膝盖风险"
        ]
      },
      "right_low": {
        "label": "湿气偏重",
        "points": [
          "大便异常",
          "粘马桶",
          "子宫相关风险",
          "经期延长或量多",
          "四肢疼痛",
          "膝盖问题"
        ]
      },
      "cross": {
        "label": "血糖 / 代谢紊乱提示",
        "points": [
          "血糖相关风险需重点关注"
        ]
      },
      "notes": [
        "思虑相关表述用中性语言，不做性格判断"
      ]
    },
    {
      "meridian_id": "kidney",
      "meridian_name": "肾经",
      "priority_level": "A",
      "enabled_in_standard_report": true,
      "left_low": {
        "label": "肾阴偏虚",
        "points": [
          "尿酸偏高风险",
          "耳鸣耳背",
          "偏热",
          "恢复偏慢"
        ]
      },
      "right_low": {
        "label": "肾阳偏虚",
        "points": [
          "怕冷",
          "四肢发凉",
          "夜尿偏多",
          "体力恢复慢"
        ]
      },
      "cross": {
        "label": "阴阳两虚",
        "points": [
          "结石风险需关注",
          "囊肿风险需关注",
          "生殖系统相关风险需关注"
        ]
      },
      "notes": [
        "男女、生育相关内容全部剔除"
      ]
    },
    {
      "meridian_id": "stomach",
      "meridian_name": "胃经",
      "priority_level": "C",
      "enabled_in_standard_report": true,
      "left_low": {
        "label": "胃部津液偏少",
        "points": [
          "胃炎倾向",
          "反酸",
          "胃部刺激",
          "饮食不规律风险"
        ]
      },
      "right_low": {
        "label": "胃阳不足 / 胃寒",
        "points": [
          "胃寒",
          "消化偏弱",
          "胃胀",
          "饮食后不适"
        ]
      },
      "cross": {
        "label": "胃经功能失衡",
        "points": [
          "胃功能状态需持续关注"
        ]
      },
      "notes": [
        "作为次要项保留，除非异常明显，否则不前置"
      ]
    },
    {
      "meridian_id": "gallbladder",
      "meridian_name": "胆经",
      "priority_level": "B",
      "enabled_in_standard_report": true,
      "left_low": {
        "label": "胆经偏弱",
        "points": [
          "口干口苦",
          "偏头痛",
          "胆红素相关风险"
        ]
      },
      "right_low": {
        "label": "胆脂代谢需关注",
        "points": [
          "胆固醇风险",
          "甘油三酯风险",
          "脂肪瘤风险",
          "精神状态或决策效率可能受身体状态影响"
        ]
      },
      "cross": {
        "label": "胆经交叉失衡",
        "points": [
          "结石风险需关注",
          "囊肿风险需关注",
          "息肉风险需关注",
          "表面粗糙等风险需关注"
        ]
      }
    },
    {
      "meridian_id": "bladder",
      "meridian_name": "膀胱经",
      "priority_level": "A",
      "enabled_in_standard_report": true,
      "left_low": {
        "label": "肩颈腰与肠道方向需关注",
        "points": [
          "肩颈腰问题",
          "便秘",
          "痔疮",
          "大肠息肉风险",
          "肺左侧功能风险"
        ]
      },
      "right_low": {
        "label": "湿下注与腰部方向需关注",
        "points": [
          "大便不成形",
          "湿气下注大肠",
          "肺右侧功能风险"
        ]
      },
      "cross": {
        "label": "膀胱经交叉失衡",
        "points": [
          "肠道问题需关注",
          "生殖系统问题需关注",
          "腰部及循环问题需关注"
        ]
      },
      "notes": [
        "肺部只写功能或风险关注，不做确定诊断"
      ]
    }
  ]
}
```

### 10.2 combination_rules.json

```json
{
  "version": "1.0",
  "rules": [
    {
      "rule_id": "combo_heart_supply",
      "rule_name": "心脏供血关注",
      "enabled": true,
      "priority": "A",
      "trigger": {
        "type": "count_by_side",
        "phase": "before_or_overall",
        "side": "right",
        "min_count": 4
      },
      "output": {
        "title": "心脏供血需关注",
        "description": "整体偏右较明显时，提示循环及心脏供血方向需重点关注。"
      }
    },
    {
      "rule_id": "combo_head_supply",
      "rule_name": "头部供血关注",
      "enabled": true,
      "priority": "A",
      "trigger": {
        "type": "count_by_side",
        "phase": "before_or_overall",
        "side": "left",
        "min_count": 4
      },
      "output": {
        "title": "头部供血需关注",
        "description": "整体偏左较明显时，提示头部供血方向需重点关注。"
      }
    },
    {
      "rule_id": "combo_waist",
      "rule_name": "腰椎风险提示",
      "enabled": true,
      "priority": "A",
      "trigger": {
        "type": "same_side_abnormal",
        "meridians": ["kidney", "bladder"]
      },
      "output": {
        "title": "腰椎相关问题需关注",
        "description": "肾主骨，膀胱管肩颈腰，同向异常时优先看腰椎方向。"
      }
    },
    {
      "rule_id": "combo_neck",
      "rule_name": "颈椎风险提示",
      "enabled": true,
      "priority": "A",
      "trigger": {
        "type": "joint_abnormal",
        "meridians": ["kidney", "bladder", "spleen"]
      },
      "output": {
        "title": "颈椎相关问题需关注",
        "description": "采用膀胱定位、脾定侧、肾定骨的逻辑综合判断颈椎方向风险。"
      }
    },
    {
      "rule_id": "combo_reproductive",
      "rule_name": "生殖系统关注",
      "enabled": true,
      "priority": "A",
      "trigger": {
        "type": "cross_pair",
        "pairs": ["kidney", "bladder"]
      },
      "output": {
        "title": "生殖系统相关风险需重点关注",
        "description": "肾经与膀胱经同时交叉时，优先提示生殖系统方向需提前预防。"
      }
    },
    {
      "rule_id": "combo_intestine_lung",
      "rule_name": "肠道与肺方向关注",
      "enabled": true,
      "priority": "B",
      "trigger": {
        "type": "compound",
        "conditions": [
          { "meridian": "bladder", "status_in": ["left_low", "right_low", "cross"] },
          { "tags_any": ["spleen_damp", "bowel_abnormal"] }
        ]
      },
      "output": {
        "title": "肠道及肺部情况需关注",
        "description": "优先提示肠道，再提示肺部功能或相关风险。"
      }
    },
    {
      "rule_id": "combo_liver_gall",
      "rule_name": "肝胆代谢关注",
      "enabled": true,
      "priority": "B",
      "trigger": {
        "type": "joint_abnormal",
        "meridians": ["liver", "gallbladder"]
      },
      "output": {
        "title": "肝胆代谢压力需关注",
        "description": "肝胆联动异常时，提示代谢、解毒及相关风险需关注。"
      }
    },
    {
      "rule_id": "combo_liver_gall_spleen_mass",
      "rule_name": "结节/囊肿/息肉风险关注",
      "enabled": true,
      "priority": "A",
      "trigger": {
        "type": "specific_combo",
        "conditions": [
          { "meridian": "gallbladder", "status": "left_low" },
          { "meridian": "liver", "status_in": ["cross", "left_low", "right_low"] },
          { "meridian": "spleen", "status": "right_low" }
        ]
      },
      "output": {
        "title": "结节、囊肿、息肉方向需关注",
        "description": "肝胆代谢与湿气问题叠加时，此方向风险更高。"
      }
    },
    {
      "rule_id": "combo_multi_cross",
      "rule_name": "多经络交叉失衡",
      "enabled": true,
      "priority": "A",
      "trigger": {
        "type": "cross_count",
        "min_count": 3
      },
      "output": {
        "title": "多经络交叉失衡需重点关注",
        "description": "当前不是单一经络问题，而是整体经络调节状态较不稳定。"
      }
    }
  ]
}
```

### 10.3 score_rules.json

```json
{
  "version": "1.0",
  "base_score": 100,
  "min_score": 30,
  "max_score": 100,
  "deductions": [
    { "rule_id": "single_meridian_mild_abnormal", "condition": "single_meridian_mild_abnormal", "score": -2 },
    { "rule_id": "single_meridian_obvious_abnormal", "condition": "single_meridian_obvious_abnormal", "score": -4 },
    { "rule_id": "single_meridian_cross", "condition": "single_meridian_cross", "score": -4 },
    { "rule_id": "kidney_bladder_double_cross", "condition": "kidney_cross_and_bladder_cross", "score": -8 },
    { "rule_id": "multi_cross", "condition": "cross_count_gte_3", "score": -8 },
    { "rule_id": "right_bias", "condition": "right_low_count_gte_4", "score": -6 },
    { "rule_id": "left_bias", "condition": "left_low_count_gte_4", "score": -6 },
    { "rule_id": "heart_supply_hit", "condition": "hit_combo_heart_supply", "score": -6 },
    { "rule_id": "head_supply_hit", "condition": "hit_combo_head_supply", "score": -6 },
    { "rule_id": "neck_or_waist_or_reproductive_hit", "condition": "hit_combo_neck_or_waist_or_reproductive", "score": -5 },
    { "rule_id": "mass_risk_hit", "condition": "hit_combo_liver_gall_spleen_mass", "score": -6 },
    { "rule_id": "multi_imbalance", "condition": "abnormal_meridian_count_gte_4", "score": -8 }
  ],
  "bonuses": [
    { "rule_id": "after_more_balanced", "condition": "after_measurement_more_balanced", "score": 3 },
    { "rule_id": "multiple_meridians_improved", "condition": "multiple_meridians_improved", "score": 4 },
    { "rule_id": "overall_stable", "condition": "no_cross_and_good_balance", "score": 3 }
  ],
  "score_levels": [
    { "min": 90, "max": 100, "level": "整体状态较好", "summary": "当前整体状态较平稳，请继续保持。" },
    { "min": 75, "max": 89, "level": "轻度失衡", "summary": "整体状态尚可，局部仍需关注。" },
    { "min": 60, "max": 74, "level": "中度失衡", "summary": "存在较明确失衡，建议持续调理。" },
    { "min": 0, "max": 59, "level": "需重点关注", "summary": "当前失衡较明显，建议尽早重视。" }
  ]
}
```

### 10.4 wellness_advice_rules.json

```json
{
  "version": "1.0",
  "rules": [
    {
      "tag": "stomach_cold",
      "priorityDirections": ["温胃", "调理胃部功能"],
      "lifestyleAdvice": ["饮食规律", "少食寒凉、生冷食物"],
      "wellnessAdvice": ["三餐尽量规律，少空腹", "避免长期节食", "减少冰凉刺激"]
    },
    {
      "tag": "spleen_damp",
      "priorityDirections": ["健脾", "祛湿"],
      "lifestyleAdvice": ["少甜、少油、少黏腻", "注意活动"],
      "wellnessAdvice": ["适量活动，避免久坐", "关注排湿和大便状态", "注意膝盖和四肢的保养"]
    },
    {
      "tag": "kidney_yang_weak",
      "priorityDirections": ["温养肾阳"],
      "lifestyleAdvice": ["注意腰腹和四肢保暖", "避免过劳"],
      "wellnessAdvice": ["作息规律", "减少熬夜", "避免长期身体透支"]
    },
    {
      "tag": "liver_blood_weak",
      "priorityDirections": ["养肝", "补血", "改善循环"],
      "lifestyleAdvice": ["注意休息", "减少熬夜", "关注睡眠质量"],
      "wellnessAdvice": ["保持规律作息", "避免情绪过度紧张", "重视身体恢复和气血调养"]
    },
    {
      "tag": "gallbladder_metabolism_pressure",
      "priorityDirections": ["关注肝胆代谢"],
      "lifestyleAdvice": ["饮食清淡", "少高脂、高油食物"],
      "wellnessAdvice": ["规律作息", "适量活动", "减轻身体代谢负担"]
    },
    {
      "tag": "heart_supply_attention",
      "priorityDirections": ["优先关注循环与供血状态"],
      "lifestyleAdvice": ["避免劳累", "注意休息与睡眠"],
      "wellnessAdvice": ["日常关注心悸、乏力等表现", "保持节律稳定", "避免情绪和体力过度消耗"]
    },
    {
      "tag": "head_supply_attention",
      "priorityDirections": ["优先关注头部循环状态"],
      "lifestyleAdvice": ["避免熬夜", "减少脑力透支"],
      "wellnessAdvice": ["注意睡眠", "关注精神状态和记忆力变化", "避免长期紧张和疲劳"]
    },
    {
      "tag": "reproductive_system_attention",
      "priorityDirections": ["优先关注生殖系统方向"],
      "lifestyleAdvice": ["注意休息", "注意保暖", "避免过度劳累"],
      "wellnessAdvice": ["关注腰腹、生殖系统及周期性不适情况", "避免长期受凉", "出现持续不适时及时检查"]
    }
  ]
}
```

### 10.5 followup_policy_rules.json

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

### 10.6 JSON 文件与规则层对应关系

| JSON 文件 | 对应规则层 |
|---|---|
| `meridian_rules.json` | 单经判断 |
| `combination_rules.json` | 组合判断 |
| `score_rules.json` | 综合评分 |
| `wellness_advice_rules.json` | 建议生成 |
| `followup_policy_rules.json` | 复测保护策略 |

---

## 11. 版本结论

当前规则库 v1 已覆盖：

- 六经络主规则
- 核心组合规则
- 综合评分规则
- 复测保护规则
- 养生建议映射
- 边界与禁用内容

本规则库可作为后端规则实现、模型文案生成、前端展示结构的统一依据，与《六条经络报告系统 PRD v1.2》配套使用。
