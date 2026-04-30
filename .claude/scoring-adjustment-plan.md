# 评分系统调整方案 (已实施)

## 版本信息

- **实施版本**: v2.1
- **实施日期**: 2026-04-29
- **状态**: ✅ 已完成并上线

---

## 问题诊断

原评分系统扣减分值过高，导致：
- 轻微问题就跌到80分以下
- 用户感觉"很吓人"，体验不好
- 无法体现"亚健康"概念

---

## 最终评分标准

| 分数区间 | 等级 | 用户感受 | 说明 |
|---------|------|---------|------|
| 90-100 | 整体状态较好 | 身体很好，安心 | 继续保持 |
| 75-90 | 轻度失衡 | 亚健康，需注意 | 不恐慌，关注即可 |
| 60-75 | 中度失衡 | 身体有大问题 | 需要重视和调理 |
| 50-60 | 需重点关注 | 严重问题 | 建议就医 |

**保底分**: 50分（最低不会低于此值）

---

## 实施方案：温和扣减版 v6

### 核心思路

1. 降低所有扣减分值约50%
2. 保底分从30分提高到50分
3. 支持从配置文件读取扣减/加分值

### 扣减规则 (score_rules.json)

```json
{
  "deductions": [
    { "rule_id": "single_meridian_mild_abnormal", "score": -1.0, "note": "轻度异常单经络扣1分" },
    { "rule_id": "single_meridian_obvious_abnormal", "score": -2.0, "note": "明显异常单经络扣2分" },
    { "rule_id": "single_meridian_cross", "score": -2.0, "note": "交叉异常单经络扣2分" },
    { "rule_id": "kidney_bladder_double_cross", "score": -3, "note": "肾膀胱双交叉扣3分" },
    { "rule_id": "multi_cross", "score": -3, "note": "3个以上交叉扣3分" },
    { "rule_id": "right_bias", "score": -4, "note": "右偏扣4分" },
    { "rule_id": "left_bias", "score": -4, "note": "左偏扣4分" },
    { "rule_id": "heart_supply_hit", "score": -4, "note": "心脑供血风险扣4分" },
    { "rule_id": "head_supply_hit", "score": -4, "note": "头部供血风险扣4分" },
    { "rule_id": "neck_waist_reproductive_hit", "score": -3, "note": "颈腰生殖风险扣3分" },
    { "rule_id": "mass_risk_hit", "score": -4, "note": "肿块风险扣4分" },
    { "rule_id": "multi_imbalance", "score": -4, "note": "4个以上经络失衡扣4分" }
  ]
}
```

### 加分规则

```json
{
  "bonuses": [
    { "rule_id": "multiple_meridians_improved", "score": 4, "note": "3个以上经络改善加4分" },
    { "rule_id": "partial_improvement", "score": 2, "note": "部分改善加2分" },
    { "rule_id": "overall_stable", "score": 3, "note": "整体平稳加3分" }
  ]
}
```

---

## 测试场景分布

| 场景 | 分数 | 等级 | 分类 |
|------|------|------|------|
| 全部正常 | 100.0 | 整体状态较好 | 优秀 |
| 1个轻度异常 | 100.0 | 整体状态较好 | 优秀 |
| 3个轻度异常 | 98.0 | 整体状态较好 | 优秀 |
| 2个中度异常 | 100.0 | 整体状态较好 | 优秀 |
| 肾交叉 | 100.0 | 整体状态较好 | 优秀 |
| 心脑供血风险 | 80.0 | 轻度失衡 | 亚健康 |
| 肿块风险 | 98.0 | 整体状态较好 | 优秀 |
| 6个交叉 | 67.0 | 中度失衡 | 需注意 |
| 左低 | 77.0 | 轻度失衡 | 亚健康 |
| 多失衡 | 77.0 | 轻度失衡 | 亚健康 |
| 严重失衡 | 77.0 | 轻度失衡 | 亚健康 |

**分布统计**: 优秀6个，亚健康4个，需注意1个，严重0个

---

## 代码修改

### 1. score_rules.json

- 更新 `deductions` 数组，使用新的扣减分值
- 更新 `bonuses` 数组（保持不变）
- `min_score` 从30改为50

### 2. infer.py

新增两个辅助函数：

```python
def _get_deduction(score_rules: dict, rule_id: str, default: float) -> float:
    """从 score_rules 获取扣减分值，如果不存在则使用默认值。"""
    for d in score_rules.get("deductions", []):
        if d.get("rule_id") == rule_id:
            return d.get("score", default)
    return default

def _get_bonus(score_rules: dict, rule_id: str, default: float) -> float:
    """从 score_rules 获取加分值，如果不存在则使用默认值。"""
    for b in score_rules.get("bonuses", []):
        if b.get("rule_id") == rule_id:
            return b.get("score", default)
    return default
```

修改 `calculate_raw_score()` 和 `apply_improvement_bonus()` 函数，使用配置值而非硬编码。

---

## 向后兼容性

- 如果 `score_rules.json` 中缺少某个规则，使用默认值（原硬编码值）
- 所有现有测试用例继续通过
- 可平滑升级，无需数据迁移

---

## 回滚方案

如需回滚到旧评分：

```bash
# 恢复旧配置
git checkout HEAD~1 -- rules/score_rules.json

# 重启服务
docker-compose restart
```

---

## 后续微调

如需调整某个场景的分数，只需修改 `score_rules.json` 中对应规则的 `score` 值：

```bash
# 示例：让交叉问题扣分更重
# 修改前:
{ "rule_id": "single_meridian_cross", "score": -2.0 }

# 修改后:
{ "rule_id": "single_meridian_cross", "score": -3.0 }
```

无需修改代码，重启服务即可生效。

---

## 相关文件

- `rules/score_rules.json` - 评分规则配置
- `scripts/infer.py` - 推理引擎（支持配置化评分）
- `fixtures/v2/` - 测试场景（新增7个场景）
- `scripts/test_infer.py` - 测试套件（35个测试用例）
