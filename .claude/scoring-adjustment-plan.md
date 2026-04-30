# 评分系统调整方案

## 问题诊断

当前评分系统扣减分值过高，导致：
- 轻微问题就跌到80分以下
- 用户感觉"很吓人"，体验不好
- 无法体现"亚健康"概念

## 目标评分区间

| 分数 | 状态描述 | 目标用户感受 |
|------|----------|--------------|
| 90-100 | 身体很好 | 安心，继续保持 |
| 75-90 | 亚健康 | 需要注意，但不恐慌 |
| 60-75 | 身体有大问题 | 需要重视和调理 |
| <60 | 严重问题 | 必须立即就医 |

---

## Plan A: 温和扣减版（推荐）

**核心思路**：降低所有扣减分值约50%，设置更高的保底分

### 修改内容

1. **score_rules.json** - 扣减规则调整
```json
{
  "deductions": [
    { "rule_id": "single_meridian_mild_abnormal", "score": -0.5 },
    { "rule_id": "single_meridian_obvious_abnormal", "score": -1.5 },
    { "rule_id": "single_meridian_cross", "score": -2 },
    { "rule_id": "kidney_bladder_double_cross", "score": -4 },
    { "rule_id": "multi_cross", "score": -4 },
    { "rule_id": "right_bias", "score": -3 },
    { "rule_id": "left_bias", "score": -3 },
    { "rule_id": "heart_supply_hit", "score": -3 },
    { "rule_id": "head_supply_hit", "score": -3 },
    { "rule_id": "neck_waist_reproductive_hit", "score": -2.5 },
    { "rule_id": "mass_risk_hit", "score": -4 },
    { "rule_id": "multi_imbalance", "score": -5 }
  ],
  "min_score": 50,
  "max_score": 100
}
```

2. **加分规则** - 保持不变

3. **等级区间** - 保持不变（已符合目标）

### 预期效果

| 场景 | 旧评分 | 新评分 | 说明 |
|------|--------|--------|------|
| 全部正常 | 100 | 100 | 无变化 |
| 1个轻度异常 | 98 | 99.5 | 几乎无感 |
| 2个中度异常 | 92 | 97 | 温和提醒 |
| 1个交叉问题 | 96 | 98 | 不恐慌 |
| 肾膀胱双交叉 | 92 | 96 | 亚健康 |
| 多问题组合 | 60-70 | 75-85 | 可接受范围 |

### 优点
- ✅ 改动最小，风险低
- ✅ 向后兼容性好
- ✅ 逻辑简单可预测

### 缺点
- ⚠️ 对于严重问题分数可能偏高

---

## Plan B: 等级保护版

**核心思路**：高分区域扣分减半，低分区域扣分加重

### 修改内容

1. **infer.py** - 添加保护逻辑
```python
def apply_score_protection(score: float, deductions: list) -> float:
    """根据当前分数应用保护机制"""
    if score >= 90:
        # 高分保护：扣分减半
        return score - sum(d['score'] for d in deductions) * 0.5
    elif score >= 75:
        # 正常扣分
        return score - sum(d['score'] for d in deductions)
    else:
        # 低分加重：扣分1.2倍
        return score - sum(d['score'] for d in deductions) * 1.2
```

2. **score_rules.json** - 基础扣减不变，增加保护开关

### 优点
- ✅ 鼓励保持高分状态
- ✅ 严重问题仍能被反映

### 缺点
- ⚠️ 逻辑复杂，难以解释
- ⚠️ 可能产生非直观的结果

---

## Plan C: 加权平均版

**核心思路**：从"扣分制"改为"加权平均制"

### 修改内容

1. **新算法设计**
```python
def calculate_weighted_score(meridian_states: dict) -> float:
    """加权平均评分"""
    weights = {
        "liver": 0.20,
        "spleen": 0.18,
        "kidney": 0.20,
        "stomach": 0.15,
        "gallbladder": 0.15,
        "bladder": 0.12
    }
    
    # 每个经络基础分
    meridian_scores = {
        "normal": 100,
        "mild": 90,
        "medium": 75,
        "high": 60,
        "cross": 70
    }
    
    weighted_sum = sum(
        meridian_scores[state["status"]] * weights[m]
        for m, state in meridian_states.items()
    )
    
    # 应用组合规则系数
    combo_multiplier = calculate_combo_multiplier(combination_hits)
    
    return weighted_sum * combo_multiplier
```

### 优点
- ✅ 更符合健康评估的科学性
- ✅ 每个经络独立评估

### 缺点
- ⚠️ 改动巨大，需要全面重构
- ⚠️ 难以向后兼容
- ⚠️ 用户理解成本高

---

## Plan D: 分段保底版

**核心思路**：设置多个保底分，防止分数暴跌

### 修改内容

1. **分段保底逻辑**
```python
def apply_floor_protection(score: float, meridian_states: dict) -> float:
    """分段保底保护"""
    # 计算问题严重程度
    problem_count = sum(1 for s in meridian_states.values() if s["status"] != "normal")
    
    # 根据问题数量设置保底分
    if problem_count <= 1:
        return max(score, 90)  # 单问题保底90
    elif problem_count <= 3:
        return max(score, 80)  # 多问题保底80
    elif problem_count <= 5:
        return max(score, 65)  # 较多问题保底65
    else:
        return max(score, 50)  # 严重问题保底50
```

2. **结合Plan A的温和扣减**

### 优点
- ✅ 分数不会剧烈波动
- ✅ 给用户心理安全感

### 缺点
- ⚠️ 可能掩盖真实问题
- ⚠️ 不同场景下的保底分不一致

---

## 推荐方案

**首选：Plan A 温和扣减版**

理由：
1. 改动最小，当天可上线
2. 风险可控，可随时回滚
3. 用户感知明显，体验提升

**备选：Plan A + D 组合**

如果需要更强的保底效果，可以结合 Plan A 的温和扣减 + Plan D 的单问题保底90分机制。

---

## 实施步骤

1. 修改 `rules/score_rules.json`
2. 验证 `scripts/infer.py` 支持小数扣减
3. 运行测试验证新评分分布
4. 灰度发布，观察用户反馈
5. 必要时微调参数

## 回滚方案

保留原 `score_rules.json.bak`，如出现问题可立即回滚。
