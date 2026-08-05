# 蜗牛全天候

蜗牛全天候是一套基于宏观环境、资产分层、市场信号、执行纪律与决策复盘的个人投资研究和模拟框架。

当前仓库首先作为公开设计展示站使用：让读者快速理解项目为什么存在、五层系统怎样协作、六个资产桶分别承担什么角色、第一阶段明确不做什么，以及项目准备怎样验证。

> 当前阶段：M0 公开设计与范围收敛。
>
> 本项目仅用于学习、研究和模拟，不构成投资建议或收益承诺。

## 第一阶段回答的问题

1. 当前宏观环境是什么状态？
2. 当前允许承担多少风险？
3. 可以配置哪些资产大类？
4. 哪些资产桶相对较强或较弱？
5. 应以什么频率检查和调整？
6. 每次决策之后如何复盘？

## 公开页面

- `/`：项目首页与最小闭环总览
- `/design/`：五层系统、六个资产桶和执行节奏
- `/scope/`：第一阶段范围、禁止事项和完成标准
- `/roadmap/`：M0—M4 小闭环路线图
- `/status/`：当前状态、阻塞点和唯一优先事项
- `/decision-log/`：系统级设计决定及重新评估条件
- `/about/`：项目背景与目标读者
- `/disclaimer/`：项目成熟度、数据边界与风险提示

## 旧内容处理

原有宏观文章、专题、词汇表和栏目继续保留在仓库中，但当前不参与生产构建，也不代表蜗牛全天候的现行规则、参数或投资结论。

旧内容未来可以逐篇恢复。恢复前需要确认：

- 它属于五层中的哪一层；
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
- 宏观层只管理风险预算，不直接生成买卖指令；
- 当前不做个股、高频、实盘连接或自动下单；
- 旧文章中的示例比例不能自动升级为现行参数。
