# 中医经络检测推理接口：20 轮迭代验收清单（严格版）

> 项目路径：`/home/aa/clawd/projects/tcm-meridian-inference-mvp`
> 
> 目的：为 code agent 提供一份**严格、可执行、可验收**的接口验收标准，目标是让调用方访问 API 后，稳定获得：
> - 专业的 **6 个角度评分**
> - 报告摘要
> - 建议
>
> 说明：本文**只基于仓库内可见证据**（README、schema、源码、测试、fixtures）整理；不把未实现内容写成“已支持”。

---

## 1. 基于证据的当前 contract 梳理

### 1.1 当前主接口
- 健康检查：`GET /healthz`
- 推理接口：`POST /api/inference/meridian-diagnosis`
- 规则加载查看：`POST /api/rules/load`

证据：
- `src/tcm_meridian_inference/api.py`

### 1.2 当前代码真实接受的输入语义
当前代码真实支持 3 种输入模式：

1. **正式主路径：脚上六经 + 显式 left/right/trendDelta**
   - 六条经络：`liver / spleen / kidney / stomach / gallbladder / bladder`
   - 每条经络字段：`left`、`right`、`trendDelta`
   - 返回 `input.mode = foot_six_explicit`

2. **兼容路径：脚上六经 + 旧 t1/t2**
   - 自动解释为：`left=t1`、`right=t2`、`trendDelta=t2-t1`
   - 返回 `input.mode = foot_six_legacy_pair`

3. **兼容路径：旧六键 payload**
   - 输入键：`lung / pericardium / heart / spleen / liver / kidney`
   - 映射为：
     - `lung -> stomach`
     - `pericardium -> gallbladder`
     - `heart -> bladder`
   - 返回 `input.mode = legacy_mapped`

证据：
- `src/tcm_meridian_inference/schemas.py`
- `tests/test_validation.py`
- `README.md`

### 1.3 当前代码真实返回的输出顶层字段
当前 `infer()` / API 响应已稳定返回：
- `subject`
- `context`
- `input`
- `engine`
- `meridianResults`
- `sixDimensionScores`
- `scores`
- `riskTags`
- `recommendations`
- `advice`（= recommendations 别名）
- `summary`
- `reportSummary`（= summary 别名）
- `storefront`
- `trace`

证据：
- `src/tcm_meridian_inference/rules.py`
- `src/tcm_meridian_inference/engine.py`
- `tests/test_scores_contract.py`
- `tests/test_api_contract_scores.py`

### 1.4 当前“sixDimensionScores”真实含义
**当前代码里的 `sixDimensionScores` 不是“6 个分析角度评分”，而是“6 条经络的分数列表”。**

当前实现是按固定顺序输出 6 条经络：
- liver
- spleen
- kidney
- stomach
- gallbladder
- bladder

每项字段为：
- `meridian`
- `label`
- `score`
- `riskScore`
- `riskLevel`
- `status`
- `sideState`
- `trend`

其中：
- `riskScore` 来源于特征层启发式规则（例如左低/右低/交叉/趋势）
- `score = 100 - riskScore`（夹在 0~100）

证据：
- `src/tcm_meridian_inference/rules.py` 中 `_build_six_dimension_scores()`
- `tests/test_scores_contract.py`

**结论：当前实现满足“6 条经络评分”，不满足“专业的 6 个角度评分”的产品表达。**

---

## 2. 本验收单采用的目标口径

为避免概念混乱，后续验收必须把两个层次分开：

### 2.1 必须保留：6 条经络结果
这是当前系统的核心解释对象，不能丢：
- 肝经 / 脾经 / 肾经 / 胃经 / 胆经 / 膀胱经

### 2.2 必须新增并正式定义：6 个分析角度评分
这是面向最终用户目标的“专业的 6 个角度评分”。

**建议新增正式字段：`analysisScores`**，不要继续借用 `sixDimensionScores` 这个名字，以免与“6 条经络评分”混淆。

---

