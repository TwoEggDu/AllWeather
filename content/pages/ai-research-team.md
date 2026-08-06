---
title: "00｜AI 投研专家系统总导读"
url: /ai-research-team/
summary: "一套面向蜗牛全天候与 AlphaLab 的未来 AI 投研组织设计：角色分工、模拟投决权、独立控制和审计边界。"
status: published
draft: false
public: true
---

> 组织定义 V0.1 · 设计状态：已定义 · 实现状态：未实现 · 运行状态：未运行 · 适用环境：隔离模拟 · 不构成投资建议。

## 第一层：投资解释

### 这套组织要解决什么问题

单个 AI 可以写观点、算指标或生成报告，但“能输出内容”不等于“能够承担一套投资流程”。真正的投研组织需要把提出假设、管理证据、独立验证、构造组合、限制风险、审查资格、执行指令和事后归因分开，避免同一个角色既出题、又评分、又批准自己的答案。

这套组织不是让人类假装成为宏观、量化或风控专家。AI 专家是策略研发与验证的基础力量；Human Owner / Informed Supervisor 负责提出要研究的问题、理解专家为何这样判断以及风险在哪里，并在理解后作系统级授权。

本系列定义的是一套未来目标治理结构。它服务两个研究系统：

- **蜗牛全天候**：研究资产配置、风险分散与低频组合治理；
- **AlphaLab**：研究个股选择、择时、事件驱动和其他主动策略假设。

两者可以使用相同的角色语言和审计纪律，但不是同一个投资账户。每项任务都必须带有独立的 `system_id`（所属研究系统）与 `mandate_id`（本次任务获准使用的投资范围），数据、策略、组合、模拟资金和研究结论默认不跨系统传递。

### 当前状态与目标状态

M0 是当前网站的人工研究、方法设计与合作评审阶段，还没有 AI 投研组织运行。

| 维度 | 当前网站 M0（人工研究与合作评审） | 本系列描述的未来目标 |
|---|---|---|
| 核心工作 | 方法论设计、公开阅读和合作评审 | 隔离模拟环境中的 AI 投研治理 |
| 最终判断 | 当前仍由人完成 | 已授权边界内由 AI CIO 作最终模拟投决 |
| 人类职责 | 研究与评审主体 | 系统授权者和监督者，不逐笔审批 |
| 自动执行 | 没有 | 只允许未来的模拟执行，不接真实券商 |
| 运行证据 | 尚无 AI 组织运行证据 | 必须等实现、验证和正式授权后另行记录 |

因此，公开这些定义不等于改变当前系统状态，也不等于 AI 已经获得真实资产管理权限。未来若要从当前边界迁移到目标边界，仍需单独的版本决定、实现验证和运行授权。

### 组织的五个职能组

#### 1. 治理与最终模拟投决

- [Human Owner / Informed Supervisor]({{< relref "pages/ai-expert-human-supervisor.md" >}})：提出研究问题，要求专家用可理解的方式说明策略与风险，授权系统、策略版本和投资范围，并监督异常；
- [AI CIO]({{< relref "pages/ai-expert-cio.md" >}})：在所有前置控制通过后，接受、拒绝、暂缓或退回候选组合，作出最终模拟投决。

这里不是一条可以逐级覆盖的权力链，而是按事项分权：Human Owner / Informed Supervisor 决定系统是否获授权、暂停或终止，并要求理解策略与风险；AI CIO 只在合格候选中作最终模拟投资选择；AI Risk Manager 对硬限制拥有不可覆盖的否决权；AI Compliance Reviewer 可以因投资资格或流程不合规阻止签署，但不判断哪个合格方案更值得投资。

#### 2. 数据与研究证据

- [AI Data Administrator]({{< relref "pages/ai-expert-data-administrator.md" >}})：管理数据来源、点时快照、修订、质量和可追溯性；
- [AI Macro Researcher]({{< relref "pages/ai-expert-macro-researcher.md" >}})：形成宏观环境状态、证据与风险倾向建议；
- [AI Industry Researcher]({{< relref "pages/ai-expert-industry-researcher.md" >}})：研究产业结构、景气、竞争和传导链；
- [AI Security/Product Researcher]({{< relref "pages/ai-expert-security-product-researcher.md" >}})：研究公司基本面、估值、ETF 或基金产品，并形成可投资工具候选材料。

