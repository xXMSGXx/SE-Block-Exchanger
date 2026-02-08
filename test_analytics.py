import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from blueprint_analytics import BlueprintAnalyticsEngine


class TestBlueprintAnalytics(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp.name)
        self.bp_file = self.tmp_path / "bp.sbc"
        self.engine = BlueprintAnalyticsEngine()

    def tearDown(self):
        self.tmp.cleanup()

    def _write_blueprint(self, subtypes):
        root = ET.Element("Definitions")
        ship_blueprints = ET.SubElement(root, "ShipBlueprints")
        ship_blueprint = ET.SubElement(ship_blueprints, "ShipBlueprint")
        cube_grid = ET.SubElement(ship_blueprint, "CubeGrid")
        ET.SubElement(cube_grid, "GridSizeEnum").text = "Large"
        cube_blocks = ET.SubElement(cube_grid, "CubeBlocks")
        for subtype in subtypes:
            block = ET.SubElement(cube_blocks, "MyObjectBuilder_CubeBlock")
            ET.SubElement(block, "SubtypeName").text = subtype
        ET.ElementTree(root).write(self.bp_file, encoding="utf-8", xml_declaration=True)

    def test_analyze_blueprint(self):
        self._write_blueprint(
            [
                "LargeBlockArmorBlock",
                "LargeBlockArmorBlock",
                "LargeBlockCockpit",
                "LargeBlockBatteryBlock",
                "LargeBlockSmallThrust",
            ]
        )
        result = self.engine.analyze_blueprint(self.bp_file)
        self.assertEqual(result.block_count, 5)
        self.assertGreater(result.pcu_total, 0)
        self.assertIn("SteelPlate", result.component_totals)
        self.assertEqual(result.grid_size, "Large")
        self.assertTrue(all(issue.code != "missing_power" for issue in result.health_issues))

    def test_compare_conversion_cost(self):
        self._write_blueprint(["LargeBlockArmorBlock", "LargeBlockArmorBlock", "LargeBlockCockpit"])
        mapping = {"LargeBlockArmorBlock": "LargeHeavyBlockArmorBlock"}
        comparison = self.engine.compare_conversion_cost(
            self.bp_file,
            mapping=mapping,
            mode="light_to_heavy",
        )
        self.assertIn("LargeBlockArmorBlock -> LargeHeavyBlockArmorBlock", comparison.block_changes)
        self.assertGreater(comparison.component_delta.get("SteelPlate", 0), 0)

    def test_export_reports(self):
        self._write_blueprint(["LargeBlockArmorBlock", "LargeBlockCockpit"])
        comparison = self.engine.compare_conversion_cost(
            self.bp_file,
            mapping={"LargeBlockArmorBlock": "LargeHeavyBlockArmorBlock"},
            mode="light_to_heavy",
        )
        csv_path = self.tmp_path / "report.csv"
        txt_path = self.tmp_path / "report.txt"
        self.engine.export_comparison_csv(comparison, csv_path)
        self.engine.export_comparison_text(comparison, txt_path)
        self.assertTrue(csv_path.exists())
        self.assertTrue(txt_path.exists())

    def test_apply_fix_add_power(self):
        self._write_blueprint(["LargeBlockArmorBlock", "LargeBlockCockpit"])
        result = self.engine.analyze_blueprint(self.bp_file)
        self.assertTrue(any(issue.code == "missing_power" for issue in result.health_issues))

        applied = self.engine.apply_fix(self.bp_file, "add_power_block")
        self.assertTrue(applied)

        fixed = self.engine.analyze_blueprint(self.bp_file)
        self.assertFalse(any(issue.code == "missing_power" for issue in fixed.health_issues))


if __name__ == "__main__":
    unittest.main()

