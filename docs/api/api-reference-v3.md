# TCM Meridian Inference API v3.0

面向：前端 / 调用方 / 集成开发  
项目：`tcm-meridian-inference-mvp`  
当前版本：`3.0`  
更新日期：2026-05-07

---

## 1. 架构概述

```
用户 POST JSON
    ↓
tcm_api.py (HTTP Server)
    ↓ TCM_INFER_MODE
    ├─ rule  → infer_v3.py v3 规则引擎（确定性，无需 API Key）
    ├─ agent → infer_agent.py 混合推理（规则引擎 + DeepSeek 自然语言）
    └─ auto  → 有 LLM API Key 时用 agent，否则 fallback 到 rule
```

**核心原则：** 硬逻辑（分数、问题指数、趋势、组合判症）始终由规则引擎决定，LLM 只负责生成可读的自然语言文案。LLM 失败时自动 fallback 到 rule 模式。

> 重要边界：本服务是**规则驱动 + LLM 辅助**的推理服务，不是训练型医学诊断模型，输出不应被表述为临床诊断结论。

---

## 2. 端点一览

| Method | Path | 说明 |
|--------|------|------|
| `GET` | `/` | 服务信息（版本、推理模式、端点列表） |
| `GET` | `/health` | 健康检查（legacy） |
| `GET` | `/healthz` | 健康检查 |
| `POST` | `/test` | 使用内置样例数据运行推理 |
| `POST` | `/api/inference/meridian-diagnosis` | **主推理接口** |

---

## 3. 测试指南

### 统一测试脚本

```bash
# 本地测试（推荐）
python3 tests/run_v3_tests.py                    # 自动模式(有KEY用hybrid)
python3 tests/run_v3_tests.py --mode rule        # 纯规则引擎
python3 tests/run_v3_tests.py --mode agent       # Hybrid模式(需DEEPSEEK_API_KEY)

# 线上API测试
python3 tests/run_v3_tests.py --url http://180.76.137.183:18970/api/inference/meridian-diagnosis
python3 tests/run_v3_tests.py --port 18970      # 指定端口

# 顺序执行（便于调试）
python3 tests/run_v3_tests.py --sequential
```

**测试用例**: 38个测试用例位于 `fixtures/v3/` 目录，测试结果记录在 `docs/v3/testing/actual-results/`

---

## 4. 完整请求/响应示例

### 4.1 测试用例索引

| 测试场景 | 测试文件 | 说明 |
|----------|----------|------|
| 首测-健康优秀 | `test_01_excellent_score.json` | 全部平衡，分数89 |
| 首测-轻度失衡 | `test_02_mild_imbalance.json` | 肝经/脾经轻微异常 |
| 首测-中度失衡 | `test_03_moderate_imbalance.json` | 6条经络左低 |
| 复测-改善 | `case_02_retest.json` | 分数从77提升到89 |
| 趋势-stable_left_low | `test_05_trend_stable_left_low.json` | 肾+膀胱左低=腰椎 |
| 趋势-cross | `test_07_trend_cross.json` | 交叉=颈椎+腰椎 |
| 偏侧-4条左低 | `test_11_side_bias_4.json` | C=3.5 |
| 复测-30天+ | `test_24_retest_30_plus_days.json` | usage_bonus=4 |

完整测试用例请参见 [api-test-cases.md](api-test-cases.md)（全部34个用例完整请求/响应）。

---

### 4.2 首次检测请求体

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

### 4.3 复测请求体（额外字段）

```json
{
  "measurement_type": "retest",
  "gender": "female",
  "previous_score": 77,
  "previous_problem_index": 24.9,
  "usage_days_between_tests": 14,
  "meridians": {
    "stomach": { "group1_left": 40.0, "group1_right": 40.5, "group2_left": 42.5, "group2_right": 42.6 },
    "gallbladder": { "group1_left": 37.0, "group1_right": 37.0, "group2_left": 42.2, "group2_right": 42.2 },
    "bladder": { "group1_left": 37.0, "group1_right": 37.2, "group2_left": 40.0, "group2_right": 41.0 },
    "liver": { "group1_left": 37.0, "group1_right": 36.8, "group2_left": 40.0, "group2_right": 40.2 },
    "spleen": { "group1_left": 37.0, "group1_right": 36.8, "group2_left": 40.0, "group2_right": 40.8 },
    "kidney": { "group1_left": 37.0, "group1_right": 37.0, "group2_left": 41.0, "group2_right": 41.5 }
  }
}
```

