# TCM 经络推理引擎文档

## 文档导航

### v3 版本 (当前)

#### 规范文档
| 文档 | 路径 | 说明 |
|------|------|------|
| PRD v1.0 | [v3/spec/prd-mulinsen-v1.md](v3/spec/prd-mulinsen-v1.md) | **木林森报告PRD** - 最新算法规范 |
| 测试规范 | [v3/spec/test-specification.md](v3/spec/test-specification.md) | 完整输入输出规范 |

#### 测试文档
| 文档 | 路径 | 说明 |
|------|------|------|
| 测试速查表 | [v3/testing/cheatsheet.md](v3/testing/cheatsheet.md) | 快速参考 |
| 测试报告 | [v3/testing/test-report.md](v3/testing/test-report.md) | 30个测试用例结果 |
| 验证报告 | [v3/testing/validation-report.md](v3/testing/validation-report.md) | 后端真实数据验证 |
| Agent模式测试规范 | [v3/testing/agent-test-specification.md](v3/testing/agent-test-specification.md) | Agent模式(LLM)输入输出规范 |

#### 分析文档
| 文档 | 路径 | 说明 |
|------|------|------|
| 算法边界分析 | [v3/analysis/algorithm-limits.md](v3/analysis/algorithm-limits.md) | 理论边界和限制 |

---

### 历史版本

#### v2.x 文档 (已归档)
| 文档 | 路径 | 说明 |
|------|------|------|
| PRD v2.0 | [archive/scoring-algorithm-prd-v2.md](archive/scoring-algorithm-prd-v2.md) | 旧版评分算法 |
| PRD v2.1 | [archive/scoring-algorithm-v2.1.md](archive/scoring-algorithm-v2.1.md) | 旧版评分算法更新 |
| Agent PRD | [archive/PRD-V2.1-AGENT.md](archive/PRD-V2.1-AGENT.md) | 旧版Agent规范 |
| 测试结果 | [archive/test_results.md](archive/test_results.md) | 旧版测试结果 |
| 验收标准 | [archive/acceptance-criteria.md](archive/acceptance-criteria.md) | 旧版验收标准 |

---

### 设计文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 规则库设计 | [design/rule-library.md](design/rule-library.md) | 规则库设计文档 |

---

### API 文档

| 文档 | 路径 | 说明 |
|------|------|------|
| API v3.0 | [api/api-reference-v3.md](api/api-reference-v3.md) | **最新接口规范** |
| API 测试用例 | [api/api-test-cases.md](api/api-test-cases.md) | **全部34个测试用例完整请求/响应** |
| API v2.0 | [api/api-reference.md](api/api-reference.md) | 旧版接口文档 |

---

### 外部资源

| 文档 | 路径 | 说明 |
|------|------|------|
| 规则库 PRD | [sources/rule-library-prd.md](sources/rule-library-prd.md) | 规则库详细规范 |
| AI 报告 PRD | [sources/ai-report-prd.md](sources/ai-report-prd.md) | AI报告规范 |
| 报告结构概览 | [sources/report-structure-overview.md](sources/report-structure-overview.md) | 报告结构 |
| 推理流程 | [sources/infer-engine-flow.md](sources/infer-engine-flow.md) | 引擎流程 |
| 六条经络辩证 | [sources/六条经络辩证.xlsx](sources/六条经络辩证.xlsx) | 经络辩证Excel |

---

### 项目规划

| 文档 | 路径 | 说明 |
|------|------|------|
| 路线图 | [roadmap.md](roadmap.md) | 项目路线图 |

---

## 快速开始

### 1. 了解最新算法
阅读 [v3/spec/prd-mulinsen-v1.md](v3/spec/prd-mulinsen-v1.md) 了解完整算法规范。

### 2. 查看测试用例
阅读 [v3/spec/test-specification.md](v3/spec/test-specification.md) 了解所有测试用例的输入输出。

### 3. 运行测试
```bash
# 运行所有测试
cd tests && python3 run_tests_v3.py

# 运行后端验证
cd tests && python3 validate_backend.py

# 记录 Rule-only 输出
cd tests && python3 record_actual_outputs.py

# 记录 Agent 输出
cd tests && python3 record_agent_outputs.py

# 运行单个测试（CLI）
python3 scripts/infer_v2.py fixtures/v3/case_01_first_test.json --pretty
```

---

## v3 关键变更

### 输入格式
```yaml
# v3 (新)
measurement_type: "first_test" | "retest"
gender: "male" | "female" | "unknown"
meridians:
  stomach:
    group1_left: 39.5    # 5分钟
    group1_right: 40.5
    group2_left: 42.4    # 20分钟
    group2_right: 42.5
```

### 评分算法
```yaml
# v3: 问题指数映射制
I = A + B + C + D + E
score = map_index_to_score(I)  # 分段映射
```

### 输出字段
```yaml
score_result:
  problem_index: 24.9
  problem_index_detail:
    A_low_temperature: 5.0
    B_temp_difference: 8.5
    C_side_bias: 5.0
    D_trend: 3.9
    E_combo: 2.5

lowest_points: { ... }
side_bias_summary: { ... }
cervical_lumbar_result: { ... }
focus_issues: [ ... ]
```

---

## 文件结构

```
docs/
├── README.md                    # 本文档
├── roadmap.md                   # 项目路线图
├── v3/                          # v3版本文档
│   ├── spec/                    # 规范文档
│   │   ├── prd-mulinsen-v1.md   # PRD v1.0
│   │   └── test-specification.md # 测试规范
│   ├── testing/                 # 测试文档
│   │   ├── cheatsheet.md        # 测试速查表
│   │   ├── test-report.md       # 测试报告
│   │   └── validation-report.md # 后端验证报告
│   └── analysis/                # 分析文档
│       └── algorithm-limits.md  # 算法边界分析
├── api/                         # API文档
│   └── api-reference.md
├── design/                      # 设计文档
│   └── rule-library.md
├── sources/                     # 外部资源
│   ├── rule-library-prd.md
│   ├── ai-report-prd.md
│   ├── report-structure-overview.md
│   ├── infer-engine-flow.md
│   └── 六条经络辩证.xlsx
└── archive/                     # 历史版本
    ├── scoring-algorithm-prd-v2.md
    ├── scoring-algorithm-v2.1.md
    ├── PRD-V2.1-AGENT.md
    ├── test_results.md
    └── acceptance-criteria.md
```

---

*最后更新: 2026-05-04*
