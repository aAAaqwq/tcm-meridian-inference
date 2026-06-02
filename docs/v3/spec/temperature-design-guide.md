# V3 推理引擎温度数据设计指南

根据目标分数反推温度分布参数的完整指南。

## 1. 评分算法回顾

### 1.1 问题指数计算

```
I = A + B + C + D + E

A: 低温指数 (0-8)
B: 温差指数 (0-16)
C: 偏侧指数 (0/4/6/8)
D: 趋势指数 (0-8)
E: 组合问题 (0-7)
```

### 1.2 分数映射公式

```
I <= 5:        score = 88 - 1.6 * I              → 80-88分 (整体良好)
5 < I <= 12:   score = 80 - 0.71 * (I - 5)       → 75-80分 (轻度失衡)
12 < I <= 20:  score = 75 - 0.625 * (I - 12)     → 70-75分 (中度失衡)
20 < I <= 30:  score = 70 - 0.7 * (I - 20)       → 63-70分 (严重失衡)
I > 30:        score = 63                        → 最低分
```

## 2. 目标分数 → PI 反推公式

```python
def target_pi_from_score(target_score):
    """根据目标分数计算所需PI值"""
    if target_score >= 80:
        # 80-88分: I <= 5
        # score = 88 - 1.6 * I
        # I = (88 - score) / 1.6
        return (88 - target_score) / 1.6
    elif target_score >= 75:
        # 75-80分: 5 < I <= 12
        # score = 80 - 0.71 * (I - 5)
        # I = 5 + (80 - score) / 0.71
        return 5 + (80 - target_score) / 0.71
    elif target_score >= 70:
        # 70-75分: 12 < I <= 20
        # score = 75 - 0.625 * (I - 12)
        # I = 12 + (75 - score) / 0.625
        return 12 + (75 - target_score) / 0.625
    elif target_score >= 63:
        # 63-70分: 20 < I <= 30
        # score = 70 - 0.7 * (I - 20)
        # I = 20 + (70 - score) / 0.7
        return 20 + (70 - target_score) / 0.7
    else:
        return 30  # 最低分

# 常用目标分数对应PI参考表
PI_REFERENCE = {
    88: 0.0,   85: 1.9,   82: 3.8,   80: 5.0,
    78: 7.8,   76: 10.6,  75: 12.0,  73: 15.2,
    71: 18.4,  70: 20.0,  68: 22.9,  66: 25.7,
    65: 27.1,  63: 30.0,
}
```

## 3. 温度设计模板

### 3.1 基础结构

```json
{
  "_comment": "目标分数XX分，所需PI约YY",
  "measurement_type": "first_test",
  "gender": "female",
  "meridians": {
    "stomach":     { "group1_left": X, "group1_right": X, "group2_left": X, "group2_right": X },
    "gallbladder": { "group1_left": X, "group1_right": X, "group2_left": X, "group2_right": X },
    "bladder":     { "group1_left": X, "group1_right": X, "group2_left": X, "group2_right": X },
    "liver":       { "group1_left": X, "group1_right": X, "group2_left": X, "group2_right": X },
    "spleen":      { "group1_left": X, "group1_right": X, "group2_left": X, "group2_right": X },
    "kidney":      { "group1_left": X, "group1_right": X, "group2_left": X, "group2_right": X }
  },
  "expected": {
    "target_score": XX,
    "score_level": "XX失衡"
  }
}
```

### 3.2 按目标分数设计温度

#### 目标 75-80 分 (轻度失衡，PI: 5-12)

**设计要点：**
- 低温差距: 0.5-1.5℃ (A = 2-4)
- 偏侧数量: 2-3条经络 (C = 0-4)
- 温差: 0.5-1.5℃ (B ≈ 3-6)
- 趋势: 少量稳定左低/右低 (D ≈ 3-5)

