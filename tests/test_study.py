import unittest
from datetime import date

import bible
import study
from verses import THEMES, WISDOM_VERSES


class StudyContentTests(unittest.TestCase):
    def test_every_wisdom_verse_has_complete_notes(self):
        for refs in WISDOM_VERSES.values():
            for ref in refs:
                with self.subTest(ref=ref):
                    notes = study.notes_for(ref)
                    self.assertIsNotNone(notes)
                    for key in ("wisdom", "context", "meaning"):
                        self.assertTrue(notes.get(key))

    def test_no_orphan_notes(self):
        curated = {ref for refs in WISDOM_VERSES.values() for ref in refs}
        self.assertEqual(set(study._load("study_notes.json")), curated)

    def test_every_book_has_background(self):
        books = {ref.rsplit(" ", 1)[0] for ref in bible.load()}
        self.assertEqual(len(books), 66)
        for book in books:
            with self.subTest(book=book):
                info = study.book_info(book)
                self.assertIsNotNone(info)
                self.assertEqual(set(info), {"type", "author", "date", "about"})

    def test_reflection_questions_for_every_theme(self):
        for theme in THEMES:
            self.assertTrue(study.reflection_question(theme, date(2026, 10, 14)))
        self.assertTrue(study.reflection_question(None, date(2026, 10, 14)))

    def test_reflection_question_rotates_daily(self):
        days = [date(2026, 10, d) for d in range(1, 6)]
        self.assertEqual(len({study.reflection_question("patience", d) for d in days}), 5)


class ReadingPlanTests(unittest.TestCase):
    def test_chapter_matches_day_of_month(self):
        self.assertEqual(study.reading_for(date(2026, 10, 14)), ("Proverbs", 14))
        self.assertEqual(study.reading_for(date(2026, 1, 31)), ("Proverbs", 31))

    def test_every_chapter_exists(self):
        for chapter in range(1, 32):
            with self.subTest(chapter=chapter):
                self.assertTrue(bible.passage("Proverbs", chapter))


if __name__ == "__main__":
    unittest.main()
