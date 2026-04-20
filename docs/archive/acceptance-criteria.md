# 验收标准 — TCM Meridian Inference Agent v2.1

## 概述
1 个 OpenClaw Agent，输入温度数据，输出健康评分 + 经络状态 + 调理建议。

## 验收条件

### 1. [c1] 项目结构就绪
- **验证方法**: `file_exists`
- **验证目标**: `~/clawd/projects/tcm-meridian-inference-mvp/scripts/infer.py`
- **负责 Agent**: code
- **依赖**: 无
- **输出物**: `scripts/infer.py`, `rules/meridian_rules.json`, `rules/combination_rules.json`, `rules/thresholds.json`
- **通过标准**: 文件存在且非空，`python3 scripts/infer.py --help` 可执行

### 2. [c2] 规则库 JSON 完成（从 Excel 提取）
- **验证方法**: `file_contains`
- **验证目标**: `rules/meridian_rules.json` 包含 liver/spleen/kidney/stomach/gallbladder/bladder 六经各自 left_low/right_low/cross 规则
- **负责 Agent**: code
- **依赖**: 无
- **输出物**: `rules/meridian_rules.json`, `rules/combination_rules.json`, `rules/thresholds.json`
- **通过标准**: 每经至少 3 条规则（左低/右低/交叉），组合规则至少 5 条（肝+胆→转氨酶、肾+膀胱→颈椎/腰椎、4条偏侧→心脏/头部供血等）

### 3. [c3] 推理脚本核心逻辑完成
- **验证方法**: `exec`
- **验证目标**: `cd ~/clawd/projects/tcm-meridian-inference-mvp && python3 scripts/infer.py fixtures/case_left_low.json`
- **负责 Agent**: code
- **依赖**: c1, c2
- **输出物**: 推理脚本输出符合输出规范的 JSON
- **通过标准**: 输出 JSON 包含 healthScore, meridians, combinations, summary, storefront 字段；左低 case 的 liver.status 为 "left_low"

### 4. [c4] 单经推理正确性（AC-2 核心）
- **验证方法**: `exec`
- **验证目标**: `python3 scripts/test_infer.py`
- **负责 Agent**: code
- **依赖**: c3
- **输出物**: 测试脚本执行全部通过
- **通过标准**: 
  - 肝左低 → symptoms 含 "代谢" 或 "气虚"
  - 肝右低 → symptoms 含 "血虚" 或 "心脏供血"
  - 肾左低 → symptoms 含 "尿酸" 或 "耳鸣"
  - 胆左低 → symptoms 含 "胆红素" 或 "偏头痛"
  - 膀胱交叉 → 相关症状正确

### 5. [c5] 组合判症正确性（AC-3）
- **验证方法**: `exec`
- **验证目标**: `python3 scripts/test_infer.py` 中组合规则测试
- **负责 Agent**: code
- **依赖**: c3
- **输出物**: 测试通过
- **通过标准**:
  - 肝左低+胆左低 → combinations 含 "转氨酶"
  - 肾+膀胱相反低 → combinations 含 "颈椎"
  - 肾+膀胱同向低 → combinations 含 "腰椎"
  - 4条以上偏右低 → combinations 含 "心脏供血"

### 6. [c6] 5 个 Demo Case 全过（AC-6）
- **验证方法**: `exec`
- **验证目标**: `cd ~/clawd/projects/tcm-meridian-inference-mvp && for f in fixtures/case_*.json; do python3 scripts/infer.py "$f" > /dev/null 2>&1 && echo "✅ $f" || echo "❌ $f"; done`
- **负责 Agent**: code
- **依赖**: c3
- **输出物**: 5 个 demo case JSON 输出
- **通过标准**: 所有 case 输出合法 JSON，含完整字段（healthScore, meridians, summary, storefront.talkTrack）；左低/右低/交叉/多失衡/平稳 各场景 focusHeadline 正确

### 7. [c7] 门店讲解层可用（AC-4）
- **验证方法**: `file_contains`
- **验证目标**: 推理输出 JSON 的 storefront 字段
- **负责 Agent**: code
- **依赖**: c3
- **输出物**: 推理脚本输出的 storefront 层
- **通过标准**:
  - `storefront.clientExplanation` 含"不等同"或"非诊断"
  - `storefront.talkTrack` 为数组，长度 3
  - 平稳 case 不含"预警""严重"等制造紧张的词

### 8. [c8] Agent 注册到 OpenClaw
- **验证方法**: `file_exists`
- **验证目标**: `~/.openclaw/agents/tcm-meridian/agent.json`
- **负责 Agent**: ops
- **依赖**: c3
- **输出物**: Agent 配置文件
- **通过标准**: agent.json 存在且配置了模型和 skill 路径

### 9. [c9] Demo Case 文件重写（新格式）
- **验证方法**: `file_exists`
- **验证目标**: `~/clawd/projects/tcm-meridian-inference-mvp/fixtures/case_left_low.json` 等 5 个新格式 case
- **负责 Agent**: code
- **依赖**: 无（可与 c2 并行）
- **输出物**: 5 个新格式 demo case JSON（left/right 数值格式，不再用 t1/t2）
- **通过标准**: 每个文件含 subject + measurements（6经络，每经 left/right 数值）

### 10. [c10] Git Push + README
- **验证方法**: `exec`
- **验证目标**: `cd ~/clawd/projects/tcm-meridian-inference-mvp && git log --oneline -1`
- **负责 Agent**: code
- **依赖**: c3, c6
- **输出物**: 更新后的 GitHub 仓库
- **通过标准**: 最新 commit 包含推理脚本和规则库，README 反映当前架构
