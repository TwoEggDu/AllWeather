from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / 'tools' / 'bilibili_summarizer.py'
SPEC = importlib.util.spec_from_file_location("bilibili_summarizer", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

VIDEO_HTML = """
<html>
  <body>
    <script>
      window.__INITIAL_STATE__={"videoData":{"bvid":"BV1xx411c7mD","title":"宏观测试视频","owner":{"name":"测试UP"},"desc":"这是一个关于宏观研究的测试简介。","pubdate":1700000000,"stat":{"view":12345,"like":456},"pages":[{"cid":987654,"page":1,"part":"P1 开场"}]},"tags":[{"tag_name":"宏观"},{"tag_name":"投资"}]};
    </script>
    <script>
      window.__playinfo__={"data":{"subtitle":{"subtitles":[{"lan":"zh-CN","lan_doc":"中文","subtitle_url":"https://example.com/subtitle.json"}]}}};
    </script>
  </body>
</html>
"""


class BilibiliSummarizerTest(unittest.TestCase):
    def test_extract_json_assignment(self) -> None:
        state = MODULE.extract_json_assignment(VIDEO_HTML, "window.__INITIAL_STATE__")
        self.assertEqual(state["videoData"]["bvid"], "BV1xx411c7mD")
        self.assertEqual(state["tags"][0]["tag_name"], "宏观")

    def test_parse_subtitle_payload(self) -> None:
        payload = {
            "body": [
                {"from": 0, "to": 2, "content": "第一段内容。"},
                {"from": 2, "to": 7, "content": "第二段继续展开。"},
            ]
        }
        lines = MODULE.parse_subtitle_payload(payload)
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0].text, "第一段内容。")
        self.assertEqual(MODULE.format_timestamp(lines[1].start), "00:02")

    def test_text_lines_to_subtitles_supports_timestamp_prefix(self) -> None:
        lines = MODULE.text_lines_to_subtitles("00:03 第一段内容。\n第二段内容。")
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0].start, 3.0)
        self.assertEqual(lines[1].start, None)
        self.assertEqual(lines[1].text, "第二段内容。")

    def test_summarize_text_has_sections(self) -> None:
        subtitles = [
            MODULE.SubtitleLine("今天讨论高利率为什么会让市场继续分化。", 0, 20),
            MODULE.SubtitleLine("第二部分解释增长和通胀如何影响资产定价。", 20, 40),
            MODULE.SubtitleLine("第三部分解释贴现率和现金流之间的关系。", 40, 70),
            MODULE.SubtitleLine("最后给出普通投资者的观察框架。", 70, 95),
        ]
        text = "\n".join(f"{MODULE.format_timestamp(line.start)} {line.text}" for line in subtitles)
        summary = MODULE.summarize_text(text, subtitles)
        self.assertIn("## 总览", summary)
        self.assertIn("## 核心要点", summary)
        self.assertIn("## 内容脉络", summary)
        self.assertIn("高利率", summary)

    def test_fetch_video_summary_falls_back_to_transcript(self) -> None:
        transcript = MODULE.TranscriptResult(
            source_label="自动转写(缓存)",
            source_text="第一段讲行业周期。\n第二段讲三家公司定位。",
            lines=MODULE.text_lines_to_subtitles("第一段讲行业周期。\n第二段讲三家公司定位。"),
            warnings=["未找到公开字幕，已复用本地逐字稿。逐字稿可能包含语音识别误差。"],
            transcript_path=REPO_ROOT / 'tools' / 'transcripts' / 'BV1xx411c7mD.txt',
        )
        with patch.object(MODULE, "fetch_text", return_value=(VIDEO_HTML, "https://www.bilibili.com/video/BV1xx411c7mD")), patch.object(
            MODULE,
            "fetch_subtitles",
            return_value=([], ""),
        ), patch.object(MODULE, "maybe_load_or_create_transcript", return_value=transcript):
            summary = MODULE.fetch_video_summary(
                "https://www.bilibili.com/video/BV1xx411c7mD",
                transcribe=MODULE.TranscribeOptions(),
            )
        self.assertEqual(summary.source_label, "自动转写(缓存)")
        self.assertIn("行业周期", summary.source_text)
        self.assertIn("识别误差", "；".join(summary.warnings))
        self.assertEqual(summary.transcript_path, str(transcript.transcript_path))


if __name__ == "__main__":
    unittest.main()
