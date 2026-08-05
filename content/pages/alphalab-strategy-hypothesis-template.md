---
title: AlphaLab 策略假设卡模板
url: /alphalab/strategy-hypothesis-template/
summary: 将策略想法登记为带时点、证据、失效条件、验证计划和生命周期门槛的可证伪假设。
status: draft
draft: true
public: false
---

> 复制本模板时保留全部字段。缺失信息只能写“待验证”“待决定”“未知”或“暂无充分证据”，不得用虚构数字或默认值补齐。

## 使用规则

- 一张卡只登记一个主要研究问题和一个 `strategy_family`；
- 假设必须可证伪，不能只写“看好”“有潜力”或“可能上涨”；
- `data_available_at` 记录信息首次真实可得时间，不等于数据所属时间；
- 支持证据、反对证据、未知项和替代解释同时登记；
- 晋级、暂停和淘汰条件要在看到对应结果前写出；
- 假设、研究协议、数据契约或规则改变时创建新版本，不覆盖旧卡；
- 假设卡不是实验结果、策略批准书、仓位建议或交易指令。

## 可复制模板

```yaml
strategy_id: 待决定
record_schema_version: 待决定
strategy_name: 待决定
strategy_family: stock_selection | timing | event_driven

status: idea | researching | historical_testing | out_of_sample | forward_simulation | stable_observation | paused | retired

research_question: 待验证
hypothesis: 待验证
why_edge_may_exist: 暂无充分证据
who_or_what_may_pay_for_the_edge: 未知

market: 待决定
eligible_universe: 待决定
excluded_universe: 待决定
expected_holding_period: 待验证

required_data: 待决定
data_as_of: 待决定
published_at: 待决定
data_available_at: 待决定
known_data_risks: 待验证
data_contract_version: 待决定

signal_definition: 待验证
entry_logic: 待验证
exit_logic: 待验证
expiry_logic: 待验证
invalidation_conditions: 待验证

expected_return_source: 暂无充分证据
primary_risk_source: 待验证
expected_failure_regime: 待验证
competing_explanations: 待验证

transaction_cost_assumption: 待决定
slippage_assumption: 待决定
liquidity_requirements: 待决定
capacity_constraints: 待验证

validation_plan: 待决定
in_sample_role: 待决定
out_of_sample_role: 待决定
walk_forward_plan: 待决定
forward_simulation_plan: 待决定

promotion_conditions: 待决定
pause_conditions: 待决定
resume_conditions: 待决定
retirement_conditions: 待决定
rollback_conditions: 待决定

hypothesis_version: 待决定
research_protocol_version: 待决定
strategy_version: 待决定
created_at: 待决定
recorded_at: 待决定
next_review_date_or_event: 待决定

supporting_evidence: 暂无充分证据
counter_evidence: 暂无充分证据
evidence_refs: 暂无充分证据
unknowns: 未知
owner: 待决定
reviewer: 待决定
review_status: 待决定
corrections: 无
```

## 字段检查

### 研究对象与机制

`research_question` 只问一个可以通过证据回答的问题。`hypothesis` 应写清输入、作用机制、预期结果、比较对象和反证；`why_edge_may_exist` 与 `who_or_what_may_pay_for_the_edge` 用来阻止只凭相关性命名 Alpha。

### 时间与数据

数据记录至少区分：

- `data_as_of`：数据描述哪个时期；
- `published_at`：来源何时发布该值或事件；
- `data_available_at`：研究者最早何时真实可见；
- 信号形成时间和未来最早可模拟执行时间；
- 原发布值、修订值及其数据契约版本。

无法证明当时可得的字段不得用于历史信号。只有当前存续对象组成的样本不得被称为已控制幸存者偏差。

### 信号、执行与失效

`signal_definition` 描述逻辑，不在 A0 填因子公式或阈值。`entry_logic`、`exit_logic` 和 `expiry_logic` 必须分开；事件驱动策略尤其要说明事件结束后何时到期，不能无限期持有。

`invalidation_conditions` 优先描述机制、边界、测量、数据或实现失效；一次不利价格结果不自动等于假设失效。

### 验证与生命周期

`validation_plan` 应说明样本内、样本外、Walk-forward、成本、偏差控制和前向观察分别回答什么。具体区间、门槛和周期在相应阶段决定，不在模板中预填。

`promotion_conditions`、`pause_conditions`、`resume_conditions`、`retirement_conditions` 和 `rollback_conditions` 必须先于结果登记。若门槛仍是“待决定”，策略不得据此晋级。

## 当前候选登记

```yaml
strategy_id: Strategy-001
strategy_name: 成长股选股
strategy_family: stock_selection
status: idea
research_question: 待研究
strategy_version: 尚未建立
```

这条登记只证明候选想法存在。它没有确定市场、股票池、因子、数据、参数、风险上限、验证协议或策略版本，因此不能进入历史验证，也不能输出任何股票或仓位。

## 相关文档

- [AlphaLab 方法论](/alphalab/methodology/)
- [实验、复盘与版本模板](/alphalab/experiment-and-review-template/)
