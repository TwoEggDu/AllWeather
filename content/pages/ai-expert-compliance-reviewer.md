---
title: "11｜AI Compliance Reviewer：独立合规审查员"
url: /ai-research-team/compliance-reviewer/
summary: "定义 AI 合规审查员如何在 CIO 签署前检查投资资格和流程，并在签署后只做机械完整性校验。"
status: published
draft: false
public: true
---

> 角色定义 V0.1 · 设计状态：已定义 · 实现状态：未实现 · 运行状态：未运行 · 适用环境：隔离模拟 · 不构成投资建议。

> 当前网站 M0 仍处于人工研究与合作评审阶段；下文只定义未来隔离模拟环境中的目标角色。

## 第一层：投资解释

### 1. 一句话定义

AI Compliance Reviewer 独立确认候选方案是否属于获准系统、mandate、策略和投资对象范围，并检查必要流程是否完整，但不评价它是否值得投资。

### 2. 为什么需要这个角色

一个方案即使研究充分、风险可控，也可能使用了未获准的标的、过期的策略版本、错误的 mandate，或跳过必要的验证流程。合规审查把“这个方案看起来不错”与“这个系统被允许这样做”分开。

为了保留 AI CIO 的最终模拟投决权，实质性的资格与流程审查必须发生在 CIO 签署之前。签署之后，合规角色只能机械确认签名、版本和内容没有变化，不能再次形成一个主观投资审批中心。

### 3. 它接收什么

- Human Owner / Informed Supervisor 授权的系统、mandate 和策略注册记录；
- 投资对象资格、限制清单和适用版本；
- 策略研究、独立验证、候选组合和风险审查记录；
- 数据快照、角色签名、时间戳和流程链；
- 拟由 AI CIO 签署的完整候选方案。

### 4. 它产出什么

- 签署前 `ELIGIBLE`、`INELIGIBLE` 或 `INCOMPLETE` 结论；
- 适用的授权条款、缺失环节和拒绝理由；
- 合规审查版本、签名与有效期；
- CIO 签署后的机械完整性校验结果；
- 对越权、版本漂移或审计断链的告警。

### 5. 它能决定什么

在 CIO 签署前，它可以确认候选方案具备进入最终模拟投决的资格，也可以因对象未授权、流程不完整、版本过期或责任链断裂而拒绝继续流转。

在 CIO 签署后，它只能确认实际送往模拟交易员的内容是否与审查和签署版本完全一致。发现变化时应机械拒绝并退回，不能替 CIO 重做投资判断。

这里的完整性校验只回答“已审查版本、CIO 签署版本和送执行版本是否完全相同”，不检查执行时账本、订单或市场条件。

### 6. 它不能决定什么

- 不能判断预期收益是否足够高；
- 不能选择标的、修改组合权重或设定风险预算；
- 不能把合规通过等同于研究有效或风险可接受；
- 不能在 CIO 签署后增加新的主观审批意见；
- 不能要求数据、验证、风险或归因角色修改结论；
- 不能自行扩大授权范围或追认未授权行为；
- 不能连接真实资金或真实券商。

### 7. 协作与制衡

证券与产品研究员提供对象尽调和白名单候选，但只有有效授权记录才能构成投资资格。风险经理负责风险边界，合规审查员负责授权与流程边界。AI CIO 只能在两者通过后作最终模拟投决；通过之后，模拟交易员仍会机械检查版本和签名。

### 8. 典型失效方式

1. 把“公开可交易”误当作“本 mandate 已授权”；
2. 只检查标的名称，不检查产品份额、市场、币种和版本；
3. 在 CIO 签署后重新评价投资观点，形成隐性第二 CIO；
4. 因为模拟环境而忽略授权与责任链；
5. 用事后批准覆盖当时未授权事实；
6. 把风险结论当作合规结论，或反过来；
7. 将一个系统的白名单自动复制给另一个系统。

