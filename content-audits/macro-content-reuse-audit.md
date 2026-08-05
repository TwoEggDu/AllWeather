# 宏观内容复用审计

> 审计日期：2026-08-05
> 目标：用尽可能少的新增内容，把旧知识资产整理成“宏观环境层”的八篇核心文章。
> 边界：本审计只判断内容用途，不把旧文中的观点、参数或交易表达升级为现行规则。

## 一、审计范围和口径

本轮对仓库中的 **180 篇历史文章**做了标题、分类、链接和边界词扫描，并对其中 **34 篇宏观高相关旧文**做了结构和内容复核；同时检查了 `文档/宏观系统/` 的 8 份材料，以及当前的宏观总纲和宏观索引。详细复核范围合计 **44 份宏观相关内容**。

复用比例是工程判断，不是内容质量评分：

- 约 60% 以上的目标结构已经存在：优先原地改造并保留 slug；
- 约 30%～60% 可复用：摘取或多篇合并，旧文可继续承担基础阅读；
- 不足约 30%：不强行改写，只作为背景或延伸阅读；
- 旧文凡缺少精确来源、数据真实可得时间或边界说明，均不能直接成为当前系统结论。

## 二、八篇核心文章的复用决定

| 目标核心文章 | 现有候选文件 | 可复用内容 | 主要缺口 | 建议动作 | 是否需要新建 |
|---|---|---|---|---|---|
| 1. 宏观环境层总纲：它负责什么、不负责什么 | `content/pages/macro-layer.md`；`文档/宏观系统/宏观仪表盘_指标定义.md`；`文档/宏观系统/月度宏观复盘.md` | 六模块、统一状态卡、共同风险边界、宏观与执行边界；旧文的证据和复查意识 | 缺少统一 14 节结构、`available_at`、共同环境描述与风险边界的分离、完整输入输出契约 | 原地改造 | 否 |
| 2. 中国增长周期怎么判断 | `growth-inflation-liquidity-basics.md`；`pmi-leading-risk-assets.md`；`how-to-read-china-pmi-official-vs-caixin.md`；`why-real-estate-matters-in-china.md`；`how-to-read-china-trade-data-and-rmb.md` | 增长概念、PMI 结构、内需/地产/外需观察维度 | 没有一篇承担增长模块的状态表达、证据冲突、真实可得时间和下游契约 | 新建核心文章 | 是 |
| 3. 中国通胀与价格周期怎么判断 | `why-china-cpi-and-ppi-diverge.md`；`cpi-and-assets.md`；`core-vs-headline-cpi.md`；`inflation-expectations-vs-realized-inflation.md`；`why-service-inflation-is-sticky.md`；`how-oil-price-transmits-to-assets.md` | 中国 CPI/PPI 背离、总量与结构、预期与实际、服务与商品、外部成本传导 | 旧文多为美国/全球教程，缺少中国价格模块状态卡、来源与可得时间；资产表达越过宏观边界 | 多篇合并 | 否；计划原地改造 `why-china-cpi-and-ppi-diverge.md` 并保留 slug |
| 4. 中国流动性与信用怎么判断 | `how-to-read-tsf-and-credit-impulse-in-china.md`；`what-financial-conditions-are.md`；`how-to-read-pboc-policy-signals.md`；`what-credit-spreads-signal.md`；`qt-vs-rate-hikes.md` | 实体信用、银行间资金、市场融资条件的概念与传导 | 中国与美国口径混杂；政策意图和流动性结果混杂；没有三子层及其分歧表达 | 新建核心文章 | 是 |
| 5. 中国政策周期怎么记录和判断 | `how-to-read-china-fiscal-policy.md`；`how-to-read-pboc-policy-signals.md`；`fiscal-vs-monetary-policy-basics.md`；`case-study-2024-924-policy-pivot.md` | 财政、货币、地产、资本市场政策的分类；政策事件时间线 | 部分央行机制表述需重新核验；缺少“表态—发布—执行—传导”分层和点时证据 | 多篇合并 | 否；计划原地改造 `how-to-read-china-fiscal-policy.md` 并保留 slug |
| 6. 全球外部环境如何约束中国资产 | `what-financial-conditions-are.md`；`what-fed-hikes-and-cuts-really-change.md`；`how-to-read-fomc.md`；`why-the-dollar-rises.md`；`real-rates-gold-bonds-dollar.md`；`how-oil-price-transmits-to-assets.md` | 全球增长、利率、美元、商品和金融条件的传导框架 | 旧文以美国资产交易为中心，缺少“只约束中国共同环境”的边界及证据卡 | 多篇合并 | 否；计划原地改造 `what-financial-conditions-are.md` 并保留 slug |
| 7. 日历与事件风险怎样进入系统 | `data-release-day-playbook.md`；`weekly-macro-tracking-workflow.md`；`monthly-macro-review-workflow.md`；`crisis-playbooks-three-scenarios.md` | 事件前准备、事实/预期/修正区分、复查和记录意识 | 旧文偏交易流程或固定频率，部分直接给操作；没有计划事件与突发事件的系统边界 | 新建核心文章 | 是 |
| 8. 六个模块如何形成共同风险边界 | `content/pages/macro-layer.md`；`文档/宏观系统/月度宏观复盘.md`；`how-to-build-a-macro-observation-board.md`；`first-postmortem-for-a-macro-view.md` | 支持/反对证据、未知项、复盘，以及开放/中性/收敛/防守的基本语言 | 缺少六模块分歧处理、未知状态、边界形成过程；旧月度复盘直接给组合动作 | 新建核心文章 | 是 |

