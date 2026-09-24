# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class AcmeLegacyHttp(http.Controller):
    @http.route("/acme/legacy/json", type="json", auth="user")
    def legacy_json(self):
        return {"ok": True}
