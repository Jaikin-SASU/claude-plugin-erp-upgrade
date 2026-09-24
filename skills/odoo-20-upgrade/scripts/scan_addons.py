#!/usr/bin/env python3
"""Read-only static scanner for Odoo addon migration readiness (target 20).

Standard library only. Never exec/import manifests — use ast.literal_eval.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

RULES_VERSION = "2026-09-24"

# vérifié sur l'arborescence odoo/odoo 20.0 le 2026-09-24 (Community)
REMOVED_OR_MERGED_MODULES: Set[str] = {
    "base_vat",
    "base_iban",
    "stock_picking_batch",
    "website_sale_wishlist",
    "website_sale_comparison",
    "hr_org_chart",
    "hr_homeworking",
    "delivery_mondialrelay",
    "transifex",
    "l10n_fr_hr_work_entry_holidays",
    "hr_work_entry_holidays",
    "industry_fsm",
}

EFFORT = {"blocker": 5.0, "major": 2.0, "minor": 0.5}

OWL2_PATTERNS = (
    "useState(",
    "reactive(",
    "onWillUpdateProps",
    "t-esc=",
    "t-portal",
    "useComponent(",
    "useExternalListener(",
)

Finding = Dict[str, Any]


def group_findings(findings: Sequence[Finding]) -> List[Finding]:
    """Collapse raw line hits into one group per (rule_id, file)."""
    order: List[Tuple[str, str]] = []
    buckets: Dict[Tuple[str, str], List[Finding]] = {}
    for raw in findings:
        key = (str(raw["rule_id"]), str(raw["file"]))
        if key not in buckets:
            buckets[key] = []
            order.append(key)
        buckets[key].append(raw)

    grouped: List[Finding] = []
    for key in order:
        items = buckets[key]
        first = items[0]
        lines = [int(item["line"]) for item in items][:20]
        grouped.append(
            {
                "rule_id": first["rule_id"],
                "severity": first["severity"],
                "file": first["file"],
                "occurrences": len(items),
                "lines": lines,
                "first_excerpt": first["excerpt"],
                "fix_hint": first["fix_hint"],
                "source_url": first["source_url"],
            }
        )
    return grouped


def is_removed_or_merged_module(name: str) -> bool:
    if name in REMOVED_OR_MERGED_MODULES:
        return True
    if name.startswith("industry_fsm"):
        return True
    return False


def _excerpt(text: str, limit: int = 120) -> str:
    one_line = " ".join(text.strip().split())
    if len(one_line) <= limit:
        return one_line
    return one_line[: limit - 1] + "…"


def _finding(
    rule_id: str,
    severity: str,
    file: Path,
    line: int,
    excerpt: str,
    fix_hint: str,
    source_url: str,
    root: Path,
) -> Finding:
    try:
        rel = str(file.relative_to(root))
    except ValueError:
        rel = str(file)
    return {
        "rule_id": rule_id,
        "severity": severity,
        "file": rel,
        "line": line,
        "excerpt": _excerpt(excerpt),
        "fix_hint": fix_hint,
        "source_url": source_url,
    }


def _strip_python_comments(source: str) -> str:
    """Best-effort: drop full-line and trailing # comments outside strings."""
    out: List[str] = []
    for line in source.splitlines():
        in_single = False
        in_double = False
        buf: List[str] = []
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == "'" and not in_double:
                in_single = not in_single
                buf.append(ch)
            elif ch == '"' and not in_single:
                in_double = not in_double
                buf.append(ch)
            elif ch == "#" and not in_single and not in_double:
                break
            else:
                buf.append(ch)
            i += 1
        out.append("".join(buf))
    return "\n".join(out)


def _iter_files(module_dir: Path) -> Iterable[Path]:
    for path in module_dir.rglob("*"):
        if not path.is_file():
            continue
        if any(part.startswith(".") for part in path.parts):
            continue
        if "__pycache__" in path.parts:
            continue
        yield path


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="replace")