### 4.4 字段说明

#### 顶层字段

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `measurement_type` | **是** | string | `"first_test"` 或 `"retest"` |
| `gender` | **是** | string | `"male"` / `"female"` / `"unknown"` |
| `meridians` | **是** | object | 6条经络测量数据 |
| `previous_score` | 复测时 | number | 上次展示给用户的综合评分 |
| `previous_problem_index` | 复测时 | number | 上次问题指数 |
| `usage_days_between_tests` | 复测时 | int | 两次测量间使用仪器天数（0~365） |

#### meridians 结构

必须包含 6 条经络：`stomach`、`gallbladder`、`bladder`、`liver`、`spleen`、`kidney`

每条经络：

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `group1_left` | **是** | number | 第一组（5分钟）左侧温度值（°C） |
| `group1_right` | **是** | number | 第一组（5分钟）右侧温度值（°C） |
| `group2_left` | **是** | number | 第二组（20分钟）左侧温度值（°C） |
| `group2_right` | **是** | number | 第二组（20分钟）右侧温度值（°C） |

---

## 5. 响应规范

### 5.1 核心输出结构

```json
{
  "engine": {
    "mode": "hybrid",
    "version": "3.0",
    "llmModel": "deepseek-v4-flash",
    "llmLatency": 8.83
  },

  "score_result": {
    "score": 89,
    "score_raw": 90.0,
    "problem_index": 0.0,
    "problem_index_detail": {
      "low_temperature_index": 0.0,
      "temperature_difference_index": 0.0,
      "side_bias_index": 0.0,
      "trend_index": 0.0,
      "combo_index": 0.0
    }
  },

  "lowest_points": {
    "selected": [
      {
        "meridian": "stomach",
        "side": "left",
        "value": 40.0,
        "rank": 1,
        "must_report": true
      }
    ],
    "tie_candidates": []
  },

  "side_bias_summary": {
    "left_low_count": 0,
    "right_low_count": 0,
    "balanced_count": 6,
    "result": "none"
  },

  "cervical_lumbar_result": {
    "result": "none",
    "kidney_trend": "stable_balanced",
    "bladder_trend": "stable_balanced"
  },

  "meridian_analysis": [
    {
      "meridian": "stomach",
      "meridian_name": "胃经",
      "group1_status": "balanced",
      "group2_status": "balanced",
      "trend": "stable_balanced",
      "group1_diff": 0.0,
      "group2_diff": 0.0,
      "group1_diff_level": "balanced",
      "group2_diff_level": "balanced",
      "diff_change": "unchanged",
      "matched_rules": [],
      "is_focus": true,
      "focus_reason": ["second_group_lowest_point"],
      "narrative": "胃经是本次重点关注经络，两组测量均左右平衡..."
    }
  ],

  "focus_issues": [
    {
      "priority": 1,
      "type": "lowest_point",
      "meridian": "stomach",
      "meridian_name": "胃经",
      "side": "left",
      "title": "胃经问题较突出",
      "reason_codes": ["second_group_lowest_point"]
    }
  ],

  "gender": "female",
  "measurement_type": "first_test",

  "summary": "您的经络检测结果显示整体健康状态良好...",
  "reportSummary": "您的经络检测结果显示整体健康状态良好...",
  "storefront": {
    "focusHeadline": "胃经需关注，整体状态佳",
    "clientExplanation": "本次检测结果整体良好...",
    "talkTrack": ["...", "...", "..."],
    "retestPrompt": "建议一个月后进行复测..."
  },
  "recommendations": ["...", "...", "..."],
  "meridianNarrative": {
    "stomach": "...",
    "gallbladder": "...",
    "bladder": "...",
    "liver": "...",
    "spleen": "...",
    "kidney": "..."
  }
}
```

