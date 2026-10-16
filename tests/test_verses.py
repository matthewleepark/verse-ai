import unittest
from datetime import date, timedelta

import verses
from bible import lookup


class DailyListTests(unittest.TestCase):
    def test_every_entry_is_a_real_verse_with_a_title_word(self):
        for entry in verses.daily_list():
            with self.subTest(ref=entry["ref"]):
                self.assertEqual(lookup(entry["ref"]).reference, entry["ref"])
                self.assertTrue(entry["word"])
                self.assertEqual(entry["word"], entry["word"].upper())

    def test_no_repeats_for_over_a_year(self):
        refs = [e["ref"] for e in verses.daily_list()]
        self.assertEqual(len(refs), len(set(refs)))
        self.assertGreaterEqual(len(refs), 366)

    def test_all_wisdom_verses_are_in_the_daily_list(self):
        refs = {e["ref"] for e in verses.daily_list()}
        for theme_refs in verses.WISDOM_VERSES.values():
            for ref in theme_refs:
                self.assertTrue(ref in refs, f"{ref} is missing from data/daily_verses.json")


class GetVerseTests(unittest.TestCase):
    def test_same_day_same_verse(self):
        d = date(2026, 10, 15)
        self.assertEqual(verses.get_verse(d), verses.get_verse(d))

    def test_a_new_verse_every_day_for_a_year(self):
        start = date(2026, 1, 1)
        refs = [verses.get_verse(start + timedelta(days=n)).reference for n in range(366)]
        self.assertEqual(len(set(refs)), 366)

    def test_verse_has_a_title_word(self):
        self.assertTrue(verses.get_verse(date(2026, 10, 15)).word)

    def test_wisdom_verses_know_their_theme(self):
        verse = verses.get_verse(reference="James 1:19")
        self.assertEqual(verse.theme, "patience")
        self.assertEqual(verse.word, "LISTEN")

    def test_theme_filter(self):
        verse = verses.get_verse(date(2026, 1, 1), theme="integrity")
        self.assertIn(verse.reference, verses.WISDOM_VERSES["integrity"])
        self.assertEqual(verse.theme, "integrity")

    def test_unknown_theme(self):
        with self.assertRaises(ValueError):
            verses.pick_reference(theme="astrology")

    def test_reference_outside_the_list_gets_a_default_word(self):
        verse = verses.get_verse(reference="Genesis 2:7")
        self.assertEqual(verse.word, "FAITH")
        self.assertIsNone(verse.theme)

    def test_shuffle_with_theme(self):
        verse = verses.get_verse(theme="empathy", shuffle=True)
        self.assertIn(verse.reference, verses.WISDOM_VERSES["empathy"])


if __name__ == "__main__":
    unittest.main()