最终建议保持 **8 篇核心文章**：4 篇新建、4 篇原地改造。第一轮实际只新建增长、流动性与信用两篇，并原地改造总纲；另外两篇新文和三篇旧文改造仅保留为后续提纲。

## 三、候选旧文逐篇标记

说明：

- “未经验证”指文章包含需要重新核验的事实、机制或普遍化结论，不表示结论必然错误；
- “缺来源”指缺少能够支持正文主要结论的精确来源链接；
- “缺可得时间”指没有记录信息在当时何时真实可获得；
- “边界冲突”指宏观文章直接进入资产偏好、仓位、买卖或执行；
- 风险等级描述“被误读为投资建议”的可能性。

| 候选旧文件 | 主要范围 | 类型 | 未经验证 | 缺来源 | 缺真实可得时间 | 与六层边界冲突 | 投资建议误读风险 | 处置 |
|---|---|---|---|---|---|---|---|---|
| `growth-inflation-liquidity-basics.md` | 中国/全球混合 | 方法论教程 | 部分 | 是 | 是 | 部分 | 中 | 摘取部分内容 |
| `pmi-leading-risk-assets.md` | 全球 | 数据解读 | 是 | 是 | 是 | 是 | 高 | 仅作为延伸阅读 |
| `how-to-read-china-pmi-official-vs-caixin.md` | 中国 | 数据解读 | 部分 | 是 | 是 | 是 | 高 | 仅作为延伸阅读 |
| `how-to-read-tsf-and-credit-impulse-in-china.md` | 中国 | 数据解读 | 部分 | 是 | 是 | 是 | 高 | 仅作为延伸阅读 |
| `why-real-estate-matters-in-china.md` | 中国 | 市场机制 | 部分 | 是 | 是 | 是 | 高 | 仅作为延伸阅读 |
| `china-proxy-variables-mapping.md` | 中国 | 方法论/数据映射 | 是 | 是 | 是 | 是 | 高 | 摘取部分内容 |
| `how-to-read-china-trade-data-and-rmb.md` | 中国 | 数据解读 | 部分 | 是 | 是 | 是 | 高 | 仅作为延伸阅读 |
| `why-china-cpi-and-ppi-diverge.md` | 中国 | 数据解读 | 部分 | 是 | 是 | 是 | 中 | 多篇合并 |
| `cpi-and-assets.md` | 美国/全球 | 数据解读 | 是 | 是 | 是 | 是 | 高 | 仅作为延伸阅读 |
| `core-vs-headline-cpi.md` | 美国/全球 | 数据解读 | 部分 | 是 | 是 | 是 | 中 | 仅作为延伸阅读 |
| `inflation-expectations-vs-realized-inflation.md` | 美国/全球 | 方法论教程 | 部分 | 是 | 是 | 是 | 中 | 摘取部分内容 |
| `why-service-inflation-is-sticky.md` | 美国/全球 | 市场机制 | 部分 | 是 | 是 | 是 | 中 | 仅作为延伸阅读 |
| `how-oil-price-transmits-to-assets.md` | 全球 | 市场机制 | 是 | 是 | 是 | 是 | 高 | 仅作为延伸阅读 |
| `what-financial-conditions-are.md` | 美国/全球 | 方法论教程 | 部分 | 是 | 是 | 是 | 高 | 多篇合并 |
| `how-to-read-pboc-policy-signals.md` | 中国 | 数据解读 | 是 | 是 | 是 | 是 | 高 | 摘取部分内容 |
| `fiscal-vs-monetary-policy-basics.md` | 中国/全球混合 | 方法论教程 | 部分 | 是 | 是 | 是 | 中 | 摘取部分内容 |
| `how-to-read-china-fiscal-policy.md` | 中国 | 数据解读 | 部分 | 是 | 是 | 是 | 高 | 多篇合并 |
| `case-study-2024-924-policy-pivot.md` | 中国 | 案例复盘 | 是 | 部分 | 是 | 是 | 高 | 仅作为延伸阅读 |
| `what-fed-hikes-and-cuts-really-change.md` | 美国/全球 | 市场机制 | 部分 | 是 | 是 | 是 | 高 | 摘取部分内容 |
| `how-to-read-fomc.md` | 美国 | 数据解读 | 部分 | 是 | 是 | 是 | 中 | 仅作为延伸阅读 |
| `why-the-dollar-rises.md` | 全球 | 市场机制 | 部分 | 是 | 是 | 是 | 高 | 摘取部分内容 |
| `real-rates-gold-bonds-dollar.md` | 美国/全球 | 市场机制 | 部分 | 是 | 是 | 是 | 高 | 仅作为延伸阅读 |
| `qt-vs-rate-hikes.md` | 美国 | 方法论教程 | 部分 | 是 | 是 | 是 | 中 | 仅作为延伸阅读 |
| `what-term-premium-is.md` | 美国/全球 | 方法论教程 | 部分 | 是 | 是 | 是 | 中 | 仅作为延伸阅读 |
| `why-yield-curve-matters.md` | 美国/全球 | 数据解读 | 部分 | 是 | 是 | 是 | 高 | 仅作为延伸阅读 |
| `what-credit-spreads-signal.md` | 美国/全球 | 数据解读 | 部分 | 是 | 是 | 是 | 高 | 仅作为延伸阅读 |
| `data-release-day-playbook.md` | 美国/全球 | 交易工作流 | 是 | 是 | 是 | 是 | 高 | 保留但继续隐藏 |
| `weekly-macro-tracking-workflow.md` | 中国/全球混合 | 研究工作流 | 部分 | 是 | 是 | 部分 | 中 | 保留但继续隐藏 |
| `monthly-macro-review-workflow.md` | 中国/全球混合 | 研究工作流 | 部分 | 是 | 是 | 是 | 高 | 摘取部分内容 |
| `how-to-build-a-macro-observation-board.md` | 美国/全球 | 研究工作流 | 部分 | 是 | 是 | 是 | 中 | 摘取部分内容 |
| `first-postmortem-for-a-macro-view.md` | 中国/全球混合 | 复盘方法论 | 部分 | 是 | 是 | 是 | 高 | 摘取部分内容 |
| `case-study-nonfarm-surprise-market-reaction.md` | 美国 | 案例复盘 | 是 | 是 | 是 | 是 | 高 | 保留但继续隐藏 |
| `how-to-read-nonfarm-payrolls.md` | 美国 | 数据解读 | 部分 | 是 | 是 | 是 | 高 | 仅作为延伸阅读 |
| `crisis-playbooks-three-scenarios.md` | 全球/中国 | 情景与交易预案 | 是 | 部分 | 是 | 是 | 高 | 保留但继续隐藏 |

