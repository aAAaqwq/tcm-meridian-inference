# TCM Meridian Inference MVP × n8n 最小原型

## 结论

**n8n 适合这个业务，前提是把它放在“编排层”而不是“核心规则引擎层”。**

原因：
- 当前项目已经有稳定规则引擎与 FastAPI：`POST /api/inference/meridian-diagnosis`
- 已有可选 LLM 增强层：`src/tcm_meridian_inference/llm_reporter.py`
- n8n 最擅长的正是：Webhook 接口、流程编排、模型路由、报告装配、后续扩展

因此推荐结构不是“把规则全重写进 n8n”，而是：

```text
Webhook -> 输入校验/归一化 -> 规则评分(API) -> 模型增强(可选) -> 报告/建议输出 -> 记录/回调
```

---

## 已验证事实

### 1. 现有项目已具备规则评分 API
- 路径：`src/tcm_meridian_inference/api.py`
- 接口：`POST /api/inference/meridian-diagnosis`
- 请求体支持：
  - `subject`
  - `measurements`
  - `context`
  - `ruleConfigPath`
  - `thresholds`
  - `useLlm`

### 2. 现有项目已具备 LLM 增强接口基础
- 路径：`src/tcm_meridian_inference/llm_reporter.py`
- 环境变量：
  - `OLLAMA_HOST`
  - `OLLAMA_MODEL`（默认 `qwen3.5:cloud`）
  - `OLLAMA_TIMEOUT`
  - `TCM_USE_LLM`

### 3. 当前业务边界清晰
- 核心规则判断：规则引擎负责
- LLM：只负责增强解释/门店话术/报告润色
- 不建议把评分/风险判定完全黑盒化

---

## 推荐最小落地结构

### 结构图

```text
[Webhook]
   -> [Set: normalize request]
   -> [IF: useLocalRules?]
       -> [HTTP Request: FastAPI /api/inference/meridian-diagnosis]
   -> [IF: useModelEnhancement?]
       -> [HTTP Request: Ollama / API model]
   -> [Code: merge final report]
   -> [Respond to Webhook]
```

### 节点职责

#### 1. Webhook
- 对外统一 API 入口
- 路径建议：`/tcm/meridian/report`
- Method：`POST`

#### 2. Set / Code（Normalize）
- 统一输入 schema
- 补默认字段：
  - `context.source = "n8n-webhook"`
  - `options.useModel = true|false`
  - `options.modelProvider = ollama|cloud`

#### 3. HTTP Request（Rule Engine）
请求到：
- `http://tcm-api:8000/api/inference/meridian-diagnosis`

建议 body：
```json
{
  "subject": {{$json.subject}},
  "measurements": {{$json.measurements}},
  "context": {{$json.context}},
  "thresholds": {{$json.thresholds || {}}},
  "ruleConfigPath": {{$json.ruleConfigPath || null}},
  "useLlm": false
}
```

#### 4. IF（是否做模型增强）
条件：
- `options.useModel === true`

#### 5A. HTTP Request（调用 Ollama / qwen3.5:cloud）
如果直接调模型：
- URL: `${OLLAMA_HOST}/api/chat`
- 输入只喂**规则层稳定输出**，不要直接喂原始脉络测量

推荐 prompt 输入：
- `scores`
- `reportSummary`
- `advice`
- `storefront.focusHeadline`
- `storefront.clientExplanation`
- `storefront.retestPrompt`

#### 5B. 或直接让现有 API 内部带 LLM
如果后端已经稳定支持 `useLlm=true`，则 n8n 也可以不单独调模型，直接：
- Rule Engine API 请求时带 `useLlm: true`

#### 6. Code（Merge Final Output）
输出统一结构：
```json
{
  "requestId": "...",
  "engine": {
    "mode": "rule-based-mvp",
    "ruleSetId": "...",
    "model": "qwen3.5:cloud"
  },
  "scores": {...},
  "riskTags": [...],
  "reportSummary": "...",
  "advice": [...],
  "storefront": {...},
  "llmReport": "...",
  "finalReport": {
    "headline": "...",
    "customerSummary": "...",
    "recommendations": [...],
    "followup": "..."
  }
}
```

#### 7. Respond to Webhook
- 统一把最终 JSON 返回给前端 / 门店系统 / 小程序

---

## 为什么这个结构“可验收、可扩展、方便修改”

### 可验收
- Webhook 是固定入口
- 规则评分来自现有已测试 API
- 输出字段稳定，可直接比对 demo case

### 可扩展
- 新指标：先扩 `measurements` 与规则文件
- 新规则：改 `knowledge/expert_rules/*.json`
- 新模型：在 n8n 切换 provider / model 节点即可

### 方便修改
- 规则与模型分层
- n8n 只编排，不承载核心医学/规则逻辑
- 报告格式变更主要在 Code/Set 节点，不必动底层引擎

---

## 最小验收建议

用 `fixtures/demo_case_01.json` 跑通：
1. Webhook 收到请求
2. 调 FastAPI 规则评分成功
3. 调 `qwen3.5:cloud` 成功（或 `useLlm=true` 成功）
4. 返回统一最终 JSON

最低通过标准：
- 有 `scores`
- 有 `reportSummary`
- 有 `advice`
- 有 `storefront`
- 有 `finalReport`
- 保留“非医疗诊断”边界表达

---

## 下一步 1-3 个动作

1. 先在 n8n 导入 `n8n/tcm-meridian-minimal-workflow.json`
2. 把 `HTTP Request` 节点 URL 改成实际 `tcm-meridian-inference-mvp` 服务地址
3. 用 `fixtures/demo_case_01.json` 跑一遍最小联调，确认最终 JSON 输出稳定
