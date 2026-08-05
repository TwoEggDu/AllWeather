---
title: AlphaLab 实验、复盘与版本模板
url: /alphalab/experiment-and-review-template/
summary: 分开记录策略实验、前向模拟、收益归因、策略治理决定和系统方法论变更。
status: draft
draft: true
public: false
---

> 本页只提供空模板。A0 不创建实验结果、模拟交易、收益数字或策略版本。

## 1. 公共记录契约

每类记录都必须包含稳定 ID、对象版本、模板版本、负责人、记录时间、上游证据引用和追加更正链。旧记录只读；发现错误时追加更正，说明时间、原因和影响范围，不覆盖原始内容。

七类对象各自回答不同问题：

| 记录 | 回答什么 | 不能替代什么 |
|---|---|---|
| 策略假设卡 | 为什么一个可证伪想法值得研究 | 不能写实验结果或批准策略 |
| 策略实验记录 | 一个冻结设计怎样检验了什么 | 不能自行推动晋级 |
| 前向模拟记录 | 当时可见信息、信号和模拟执行发生了什么 | 不能补写历史或连接实盘 |
| 收益归因与复盘 | 结果来自哪里，过程和规则是否合格 | 不能自行裁决策略去留 |
| 规则修改与版本记录 | 为什么提出一项单一修改，怎样验证与回滚 | 不能让未验证修改直接生效 |
| 策略治理决定 | 为什么晋级、观察、暂停、恢复、回滚或淘汰 | 不能临时改实验结果或规则 |
| 系统方法论决定 | 为什么改变 AlphaLab 的流程、模板或门槛 | 不能评价单一策略表现 |

## 2. 策略实验记录

```yaml
experiment_id: 待决定
run_id: 待决定
strategy_id: 待决定
strategy_version: 待决定
record_schema_version: 待决定
status: planned | running | paused | completed | invalid | aborted

owner: 待决定
reviewer: 待决定
created_at: 待决定
recorded_at: 待决定
started_at: 待决定
closed_at: 待决定

research_question: 待验证
pre_registered_expectation: 待验证
null_or_competing_explanation: 待验证
single_primary_change: 待决定

hypothesis_version: 待决定
research_protocol_version: 待决定
data_contract_version: 尚未连接
data_snapshot_id: 尚未连接
implementation_version: 尚未实现
cost_and_execution_assumption_version: 待决定
benchmark_version: 待决定

sample_roles:
  in_sample: 待决定
  out_of_sample: 待决定
  walk_forward: 待决定

leakage_checks: 待验证
survivorship_bias_checks: 待验证
multiple_testing_record: 待验证
parameter_stability_plan: 待验证

run_manifest: 尚未运行
result_summary: 尚未运行
attribution_summary: 尚未运行
risk_observations: 尚未运行
limitations: 未知
invalidity_reason: 不适用

recommended_disposition: 待决定
evidence_refs: 暂无充分证据
corrections: 无
```

`invalid` 表示数据、实现或研究完整性使结果不能用于结论，不等于策略“不通过”；`aborted` 表示实验被中止，也必须保留已有运行和原因。重跑创建新 `run_id`，不能覆盖不利结果。

## 3. 前向模拟记录

```yaml
forward_run_id: 待决定
event_or_decision_id: 待决定
strategy_id: 待决定
strategy_version: 待决定
simulation_spec_version: 待决定
record_schema_version: 待决定
owner: 待决定

decision_at: 待决定
data_as_of: 待决定
published_at: 待决定
data_available_at: 待决定
recorded_at: 待决定
earliest_execution_at: 待决定

input_snapshot_ref: 尚未连接
source_versions: 尚未连接
missing_or_revised_state: 未知

signal_snapshot: 尚未生成
supporting_evidence: 暂无充分证据
counter_evidence: 暂无充分证据
evidence_refs: 暂无充分证据
unknowns: 未知
invalidation_status: 待验证

simulated_order: 尚未生成
fill_assumption_version: 待决定
fill_status: not_started | filled | partially_filled | unfilled | cancelled | blocked
unfilled_or_block_reason: 不适用
transaction_cost_record: 尚未生成
slippage_record: 尚未生成

later_observation: 尚未到期
review_trigger: 待决定
closure_reason: 待决定
corrections: 无
```

规则进入前向模拟后冻结。修改规则要停止当前版本、保存旧结果、记录原因、创建新版本并重新观察。后续事实只追加到 `later_observation`，不得反写 `signal_snapshot`。未成交、部分成交、保持不动、数据阻塞和系统失败都是正式结果。

## 4. 收益归因与复盘

