# TCM Meridian Inference MVP — 中医经络推理 Agent

一个基于规则库的六经络推理 MVP：输入 6 条经络的左右测量值，输出健康评分、经络状态、组合判症、门店讲解层文案与调理建议。

当前仓库已完成并验证：**c3 / c4 / c5 / c6 / c7 / c9**。

---

## 1. 当前架构

```text
fixtures/*.json
  -> scripts/infer.py
      -> rules/thresholds.json
      -> rules/meridian_rules.json
      -> rules/combination_rules.json
  -> JSON result
      - healthScore
      - meridians
      - combinations
      - summary
      - storefront
      - trace
```

### 组件说明
- `scripts/infer.py`
  - 主入口
  - 读取新格式 fixture / 输入 JSON
  - 加载阈值、单经规则、组合规则
  - 输出完整 JSON
- `rules/thresholds.json`
  - 温度阈值、左右差阈值、评分参数
- `rules/meridian_rules.json`
  - 六经单经规则（left_low / right_low / cross）
- `rules/combination_rules.json`
  - 组合判症规则（转氨酶 / 颈椎 / 腰椎 / 心脏供血 / 头部供血等）
- `fixtures/`
  - 新格式 demo cases（subject + measurements）
- `scripts/test_infer.py`
  - c3/c4/c5/c6/c7 自动化验收脚本

---

## 2. 输入格式

当前采用 **新格式**：仅包含 `subject` 与 `measurements`。

### 示例

```json
{
  "subject": {
    "id": "case-left-low-001",
    "name": "左低场景"
  },
  "measurements": {
    "liver": { "left": 35.0, "right": 36.1 },
    "spleen": { "left": 35.1, "right": 35.9 },
    "kidney": { "left": 35.0, "right": 35.8 },
    "stomach": { "left": 35.1, "right": 36.0 },
    "gallbladder": { "left": 35.0, "right": 35.9 },
    "bladder": { "left": 35.2, "right": 35.9 }
  }
}
```

### 必填要求
- `subject`
- `measurements`
- 共 6 条经络：
  - `liver`
  - `spleen`
  - `kidney`
  - `stomach`
  - `gallbladder`
  - `bladder`
- 每条经络必须仅有：
  - `left`
  - `right`

---

## 3. 输出格式

### 顶层关键字段
- `healthScore`
- `meridians`
- `combinations`
- `summary`
- `storefront`

除此之外，当前实现还会输出：
- `engine`
- `subject`
- `context`
- `input`
- `scores`
- `sixDimensionScores`
- `riskTags`
- `reportSummary`
- `advice`
- `trace`

### storefront 字段
当前门店讲解层包含：
- `focusHeadline`
- `clientExplanation`
- `talkTrack`
- `retestPrompt`

其中：
- `clientExplanation` 必须包含“不等同于医疗诊断”或等效表述
- `talkTrack` 为 **恰好 3 句**
- stable case 不使用“预警”“严重”等制造紧张的词

---

## 4. 当前支持的场景（Demo Cases）

已落地并验证的 5 个 demo cases：

- `fixtures/case_left_low.json`
- `fixtures/case_right_low.json`
- `fixtures/case_cross.json`
- `fixtures/case_multi.json`
- `fixtures/case_stable.json`

### 当前 focusHeadline 设计
- `case_left_low.json` → `左侧偏低：重点关注 ...`
- `case_right_low.json` → `右侧偏低：重点关注 ...`
- `case_cross.json` → `左右交叉/不对称：重点关注 ...`
- `case_multi.json` → `多经络失衡：重点关注 ...`
- `case_stable.json` → `整体相对平稳`

这层 headline 做的是 **场景优先 + 前 2 个关键组合提示**，既保留 trace/combinations 的完整性，又让门店展示更容易验收。

---

## 5. 单经规则（c4 已验证）

当前已通过自动化断言：

- 肝左低 → symptoms 含 `代谢` 或 `气虚`
- 肝右低 → symptoms 含 `血虚` 或 `心脏供血`
- 肾左低 → symptoms 含 `尿酸` 或 `耳鸣`
- 胆左低 → symptoms 含 `胆红素` 或 `偏头痛`
- 膀胱交叉 → 保留 `cross` 标记，且症状输出正确

说明：
- 当前主状态优先级采用 **left_low / right_low 优先于 cross**
- `cross` 仍会保留在 `tags` 中，用于追踪左右不对称信息

---

## 6. 组合规则（c5 已验证）

当前已通过自动化断言：

- 肝左低 + 胆左低 → `转氨酶偏高`
- 肾 + 膀胱相反低 → `颈椎风险提示`
- 肾 + 膀胱同向低 → `腰椎风险提示`
- 4 条以上偏右低 → `心脏供血注意`

当前规则库还包含：
- 4 条以上偏左低 → `头部供血注意`
- 肾 + 膀胱 + 脾联动的加重提示等

---

## 7. 快速使用

### 单个 case 推理

```bash
cd ~/clawd/projects/tcm-meridian-inference-mvp
python3 scripts/infer.py fixtures/case_left_low.json
```

### 查看帮助

```bash
python3 scripts/infer.py --help
```

### 运行自动化验收

```bash
python3 scripts/test_infer.py
```

### 批量 smoke test

```bash
for f in fixtures/case_*.json; do
  echo "== $f =="
  python3 scripts/infer.py "$f" > /dev/null && echo OK || echo FAIL
done
```

---

## 8. 当前测试覆盖

`scripts/test_infer.py` 当前覆盖：

### c3
- 输出合法 JSON
- 顶层字段齐全
- `case_left_low` 的 `meridians.liver.status == "left_low"`

### c4
- 单经推理症状正确性

### c5
- 组合判症正确性

### c6
- 5 个 demo case 都输出合法 JSON
- `storefront.talkTrack` 存在且长度为 3
- `focusHeadline` 与场景匹配

### c7
- `clientExplanation` 包含“不等同”/“非诊断”
- stable case 文案不制造紧张感

---

## 9. 已知实现约束

- 当前为 **规则引擎 MVP**，不是临床诊断系统
- 输出中会保留较完整的 `trace` 和 `riskTags`，方便后续调试和解释
- 某些 case 可能同时命中多个组合规则，这是当前设计允许的行为
- storefront 负责“展示收敛”，不会删除底层 trace/combinations
- 已处理 `BrokenPipeError`，适配 `head/grep/python pipe` 等提前关流场景

---

## 10. 里程碑状态

- [x] c1 项目结构就绪
- [x] c2 规则库 JSON 完成
- [x] c3 推理脚本核心逻辑完成
- [x] c4 单经推理正确性
- [x] c5 组合判症正确性
- [x] c6 5 个 Demo Case 全过
- [x] c7 门店讲解层可用
- [ ] c8 Agent 注册到 OpenClaw（需按实际 agent 配置确认）
- [x] c9 Demo Case 文件重写（新格式）
- [ ] c10 Git Push + README（本次进行中）