### 5.2 复测额外字段

```json
{
  "retest_detail": {
    "usage_days": 14,
    "usage_bonus": 3.0,
    "delta_I": 10.2,
    "improvement_bonus": 3.0,
    "retest_score_base": 89.42,
    "protected_score": 89.42,
    "previous_score": 77,
    "previous_problem_index": 24.9,
    "current_problem_index": 14.7
  }
}
```

---

## 6. 关键字段说明

### 6.1 engine

| 字段 | 类型 | 说明 |
|------|------|------|
| `mode` | string | `hybrid` / `rule-based-v3` / `rule-fallback` |
| `version` | string | 引擎版本 |
| `llmModel` | string | LLM模型 (hybrid模式) |
| `llmLatency` | float | LLM调用耗时秒数 (hybrid模式) |

### 6.2 score_result

| 字段 | 类型 | 说明 |
|------|------|------|
| `score` | int | 展示分数（首测65-89，复测65-95） |
| `score_raw` | float | 原始计算分数 |
| `problem_index` | float | 问题指数 I = A+B+C+D+E |
| `problem_index_detail` | object | 各分量详情 |

### 6.2 problem_index_detail

| 字段 | 说明 | 最大值 |
|------|------|--------|
| `low_temperature_index` | A: 低温指数 | 6 |
| `temperature_difference_index` | B: 温差指数 | 12 (封顶) |
| `side_bias_index` | C: 偏侧指数 | 6 |
| `trend_index` | D: 趋势指数 | 4 (封顶) |
| `combo_index` | E: 组合指数 | 2.5 |

### 6.4 lowest_points

第二组（20分钟）温度最低的两个点，报告必讲项。

### 6.5 side_bias_summary

| 字段 | 说明 |
|------|------|
| `left_low_count` | 第二组左低经络数 |
| `right_low_count` | 第二组右低经络数 |
| `result` | `head_blood_supply_attention` / `heart_attention` / `none` |

### 6.6 cervical_lumbar_result

| result值 | 说明 |
|----------|------|
| `none` | 无颈椎/腰椎问题 |
| `cervical` | 颈椎问题 |
| `lumbar` | 腰椎问题 |
| `cervical_and_lumbar` | 颈椎和腰椎同时存在 |

### 6.7 meridian_analysis

每条经络的详细分析：

| 字段 | 说明 |
|------|------|
| `meridian` | 经络英文名: `stomach`/`gallbladder`/`bladder`/`liver`/`spleen`/`kidney` |
| `meridian_name` | 经络中文名 |
| `group1_status` | 第一组状态: `balanced`/`left_low`/`right_low` |
| `group2_status` | 第二组状态: `balanced`/`left_low`/`right_low` |
| `trend` | 趋势类型: `stable_left_low`/`stable_right_low`/`cross`/`stable_balanced`/`potential_symptom`/`fast_response` |
| `group1_diff` | 第一组温差绝对值 |
| `group2_diff` | 第二组温差绝对值 |
| `group1_diff_level` | 第一组温差等级: `balanced`/`mild_sub_health`/`health_problem`/`serious_problem` |
| `group2_diff_level` | 第二组温差等级: `balanced`/`mild_sub_health`/`health_problem`/`serious_problem` |
| `diff_change` | 温差变化: `improved`/`worsened`/`unchanged` |
| `matched_rules` | 匹配到的问题规则列表 |
| `is_focus` | 是否属于重点关注经络 |
| `focus_reason` | 重点关注原因列表 |
| `narrative` | LLM生成的自然语言描述（Hybrid模式）|

### 6.8 自然语言输出字段 (Hybrid模式)

| 字段 | 类型 | 说明 |
|------|------|------|
| `summary` | string | 综合健康解读文案 |
| `reportSummary` | string | 报告摘要（与summary相同） |
| `storefront` | object | 门店展示话术对象 |
| `storefront.focusHeadline` | string | 关注标题，一句话总结 |
| `storefront.clientExplanation` | string | 向客户解释检测结果 |
| `storefront.talkTrack` | array[string] | 对话要点（3条） |
| `storefront.retestPrompt` | string | 复测建议提示 |
| `recommendations` | array[string] | 调理建议列表（3-5条） |
| `meridianNarrative` | object | 各经络自然语言描述 {meridian: narrative} |

