import json
import re
import tempfile
import unittest
from datetime import date
from pathlib import Path

import verses
import visual
from verses import get_verse

DAY = date(2026, 10, 15)


def embedded_data(html: str) -> dict:
    match = re.search(r"const DATA = (\{.*?\});\n", html, re.DOTALL)
    return json.loads(match.group(1).replace("<\\/", "</"))


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        out = Path(cls.tmp.name) / "today.html"
        cls.verse = get_verse(reference="Matthew 14:31")
        cls.html = visual.build(cls.verse, DAY, out).read_text(encoding="utf-8")
        cls.data = embedded_data(cls.html)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_page_opens_on_the_chosen_verse(self):
        self.assertNotIn("/*__VERSE_DATA__*/", self.html)
        start = self.data["start"]
        self.assertEqual(start["ref"], "Matthew 14:31")
        self.assertEqual(start["word"], "FAITH")
        self.assertIn("doubt", start["text"])
        self.assertEqual(self.data["startDate"], "2026-10-15")

    def test_every_daily_verse_is_embedded_for_browsing(self):
        self.assertEqual(len(self.data["daily"]), len(verses.daily_list()))
        # The page picks entry (ordinal + offset) % length, the same rule as get_verse().
        tomorrow = date(2026, 10, 16)
        i = tomorrow.toordinal() % len(self.data["daily"])
        self.assertEqual(self.data["daily"][i]["ref"], get_verse(tomorrow).reference)

    def test_page_knows_the_real_date(self):
        # "Today" must mean the actual date even when the page opens on another day.
        self.assertEqual(self.data["todayOrdinal"], date.today().toordinal())
        self.assertEqual(self.data["startOrdinal"], DAY.toordinal())

    def test_about_panel_has_notes_context_and_book(self):
        self.assertIn("James 1:19", self.data["notes"])
        start = self.data["start"]
        self.assertEqual(start["book"], "Matthew")
        self.assertEqual(start["range"], [31, 31])
        self.assertIn(31, [n for n, _ in start["context"]])
        self.assertIn("Matthew", self.data["books"])

    def test_artwork_and_fonts_are_embedded_for_offline_use(self):
        self.assertTrue(self.data["image"].startswith("data:image/jpeg;base64,"))
        for name in ("bangers", "comicNeue"):
            self.assertTrue(self.data["fonts"][name].startswith("data:font/ttf;base64,"))

    def test_verse_text_cannot_break_out_of_the_script_tag(self):
        self.assertEqual(self.html.count("</script>"), 1)


if __name__ == "__main__":
    unittest.main()
