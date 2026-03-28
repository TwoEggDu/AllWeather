# 宏观全天候研究日志

这是一个面向中文读者的 Hugo blog，用来长期记录以下主题的学习与研究：

- 全球宏观
- 宏观对冲思维
- 跨资产研究
- 数据解读
- 交易表达
- 复盘纠错

它是一个公开研究日志，不是荐股站，不展示虚假收益，也不制造 FOMO。

网站的核心方法只有一句话：

> 理解经济，观察市场，复盘错误。

---

## 这个仓库现在包含两层内容

### 1. Hugo 站点层

这部分用于公开发布、长期维护和本地运行：

- `hugo.toml`
- `content/`
- `layouts/`
- `static/`
- `archetypes/`
- `templates/`

### 2. 中文研究底稿层

这部分保留原有的内部研究资料与工作模板：

- `文档/`
- `模板/`

可以把它理解为：

- `content/` 负责对外可读的文章与页面
- `文档/` 负责更细的底稿、框架、清单与实验记录

---

## 当前已实现的页面

- `/`
  首页，包含 hero、最新文章、五个栏目入口、方法论说明和免责声明入口
- `/about`
  说明为什么写这个 blog、学习目标和写作原则
- `/posts`
  全部文章列表，支持按栏目和标签筛选
- `/posts/[slug]`
  文章详情页，包含目录、元信息、统一免责声明和前后导航
- `/topics`
  五个栏目总览与文章计数
- `/glossary`
  基础术语词汇表
- `/disclaimer`
  统一免责声明页面
- `/writing-template`
  写作模板说明页

---

## 内容结构

```text
content/
  _index.md
  posts/
  glossary/
  topics/
  pages/

archetypes/
  posts.md

templates/
  research-post-template.mdx
```

### 文章 front matter 约定

每篇文章至少包含：

- `title`
- `slug`
- `date`
- `summary`
- `category`
- `tags`
- `level`
- `status`
- `draft`

推荐栏目：

- `宏观基础`
- `市场机制`
- `数据解读`
- `交易表达`
- `复盘纠错`

推荐难度：

- `beginner`
- `intermediate`

推荐状态：

- `draft`
- `published`

---

## 初始内容

站点已包含 8 篇 starter posts：

1. 我为什么要写一个宏观投资 blog
2. 增长、通胀、流动性：投资最基础的三条线
3. 为什么债券价格和收益率是反着走的
4. CPI 变化如何影响股市、债市和美元
5. PMI 为什么经常领先于部分风险资产
6. 美联储加息/降息，真正影响市场的是什么
7. 油价上涨会通过哪些路径传导到资产价格
8. 同一个宏观观点，为什么可以用不同资产来表达

词汇表已包含 20 个基础术语，包括：

- GDP
- CPI
- PPI
- PMI
- 非农
- 利率
- 收益率曲线
- 实际利率
- 美元指数
- 风险偏好
- 信用利差
- 杠杆
- 波动率
- 回撤
- 久期
- 流动性
- 通胀预期
- 名义利率
- 国债
- 大宗商品

---

## 本地运行

### 1. 本地预览

如果你的系统已经能直接调用 `hugo`：

```powershell
hugo server -D
```

如果本机 Hugo 不在 `PATH`，可直接使用当前机器上的已知路径：

```powershell
& 'C:\Users\IGG\AppData\Local\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe' server -D
```

### 2. 生产构建

```powershell
& 'C:\Users\IGG\AppData\Local\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe' --gc --minify
```

构建结果输出到：

- `public/`

---

## 如何继续写文章

### 方式 1：用 Hugo archetype 生成新文

```powershell
hugo new content posts/your-slug.md
```

这会自动使用：

- `archetypes/posts.md`

### 方式 2：复制 MDX 写作模板

可直接复制：

- `templates/research-post-template.mdx`

把内容改写后保存到：

- `content/posts/your-slug.md`

说明：

- 仓库提供 `.mdx` 模板，是为了起草更顺手
- 站点实际渲染仍以 Hugo 的 `.md` 内容文件为主

---

## 研究型文章推荐结构

每篇文章建议优先回答这六个问题：

1. 这篇文章要回答的问题是什么
2. 事实 / 数据是什么
3. 机制链条是什么
4. 市场如何交易这个逻辑
5. 反例 / 风险是什么
6. 未来如何验证和复盘

如果暂时没有真实数据或图表，请明确标注：

- 草稿阶段可以保留原始占位符：
  - `[待补数据]`
  - `[图表占位]`
  - `[待补参考资料]`
- 已发布文章不得保留这些原始占位符
- 缺数据时，应改写成不依赖具体数值也能成立的正文，或降级回草稿
- 缺图时，应改写成没有图也成立的说明，或写成明确的“后续可补图”提示
- 缺参考资料时，应写成“后续可补官方来源类别”，不要伪造具体引用

---

## 发布前检查

每次准备把文章从草稿改成已发布前，至少做两步：

1. 运行内容校验脚本：

```powershell
node scripts/validate-content.mjs
```

2. 运行 Hugo 构建：

```powershell
& 'C:\Users\IGG\AppData\Local\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe' --gc --minify
```

详细编辑规则见：

- `docs/editorial-workflow.md`
- `docs/content-audit.md`

---

## 内容约束

- 默认语言为简体中文
- 不使用“保证收益”“稳定盈利”等表述
- 不伪造市场数据、收益、引用或来源
- 站点页脚和文章页统一显示免责声明

统一免责声明为：

> 本文仅用于学习与研究，不构成任何投资建议。

---

## 设计与维护原则

- 风格偏研究机构与高质量编辑部，而不是营销落地页
- 以内容为中心，避免不必要的依赖和复杂交互
- 优先保证中文排版、移动端和桌面端阅读体验
- 保持文件式内容系统，便于长期维护和版本管理

---

## 后续可以继续扩展的方向

- 增加更多栏目文章
- 补充图表与数据来源
- 增加 taxonomy 页面与栏目归档页
- 为词汇表增加交叉引用
- 补充部署配置

---

## 备注

本仓库仍包含原有的中文研究文档体系。如果你想做更细的底稿、策略清单或实验记录，建议继续放在：

- `文档/`
- `模板/`

如果你想发布一篇适合公开阅读的文章，则优先写入：

- `content/posts/`
