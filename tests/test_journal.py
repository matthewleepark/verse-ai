import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from bible import Verse
from journal import save_entry

VERSE = Verse(
    "James 1:19", "Everyone should be quick to listen, slow to speak.", theme="patience", word="LISTEN"
)


class SaveEntryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name) / "journals"

    def tearDown(self):
        self.tmp.cleanup()

    def test_creates_dated_file_with_the_verse(self):
        path = save_entry(VERSE, "I interrupted someone today.", datetime(2026, 10, 14, 9, 30), self.folder)
        self.assertEqual(path.name, "2026-10-14.md")
        text = path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Journal — Wednesday, October 14, 2026"))
        self.assertIn("## 09:30 — James 1:19 · LISTEN", text)
        self.assertIn("quick to listen", text)
        self.assertIn("I interrupted someone today.", text)

    def test_second_entry_same_day_appends(self):
        save_entry(VERSE, "First.", datetime(2026, 10, 14, 9, 0), self.folder)
        path = save_entry(VERSE, "Second.", datetime(2026, 10, 14, 21, 0), self.folder)
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text.count("# Journal"), 1)
        self.assertLess(text.index("First."), text.index("Second."))

    def test_empty_reflection_rejected(self):
        with self.assertRaises(ValueError):
            save_entry(VERSE, "   ", folder=self.folder)


if __name__ == "__main__":
    unittest.main()
