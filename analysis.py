"""Claude-powered breakdown and Q&A for the day's verse pair.

VerseCompanion keeps one conversation per pair so follow-up questions and
summaries have the breakdown (and earlier answers) as context. Breakdowns are
saved locally, so a pair you've seen before works offline.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import anthropic

import cache
from verses import DailyPair

MODEL = "claude-opus-5-5"
MAX_TOKENS = 16000
EFFORT = "medium"
# If Claude's safety classifiers decline a request, the API retries it on
# Anthropic's recommended fallback model instead of returning a refusal.
FALLBACK_BETA = "server-side-fallback-2026-07-01"

SYSTEM_TEMPLATE = """\
You are verse-ai, a thoughtful study companion in a command-line app. Each day \
the student gets two Bible verses (Berean Standard Bible): a main verse chosen \
for its wisdom on {theme}, and a partner verse picked at random from anywhere \
in the Bible.

Main verse: {main_ref}
"{main_text}"

Partner verse: {partner_ref}
"{partner_text}"

Guidelines:
- Your output is printed in a plain terminal. Don't use Markdown: no #, no **, \
no tables. Simple hyphen lists are fine.
- Be accurate about history and scholarship. When authorship, dating, or \
interpretation is debated or uncertain, say so rather than picking one view.
- Describe theology as what a tradition teaches ("In Christian tradition...", \
"Jewish commentators..."), and note where traditions differ. Don't assume the \
student's beliefs or preach.
- The partner verse is random, so the link to the main verse may be loose. \
Be honest about that; a contrast or an unexpected angle is better than a \
forced connection.
- Answer follow-up questions in a short paragraph or two unless asked for more. \
If a question is unrelated to the verses, answer briefly and connect it back.
"""

BREAKDOWN_PROMPT = """\
Break down today's pair. Put each section title on its own line in capitals, \
followed by about 80-120 words:

UNIVERSAL WISDOM - the main verse's principle that anyone could apply \
regardless of faith, with one concrete everyday example.
HISTORICAL CONTEXT - who wrote the main verse, roughly when, to whom, and what \
was going on; mention the surrounding passage if it changes the meaning.
THEOLOGICAL MEANING - how Jewish and/or Christian traditions have read the \
main verse.
THE CONNECTION - briefly place the partner verse in its own context, then show \
how it echoes, deepens, or pushes against the main verse.
"""

SUMMARY_PROMPT = """\
Give me a quick summary: the core idea of the pair in one sentence, then two or \
three short takeaways drawn from our conversation so far.
"""


class AnalysisError(Exception):
    """Raised when Claude can't produce a response; message is user-facing."""


def _history_blocks(content: list) -> list:
    """Assistant content to echo back into the conversation.

    After a mid-response fallback, everything before the last `fallback` block
    except text came from the declined model and must not be sent back.
    """
    boundary = max((i for i, b in enumerate(content) if b.type == "fallback"), default=-1)
    return [b for i, b in enumerate(content) if i > boundary or b.type == "text"]


class VerseCompanion:
    def __init__(
        self,
        pair: DailyPair,
        client: anthropic.Anthropic | None = None,
        offline: bool = False,
        cache_path: Path = cache.CACHE_FILE,
    ):
        self.pair = pair
        self.offline = offline
        self.cache_path = cache_path
        self._client = client
        self.system = SYSTEM_TEMPLATE.format(
            theme=pair.main.theme or "universal human wisdom",
            main_ref=pair.main.reference,
            main_text=pair.main.text,
            partner_ref=pair.partner.reference,
            partner_text=pair.partner.text,
        )
        self.messages: list[dict] = []

    def breakdown(self, on_text: Callable[[str], None] = print) -> str:
        refs = (self.pair.main.reference, self.pair.partner.reference)
        saved = cache.get_breakdown(*refs, path=self.cache_path)
        if saved:
            # Replay it as the first exchange so follow-ups still have it as context.
            self.messages += [
                {"role": "user", "content": BREAKDOWN_PROMPT},
                {"role": "assistant", "content": saved},
            ]
            on_text(saved)
            return saved
        text = self._send(BREAKDOWN_PROMPT, on_text)
        cache.save_breakdown(*refs, text, path=self.cache_path)
        return text

    def summary(self, on_text: Callable[[str], None] = print) -> str:
        return self._send(SUMMARY_PROMPT, on_text)

    def ask(self, question: str, on_text: Callable[[str], None] = print) -> str:
        return self._send(question, on_text)

    @property
    def client(self) -> anthropic.Anthropic:
        if self._client is None:
            client = anthropic.Anthropic()
            # The SDK only notices missing credentials when it sends a request, so check now.
            if not (client.api_key or client.auth_token or client.credentials):
                raise AnalysisError(
                    "No Claude API key is set (ANTHROPIC_API_KEY), so AI features are off. "
                    "Verses and journaling still work."
                )
            self._client = client
        return self._client

    def _send(self, prompt: str, on_text: Callable[[str], None]) -> str:
        """Stream one turn, calling on_text with each chunk; returns the full text."""
        if self.offline:
            raise AnalysisError("Offline mode is on, so AI features are off. Verses and journaling still work.")
        client = self.client
        self.messages.append({"role": "user", "content": prompt})
        try:
            with client.beta.messages.stream(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=self.system,
                messages=self.messages,
                output_config={"effort": EFFORT},
                betas=[FALLBACK_BETA],
                fallbacks="default",
            ) as stream:
                for chunk in stream.text_stream:
                    on_text(chunk)
                message = stream.get_final_message()
        except anthropic.AuthenticationError as e:
            raise self._fail("Claude rejected the API key. Check ANTHROPIC_API_KEY.") from e
        except anthropic.RateLimitError as e:
            raise self._fail("Rate limited by the Claude API. Wait a minute and try again.") from e
        except anthropic.APIStatusError as e:
            raise self._fail(f"Claude API error ({e.status_code}): {e.message}") from e
        except anthropic.APIConnectionError as e:
            raise self._fail(
                "Can't reach Claude (no internet?). Verses and journaling still work offline."
            ) from e
        except KeyboardInterrupt:
            self.messages.pop()
            raise

        if message.stop_reason == "refusal":
            raise self._fail("Claude declined to answer that. Try rephrasing your question.")

        self.messages.append({"role": "assistant", "content": _history_blocks(message.content)})
        return "".join(b.text for b in message.content if b.type == "text")

    def _fail(self, reason: str) -> AnalysisError:
        # Drop the unanswered question so the conversation stays valid for the next turn.
        self.messages.pop()
        return AnalysisError(reason)
