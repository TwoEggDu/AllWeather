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

async function main() {
  const repoRoot = process.cwd();
  const postsDir = path.join(repoRoot, "content", "posts");
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