#### 3. 策略验证与组合构建

- [AI Strategy Researcher]({{< relref "pages/ai-expert-strategy-researcher.md" >}})：把投资想法改写成可证伪的策略假设；
- [AI Independent Model Validator]({{< relref "pages/ai-expert-model-validator.md" >}})：独立检查复现性、数据泄漏、过拟合、样本外表现和成本口径；
- [AI Portfolio Manager]({{< relref "pages/ai-expert-portfolio-manager.md" >}})：把获准研究结论映射为符合 mandate 的候选组合。

#### 4. 独立控制与模拟执行

- [AI Risk Manager]({{< relref "pages/ai-expert-risk-manager.md" >}})：独立检查风险限制，并对越界方案作出硬否决；
- [AI Compliance Reviewer]({{< relref "pages/ai-expert-compliance-reviewer.md" >}})：在 CIO 签署前检查投资资格、授权范围和流程合规；
- [AI Simulation Trader]({{< relref "pages/ai-expert-simulation-trader.md" >}})：机械验证并执行完整、有效的模拟指令，不创造投资观点。

#### 5. 独立复盘与公开表达

- [AI Performance Attribution Analyst]({{< relref "pages/ai-expert-attribution-analyst.md" >}})：独立区分市场、配置、选择、执行和随机性对结果的影响；
- [AI Research Editor]({{< relref "pages/ai-expert-research-editor.md" >}})：把已确认的研究事实与边界转化为可公开、可质疑的内容，不修改研究结论。

### 一次模拟决策怎样流转

```text
Human Owner 提出研究问题并确认授权范围
  → 专家形成策略与人类可理解说明卡
  → 授权 mandate 与策略版本
  → 数据管理员冻结点时证据
  → 宏观 / 行业 / 证券与产品研究形成研究材料
  → 策略研究员提出可证伪假设
  → 独立模型验证员给出独立验证结论
  → 组合经理形成候选组合
  → 风险经理审查并保留硬否决权
  → 合规审查员完成签署前资格审查
  → AI CIO 接受、拒绝、暂缓或退回
  → 合规审查员机械校验签署内容、版本与审查结果一致
  → 模拟交易员校验版本并模拟执行
  → 独立账本保存不可覆盖的状态
  → 归因分析师复盘，研究编辑形成公开表达
```

“AI CIO 最终决定”只表示没有另一个角色在它之后重新作主观投资判断。风险否决、合规资格和执行完整性仍是前置条件；CIO 不能把被否决的同一方案直接改名后执行。

签署后的合规校验只比较内容、签名和版本是否一致；模拟交易员随后检查账本状态、有效期和执行条件。两者都不是新的主观投资审批。

### 组织级模拟案例

假设 AlphaLab 提交一项已经完成独立模型验证的候选组合。组合经理冻结候选版本后，风险经理发现共同因子暴露超过 mandate 的硬限制并作出否决。AI CIO 不能签署该方案，人类监督者也不能用一句人工同意让它继续执行。

组合经理可以形成降低共同暴露的新版本。新版本重新经过风险和签署前合规审查后，AI CIO 决定接受。合规审查员随后只机械确认签署内容与已审查版本一致，模拟交易员再检查账本和执行条件。归因分析师在观察窗口结束后独立解释结果，研究编辑只能忠实公开证据、限制和未知。旧版本的风险否决仍保留在审计链中。

### 三类不是 AI 专家的基础能力

完整系统未来还需要三类确定性基础设施，但它们不是拥有观点或权力的专家：

1. **不可变模拟账本与估值服务**：保存订单、成交假设、持仓、现金、估值和成本；
2. **版本与审计日志**：保存输入、模型、规则、签名、拒绝原因和人工干预；
3. **授权策略注册表**：回答哪个 `system_id` 可以在什么 `mandate_id` 下运行哪个冻结版本。

基础设施只能忠实记录和校验，不能替任何专家补写缺失结论。

### 权力边界

以下权力按事项分立，不构成一条可以逐级覆盖的审批链。

