# 木林森足部经络测温报告 PRD：经络分析规则与综合健康分算法

版本：v1.0  
用途：交付技术开发，用于实现经络测温报告的规则分析、综合健康分计算与报告结构化输出。

---

## 1. 产品目标

本报告基于用户足部经络测温数据，生成一份结构化健康报告。

系统不让 AI 直接自由判断，而是先通过固定规则完成数据分析，再由 AI 基于规则结果进行整理、合并、润色和生成调理建议。

报告包含四个核心模块：

1. 健康总览：综合健康分 + 总览文字  
2. 本次重点关注的问题：控制在 3-4 个主要问题  
3. 经络分析：逐一分析 6 条经络  
4. 调理建议：基于已触发问题生成具体建议

---

## 2. 输入数据

### 2.1 基础输入

每次检测共 24 个温度数据。

6 条经络：

```text
stomach        胃经
gallbladder    胆经
bladder        膀胱经
liver          肝经
spleen         脾经
kidney         肾经
```

每条经络包含 4 个值：

```text
group1_left     第一组左脚温度，使用仪器 5 分钟时测量
group1_right    第一组右脚温度，使用仪器 5 分钟时测量
group2_left     第二组左脚温度，使用仪器 20 分钟时测量
group2_right    第二组右脚温度，使用仪器 20 分钟时测量
```

示例：

```json
{
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach": {
      "group1_left": 39.5,
      "group1_right": 40.5,
      "group2_left": 42.4,
      "group2_right": 42.5
    },
    "gallbladder": {
      "group1_left": 36.7,
      "group1_right": 36.7,
      "group2_left": 42.1,
      "group2_right": 42.1
    },
    "bladder": {
      "group1_left": 36.2,
      "group1_right": 36.5,
      "group2_left": 37.9,
      "group2_right": 41.1
    },
    "liver": {
      "group1_left": 36.7,
      "group1_right": 36.4,
      "group2_left": 39.6,
      "group2_right": 39.9
    },
    "spleen": {
      "group1_left": 36.6,
      "group1_right": 36.5,
      "group2_left": 39.1,
      "group2_right": 40.6
    },
    "kidney": {
      "group1_left": 36.6,
      "group1_right": 36.7,
      "group2_left": 40.5,
      "group2_right": 41.6
    }
  }
}
```

### 2.2 复测额外输入

复测时需要额外传入：

```json
{
  "measurement_type": "retest",
  "test_number": 2,
  "previous_score": 77,
  "previous_problem_index": 24.4,
  "usage_days_between_tests": 14
}
```

字段说明：

```text
test_number：本次是第几次测试（第一次测试为1，第二次为2，以此类推）
previous_score：上一次展示给用户的综合健康分
previous_problem_index：上一次计算出的内部问题指数 I
usage_days_between_tests：两次检测之间用户实际使用仪器的天数
```

### 2.3 性别字段

```text
gender = male / female / unknown
```

性别用于最终报告过滤。

男性报告不能出现：宫寒、子宫、例假、人流、剖腹产、子宫肌瘤等女性专属表达。  
女性报告不能出现：前列腺、前列腺炎、前列腺钙化等男性专属表达。  
如果 gender = unknown，则不输出任何性别专属表达，只保留中性表达，如“生殖系统”“泌尿系统”“腹部手术史”等。

---

## 3. 基础计算规则

### 3.1 数据精度

所有温度值统一保留 1 位小数后再参与判断和计算。

### 3.2 左右状态判断

```text
left < right     → left_low，左低
right < left     → right_low，右低
left == right    → balanced，平衡
```

只有左右数值完全相等才算平衡。只要相差 0.1，也按低的一侧判断。

### 3.3 温差计算

```text
group1_diff = abs(group1_left - group1_right)
group2_diff = abs(group2_left - group2_right)
```

温差也统一保留 1 位小数。

---

## 4. 经络问题分析流程

### 4.1 第一步：第二组最低两点分析

只看第二组，也就是使用仪器 20 分钟后的 12 个数据。

从 12 个温度值中找出最低的两个点。最低两个点是报告必讲项。

如果没有并列，最低两个点必须进入“本次重点关注的问题”。  
如果出现并列，则先记录并列候选，再结合温差、左右偏向、经络趋势、组合问题等规则筛选，避免报告重点过多。

