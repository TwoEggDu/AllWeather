---
title: 写作模板
url: /writing-template/
summary: 研究型文章的推荐结构，以及如何在 Hugo 中复用模板开始新文章。
---

## 推荐结构

研究型文章建议优先回答这六个问题：

1. 这篇文章要回答的问题是什么
2. 事实 / 数据是什么
3. 机制链条是什么
4. 市场如何交易这个逻辑
5. 反例 / 风险是什么
6. 未来如何验证和复盘

## 仓库里的模板文件

这个仓库同时提供两种模板：

- `archetypes/posts.md`
  这是 Hugo 真正会使用的文章原型文件，适合直接用命令生成新文。
- `templates/research-post-template.mdx`
  这是一个更接近写作草稿习惯的 MDX 模板文件，适合先起草结构和占位内容。

## 推荐使用方式

如果你想直接在 Hugo 内容目录里生成新文，优先使用：

```powershell
hugo new content posts/your-slug.md
```

如果你想先起草，再手动整理 front matter，可以复制 `templates/research-post-template.mdx` 的内容到 `content/posts/` 下的新文件中，再改成 `.md`。

## 备注

站点会自动在文章页底部渲染免责声明，因此不需要在每篇文章里重复手工粘贴相同声明。
