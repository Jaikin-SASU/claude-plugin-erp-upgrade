# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.http import request, route


class AcmeLegacy(models.Model):
    _name = "acme.legacy"
    _description = "ACME Legacy"
    _sql_constraints = [
        ("name_uniq", "unique(name)", "Name must be unique."),
    ]

    name = fields.Char()
    active = fields.Boolean(default=True)

    def action_group(self):
        # Old read_group signature with fields list and lazy=
        return self.env["acme.legacy"].read_group(
            [("active", "=", True)],
            ["name"],
            ["name"],
            lazy=False,
        )

    def action_tracking(self):
        Tracking = self.env["mail.tracking.value"]
        return Tracking.search([])

    def action_model_access(self):
        return self.env["ir.model.access"].search([])

    def action_cr(self):
        cr = self._cr
        return cr

    @api.model
    def create(self, vals):
        return super().create(vals)


class AcmeLegacyController(models.AbstractModel):
    _name = "acme.legacy.controller"
    _description = "Placeholder so controllers stay in package"