最低点归因方式：

```text
先判断属于哪条经络
再判断是左侧点还是右侧点
再匹配该经络的左低 / 右低 / 辅助规则
```

特殊规则：

如果最低点落在膀胱经，仍然必须讲，但膀胱经左低 / 右低不做独立具体疾病归因，只提示肩颈、腰、泌尿、生殖、消化、呼吸系统方向，并结合肾经和温差进一步分析。

---

### 4.2 第二步：第二组左右偏向统计

只看第二组数据，逐条比较 6 条经络的左右状态。

统计：

```text
left_low_count
right_low_count
balanced_count
```

判定：

```text
left_low_count >= 4   → 提示头部供血不足
right_low_count >= 4  → 提示心脏方向问题
```

如果两者都未达到 4 条，则不输出整体偏向问题。

该规则属于报告必讲规则，只要触发，就需要进入“本次重点关注的问题”。

---

### 4.3 第三步：六条经络逐一趋势分析

每条经络先分别判断第一组左右状态、第二组左右状态，再得到整体趋势。

趋势枚举：

```text
stable_left_low       两组均左低
stable_right_low      两组均右低
cross                 两组左右方向相反
stable_balanced       两组均平衡
potential_symptom     第一组平衡，第二组左低/右低
fast_response         第一组左低/右低，第二组平衡
```

判定规则：

```text
group1_status = left_low，group2_status = left_low
→ stable_left_low

group1_status = right_low，group2_status = right_low
→ stable_right_low

group1_status = left_low，group2_status = right_low
→ cross

group1_status = right_low，group2_status = left_low
→ cross

group1_status = balanced，group2_status = balanced
→ stable_balanced

group1_status = balanced，group2_status = left_low/right_low
→ potential_symptom

group1_status = left_low/right_low，group2_status = balanced
→ fast_response
```

趋势含义：

```text
stable_left_low / stable_right_low：
两次测量均表现为同一侧偏低，匹配该经络左低或右低规则。

cross：
两组左右方向相反，匹配该经络交叉规则。

stable_balanced：
两组均平衡，一般不作为重点问题，只在经络分析中简短说明。

potential_symptom：
第一组平衡，第二组出现偏低，表示潜在症状问题，需要提前预防，调理时间相对更长。
根据第二组低侧方向做弱归因。

fast_response：
第一组偏低，第二组恢复平衡，表示调理反应较快，问题相对在表，使用后改善明显。
一般不进入重点问题，除非同时触发最低点、严重温差、组合问题等高优先级规则。
```

---

### 4.4 第四步：左右温差分析

温差等级：

```text
diff <= 0.2
→ balanced，平衡

0.2 < diff <= 0.5
→ mild_sub_health，有一定亚健康

0.5 < diff <= 2
→ health_problem，有健康问题

diff > 2
→ serious_problem，有比较严重的问题
```

前后变化判断：

```text
group2_diff - group1_diff > 0.2
→ worsened，问题更突出 / 左右差异变大

group1_diff - group2_diff > 0.2
→ improved，问题有所好转 / 左右差异缩小

abs(group2_diff - group1_diff) <= 0.2
→ unchanged，基本不变
```

以下情况需要重点记录：

```text
group2_diff_level = health_problem
group2_diff_level = serious_problem
diff_change = worsened
该经络同时是第二组最低两点之一
该经络同时参与偏侧统计或颈腰椎组合判断
```

---

### 4.5 第五步：肾经 + 膀胱经判断颈椎 / 腰椎

使用第三步得到的：

```text
kidney.trend
bladder.trend
```

#### 4.5.1 明确稳定左低 / 右低时

相同低 → 腰椎问题：

```text
kidney = stable_left_low，bladder = stable_left_low
→ lumbar，腰椎问题

kidney = stable_right_low，bladder = stable_right_low
→ lumbar，腰椎问题
```

相反低 → 颈椎问题：

```text
kidney = stable_left_low，bladder = stable_right_low
→ cervical，颈椎问题

kidney = stable_right_low，bladder = stable_left_low
→ cervical，颈椎问题
```

#### 4.5.2 任意一条整体平衡

如果肾经或膀胱经任意一条为 `stable_balanced`：

```text
→ none，不输出颈椎 / 腰椎问题
```

#### 4.5.3 任意一条交叉

