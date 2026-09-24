# -*- coding: utf-8 -*-
from odoo import models, fields


class AcmeClean(models.Model):
    _name = "acme.clean"
    _description = "ACME Clean"

    name = fields.Char()
