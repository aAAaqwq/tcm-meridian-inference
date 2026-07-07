# TCM v3 Agent 模式测试规范

## 文档说明

本文档记录 TCM v3 推理引擎在 **Agent 模式**（规则引擎 + DeepSeek LLM）下的测试用例和实际输出。

**Agent 模式特点**：
- 规则引擎提供确定性计算（分数、问题指数、经络分析等）
- LLM 生成自然语言内容（storefront、summary、recommendations）

**与 Rule-only 模式的区别**：
| 特性 | Rule-only | Agent/Hybrid |
|------|-----------|--------------|
| 环境变量 | `TCM_INFER_MODE=rule` | `TCM_INFER_MODE=agent` 或 `auto` |
| 需要 API Key | 否 | 是（`DEEPSEEK_API_KEY`） |
| 输出字段 | 规则引擎字段 | 规则引擎字段 + LLM 生成字段 |
| LLM 字段 | 无 | storefront, summary, recommendations |

---

## 实际输出文件位置

```
docs/v3/testing/agent-results/
├── summary.json                    # 所有测试用例摘要
├── comparison-report.md            # 对比报告
├── case_01_first_test-agent.json   # 完整输出（34个文件）
├── case_02_retest-agent.json
└── ...
```

**生成时间**: 2026-05-05  
**后端版本**: v3.0 (Agent 模式)  
**LLM 模型**: deepseek-v4-flash

---

## 测试用例 1：PRD 首测示例

**输入文件**: `fixtures/v3/case_01_first_test.json`

### 规则引擎输出

```yaml
score: 77
score_raw: 77.08
problem_index: 24.9

problem_index_detail:
  A_low_temperature: 5.0
  B_temp_difference: 8.5
  C_side_bias: 5.0
  D_trend: 3.9
  E_combo: 2.5

side_bias_summary:
  left_low_count: 5
  right_low_count: 0
  result: "head_blood_supply_attention"

cervical_lumbar_result: "lumbar"

focus_issues:
  - priority: 1, title: "膀胱经问题较突出"
  - priority: 2, title: "脾经问题较突出"
  - priority: 3, title: "头部供血需关注"
  - priority: 4, title: "腰椎相关问题需关注"
```

### LLM 生成字段（Agent 模式特有）

```yaml
storefront:
  focusHeadline: "膀胱经与脾经需重点关注"
  clientExplanation: "本次检测基于足部经络温度分析，不等同于医疗诊断。您的综合健康分77分，提示身体存在一些需要关注的失衡点。"
  talkTrack:
    - "您的膀胱经和脾经温度差异较大，可能与肩颈腰部和消化代谢有关。"
    - "同时整体经络偏左侧较低，提示头部供血方面需要留意。"
    - "结合肾经与膀胱经的趋势，腰椎区域也需要关注，建议配合调理改善。"
  retestPrompt: "建议经过一段时间的调理后复测，观察改善情况。"

summary: "本次检测显示综合健康分为77分，属于中度失衡状态。主要问题集中在膀胱经、脾经和肾经，其中膀胱经和脾经温差显著，且整体经络偏左明显，提示头部供血和腰椎方向需重点关注。建议持续调理，改善亚健康状态。"

recommendations:
  - "注意腰部保暖，避免久坐，可适当进行腰椎伸展运动。"
  - "饮食上减少生冷油腻，增加薏米、山药等健脾祛湿食材。"
  - "保持规律作息，避免熬夜，多饮水，可食用枸杞、黑芝麻等补肾滋阴食物。"
```

---

## 测试用例 2：PRD 复测示例

**输入文件**: `fixtures/v3/case_02_retest.json`

### 规则引擎输出

```yaml
score: 89
score_raw: 89.42
problem_index: 14.7

retest_detail:
  usage_days: 14
  usage_bonus: 3.0
  improvement_bonus: 3.0
  delta_I: 10.2
  previous_score: 77
  previous_problem_index: 24.9
  current_problem_index: 14.7
```

### LLM 生成字段（Agent 模式特有）