def load_manifest(manifest_path: Path) -> Dict[str, Any]:
    raw = _read_text(manifest_path)
    data = ast.literal_eval(raw)
    if not isinstance(data, dict):
        raise ValueError(f"manifest is not a dict: {manifest_path}")
    return data


def discover_modules(addons_dir: Path) -> List[Path]:
    modules: List[Path] = []
    if not addons_dir.is_dir():
        return modules
    for child in sorted(addons_dir.iterdir()):
        if child.is_dir() and (child / "__manifest__.py").is_file():
            modules.append(child)
    return modules


def _line_of(content: str, index: int) -> int:
    return content.count("\n", 0, index) + 1


def _search_lines(
    content: str,
    pattern: re.Pattern[str],
    *,
    strip_py_comments: bool = False,
) -> List[Tuple[int, str]]:
    text = _strip_python_comments(content) if strip_py_comments else content
    hits: List[Tuple[int, str]] = []
    # Map stripped lines back to original line numbers when possible
    original_lines = content.splitlines()
    scan_lines = text.splitlines() if strip_py_comments else original_lines
    for i, line in enumerate(scan_lines):
        if pattern.search(line):
            hits.append((i + 1, original_lines[i] if i < len(original_lines) else line))
    return hits


def scan_module(module_dir: Path, target: int = 20) -> Dict[str, Any]:
    root = module_dir
    manifest_path = module_dir / "__manifest__.py"
    manifest = load_manifest(manifest_path)
    findings: List[Finding] = []

    def add(
        rule_id: str,
        severity: str,
        file: Path,
        line: int,
        excerpt: str,
        fix_hint: str,
        source_url: str,
    ) -> None:
        findings.append(
            _finding(rule_id, severity, file, line, excerpt, fix_hint, source_url, root)
        )

    # --- ACCESS_CSV ---
    for path in _iter_files(module_dir):
        if path.name == "ir.model.access.csv" or (
            path.parent.name == "security" and path.name == "ir.model.access.csv"
        ):
            add(
                "ACCESS_CSV",
                "blocker",
                path,
                1,
                path.name,
                "Convert to ir.access.csv (id,name,model_id,group_id/id,operation,domain).",
                "https://github.com/odoo/odoo/pull/166359",
            )

    # --- REMOVED_DEPENDS ---
    depends = manifest.get("depends") or []
    if isinstance(depends, (list, tuple)):
        for dep in depends:
            if isinstance(dep, str) and is_removed_or_merged_module(dep):
                add(
                    "REMOVED_DEPENDS",
                    "blocker",
                    manifest_path,
                    1,
                    f"depends: {dep}",
                    f"Remove or replace dependency on removed/merged module '{dep}'.",
                    "https://www.odoo.com/odoo-20-release-notes",
                )

    py_count = js_count = xml_count = 0

    for path in _iter_files(module_dir):
        suffix = path.suffix.lower()
        if suffix == ".py":
            py_count += 1
            _scan_python(path, add)
        elif suffix == ".js":
            js_count += 1
            _scan_js(path, add)
        elif suffix == ".xml":
            xml_count += 1
            _scan_xml(path, add)

    grouped = group_findings(findings)
    effort = sum(EFFORT.get(f["severity"], 0) for f in grouped)

    return {
        "name": module_dir.name,
        "version": str(manifest.get("version") or ""),
        "author": str(manifest.get("author") or ""),
        "file_counts": {"py": py_count, "js": js_count, "xml": xml_count},
        "findings": grouped,
        "effort_points": effort,
        "target": target,
    }


