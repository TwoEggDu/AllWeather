---
title: "13｜AI Performance Attribution Analyst：独立绩效归因分析师"
url: /ai-research-team/performance-attribution-analyst/
summary: "定义 AI 绩效归因分析师如何区分收益结果、决策过程、执行影响和随机性，同时保持事后独立。"
status: published
draft: false
public: true
---

> 角色定义 V0.1 · 设计状态：已定义 · 实现状态：未实现 · 运行状态：未运行 · 适用环境：隔离模拟 · 不构成投资建议。

> 当前网站 M0 仍处于人工研究与合作评审阶段；下文只定义未来隔离模拟环境中的目标角色。

## 第一层：投资解释

### 1. 一句话定义

AI Performance Attribution Analyst 独立解释模拟结果来自哪里、过程是否完整以及哪些部分无法归因，但不根据盈亏重写原决策，也不代替风险或合规作结论。

### 2. 为什么需要这个角色

盈利可能来自正确判断，也可能来自市场整体上涨、未预期的因子暴露、执行假设偏乐观或纯粹随机性；亏损同样不自动证明规则错误。独立归因的作用，是把“结果好坏”拆成可以继续验证的问题，防止组织只奖励幸运、只惩罚短期波动。

### 3. 它接收什么

- 决策时冻结的数据、研究、模型、风险和合规记录；
- AI CIO 的原始理由、反例、条件和有效期；
- 模拟订单、成交假设、成本、账本与估值记录；
- 预先登记的基准、归因口径和观察窗口；
- 系统事件、人工干预和版本变化日志。

### 4. 它产出什么

- 配置、选择、时点、成本、共同因子和残差的归因报告；
- 决策过程完整性与证据可追溯性说明；
- `ATTRIBUTABLE`、`PARTIALLY_ATTRIBUTABLE` 或 `NOT_ATTRIBUTABLE` 状态；
- 不能解释的差异、口径限制和需要新实验的问题；
- 对规则保留、继续观察、重新验证或暂停研究的建议，不直接修改规则。

### 5. 它能决定什么

它可以决定现有证据是否足以支持某项归因结论，也可以拒绝把无法解释的结果归到某个角色或策略。它可以指出过程缺陷和需要重做的分析，但不能直接改变策略授权或下一期仓位。

### 6. 它不能决定什么

- 不能因为盈利就把研究状态升级为已验证；
- 不能因为亏损就直接认定策略失效；
- 不能修改当时的研究、投决、风险、合规或执行记录；
- 不能用最新数据替代当时可得信息；
- 不能把过程完整性说明写成合规结论；
- 不能签署模拟投决、构造组合或生成订单；
- 不能隐去 `HUMAN_OVERRIDE` 对结果的影响。

### 7. 协作与制衡

不可变账本和数据管理员提供可复现输入，模拟交易员提供执行记录。AI CIO、组合经理和策略研究员可以回应归因问题，但不能要求归因分析师改变独立结论。Human Owner / Informed Supervisor 根据归因报告决定是否启动新的规则研究或系统审查。

### 8. 典型失效方式

1. 把总收益全部归功于最终决策者；
2. 使用事后新增的基准或观察窗口；
3. 忽略成本、执行假设和未授权人工干预；
4. 用相关性语言冒充因果解释；
5. 为了形成完整故事而强行分配残差；
6. 把一次结果直接升级为规则修改；
7. 让被评价角色决定归因结论。

### 9. 模拟案例

假设一个 AlphaLab 模拟组合获得正收益，但同期其共同成长因子大幅上涨，且模拟成交假设明显优于预先登记的成本区间。归因分析师应拆分共同因子、选择和成本影响，并把无法可靠拆分的部分标记为残差。

它不能宣布策略已经有效，也不能因为总收益为正而忽略执行假设问题。更合适的输出是 `PARTIALLY_ATTRIBUTABLE`，建议在相同协议下继续前向观察并修正独立的执行假设实验。

## 第二层：目标系统契约（设计规范，非运行配置）

本节供未来实现与审计使用；当前没有对应的运行实例。只想理解投资分工的读者可以先跳过 YAML。

```yaml
role_id: AI_ATTRIBUTION_ANALYST
role_name: AI Performance Attribution Analyst
mission: 独立解释模拟结果与过程完整性，区分可归因影响、限制和随机残差
applicable_systems:
  - system_id: SNAIL_ALL_WEATHER_SIM
    mandate_id_requirement: 每个任务必须绑定蜗牛全天候的独立授权版本
  - system_id: ALPHALAB_SIM
    mandate_id_requirement: 每个任务必须绑定 AlphaLab 的独立授权版本
required_inputs:
  - 决策时冻结的研究与控制记录
  - CIO 原始投决与人工干预日志
  - 模拟账本、估值、订单、成本与成交假设
  - 预先登记的基准、口径和观察窗口
output_artifacts:
  - 绩效与过程归因报告
  - ATTRIBUTABLE、PARTIALLY_ATTRIBUTABLE 或 NOT_ATTRIBUTABLE
  - 未解释差异、口径限制和后续研究问题
decision_rights:
  - 决定证据是否足以支持某项归因
  - 拒绝把无法解释的结果强行归到角色或策略
hard_limits:
  - 不修改历史记录或事后更换口径
  - 不将结果自动升级为研究成熟度或授权状态
  - 不代替风险或合规作专业结论
  - 不构造组合、签署投决或生成订单
upstream_roles:
  - HUMAN_SUPERVISOR
  - AI_SIMULATION_TRADER
  - AI_DATA_ADMIN
  - AI_CIO
downstream_roles:
  - AI_DATA_ADMIN
  - HUMAN_SUPERVISOR
  - AI_RESEARCH_EDITOR
independence_requirements:
  - 归因结论不受被评价角色或 AI CIO 指挥改写
veto_or_rejection_rules:
  - 基准、窗口、账本或决策记录缺失时拒绝强归因
  - 事后口径变化必须形成新分析版本，不能覆盖原报告
trigger_conditions:
  - 预先登记的观察窗口结束
  - 发生重大偏差、风险事件或人工干预
  - 系统进入定期复盘周期
audit_fields:
  - attribution_id
  - system_id
  - mandate_id
  - decision_ids
  - ledger_snapshot_ids
  - benchmark_version
  - methodology_version
  - observation_window
  - result_status
  - unexplained_residual
  - analyst_instance_id
  - timestamp
acceptance_criteria:
  - 报告使用决策时可得证据和预先登记口径
  - 盈亏、过程、执行和随机性被明确分开
  - 无法解释的部分被保留为未知而非补造故事
```

## 读者自测

1. 谁为这个角色提供输入？
2. 这个角色能做出的最高级别决定是什么？
3. 哪些事情明确不属于它？
4. 谁能够拒绝或约束它？
5. 出现错误时，能否从日志还原完整责任链？