如果肾经或膀胱经任意一条为 `cross`：

```text
→ cervical_and_lumbar，颈椎和腰椎问题同时存在
```

#### 4.5.4 potential_symptom / fast_response

如果肾经或膀胱经为：

```text
potential_symptom
fast_response
```

暂不进入强颈椎 / 腰椎判断。

---

## 5. 膀胱经专项规则

膀胱经关联：

```text
肩颈
腰
生殖系统
泌尿系统
消化系统
呼吸系统
```

膀胱经左低或右低不单独对应具体问题，只作为辅助判断。

如果第二组最低点落在膀胱经，报告表达方向为：

```text
膀胱经温度偏低，提示肩颈、腰部、泌尿、生殖、消化、呼吸系统方向需要关注，需结合肾经和温差情况进一步分析。
```

膀胱经 + 肾经组合：

```text
膀胱经左低 + 肾左低 → 腰椎问题
膀胱经左低 + 肾右低 → 颈椎问题
膀胱经右低 + 肾右低 → 腰椎问题
膀胱经右低 + 肾左低 → 颈椎问题
```

膀胱经温差大 + 肾经异常：

触发条件建议：

```text
bladder.group2_diff > 0.5
且 bladder.group2_diff_level in ["health_problem", "serious_problem"]
且 kidney.trend != stable_balanced
```

触发后提示：

```text
肠道问题
生殖系统问题
肺部 / 呼吸道问题
```

最终表达仍需经过性别过滤。

---

## 6. 经络分析规则库

### 6.1 肝经 liver

肝经主气，其华在爪，关联代谢、解毒、眼睛、藏血。

左低：

```text
气虚
血液流速不够
血液循环推动不足
垃圾容易沉积在血管中
血稠、血脂、高血压方向
代谢差
口臭
放屁多
解毒功能变弱
皮肤易过敏
湿疹
容易长斑
```

右低：

```text
藏血功能变弱
血虚
心脏供血功能不足
心慌
胸闷
心悸
心律不齐
容易做梦
结合肾右低，容易掉发
温度特别低时，血虚严重，容易抽筋
```

交叉：

```text
是否熬夜
气血两虚
脂肪肝
酒精肝
肝囊肿
```

组合：

```text
肝左低 + 胆左低
→ 胆红素较高
→ 皮肤黄
→ 偶发性口干、口苦
```

---

### 6.2 脾经 spleen

脾经主四肢、肌肉、运化、过滤，关联血糖、思虑、唇。

左低：

```text
过滤能力弱
温差大时，容易出现血糖高方向问题
思虑重
容易操心
```

右低：

```text
湿气重
阳少湿气重
湿气下注到大肠，结合肝右低、肾右低，容易便溏
湿气下注到子宫，可能例假长
湿气下注到小腿，容易腿沉
```

交叉：

```text
血糖
思虑重
湿气
四肢乏力
肌肉松弛
腿沉
```

组合：

```text
脾经异常 + 膀胱经右低
→ 可能关联眼袋
```

---

### 6.3 肾经 kidney

肾经主骨，骨生髓，髓造血，通脑，关联记忆力、耳、肩颈腰、生殖系统、泌尿系统。

左低：

```text
耳鸣，尤其是嗡鸣声
阴虚
阴虚生内热
手心脚心热
体内像有一把火
容易缺水
五心烦躁
尿黄
尿短
```

右低：

```text
耳背
阳虚
夜尿
尿长
怕冷
宫寒
结合肝右低，容易掉发
```

交叉：

```text
结石
囊肿
腹部手术史
女性：剖腹产、人流、子宫肌瘤
男性：前列腺炎、前列腺钙化
```

---

### 6.4 胃经 stomach

胃经主消化。

左低：

```text
阴虚生内热
消化快
容易饿
```

右低：

```text
胃阳不足
胃胀
温度特别低时，可能吃什么拉什么
```

交叉：

```text
饮食不规律
胃炎
胃溃疡
消化不良
```

---

### 6.5 胆经 gallbladder

胆经主分泌胆汁、消化脂肪、决断力。

左低：

```text
胆红素高
皮肤黄
眼白黄
偏头痛
```

右低：

```text
胆固醇
脂肪瘤
优柔寡断
决断力不够
```

交叉：

```text
温度上不去时，容易胆结石、胆囊炎
不按时吃早餐
```

