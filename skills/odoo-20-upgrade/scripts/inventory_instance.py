#!/usr/bin/env python3
"""Read-only Odoo instance inventory for migration readiness.

The API key is typed by the user at a hidden prompt, or piped on stdin with
--api-key-stdin (e.g. from a password manager). It is never read from shell
variables or files, never accepted as a CLI argument, never printed or
persisted.
Standard library only.
"""

from __future__ import annotations

import argparse
import getpass
import json
import sys
import xmlrpc.client
from typing import Any, Dict, List, Optional, Sequence, Set
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ALLOWED_METHODS: Set[str] = {"search_read", "search_count", "read", "fields_get"}

MODULE_FIELDS = [
    "name",
    "author",
    "website",
    "installed_version",
    "license",
]


class WhitelistError(Exception):
    """Raised when a non-whitelisted ORM method is requested."""


class ConnectionError(Exception):
    """Raised on connection / authentication failures."""


def _parse_major(version: Any) -> int:
    if isinstance(version, dict):
        info = version.get("server_version_info") or version.get("version_info")
        if isinstance(info, (list, tuple)) and info:
            return int(info[0])
        ver = version.get("server_version") or version.get("version") or ""
        return _parse_major(ver)
    text = str(version).strip()
    if not text:
        return 0
    major = text.split(".", 1)[0]
    try:
        return int(major)
    except ValueError:
        return 0


def classify_module(mod: Dict[str, Any]) -> str:
    author = str(mod.get("author") or "")
    website = str(mod.get("website") or "")
    if "Odoo S.A." in author:
        return "odoo"
    if "Odoo Community Association" in author or "github.com/OCA" in website:
        return "oca"
    if website and website not in ("False", "None"):
        return "third_party"
    return "custom"


