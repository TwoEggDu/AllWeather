# 恢复中国增长周期延伸阅读链接 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让“中国增长周期怎么判断”页面公开链接五篇已发布的基础文章，并保留用途边界。

**Architecture:** 修改增长周期页的延伸阅读区，并在五篇目标文章中分别用 `build.render: always` 覆盖 posts 区域的隐藏 cascade；不改文章正文或全局 posts 配置。使用仓库既有的 `/posts/<slug>/` 站内链接格式，再通过内容校验、Hugo 临时构建和生成文件检查完成闭环。

**Tech Stack:** Hugo、Markdown、Node.js 内容校验脚本、PowerShell

## Global Constraints

- 已发布文章不得包含 `[待补数据]`、`[图表占位]`、`[待补参考资料]`。
- `status` 与 `draft` 必须一致。
- 不伪造数据、图表、引用或来源 URL。
- 五篇文章只作基础或延伸阅读，不升级为现行状态、系统规则或交易指令。
- 不修改 `content/posts/_index.md`，其余旧文章继续隐藏。
- 不修改工作区中与本任务无关的文件。

---

### Task 1: 恢复五篇延伸阅读入口

**Files:**
- Modify: `content/pages/china-growth-cycle.md:141-155`
- Modify: `content/posts/growth-inflation-liquidity-basics.md`
- Modify: `content/posts/pmi-leading-risk-assets.md`
- Modify: `content/posts/how-to-read-china-pmi-official-vs-caixin.md`
- Modify: `content/posts/why-real-estate-matters-in-china.md`
- Modify: `content/posts/how-to-read-china-trade-data-and-rmb.md`
- Modify: `docs/superpowers/specs/2026-08-06-reopen-growth-extension-reading-design.md`
- Create: `docs/superpowers/plans/2026-08-06-reopen-growth-extension-reading.md`

**Interfaces:**
- Consumes: 五篇目标文章既有的 `slug` 与 `status: published` / `draft: false` 状态。
- Produces: `/china-growth-cycle/` 页面上的五个 `/posts/<slug>/` 站内链接、五个可生成的文章页面和一段用途边界说明。

- [x] **Step 1: 运行链接前置检查并确认当前状态失败**

```powershell
$source = Get-Content 'content/pages/china-growth-cycle.md' -Raw -Encoding UTF8
$requiredLinks = @(
  '/posts/growth-inflation-liquidity-basics/',
  '/posts/pmi-leading-risk-assets/',
  '/posts/how-to-read-china-pmi-official-vs-caixin/',
  '/posts/why-real-estate-matters-in-china/',
  '/posts/how-to-read-china-trade-data-and-rmb/'
)
$missing = $requiredLinks | Where-Object { -not $source.Contains($_) }
if ($missing.Count -gt 0) { throw "缺少链接: $($missing -join ', ')" }
```

Expected: FAIL，列出五个缺少的链接。

- [x] **Step 2: 开放目标页面并替换延伸阅读条目**

在五篇目标文章的 front matter 中分别增加：

```yaml
build:
  render: always
```

不要修改 `content/posts/_index.md`，避免开放整个旧文章区。

把原有“继续隐藏”段落替换为：

```markdown
以下公开文章可作为概念、数据解读和机制背景的延伸阅读：

- [增长、通胀、流动性：投资最基础的三条线](/posts/growth-inflation-liquidity-basics/)
- [PMI 为什么经常领先于部分风险资产](/posts/pmi-leading-risk-assets/)
- [中国 PMI 怎么看：官方 PMI 和财新 PMI 有什么区别](/posts/how-to-read-china-pmi-official-vs-caixin/)
- [为什么房地产在中国宏观里如此重要](/posts/why-real-estate-matters-in-china/)
- [中国贸易数据和汇率之间的关系怎么看](/posts/how-to-read-china-trade-data-and-rmb/)

这些文章不是蜗牛全天候的现行状态、系统规则或交易指令；其中的数据口径、结论和资产表达仍需单独核验。
```

- [x] **Step 3: 运行链接与目标文件检查**

```powershell
$source = Get-Content 'content/pages/china-growth-cycle.md' -Raw -Encoding UTF8
$slugs = @(
  'growth-inflation-liquidity-basics',
  'pmi-leading-risk-assets',
  'how-to-read-china-pmi-official-vs-caixin',
  'why-real-estate-matters-in-china',
  'how-to-read-china-trade-data-and-rmb'
)
foreach ($slug in $slugs) {
  if (-not $source.Contains("/posts/$slug/")) { throw "页面缺少链接: $slug" }
  if (-not (Test-Path "content/posts/$slug.md")) { throw "目标文章不存在: $slug" }
  $post = Get-Content "content/posts/$slug.md" -Raw -Encoding UTF8
  if (-not $post.Contains('status: published')) { throw "目标文章不是 published: $slug" }
  if (-not $post.Contains('draft: false')) { throw "目标文章仍是草稿: $slug" }
  if ($post -notmatch '(?m)^build:\r?\n  render: always$') { throw "目标文章没有渲染覆盖: $slug" }
}
if ($source.Contains('目前继续隐藏，不提供公开链接')) { throw '仍存在过时隐藏说明' }
```

Expected: PASS，无输出。

- [x] **Step 4: 运行内容校验**

Run: `node scripts/validate-content.mjs`

Expected: `内容校验通过`。

- [x] **Step 5: 构建站点并检查生成页面**

```powershell
& 'C:\Users\IGG\AppData\Local\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe' --gc --minify --cleanDestinationDir --buildFuture --destination '.tmp/reopen-growth-links-public'
$paths = @(
  '.tmp/reopen-growth-links-public/china-growth-cycle/index.html',
  '.tmp/reopen-growth-links-public/posts/growth-inflation-liquidity-basics/index.html',
  '.tmp/reopen-growth-links-public/posts/pmi-leading-risk-assets/index.html',
  '.tmp/reopen-growth-links-public/posts/how-to-read-china-pmi-official-vs-caixin/index.html',
  '.tmp/reopen-growth-links-public/posts/why-real-estate-matters-in-china/index.html',
  '.tmp/reopen-growth-links-public/posts/how-to-read-china-trade-data-and-rmb/index.html'
)
$missing = $paths | Where-Object { -not (Test-Path $_) }
if ($missing.Count -gt 0) { throw "构建缺少页面: $($missing -join ', ')" }
$renderedPosts = Get-ChildItem '.tmp/reopen-growth-links-public/posts' -Recurse -Filter index.html
if ($renderedPosts.Count -ne 5) { throw "误开放其他 posts 页面，实际生成: $($renderedPosts.Count)" }
```

Expected: Hugo 构建成功，六个目标 HTML 全部存在，并且 posts 区域恰好只生成这五篇文章。

- [x] **Step 6: 检查差异并提交明确文件**

```powershell
$targets = @(
  'content/pages/china-growth-cycle.md',
  'content/posts/growth-inflation-liquidity-basics.md',
  'content/posts/pmi-leading-risk-assets.md',
  'content/posts/how-to-read-china-pmi-official-vs-caixin.md',
  'content/posts/why-real-estate-matters-in-china.md',
  'content/posts/how-to-read-china-trade-data-and-rmb.md',
  'docs/superpowers/specs/2026-08-06-reopen-growth-extension-reading-design.md',
  'docs/superpowers/plans/2026-08-06-reopen-growth-extension-reading.md'
)
git diff --check -- $targets
git add -- $targets
git commit -m "docs: 恢复增长周期延伸阅读链接"
```

Expected: 只提交上述八个文件；其他未跟踪文件保持不变。
