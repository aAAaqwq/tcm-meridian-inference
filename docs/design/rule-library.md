# 规则库设计

> 版本：0.2.0 | 来源：`docs/六条经络辩证.xlsx`

## 规则文件

| 文件 | 说明 |
|------|------|
| `rules/thresholds.json` | 温度阈值、评分参数 |
| `rules/meridian_rules.json` | 六经单经规则（18 条） |
| `rules/combination_rules.json` | 组合判症规则（6 条） |

## 规则类型

### 1. 单经规则（meridian_rules.json）

每条经络 3 条规则：`left_low`、`right_low`、`cross`，共 18 条。

结构：

```json
{
  "id": "liver_left_low",
  "meridian": "liver",
  "status": "left_low",
  "tag": "left_low",
  "penaltyKey": "left_low",
  "conditions": [{"field": "left", "op": "<", "valueFrom": "thresholds.temperature.lowMin"}],
  "summary": "肝左低：代谢侧偏弱",
  "symptoms": ["代谢差", "气虚", ...],
  "advice": ["关注代谢与睡眠节律", ...]
}
```

条件字段说明：
- `field`：取自输入计算的字段（left、right、avg、diffAbs、trendDelta、trendAbs）
- `op`：比较操作（<、<=、>、>=、==）
- `valueFrom`：从 `thresholds.json` 动态取值（格式：`thresholds.xxx.yyy`）
- `value`：静态阈值

### 2. 组合规则（combination_rules.json）

跨经络联动判症，共 6 条：

| ID | 名称 | 条件 |
|----|------|------|
| `liver_gallbladder_left_low_transaminase` | 转氨酶偏高 | 肝左低 + 胆左低 |
| `kidney_bladder_opposite_low_cervical` | 颈椎风险提示 | 肾膀相反方向低 |
| `kidney_bladder_same_side_low_lumbar` | 腰椎风险提示 | 肾膀同方向低 |
| `right_side_four_plus_heart_supply` | 心脏供血注意 | >=4 条 right_low |
| `left_side_four_plus_head_supply` | 头部供血注意 | >=4 条 left_low |
| `kidney_bladder_spleen_cervical_plus` | 颈椎加重提示 | 脾左低 + 肾膀相反低 |

条件语法：
- `allStatuses`：所有条件必须满足
- `anyOf`：满足任一子句即可
- `minStatusCount`：满足某状态的最少经络数

## 状态判定优先级

单经主状态判定顺序：

1. 如果仅有 `left_low` → `left_low`
2. 如果仅有 `right_low` → `right_low`
3. 如果有 `cross` → `cross`
4. 如果同时有 `left_low` 和 `right_low` → `left_low`
5. 其他 → `stable`

`cross` 仍保留在 `tags` 中用于追踪，但不一定作为主状态。

## 数据规避

以下 Excel 内容**未进入规则库**：
- "偏父亲/偏母亲体质"、"生男孩/生女孩"等不可验证的强结论
- 胃经相关：Excel 标注"可以忽略不讲"，但已保留规则供后续激活

## 设计原则

1. **JSON 驱动**：规则数据与推理代码分离，修改阈值/症状不需要改 Python
2. **可追溯**：每条规则有 `id`、`summary`、`source`，输出中有 `trace` 完整记录命中
3. **安全边界**：所有输出文案必须包含"不等同于医疗诊断"免责声明