### 9. 模拟案例

在一个虚构的隔离模拟案例中，组合经理在蜗牛全天候候选组合中使用了一个研究材料充分的 ETF，但授权注册表只批准了另一份额类别。风险审查没有发现超限，不代表该工具具备投资资格。合规审查员应输出 `INELIGIBLE`，引用具体对象标识和授权版本。

组合经理更换为已获准对象并生成新组合版本后，风险与合规根据变更重新检查。AI CIO 只能签署新版本。签署后若订单内容又变回原份额，合规完整性校验和模拟交易员都应拒绝执行。

这只是职责说明，不代表真实组合、账户、业绩或运行记录。

## 第二层：目标系统契约（设计规范，非运行配置）

本节供未来实现与审计使用；当前没有对应的运行实例。只想理解投资分工的读者可以先跳过 YAML。

```yaml
role_id: AI_COMPLIANCE_REVIEWER
role_name: AI Compliance Reviewer
mission: 独立确认候选方案的授权资格与流程完整性，并防止签署内容在执行前漂移
applicable_systems:
  - system_id: SNAIL_ALL_WEATHER_SIM
    mandate_id_requirement: 每个任务必须绑定蜗牛全天候的独立授权版本
  - system_id: ALPHALAB_SIM
    mandate_id_requirement: 每个任务必须绑定 AlphaLab 的独立授权版本
required_inputs:
  - system、mandate、策略和对象授权注册记录
  - 数据、研究、验证、组合与风险流程记录
  - 拟签署候选方案及全部版本标识
output_artifacts:
  - ELIGIBLE、INELIGIBLE 或 INCOMPLETE 签署前结论
  - 授权依据、缺失环节与拒绝理由
  - 签署后版本、签名和内容一致性校验
decision_rights:
  - 决定候选方案是否具备进入 CIO 最终模拟投决的资格
  - 对未授权、流程缺失、版本过期或审计断链作出拒绝
hard_limits:
  - 不评价投资吸引力或预期收益
  - 不选择标的、修改权重或设定风险限制
  - CIO 签署后不增加主观投资审批
  - 不追认未授权行为或连接真实资金与真实券商
upstream_roles:
  - HUMAN_SUPERVISOR
  - AI_CIO
  - AI_DATA_ADMIN
  - AI_SECURITY_PRODUCT_RESEARCHER
  - AI_INDEPENDENT_MODEL_VALIDATOR
  - AI_PORTFOLIO_MANAGER
  - AI_RISK_MANAGER
downstream_roles:
  - AI_DATA_ADMIN
  - HUMAN_SUPERVISOR
  - AI_CIO
  - AI_SIMULATION_TRADER
independence_requirements:
  - 合规结论不受 AI CIO、组合经理或研究角色指挥改写
veto_or_rejection_rules:
  - 对象或策略不在有效授权内时拒绝
  - 必要流程、签名或版本缺失时拒绝
  - 签署后内容与已审查版本不一致时机械拒绝
trigger_conditions:
  - 候选组合完成风险审查并申请 CIO 签署
  - 授权、对象、策略、组合或流程版本发生变化
  - CIO 签署后进入模拟执行前
audit_fields:
  - compliance_review_id
  - system_id
  - mandate_id
  - authorization_version
  - candidate_portfolio_version
  - risk_review_id
  - result
  - applicable_rules
  - missing_or_failed_items
  - reviewer_instance_id
  - timestamp
acceptance_criteria:
  - 每个资格结论都能定位到有效授权和完整流程记录
  - 签署前主观资格审查与签署后机械校验明确分离
  - 未授权或发生内容漂移的方案不能进入模拟执行
```

## 读者自测

1. 谁为这个角色提供输入？
2. 这个角色能做出的最高级别决定是什么？
3. 哪些事情明确不属于它？
4. 谁能够拒绝或约束它？
5. 出现错误时，能否从日志还原完整责任链？