**模板示例：**
```json
{
  "stomach":     { "g1_left": 37.0, "g1_right": 37.0, "g2_left": 39.0, "g2_right": 40.0 },  // potential_symptom, diff=1.0
  "gallbladder": { "g1_left": 37.0, "g1_right": 37.5, "g2_left": 39.0, "g2_right": 40.0 },  // left_low, diff=1.0
  "bladder":     { "g1_left": 37.0, "g1_right": 37.0, "g2_left": 39.0, "g2_right": 39.5 },  // right_low, diff=0.5
  "liver":       { "g1_left": 37.2, "g1_right": 37.2, "g2_left": 39.2, "g2_right": 40.0 },  // right_low, diff=0.8
  "spleen":      { "g1_left": 37.0, "g1_right": 37.0, "g2_left": 39.0, "g2_right": 39.0 },  // balanced
  "kidney":      { "g1_left": 37.0, "g1_right": 37.0, "g2_left": 39.0, "g2_right": 39.0 }   // balanced
}
// 估算: A=2, B≈5, C=4(2条偏侧), D≈3, E=0 → PI≈14 → score≈75
```

#### 目标 70-75 分 (中度失衡，PI: 12-20)

**设计要点：**
- 低温差距: 1.0-2.0℃ (A = 4-6)
- 偏侧数量: 3-4条经络 (C = 4)
- 温差: 1.0-2.0℃ (B ≈ 6-10)
- 趋势: 稳定左低/右低 (D ≈ 5-6)

**模板示例：**
```json
{
  "stomach":     { "g1_left": 36.0, "g1_right": 38.0, "g2_left": 38.0, "g2_right": 40.0 },  // cross, diff=2.0
  "gallbladder": { "g1_left": 36.5, "g1_right": 37.0, "g2_left": 38.5, "g2_right": 40.0 },  // left_low, diff=1.5
  "bladder":     { "g1_left": 36.5, "g1_right": 36.5, "g2_left": 38.0, "g2_right": 40.0 },  // right_low, diff=2.0
  "liver":       { "g1_left": 36.8, "g1_right": 36.8, "g2_left": 38.8, "g2_right": 40.0 },  // right_low, diff=1.2
  "spleen":      { "g1_left": 36.5, "g1_right": 37.0, "g2_left": 38.5, "g2_right": 40.0 },  // left_low, diff=1.5
  "kidney":      { "g1_left": 36.8, "g1_right": 36.8, "g2_left": 38.8, "g2_right": 39.5 }   // left_low, diff=0.7
}
// 估算: A=4, B≈10, C=4(4条偏侧), D≈5(1条cross+4条stable), E=0 → PI≈23 → score≈68
// 调整: 减少交叉，降低温差 → PI≈16 → score≈73
```

#### 目标 65-70 分 (严重失衡，PI: 20-30)

**设计要点：**
- 低温差距: 2.0-3.0℃ (A = 6-8)
- 偏侧数量: 4-6条经络 (C = 4-8)
- 温差: 1.5-3.0℃ (B ≈ 8-14)
- 趋势: 交叉或稳定低 (D ≈ 6-8)
- 组合问题: 触发颈椎/腰椎 (E = 3-4)

**模板示例：**
```json
{
  "stomach":     { "g1_left": 35.0, "g1_right": 37.0, "g2_left": 37.5, "g2_right": 40.0 },  // cross, diff=2.5
  "gallbladder": { "g1_left": 35.5, "g1_right": 36.0, "g2_left": 38.0, "g2_right": 40.5 },  // left_low, diff=2.5
  "bladder":     { "g1_left": 35.0, "g1_right": 35.5, "g2_left": 37.0, "g2_right": 40.0 },  // right_low, diff=3.0
  "liver":       { "g1_left": 35.5, "g1_right": 35.5, "g2_left": 37.5, "g2_right": 40.0 },  // right_low, diff=2.5
  "spleen":      { "g1_left": 35.5, "g1_right": 36.0, "g2_left": 37.5, "g2_right": 40.5 },  // left_low, diff=3.0
  "kidney":      { "g1_left": 35.0, "g1_right": 35.0, "g2_left": 37.0, "g2_right": 40.0 }   // right_low, diff=3.0 → 腰椎
}
// 估算: A=8, B≈14, C=8(6条偏侧), D≈8, E=3(腰椎) → PI≈33 → score=63
// 调整: 减少1-2条偏侧，降低温差 → PI≈27 → score≈66
```

## 4. 具体修正建议

### 4.1 test_04_significant_imbalance (目标73分)