### 6.9 复测额外字段 (retest_detail)

仅当 `measurement_type` 为 `retest` 时返回：

| 字段 | 类型 | 说明 |
|------|------|------|
| `retest_detail.usage_days` | int | 两次测试间使用仪器天数 |
| `retest_detail.usage_bonus` | float | 使用天数加分（0-4分） |
| `retest_detail.delta_I` | float | 问题指数变化量（上次-本次） |
| `retest_detail.improvement_bonus` | float | 改善奖励分（如适用） |
| `retest_detail.retest_score_base` | float | 复测基础分数（加分前） |
| `retest_detail.protected_score` | float | 保护后的分数（不低于上次） |
| `retest_detail.previous_score` | int | 上次展示分数 |
| `retest_detail.previous_problem_index` | float | 上次问题指数 |
| `retest_detail.current_problem_index` | float | 本次问题指数 |

---

## 7. 评分算法摘要

### 7.1 问题指数计算

```
I = A + B + C + D + E

A (低温指数):
  低温差距 <= 0.5℃:     0
  0.5 < 差距 <= 1℃:      1
  1 < 差距 <= 2℃:        3
  2 < 差距 <= 3℃:        5
  差距 > 3℃:             6

B (温差指数):
  单经基础指数 + 修正值
  B = min(总和, 12)

C (偏侧指数):
  max_count < 4:  0
  max_count = 4:  3.5
  max_count = 5:  5
  max_count = 6:  6

D (趋势指数):
  stable_balanced: 0, potential_symptom: 0.3, fast_response: 0.3
  stable_left/right_low: 0.5, cross: 1.2
  D = min(总和, 4)

E (组合指数):
  无颈椎/腰椎: 0
  有颈椎或腰椎: 2.5 (不叠加)
```

### 7.2 分数映射

```
if I <= 10:      score_raw = 90 - 0.4 * I
elif I <= 22:    score_raw = 86 - 0.55 * (I - 10)
elif I <= 32:    score_raw = 79.4 - 0.8 * (I - 22)
else:            score_raw = 71.4 - 1.0 * (I - 32)

首测: clamp(score_raw, 65, 89)
复测: clamp(score_raw + usage_bonus + improvement_bonus, 65, 95)
```

### 7.3 分数等级

| 分数 | 等级 | 说明 |
|------|------|------|
| 90-100 | 健康优秀 | 状态较好 |
| 80-89 | 轻度失衡 | 常见亚健康 |
| 70-79 | 中度失衡 | 需要重点关注和调理 |
| 65-69 | 明显失衡 | 建议持续调理并复测 |

---

## 8. 调用示例

### 8.1 CLI 直接运行

```bash
# 使用 v3 推理引擎
python3 scripts/infer_v3.py fixtures/v3/case_01_first_test.json --pretty

# 运行全部测试
python3 run_tests_v3.py

# 后端验证
python3 validate_backend.py
```

### 8.2 HTTP 调用

```bash
curl -X POST http://127.0.0.1:18790/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  --data @fixtures/v3/case_01_first_test.json
```

### 8.3 健康检查

```bash
curl http://127.0.0.1:18790/healthz
```

---

## 9. 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `TCM_API_PORT` | `18790` | 服务端口 |
| `TCM_INFER_MODE` | `auto` | 推理模式：`rule` / `agent` / `auto` |
| `DEEPSEEK_API_KEY` | （空） | LLM API 密钥，hybrid 模式必需 |

---

## 10. Agent 模式输出（LLM 增强）

当 `TCM_INFER_MODE=agent` 或 `auto`（且配置了 `DEEPSEEK_API_KEY`）时，响应会包含 LLM 生成的自然语言字段：

### 10.1 完整响应示例（Agent 模式）

