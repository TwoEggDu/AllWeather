---
title: "01｜Human Owner / Informed Supervisor：知情监督与系统授权"
url: /ai-research-team/human-supervisor/
summary: "定义系统所有者如何提出研究问题、理解专家的策略与风险说明，并作系统级授权而不替代专业判断。"
status: published
draft: false
public: true
---

> 角色定义 V0.1 · 设计状态：已定义 · 实现状态：未实现 · 运行状态：未运行 · 适用环境：隔离模拟 · 不构成投资建议。

> 当前网站 M0 仍处于人工研究与合作评审阶段；下文只定义未来隔离模拟环境中的目标角色。

## 第一层：投资解释

### 1. 一句话定义

在未来目标设计中，Human Owner / Informed Supervisor 将提出研究问题、要求理解策略与风险、负责系统授权和紧急制动，但不会成为每一笔模拟交易的幕后基金经理或技术验证员。

### 2. 为什么需要这个角色

AI 不能自行决定自己可以管理什么、使用什么策略、承担多少风险或何时连接新的能力。即使模拟系统拥有完整的投研流程，也需要一个系统外责任主体提出真正要解决的问题，确认目标、范围、禁止事项和暂停条件。

这个角色的价值不在于比所有专家更懂每一个研究细节，而在于让专家必须把“为什么这样做、证据在哪里、最大风险是什么、什么会让结论失效”解释到系统所有者能够监督的程度。人类随后只在明确授权内决定系统是否运行、策略版本是否进入隔离模拟，并在异常发生时保留停止系统、追问责任和修改下一版本规则的能力。

### 3. 它接收什么

- 系统状态、异常告警和审计日志；
- AI CIO 的模拟决策记录；
- 数据、验证、风险、合规和归因角色的独立报告；
- 每个策略版本和最终模拟投决的人类可理解说明卡；
- mandate、策略、模型、风险和执行规则的版本变更申请；
- 人工干预前的完整原始状态。

### 4. 它产出什么

- 已签署的 `system_id`、`mandate_id` 和允许能力范围；
- 策略或系统规则版本的授权、拒绝或暂停记录；
- 系统级继续运行、降级、暂停或终止决定；
- 追加式 `HUMAN_OVERRIDE` 记录及理由；
- 需要重新研究、重新验证或重新授权的问题单。
- 研究问题、优先级和解释补充请求记录。

### 5. 它能决定什么

它的常规治理权包括：提出或排序研究问题，要求专家补充解释，决定某个模拟系统是否启动、暂停或终止，哪个策略或规则版本获准生效，以及这些授权何时到期。

它的紧急制动权只在授权失效、审计断链或系统级紧急状态下使用。此时它可以追加 `HUMAN_OVERRIDE`，停止尚未执行的 CIO 决策或暂停全部模拟执行；这不是基于另一项投资观点逐笔否决 CIO。

### 6. 它不能决定什么

- 不能要求数据管理员删除不利数据或修改点时证据；
- 不能要求独立验证、风险、合规或归因角色改变结论；
- 不能把风险经理对同一方案的硬否决强行改成可执行；
- 不能在不生成新版本和新责任链的情况下临时改变 mandate；
- 不能让人工口头意见覆盖原始 AI 决策；
- 不能把隔离模拟授权解释成真实资金管理授权。
- 不需要也不能以外行身份替代模型验证、风险、合规或研究结论的专业判断。

### 7. 协作与制衡

Human Owner / Informed Supervisor 向 AI CIO 提供授权边界，但不指导单笔模拟投决；它可以直接读取所有独立控制报告，并要求专家把内容解释清楚，但不能通过组织关系压低风险或验证标准。它对系统是否继续存在负责，AI CIO 对已授权边界内的最终模拟投决负责。

在未来目标设计中，授权策略注册表会拒绝未获授权或已过期的人类指令，风险、合规和模拟交易角色也会对越界指令作机械拒绝。当前这些基础设施尚未实现，因此这里只定义应有的制衡，不声称已经形成运行闭环。

### 8. 典型失效方式

1. **影子 CIO**：名义上让 AI 决策，实际上逐笔口头指挥；
2. **只看盈亏授权**：因为一次盈利放松规则，或因为一次亏损立即改参数；
3. **无痕干预**：直接修改结果，没有保留原始 AI 决策；
4. **越过独立控制**：要求风险或合规“配合通过”；
5. **跨系统误授权**：把 AlphaLab 的策略资格自动扩展到蜗牛全天候；
6. **永久紧急状态**：长期依靠人工救火，掩盖系统本身不可运行。

### 9. 模拟案例