## 四、旧宏观文档的处置

| 文件 | 可复用内容 | 冲突或缺口 | 建议动作 |
|---|---|---|---|
| `文档/宏观系统/宏观仪表盘_指标定义.md` | 中国增长、价格、信用、政策的候选指标和交叉验证关系 | 指标未形成点时数据契约；部分资产映射越过宏观层 | 摘取部分内容 |
| `文档/宏观系统/月度宏观复盘.md` | 证据、假设、复盘和记录结构 | 固定月频、目标波动示例、直接输出加/持/减及再平衡 | 保留但继续隐藏 |
| `文档/宏观系统/非农数据怎么看.md` | 数据修正、预期差和多指标交叉验证 | 美国就业专题，不是中国共同环境核心模块 | 仅作为延伸阅读 |
| `文档/宏观系统/原油价格怎么看_中国成品油与A股传导.md` | 外部成本冲击到中国价格的传导线索 | 进入行业和 A 股受益/受损映射 | 保留但继续隐藏 |
| `文档/宏观系统/期货观察清单_新手版.md` | 商品与风险事件的观察线索 | 工具和交易导向强，不属于宏观六模块规范 | 保留但继续隐藏 |
| `文档/宏观系统/居民消费支出分类总表.md` | 居民消费口径，可作为增长模块输入字典 | 不是系统判断方法；数据口径和来源仍需核验 | 仅作为延伸阅读 |
| `文档/宏观系统/需求市场系统_V1总目录.md` | 需求和场景拆解方法 | 属于行业/公司研究，不属于共同宏观环境 | 保留但继续隐藏 |
| `文档/宏观系统/需求-场景-市场卡模板.md` | 结构化记录意识 | 属于需求市场研究，不属于宏观层 | 保留但继续隐藏 |

