import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from update_checker import UpdateChecker


class TestUpdateChecker(unittest.TestCase):
    def test_uses_cache_and_detects_newer_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "cache.json"
            payload = {
                "tag_name": "v99.0.0",
                "html_url": "https://example.com/release",
                "published_at": "2026-01-01T00:00:00Z",
                "body": "release notes",
                "cached_at": datetime.now(timezone.utc).isoformat(),
            }
            cache_path.write_text(json.dumps(payload), encoding="utf-8")

            checker = UpdateChecker(cache_path=cache_path, cache_hours=24)
            info = checker.check_for_updates(force=False)
            self.assertTrue(info.available)
            self.assertEqual(info.latest_version, "99.0.0")
            self.assertEqual(info.release_url, "https://example.com/release")

    def test_cache_version_not_newer(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp) / "cache.json"
            payload = {
                "tag_name": "v0.0.1",
                "html_url": "https://example.com/release",
                "published_at": "2026-01-01T00:00:00Z",
                "body": "release notes",
                "cached_at": datetime.now(timezone.utc).isoformat(),
            }
            cache_path.write_text(json.dumps(payload), encoding="utf-8")

            checker = UpdateChecker(cache_path=cache_path, cache_hours=24)
            info = checker.check_for_updates(force=False)
            self.assertFalse(info.available)


if __name__ == "__main__":
    unittest.main()

