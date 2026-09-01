# AllWeather 文章能力补全最终报告

> 执行日期：2026-09-01
>
> 授权方案：方案 B——有限范围例外
>
> 当前阶段：M0 仍在进行中；M1 未正式开始

## 1. 治理决定是什么

已在 `content/pages/decision-log.md` 追加 D-015“有限补全五项投资研究知识能力”，把本次工作记录为一次**有限、可验证、可回滚的知识能力补全例外**。

D-015 固定了三篇新建、两篇原地重构、首页单一区块和核心页最少互引的范围，并保留以下边界：六层架构、M0 退出条件、M1 未启动、Roadmap 阶段定义、不接实盘、不批量公开旧 posts、不把宏观、盈利、估值或资金状态直接变成交易信号。

同时在 `content/pages/status.md` 做了最小状态更新，明确“内容能力补全不等于 M0 验收完成”。

## 2. 为什么允许本次有限例外

审计确认的五项缺口不是文章数量问题，而是现有六层之间的解释和验证断点：普通读者能看到宏观与六层职责，却缺少“宏观如何进入企业盈利”“好基本面为什么未必是好价格”“市场行为如何解释”“中国为何不能机械套用投资时钟”以及“完整研究为何仍可能不操作”的连续路径。

本次例外只补这些已经确认的断点；它不证明方法有效，也不扩大系统权限。若出现职责混淆、内容重复、交易建议化、第二套宏观系统、独立择时系统或首页路径复杂化，D-015 允许撤回入口并重新隐藏文章。

## 3. 新建的 3 篇文章

1. `content/pages/corporate-earnings-cycle.md`：《企业盈利周期：宏观改善如何真正变成利润》。从政策、信用、需求走到订单、收入、利润、现金流和股东回报，用于验证宏观和产业叙事。
2. `content/pages/market-flows-trend-crowding.md`：《资金到底在交易什么：趋势、拥挤与风险偏好》。解释 ETF 份额、申赎、成交、融资、市场宽度、集中度和拥挤度，但不增加 Signal Layer 正式输出。
3. `content/pages/complete-investment-decision.md`：《一次完整投资判断是怎样形成的？》。使用明确标注的弱复苏 Synthetic Scenario 走完六层，最终因估值赔率和产品风险预算约束得出“暂不调整”。

## 4. 原地重构的 2 篇文章

1. `content/posts/how-to-value-a-stock.md`：保留 slug `how-to-value-a-stock`，重构为《好公司为什么也会亏钱：估值与预期差》，增加 `build.render: always`。
2. `content/posts/four-phases-of-economic-cycle.md`：保留 slug `four-phases-of-economic-cycle`，重构为《为什么“美林投资时钟”不能直接照搬到中国？》，增加 `build.render: always`。

两篇都只逐篇开放；`content/posts/_index.md` 的全局隐藏规则没有修改。

## 5. 为什么没有新增 5 个文件

估值和四阶段经济周期已经存在同主题旧文。若另建新文件，会形成重复主题、旧链接碎片和两套相互竞争的解释。原地重构既保留历史 slug，也让旧的危险交易表达从生产内容中消失。只有盈利、资金与完整案例缺少可复用的单一职责页面，因此新建三篇。

## 6. 删除或修改的危险表达

估值旧文中的以下内容已删除：

- 固定 WACC、永续增长率、PE/PB/PEG 和历史分位阈值；
- “低于悲观估值可以买”“小仓位试水”“高于乐观估值不要买”等直接动作；
- 具体每股目标价、统一安全边际和无来源的行业溢价/折价经验数；
- 把估值区间机械映射成买卖结论的示例。

投资时钟旧文中的机械资产方向也已重构：不再把复苏、过热、滞胀、衰退直接对应成资产赢家或轮动动作；四象限现在只承担宏观环境识别，必须继续经过中国信用、政策、地产、盈利、估值、市场状态、产品风险预算和执行条件。

新内容中的“可以买”“必涨”“目标价”等字样只出现在明确的禁止或否定语境中，不构成建议。