def _scan_python(path: Path, add) -> None:
    content = _read_text(path)
    src_url_access = "https://github.com/odoo/odoo/pull/166359"
    src_read_group = (
        "https://github.com/odoo/odoo/commit/cfeab5eefe8818559ecaa6901857ff0e346aa885"
    )
    src_tracking = "https://www.odoo.com/odoo-20-release-notes"
    src_table = (
        "https://www.odoo.com/documentation/20.0/developer/reference/backend/"
        "orm/changelog.html"
    )
    src_jsonrpc = (
        "https://www.odoo.com/documentation/20.0/developer/reference/external_api.html"
    )

    # MODEL_ACCESS_REF
    for line_no, line in _search_lines(
        content, re.compile(r"['\"]ir\.model\.access['\"]"), strip_py_comments=True
    ):
        add(
            "MODEL_ACCESS_REF",
            "major",
            path,
            line_no,
            line,
            "Replace ir.model.access usage with the new ir.access API.",
            src_url_access,
        )

    # TRACKING_VALUE
    for line_no, line in _search_lines(
        content,
        re.compile(r"mail\.tracking\.value|tracking_value_ids"),
        strip_py_comments=True,
    ):
        add(
            "TRACKING_VALUE",
            "major",
            path,
            line_no,
            line,
            "mail.tracking.value / tracking_value_ids removed — migrate tracking logic.",
            src_tracking,
        )

    # TABLE_QUERY
    for line_no, line in _search_lines(
        content, re.compile(r"_table_query"), strip_py_comments=True
    ):
        add(
            "TABLE_QUERY",
            "major",
            path,
            line_no,
            line,
            "Replace _table_query with supported ORM alternatives.",
            src_table,
        )

    # CHECK_ACCESS_DEPRECATED
    for line_no, line in _search_lines(
        content,
        re.compile(r"_check_access\(|_check_field_access\("),
        strip_py_comments=True,
    ):
        add(
            "CHECK_ACCESS_DEPRECATED",
            "minor",
            path,
            line_no,
            line,
            "Replace deprecated _check_access / _check_field_access calls.",
            src_url_access,
        )

    # SQL_CONSTRAINTS
    for line_no, line in _search_lines(
        content, re.compile(r"_sql_constraints\s*="), strip_py_comments=True
    ):
        add(
            "SQL_CONSTRAINTS",
            "major",
            path,
            line_no,
            line,
            "Replace _sql_constraints with models.Constraint (since 18.1).",
            "https://www.odoo.com/documentation/20.0/developer/reference/backend/orm/changelog.html",
        )

    # JSON_ROUTE
    for line_no, line in _search_lines(
        content,
        re.compile(r"""type\s*=\s*['"]json['"]"""),
        strip_py_comments=True,
    ):
        add(
            "JSON_ROUTE",
            "major",
            path,
            line_no,
            line,
            "Change @http.route type='json' to type='jsonrpc' (since 18.1).",
            "https://www.odoo.com/documentation/20.0/developer/reference/backend/http.html",
        )

    # CR_UID_CONTEXT
    for line_no, line in _search_lines(
        content,
        re.compile(r"\._cr\b|\._uid\b|\._context\b"),
        strip_py_comments=True,
    ):
        add(
            "CR_UID_CONTEXT",
            "minor",
            path,
            line_no,
            line,
            "Avoid private ._cr / ._uid / ._context (deprecated since 19.0).",
            "https://www.odoo.com/documentation/20.0/developer/reference/backend/orm/changelog.html",
        )

    # XMLRPC_CLIENT
    for line_no, line in _search_lines(
        content,
        re.compile(r"xmlrpc\.client|/xmlrpc/2|/jsonrpc"),
        strip_py_comments=True,
    ):
        add(
            "XMLRPC_CLIENT",
            "major",
            path,
            line_no,
            line,
            "External XML-RPC/JSON-RPC APIs are deprecated; prefer JSON-2 where available.",
            src_jsonrpc,
        )

    # READ_GROUP_OLD — heuristic on call sites
    _scan_read_group(content, path, add, src_read_group)


