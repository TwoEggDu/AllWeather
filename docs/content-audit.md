# 内容审计记录

本次审计范围：`content/posts/*.md`（排除 `_index.md`），共 13 篇文章。

审计目标：

- 已发布文章不再包含原始占位符
- `status` 与 `draft` 保持语义一致
- 文章在不伪造数据、图表、引用的前提下可以独立阅读

审计结果摘要：

- 保留 `published`：13 篇
- 改回 `draft`：0 篇
- 原始占位符清理后剩余：0

| 文件名 | 标题 | 当前状态 | 修复前含占位符 | 本次动作 | 剩余待补项 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| `bond-price-and-yield.md` | 为什么债券价格和收益率是反着走的 | published | 是（图表） | 保留 published；补成“后续可补图”说明 | 可选补图：固定票息债券价格变化示意图 | 图表只是辅助理解，不影响正文成立 |
| `cpi-and-assets.md` | CPI 变化如何影响股市、债市和美元 | published | 是（数据、参考资料） | 保留 published；补充实证观察方向与官方来源类别 | 可补 CPI 分项与资产联动复盘 | 文章核心是传导逻辑，不依赖具体数值 |
| `first-postmortem-for-a-macro-view.md` | 第一次完整复盘：我如何用一篇文章记录一个宏观判断的前提、表达和验证 | published | 是（参考资料） | 保留 published；补成方法论资料入口说明 | 可补固定复盘模板示例 | 方法论文章可独立成立 |
| `growth-inflation-liquidity-basics.md` | 增长、通胀、流动性：投资最基础的三条线 | published | 是（图表、参考资料） | 保留 published；补成示意图说明和来源类别 | 可补三条线到资产映射图 | 属于框架入门文，不需要先有数据表才能发布 |
| `how-oil-price-transmits-to-assets.md` | 油价上涨会通过哪些路径传导到资产价格 | published | 是（图表） | 保留 published；补成清晰的后续图示说明 | 可补油价冲击传导示意图 | 图示用于帮助初学者整理路径 |
| `how-to-read-nonfarm-payrolls.md` | 非农数据怎么看：为什么同样是就业强，市场反应有时完全相反 | published | 是（数据、图表、参考资料） | 保留 published；补充实证观察框架和官方来源类别 | 可补数据日联动案例 | 现在已能独立解释“市场在交易什么” |
| `inflation-expectations-vs-realized-inflation.md` | 通胀预期和实际通胀有什么区别 | published | 是（数据、图表、参考资料） | 保留 published；补充对照框架和官方来源类别 | 可补预期与实际通胀对照图 | 概念边界已清晰，可公开阅读 |
| `one-view-many-trade-expressions.md` | 同一个宏观观点，为什么可以用不同资产来表达 | published | 是（参考资料） | 保留 published；补成后续数据入口说明 | 可补不同表达方式的复盘表 | 文章重点是映射逻辑与风险预算 |
| `pmi-leading-risk-assets.md` | PMI 为什么经常领先于部分风险资产 | published | 是（图表） | 保留 published；补成示意图说明 | 可补 PMI 与新订单分项示意图 | 图表并非论证核心 |
| `real-rates-gold-bonds-dollar.md` | 实际利率到底是什么，为什么它同时影响黄金、债券和美元 | published | 是（数据、图表、参考资料） | 保留 published；补充联动观察框架和官方来源类别 | 可补名义利率/通胀预期/实际利率关系图 | 文章主题是变量关系，不依赖伪造历史样本 |
| `what-fed-hikes-and-cuts-really-change.md` | 美联储加息/降息，真正影响市场的是什么 | published | 是（数据、参考资料） | 保留 published；补充政策前后联动观察方向和官方来源类别 | 可补会议前后资产反应复盘 | 已能独立解释“动作”和“路径”的区别 |
| `why-write-a-macro-blog.md` | 我为什么要写一个宏观投资 blog | published | 是（数据、图表、参考资料） | 保留 published；把占位符改写成明确的写作纪律说明 | 可补后续写作复盘案例 | 这是站点定位文，不需要外部数据才成立 |
| `why-yield-curve-matters.md` | 收益率曲线为什么重要，倒挂到底在提示什么 | published | 是（数据、图表、参考资料） | 保留 published；补充实证观察方向和官方来源类别 | 可补利差与曲线形态示意图 | 文章当前已能独立解释曲线的含义与局限 |
