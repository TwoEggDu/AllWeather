# 蜗牛量化

蜗牛量化是一个面向所有读者和研究者的开放中国市场投研知识库。

网站以公开、可追溯信息为基础，聚焦：

- 中国宏观与产业政策
- 国家资本与地方产业资金
- 行业与企业基本面
- 市场资金与交易结构
- 全球变量对中国资产的影响
- 热点跟踪、证伪与研究复盘

核心研究链：

> 政策方向 → 国家与社会资本 → 行业基本面 → 市场定价 → 全球反馈 → 验证与复盘

本站不以荐股、喊单、仓位建议和短期涨跌预测为主要产出。

---

## 仓库结构

### Hugo 站点

- `content/`：公开页面、文章和术语库
- `layouts/`：Hugo 页面和组件模板
- `static/`：CSS、JavaScript 和静态资源
- `data/topics.yaml`：六个研究领域及兼容映射
- `archetypes/`：Hugo 新文章原型
- `templates/`：完整研究草稿模板

### 研究和系统文档

- `文档/`：顶层设计、路线图、宏观系统、组合和风险管理文档
- `模板/`：检查清单、决策记录和实验模板
- `docs/`：内容发布和审计规则
- `scripts/`：内容校验工具

主要设计文档：

- `文档/宏观系统/投研体系顶层设计.md`
- `文档/宏观系统/开放投研内容架构与改造清单.md`
- `文档/路线图/05_开放投研网站改造计划.md`

---

## 站点页面

- `/`：开放投研首页、最新文章和六个研究入口
- `/macro-index/`：入门路径与研究工作路径
- `/topics/`：六个研究领域总览
- `/posts/`：按研究领域和标签筛选全部文章
- `/glossary/`：宏观和市场术语库
- `/writing-template/`：研究文章写作结构
- `/about/`：开放研究使命、边界、使用方式和内容纪律
- `/disclaimer/`：统一免责声明

---

## 内容结构

每篇文章至少使用以下 front matter：

- `title`
- `slug`
- `date`
- `summary`
- `category`
- `tags`
- `level`
- `status`
- `draft`

新文章优先使用六个研究领域之一作为 `category`。旧文章在迁移期间保留原分类，站点使用标签和旧分类映射到新的研究领域，不需要一次性修改全部文章。

详细写作结构见：

- `archetypes/posts.md`
- `templates/research-post-template.mdx`
- `content/pages/writing-template.md`

---

## 本地运行

### 内容校验

```bash
node scripts/validate-content.mjs
```

### 本地预览

```bash
hugo server -D
```

### 生产构建

```bash
hugo --gc --minify
```

构建结果默认输出到 `public/`。

---

## 发布纪律

- 草稿必须使用 `status: draft` 和 `draft: true`。
- 已发布文章必须使用 `status: published` 和 `draft: false`。
- 已发布文章不得保留未解决的原始占位标记。
- 不伪造数据、图表、引用和来源链接。
- 依赖未获取数据、图表或已验证资料才能成立的文章必须保持草稿。

详细规则见 `docs/editorial-workflow.md`。
