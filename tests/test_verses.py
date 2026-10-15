import unittest
from datetime import date

import verses
from bible import lookup


class WisdomListTests(unittest.TestCase):
    def test_every_curated_reference_exists(self):
        for theme, refs in verses.WISDOM_VERSES.items():
            for ref in refs:
                with self.subTest(theme=theme, ref=ref):
                    self.assertTrue(lookup(ref).text)


class PickReferenceTests(unittest.TestCase):
    def test_same_day_same_verse(self):
        d = date(2026, 10, 14)
        self.assertEqual(verses.pick_reference(d), verses.pick_reference(d))

    def test_consecutive_days_differ(self):
        self.assertNotEqual(
            verses.pick_reference(date(2026, 10, 14)),
            verses.pick_reference(date(2026, 10, 15)),
        )

    def test_theme_filter(self):
        theme, ref = verses.pick_reference(date(2026, 1, 1), theme="integrity")
        self.assertEqual(theme, "integrity")
        self.assertIn(ref, verses.WISDOM_VERSES["integrity"])

    def test_unknown_theme(self):
        with self.assertRaises(ValueError):
            verses.pick_reference(theme="astrology")


class GetPairTests(unittest.TestCase):
    def test_same_day_same_pair(self):
        d = date(2026, 10, 14)
        self.assertEqual(verses.get_pair(d), verses.get_pair(d))

    def test_main_verse_is_themed_and_partner_differs(self):
        pair = verses.get_pair(date(2026, 10, 14))
        self.assertIn(pair.main.theme, verses.THEMES)
        self.assertNotEqual(pair.main.reference, pair.partner.reference)

    def test_partners_vary_across_days(self):
        partners = {verses.get_pair(date(2026, 1, 1).replace(day=d)).partner for d in range(1, 29)}
        self.assertGreater(len(partners), 20)

    def test_specific_reference(self):
        pair = verses.get_pair(date(2026, 10, 14), reference="John 3:16")
        self.assertEqual(pair.main.reference, "John 3:16")
        self.assertIsNone(pair.main.theme)

    def test_shuffle_still_themed(self):
        pair = verses.get_pair(theme="empathy", shuffle=True)
        self.assertEqual(pair.main.theme, "empathy")


if __name__ == "__main__":
    unittest.main()