## 3. 严格验收清单

## 3.1 输入要求

### A. 请求路径
- 必须支持 `POST /api/inference/meridian-diagnosis`
- `Content-Type` 必须为 `application/json`

### B. 必填字段
- `subject.id` 必填
- `measurements` 必填

### C. 正式主输入（验收主路径）
`measurements` 必须包含以下 6 条经络：
- `liver`
- `spleen`
- `kidney`
- `stomach`
- `gallbladder`
- `bladder`

每条经络必须至少包含：
- `left: number`
- `right: number`
- `trendDelta: number`

### D. 兼容输入（允许，但不是主验收口径）
- 脚上六经 + `t1/t2`
- 旧六键 legacy payload

兼容模式下必须在输出中明确标记：
- `input.mode`
- `input.compatibility.usedLegacyT1T2Proxy`
- `input.compatibility.usedCompatibilityMapping`

### E. 错误处理
以下情况必须返回 422：
- 缺失 `subject.id`
- 缺失 `measurements`
- 6 条经络不完整
- 显式输入时缺失 `trendDelta`
- 任一数值字段不可转为 number

### F. schema 一致性要求
仓库中的正式 schema 必须与代码主路径一致。
也就是说，正式 schema 不应继续把 `t1/t2` 作为唯一 required 字段。

---

## 3.2 输出必含字段

接口成功响应（200）必须至少包含：
- `subject`
- `context`
- `input`
- `engine`
- `meridianResults`
- `riskTags`
- `summary`
- `recommendations`
- `storefront`
- `trace`

若本轮目标包含“专业的 6 个角度评分”，则还必须包含：
- `analysisScores`
- `overallScore`

为兼容当前测试/调用方，可继续返回：
- `sixDimensionScores`
- `scores`
- `reportSummary`
- `advice`

但这些字段应被视为：
- `sixDimensionScores` / `scores`：**6 条经络评分层**
- `analysisScores` / `overallScore`：**6 个分析角度评分层**

---

## 3.3 6 条经络评分的验收要求（当前实现基础上收口）

### 字段结构
`meridianResults.<meridian>` 必须包含：
- `label`
- `status`
- `riskLevel`
- `trend`
- `sideState`
- `riskScore`
- `measurements.left`
- `measurements.right`
- `measurements.trendDelta`
- `signals`
- `ruleHits`
- `recommendations`

### 分数字段
`sixDimensionScores` 和 `scores` 必须与 `meridianResults` 一致，且：
- 必须固定 6 条经络，不多不少
- 每项 `score` 范围为 `0..100`
- 每项 `riskScore` 范围为 `0..100`
- `score + riskScore` 不要求严格等于 100，但若当前实现继续使用 `100-riskScore`，需在文档中写清楚

### 可追溯性
每条经络若命中规则，`ruleHits[*]` 至少应包含：
- `ruleId`
- `name`
- `category`
- `riskLevel`
- `explanation`
- `recommendations`
- `source`
- `evidence`

---

## 3.4 “专业的 6 个角度评分”定义建议（正式新增验收口径）

> 这里是**建议方案**，因为仓库当前没有正式的 6 角度模型；但为了让 code agent 在 20 轮内可执行，这里给出最稳妥、最贴近现有特征与规则的设计。

### 新增字段建议

```json
{
  "overallScore": 0,
  "analysisScores": [
    {
      "code": "leftRightBalance",
      "label": "左右平衡",
      "score": 0,
      "riskLevel": "low|medium|high",
      "basis": [],
      "summary": ""
    }
  ]
}
```

### 6 个角度定义建议

#### 1) `leftRightBalance` 左右平衡
**定义**：评估 6 条经络的左右差异是否整体平衡。

**可用证据**：
- `sideState`
- `abs_lr_delta`
- `cross_low`
- `left_low/right_low` 数量