**当前问题：**
- 温度范围 26-44℃，低温差距7.0℃ → A=8
- 6条交叉 → D=8 (封顶)
- 实际PI=40，分数=63

**修正方案：**
```json
{
  "stomach":     { "g1_left": 35.0, "g1_right": 37.0, "g2_left": 38.0, "g2_right": 40.0 },  // cross → stable_left_low
  "gallbladder": { "g1_left": 36.0, "g1_right": 36.0, "g2_left": 38.0, "g2_right": 40.0 },  // cross → stable_left_low
  "bladder":     { "g1_left": 35.0, "g1_right": 35.0, "g2_left": 37.0, "g2_right": 40.0 },  // 保持
  "liver":       { "g1_left": 35.0, "g1_right": 37.0, "g2_left": 38.0, "g2_right": 40.0 },  // cross → stable_right_low
  "spleen":      { "g1_left": 36.0, "g1_right": 36.0, "g2_left": 38.0, "g2_right": 40.0 },  // cross → stable_left_low
  "kidney":      { "g1_left": 35.0, "g1_right": 35.0, "g2_left": 37.0, "g2_right": 40.0 }   // 保持
}
// 调整后: A=6, B≈12, C=8, D≈6(无交叉), E=3 → PI≈25 → score≈69
// 再降低低温差距到1.5 → A=4 → PI≈23 → score≈71
```

### 4.2 test_44_score_65_pi_46 (目标65分)

**当前问题：**
- 偏侧5条但温差不足 → PI=13，实际分数74

**修正方案：**
- 增加低温点到33℃ (低温差距2.0℃)
- 增加温差到1.5-2.0℃
- 确保6条偏侧

```json
{
  "stomach":     { "g1_left": 33.0, "g1_right": 37.0, "g2_left": 35.0, "g2_right": 40.0 },  // 低温+温差
  "gallbladder": { "g1_left": 34.0, "g1_right": 36.0, "g2_left": 36.0, "g2_right": 40.0 },  // 低温+温差
  "bladder":     { "g1_left": 33.0, "g1_right": 35.0, "g2_left": 35.0, "g2_right": 39.0 },  // 低温+温差
  "liver":       { "g1_left": 34.0, "g1_right": 37.0, "g2_left": 36.0, "g2_right": 40.0 },  // 低温+温差
  "spleen":      { "g1_left": 33.0, "g1_right": 36.0, "g2_left": 35.0, "g2_right": 40.0 },  // 低温+温差
  "kidney":      { "g1_left": 34.0, "g1_right": 35.0, "g2_left": 36.0, "g2_right": 39.0 }   // 低温+温差
}
// 调整后: A=8, B≈14, C=8, D≈6, E=0 → PI≈27 → score≈66
```

## 5. 快速参考表

| 目标分数 | 所需PI | 低温差距 | 偏侧数 | 平均温差 | 交叉数 |
|---------|-------|---------|-------|---------|-------|
| 88 | 0 | <0.5 | 0 | <0.5 | 0 |
| 80 | 5 | 0.5 | 0-1 | 0.5 | 0 |
| 78 | 8 | 0.5-1 | 2 | 0.8 | 0 |
| 76 | 11 | 1 | 3 | 1.0 | 0-1 |
| 75 | 12 | 1-1.5 | 3-4 | 1.2 | 0-1 |
| 73 | 15 | 1.5 | 4 | 1.5 | 0-1 |
| 71 | 18 | 1.5-2 | 4 | 1.8 | 1 |
| 70 | 20 | 2 | 4-5 | 2.0 | 1-2 |
| 68 | 23 | 2-2.5 | 5-6 | 2.2 | 1-2 |
| 66 | 26 | 2.5-3 | 5-6 | 2.5 | 2-3 |
| 65 | 27 | 2.5-3 | 6 | 2.5 | 2-3 |
| 63 | 30+ | >3 | 6 | >3 | 3+ |

## 6. 验证工具

使用以下脚本验证温度设计：

```bash
python tests/validate_temperature.py fixtures/v3/your_test.json
```

输出将显示：
- 估算PI值
- 各分量(A/B/C/D/E)
- 预期分数
- 与目标分数的偏差
