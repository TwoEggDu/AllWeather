#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIO_DIR = ROOT / 'tools' / 'audio_cache'
DEFAULT_OUTPUT_DIR = ROOT / 'tools' / 'transcripts'
DEFAULT_MODEL = ROOT / 'vendor' / 'whisper.cpp' / 'models' / 'ggml-base.bin'
DEFAULT_WHISPER = ROOT / 'vendor' / 'whisper.cpp' / 'build' / 'bin' / 'whisper-cli.exe'
USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/133.0.0.0 Safari/537.36'
)


@dataclass
class VideoAudio:
    url: str
    canonical_url: str
    bvid: str
    title: str
    author: str
    duration_seconds: float
    audio_url: str


def find_ffmpeg() -> Path:
    for name in ('ffmpeg.exe', 'ffmpeg'):
        resolved = shutil.which(name)
        if resolved:
            return Path(resolved)

    candidates = sorted((ROOT / 'vendor' / 'ffmpeg').glob('**/ffmpeg.exe'))
    if candidates:
        return candidates[0]

    raise FileNotFoundError('没有找到 ffmpeg.exe，请先安装 ffmpeg，或通过 --ffmpeg 指定路径。')


def fetch_text(url: str, *, referer: str | None = None, timeout: int = 20) -> tuple[str, str]:
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
            stack.pop()
            if not stack:
                return json.loads(document[index : end_index + 1])
    return None


def pick_best_audio(playinfo: dict[str, Any]) -> str:
    audio_tracks = ((playinfo.get('data') or {}).get('dash') or {}).get('audio') or []
    if not audio_tracks:
        raise RuntimeError('没有在播放信息里找到音频流。')
    track = audio_tracks[-1]
    return str(track.get('baseUrl') or track.get('base_url') or '')


def inspect_video(url: str) -> VideoAudio:
    html, final_url = fetch_text(url)
    state = extract_json_assignment(html, 'window.__INITIAL_STATE__') or {}
    playinfo = extract_json_assignment(html, 'window.__playinfo__') or {}
    video = state.get('videoData') or {}
    if not video:
        raise RuntimeError('没有在页面里识别到公开视频信息。')
    pages = video.get('pages') or []
    current_page = pages[0] if pages else {}
    bvid = str(video.get('bvid') or '')
    title = str(video.get('title') or bvid or 'bilibili-video')
    author = str((video.get('owner') or state.get('upData') or {}).get('name') or '')
    audio_url = pick_best_audio(playinfo)
    return VideoAudio(
        url=url,
        canonical_url=final_url,
        bvid=bvid or 'bilibili-video',
        title=title,
        author=author,
        duration_seconds=float((playinfo.get('data') or {}).get('timelength') or 0) / 1000,
        audio_url=audio_url,
    )


def download_audio(meta: VideoAudio, output_path: Path, *, timeout: int = 60) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    headers = {
        'User-Agent': USER_AGENT,
        'Accept-Encoding': 'gzip',
        'Referer': meta.canonical_url,
    }
    request = urllib.request.Request(meta.audio_url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response, output_path.open('wb') as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
    return output_path


def convert_to_wav(ffmpeg: Path, source: Path, target: Path) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(ffmpeg),
        '-y',
        '-i',
        str(source),
        '-ar',
        '16000',
        '-ac',
        '1',
        '-c:a',
        'pcm_s16le',
        str(target),
    ]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return target


def transcribe_audio(
    whisper_cli: Path,
    model: Path,
    wav_path: Path,
    output_prefix: Path,
    *,
    language: str,
    threads: int,
) -> Path:
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(whisper_cli),
        '-m', str(model),
        '-l', language,
        '-f', str(wav_path),
        '-otxt',
        '-of', str(output_prefix),
        '-t', str(threads),
    ]
    subprocess.run(command, check=True)
    text_path = output_prefix.with_suffix('.txt')
    if not text_path.exists():
        raise FileNotFoundError(f'转写已执行，但没有找到输出文件: {text_path}')
    return text_path


def sanitize_filename(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', value)
    value = re.sub(r'\s+', ' ', value).strip(' .')
    return value or 'bilibili'


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='下载 B 站视频音频并生成逐字稿。')
    parser.add_argument('url', help='B 站视频链接')
    parser.add_argument('--audio-dir', default=str(DEFAULT_AUDIO_DIR), help='音频缓存目录')
    parser.add_argument('--output-dir', default=str(DEFAULT_OUTPUT_DIR), help='逐字稿输出目录')
    parser.add_argument('--model', default=str(DEFAULT_MODEL), help='whisper.cpp 模型路径')
    parser.add_argument('--whisper-cli', default=str(DEFAULT_WHISPER), help='whisper-cli.exe 路径')
    parser.add_argument('--ffmpeg', default='', help='ffmpeg.exe 路径，不传则先搜索系统 PATH，再搜索 vendor/ffmpeg')
    parser.add_argument('--language', default='zh', help='转写语言，默认 zh')
    parser.add_argument('--threads', type=int, default=4, help='转写线程数')
    parser.add_argument('--keep-audio', action='store_true', help='保留下载后的 m4s 和 wav 文件')
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    ffmpeg = Path(args.ffmpeg) if args.ffmpeg else find_ffmpeg()
    whisper_cli = Path(args.whisper_cli)
    model = Path(args.model)
    audio_dir = Path(args.audio_dir)
    output_dir = Path(args.output_dir)

    if not whisper_cli.exists():
        print(f'没有找到 whisper-cli: {whisper_cli}', file=sys.stderr)
        return 1
    if not model.exists():
        print(f'没有找到模型文件: {model}', file=sys.stderr)
        return 1
    if not ffmpeg.exists():
        print(f'没有找到 ffmpeg: {ffmpeg}', file=sys.stderr)
        return 1

    try:
        meta = inspect_video(args.url)
        stem = sanitize_filename(meta.bvid)
        audio_path = audio_dir / f'{stem}.m4s'
        wav_path = audio_dir / f'{stem}.wav'
        transcript_prefix = output_dir / stem

        print(f'识别视频: {meta.title}')
        print(f'音频时长: {meta.duration_seconds:.1f} 秒')
        print('下载音频...')
        download_audio(meta, audio_path)
        print('转 WAV...')
        convert_to_wav(ffmpeg, audio_path, wav_path)
        print('开始转写...')
        transcript_path = transcribe_audio(
            whisper_cli,
            model,
            wav_path,
            transcript_prefix,
            language=args.language,
            threads=args.threads,
        )
        print(f'逐字稿已生成: {transcript_path}')

        meta_path = output_dir / f'{stem}.meta.json'
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

        if not args.keep_audio:
            audio_path.unlink(missing_ok=True)
            wav_path.unlink(missing_ok=True)
        return 0
    except Exception as error:
        print(f'转写失败: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