**建议评分口径**：
- 基础分 100
- 每出现 1 条 `left_low/right_low` 扣 12 分
- 每出现 1 条 `cross_low` 扣 18 分
- 若出现 aggregate 左偏/右偏模式，再额外扣 10~15 分
- 最终夹在 `0..100`

**验收要求**：
- 至少引用 1 个以上 `trace.featureSnapshot.*.side_state` 或 aggregate rule 作为依据
- 返回 `basis` 不得为空

#### 2) `thermalLevel` 寒热水平
**定义**：评估当前偏低温/偏高温信号的整体强弱。

**可用证据**：
- `low_temp_signal`
- `high_temp_signal`
- `left/right` 与 `low_temp/high_temp` 阈值关系

**建议评分口径**：
- 基础分 100
- 每出现 1 条低温信号扣 10 分
- 每出现 1 条高温信号扣 8 分
- 若双侧均低（`bilateral_low`）每条额外扣 10 分

**验收要求**：
- 必须说明本分数偏向“温度风险程度”，不是医学寒热诊断

#### 3) `trendStability` 趋势稳定度
**定义**：评估 6 条经络的 `trendDelta` 是否整体平稳。

**可用证据**：
- `trend`
- `trendDelta`
- `down_strong/down_mild/up_strong/up_mild`

**建议评分口径**：
- 基础分 100
- 每条 `down_strong` 扣 20 分
- 每条 `down_mild` 扣 10 分
- 每条 `up_strong` 扣 15 分
- 每条 `up_mild` 扣 8 分

**验收要求**：
- `basis` 必须列出命中的趋势经络与方向

#### 4) `multiMeridianCoordination` 多经络协同性
**定义**：评估是否出现多条经络联动失衡。

**可用证据**：
- `trace.globalRuleHits`
- `multi_meridian_imbalance`
- 组合规则 / 聚合规则命中数

**建议评分口径**：
- 基础分 100
- 命中 1 条 combination 规则扣 10 分
- 命中 1 条 aggregate 规则扣 15 分
- 命中 `multi_meridian_imbalance` 再额外扣 20 分

**验收要求**：
- 必须至少使用 `globalRuleHits` 或 `riskTags`

#### 5) `recoveryPressure` 恢复压力
**定义**：评估当前是否存在“偏虚、偏冷、下降、恢复不足”的综合信号。

**可用证据**：
- `cold_or_deficiency_pattern`
- 高风险经络数量
- `down_strong`
- `left_low/right_low/bilateral_low`

**建议评分口径**：
- 基础分 100
- 每条高风险经络扣 15 分
- 命中 `cold_or_deficiency_pattern` 再扣 20 分
- 若肾经为高风险，再额外扣 10 分（依据当前规则库中肾经优先级较高）

**验收要求**：
- 必须基于已实现规则/特征，不得凭空生成

#### 6) `overallRhythm` 整体节律
**定义**：综合评估本次状态是否整体平稳、可持续观察。

**可用证据**：
- `riskTags`
- top meridian 风险分
- aggregate / combination 命中
- `summary`

**建议评分口径**：
- 可作为前 5 项加权平均
- 或以全局风险标签为主修正
- 建议权重：
  - 左右平衡 20%
  - 寒热水平 15%
  - 趋势稳定度 20%
  - 多经络协同性 20%
  - 恢复压力 25%

**验收要求**：
- 必须可解释
- 必须给出 `summary`
- 不能与 `overallScore` 含义完全重复；若重复，则保留一个即可

### `overallScore` 建议
- `overallScore` = `analysisScores` 六项加权平均后四舍五入
- 范围必须为 `0..100`
- 必须能从明细重算

---

## 3.5 报告摘要要求

### 当前最低要求
- `summary` 必须存在
- `reportSummary` 可作为兼容别名

### 正式验收要求
建议将摘要拆成结构化对象，而不是只保留单个字符串：

```json
{
  "reportSummary": {
    "headline": "",
    "overallAssessment": "",
    "keyFindings": ["", "", ""],
    "disclaimer": ""
  }
}
```

