import random
import unittest

import bible
from bible import VerseNotFoundError, lookup, random_verse


class LoadTests(unittest.TestCase):
    def test_full_bible_loaded(self):
        verses = bible.load()
        self.assertEqual(len(verses), 31102)
        self.assertEqual(next(iter(verses)), "Genesis 1:1")
        self.assertEqual(list(verses)[-1], "Revelation 22:21")


class LookupTests(unittest.TestCase):
    def test_single_verse(self):
        verse = lookup("Genesis 1:1")
        self.assertEqual(verse.reference, "Genesis 1:1")
        self.assertEqual(verse.text, "In the beginning God created the heavens and the earth.")
        self.assertEqual(verse.translation, "Berean Standard Bible")

    def test_case_and_spacing_insensitive(self):
        self.assertEqual(lookup("  1  peter 3:8 ").reference, "1 Peter 3:8")

    def test_psalms_alias(self):
        self.assertEqual(lookup("Psalms 23:1").reference, "Psalm 23:1")

    def test_range_joins_text(self):
        verse = lookup("Genesis 1:1-2")
        self.assertEqual(verse.reference, "Genesis 1:1-2")
        self.assertTrue(verse.text.startswith("In the beginning"))
        self.assertIn("formless and void", verse.text)

    def test_missing_verse(self):
        with self.assertRaisesRegex(VerseNotFoundError, "not found"):
            lookup("Psalm 999:1")

    def test_unreadable_reference(self):
        with self.assertRaisesRegex(VerseNotFoundError, "Can't read"):
            lookup("hello")

    def test_backwards_range(self):
        with self.assertRaises(VerseNotFoundError):
            lookup("John 3:18-16")

    def test_verse_omitted_by_bsb(self):
        with self.assertRaisesRegex(VerseNotFoundError, "earliest manuscripts"):
            lookup("Matthew 17:21")


class PassageTests(unittest.TestCase):
    def test_context_surrounds_the_verse(self):
        numbers = [n for n, _ in bible.context("James 1:19", radius=2)]
        self.assertEqual(numbers, [17, 18, 19, 20, 21])

    def test_context_stops_at_chapter_start(self):
        numbers = [n for n, _ in bible.context("Genesis 1:1", radius=2)]
        self.assertEqual(numbers, [1, 2, 3])

    def test_whole_chapter(self):
        self.assertEqual(len(bible.passage("Psalm", 119)), 176)
        self.assertEqual(len(bible.passage("Proverbs", 14)), 35)

    def test_passage_skips_omitted_verses(self):
        numbers = [n for n, _ in bible.passage("Matthew", 17, 20, 22)]
        self.assertEqual(numbers, [20, 22])

    def test_book_of(self):
        self.assertEqual(bible.book_of("psalms 23:1"), "Psalm")
        self.assertEqual(bible.book_of("1 John 3:17"), "1 John")


class RandomVerseTests(unittest.TestCase):
    def test_seeded_rng_is_repeatable(self):
        self.assertEqual(random_verse(random.Random(42)), random_verse(random.Random(42)))

    def test_never_empty_and_respects_exclude(self):
        rng = random.Random(0)
        first = random_verse(rng)
        for _ in range(500):
            verse = random_verse(rng, exclude=frozenset({first.reference}))
            self.assertTrue(verse.text)
            self.assertNotEqual(verse.reference, first.reference)


if __name__ == "__main__":
    unittest.main()