def _scan_read_group(content: str, path: Path, add, source_url: str) -> None:
    """Detect old read_group usage: lazy=, fields=, or 3+ positional args."""
    try:
        tree = ast.parse(content)
    except SyntaxError:
        # Fallback regex
        for line_no, line in _search_lines(
            content,
            re.compile(r"\.read_group\("),
            strip_py_comments=True,
        ):
            window = "\n".join(content.splitlines()[line_no - 1 : line_no + 8])
            if re.search(r"lazy\s*=", window) or re.search(r"fields\s*=", window):
                add(
                    "READ_GROUP_OLD",
                    "major",
                    path,
                    line_no,
                    line,
                    "Update read_group to the new signature (no lazy=, no fields list).",
                    source_url,
                )
        return

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
            name = None
            if isinstance(node.func, ast.Attribute) and node.func.attr == "read_group":
                name = "read_group"
            if name == "read_group":
                has_lazy = any(kw.arg == "lazy" for kw in node.keywords if kw.arg)
                has_fields = any(kw.arg == "fields" for kw in node.keywords if kw.arg)
                # 3 positional args beyond self/domain heuristic: domain, fields, groupby
                positional = len(node.args)
                old = has_lazy or has_fields or positional >= 3
                if old:
                    line_no = getattr(node, "lineno", 1)
                    lines = content.splitlines()
                    excerpt = lines[line_no - 1] if 0 < line_no <= len(lines) else "read_group"
                    add(
                        "READ_GROUP_OLD",
                        "major",
                        path,
                        line_no,
                        excerpt,
                        "Update read_group to the new signature (no lazy=, no fields list).",
                        source_url,
                    )
            self.generic_visit(node)

    Visitor().visit(tree)


def _scan_js(path: Path, add) -> None:
    content = _read_text(path)
    owl_src = "https://github.com/odoo/owl/blob/master/doc/v3/owl/migration_owl2_to_owl3.md"

    for pat in OWL2_PATTERNS:
        for line_no, line in _search_lines(content, re.compile(re.escape(pat))):
            add(
                "OWL2_API",
                "major",
                path,
                line_no,
                line,
                f"OWL 2 API '{pat.rstrip('(')}' — migrate to OWL 3.",
                owl_src,
            )

    for line_no, line in _search_lines(content, re.compile(r"odoo\.define\(")):
        add(
            "ODOO_DEFINE",
            "major",
            path,
            line_no,
            line,
            "Replace odoo.define with ES module / @odoo-module imports.",
            owl_src,
        )

    for line_no, line in _search_lines(
        content, re.compile(r"xmlrpc\.client|/xmlrpc/2|/jsonrpc")
    ):
        add(
            "XMLRPC_CLIENT",
            "major",
            path,
            line_no,
            line,
            "External XML-RPC/JSON-RPC APIs are deprecated; prefer JSON-2 where available.",
            "https://www.odoo.com/documentation/20.0/developer/reference/external_api.html",
        )