### 验收口径
- 必须包含 1 句总评
- 必须列出 2~3 个重点发现
- 必须包含“仅作风险提示/趋势参考，不等同于医疗诊断”边界表达
- 不得直接输出未经降级的临床结论

---

## 3.6 建议要求

### 当前最低要求
- `recommendations` 必须存在
- `advice` 可作为兼容别名

### 正式验收要求
建议输出结构化建议：

```json
{
  "advice": {
    "lifestyle": [""],
    "retest": [""],
    "consultation": [""],
    "focusMeridians": ["liver", "kidney"]
  }
}
```

### 验收口径
- 至少 3 条建议
- 至少覆盖：
  - 作息/饮食/保暖等轻干预建议
  - 复测建议
  - 问询/进一步确认建议
- 文案应基于已命中的规则或全局标签，不得无依据扩写
- 平稳 case 应更克制，不应套用高风险 case 口径

---

## 3.7 门店讲解层要求

`storefront` 必须至少包含：
- `focusHeadline`
- `clientExplanation`
- `retestPrompt`
- `conditioningPrompt`
- `talkTrack`

### 验收口径
- `clientExplanation` 必须包含非诊断边界表达
- `talkTrack` 必须固定 3 句
- 非平稳 case 的 `retestPrompt` 应包含“7-14 天内复测一次”
- 平稳 case 应强调“整体节律比较平稳/按周期复测”

证据：
- `tests/test_demo_storefront_fields.py`

---

## 3.8 非目标 / 不必做

本 20 轮迭代内，不必验收以下内容：
- 临床级医学诊断结论
- 真实硬件采集链路接入
- 历史多次测量的长期趋势建模
- 个体化治疗/处方生成
- “父/母体质偏向”“生男生女”等不稳健话术自动化
- 完整专家系统冲突消解引擎
- UI 页面或可视化大屏

---

## 4. 当前代码与本验收单的差距

### Gap 1：`input.schema.json` 与真实代码主路径不一致
当前 schema 文件仍要求每条经络为：
- `t1`
- `t2`

但代码主路径已是：
- `left`
- `right`
- `trendDelta`

**影响**：
- 文档、校验、调用方理解会分裂
- 无法把“显式 left/right/trendDelta”当成正式 contract

证据：
- `schemas/input.schema.json`
- `src/tcm_meridian_inference/schemas.py`

### Gap 2：当前 `sixDimensionScores` 命名与用户目标不一致
当前 `sixDimensionScores` 实际是**6 条经络评分**，不是**6 个分析角度评分**。

**影响**：
- 产品语义误导
- 后续前后端/客户演示容易把“经络维度”误认为“分析维度”

证据：
- `src/tcm_meridian_inference/rules.py::_build_six_dimension_scores`

### Gap 3：缺少正式 `analysisScores` / `overallScore`
当前没有真正定义：
- 6 个分析角度评分
- 总分 `overallScore`

**影响**：
- 用户要求的“专业的 6 个角度评分”仍未完成

### Gap 4：摘要与建议仍偏字符串列表，结构化不足
当前：
- `summary` 是单字符串
- `recommendations` 是字符串数组

**影响**：
- 对 API 调用方可读，但对后续 UI/报表/多端集成不够稳定

### Gap 5：验证命令在 README/ACCEPTANCE 中不够稳
README/ACCEPTANCE 写的是：
```bash
pytest -q
```
但在当前仓库环境中，直接运行会报：
- `ModuleNotFoundError: No module named 'tcm_meridian_inference'`

实测可通过以下方式运行：
```bash
PYTHONPATH=src pytest -q
```
或先：
```bash
pip install -e .[dev]
```

**影响**：
- 人工验收会误判项目不可用

### Gap 6：analysis 维度的评分公式未文档化
当前经络分数使用：
- `score = 100 - riskScore`

但该口径没有在 README / ACCEPTANCE 中作为正式 contract 说明。

**影响**：
- 结果可跑，但不可稳定对齐