组合：

```text
胆左低 + 肝左低
→ 口干、口苦
```

---

### 6.6 膀胱经 bladder

膀胱经关联：

```text
肩颈
腰
生殖系统
泌尿系统
消化系统
呼吸系统
```

左低 / 右低：

```text
不单独对应具体问题，只作为辅助判断。
```

组合：

```text
肾左低 + 膀胱右低 → 颈椎问题
肾右低 + 膀胱左低 → 颈椎问题
肾左低 + 膀胱左低 → 腰椎问题
肾右低 + 膀胱右低 → 腰椎问题
肾经或膀胱经任意一个交叉 → 颈椎、腰椎同时存在
肾经或膀胱经任意一个整体平衡 → 不提出颈椎 / 腰椎问题
```

温差辅助：

```text
膀胱经左低或右低
且膀胱经左右温差大
且肾经存在异常
→ 关注肠道、生殖系统、肺部 / 呼吸道问题
```

相关问题：

```text
前列腺
子宫手术史
腰椎手术史
女性：人流、子宫肌瘤、剖腹产
男性：前列腺相关问题
```

---

## 7. 综合健康分算法

综合健康分是报告第一部分“健康总览”的核心展示内容。

评分不采用“100 分直接扣分法”，而是先计算内部问题指数 I，再将 I 映射为健康分。

### 7.1 评分目标

```text
首测大部分用户落在 63-75 分之间
63 分只出现在问题明显集中的用户身上
首测不轻易超过 75 分
复测时，如果用户持续使用仪器，分数应有改善空间
如果用户坚持使用仪器达到一定天数，复测分数不能下降
```

### 7.2 总公式

```text
I = A + B + C + D + E
```

其中：

```text
A = 低温指数
B = 温差指数
C = 偏侧指数
D = 经络趋势指数
E = 组合问题指数
```

---

### 7.3 A：低温指数

只看第二组 12 个温度值。

计算：

```text
M = 第二组 12 个数据的中位数
L = 第二组最低两个温度值的平均值
低温差距 = M - L
```

如果 `M - L < 0`，按 0 处理。

A 取值：

```text
低温差距 <= 0.5℃        A = 0
0.5℃ < 低温差距 <= 1℃   A = 2
1℃ < 低温差距 <= 2℃     A = 4
2℃ < 低温差距 <= 3℃     A = 6
低温差距 > 3℃           A = 8
```

---

### 7.4 B：温差指数

每条经络根据第二组温差计算基础指数：

```text
第二组温差 <= 0.2℃         0
0.2℃ < 第二组温差 <= 0.5℃  1
0.5℃ < 第二组温差 <= 2℃    2.5
第二组温差 > 2℃            5
```

再看前后温差变化：

```text
第二组温差 - 第一组温差 > 0.2℃   +0.5
第一组温差 - 第二组温差 > 0.2℃   -0.5
abs(第二组温差 - 第一组温差) <= 0.2℃   0
```

单经温差指数：

```text
单经温差指数 = max(0, 基础指数 + 修正值)
```

六条经络累计后封顶：

```text
B = min(六条经络单经温差指数之和, 16)
```

---

### 7.5 C：偏侧指数

只看第二组左右偏向统计。

```text
max_count = max(left_low_count, right_low_count)
```

C 取值：

```text
max_count < 4    C = 0
max_count = 4    C = 4
max_count = 5    C = 6
max_count = 6    C = 8
```

---

### 7.6 D：经络趋势指数

每条经络根据整体趋势计分：

```text
stable_balanced       0
potential_symptom     0.5
fast_response         0.5
stable_left_low       1
stable_right_low      1
cross                 2
```

六条经络累计后封顶：

```text
D = min(六条经络趋势指数之和, 8)
```

---

### 7.7 E：组合问题指数

**E1：肾经 + 膀胱经组合判断**

```text
未触发颈椎 / 腰椎问题      E1 = 0
触发 cervical              E1 = 3
触发 lumbar                E1 = 3
触发 cervical_and_lumbar   E1 = 4
```

**E2：肝经温度最低判断**

如果肝经是六条经络中第二组温度最低的（左或右）：

```text
肝经为六条最低            E2 = 3
```

**E 总分计算**

```text
E = E1 + E2
```