| 事项 | 该事项上的最高决定权 | 不能做什么 |
|---|---|---|
| 研究问题、系统范围、mandate 与规则版本 | Human Owner / Informed Supervisor | 不得覆盖历史证据、替代技术验证或强行通过同一风险否决 |
| 研究数据是否可用于本次任务 | AI Data Administrator | 不得把数据可用等同于投资有效 |
| 模型验证结论 | AI Independent Model Validator | 不得批准投资或构造组合 |
| 候选组合 | AI Portfolio Manager | 不得自行越过风险与合规 |
| 风险硬限制 | AI Risk Manager | 不得创造新的收益观点 |
| 签署前资格与流程合规 | AI Compliance Reviewer | 不得变成第二个主观 CIO |
| 最终模拟投决 | AI CIO | 不得改写独立结论或绕过前置控制 |
| 模拟执行是否满足机械条件 | AI Simulation Trader | 不得自行改变方向、规模或标的 |
| 事后归因 | AI Performance Attribution Analyst | 不得用盈亏倒推篡改原决策 |
| 公开表达 | AI Research Editor | 不得把未知写成事实或把研究写成建议 |

## 第二层：目标系统契约（设计规范，非运行配置）

本节供未来实现与审计使用；当前没有对应的运行实例。只想理解投资分工的读者可以先跳过 YAML。

```yaml
role_id: AI_RESEARCH_ORG
role_name: AI 投研专家系统
mission: 在隔离模拟环境中，让 AI 专家主导研究与验证，并以职责分离、独立控制、可理解说明和不可覆盖记录完成可审计的投研闭环
applicable_systems:
  - system_id: SNAIL_ALL_WEATHER_SIM
    mandate_id_requirement: 每个任务必须绑定蜗牛全天候的独立授权版本
  - system_id: ALPHALAB_SIM
    mandate_id_requirement: 每个任务必须绑定 AlphaLab 的独立授权版本
required_inputs:
  - Human Owner 提出的研究问题与授权范围
  - 已授权的 system_id 与 mandate_id
  - 冻结的策略、数据、风险和执行版本
  - 可追溯的点时证据
output_artifacts:
  - 带签名和理由的模拟投决
  - 面向 Human Owner 的人类可理解说明卡
  - 模拟订单、账本与估值记录
  - 独立风险、合规、验证和归因结论
decision_rights:
  - 由各角色在明确边界内分别行使，不允许单一角色包办全流程
hard_limits:
  - 禁止连接真实资金或真实券商
  - 禁止跨 system_id 或 mandate_id 默认复用状态
  - 禁止覆盖原始结论与人工干预前记录
upstream_roles:
  - Human Owner / Informed Supervisor
downstream_roles:
  - AI Research Editor
independence_requirements:
  - 数据、模型验证、风险、合规和归因结论不受 AI CIO 指挥改写
veto_or_rejection_rules:
  - 风险硬否决不得在同一决策中被覆盖
  - 缺少授权、版本、签名或点时证据时停止流转
trigger_conditions:
  - 新 mandate 获得授权
  - 已授权周期检查到期
  - 数据、规则、策略或风险版本发生变化
audit_fields:
  - system_id
  - mandate_id
  - strategy_version
  - data_snapshot_id
  - risk_rule_version
  - decision_id
  - actor_id
  - timestamp
  - parent_record_id
acceptance_criteria:
  - 任一模拟决策都能还原输入、独立结论、签署、执行和复盘责任链
  - 任何越界、缺失或人工干预都有不可覆盖记录
```

## 怎样阅读本系列

不必先相信这套分工。更有价值的阅读方式是逐篇追问：这个角色的输入从哪里来，它能作出什么最高决定，谁能拒绝它，它最可能怎样越权，以及日志能否在出错后还原责任链。

## 读者自测

1. 为什么文章已经发布不等于 AI 组织已经运行？
2. AI CIO 的“最终模拟投决权”为什么不等于可以覆盖风险否决？
3. 蜗牛全天候与 AlphaLab 共用角色模型时，哪些状态默认不能互通？
4. 为什么模拟账本、审计日志和授权注册表不被定义为 AI 专家？
5. 如果一项模拟决策出错，最少需要哪些标识才能还原责任链？
