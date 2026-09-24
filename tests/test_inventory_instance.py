#!/usr/bin/env python3
"""Tests for inventory_instance.py (TDD — written before implementation)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse
from xmlrpc.server import SimpleXMLRPCDispatcher

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "odoo-20-migration-readiness" / "scripts"
INVENTORY = SCRIPTS / "inventory_instance.py"

FAKE_API_KEY = "secret-test-api-key-DO-NOT-LEAK"


def _import_inventory():
    sys.path.insert(0, str(SCRIPTS))
    import inventory_instance  # noqa: WPS433

    return inventory_instance


class FakeOdooHandler(BaseHTTPRequestHandler):
    """Minimal fake Odoo HTTP surface for inventory tests."""

    server_version_label = "20.0"
    # Set on the HTTPServer instance before serving.
    mode = "json2"  # "json2" (>=19) or "xmlrpc" (<19)

    def log_message(self, format, *args):  # noqa: A003
        return

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", "0") or 0)
        return self.rfile.read(length) if length else b""

    def _send_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_xmlrpc(self, payload_xml: bytes, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/xml")
        self.send_header("Content-Length", str(len(payload_xml)))
        self.end_headers()
        self.wfile.write(payload_xml)

    def do_GET(self):  # noqa: N802
        path = urlparse(self.path).path
        if path == "/web/version":
            self._send_json(
                {
                    "version": self.server.server_version_label,
                    "version_info": [
                        int(self.server.server_version_label.split(".")[0]),
                        0,
                        0,
                        "final",
                        0,
                        "",
                    ],
                }
            )
            return
        self._send_json({"error": "not found"}, status=404)

    def do_POST(self):  # noqa: N802
        path = urlparse(self.path).path
        body = self._read_body()

        if path.startswith("/json/2/"):
            self._handle_json2(path, body)
            return
        if path.startswith("/xmlrpc/2/"):
            self._handle_xmlrpc(path, body)
            return
        # JSON-RPC fallback for version
        if path in ("/jsonrpc", "/web/dataset/call_kw"):
            try:
                data = json.loads(body.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                data = {}
            method = data.get("method") or (data.get("params") or {}).get("method")
            if method == "version" or data.get("method") == "call":
                self._send_json(
                    {
                        "jsonrpc": "2.0",
                        "id": data.get("id"),
                        "result": {
                            "server_version": self.server.server_version_label,
                            "server_version_info": [
                                int(self.server.server_version_label.split(".")[0]),
                                0,
                                0,
                                "final",
                                0,
                                "",
                            ],
                        },
                    }
                )
                return
        self._send_json({"error": "not found"}, status=404)

    def _handle_json2(self, path: str, body: bytes):
        auth = self.headers.get("Authorization", "")
        db = self.headers.get("X-Odoo-Database", "")
        if not auth.lower().startswith("bearer ") or not db:
            self._send_json({"error": "unauthorized"}, status=401)
            return
        parts = path.strip("/").split("/")
        # json/2/{model}/{method}
        if len(parts) < 4:
            self._send_json({"error": "bad path"}, status=400)
            return
        model, method = parts[2], parts[3]
        try:
            args = json.loads(body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            args = {}
        try:
            result = self.server.dispatch_odoo(model, method, args, protocol="json2")
        except PermissionError as exc:
            self._send_json({"error": str(exc)}, status=403)
            return
        except Exception as exc:  # noqa: BLE001
            self._send_json({"error": str(exc)}, status=500)
            return
        self._send_json(result)

    def _handle_xmlrpc(self, path: str, body: bytes):
        service = path.rstrip("/").split("/")[-1]
        dispatcher = SimpleXMLRPCDispatcher(allow_none=True)

        def authenticate(db, login, password, user_agent_env=None):
            if login and password:
                return 2
            return False

        def version():
            return {
                "server_version": self.server.server_version_label,
                "server_version_info": [
                    int(self.server.server_version_label.split(".")[0]),
                    0,
                    0,
                    "final",
                    0,
                    "",
                ],
            }

        def execute_kw(db, uid, password, model, method, args, kwargs=None):
            kwargs = kwargs or {}
            # Map positional execute_kw args into named-style for dispatcher
            named = dict(kwargs)
            if method == "search_read":
                named.setdefault("domain", args[0] if args else [])
                if len(args) > 1 and isinstance(args[1], list):
                    named.setdefault("fields", args[1])
            elif method == "search_count":
                named.setdefault("domain", args[0] if args else [])
            elif method == "read":
                named.setdefault("ids", args[0] if args else [])
                if len(args) > 1:
                    named.setdefault("fields", args[1])
            elif method == "fields_get":
                if args:
                    named.setdefault("allfields", args[0])
            return self.server.dispatch_odoo(model, method, named, protocol="xmlrpc")

        if service == "common":
            dispatcher.register_function(authenticate, "authenticate")
            dispatcher.register_function(version, "version")
        elif service == "object":
            dispatcher.register_function(execute_kw, "execute_kw")
        else:
            self._send_json({"error": "unknown service"}, status=404)
            return

        response = dispatcher._marshaled_dispatch(body)  # noqa: SLF001
        self._send_xmlrpc(response)


class FakeOdooServer(HTTPServer):
    def __init__(self, server_address, version_label="20.0"):
        super().__init__(server_address, FakeOdooHandler)
        self.server_version_label = version_label
        FakeOdooHandler.server_version_label = version_label
        self.access_errors = set()  # model names that raise access error

    def dispatch_odoo(self, model, method, args, protocol="json2"):
        if model in self.access_errors:
            raise PermissionError(f"Access denied on {model}")

        if method not in ("search_read", "search_count", "read", "fields_get"):
            raise ValueError(f"method not allowed in fake: {method}")

        if model == "ir.module.module" and method == "search_read":
            return [
                {
                    "id": 1,
                    "name": "sale",
                    "author": "Odoo S.A.",
                    "website": "https://www.odoo.com",
                    "installed_version": "20.0.1.0",
                    "license": "LGPL-3",
                },
                {
                    "id": 2,
                    "name": "sale_order_type",
                    "author": "Odoo Community Association (OCA)",
                    "website": "https://github.com/OCA/sale-workflow",
                    "installed_version": "20.0.1.0.0",
                    "license": "AGPL-3",
                },
                {
                    "id": 3,
                    "name": "vendor_bridge",
                    "author": "Vendor Inc",
                    "website": "https://vendor.example.com",
                    "installed_version": "1.0",
                    "license": "OPL-1",
                },
                {
                    "id": 4,
                    "name": "acme_custom",
                    "author": "ACME Corp",
                    "website": False,
                    "installed_version": "1.0",
                    "license": "LGPL-3",
                },
            ]
        if model == "ir.model.fields" and method == "search_count":
            return 3
        if model == "ir.ui.view" and method == "search_count":
            return 2
        if model == "base.automation" and method == "search_count":
            return 5
        if model == "ir.actions.server" and method == "search_count":
            return 4
        if model == "res.users" and method == "search_count":
            return 7
        if model == "hr.employee" and method == "search_count":
            return 2
        if model == "res.users.apikeys" and method == "search_count":
            return 1
        if method == "fields_get":
            return {"name": {"type": "char"}}
        if method == "search_read":
            return []
        if method == "search_count":
            return 0
        if method == "read":
            return []
        raise RuntimeError(f"unhandled {model}.{method}")


class FakeServerMixin:
    def start_fake(self, version="20.0"):
        self._httpd = FakeOdooServer(("127.0.0.1", 0), version_label=version)
        self._port = self._httpd.server_address[1]
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()
        return f"http://127.0.0.1:{self._port}"

    def stop_fake(self):
        if getattr(self, "_httpd", None):
            self._httpd.shutdown()
            self._httpd.server_close()
            self._httpd = None


class TestInventoryInstance(FakeServerMixin, unittest.TestCase):
    def setUp(self):
        self.inv = _import_inventory()
        self.url = self.start_fake("20.0")
        os.environ["ODOO_API_KEY"] = FAKE_API_KEY

    def tearDown(self):
        self.stop_fake()
        os.environ.pop("ODOO_API_KEY", None)

    def test_classify_modules(self):
        result = self.inv.inventory_instance(self.url, "testdb")
        cats = result["modules"]
        self.assertEqual(len(cats["odoo"]), 1)
        self.assertEqual(cats["odoo"][0]["name"], "sale")
        self.assertEqual(len(cats["oca"]), 1)
        self.assertEqual(cats["oca"][0]["name"], "sale_order_type")
        self.assertEqual(len(cats["third_party"]), 1)
        self.assertEqual(cats["third_party"][0]["name"], "vendor_bridge")
        self.assertEqual(len(cats["custom"]), 1)
        self.assertEqual(cats["custom"][0]["name"], "acme_custom")

    def test_collects_counts(self):
        result = self.inv.inventory_instance(self.url, "testdb")
        self.assertEqual(result["server_version"], "20.0")
        self.assertEqual(result["studio_fields"], 3)
        self.assertEqual(result["studio_views"], 2)
        self.assertEqual(result["automated_actions"], 5)
        self.assertEqual(result["server_actions_code"], 4)
        self.assertEqual(result["internal_users"], 7)
        self.assertEqual(result["employees_without_user"], 2)
        self.assertIn("light_user_indicator", result)
        self.assertEqual(result["api_keys_count"], 1)

    def test_api_key_never_in_output(self):
        result = self.inv.inventory_instance(self.url, "testdb")
        dumped = json.dumps(result)
        self.assertNotIn(FAKE_API_KEY, dumped)
        proc = subprocess.run(
            [
                sys.executable,
                str(INVENTORY),
                "--url",
                self.url,
                "--db",
                "testdb",
                "--format",
                "json",
            ],
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "ODOO_API_KEY": FAKE_API_KEY},
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn(FAKE_API_KEY, proc.stdout)
        self.assertNotIn(FAKE_API_KEY, proc.stderr)

    def test_whitelist_rejects_write(self):
        client = self.inv.OdooReadClient(
            self.url, "testdb", api_key=FAKE_API_KEY, login="admin"
        )
        client.detect_version()
        with self.assertRaises(Exception) as ctx:
            client.call("res.partner", "create", {"vals_list": [{"name": "X"}]})
        self.assertIn("white", str(ctx.exception).lower())

    def test_access_error_returns_null_note(self):
        self._httpd.access_errors.add("hr.employee")
        result = self.inv.inventory_instance(self.url, "testdb")
        self.assertIsNone(result["employees_without_user"])
        notes = result.get("notes") or []
        self.assertTrue(any("hr.employee" in n for n in notes))

    def test_cli_usage_without_key(self):
        env = {k: v for k, v in os.environ.items() if k != "ODOO_API_KEY"}
        proc = subprocess.run(
            [
                sys.executable,
                str(INVENTORY),
                "--url",
                self.url,
                "--db",
                "testdb",
            ],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
        self.assertEqual(proc.returncode, 2)

    def test_cli_usage_missing_args(self):
        proc = subprocess.run(
            [sys.executable, str(INVENTORY)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)


class TestInventoryXmlrpcFallback(FakeServerMixin, unittest.TestCase):
    def setUp(self):
        self.inv = _import_inventory()
        self.url = self.start_fake("17.0")
        os.environ["ODOO_API_KEY"] = FAKE_API_KEY

    def tearDown(self):
        self.stop_fake()
        os.environ.pop("ODOO_API_KEY", None)

    def test_xmlrpc_path_for_v17(self):
        result = self.inv.inventory_instance(
            self.url, "testdb", login="admin"
        )
        self.assertTrue(str(result["server_version"]).startswith("17"))
        self.assertEqual(result["protocol"], "xmlrpc")
        self.assertEqual(len(result["modules"]["odoo"]), 1)
        self.assertNotIn(FAKE_API_KEY, json.dumps(result))


if __name__ == "__main__":
    unittest.main()
