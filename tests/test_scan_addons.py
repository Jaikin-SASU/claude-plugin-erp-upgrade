#!/usr/bin/env python3
"""Tests for scan_addons.py (TDD — written before implementation)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "odoo-20-upgrade" / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "addons"
SCAN = SCRIPTS / "scan_addons.py"

# Rules that acme_legacy must trigger (all except the four listed in the brief).
EXPECTED_LEGACY_RULES = {
    "ACCESS_CSV",
    "IR_RULE",
    "MODEL_ACCESS_REF",
    "OWL2_API",
    "ODOO_DEFINE",
    "READ_GROUP_OLD",
    "TRACKING_VALUE",
    "SQL_CONSTRAINTS",
    "ATTRS_STATES",
    "TREE_VIEW",
    "JSON_ROUTE",
    "CR_UID_CONTEXT",
    "REMOVED_DEPENDS",
}
EXCLUDED_FROM_LEGACY = {
    "XMLRPC_CLIENT",
    "TABLE_QUERY",
    "CHECK_ACCESS_DEPRECATED",
    "FA_ICONS",
}


def _import_scan():
    sys.path.insert(0, str(SCRIPTS))
    import scan_addons  # noqa: WPS433

    return scan_addons


class TestScanAddonsFixtures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scan = _import_scan()
        cls.result = cls.scan.scan_addons_dir(str(FIXTURES), target=20)

    def _module(self, name: str) -> dict:
        for mod in self.result["modules"]:
            if mod["name"] == name:
                return mod
        self.fail(f"module {name!r} not found in scan result")

    def test_global_envelope(self):
        self.assertEqual(self.result["target"], 20)
        self.assertEqual(self.result["rules_version"], "2026-09-24")
        self.assertIn("scanned_on", self.result)
        self.assertIn("totals", self.result)
        totals = self.result["totals"]
        for key in ("blockers", "majors", "minors", "effort_points", "occurrences"):
            self.assertIn(key, totals)

    def test_acme_legacy_triggers_expected_rules(self):
        mod = self._module("acme_legacy")
        found = {f["rule_id"] for f in mod["findings"]}
        self.assertTrue(
            EXPECTED_LEGACY_RULES.issubset(found),
            f"missing rules: {EXPECTED_LEGACY_RULES - found}; got {found}",
        )
        leaked = found & EXCLUDED_FROM_LEGACY
        self.assertFalse(leaked, f"unexpected excluded rules on legacy: {leaked}")

    def test_acme_clean_has_zero_findings(self):
        mod = self._module("acme_clean")
        self.assertEqual(mod["findings"], [])
        self.assertEqual(mod["effort_points"], 0)

    def test_acme_legacy_manifest_meta(self):
        mod = self._module("acme_legacy")
        self.assertEqual(mod["version"], "18.0.1.0.0")
        self.assertIn("ACME", mod["author"])
        self.assertGreater(mod["file_counts"]["py"], 0)
        self.assertGreater(mod["file_counts"]["js"], 0)
        self.assertGreater(mod["file_counts"]["xml"], 0)
        self.assertGreater(mod["effort_points"], 0)

    def test_finding_shape(self):
        mod = self._module("acme_legacy")
        finding = mod["findings"][0]
        for key in (
            "rule_id",
            "severity",
            "file",
            "occurrences",
            "lines",
            "first_excerpt",
            "fix_hint",
            "source_url",
        ):
            self.assertIn(key, finding)
        self.assertIn(finding["severity"], ("blocker", "major", "minor"))
        self.assertIsInstance(finding["lines"], list)
        self.assertEqual(len(finding["lines"]), min(20, finding["occurrences"]))
        self.assertGreaterEqual(finding["occurrences"], 1)
        self.assertLessEqual(len(finding["first_excerpt"]), 120)

    def test_effort_scoring(self):
        mod = self._module("acme_legacy")
        expected = 0.0
        for f in mod["findings"]:
            if f["severity"] == "blocker":
                expected += 5
            elif f["severity"] == "major":
                expected += 2
            elif f["severity"] == "minor":
                expected += 0.5
        self.assertEqual(mod["effort_points"], expected)
        total_occ = sum(
            f["occurrences"] for m in self.result["modules"] for f in m["findings"]
        )
        self.assertEqual(self.result["totals"]["occurrences"], total_occ)

    def test_group_same_file_t_esc_counts_once(self):
        """3 t-esc in one XML file → 1 OWL2_API group, occurrences=3, effort=2."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mod_dir = root / "acme_tesc"
            static = mod_dir / "static" / "src" / "xml"
            static.mkdir(parents=True)
            (mod_dir / "__manifest__.py").write_text(
                "{'name': 'acme_tesc', 'version': '18.0.1.0.0', 'author': 'ACME', 'depends': ['base']}",
                encoding="utf-8",
            )
            (mod_dir / "__init__.py").write_text("", encoding="utf-8")
            (static / "template.xml").write_text(
                "\n".join(
                    [
                        '<?xml version="1.0" encoding="UTF-8"?>',
                        "<templates>",
                        '  <t t-name="acme.One"><span t-esc="a"/></t>',
                        '  <t t-name="acme.Two"><span t-esc="b"/></t>',
                        '  <t t-name="acme.Three"><span t-esc="c"/></t>',
                        "</templates>",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            result = self.scan.scan_addons_dir(str(root), target=20)
            self.assertEqual(len(result["modules"]), 1)
            mod = result["modules"][0]
            owl = [f for f in mod["findings"] if f["rule_id"] == "OWL2_API"]
            self.assertEqual(len(owl), 1, owl)
            group = owl[0]
            self.assertEqual(group["occurrences"], 3)
            self.assertEqual(group["lines"], [3, 4, 5])
            self.assertEqual(group["severity"], "major")
            self.assertEqual(mod["effort_points"], 2.0)
            self.assertEqual(result["totals"]["majors"], 1)
            self.assertEqual(result["totals"]["occurrences"], 3)
            self.assertEqual(result["totals"]["effort_points"], 2.0)

            text = self.scan.format_text(result)
            self.assertIn("OWL2_API", text)
            self.assertIn("×3", text)
            self.assertRegex(text, r"\[major\] OWL2_API .+ ×3 \(l\. 3, 4, 5\)")

    def test_removed_depends_constant_documented(self):
        self.assertTrue(hasattr(self.scan, "REMOVED_OR_MERGED_MODULES"))
        src = Path(self.scan.__file__).read_text(encoding="utf-8")
        self.assertIn("vérifié sur l'arborescence odoo/odoo 20.0 le 2026-09-24", src)
        self.assertIn("stock_picking_batch", self.scan.REMOVED_OR_MERGED_MODULES)
        self.assertIn("base_vat", self.scan.REMOVED_OR_MERGED_MODULES)

    def test_industry_fsm_prefix(self):
        # Prefix match: any module starting with industry_fsm
        self.assertTrue(
            self.scan.is_removed_or_merged_module("industry_fsm_report")
        )

    def test_cli_json_stdout(self):
        proc = subprocess.run(
            [sys.executable, str(SCAN), str(FIXTURES), "--format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["rules_version"], "2026-09-24")

    def test_cli_text_format(self):
        proc = subprocess.run(
            [sys.executable, str(SCAN), str(FIXTURES), "--format", "text"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("acme_legacy", proc.stdout)
        self.assertIn("ACCESS_CSV", proc.stdout)

    def test_cli_usage_error(self):
        proc = subprocess.run(
            [sys.executable, str(SCAN)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)

    def test_manifest_not_executed(self):
        # Guard: scanner must use literal_eval, never exec on manifests
        src = Path(self.scan.__file__).read_text(encoding="utf-8")
        self.assertIn("literal_eval", src)
        self.assertNotRegex(src, r"\bexec\(")
        self.assertNotRegex(src, r"\b__import__\(")


if __name__ == "__main__":
    unittest.main()
