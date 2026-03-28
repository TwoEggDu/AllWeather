# 内容编辑与发布规则

这份文档约束的是 `content/posts/*.md` 的发布纪律。目标只有一个：公开页只能出现可独立阅读的文章，半成品只能停留在草稿区。

## 状态规则

- 草稿文章必须同时满足：
  - `status: draft`
  - `draft: true`
- 已发布文章必须同时满足：
  - `status: published`
  - `draft: false`

不要出现下面这种矛盾状态：

- `status: published` 但 `draft: true`
- `status: draft` 但 `draft: false`

## 占位符规则

草稿阶段允许使用原始占位符：

- `[待补数据]`
- `[图表占位]`
- `[待补参考资料]`

已发布文章禁止出现这些原始占位符字符串。

## 缺数据时怎么处理

- 如果文章可以用概念解释、机制链条和验证路径说清楚，就把原始占位符改写成正文
- 如果文章必须依赖具体数据才能成立，而当前仓库里没有可靠数据来源，就把文章降级回草稿
- 不要为了“凑完整”去编造数字、回测、统计结论或历史案例

## 缺图时怎么处理

- 如果图只是辅助理解，就删除原始占位符，并把周边文字改写成没有图也能成立
- 如果图对论证非常关键，就把文章保留为草稿，并明确写清“后续可补图：……”
- 不要伪造图表数据、图表标题或图表来源

## 缺参考资料时怎么处理

- 可以写“后续可补官方来源类别”，例如：FRED、BLS、BEA、Federal Reserve、ISM、EIA、CME FedWatch
- 不要伪造具体链接、发布日期、论文题目或报告名称
- 只要正文里还保留原始字符串 `[待补参考资料]`，文章就不能发布

## 什么时候应该降级回草稿

满足任意一条，就应该把文章从已发布降回草稿：

- 出现原始占位符
- 结构仍然依赖未来补的数据或图表才能成立
- 关键机制链条写不完整
- 读者容易把它误读为“已经有完备证据支撑”，但实际没有
- 修改后 `status` 与 `draft` 不一致

## 发布前检查

每次准备发布前，按这个顺序跑：

1. 内容校验

```powershell
node scripts/validate-content.mjs
```

2. 站点构建

```powershell
& 'C:\Users\IGG\AppData\Local\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe' --gc --minify
```

3. 本地预览复查

```powershell
& 'C:\Users\IGG\AppData\Local\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe' server -D
```

## 自动保护

仓库已经补了两层自动保护：

- `scripts/validate-content.mjs`
  - 校验 frontmatter 必填字段
  - 校验 `status` 与 `draft` 一致
  - 校验已发布文章不含原始占位符
- Hugo 模板层的公开过滤
  - 首页、文章列表、栏目统计只统计已发布文章
  - 文章详情页在生产构建中拒绝渲染非公开文章
  - RSS 与 sitemap 只输出符合公开条件的文章