```yaml
review_id: 待决定
strategy_id: 待决定
strategy_version: 待决定
experiment_or_forward_ref: 待决定
attribution_method_version: 待决定
record_schema_version: 待决定
owner: 待决定
recorded_at: 待决定
evidence_refs: 暂无充分证据

original_hypothesis: 待验证
information_available_at_decision: 待验证
supporting_evidence_then: 暂无充分证据
counter_evidence_then: 暂无充分证据
rules_followed: 待验证

market_beta_contribution: 未计算
industry_beta_contribution: 未计算
style_exposure_contribution: 未计算
stock_selection_contribution: 未计算
timing_contribution: 未计算
event_contribution: 未计算
transaction_cost: 未计算
slippage: 未计算
unexplained_residual: 未计算

process_attribution: 待验证
luck_or_randomness: 未知
invalidation_condition_triggered: 待验证
new_evidence: 暂无充分证据

recommended_next_step: continue_observation | propose_experiment | pause | retire | 待决定
reviewer: 待决定
corrections: 无
```

归因先检查结果能否对平，再解释来源；无法解释的部分保留为残差，不强行分配。相关性不等于机制已被证明，结果有利也不能把全部收益归给策略。复盘只形成证据和建议，正式去留写入策略治理决定。

## 5. 规则修改与版本记录

```yaml
change_id: 待决定
strategy_id: 待决定
record_schema_version: 待决定
owner: 待决定
recorded_at: 待决定
evidence_refs: 暂无充分证据
problem_statement: 待验证
problem_classification: data | hypothesis | signal | execution | risk | overfitting | expression | randomness

original_version: 待决定
proposed_version: 待决定
single_primary_change: 待决定
change_hypothesis: 待验证
new_risks_introduced: 待验证

validation_method: 待决定
observation_horizon: 待决定
keep_conditions: 待决定
rollback_conditions: 待决定

status: proposed_experiment | under_validation | accepted | rejected | rolled_back
decision_ref: 待决定
corrections: 无
```

一次只修改一个主要假设或规则。数据错误、实现错误、规则问题和随机波动分别记账；不得用“策略升级”掩盖 bug，也不得因结果不好直接改参数。未经验证的修改只能是 `proposed_experiment`。

## 6. 策略治理决定

```yaml
strategy_decision_id: 待决定
strategy_id: 待决定
subject_strategy_version: 待决定
record_schema_version: 待决定
owner: 待决定
recorded_at: 待决定
decision_type: promote | continue_observation | pause | resume | downgrade | return_to_hypothesis | rollback | retire

decided_at: 待决定
current_status: 待决定
target_status: 待决定
criteria_contract_version: 待决定
criteria_evaluation: 待验证

evidence_refs: 暂无充分证据
evidence_as_of: 待决定
rationale: 待验证
counterarguments: 暂无充分证据
unknowns: 未知
risks_and_dependencies: 待验证

conditions_attached: 待决定
stop_or_rollback_instructions: 待决定
approver: 待决定
reviewer: 待决定
corrections: 无
```

恢复必须引用原暂停决定并证明原问题已修复；等待时间经过或结果反弹不是恢复证据。淘汰不删除记录。降级针对成熟度，回滚针对版本，两者不能混用。任何 AlphaLab 晋级都只表示研究成熟度变化，不表示实盘资格或外部系统采用。

## 7. 系统方法论决定

```yaml
method_decision_id: 待决定
method_area: 待决定
record_schema_version: 待决定
owner: 待决定
recorded_at: 待决定
method_version_before: 待决定
method_version_after: 待决定

problem_statement: 待验证
problem_classification: data | methodology | governance | template | expression
evidence_refs: 暂无充分证据
decision: 待决定
rationale: 待验证
alternatives_considered: 待验证
rejected_options: 待验证

scope: 待决定
out_of_scope: 待决定
new_risks: 待验证
validation_plan: 待决定
rollback_plan: 待决定

effective_at: 待决定
review_trigger: 待决定
approver: 待决定
reviewer: 待决定
status: proposed | experimental | accepted | rejected | rolled_back
corrections: 无
```

系统方法改版只对声明的后续记录生效，不批量重写历史。旧记录缺少新字段时，写明“旧模板未采集”，不得事后猜填。

## 8. 当前禁用项

A0 不启用主观 Override、自动调参、自动晋级、自动风险动作或真实交易。未来若提出例外机制，也必须先建立独立方法论决定、授权范围、到期条件和撤销方式；本页不提供该能力。

## 相关文档

- [策略假设卡模板](/alphalab/strategy-hypothesis-template/)
- [AlphaLab 方法论](/alphalab/methodology/)
- [AlphaLab Roadmap](/alphalab/roadmap/)
