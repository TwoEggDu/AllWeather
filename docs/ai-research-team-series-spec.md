# AI 投研专家系列统一规格

## 系列定位

本系列公开定义一套未来可用于蜗牛全天候与 AlphaLab 的 AI 投研组织治理目标。当前只定义角色、权力、接口和审计边界，不表示任何 AI 专家、数据链路、策略、组合、模拟账户或自动执行能力已经实现或运行。

蜗牛全天候与 AlphaLab 可以复用同一套上层组织模型，但必须使用不同的 `system_id` 与 `mandate_id`。数据、策略、组合、资金记录和结论默认不跨系统传递。

V0.1 使用两个规范系统标识：蜗牛全天候为 `SNAIL_ALL_WEATHER_SIM`，AlphaLab 为 `ALPHALAB_SIM`。`applicable_systems` 必须使用带 `system_id` 和 `mandate_id_requirement` 的对象列表，不能只写展示名称；`audit_fields` 必须逐字段列出，不能把多个字段压在同一个字符串中。

`upstream_roles` 只列出直接提供必需输入、任务授权或前置控制的角色，`downstream_roles` 只列出直接消费本角色正式输出的角色；两者统一使用本规格中的 `role_id`。公开读者等非角色接收方可以使用单独的稳定标识。

V0.1 的正式产物传递主干为：

```text
HUMAN_SUPERVISOR → 所有角色的授权边界
AI_DATA_ADMIN ↔ 直接提出数据请求并消费冻结快照的角色
AI_MACRO_RESEARCHER → AI_INDUSTRY_RESEARCHER / AI_SECURITY_PRODUCT_RESEARCHER / AI_STRATEGY_RESEARCHER
AI_INDUSTRY_RESEARCHER → AI_SECURITY_PRODUCT_RESEARCHER / AI_STRATEGY_RESEARCHER
AI_SECURITY_PRODUCT_RESEARCHER → AI_STRATEGY_RESEARCHER / AI_COMPLIANCE_REVIEWER
AI_STRATEGY_RESEARCHER → AI_INDEPENDENT_MODEL_VALIDATOR
AI_INDEPENDENT_MODEL_VALIDATOR → AI_PORTFOLIO_MANAGER / AI_COMPLIANCE_REVIEWER / AI_CIO
AI_PORTFOLIO_MANAGER → AI_RISK_MANAGER / AI_COMPLIANCE_REVIEWER / AI_CIO
AI_RISK_MANAGER → AI_COMPLIANCE_REVIEWER / AI_CIO
AI_COMPLIANCE_REVIEWER → AI_CIO → 签署后 AI_COMPLIANCE_REVIEWER → AI_SIMULATION_TRADER
AI_SIMULATION_TRADER → AI_ATTRIBUTION_ANALYST → AI_RESEARCH_EDITOR
独立数据、验证、风险、合规、归因和编辑报告 → HUMAN_SUPERVISOR
```

AI CIO 可以把方案退回 AI Portfolio Manager 重构；这会产生新版本并重新进入风险与合规流程，不是对原版本的无痕修改。

## 不可改写的共同边界

1. 不连接真实资金、真实券商或真实交易账户。
2. Human Owner / Informed Supervisor 提出研究问题、授权投资范围、系统规则与策略版本，并监督异常；不需要独立验证技术细节，也不逐笔审批模拟投资。
3. AI CIO 在冻结且已授权的策略、数据、风险与执行边界内拥有最终模拟投决权。
4. AI Risk Manager 拥有独立硬否决权；同一决策上的否决不能被 AI CIO 覆盖。修改风险规则必须形成新版本并重新运行流程。
5. AI Compliance Reviewer 在 AI CIO 签署前完成投资资格与流程合规审查；签署后只允许机械校验版本、签名和完整性，不形成第二个主观投决中心。
6. AI CIO 不得指挥 AI Data Administrator、AI Independent Model Validator、AI Risk Manager、AI Compliance Reviewer 或 AI Performance Attribution Analyst 改写独立结论。
7. AI Macro Researcher 输出环境状态、证据与风险倾向建议，不直接设定产品权重、交易动作或正式硬风险预算。
8. AI Portfolio Manager 负责将获准研究结论构造成候选组合；若 AI CIO 要求修改风险审查过的权重，必须退回组合构建与控制流程。
9. AI Simulation Trader 只执行完整、已签署且仍在有效版本上的模拟指令；它可以因机械条件不满足而拒绝执行，但不能创造投资观点。
10. AI Performance Attribution Analyst 独立解释结果、过程完整性和可归因性，不代替合规结论，也不根据结果倒推修改历史记录。
11. 人工干预必须保留原始 AI 决策，并追加 `HUMAN_OVERRIDE` 记录，不能覆盖原记录。
12. 角色定义不是对当前网站现行 M0 人工评审流程的运行状态声明，而是未来隔离模拟环境的目标治理设计。

## 角色清单与文件