### Gap 7：没有正式 response schema
当前有输入 schema、规则库 schema，但没有完整的 API response schema。

**影响**：
- 输出字段容易继续漂移
- 很难做跨端强校验

---

## 5. 迭代验收优先级建议（20 轮内）

### P0：先把 contract 定死
1. 修正 `schemas/input.schema.json` 与代码一致
2. 增加 response schema
3. 明确 `sixDimensionScores` = 6 条经络评分
4. 正式新增 `analysisScores` + `overallScore`

### P1：把 6 个分析角度真正算出来
5. 基于现有特征/规则实现 6 个分析角度评分
6. 给每个角度补 `basis` 和 `summary`
7. 保证能从 trace / ruleHits 追溯依据

### P2：把摘要和建议结构化
8. `reportSummary` 结构化
9. `advice` 结构化
10. 保留旧别名兼容一段时间

---

## 6. 验证命令（建议作为最终验收命令）

## 6.1 环境准备
```bash
cd /home/aa/clawd/projects/tcm-meridian-inference-mvp
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## 6.2 测试
若已 `pip install -e .[dev]`：
```bash
pytest -q
```

若未安装 editable package：
```bash
PYTHONPATH=src pytest -q
```

## 6.3 验证现有 5 个 demo case
```bash
PYTHONPATH=src python3 -m tcm_meridian_inference.cli fixtures/demo_case_01.json
PYTHONPATH=src python3 -m tcm_meridian_inference.cli fixtures/demo_case_02_right_low.json
PYTHONPATH=src python3 -m tcm_meridian_inference.cli fixtures/demo_case_03_cross_low.json
PYTHONPATH=src python3 -m tcm_meridian_inference.cli fixtures/demo_case_04_multi_imbalance.json
PYTHONPATH=src python3 -m tcm_meridian_inference.cli fixtures/demo_case_05_stable.json
```

## 6.4 API 验收
```bash
source .venv/bin/activate
uvicorn tcm_meridian_inference.api:app --host 0.0.0.0 --port 8000
```

```bash
curl http://127.0.0.1:8000/healthz
```

```bash
curl -X POST http://127.0.0.1:8000/api/inference/meridian-diagnosis \
  -H 'Content-Type: application/json' \
  --data @fixtures/demo_case_01.json
```

## 6.5 规则库加载状态
```bash
curl -X POST http://127.0.0.1:8000/api/rules/load \
  -H 'Content-Type: application/json' \
  -d '{}'
```

## 6.6 6 个分析角度评分最终验收（应新增）
最终应补一条专门测试：
- 响应中存在 `analysisScores`
- 长度必须为 6
- 6 个 `code` 固定不漂移
- 每项 `score` 范围 `0..100`
- `overallScore` 范围 `0..100`
- `overallScore` 可由 6 项重算

---

## 7. 最终验收结论（当前状态）

### 当前已经满足
- 有可运行 API
- 有脚上六经正式输入主路径
- 有兼容层与清晰标记
- 有 6 条经络结果
- 有经络级分数输出（`sixDimensionScores` / `scores`）
- 有摘要、建议、门店讲解层
- 有 trace / ruleHits / evidence 可解释性

### 当前还不算完成
**如果最终目标是：访问 API 可获取“专业的 6 个角度评分、报告摘要、建议”**，那当前还差：
1. 正式定义并实现 `analysisScores`
2. 正式定义并实现 `overallScore`
3. 修正 input schema 与代码主路径一致
4. 增加 response schema
5. 将摘要/建议进一步结构化为稳定 contract

---

## 8. 建议 code agent 严格遵循的最小完成标准

只有同时满足以下 5 条，才算本目标完成：
1. `POST /api/inference/meridian-diagnosis` 稳定返回 200
2. 返回 6 条经络结果 + 6 个分析角度评分
3. 返回结构化摘要和建议
4. 所有分数均可追溯到现有特征/规则/trace
5. README / schema / tests / API 输出四者一致
