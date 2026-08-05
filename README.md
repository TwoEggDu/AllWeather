# 蜗牛全天候

蜗牛全天候是一套面向合作伙伴、可解释、可约束、可复盘并可持续优化的资产配置方法论与模拟系统。

当前仓库首先作为方法论展示站使用：让合作伙伴理解六层系统怎样从宏观环境走到产品风险预算、执行与复盘，问题怎样被发现和分类，以及系统怎样验证、保留或回滚一项修改。

> 当前阶段：M0 公开设计与范围收敛。
>
> 本项目仅用于学习、研究和模拟，不构成投资建议或收益承诺。

## 第一阶段回答的问题

1. 当前宏观环境是什么状态？
2. 当前允许承担多少风险？
3. 六个资产桶分别承担什么功能？
4. 三类市场信号说明了什么？
5. 中波产品如何把共同判断变成风险约束？
6. 什么时候模拟调整、保持不动或暂停？
7. 每次决策之后如何复盘和优化系统？

## 公开页面

- `/`：项目首页与最小闭环总览
- `/design/`：投资方法论总纲、六层职责与单向约束
- `/system-loop/`：系统运转、问题分类、修改验证与回滚
- `/macro-layer/`：宏观环境层字段与共同风险边界
- `/middle-risk-product/`：蜗牛全天候·中波母产品概念卡
- `/partner-review/`：合作伙伴独立阅读与反馈问题清单
- `/scope/`：第一阶段范围、禁止事项和完成标准
- `/roadmap/`：M0—M4 小闭环路线图
- `/status/`：当前状态、阻塞点和唯一优先事项
- `/decision-log/`：系统级设计决定及重新评估条件
- `/about/`：项目背景与目标读者
- `/disclaimer/`：项目成熟度、数据边界与风险提示

## 旧内容处理

原有宏观文章、专题、词汇表和栏目继续保留在仓库中，但当前不参与生产构建，也不代表蜗牛全天候的现行规则、参数或投资结论。

旧内容未来可以逐篇恢复。恢复前需要确认：

- 它服务六层中的哪一层；
- 是否符合当前范围；
- 数据、引用和时点是否仍可核验；
- 是否会被读者误解为现行建议。

## 本地运行

如果 Hugo 已在 `PATH`：

```powershell
hugo server -D
```

当前机器的已知 Hugo 路径：

```powershell
& 'C:\Users\IGG\AppData\Local\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe' server -D
```

生产构建：

```powershell
node scripts/validate-content.mjs
& 'C:\Users\IGG\AppData\Local\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe' --gc --minify --cleanDestinationDir
```

构建结果位于 `public/`。该目录是生成物，不提交到 Git。

## 内容原则

- 缺数据、来源不明或历史不足时，明确记录未知，不补造数字；
- 具体参数必须说明数据、口径、时点、基准和验证方法；
- 宏观层只输出共同环境和风险边界，不直接生成产品权重或买卖指令；
- 产品风险预算层负责把共同边界映射为中波产品约束；
- 当前不做个股、高频、实盘连接或自动下单；
- 旧文章中的示例比例不能自动升级为现行参数。