class OdooReadClient:
    """Read-only Odoo client with a hard method whitelist."""

    def __init__(
        self,
        url: str,
        db: str,
        *,
        api_key: str,
        login: Optional[str] = None,
    ) -> None:
        self.url = url.rstrip("/")
        self.db = db
        self.api_key = api_key
        self.login = login or ""
        self.server_version: str = ""
        self.major: int = 0
        self.protocol: str = ""
        self._uid: Optional[int] = None

    def detect_version(self) -> str:
        # 1) GET /web/version
        try:
            req = Request(f"{self.url}/web/version", method="GET")
            with urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            self.server_version = str(
                data.get("version")
                or data.get("server_version")
                or (data.get("version_info") or [""])[0]
            )
            if isinstance(data.get("version_info"), list) and data["version_info"]:
                self.major = int(data["version_info"][0])
            else:
                self.major = _parse_major(data)
            self._set_protocol()
            return self.server_version
        except (URLError, HTTPError, TimeoutError, json.JSONDecodeError, ValueError, OSError):
            pass

        # 2) JSON-RPC 'version'
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {"service": "common", "method": "version", "args": []},
                "id": 1,
            }
            req = Request(
                f"{self.url}/jsonrpc",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            result = data.get("result") or {}
            self.server_version = str(
                result.get("server_version") or result.get("version") or ""
            )
            self.major = _parse_major(result)
            self._set_protocol()
            return self.server_version
        except (URLError, HTTPError, TimeoutError, json.JSONDecodeError, ValueError, OSError):
            pass

        # 3) XML-RPC common.version
        try:
            common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
            result = common.version()
            self.server_version = str(
                result.get("server_version") or result.get("version") or ""
            )
            self.major = _parse_major(result)
            self._set_protocol()
            return self.server_version
        except (OSError, xmlrpc.client.Fault, xmlrpc.client.ProtocolError) as exc:
            raise ConnectionError(f"cannot detect Odoo version: {exc}") from exc

    def _set_protocol(self) -> None:
        if self.major >= 19:
            self.protocol = "json2"
        else:
            self.protocol = "xmlrpc"

    def _ensure_xmlrpc_auth(self) -> None:
        if self._uid is not None:
            return
        if not self.login:
            raise ConnectionError("login required for XML-RPC authenticate")
        common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        uid = common.authenticate(self.db, self.login, self.api_key, {})
        if not uid:
            raise ConnectionError("XML-RPC authenticate failed")
        self._uid = int(uid)

    def call(self, model: str, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        if method not in ALLOWED_METHODS:
            raise WhitelistError(
                f"method {method!r} is not on the read-only whitelist "
                f"{sorted(ALLOWED_METHODS)}"
            )
        params = dict(params or {})
        if not self.protocol:
            self.detect_version()
        if self.protocol == "json2":
            return self._call_json2(model, method, params)
        return self._call_xmlrpc(model, method, params)

    def _call_json2(self, model: str, method: str, params: Dict[str, Any]) -> Any:
        url = f"{self.url}/json/2/{model}/{method}"
        body = json.dumps(params).encode("utf-8")
        req = Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"bearer {self.api_key}",
                "X-Odoo-Database": self.db,
            },
            method="POST",
        )
        try:
            with urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8")
        except HTTPError as exc:
            try:
                detail = exc.read().decode("utf-8", errors="replace")
            finally:
                exc.close()
            raise PermissionError(
                f"access error on {model}.{method}: {exc.code} {detail}"
            ) from None
        except (URLError, TimeoutError, OSError) as exc:
            raise ConnectionError(f"JSON-2 call failed: {exc}") from exc
        if not raw:
            return None
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ConnectionError(f"invalid JSON-2 response: {exc}") from exc
        if isinstance(data, dict) and data.get("error"):
            raise PermissionError(f"access error on {model}.{method}: {data['error']}")
        # JSON-2 may return the result directly or wrapped
        if isinstance(data, dict) and "result" in data and set(data.keys()) <= {
            "result",
            "jsonrpc",
            "id",
        }:
            return data["result"]
        return data

    def _call_xmlrpc(self, model: str, method: str, params: Dict[str, Any]) -> Any:
        self._ensure_xmlrpc_auth()
        models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        args: List[Any] = []
        kwargs: Dict[str, Any] = {}
        if method == "search_read":
            args = [params.get("domain", [])]
            kwargs = {
                k: v
                for k, v in params.items()
                if k != "domain" and v is not None
            }
        elif method == "search_count":
            args = [params.get("domain", [])]
            kwargs = {k: v for k, v in params.items() if k != "domain"}
        elif method == "read":
            args = [params.get("ids", [])]
            if "fields" in params:
                kwargs["fields"] = params["fields"]
        elif method == "fields_get":
            allfields = params.get("allfields")
            args = [allfields] if allfields is not None else []
            kwargs = {k: v for k, v in params.items() if k != "allfields"}
        try:
            return models.execute_kw(
                self.db, self._uid, self.api_key, model, method, args, kwargs
            )
        except xmlrpc.client.Fault as exc:
            raise PermissionError(f"access error on {model}.{method}: {exc}") from exc
        except (OSError, xmlrpc.client.ProtocolError) as exc:
            raise ConnectionError(f"XML-RPC call failed: {exc}") from exc


def _safe_count(
    client: OdooReadClient,
    model: str,
    domain: List[Any],
    notes: List[str],
) -> Optional[int]:
    try:
        return int(client.call(model, "search_count", {"domain": domain}))
    except (PermissionError, ConnectionError, WhitelistError, TypeError, ValueError) as exc:
        notes.append(f"{model}: {exc.__class__.__name__}")
        return None


