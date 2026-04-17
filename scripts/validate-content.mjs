import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const requiredFields = [
  "title",
  "slug",
  "date",
  "summary",
  "category",
  "tags",
  "level",
  "status",
  "draft",
];

const placeholderTokens = ["[待补数据]", "[图表占位]", "[待补参考资料]"];

function parseFrontmatter(source, filePath) {
  const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!match) {
    return {
      data: {},
      body: source,
      issues: [`缺少 frontmatter：${filePath}`],
    };
  }

  const data = {};
  let currentListKey = null;

  for (const rawLine of match[1].split(/\r?\n/)) {
    const line = rawLine.trimEnd();

    if (!line.trim()) {
      continue;
    }

    const keyMatch = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (keyMatch) {
      const [, key, rawValue] = keyMatch;
      currentListKey = null;

      if (rawValue === "") {
        data[key] = [];
        currentListKey = key;
      } else {
        data[key] = rawValue.trim();
      }

      continue;
    }

    const listMatch = line.match(/^\s*-\s*(.+)$/);
    if (listMatch && currentListKey) {
      if (!Array.isArray(data[currentListKey])) {
        data[currentListKey] = [];
      }

      data[currentListKey].push(listMatch[1].trim());
    }
  }

  return {
    data,
    body: source.slice(match[0].length),
    issues: [],
  };
}