```yaml
storefront:
  focusHeadline: "膀胱与肝经需关注，建议复测观察进展"
  clientExplanation: "本次复测显示综合健康分89分，相比上次77分有明显改善。膀胱和肝经仍需要持续关注，建议您继续调理。"
  talkTrack:
    - "复测结果显示整体改善明显，14天内健康分提升了12分。"
    - "膀胱经和肝经仍有改善空间，建议继续针对性调理。"
    - "坚持目前的调理方案，预计下次复测会有更好表现。"
  retestPrompt: "建议继续使用仪器调理，2-4周后再次复测。"

summary: "本次复测综合健康分89分，相比上次77分提升12分，改善显著。膀胱经和肝经仍是关注重点，但整体趋势向好。建议持续调理，争取达到更优状态。"

recommendations:
  - "继续保持规律作息，巩固目前的改善成果。"
  - "针对膀胱经，可多进行腰部保健运动。"
  - "肝经调理建议保持心情舒畅，适量运动。"
```

---

## 测试用例 3：健康优秀

**输入文件**: `fixtures/v3/test_01_excellent_score.json`

### 规则引擎输出

```yaml
score: 89
score_raw: 90.0
problem_index: 0.0

problem_index_detail:
  A_low_temperature: 0.0
  B_temp_difference: 0.0
  C_side_bias: 0.0
  D_trend: 0.0
  E_combo: 0.0
```

### LLM 生成字段（Agent 模式特有）

```yaml
storefront:
  focusHeadline: "整体平衡，胃经略低可留意"
  clientExplanation: "恭喜！您的综合健康分89分，整体状态良好。仅胃经有轻微偏低，可在日常生活中稍加留意。"
  talkTrack:
    - "整体经络平衡度很好，说明您的身体状况不错。"
    - "胃经略有偏低，建议注意饮食规律，避免过饥过饱。"
    - "当前状态适合继续保持，建议定期复测观察。"
  retestPrompt: "建议1-2个月后复测，保持当前良好状态。"

summary: "本次检测综合健康分89分，整体状态良好。六条经络基本平衡，仅胃经有轻微偏低。建议保持良好的生活习惯，定期复测即可。"

recommendations:
  - "保持规律饮食，定时定量，避免暴饮暴食。"
  - "继续保持良好的作息习惯，适当运动。"
  - "定期复测，监测身体状态变化。"
```

---

## LLM 输出字段详细说明

### storefront（门店展示内容）

用于门店前台向客户展示检测结果。

| 子字段 | 说明 | 示例 |
|--------|------|------|
| `focusHeadline` | 一句话总结关注重点 | "膀胱经与脾经需重点关注" |
| `clientExplanation` | 向客户解释检测结果，必须包含免责声明 | "本次检测基于足部经络温度分析，不等同于医疗诊断..." |
| `talkTrack` | 3条对话要点，用于店员与客户沟通 | [...] |
| `retestPrompt` | 复测建议 | "建议经过一段时间的调理后复测..." |

### summary / reportSummary（报告摘要）

完整的报告摘要，描述整体健康状况和建议。

### recommendations（养生建议）

3-5条具体的养生建议，针对检测结果给出可操作的改善方案。

---

## 测试验证要点

### 1. 规则引擎字段一致性

Agent 模式的规则引擎输出应与 Rule-only 模式**完全一致**：
- score
- score_raw
- problem_index
- problem_index_detail (A/B/C/D/E)
- meridian_analysis
- side_bias_summary
- cervical_lumbar_result
- focus_issues

### 2. LLM 字段完整性

每个测试用例都应包含：
- [ ] storefront（包含4个子字段）
- [ ] summary 或 reportSummary
- [ ] recommendations（3-5条）

### 3. 安全与合规检查

- [ ] clientExplanation 包含免责声明
- [ ] 无过度医疗化表述（"预警"、"严重"、"危险"等）
- [ ] 性别过滤正确（根据 gender 字段）

---

## 附录：运行测试

### 记录 Agent 模式输出

```bash
# 确保配置了 DeepSeek API Key
export DEEPSEEK_API_KEY=sk-...

# 进入测试目录并运行 Agent 模式测试记录
cd tests && python3 record_agent_outputs.py
```

### 对比 Rule-only 和 Agent 模式

```bash
# Rule-only 模式
cd tests && python3 record_actual_outputs.py

# Agent 模式
cd tests && python3 record_agent_outputs.py
```

---

*文档版本: v1.0*  
*最后更新: 2026-05-05*