说明：颈椎和腰椎问题同时存在时 E1 = 4，单项问题 E1 = 3。肝经温度最低是比较严重的问题，需额外加 E2 = 3。

---

### 7.8 问题指数映射为健康分

根据问题指数 I 映射为原始健康分，确保所有测试结果最终落在63-88分区间。

```text
如果 I <= 5：
    score_raw = 88 - 1.6 * I        → 范围：80-88分（整体状态良好）

如果 5 < I <= 12：
    score_raw = 80 - 0.71 * (I - 5) → 范围：75-80分（轻度失衡）

如果 12 < I <= 20：
    score_raw = 75 - 0.625 * (I - 12) → 范围：70-75分（中度失衡）

如果 20 < I <= 30：
    score_raw = 70 - 0.7 * (I - 20) → 范围：63-70分（严重失衡）

如果 I > 30：
    score_raw = 63                  → 最低63分
```

首测展示分：

```text
first_test_score = clamp(score_raw, 63, 75)
display_score = round(first_test_score)
```

**首测分数控制在63-75分之间，确保用户有持续使用和复测的动力。**

### 7.9 分数区间解释

```text
63-70：严重失衡；需极度关注身体的健康调理
70-75：中度失衡；需重点关注身体的健康调理
75-80：轻度失衡；身体亚健康，需重视身体的健康情况
80-88：整体状态良好；继续保持
```

**说明**：所有测试结果最终分数控制在63-88分之间。首测最低63分，复测最高88分。

---

## 8. 复测评分规则

复测先按同一套规则计算本次 `score_raw` 和 `current_problem_index`，再加入测试次数加分、数据改善加分和复测保护。

### 8.1 测试次数加分

根据用户第几次测试，在真实温度反映的分数基础上额外加分：

```text
test_number = 1（首测）：        test_bonus = 0（首测不加，且上限 75）
test_number = 2（第二次）：      test_bonus = 4
test_number = 3（第三次）：      test_bonus = 5
test_number = 4（第四次）：      test_bonus = 6
test_number = 5（第五次）：      test_bonus = 7
test_number >= 6（第六次及以上）：test_bonus = 8
```

### 8.2 数据改善加分

```text
delta_I = previous_problem_index - current_problem_index
```

如果 `delta_I > 0`：

```text
improvement_bonus = min(3, 0.3 * delta_I)
```

如果 `delta_I <= 0`：

```text
improvement_bonus = 0
```

### 8.3 复测基础修正分

```text
retest_score_base = score_raw + test_bonus + improvement_bonus
```

### 8.4 复测保护

```text
usage_days_between_tests <= 2：
protected_score = retest_score_base

3 <= usage_days_between_tests <= 6：
protected_score = max(retest_score_base, previous_score - 2)

7 <= usage_days_between_tests <= 13：
protected_score = max(retest_score_base, previous_score)

14 <= usage_days_between_tests <= 29：
如果 previous_score < 88：
    protected_score = max(retest_score_base, previous_score + 1)
否则：
    protected_score = max(retest_score_base, previous_score)

usage_days_between_tests >= 30：
如果 previous_score < 88：
    protected_score = max(retest_score_base, previous_score + 2)
否则：
    protected_score = max(retest_score_base, previous_score)
```

复测最终展示分：

```text
retest_final_score = clamp(protected_score, 63, 88)
display_score = round(retest_final_score)
```

复测保护只影响综合健康分，不影响具体问题分析。

---

## 9. 重点问题排序与合并

“本次重点关注的问题”建议控制在 3-4 个。

优先级如下：

1. 第二组最低两个点  
2. 温差严重或加重问题  
3. 第二组整体左右偏向问题  
4. 颈椎 / 腰椎组合问题  
5. 交叉问题中同时伴随温差明显或最低点候选的问题

合并规则：

如果多个规则指向同一条经络或同一类问题，需要合并表达，不要重复输出。

示例：

```text
膀胱经是第二组最低点
膀胱经温差严重
膀胱经参与腰椎组合判断
```

应合并为：

```text
膀胱经问题最突出，需结合肾经关注腰椎、泌尿生殖、肠道及呼吸系统方向。
```

---

## 10. 报告输出结构

### 10.1 健康总览

包含：

```text
综合健康分
分数等级说明
整体状态总结
```

使用字段：

```text
score
problem_index
lowest_points
side_bias_summary
cervical_lumbar_result
serious_diff_meridians
focus_issues
```

