# Expert Rule Library 接入说明（首批）

## 1. 这次交付了什么

本次不是只做分析，而是已经把 Excel《六条经络辩症》拆成了一份**可程序消费**的核心规则库：

- `knowledge/expert_rules/foot_six_meridian.rule_set.core.json`
- `schemas/expert_rule_library.schema.json`
- `docs/expert-rule-library-integration.md`

其中：
- JSON 文件是实际规则库
- schema 用于校验规则格式一致性
- 本文档告诉 code agent 如何接入

---

## 2. 为什么先用 JSON 而不是 YAML

当前项目是 Python MVP，且已有 fixture / schema / ruleHits 输出风格，JSON 的优点是：

- 标准库可直接加载，不新增依赖
- 更容易做 schema 校验
- 更适合 API/配置中心分发
- 对后续前后端共享更稳定

后续如果业务侧更偏向人工维护，也可以在此 JSON 结构稳定后再增加 YAML 编译层。

---

## 3. 规则库设计原则

### 3.1 分层思想

不要把 Excel 文案直接硬编码到 Python if/else 里。

建议拆成三层：

1. **输入层**：原始测量值（左右温度、前后测量值、上下文）
2. **特征层 / 信号层**：产出标准化 signal，例如：
   - `side_state = left_low/right_low/cross_low/...`
   - `trend = down_strong/down_mild/stable/...`
   - `delta`
   - `abs_lr_delta`
3. **规则层**：读取 JSON 规则库，按 `conditions` 匹配并输出 ruleHits

这次交付的是第 3 层，同时把第 2 层所需信号契约写进了 JSON 顶层 `inputSignalContract`。

---

## 4. 当前规则库覆盖范围

### 4.1 已覆盖的单经络规则

已抽取脚上六条经络核心规则：

- 肝：左低 / 右低 / 交叉
- 脾：左低 / 右低 / 交叉
- 肾：左低 / 右低 / 交叉
- 胃：左低 / 右低 / 交叉（低优先级，待客户确认）
- 胆：左低 / 右低 / 交叉
- 膀胱：左低 / 右低 / 交叉

### 4.2 已覆盖的趋势类规则

已加入首批可落地趋势规则：

- 肝经下降趋势明显
- 肾经下降趋势明显
- 脾经下降趋势明显

说明：
这些 trend 规则不是 Excel 原文逐字存在，而是为了让程序能真正消费、复用现有 MVP `trend` 概念而补上的工程化规则，因此已在 `source` / `assumption` 中明确标注。

### 4.3 已覆盖的组合 / 聚合规则

已加入若干高价值组合规则：

- 肝左低 + 胆左低 → 肝胆联动重点关注
- 左肾低 + 右膀胱低 → 颈椎关注
- 右肾低 + 左膀胱低 → 颈椎关注
- 左肾低 + 左膀胱低 → 腰椎关注
- 右肾低 + 右膀胱低 → 腰椎关注
- 六经中 ≥4 条偏右低 → 心脏供血关注
- 六经中 ≥4 条偏左低 → 头部供血关注

---

## 5. 建议的接入方式

## 5.1 不要直接替换现有 engine

当前项目已有：

- `features.py`：基于 `t1/t2` 生成 trend / delta
- `rules.py`：基于固定阈值生成命中规则

建议不要一次性推翻，而是采用**并行扩展**：

### Phase A：保留现有 MVP，引入新规则库模块

新增建议：

- `src/tcm_meridian_inference/expert_rule_loader.py`
- `src/tcm_meridian_inference/expert_rule_engine.py`
- `src/tcm_meridian_inference/side_features.py`

职责建议：

#### `side_features.py`
负责把原始左右经络数据标准化为：

```json
{
  "liver": {
    "side_state": "left_low",
    "trend": "down_strong",
    "delta": -0.8,
    "abs_lr_delta": 0.6
  }
}
```

#### `expert_rule_loader.py`
负责：

- 加载 `knowledge/expert_rules/foot_six_meridian.rule_set.core.json`
- 做 schema 校验（可选，推荐）
- 缓存 rule set

#### `expert_rule_engine.py`
负责：

- 遍历 rules
- 根据 `conditions` 做匹配
- 按 `priority` 排序
- 输出：
  - 命中的 `ruleHits`
  - 合并后的 `riskTags`
  - 合并后的 `recommendations`

---

## 5.2 条件解释器最小实现建议

当前规则里只用了 3 类条件：

1. `all`
2. `any`
3. `count`

所以最小解释器可以非常简单。

### `all` 示例

```json
{
  "all": [
    { "fact": "side_state", "meridian": "liver", "operator": "eq", "value": "left_low" }
  ]
}
```

含义：

- `signals["liver"]["side_state"] == "left_low"`

### `count` 示例

