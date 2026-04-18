# B站视频内容总结工具

这个脚本会把公开可访问的 Bilibili 视频页整理成一份 Markdown 文本摘要。

## 目前支持的范围

- B 站视频页
- `b23.tv` 短链跳转后的视频页
- 优先读取公开字幕
- 没有字幕时，自动回退到本地音频转写
- 优先复用 `tools/transcripts/` 里已经存在的逐字稿，避免重复转写

## 运行方式

在仓库根目录执行：

```powershell
python tools/bilibili_summarizer.py "https://www.bilibili.com/video/BVxxxxxxxxxx"
```

如果想同时保留原始逐字稿文本：

```powershell
python tools/bilibili_summarizer.py "https://www.bilibili.com/video/BVxxxxxxxxxx" `
  --save-source-text
```

默认输出目录：

```text
tools/output/
```

## 常用参数

```powershell
python tools/bilibili_summarizer.py "https://www.bilibili.com/video/BVxxxxxxxxxx" `
  --save-source-text `
  --threads 4 `
  --output-dir "tools/output"
```

参数说明：

- `--output-dir`
  指定摘要输出目录。
- `--output-file`
  直接指定摘要文件路径。
- `--save-source-text`
  额外保存原始字幕或逐字稿到 `.source.txt`。
- `--timeout`
  指定页面请求超时秒数。
- `--skip-transcribe`
  没有公开字幕时，不调用本地音频转写。
- `--transcript-dir`
  指定逐字稿缓存目录。
- `--audio-dir`
  指定转写阶段的音频缓存目录。
- `--model`
  指定 `whisper.cpp` 模型路径。
- `--whisper-cli`
  指定 `whisper-cli.exe` 路径。
- `--ffmpeg`
  手动指定 `ffmpeg.exe` 路径；不传则先搜索系统 `PATH`，再搜索 `vendor/ffmpeg/`。
- `--language`
  本地转写语言，默认 `zh`。
- `--threads`
  本地转写线程数。
- `--keep-audio`
  转写结束后保留中间音频文件。

## 输出内容

Markdown 里会包含：

- 原始链接
- BV 号
- 提取来源（公开字幕 / 自动转写）
- 逐字稿文件路径（如果走了转写）
- UP 主 / 发布时间 / 标签 / 互动数据
- `## 总览`
- `## 核心要点`
- `## 内容脉络`

## 本地转写依赖

自动转写依赖以下本地文件：

- `vendor/whisper.cpp/build/bin/whisper-cli.exe`
- `vendor/whisper.cpp/models/ggml-base.bin`
- 系统 `PATH` 中可执行的 `ffmpeg`，或本地 `vendor/ffmpeg/**/ffmpeg.exe`

如果这些文件不存在，脚本仍会继续运行，但无字幕视频会退回到基于标题、简介、标签的整理。

## 局限

- 当前版本只做视频页，没有覆盖专栏、动态、直播回放。
- 会员可见、登录后可见的内容默认拿不到。
- 本地音频转写能显著提升无字幕视频的可读性，但仍然会有语音识别误差。