### 10.2 本次重点关注的问题

使用：

```text
focus_issues
```

控制在 3-4 个，按优先级排序，并进行同类合并。

### 10.3 经络分析

逐一输出 6 条经络。

每条经络包含：

```text
经络名称
第一组左右状态
第二组左右状态
整体趋势
第一组温差
第二组温差
温差等级
温差变化
匹配到的问题
是否属于重点
```

### 10.4 调理建议

由 AI 根据已触发的问题生成。

AI 不能新增未被规则触发的问题，不能给药物建议，不能替代医生诊断，不能出现与性别不匹配的内容。

---

## 11. 建议接口输出结构

```json
{
  "score_result": {
    "score": 77,
    "score_raw": 77.48,
    "problem_index": 24.4,
    "problem_index_detail": {
      "low_temperature_index": 5,
      "temperature_difference_index": 8.5,
      "side_bias_index": 5,
      "trend_index": 3.4,
      "combo_index": 2.5
    }
  },
  "lowest_points": {
    "selected": [
      {
        "meridian": "bladder",
        "side": "left",
        "value": 37.9,
        "rank": 1,
        "must_report": true
      },
      {
        "meridian": "spleen",
        "side": "left",
        "value": 39.1,
        "rank": 2,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },
  "side_bias_summary": {
    "left_low_count": 5,
    "right_low_count": 0,
    "balanced_count": 1,
    "result": "head_blood_supply_attention"
  },
  "cervical_lumbar_result": {
    "kidney_trend": "stable_left_low",
    "bladder_trend": "stable_left_low",
    "result": "lumbar"
  },
  "meridian_analysis": [
    {
      "meridian": "spleen",
      "meridian_name": "脾经",
      "group1_status": "right_low",
      "group2_status": "left_low",
      "trend": "cross",
      "group1_diff": 0.1,
      "group2_diff": 1.5,
      "group1_diff_level": "balanced",
      "group2_diff_level": "health_problem",
      "diff_change": "worsened",
      "matched_rules": [
        "血糖",
        "思虑重",
        "湿气",
        "四肢乏力",
        "肌肉松弛",
        "腿沉"
      ],
      "is_focus": true,
      "focus_reason": [
        "second_group_lowest_point",
        "group2_diff_health_problem",
        "diff_worsened"
      ]
    }
  ],
  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "bladder",
      "title": "膀胱经问题较突出",
      "related_systems": [
        "肩颈",
        "腰",
        "泌尿系统",
        "生殖系统",
        "消化系统",
        "呼吸系统"
      ],
      "reason_codes": [
        "second_group_lowest_point",
        "group2_diff_serious_problem",
        "diff_worsened"
      ]
    }
  ],
  "gender_filtered": true
}
```

---

## 12. AI 生成报告约束

AI 可以做：

```text
合并重复问题
调整语言顺序
把规则结果改写成用户能看懂的话
根据已判定问题生成调理建议
适度弱化疾病诊断感
```

AI 不能做：

```text
不能新增规则库中没有的问题
不能新增未被数据触发的问题
不能输出药物建议
不能替代医生诊断
不能输出与用户性别不匹配的内容
不能把平衡经络强行说成有问题
```

---

## 13. 开发注意事项

1. 温度和温差统一保留 1 位小数后再判断。  
2. 左右完全相等才算平衡，差 0.1 也算低侧。  
3. 第二组最低两个点是报告必讲项，只有并列时才进入候选筛选。  
4. 膀胱经左低 / 右低没有独立具体问题，只做辅助分析。  
5. 第一组平衡 + 第二组偏低，归类为 `potential_symptom`。  
6. 第一组偏低 + 第二组平衡，归类为 `fast_response`。  
7. 肾经或膀胱经任意一个为 `stable_balanced`，不输出颈椎 / 腰椎问题。  
8. 肾经或膀胱经任意一个为 `cross`，输出颈椎和腰椎同时存在。  
9. `potential_symptom` 和 `fast_response` 暂不参与颈椎 / 腰椎强判断。  
10. 所有输出进入报告前，必须做性别过滤。  
11. 综合健康分是报告第一部分内容，必须与问题分析结果共用同一套中间计算结果。  
12. 复测保护只影响综合健康分，不影响具体问题分析。  
