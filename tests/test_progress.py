import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import progress

TODAY = date(2026, 10, 14)


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "progress.json"

    def tearDown(self):
        self.tmp.cleanup()

    def study(self, day, **flags):
        progress.record(day, "James 1:19", path=self.path, **flags)

    def test_no_history_means_no_streak(self):
        self.assertEqual(progress.streak(TODAY, path=self.path), 0)
        self.assertEqual(progress.history(path=self.path), [])

    def test_just_opening_the_app_does_not_count(self):
        self.study(TODAY)
        self.assertEqual(progress.streak(TODAY, path=self.path), 0)
        self.assertFalse(progress.studied_on(TODAY, path=self.path))

    def test_consecutive_days_build_a_streak(self):
        for offset in range(3):
            self.study(TODAY - timedelta(days=offset), read=True)
        self.assertEqual(progress.streak(TODAY, path=self.path), 3)

    def test_streak_survives_until_today_is_done(self):
        self.study(TODAY - timedelta(days=1), journaled=True)
        self.study(TODAY - timedelta(days=2), read=True)
        self.study(TODAY)  # opened today, not studied yet
        self.assertEqual(progress.streak(TODAY, path=self.path), 2)

    def test_missed_day_breaks_streak(self):
        self.study(TODAY, read=True)
        self.study(TODAY - timedelta(days=2), read=True)
        self.assertEqual(progress.streak(TODAY, path=self.path), 1)

    def test_flags_never_turn_off(self):
        self.study(TODAY, read=True)
        self.study(TODAY, journaled=True)
        self.study(TODAY)
        record = progress.history(path=self.path)[0]
        self.assertTrue(record.read)
        self.assertTrue(record.journaled)

    def test_history_newest_first(self):
        self.study(TODAY - timedelta(days=5), read=True)
        self.study(TODAY, read=True)
        days = [r.day for r in progress.history(path=self.path)]
        self.assertEqual(days, [TODAY, TODAY - timedelta(days=5)])


if __name__ == "__main__":
    unittest.main()