```json
{
  "engine": {
    "mode": "agent-hybrid-v3",
    "version": "3.0"
  },

  "score_result": { ... },
  "lowest_points": { ... },
  "side_bias_summary": { ... },
  "cervical_lumbar_result": { ... },
  "meridian_analysis": [ ... ],
  "focus_issues": [ ... ],

  "storefront": {
    "focusHeadline": "膀胱经与脾经需重点关注",
    "clientExplanation": "本次检测基于足部经络温度分析，不等同于医疗诊断。您的综合健康分77分，提示身体存在一些需要关注的失衡点。",
    "talkTrack": [
      "您的膀胱经和脾经温度差异较大，可能与肩颈腰部和消化代谢有关。",
      "同时整体经络偏左侧较低，提示头部供血方面需要留意。",
      "结合肾经与膀胱经的趋势，腰椎区域也需要关注，建议配合调理改善。"
    ],
    "retestPrompt": "建议经过一段时间的调理后复测，观察改善情况。"
  },

  "summary": "本次检测显示综合健康分为77分，属于中度失衡状态...",
  "reportSummary": "本次检测显示综合健康分为77分，属于中度失衡状态...",

  "recommendations": [
    "注意腰部保暖，避免久坐，可适当进行腰椎伸展运动。",
    "饮食上减少生冷油腻，增加薏米、山药等健脾祛湿食材。",
    "保持规律作息，避免熬夜，多饮水，可食用枸杞、黑芝麻等补肾滋阴食物。"
  ]
}
```

### 10.2 LLM 生成字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `storefront` | object | 门店展示内容，用于前台展示 |
| `storefront.focusHeadline` | string | 关注标题，一句话总结 |
| `storefront.clientExplanation` | string | 向客户解释检测结果 |
| `storefront.talkTrack` | string[] | 对话要点，3条 |
| `storefront.retestPrompt` | string | 复测建议提示 |
| `summary` | string | 报告摘要（简短版） |
| `reportSummary` | string | 报告摘要（完整版） |
| `recommendations` | string[] | 养生建议列表（3-5条） |

### 10.3 Rule-only vs Agent 模式对比

| 模式 | 环境变量 | 输出字段 |
|------|----------|----------|
| Rule-only | `TCM_INFER_MODE=rule` | 规则引擎字段（score_result, meridian_analysis 等） |
| Agent/Hybrid | `TCM_INFER_MODE=agent` 或 `auto` + `DEEPSEEK_API_KEY` | 规则引擎字段 + LLM 生成字段（storefront, summary, recommendations） |

---

## 11. 错误响应

| HTTP 状态码 | 场景 | 响应示例 |
|-------------|------|----------|
| 400 | 请求体 JSON 解析失败 | `{"error": "invalid JSON: ..."}` |
| 400 | measurement_type 错误 | `measurement_type must be 'first_test' or 'retest'` |
| 400 | 复测缺少 required 字段 | `previous_score required for retest` |
| 404 | 路由不存在 | `{"error": "not found"}` |
| 500 | 服务器内部错误 | `{"error": "..."}` |

---

## 12. v2 vs v3 变更对照

| 项目 | v2 | v3 |
|------|----|----|
| 输入格式 | `measurements.before/after` | `measurement_type` + `meridians.group1/2` |
| 评分逻辑 | 100分扣分制 | 问题指数映射制 |
| 核心输出 | `healthScore`, `meridianDetails` | `score_result`, `meridian_analysis` |
| 问题指数 | 无 | `problem_index` = A+B+C+D+E |
| 最低点 | `lowestMeridianBefore/After` | `lowest_points.selected` |
| 偏侧统计 | `globalPatterns` | `side_bias_summary` |
| 颈椎/腰椎 | `combinationAnalysis` | `cervical_lumbar_result` |
| 复测保护 | `scoreAdjustedByPolicy` | `retest_detail` |

---

*文档版本: v3.1*  
*最后更新: 2026-05-05*

## 更新记录

### v3.1 (2026-05-05)
- 添加 Agent 模式输出字段说明（storefront, summary, recommendations）
- 添加 Rule-only vs Agent 模式对比
- 添加 LLM 生成字段详细说明

### v3.0 (2026-05-04)
- 初始版本
- 定义 v3 推理引擎 API 规范
