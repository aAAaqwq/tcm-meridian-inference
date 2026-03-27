# 单页系统页面验收清单 + 演示检查表

> 目标：这个单页不是“能跑就行”，而是要 **可验收、可演示、可继续产品化演进**。  
> 核心标准：Daniel 打开页面后，能在 3 分钟内看懂、跑通、讲清 6 条经络评分结果。

---

## 一、页面验收清单

## 1. 页面必须展示的模块

### A. 页面头部 / 基本说明
必须有：
- 页面标题：中医经络评分演示 / 类似明确标题
- 一句话说明：这是 **6 条经络评分 API 的演示页**
- 非医疗诊断提示：结果仅作风险提示/复测对照，不等同于医疗诊断

验收标准：
- 用户一进页面就知道这是干什么的
- 页面上能看到“非诊断”边界，不藏在接口返回里

### B. Demo Case / 输入区
必须有：
- Demo case 快速切换入口（至少 5 个）
- 或可直接粘贴/加载 JSON 请求体
- 明确显示当前使用的是哪一个 case
- 明确显示当前输入模式：
  - foot_six_explicit
  - foot_six_legacy_pair（如支持）
  - legacy_mapped（如支持）

推荐 5 个 case：
- 左低型
- 右低型
- 交叉型
- 多经络失衡型
- 相对平稳型

验收标准：
- 演示人员不需要改代码就能切 case
- 切换 case 后能立即重新请求并刷新结果

### C. 请求状态区
必须有：
- 请求中状态
- 请求成功状态
- 请求失败状态
- 接口错误信息展示

验收标准：
- 不能点了按钮没反应
- 失败时不能只在 console 报错，页面上必须可见

### D. 六经络评分结果主视图
必须有：
- 6 条经络固定展示：
  - liver
  - spleen
  - kidney
  - stomach
  - gallbladder
  - bladder
- 每条经络至少展示：
  - label / 名称
  - score
  - riskScore
  - riskLevel
  - status
  - sideState
  - trend

验收标准：
- 6 条必须完整，不多不少
- 一眼能看出哪几条最值得关注
- 不允许只展示 raw JSON 而没有结果层表达

### E. 全局结论区
必须有：
- summary / reportSummary
- riskTags
- recommendations / advice

验收标准：
- 页面能直接说清“总体看到了什么”
- 页面能直接说清“建议下一步怎么做”

### F. 门店讲解区（重点）
必须有：
- storefront.focusHeadline
- storefront.clientExplanation
- storefront.retestPrompt
- storefront.conditioningPrompt（如接口有）
- storefront.talkTrack（如接口有）

验收标准：
- 这块内容能直接用于现场讲解
- 至少能支持 Daniel 现场连续说 3 句话，不需要自己临场编

### G. 可解释性 / 技术依据区
必须有：
- trace.globalRuleHits
- 每条经络的 ruleHits 数量或明细
- engine.ruleConfigSource
- engine.ruleSetId

验收标准：
- 不要求默认全展开
- 但必须能展开看依据，证明不是“拍脑袋结果”

---

## 2. 页面必须消费的 API 字段

## A. 顶层必消费
- input.mode
- engine.ruleConfigSource
- engine.ruleSetId
- summary
- reportSummary
- riskTags
- recommendations
- advice
- storefront
- trace
- meridianResults
- sixDimensionScores
- scores

## B. 每条经络必消费字段
至少消费：
- label
- status
- riskLevel
- score
- riskScore
- sideState
- trend
- measurements.left
- measurements.right
- measurements.trendDelta
- ruleHits

说明：
- 页面主展示可优先用 `scores` 或 `sixDimensionScores`
- 但详情区必须能回到 `meridianResults` 看完整信息

## C. 门店讲解字段必消费
- storefront.focusHeadline
- storefront.clientExplanation
- storefront.retestPrompt

如已存在，也建议消费：
- storefront.conditioningPrompt
- storefront.talkTrack

## D. 可解释字段必消费
- trace.globalRuleHits
- meridianResults.<meridian>.ruleHits[*].source
- meridianResults.<meridian>.ruleHits[*].evidence

---

## 3. 演示时必须具备的交互

### 必须有
- 选择 demo case
- 点击“开始分析 / 运行演示 / 重新生成结果”
- 请求完成后页面自动刷新结果
- 能查看某一条经络的详情
- 能看到门店讲解文案
- 能看到失败提示并允许重试

### 强烈建议有
- 一键复制请求 JSON
- 一键复制结果摘要
- 一键展开/收起技术详情
- 默认高亮 Top 3 关注经络

### 演示交互验收标准
- 从打开页面到出结果，不超过 3 步
- 演示人员无需打开开发者工具
- 切换 case 后不会残留上一个 case 的结果状态

---

## 4. 不应出现的问题

### 不能出现的体验问题
- 页面只有 JSON，没有可读结果
- 页面字段名全是技术名，没有中文/可讲解表达
- 点击后无 loading、无反馈
- 请求失败但页面像成功一样
- 切换 case 后结果不刷新
- 展示字段缺失、空白、undefined、null 裸奔
- 6 条经络顺序漂移
- 平稳 case 仍然展示过度惊悚的话术

### 不能出现的业务问题
- 页面没有“非诊断”提示
- 把兼容模式当正式主路径讲
- 无法区分左低 / 右低 / 交叉 / 多经络 / 平稳几类 case
- 重点关注经络与结果排序不一致
- recommendations 和 storefront 话术互相打架
- 页面无法说明结果来源于规则命中/trace

### 不能出现的工程问题
- 依赖本地手改代码才能演示
- mock 数据和真实 API 返回结构不一致
- 首屏报错
- 控制台报错导致核心流程不可用
- 接口慢/报错时没有兜底展示

---

## 二、演示检查表

## 1. 演示前
- 页面可正常打开
- API 可请求成功
- 至少 5 个 demo case 可切换
- 页面上能看到“非诊断”提示
- 默认 case 能稳定出结果

## 2. 演示中
按这条线走：
1. 选一个 case
2. 点击分析
3. 看 6 条经络结果
4. 看重点关注 + 总结 + 建议
5. 展开 1 条经络看 ruleHits / evidence
6. 切换另一个 case，证明页面不是静态假数据

## 3. 演示通过标准
满足以下即算通过：
- 5 类 case 至少能稳定演示 3 类以上
- 6 条经络结果完整展示
- 门店讲解字段可直接读
- 可解释性入口存在
- 无明显报错、错位、假死

---

## 三、Daniel 快速验收步骤

1. 打开页面，确认这不是接口调试页，而是可讲解的演示页。  
2. 直接跑一个 demo case，确认页面能展示 6 条经络评分，不是只吐 JSON。  
3. 看页面是否同时有：重点关注、总结、建议、非诊断提示。  
4. 切换到另一个 case，确认结果会变化，且能看出左低/右低/交叉/平稳差异。  
5. 点开任意一条经络详情，确认能看到 ruleHits / evidence / 来源。  
6. 确认失败时页面有提示、可重试，不会假装成功。  
7. 如果 Daniel 能现场顺着页面讲完 1 分钟，这页就算过第一轮验收。

---

## 四、一句话验收口径

**这页是否合格，不看技术栈，先看 Daniel 能不能拿它稳定演示“6 条经络评分 API 的输入、结果、讲解、依据”。能，就过；不能，就继续收口。**