假设 AlphaLab 的候选组合已经通过模型验证。专家向 Human Owner / Informed Supervisor 说明：组合依赖何种证据、最大风险是集中度、何种情景会触发暂停。随后风险经理发现其集中度超过当前 mandate 的硬上限并予以否决。人类可以确认暂停该候选方案、要求专家解释是否值得研究新的集中度规则，或拒绝规则变更；但不能在原决策上写一句“人工同意”后让模拟交易员执行。

如果未来形成新的风险规则，必须得到新版本号和授权，再由组合经理重新构造方案，风险与合规重新审查，AI CIO 重新作出模拟投决。原否决记录仍然保留。

## 第二层：目标系统契约（设计规范，非运行配置）

本节供未来实现与审计使用；当前没有对应的运行实例。只想理解投资分工的读者可以先跳过 YAML。

```yaml
role_id: HUMAN_SUPERVISOR
role_name: Human Owner / Informed Supervisor
mission: 提出研究问题，理解专家对策略与风险的解释，授权系统范围与规则版本，监督独立控制和异常，并保留可追溯的人类责任
applicable_systems:
  - system_id: SNAIL_ALL_WEATHER_SIM
    mandate_id_requirement: 每个任务必须绑定蜗牛全天候的独立授权版本
  - system_id: ALPHALAB_SIM
    mandate_id_requirement: 每个任务必须绑定 AlphaLab 的独立授权版本
required_inputs:
  - 系统状态与异常告警
  - 完整审计日志
  - 独立验证、风险、合规和归因报告
  - 人类可理解说明卡
  - 版本变更与授权申请
output_artifacts:
  - system 与 mandate 授权记录
  - 系统启动、暂停、降级或终止决定
  - 规则版本授权或拒绝记录
  - HUMAN_OVERRIDE 追加记录
  - 研究问题、优先级与解释补充请求记录
decision_rights:
  - 提出和排序研究问题，并要求可理解说明
  - 决定系统是否获准运行
  - 决定 mandate 与系统规则版本是否生效
  - 在授权失效、审计异常或系统级紧急状态下追加 HUMAN_OVERRIDE 并停止待执行指令
hard_limits:
  - 不逐笔替代 AI CIO 作模拟投决
  - 不覆盖独立结论或原始记录
  - 不强行通过同一风险硬否决
  - 不授权真实资金或真实券商连接
  - 不替代技术验证或独立控制作专业结论
upstream_roles:
  - AI_DATA_ADMIN
  - AI_INDEPENDENT_MODEL_VALIDATOR
  - AI_RISK_MANAGER
  - AI_COMPLIANCE_REVIEWER
  - AI_ATTRIBUTION_ANALYST
  - AI_RESEARCH_EDITOR
downstream_roles:
  - AI_CIO
  - AI_DATA_ADMIN
  - AI_MACRO_RESEARCHER
  - AI_INDUSTRY_RESEARCHER
  - AI_SECURITY_PRODUCT_RESEARCHER
  - AI_STRATEGY_RESEARCHER
  - AI_INDEPENDENT_MODEL_VALIDATOR
  - AI_PORTFOLIO_MANAGER
  - AI_RISK_MANAGER
  - AI_COMPLIANCE_REVIEWER
  - AI_SIMULATION_TRADER
  - AI_ATTRIBUTION_ANALYST
  - AI_RESEARCH_EDITOR
independence_requirements:
  - 不以组织所有权要求独立控制角色修改专业结论
veto_or_rejection_rules:
  - mandate、责任主体或版本边界不完整时不得启动
  - 风险硬否决只能通过新规则版本与完整重跑处理
  - 不得以主观投资偏好逐笔取消或替换 AI CIO 决策
trigger_conditions:
  - 新系统或新 mandate 申请
  - 策略、风险、模型或执行规则版本变化
  - 严重异常、审计断链或越权告警
  - 定期治理复查到期
audit_fields:
  - supervisor_id
  - system_id
  - mandate_id
  - authorization_id
  - rule_version
  - action_type
  - reason
  - timestamp
  - parent_record_id
acceptance_criteria:
  - 每个运行范围都有明确的人类责任主体和有效授权
  - 每个授权策略和 CIO 决策都有系统所有者能够复述的策略、风险和失效条件说明
  - 所有人工干预都保留干预前状态、理由与后续影响
  - 人类监督没有变成不可审计的逐笔幕后指挥
```

## 读者自测

1. 谁为这个角色提供输入？
2. 这个角色能做出的最高级别决定是什么？
3. 哪些事情明确不属于它？
4. 谁能够拒绝或约束它？
5. 出现错误时，能否从日志还原完整责任链？
