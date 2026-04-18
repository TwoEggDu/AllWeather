#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import importlib.util
import json
import math
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / 'tools' / 'output'
DEFAULT_TRANSCRIPT_DIR = ROOT / 'tools' / 'transcripts'
DEFAULT_AUDIO_DIR = ROOT / 'tools' / 'audio_cache'
DEFAULT_MODEL = ROOT / 'vendor' / 'whisper.cpp' / 'models' / 'ggml-base.bin'
DEFAULT_WHISPER = ROOT / 'vendor' / 'whisper.cpp' / 'build' / 'bin' / 'whisper-cli.exe'
TRANSCRIBE_MODULE_PATH = Path(__file__).with_name('bilibili_transcribe.py')
DEFAULT_TIMEOUT = 20
USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/133.0.0.0 Safari/537.36'
)
STOP_TOKENS = {
    '一个', '一些', '不是', '什么', '今天', '他们', '但是', '其实', '因为', '如果', '就是',
    '已经', '开始', '很多', '怎么', '所以', '所有', '我们', '时候', '最后', '没有', '然后',
    '现在', '这个', '这种', '那个', '还是', '通过', '进行', '需要', '非常',
}
TRANSCRIPT_LINE_RE = re.compile(r'^(?P<stamp>(?:\d{1,2}:)?\d{1,2}:\d{2})\s+(?P<text>.+)$')
_TRANSCRIBE_MODULE: Any | None = None


@dataclass
class SubtitleLine:
    text: str
    start: float | None = None
    end: float | None = None


@dataclass
class TranscribeOptions:
    enabled: bool = True
    transcript_dir: Path = DEFAULT_TRANSCRIPT_DIR
    audio_dir: Path = DEFAULT_AUDIO_DIR
    model: Path = DEFAULT_MODEL
    whisper_cli: Path = DEFAULT_WHISPER
    ffmpeg: str = ''
    language: str = 'zh'
    threads: int = 4
    keep_audio: bool = False


@dataclass
class TranscriptResult:
    source_label: str = ''
    source_text: str = ''
    lines: list[SubtitleLine] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    transcript_path: Path | None = None


@dataclass
class VideoSummary:
    source_url: str
    canonical_url: str
    bvid: str
    title: str
    author: str = ''
    description: str = ''
    published_at: str = ''
    tags: list[str] = field(default_factory=list)
    stats: dict[str, int] = field(default_factory=dict)
    source_label: str = '简介'
    source_text: str = ''
    subtitles: list[SubtitleLine] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    transcript_path: str = ''


def fetch_text(url: str, *, referer: str | None = None, timeout: int = DEFAULT_TIMEOUT) -> tuple[str, str]:
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': 'text/html,application/json;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip',
    }
    if referer:
        headers['Referer'] = referer
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read()
        if response.headers.get('Content-Encoding') == 'gzip':
            body = gzip.decompress(body)
        text = body.decode(response.headers.get_content_charset() or 'utf-8', errors='replace')
        return text, response.geturl()


def fetch_json(url: str, *, referer: str | None = None, timeout: int = DEFAULT_TIMEOUT) -> Any:
    text, _ = fetch_text(url, referer=referer, timeout=timeout)
    return json.loads(text)


def extract_json_assignment(document: str, variable_name: str) -> Any | None:
    match = re.search(re.escape(variable_name) + r'\s*=', document)
    if not match:
        return None
    index = match.end()
    while index < len(document) and document[index].isspace():
        index += 1
    if index >= len(document) or document[index] not in '{[':
        return None
    stack = [document[index]]
    quote: str | None = None
    escaped = False
    for end_index in range(index + 1, len(document)):
        ch = document[end_index]
        if quote:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == quote:
                quote = None
            continue
        if ch in {"'", '"'}:
            quote = ch
            continue
        if ch in '{[':
            stack.append(ch)
        elif ch in '}]':
            opener = stack.pop()
            if (opener, ch) not in {('{', '}'), ('[', ']')}:
                raise ValueError('页面内嵌 JSON 不完整')
            if not stack:
                try:
                    return json.loads(document[index : end_index + 1])
                except json.JSONDecodeError:
                    return None
    return None