## 五、明确不采用的旧做法

- 不沿用旧月度复盘中的固定产品波动目标、仓位比例或加/持/减动作；
- 不把单一 PMI、CPI、社融、利率、美元或油价直接变成共同风险边界；
- 不把美国数据教程平移为中国宏观结论；
- 不把央行表态等同于已经执行，更不等同于已经传导；
- 不使用缺少来源、口径、`data_as_of` 与 `available_at` 的数据支持当前状态；
- 不建立评分、模块权重、固定阈值或自动切换规则；
- 不新增单指标长文、美联储独立主线、美元独立主线或与六模块并列的新模块。

## 六、第一轮交付边界

第一轮正式完成：

1. 原地改造 `content/pages/macro-layer.md`；
2. 新建“中国增长周期怎么判断”；
3. 新建“中国流动性与信用怎么判断”。

只完成提纲：

1. 中国通胀与价格周期怎么判断；
2. 中国政策周期怎么记录和判断；
3. 全球外部环境如何约束中国资产；
4. 日历与事件风险怎样进入系统；
5. 六个模块如何形成共同风险边界。

提纲不作为实时状态页，不包含当前市场结论。旧文不删除，尚未完成系统化复核的内容继续隐藏。

## 七、合作伙伴阅读检查

第一轮三篇文章交给合作伙伴后，只验证以下问题：

- 能否用自己的话说明宏观层只负责共同环境和风险上限；
- 能否区分增长动能与资金/信用条件；
- 是否误以为任一模块会直接产生买卖或产品权重；
- 哪些段落过于学术、抽象或依赖作者口头补充；
- 哪些术语仍需要进入词汇表。

读者反馈进入问题记录后，再决定第二轮五篇文章的改造顺序。
