# TCM Meridian Inference — 中医经络推理 Agent

输入 24 个温度数据（6经络 × 2次测量 × 左右）
→ 特征工程（温差计算、阴阳判定）
→ 规则引擎推理
→ 输出：健康评分 + 经络状态 + 调理建议

## 架构
- 1 个 OpenClaw Agent (`tcm-meridian`)
- 调用推理脚本执行规则匹配
- 规则库源自《六条经络辩证》

## 快速测试
```bash
cd ~/clawd/projects/tcm-meridian-inference-mvp
python3 scripts/infer.py fixtures/case_left_low.json
```