def format_timestamp(seconds: float | None) -> str:
    if seconds is None:
        return '--:--'
    total = max(0, int(seconds))
    minute, second = divmod(total, 60)
    hour, minute = divmod(minute, 60)
    if hour:
        return f'{hour:02d}:{minute:02d}:{second:02d}'
    return f'{minute:02d}:{second:02d}'


def parse_clock(value: str) -> float | None:
    parts = value.split(':')
    try:
        numbers = [int(part) for part in parts]
    except ValueError:
        return None
    if len(numbers) == 2:
        minute, second = numbers
        return float(minute * 60 + second)
    if len(numbers) == 3:
        hour, minute, second = numbers
        return float(hour * 3600 + minute * 60 + second)
    return None


def format_datetime(timestamp: Any) -> str:
    if not isinstance(timestamp, (int, float)):
        return ''
    return datetime.fromtimestamp(timestamp).astimezone().strftime('%Y-%m-%d %H:%M')


def format_count(value: int) -> str:
    if value >= 100_000_000:
        return f'{value / 100_000_000:.1f}亿'
    if value >= 10_000:
        return f'{value / 10_000:.1f}万'
    return str(value)


def sanitize_filename(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', value)
    value = re.sub(r'\s+', ' ', value).strip(' .')
    return value or 'bilibili_summary'


def normalize_source_text(text: str) -> str:
    return '\n'.join(line.strip() for line in text.splitlines() if line.strip())


def text_lines_to_subtitles(text: str) -> list[SubtitleLine]:
    lines: list[SubtitleLine] = []
    for raw_line in text.splitlines():
        cleaned = re.sub(r'\s+', ' ', raw_line).strip()
        if not cleaned:
            continue
        match = TRANSCRIPT_LINE_RE.match(cleaned)
        if match:
            stamp = parse_clock(match.group('stamp'))
            content = match.group('text').strip()
        else:
            stamp = None
            content = cleaned
        if content:
            lines.append(SubtitleLine(text=content, start=stamp))
    return lines


def pick_best_subtitle(subtitles: Sequence[dict[str, Any]]) -> dict[str, Any] | None:
    if not subtitles:
        return None
    for language in ('zh-CN', 'zh-Hans', 'ai-zh', 'zh', 'zh-TW'):
        for subtitle in subtitles:
            if subtitle.get('lan') == language:
                return subtitle
    return subtitles[0]


def ensure_absolute_url(url: str, base_url: str) -> str:
    if not url:
        return url
    if url.startswith('//'):
        return 'https:' + url
    return urllib.parse.urljoin(base_url, url)


def parse_subtitle_payload(payload: dict[str, Any]) -> list[SubtitleLine]:
    lines: list[SubtitleLine] = []
    for item in payload.get('body') or []:
        if not isinstance(item, dict):
            continue
        text = re.sub(r'\s+', ' ', str(item.get('content') or '')).strip()
        if not text:
            continue
        lines.append(
            SubtitleLine(
                text=text,
                start=float(item.get('from')) if isinstance(item.get('from'), (int, float)) else None,
                end=float(item.get('to')) if isinstance(item.get('to'), (int, float)) else None,
            )
        )
    return lines


def fetch_subtitles(playinfo: dict[str, Any], bvid: str, cid: Any, page_url: str, timeout: int) -> tuple[list[SubtitleLine], str]:
    subtitle_info = (playinfo.get('data') or {}).get('subtitle') or {}
    subtitles = subtitle_info.get('subtitles') or []
    selected = pick_best_subtitle(subtitles)
    if selected:
        subtitle_url = ensure_absolute_url(str(selected.get('subtitle_url') or ''), page_url)
        payload = fetch_json(subtitle_url, referer=page_url, timeout=timeout)
        return parse_subtitle_payload(payload), str(selected.get('lan_doc') or selected.get('lan') or '字幕')
    if not bvid or not cid:
        return [], ''
    api_url = 'https://api.bilibili.com/x/player/v2?' + urllib.parse.urlencode({'bvid': bvid, 'cid': cid})
    payload = fetch_json(api_url, referer=page_url, timeout=timeout)
    subtitles = (((payload.get('data') or {}).get('subtitle') or {}).get('subtitles') or [])
    selected = pick_best_subtitle(subtitles)
    if not selected:
        return [], ''
    subtitle_url = ensure_absolute_url(str(selected.get('subtitle_url') or ''), page_url)
    subtitle_payload = fetch_json(subtitle_url, referer=page_url, timeout=timeout)
    return parse_subtitle_payload(subtitle_payload), str(selected.get('lan_doc') or selected.get('lan') or '字幕')


def load_transcribe_module() -> Any | None:
    global _TRANSCRIBE_MODULE
    if _TRANSCRIBE_MODULE is not None:
        return _TRANSCRIBE_MODULE
    if not TRANSCRIBE_MODULE_PATH.exists():
        return None
    spec = importlib.util.spec_from_file_location('bilibili_transcribe_runtime', TRANSCRIBE_MODULE_PATH)
    if not spec or not spec.loader:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    _TRANSCRIBE_MODULE = module
    return module


def create_transcript(url: str, transcribe: TranscribeOptions) -> Path:
    transcribe_module = load_transcribe_module()
    if transcribe_module is None:
        raise FileNotFoundError('没有找到 bilibili_transcribe.py。')

    ffmpeg = Path(transcribe.ffmpeg) if transcribe.ffmpeg else transcribe_module.find_ffmpeg()
    whisper_cli = transcribe.whisper_cli
    model = transcribe.model

    if not whisper_cli.exists():
        raise FileNotFoundError(f'没有找到 whisper-cli: {whisper_cli}')
    if not model.exists():
        raise FileNotFoundError(f'没有找到模型文件: {model}')
    if not ffmpeg.exists():
        raise FileNotFoundError(f'没有找到 ffmpeg: {ffmpeg}')

    meta = transcribe_module.inspect_video(url)
    stem = sanitize_filename(meta.bvid)
    audio_path = transcribe.audio_dir / f'{stem}.m4s'
    wav_path = transcribe.audio_dir / f'{stem}.wav'
    transcript_prefix = transcribe.transcript_dir / stem

    transcribe_module.download_audio(meta, audio_path)
    transcribe_module.convert_to_wav(ffmpeg, audio_path, wav_path)
    transcript_path = transcribe_module.transcribe_audio(
        whisper_cli,
        model,
        wav_path,
        transcript_prefix,
        language=transcribe.language,
        threads=transcribe.threads,
    )

    meta_path = transcribe.transcript_dir / f'{stem}.meta.json'
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(
        json.dumps(
            {
                'source_url': meta.url,
                'canonical_url': meta.canonical_url,
                'bvid': meta.bvid,
                'title': meta.title,
                'author': meta.author,
                'duration_seconds': meta.duration_seconds,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding='utf-8',
    )

    if not transcribe.keep_audio:
        audio_path.unlink(missing_ok=True)
        wav_path.unlink(missing_ok=True)
    return transcript_path


def maybe_load_or_create_transcript(url: str, bvid: str, *, transcribe: TranscribeOptions) -> TranscriptResult:
    if not transcribe.enabled:
        return TranscriptResult()

    stem = sanitize_filename(bvid or 'bilibili-video')
    transcript_path = transcribe.transcript_dir / f'{stem}.txt'
    if transcript_path.exists():
        text = normalize_source_text(transcript_path.read_text(encoding='utf-8', errors='replace'))
        if text:
            return TranscriptResult(
                source_label='自动转写(缓存)',
                source_text=text,
                lines=text_lines_to_subtitles(text),
                warnings=['未找到公开字幕，已复用本地逐字稿。逐字稿可能包含语音识别误差。'],
                transcript_path=transcript_path,
            )

    try:
        transcript_path = create_transcript(url, transcribe)
        text = normalize_source_text(transcript_path.read_text(encoding='utf-8', errors='replace'))
        if not text:
            raise RuntimeError('转写输出为空。')
        return TranscriptResult(
            source_label='自动转写(whisper)',
            source_text=text,
            lines=text_lines_to_subtitles(text),
            warnings=['未找到公开字幕，已改用本地音频转写。逐字稿可能包含语音识别误差。'],
            transcript_path=transcript_path,
        )
    except Exception as error:
        return TranscriptResult(warnings=[f'未找到公开字幕，本地转写也失败：{error}'])


def summarize_text(text: str, subtitles: Sequence[SubtitleLine]) -> str:
    sentences = split_sentences(text)
    if not sentences:
        return '## 总览\n\n没有提取到足够文本，暂时无法生成可靠摘要。'
    overview = ' '.join(select_sentences(sentences[: min(len(sentences), 12)], 2))
    key_points = select_sentences(sentences, 4)
    outline = build_outline(subtitles if subtitles else None, text)
    lines = ['## 总览', '', overview, '', '## 核心要点', '']
    for sentence in key_points:
        lines.append(f'- {sentence}')
    if outline:
        lines.extend(['', '## 内容脉络', ''])
        lines.extend(outline)
    return '\n'.join(lines)


def split_sentences(text: str) -> list[str]:
    pieces: list[str] = []
    buffer: list[str] = []
    for ch in text:
        buffer.append(ch)
        if ch in '。！？!?；;\n':
            sentence = re.sub(r'\s+', ' ', ''.join(buffer)).strip()
            if sentence:
                pieces.append(sentence)
            buffer = []
    if buffer:
        sentence = re.sub(r'\s+', ' ', ''.join(buffer)).strip()
        if sentence:
            pieces.append(sentence)
    merged: list[str] = []
    for sentence in pieces:
        if merged and len(sentence) < 10:
            merged[-1] = f'{merged[-1]} {sentence}'.strip()
        else:
            merged.append(sentence)
    return merged


def sentence_tokens(sentence: str) -> set[str]:
    tokens: set[str] = set()
    for run in re.findall(r'[\u4e00-\u9fff]{2,}', sentence):
        for size in (2, 3):
            for index in range(max(0, len(run) - size + 1)):
                token = run[index : index + size]
                if token not in STOP_TOKENS and len(set(token)) > 1:
                    tokens.add(token)
    for token in re.findall(r'[A-Za-z]{3,}', sentence.lower()):
        tokens.add(token)
    return tokens


def select_sentences(sentences: Sequence[str], limit: int) -> list[str]:
    token_sets = [sentence_tokens(sentence) for sentence in sentences]
    freq: Counter[str] = Counter()
    for token_set in token_sets:
        freq.update(token_set)
    ranked: list[tuple[int, float]] = []
    for index, sentence in enumerate(sentences):
        tokens = token_sets[index]
        score = sum(min(freq[token], 4) for token in tokens) / math.sqrt(len(tokens) or 1)
        if index == 0:
            score += 0.4
        if index < 3:
            score += 0.15
        if 18 <= len(sentence) <= 120:
            score += 0.1
        ranked.append((index, score))
    ranked.sort(key=lambda item: item[1], reverse=True)
    chosen: list[int] = []
    chosen_tokens: list[set[str]] = []
    for index, _ in ranked:
        tokens = token_sets[index]
        if any(tokens and len(tokens & existing) / max(len(tokens | existing), 1) > 0.6 for existing in chosen_tokens):
            continue
        chosen.append(index)
        chosen_tokens.append(tokens)
        if len(chosen) >= limit:
            break
    return [sentences[index] for index in sorted(chosen)] if chosen else list(sentences[:limit])


def build_outline(subtitles: Sequence[SubtitleLine] | None, text: str) -> list[str]:
    if subtitles:
        bullets: list[str] = []
        chunk: list[SubtitleLine] = []
        size = 0
        for line in subtitles:
            chunk.append(line)
            size += len(line.text)
            if size >= 220:
                bullets.append(render_chunk(chunk))
                chunk, size = [], 0
        if chunk:
            bullets.append(render_chunk(chunk))
        return bullets[:6]
    paragraphs = [part.strip() for part in text.splitlines() if len(part.strip()) >= 18]
    return [f'- {paragraph[:90]}' for paragraph in paragraphs[:6]]


def render_chunk(chunk: Sequence[SubtitleLine]) -> str:
    text = ' '.join(item.text for item in chunk)
    sentences = split_sentences(text)
    gist = ' '.join(select_sentences(sentences, 2)) if sentences else text[:80]
    prefix = f'{format_timestamp(chunk[0].start)} ' if chunk[0].start is not None else ''
    return f'- {prefix}{gist}'.rstrip()


def format_stats(stats: dict[str, int]) -> str:
    labels = {'view': '播放', 'like': '点赞', 'coin': '投币', 'favorite': '收藏', 'share': '分享', 'reply': '评论'}
    parts = [f"{labels[key]} {format_count(value)}" for key, value in stats.items() if key in labels]
    return ' | '.join(parts)


def fetch_video_summary(
    url: str,
    *,
    timeout: int = DEFAULT_TIMEOUT,
    transcribe: TranscribeOptions | None = None,
) -> VideoSummary:
    transcribe = transcribe or TranscribeOptions()
    html_text, final_url = fetch_text(url, timeout=timeout)
    state = extract_json_assignment(html_text, 'window.__INITIAL_STATE__') or {}
    playinfo = extract_json_assignment(html_text, 'window.__playinfo__') or {}
    video_data = state.get('videoData') or {}
    if not video_data:
        raise RuntimeError('没有在页面里识别到视频信息。当前版本只支持公开 B 站视频页。')

    page_number = int((urllib.parse.parse_qs(urllib.parse.urlparse(final_url).query).get('p') or [1])[0])
    pages = video_data.get('pages') or []
    current_page = pages[page_number - 1] if page_number - 1 < len(pages) else {}
    bvid = str(video_data.get('bvid') or '')
    cid = current_page.get('cid') or video_data.get('cid')
    description = re.sub(r'\s+', ' ', str(video_data.get('desc') or '')).strip()
    tags = [str(tag.get('tag_name')) for tag in state.get('tags') or [] if isinstance(tag, dict) and tag.get('tag_name')]
    stats = {key: int(value) for key, value in (video_data.get('stat') or {}).items() if isinstance(value, (int, float))}
    warnings: list[str] = []
    subtitles: list[SubtitleLine] = []
    source_label = '简介'
    source_text = ''
    transcript_path = ''

    try:
        subtitles, language = fetch_subtitles(playinfo, bvid, cid, final_url, timeout)
        if subtitles:
            source_label = f'字幕({language})'
    except Exception as error:
        warnings.append(f'字幕提取失败：{error}')

    if subtitles:
        source_text = '\n'.join(f'{format_timestamp(line.start)} {line.text}' for line in subtitles)
    else:
        transcript_result = maybe_load_or_create_transcript(final_url, bvid, transcribe=transcribe)
        warnings.extend(transcript_result.warnings)
        if transcript_result.source_text:
            source_label = transcript_result.source_label
            source_text = transcript_result.source_text
            subtitles = transcript_result.lines
            transcript_path = str(transcript_result.transcript_path) if transcript_result.transcript_path else ''
        else:
            source_text = '\n'.join(part for part in [video_data.get('title'), description, ' / '.join(tags)] if part)
            warnings.append('未找到可用字幕或逐字稿，摘要会退化为基于标题、简介和标签的整理。')

    title = str(video_data.get('title') or bvid or 'Bilibili 视频')
    part_title = str(current_page.get('part') or '')
    full_title = f'{title} - {part_title}' if part_title and part_title != title else title
    owner = video_data.get('owner') or state.get('upData') or {}
    return VideoSummary(
        source_url=url,
        canonical_url=final_url,
        bvid=bvid or 'bilibili-video',
        title=full_title,
        author=str(owner.get('name') or ''),
        description=description,
        published_at=format_datetime(video_data.get('pubdate')),
        tags=tags,
        stats=stats,
        source_label=source_label,
        source_text=source_text,
        subtitles=subtitles,
        warnings=warnings,
        transcript_path=transcript_path,
    )


def render_markdown(summary: VideoSummary) -> str:
    lines = [f'# {summary.title}', '']
    lines.append(f'- 来源链接：{summary.canonical_url}')
    lines.append(f'- BV 号：{summary.bvid}')
    lines.append(f'- 提取来源：{summary.source_label}')
    if summary.transcript_path:
        lines.append(f'- 逐字稿文件：{summary.transcript_path}')
    if summary.author:
        lines.append(f'- UP 主：{summary.author}')
    if summary.published_at:
        lines.append(f'- 发布时间：{summary.published_at}')
    if summary.tags:
        lines.append('- 标签：' + ' / '.join(summary.tags))
    if summary.stats:
        lines.append('- 互动数据：' + format_stats(summary.stats))
    if summary.warnings:
        lines.append('- 提示：' + '；'.join(summary.warnings))
    lines.extend(['', summarize_text(summary.source_text, summary.subtitles), ''])
    return '\n'.join(lines)


def build_transcribe_options(args: argparse.Namespace) -> TranscribeOptions:
    return TranscribeOptions(
        enabled=not args.skip_transcribe,
        transcript_dir=Path(args.transcript_dir),
        audio_dir=Path(args.audio_dir),
        model=Path(args.model),
        whisper_cli=Path(args.whisper_cli),
        ffmpeg=args.ffmpeg.strip(),
        language=args.language,
        threads=max(1, args.threads),
        keep_audio=args.keep_audio,
    )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='把 B 站视频整理成 Markdown 摘要；没有字幕时会优先回退到本地音频转写。')
    parser.add_argument('url', help='B 站视频链接，支持 BV 链接和 b23.tv 跳转链接。')
    parser.add_argument('--output-dir', default=str(DEFAULT_OUTPUT_DIR), help='摘要输出目录，默认 tools/output')
    parser.add_argument('--output-file', help='直接指定摘要输出文件路径')
    parser.add_argument('--save-source-text', action='store_true', help='额外保存原始字幕或逐字稿到 .source.txt')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help='网络请求超时秒数')
    parser.add_argument('--skip-transcribe', action='store_true', help='没有公开字幕时，跳过本地音频转写')
    parser.add_argument('--transcript-dir', default=str(DEFAULT_TRANSCRIPT_DIR), help='逐字稿缓存目录')
    parser.add_argument('--audio-dir', default=str(DEFAULT_AUDIO_DIR), help='转写时的音频缓存目录')
    parser.add_argument('--model', default=str(DEFAULT_MODEL), help='whisper.cpp 模型路径')
    parser.add_argument('--whisper-cli', default=str(DEFAULT_WHISPER), help='whisper-cli.exe 路径')
    parser.add_argument('--ffmpeg', default='', help='ffmpeg.exe 路径，不传则先搜索系统 PATH，再搜索 vendor/ffmpeg')
    parser.add_argument('--language', default='zh', help='本地转写语言，默认 zh')
    parser.add_argument('--threads', type=int, default=4, help='本地转写线程数')
    parser.add_argument('--keep-audio', action='store_true', help='执行本地转写时保留音频缓存')
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        summary = fetch_video_summary(args.url, timeout=args.timeout, transcribe=build_transcribe_options(args))
        markdown = render_markdown(summary)
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = Path(args.output_file) if args.output_file else output_dir / f"{sanitize_filename(summary.bvid)}_{sanitize_filename(summary.title)[:60]}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding='utf-8')
        if args.save_source_text and summary.source_text:
            output_path.with_suffix('.source.txt').write_text(summary.source_text, encoding='utf-8')
        print(f'摘要已生成：{output_path}')
        return 0
    except urllib.error.URLError as error:
        print(f'请求页面失败：{error}', file=sys.stderr)
        return 1
    except Exception as error:
        print(f'生成摘要失败：{error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