| 编号 | 角色 | role_id | 文件 |
|---|---|---|---|
| 00 | 系列总导读 | `AI_RESEARCH_ORG` | `content/pages/ai-research-team.md` |
| 01 | Human Owner / Informed Supervisor | `HUMAN_SUPERVISOR` | `content/pages/ai-expert-human-supervisor.md` |
| 02 | AI CIO | `AI_CIO` | `content/pages/ai-expert-cio.md` |
| 03 | AI Data Administrator | `AI_DATA_ADMIN` | `content/pages/ai-expert-data-administrator.md` |
| 04 | AI Macro Researcher | `AI_MACRO_RESEARCHER` | `content/pages/ai-expert-macro-researcher.md` |
| 05 | AI Industry Researcher | `AI_INDUSTRY_RESEARCHER` | `content/pages/ai-expert-industry-researcher.md` |
| 06 | AI Security/Product Researcher | `AI_SECURITY_PRODUCT_RESEARCHER` | `content/pages/ai-expert-security-product-researcher.md` |
| 07 | AI Strategy Researcher | `AI_STRATEGY_RESEARCHER` | `content/pages/ai-expert-strategy-researcher.md` |
| 08 | AI Independent Model Validator | `AI_INDEPENDENT_MODEL_VALIDATOR` | `content/pages/ai-expert-model-validator.md` |
| 09 | AI Portfolio Manager | `AI_PORTFOLIO_MANAGER` | `content/pages/ai-expert-portfolio-manager.md` |
| 10 | AI Risk Manager | `AI_RISK_MANAGER` | `content/pages/ai-expert-risk-manager.md` |
| 11 | AI Compliance Reviewer | `AI_COMPLIANCE_REVIEWER` | `content/pages/ai-expert-compliance-reviewer.md` |
| 12 | AI Simulation Trader | `AI_SIMULATION_TRADER` | `content/pages/ai-expert-simulation-trader.md` |
| 13 | AI Performance Attribution Analyst | `AI_ATTRIBUTION_ANALYST` | `content/pages/ai-expert-attribution-analyst.md` |
| 14 | AI Research Editor | `AI_RESEARCH_EDITOR` | `content/pages/ai-expert-research-editor.md` |

## 公开页面 front matter

每篇页面使用如下字段，并填写对应标题、URL 和摘要：

```yaml
---
title: "..."
url: /ai-research-team/.../
summary: "..."
status: published
draft: false
public: true
---
```

`status: published` 只表示文章可以公开阅读，不表示角色已经实现。正文顶部必须明确：

> 角色定义 V0.1 · 设计状态：已定义 · 实现状态：未实现 · 运行状态：未运行 · 适用环境：隔离模拟 · 不构成投资建议。

不得出现 `[待补数据]`、`[图表占位]`、`[待补参考资料]`，不得虚构数据、业绩、引用或来源。

## 单篇文章结构

以下九段角色模板适用于 01—14。00 总导读同样使用“第一层：投资解释”和“第二层：系统契约”，但第一层按组织定位、现状与目标、职能组、决策流、组织级模拟案例、基础设施和权力边界展开，不套用单一角色的九段标题。

### 第一层：投资解释

1. 一句话定义
2. 为什么需要这个角色
3. 它接收什么
4. 它产出什么
5. 它能决定什么
6. 它不能决定什么
7. 协作与制衡
8. 典型失效方式
9. 模拟案例

### 第二层：目标系统契约（设计规范，非运行配置）

每篇文章在 YAML 前统一说明：本节供未来实现与审计使用，当前没有对应运行实例；只关注投资分工的读者可以跳过。

用 YAML 代码块填写以下字段，内容应具体、可审计，不写空字段：

```yaml
role_id:
role_name:
mission:
applicable_systems:
required_inputs:
output_artifacts:
decision_rights:
hard_limits:
upstream_roles:
downstream_roles:
independence_requirements:
veto_or_rejection_rules:
trigger_conditions:
audit_fields:
acceptance_criteria:
```

### 结尾：读者自测

1. 谁为这个角色提供输入？
2. 这个角色能做出的最高级别决定是什么？
3. 哪些事情明确不属于它？
4. 谁能够拒绝或约束它？
5. 出现错误时，能否从日志还原完整责任链？

## 状态词分离

- `content status`：文章是 draft 还是 published。
- `design_status`：角色定义是否形成版本。
- `implementation_status`：角色是否已经被实现。
- `runtime_status`：角色是否正在某个授权环境运行。
- `research_maturity`：研究对象的证据成熟度。
- `authorization_status`：某个策略或任务是否获得进入下一阶段的授权。

这些状态不得互相替代。文章已发布不等于角色已运行，研究成熟不等于获得授权，获得授权也不等于执行成功。

## 人类可理解说明卡

任何新策略版本申请进入隔离模拟，以及任何 AI CIO 的最终模拟投决，都必须同时附带一张面向 Human Owner / Informed Supervisor 的说明卡。它不是技术验证报告，也不是公开投资建议，而是让系统所有者能够知情监督的解释层。

```yaml
plain_language_question: 这项策略或决策试图解决什么问题
why_it_may_work: 专家认为可能成立的主要依据
key_evidence: 支持和反对证据的简明摘要
main_risks: 最重要的损失、模型、数据或执行风险
unknowns: 当前尚未解决的不确定性
change_or_stop_conditions: 什么情况会改变结论、暂停或撤回
current_status: idea、research、validated、authorized 或 simulated
```

Human Owner / Informed Supervisor 可以要求专家补充或用更清楚的语言解释这张卡；这会让方案退回解释或研究环节，不会让人类替代独立验证、风险、合规或 AI CIO 的专业结论。

## 第三方策略保证机构（未来治理接口）

第三方策略保证机构（`External Strategy Assurance Panel`）是未来可选的外部独立复核接口，不属于 V0.1 的 AI 专家角色图，也不构成当前运行能力。它仅在策略首次申请进入隔离模拟、发生重大版本变化或固定周期复审时审查策略版本与治理证据包。

它应审查策略逻辑及其学术或经验依据、独立复现与回测边界、风险和失效条件、授权版本和审计链，以及人类可理解说明是否忠实。其结论只能是 `ASSURED`、`CONDITIONAL` 或 `NOT_ASSURED`：后者阻止下一阶段授权，前者两者均不替代内部独立验证、风险、合规或 AI CIO 的单次模拟投决。

它不得选择标的、修改权重、设置日常风险预算、生成模拟订单或覆盖内部独立结论。是否以及何时接入真实第三方机构，必须另行形成版本化决策、审阅范围和授权记录。