```json
{
  "count": {
    "fact": "side_state",
    "operator": "eq",
    "value": "right_low",
    "meridians": ["liver", "spleen", "kidney", "stomach", "gallbladder", "bladder"],
    "gte": 4
  }
}
```

含义：

- 6 条经络里，满足 `side_state == right_low` 的数量 ≥ 4

---

## 6. 当前项目与 Excel 的结构差异

这是 code agent 接入前**必须知道**的一点：

当前 MVP `schemas.py` 固定要求的六条经络是：

- `lung`
- `pericardium`
- `heart`
- `spleen`
- `liver`
- `kidney`

但 Excel 的脚上六经是：

- `liver`
- `spleen`
- `kidney`
- `stomach`
- `gallbladder`
- `bladder`

也就是说，**规则库与当前输入 schema 不完全同构**。

### 这意味着什么？

如果要真正接 Excel 规则库，至少有两种路线：

### 路线 1：扩展 schema（推荐）

把输入改造成支持脚上六经 + 左右侧数据，例如：

```json
{
  "measurements": {
    "liver": { "left": 35.2, "right": 35.8, "t1": 35.5, "t2": 35.3 },
    "spleen": { ... },
    "kidney": { ... },
    "stomach": { ... },
    "gallbladder": { ... },
    "bladder": { ... }
  }
}
```

优点：
- 真正贴合规则来源
- 后续最容易扩展

缺点：
- 需要改现有 schema / fixture / tests

### 路线 2：先做映射层（过渡方案）

保留现有主引擎不动，新增一个 `expert_rules_v2` 分支，只给脚上六经专用。

优点：
- 风险低
- 不影响当前演示版

缺点：
- 短期内存在两套规则/输入模型

我的建议：**先走路线 2，稳定后再统一。**

---

## 7. 输出格式建议

建议命中规则后，输出结构保留现有 MVP 风格：

```json
{
  "ruleId": "FSM-COMBO-LIVER-L-GB-L-022",
  "name": "肝左低 + 胆左低",
  "category": "combination",
  "meridian": "multi",
  "riskLevel": "high",
  "signals": ["transaminase_attention", "hepatic_biliary_linkage"],
  "explanation": "肝经与胆经同时左低，属于 Excel 明确给出的组合规则...",
  "recommendations": ["建议结果中明确标注“肝胆联动关注”。"],
  "priority": 98,
  "source": { ... }
}
```

然后再在 engine 里按下面方式汇总：

- 单经络命中 → 填入 `meridianResults[meridian].ruleHits`
- 组合规则命中 → 放到全局 `trace.comboRuleHits`
- 聚合规则命中 → 转成 `riskTags`
- recommendations 去重后输出

---

## 8. 自查结果：我已经主动规避了哪些脏数据/歧义

### 8.1 已规避

以下 Excel 内容**没有直接进入首批自动规则**：

- “偏父亲 / 偏母亲体质”
- “生男孩 / 生女孩”
- 过于强结论化且难验证的话术

原因：
- 不适合自动化输出
- 容易引发不必要争议
- 稳定性不足

### 8.2 已保留但打标待确认

- 胃经相关规则：`pendingConfirmation = true`
- 交叉失衡 `cross_low` 的精确定义：需要客户确认算法口径
- trend 规则阈值：当前建议沿用现有 MVP 的 `significant_drop` 等阈值

---

## 9. code agent 下一步最值得做的事

优先级建议：

1. **新增脚上六经输入 schema**
2. **补 side_state 计算逻辑**（left_low/right_low/cross_low）
3. **实现 JSON 规则解释器**
4. **把命中规则并入现有输出结构**
5. **补 fixtures + pytest**

推荐先做一个最小闭环：

- 1 个 fixture
- 覆盖 1 条单经络规则
- 覆盖 1 条组合规则
- 覆盖 1 条 aggregate 规则

这样能最快验证规则库不是死文件，而是真能跑起来。

---

## 10. 我建议客户尽快确认的点

1. `cross_low` 的精确定义到底是什么
   - 是左右交叉？
   - 还是“左右温差明显 + 与趋势相反”？
   - 还是设备算法内部已有定义？

2. 胃经是否进入正式自动输出
   - Sheet2 写了“可以忽略不讲”
   - 但 Sheet1 仍给了可解释内容

3. 是否允许系统自动输出“供血不足”等较强措辞
   - 如果不允许，应统一降级为“关注/建议进一步确认”

4. 当前真实设备输入是否具备左右侧原始值
   - 如果没有左右侧原始值，就无法稳定计算 `left_low/right_low/cross_low`

---

## 11. 结论

这次交付已经满足“不是只交文档，而是交真正规则库文件”的要求。

并且规则库具备以下特性：

- 可程序消费
- 有稳定字段
- 有 source 回溯
- 有 assumptions/pendingConfirmation 控制脏数据
- 覆盖单经络、趋势、组合、聚合四类规则
- 可以直接成为下一轮 code agent 接入的基础输入
