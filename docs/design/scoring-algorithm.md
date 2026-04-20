# 评分算法

> 版本：0.2.0 | 更新：2026-04-20

## 概述

本系统采用 **规则驱动扣分制**：每条经络基础分 100，按命中规则累减，最终取六经平均值。

LLM（Hybrid 模式）不参与评分计算，只负责生成自然语言文案。分数、状态、症状、组合判症全部由规则引擎确定。

---

## 1. 单经评分

### 规则与扣分

| 规则 | 触发条件 | 扣分 | 配置位置 |
|------|----------|------|----------|
| `left_low` | 左侧温度 < 35.3°C | -16 | `thresholds.temperature.lowMin` |
| `right_low` | 右侧温度 < 35.3°C | -16 | `thresholds.temperature.lowMin` |
| `cross` | 左右温差绝对值 > 0.6°C | -20 | `thresholds.temperature.leftRightDiffWarn` |
| `high` | 温度 > 36.9°C | -10 | `thresholds.temperature.highMax` |
| `trend` | 趋势变化绝对值 > 0.4°C | -8 | `thresholds.temperature.trendDeltaWarnAbs` |

单经可以同时命中多条规则，扣分叠加。例如左侧偏低且温差大：`100 - 16(left_low) - 20(cross) = 64`。

单经评分范围：0 ~ 100（`floor=0, ceiling=100`）。

### 阈值配置

所有阈值定义在 `rules/thresholds.json`：

```json
{
  "temperature": {
    "normalMin": 35.6,
    "normalMax": 36.6,
    "lowMin": 35.3,
    "highMax": 36.9,
    "leftRightDiffWarn": 0.6,
    "trendDeltaWarnAbs": 0.4,
    "sideCountWarn": 4
  },
  "scoring": {
    "base": 100,
    "penalty": {
      "left_low": 16, "right_low": 16,
      "cross": 20, "high": 10, "trend": 8, "combo": 6
    },
    "floor": 0, "ceiling": 100
  }
}
```

---

## 2. 组合扣分

当组合规则命中时（如"肝左低+胆左低→转氨酶偏高"），**只对参与该组合的经络**扣 6 分。

### 组合规则列表

| 组合 | 涉及经络 | 条件 |
|------|----------|------|
| 转氨酶偏高 | liver, gallbladder | 两者均 left_low 或均 right_low |
| 颈椎风险提示 | kidney, bladder | 两者相反方向低 |
| 腰椎风险提示 | kidney, bladder | 两者同方向低 |
| 心脏供血注意 | 全部（>=4 条 right_low） | minStatusCount >= 4 |
| 头部供血注意 | 全部（>=4 条 left_low） | minStatusCount >= 4 |
| 颈椎加重提示 | spleen, kidney, bladder | 脾左低 + 肾膀相反低 |

### 扣分逻辑

```
对每个命中的组合规则：
  involved = 提取该规则中涉及的经络列表
  对 involved 中每条非 stable 经络：
    score -= combo_penalty (6)
```

注意：`minStatusCount` 类规则（如"头部供血注意"）涉及所有经络，因此所有非 stable 经络都会被扣分。而"肝胆组合"只涉及 liver 和 gallbladder。

---

## 3. 综合评分

```
healthScore = round(sum(六经单经评分) / 6, 1)
```

### 评分等级

| 等级 | 分数范围 | 含义 |
|------|----------|------|
| 优秀 | 85-100 | 整体平稳 |
| 良好 | 70-84 | 轻微偏差 |
| 注意 | 55-69 | 存在需要关注的信号 |
| 预警 | <55 | 多条经络失衡，建议复测 |

---

## 4. 计算示例

### case_left_low.json（所有经络左侧偏低）

所有经络命中 `left_low`(-16) + `cross`(-20) = 64：

| 经络 | 单经规则 | 参与的组合 | 最终分数 |
|------|----------|-----------|---------|
| liver | 64 | 肝胆组合(-6) + 头部供血(-6) | **52** |
| spleen | 64 | 头部供血(-6) | **58** |
| kidney | 64 | 腰椎(-6) + 头部供血(-6) | **52** |
| stomach | 64 | 头部供血(-6) | **58** |
| gallbladder | 64 | 肝胆组合(-6) + 头部供血(-6) | **52** |
| bladder | 64 | 腰椎(-6) + 头部供血(-6) | **52** |

**healthScore = (52+58+52+58+52+52) / 6 = 54.0（注意）**

spleen/stomach 得分更高（58），因为它们没有参与肝胆/腰椎组合。

### case_stable.json（整体平稳）

所有经络温度差 < 0.6°C，无规则命中 → 全部 100 分。

**healthScore = 100.0（优秀）**

### case_cross.json（交叉）

kidney 和 bladder 命中 `cross` + `left_low`/`right_low`，且方向相反 → 颈椎组合命中。

**healthScore = 62.0（注意）**