def inventory_instance(
    url: str,
    db: str,
    *,
    login: Optional[str] = None,
    api_key: str,
) -> Dict[str, Any]:
    if not api_key:
        raise ConnectionError("an Odoo API key is required")

    client = OdooReadClient(url, db, api_key=api_key, login=login)
    version = client.detect_version()
    notes: List[str] = []

    modules_raw: List[Dict[str, Any]] = []
    try:
        modules_raw = client.call(
            "ir.module.module",
            "search_read",
            {
                "domain": [("state", "=", "installed")],
                "fields": MODULE_FIELDS,
            },
        ) or []
    except (PermissionError, ConnectionError) as exc:
        notes.append(f"ir.module.module: {exc.__class__.__name__}")

    categories: Dict[str, List[Dict[str, Any]]] = {
        "odoo": [],
        "oca": [],
        "third_party": [],
        "custom": [],
    }
    for mod in modules_raw:
        entry = {
            "name": mod.get("name"),
            "author": mod.get("author") or "",
            "website": mod.get("website") or "",
            "installed_version": mod.get("installed_version") or "",
            "license": mod.get("license") or "",
        }
        # Normalize False from XML-RPC
        if entry["website"] in (False, "False"):
            entry["website"] = ""
        categories[classify_module(entry)].append(entry)

    studio_fields = _safe_count(
        client,
        "ir.model.fields",
        [("name", "=like", "x_%"), ("state", "=", "manual")],
        notes,
    )
    studio_views = _safe_count(
        client,
        "ir.ui.view",
        [("name", "ilike", "studio")],
        notes,
    )
    automated_actions = _safe_count(client, "base.automation", [], notes)
    server_actions_code = _safe_count(
        client,
        "ir.actions.server",
        [("state", "=", "code")],
        notes,
    )
    internal_users = _safe_count(
        client,
        "res.users",
        [("share", "=", False), ("active", "=", True)],
        notes,
    )
    employees_without_user = _safe_count(
        client,
        "hr.employee",
        [("user_id", "=", False), ("active", "=", True)],
        notes,
    )
    api_keys_count = _safe_count(client, "res.users.apikeys", [], notes)

    light_user_indicator: Optional[Dict[str, Any]] = None
    if internal_users is not None or employees_without_user is not None:
        light_user_indicator = {
            "internal_users": internal_users,
            "employees_without_user": employees_without_user,
            "note": (
                "Employees without a linked user may be billed as Light Users "
                "under Enterprise contract v13 (2026-09-24)."
            ),
        }

    return {
        "server_version": version,
        "protocol": client.protocol,
        "database": db,
        "modules": categories,
        "studio_fields": studio_fields,
        "studio_views": studio_views,
        "automated_actions": automated_actions,
        "server_actions_code": server_actions_code,
        "internal_users": internal_users,
        "employees_without_user": employees_without_user,
        "light_user_indicator": light_user_indicator,
        "api_keys_count": api_keys_count,
        "notes": notes,
    }


def format_text(result: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append(
        f"Odoo instance inventory — {result.get('server_version')} "
        f"(protocol={result.get('protocol')}, db={result.get('database')})"
    )
    mods = result.get("modules") or {}
    for cat in ("odoo", "oca", "third_party", "custom"):
        items = mods.get(cat) or []
        lines.append(f"  {cat}: {len(items)}")
        for m in items:
            lines.append(f"    - {m.get('name')} ({m.get('installed_version')})")
    lines.append(f"Studio fields: {result.get('studio_fields')}")
    lines.append(f"Studio views: {result.get('studio_views')}")
    lines.append(f"Automated actions: {result.get('automated_actions')}")
    lines.append(f"Server actions (code): {result.get('server_actions_code')}")
    lines.append(f"Internal users: {result.get('internal_users')}")
    lines.append(f"Employees without user: {result.get('employees_without_user')}")
    lines.append(f"API keys: {result.get('api_keys_count')}")
    notes = result.get("notes") or []
    if notes:
        lines.append("Notes:")
        for n in notes:
            lines.append(f"  - {n}")
    return "\n".join(lines) + "\n"


def read_api_key(from_stdin: bool) -> str:
    """Return the API key typed at a hidden prompt or piped on stdin."""
    if from_stdin:
        return sys.stdin.readline().strip()
    if not sys.stdin.isatty():
        return ""
    return getpass.getpass("Odoo API key (hidden): ").strip()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only inventory of an Odoo instance (API key typed at a hidden prompt)."
    )
    parser.add_argument("--url", required=True, help="Base URL of the Odoo instance")
    parser.add_argument("--db", required=True, help="Database name")
    parser.add_argument("--login", default=None, help="Login (required for XML-RPC <19)")
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        dest="fmt",
        help="Output format",
    )
    parser.add_argument(
        "--api-key-stdin",
        action="store_true",
        help="Read the API key from the first line of stdin instead of prompting",
    )
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 2
        return 2 if code else 0

    key = read_api_key(args.api_key_stdin)
    if not key:
        print(
            "error: an Odoo API key is required (hidden prompt in a terminal, or --api-key-stdin)",
            file=sys.stderr,
        )
        return 2

    try:
        result = inventory_instance(args.url, args.db, login=args.login, api_key=key)
    except (ConnectionError, WhitelistError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    # Belt-and-suspenders: never leak the key
    if args.fmt == "text":
        out = format_text(result)
    else:
        out = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if key and key in out:
        out = out.replace(key, "***")
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