## 7. 建立的交叉引用

- `china-growth-cycle` → 企业盈利周期；
- `asset-layer` → 估值与预期差；
- `signal-layer` → 资金、趋势与拥挤度，并重申正式输出不变；
- `design` → 中国版投资时钟入口、完整教学案例；
- `execution-layer`、`review-layer` → 完整教学案例；
- 五篇主题文章按“增长 → 盈利 → 估值 → 资金 → 六层 → 完整判断”建立手工上一站/下一站和正文互引。

为通过生产站全局链接门禁，还把 5 篇既有公开文章中指向隐藏旧 posts 或 glossary 的 16 个断链替换为当前公开、职责相符的页面。没有因此公开任何旧文章。

## 8. 首页学习路径如何变化

`layouts/index.html` 新增单个 `#start-here` 区块，顺序为：

```text
中国版投资时钟入口
  → 理解中国宏观
  → 企业盈利周期
  → 估值与预期差
  → 资金、趋势与拥挤
  → 六层 AllWeather
  → 一次完整投资判断
```

原主导航、五条系统入口和合作伙伴六层阅读顺序均未替换。区块复用现有 `.method-grid`；该网格使用 `auto-fit/minmax(240px, 1fr)`，并继续受站点 `max-width: 820px` 移动端布局规则约束。仓库没有独立的移动端自动化视觉测试。

## 9. 六层架构有没有变化

**没有变化。** 盈利和估值是跨层研究与验证工具，资金与拥挤度是 Signal Layer 的解释背景，中国版投资时钟是认知入口，完整案例是教学材料。它们都不是新层。

Signal Layer 的正式输出仍为趋势、相对强弱、波动与回撤风险；没有新增“资金流信号”或“中国六因子系统”。

## 10. M0 状态有没有变化

**没有变化。** 当前仍处于 M0，真实合作伙伴独立阅读仍未完成，M0 未关闭；M1 未正式开始；没有宣布 `M0 Complete`、`M1 Started`、`Architecture Complete` 或新 Milestone 完成。

## 11. 当前还剩哪些内容缺口

本次五项审计缺口已经形成可公开阅读的知识路径，但“内容存在”不等于“表达已被独立读者理解”。仍缺：

- 真实合作伙伴的独立阅读记录、误解、反例、证据缺口和处置结果；
- 对五篇文章是否造成职责混淆或首页认知负担的外部反馈；
- 现有宏观核心页中此前已经登记、但被 D-015 明确排除的后续工作；
- 真实数据、点时证据、可复现回放和产品规则参数。

因此不应继续用新增文章替代 M0 验收。

## 12. 哪些问题应通过数据或验证解决

以下问题已经不是继续写解释文章能够解决的：

- 宏观判断在当时是否使用了真实可得而非事后修订的数据；
- 信用、订单、盈利、估值和拥挤度在真实时点能否被稳定采集和版本化；
- 预期差采用什么可审计代理，口径是否跨期一致；
- 盈利改善是否进入现金流，行业利润池是否真的迁移；
- Signal Layer 状态与回撤、风险预算约束之间是否有可复现证据；
- 中波产品的风险参数、暂停条件和模拟结果是否有效；
- `SNAPSHOT_NOT_REPRODUCIBLE` 能否在前向保存不可变快照后被重新验证。

这些应回到 M0 独立阅读与后续 M1 数据契约、前向快照和点时验证，不应再靠扩写内容填充。

## 13. 十项 Quality Gate

