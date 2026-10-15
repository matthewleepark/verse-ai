import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import anthropic

from analysis import AnalysisError, VerseCompanion, _history_blocks
from bible import Verse
from verses import DailyPair

PAIR = DailyPair(
    Verse("Proverbs 15:1", "A gentle answer turns away wrath.", theme="conflict resolution"),
    Verse("Genesis 1:1", "In the beginning God created the heavens and the earth."),
)


def block(type_, text=""):
    return SimpleNamespace(type=type_, text=text)


class FakeStream:
    def __init__(self, message):
        self.message = message
        self.text_stream = [b.text for b in message.content if b.type == "text"]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def get_final_message(self):
        return self.message


class FakeClient:
    """Stands in for anthropic.Anthropic; records each request."""

    api_key, auth_token, credentials = "test-key", None, None

    def __init__(self, *results):
        self.results = list(results)
        self.requests = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(stream=self._stream))

    def _stream(self, **kwargs):
        self.requests.append({**kwargs, "messages": list(kwargs["messages"])})
        result = self.results.pop(0)
        if isinstance(result, Exception):
            raise result
        return FakeStream(result)


def reply(text, stop_reason="end_turn"):
    return SimpleNamespace(content=[block("text", text)], stop_reason=stop_reason)


class VerseCompanionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cache_path = Path(self.tmp.name) / "breakdowns.json"

    def tearDown(self):
        self.tmp.cleanup()

    def companion(self, *results, **kwargs):
        client = FakeClient(*results)
        return VerseCompanion(PAIR, client=client, cache_path=self.cache_path, **kwargs), client

    def test_system_prompt_contains_both_verses(self):
        companion, _ = self.companion()
        self.assertIn("Proverbs 15:1", companion.system)
        self.assertIn("gentle answer", companion.system)
        self.assertIn("Genesis 1:1", companion.system)

    def test_follow_up_includes_history(self):
        companion, client = self.companion(reply("BREAKDOWN"), reply("ANSWER"))
        chunks = []
        companion.breakdown(chunks.append)
        answer = companion.ask("Who wrote Proverbs?", chunks.append)

        self.assertEqual(answer, "ANSWER")
        self.assertEqual(chunks, ["BREAKDOWN", "ANSWER"])
        second = client.requests[1]["messages"]
        self.assertEqual([m["role"] for m in second], ["user", "assistant", "user"])
        self.assertEqual(second[-1]["content"], "Who wrote Proverbs?")

    def test_breakdown_is_cached_and_reused_offline(self):
        first, _ = self.companion(reply("BREAKDOWN"))
        first.breakdown(lambda _: None)

        again, client = self.companion(offline=True)
        chunks = []
        self.assertEqual(again.breakdown(chunks.append), "BREAKDOWN")
        self.assertEqual(chunks, ["BREAKDOWN"])
        self.assertEqual(client.requests, [])
        # The cached breakdown becomes context for follow-up questions.
        self.assertEqual([m["role"] for m in again.messages], ["user", "assistant"])

    def test_offline_mode_never_calls_claude(self):
        companion, client = self.companion(offline=True)
        with self.assertRaisesRegex(AnalysisError, "Offline mode"):
            companion.breakdown(lambda _: None)
        with self.assertRaisesRegex(AnalysisError, "Offline mode"):
            companion.ask("hi", lambda _: None)
        self.assertEqual(client.requests, [])
        self.assertEqual(companion.messages, [])

    def test_missing_credentials_is_friendly(self):
        keyless = FakeClient()
        keyless.api_key = None
        companion = VerseCompanion(PAIR, cache_path=self.cache_path)
        with patch("analysis.anthropic.Anthropic", return_value=keyless):
            with self.assertRaisesRegex(AnalysisError, "ANTHROPIC_API_KEY"):
                companion.ask("hi", lambda _: None)
        self.assertEqual(companion.messages, [])

    def test_refusal_raises_and_keeps_history_valid(self):
        companion, _ = self.companion(reply("", stop_reason="refusal"))
        with self.assertRaises(AnalysisError):
            companion.ask("something", lambda _: None)
        self.assertEqual(companion.messages, [])

    def test_connection_error_is_friendly(self):
        error = anthropic.APIConnectionError(request=SimpleNamespace(method="POST", url="x"))
        companion, _ = self.companion(error)
        with self.assertRaisesRegex(AnalysisError, "internet"):
            companion.ask("hi", lambda _: None)
        self.assertEqual(companion.messages, [])

    def test_failed_breakdown_is_not_cached(self):
        error = anthropic.APIConnectionError(request=SimpleNamespace(method="POST", url="x"))
        companion, _ = self.companion(error)
        with self.assertRaises(AnalysisError):
            companion.breakdown(lambda _: None)
        self.assertFalse(self.cache_path.exists())


class HistoryBlocksTests(unittest.TestCase):
    def test_no_fallback_keeps_everything(self):
        content = [block("thinking"), block("text", "hi")]
        self.assertEqual(_history_blocks(content), content)

    def test_drops_non_text_before_fallback(self):
        thinking, partial, marker, after_thinking, after_text = (
            block("thinking"), block("text", "par"), block("fallback"), block("thinking"), block("text", "tial"),
        )
        kept = _history_blocks([thinking, partial, marker, after_thinking, after_text])
        self.assertEqual(kept, [partial, after_thinking, after_text])


if __name__ == "__main__":
    unittest.main()
