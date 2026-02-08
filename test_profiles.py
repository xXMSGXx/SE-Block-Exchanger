import json
import tempfile
import unittest
from pathlib import Path

from mapping_profiles import MappingProfile, ProfileManager
from mappings import build_registry
from mappings.registry import MappingCategory


class TestProfiles(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.profile_dir = Path(self.tmp.name)
        self.manager = ProfileManager(self.profile_dir)

    def tearDown(self):
        self.tmp.cleanup()

    def test_save_and_load_profile(self):
        profile = MappingProfile(
            name="Test Profile",
            author="Tester",
            version="1.0",
            description="Test",
            game_version="1.205+",
            categories=[
                MappingCategory(
                    name="profile:test:weapons",
                    description="Test category",
                    pairs={"SmallGatlingGun": "CustomGun"},
                    source="profile:Test",
                    enabled_by_default=False,
                    tags=("profile",),
                )
            ],
        )
        saved = self.manager.upsert_profile(profile)
        self.assertTrue(saved.exists())

        self.manager.load_all()
        loaded = self.manager.get("Test Profile")
        self.assertEqual(loaded.name, "Test Profile")
        self.assertEqual(len(loaded.categories), 1)
        self.assertIn("SmallGatlingGun", loaded.categories[0].pairs)

    def test_register_profile_categories(self):
        payload = {
            "name": "Imported",
            "author": "Tester",
            "version": "1.0",
            "description": "Imported profile",
            "game_version": "1.205+",
            "categories": [
                {
                    "name": "ModCat",
                    "pairs": [["A", "B"]],
                }
            ],
        }
        path = self.profile_dir / "imported.sebx-profile"
        path.write_text(json.dumps(payload), encoding="utf-8")
        self.manager.load_all()

        registry = build_registry(include_builtin=True)
        count = self.manager.register_profile_categories(registry)
        self.assertEqual(count, 1)
        self.assertTrue(any(cat.name.startswith("profile:imported:") for cat in registry.list_categories()))

    def test_duplicate_profile(self):
        payload = {
            "name": "Original",
            "author": "Tester",
            "version": "1.0",
            "description": "Original profile",
            "game_version": "1.205+",
            "categories": [
                {
                    "name": "Cat1",
                    "pairs": [["X", "Y"]],
                }
            ],
        }
        path = self.profile_dir / "original.sebx-profile"
        path.write_text(json.dumps(payload), encoding="utf-8")
        self.manager.load_all()

        duplicated = self.manager.duplicate_profile("Original", "Original Copy")
        self.assertEqual(duplicated.name, "Original Copy")
        self.assertEqual(duplicated.categories[0].pairs["X"], "Y")


if __name__ == "__main__":
    unittest.main()