def _scan_xml(path: Path, add) -> None:
    content = _read_text(path)
    access_src = "https://github.com/odoo/odoo/pull/166359"
    owl_src = "https://github.com/odoo/owl/blob/master/doc/v3/owl/migration_owl2_to_owl3.md"

    # IR_RULE
    for line_no, line in _search_lines(
        content, re.compile(r"""model\s*=\s*["']ir\.rule["']""")
    ):
        add(
            "IR_RULE",
            "blocker",
            path,
            line_no,
            line,
            "Convert ir.rule records to the new ir.access model.",
            access_src,
        )

    # ATTRS_STATES
    for line_no, line in _search_lines(
        content, re.compile(r"\battrs\s*=|\bstates\s*=")
    ):
        add(
            "ATTRS_STATES",
            "blocker",
            path,
            line_no,
            line,
            "Replace attrs=/states= with invisible/readonly/required expressions (removed in 17.0).",
            "https://www.odoo.com/documentation/17.0/developer/reference/backend/views.html",
        )

    # TREE_VIEW — <tree or view_mode containing 'tree'
    for line_no, line in _search_lines(
        content, re.compile(r"<tree\b|view_mode[^<]*\btree\b")
    ):
        add(
            "TREE_VIEW",
            "major",
            path,
            line_no,
            line,
            "Replace <tree> / view_mode 'tree' with list (since 17.5).",
            "https://www.odoo.com/documentation/18.0/developer/reference/backend/views.html",
        )

    # FA_ICONS
    for line_no, line in _search_lines(
        content, re.compile(r"""["'][^"']*\bfa\s+fa-|["'][^"']*\bfa-""")
    ):
        add(
            "FA_ICONS",
            "minor",
            path,
            line_no,
            line,
            "Replace Font Awesome (fa-) classes with Material Symbols (Odoo 20).",
            "https://www.odoo.com/odoo-20-release-notes",
        )

    # OWL2 in static XML templates
    if "static" in path.parts:
        for pat in OWL2_PATTERNS:
            for line_no, line in _search_lines(content, re.compile(re.escape(pat))):
                add(
                    "OWL2_API",
                    "major",
                    path,
                    line_no,
                    line,
                    f"OWL 2 API '{pat.rstrip('(')}' — migrate to OWL 3.",
                    owl_src,
                )


def scan_addons_dir(addons_path: str, target: int = 20) -> Dict[str, Any]:
    addons_dir = Path(addons_path).resolve()
    modules = [scan_module(m, target=target) for m in discover_modules(addons_dir)]
    blockers = majors = minors = 0
    occurrences = 0
    effort = 0.0
    for mod in modules:
        for f in mod["findings"]:
            occurrences += int(f["occurrences"])
            if f["severity"] == "blocker":
                blockers += 1
            elif f["severity"] == "major":
                majors += 1
            elif f["severity"] == "minor":
                minors += 1
        effort += float(mod["effort_points"])
    return {
        "scanned_on": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "target": target,
        "modules": modules,
        "totals": {
            "blockers": blockers,
            "majors": majors,
            "minors": minors,
            "effort_points": effort,
            "occurrences": occurrences,
        },
        "rules_version": RULES_VERSION,
    }


def _format_group_line(f: Finding) -> str:
    line_nums = ", ".join(str(n) for n in f["lines"])
    if int(f["occurrences"]) > len(f["lines"]):
        line_nums += "…"
    return (
        f"  [{f['severity']}] {f['rule_id']} {f['file']} ×{f['occurrences']} "
        f"(l. {line_nums}) — {f['first_excerpt']}"
    )


def format_text(result: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append(
        f"Odoo {result['target']} migration scan — rules {result['rules_version']}"
        f" — {result['scanned_on']}"
    )
    totals = result["totals"]
    lines.append(
        f"Totals: {totals['blockers']} blockers, {totals['majors']} majors, "
        f"{totals['minors']} minors, effort={totals['effort_points']}, "
        f"occurrences={totals['occurrences']}"
    )
    for mod in result["modules"]:
        lines.append("")
        lines.append(
            f"## {mod['name']} v{mod['version']} ({mod['author']}) "
            f"— effort {mod['effort_points']}"
        )
        if not mod["findings"]:
            lines.append("  (no findings)")
            continue
        for f in mod["findings"]:
            lines.append(_format_group_line(f))
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scan Odoo addons for Odoo 20 migration readiness (read-only)."
    )
    parser.add_argument("addons_dir", help="Path to addons directory")
    parser.add_argument("--target", type=int, default=20, help="Target major version")
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        dest="fmt",
        help="Output format",
    )
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 2
        return 2 if code else 0

    addons = Path(args.addons_dir)
    if not addons.is_dir():
        print(f"error: not a directory: {addons}", file=sys.stderr)
        return 2

    try:
        result = scan_addons_dir(str(addons), target=args.target)
    except (OSError, ValueError, SyntaxError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.fmt == "text":
        sys.stdout.write(format_text(result))
    else:
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