| Gate | 结果 | 证据 |
|---|---|---|
| Architecture | PASS | 五项能力均声明所属职责；没有第七层 |
| Duplication | PASS | 两篇同主题旧文原地重构；三篇新文职责唯一 |
| Evidence | PASS | 关键机制引用统计局、人民银行、上交所、IMF、NBER 等来源；推断显式标注 |
| Point-in-Time | PASS | 案例明确为 Synthetic Scenario；保留 `SNAPSHOT_NOT_REPRODUCIBLE` 边界 |
| Investment Advice | PASS | 无目标价、统一买卖阈值、荐股、仓位建议或收益承诺 |
| Expectation | PASS | 明确区分基本面、Price In、预期差和当前赔率 |
| China Fit | PASS | 投资时钟显式处理信用、政策、地产、地方财政、居民资产负债表与盈利验证 |
| Signal Boundary | PASS | 资金和拥挤度不成为第四类信号，也不独立产生动作 |
| Beginner | PASS | 采用顺序路径、四层问题、表格、最小卡片和反例解释 |
| System | PASS | 首页、六层核心页与五篇主题形成可追踪互引，完整案例走完六层 |

## 14. 构建、lint、链接与测试结果

2026-09-01 最终新鲜验证：

| 检查 | 结果 |
|---|---|
| 内容 lint：`node scripts/validate-content.mjs` | PASS；扫描 261 个 Markdown，222 个声明 published |
| Hugo Extended 生产构建 | PASS；Hugo v0.157.0 extended，59 Pages，4 Static files |
| 五个目标页与首页输出 | PASS；6/6 |
| 全站生成 HTML 内部链接 | PASS；0 broken links |
| duplicate slug | PASS；206 个 slug，0 重复 |
| front matter | PASS；五篇均 `status: published`、`draft: false`；两篇重构逐篇 `render: always` |
| 原始占位符 | PASS；五篇无 `[待补数据]`、`[图表占位]`、`[待补参考资料]` |
| 生产 posts 范围 | PASS；仍为 7 篇，没有批量开放隐藏旧文；用户 `profit-pool` 草稿未公开 |
| 项目测试：`python -m pytest -q` | PASS；5 passed |
| `git diff --check` | PASS；无空白错误；仅提示 Windows 工作区未来可能进行 LF/CRLF 转换 |
| 移动端基础布局 | PASS（静态规则）; 新区块复用响应式网格；仓库无专用视觉回归测试 |

## 15. 修改文件清单

### 治理与交付记录

- `ARTICLE_GAP_AUDIT.md`
- `ARTICLE_EXPANSION_PLAN.md`
- `ARTICLE_EXPANSION_REPORT.md`
- `content/pages/decision-log.md`
- `content/pages/status.md`

### 三篇新文章

- `content/pages/corporate-earnings-cycle.md`
- `content/pages/market-flows-trend-crowding.md`
- `content/pages/complete-investment-decision.md`

### 两篇原地重构

- `content/posts/how-to-value-a-stock.md`
- `content/posts/four-phases-of-economic-cycle.md`

### 系统集成

- `layouts/index.html`
- `content/pages/china-growth-cycle.md`
- `content/pages/asset-layer.md`
- `content/pages/signal-layer.md`
- `content/pages/design.md`
- `content/pages/execution-layer.md`
- `content/pages/review-layer.md`

### 生产断链修复

- `layouts/posts/single.html`
- `content/posts/growth-inflation-liquidity-basics.md`
- `content/posts/how-to-read-china-pmi-official-vs-caixin.md`
- `content/posts/how-to-read-china-trade-data-and-rmb.md`
- `content/posts/pmi-leading-risk-assets.md`
- `content/posts/why-real-estate-matters-in-china.md`

工作区原有未跟踪的 `profit-pool` 草稿、`tools/fund_bot`、`产品合集.zip` 和 `产品合集/` 未纳入本次修改，也未删除。

## 16. 建议 commit message

```text
docs: 补全五项投资研究知识能力
```

## 下一阶段决定

**下一阶段不应自动继续写文章。** 证据指向先回到 M0：让真实合作伙伴沿新路径独立阅读，记录误解、反例和职责冲突，并决定是否触发 D-015 回滚条件。只有 M0 关闭后，才按既有 Roadmap 评估 M1 数据基础设施，优先保存真实 `available_at`、`recorded_at`、不可变原始快照和版本，而不是用更多文章替代验证。