function normalizeScalar(value) {
  if (typeof value !== "string") {
    return "";
  }

  return value.replace(/^['"]|['"]$/g, "").trim().toLowerCase();
}

function normalizePath(value) {
  return value.replace(/\\/g, "/");
}

function normalizeUrl(value) {
  if (typeof value !== "string") {
    return "";
  }

  const normalized = value.trim();
  if (!normalized) {
    return "";
  }

  const withLeadingSlash = normalized.startsWith("/") ? normalized : `/${normalized}`;
  return withLeadingSlash.endsWith("/") ? withLeadingSlash : `${withLeadingSlash}/`;
}

function stripLinkSuffix(value) {
  return value.split("#", 1)[0].split("?", 1)[0];
}

function collectMarkdownLinks(body) {
  const pattern = /\]\((?!https?:\/\/|mailto:|#)([^)]+)\)/g;
  const links = [];

  for (const line of body.split(/\r?\n/)) {
    let match;
    while ((match = pattern.exec(line)) !== null) {
      links.push(match[1].trim());
    }
    pattern.lastIndex = 0;
  }

  return links;
}

function resolveOutputUrl(relativePath, data) {
  const normalizedPath = normalizePath(relativePath);
  const normalizedDir = path.posix.dirname(normalizedPath);
  const fileName = path.posix.basename(normalizedPath);

  if (typeof data.url === "string" && data.url.trim()) {
    return normalizeUrl(data.url);
  }

  if (fileName === "_index.md") {
    if (normalizedDir === ".") {
      return "/";
    }

    return normalizeUrl(`/${normalizedDir}/`);
  }

  const section = normalizedDir === "." ? "" : normalizedDir;
  const baseName = path.posix.basename(normalizedPath, path.posix.extname(normalizedPath));
  const slug = typeof data.slug === "string" && data.slug.trim() ? data.slug.trim() : baseName;

  if (!section) {
    return normalizeUrl(`/${slug}/`);
  }

  return normalizeUrl(`/${section}/${slug}/`);
}

async function collectContentFiles(dir) {
  const files = [];
  const entries = await readdir(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      files.push(...(await collectContentFiles(fullPath)));
      continue;
    }

    if (entry.isFile() && entry.name.endsWith(".md")) {
      files.push(fullPath);
    }
  }

  return files;
}

async function main() {
  const repoRoot = process.cwd();
  const postsDir = path.join(repoRoot, "content", "posts");
  const contentDir = path.join(repoRoot, "content");
  const entries = await readdir(postsDir, { withFileTypes: true });
  const postFiles = entries
    .filter((entry) => entry.isFile() && entry.name.endsWith(".md") && entry.name !== "_index.md")
    .map((entry) => entry.name)
    .sort();

  const allIssues = [];
  let publishedCount = 0;

  for (const fileName of postFiles) {
    const relativePath = path.join("content", "posts", fileName);
    const fullPath = path.join(postsDir, fileName);
    const source = await readFile(fullPath, "utf8");
    const { data, body, issues } = parseFrontmatter(source, relativePath);

    for (const field of requiredFields) {
      if (!(field in data)) {
        issues.push(`缺少 frontmatter 字段：${field}`);
        continue;
      }

      if (field === "tags") {
        if (!Array.isArray(data.tags) || data.tags.length === 0) {
          issues.push("frontmatter 字段 tags 不能为空");
        }

        continue;
      }

      if (String(data[field]).trim() === "") {
        issues.push(`frontmatter 字段 ${field} 不能为空`);
      }
    }

    const status = normalizeScalar(data.status);
    const draft = normalizeScalar(data.draft);

    if (status && !["draft", "published"].includes(status)) {
      issues.push(`status 只能是 draft 或 published，当前为：${data.status}`);
    }

    if (draft && !["true", "false"].includes(draft)) {
      issues.push(`draft 只能是 true 或 false，当前为：${data.draft}`);
    }

    if (status === "published" && draft !== "false") {
      issues.push(`status/draft 不一致：published 文章必须是 draft: false，当前为 draft: ${data.draft}`);
    }

    if (status === "draft" && draft !== "true") {
      issues.push(`status/draft 不一致：draft 文章必须是 draft: true，当前为 draft: ${data.draft}`);
    }

    if (status === "published") {
      publishedCount += 1;

      for (const token of placeholderTokens) {
        if (body.includes(token)) {
          issues.push(`已发布文章仍包含原始占位符：${token}`);
        }
      }
    }

    if (issues.length > 0) {
      allIssues.push({ fileName: relativePath, issues });
    }
  }

  const contentFiles = await collectContentFiles(contentDir);
  const validInternalTargets = new Set();

  for (const fullPath of contentFiles) {
    const relativeFromRepo = normalizePath(path.relative(repoRoot, fullPath));
    const relativeFromContent = normalizePath(path.relative(contentDir, fullPath));
    const source = await readFile(fullPath, "utf8");
    const { data, issues } = parseFrontmatter(source, relativeFromRepo);

    if (issues.length > 0) {
      continue;
    }

    validInternalTargets.add(resolveOutputUrl(relativeFromContent, data));

    if (Array.isArray(data.aliases)) {
      for (const alias of data.aliases) {
        const normalizedAlias = normalizeUrl(alias);
        if (normalizedAlias) {
          validInternalTargets.add(normalizedAlias);
        }
      }
    }
  }

  for (const fullPath of contentFiles) {
    const relativeFromRepo = normalizePath(path.relative(repoRoot, fullPath));
    const source = await readFile(fullPath, "utf8");
    const { body, issues } = parseFrontmatter(source, relativeFromRepo);

    if (issues.length > 0) {
      continue;
    }

    const linkIssues = [];
    for (const link of collectMarkdownLinks(body)) {
      if (!link.startsWith("/")) {
        continue;
      }

      const target = normalizeUrl(stripLinkSuffix(link));
      if (!target || validInternalTargets.has(target)) {
        continue;
      }

      linkIssues.push(`内部链接指向不存在的页面：${link}`);
    }

    if (linkIssues.length > 0) {
      allIssues.push({ fileName: relativeFromRepo, issues: linkIssues });
    }
  }

  if (allIssues.length > 0) {
    console.error(`内容校验失败：共检查 ${postFiles.length} 篇文章，发现 ${allIssues.length} 篇存在问题。`);
    console.error("");

    for (const item of allIssues) {
      console.error(`- ${item.fileName}`);
      for (const issue of item.issues) {
        console.error(`  - ${issue}`);
      }
    }

    process.exitCode = 1;
    return;
  }

  console.log(`内容校验通过：共检查 ${postFiles.length} 篇文章，其中 ${publishedCount} 篇为已发布状态。`);
}

main().catch((error) => {
  console.error("内容校验执行失败：");
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
