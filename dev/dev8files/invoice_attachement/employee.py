# -*- coding: utf-8 -*-
from openerp import fields, models, api


class attach(models.Model):
    _inherit = "hr.employee"

    tva1 = fields.Char("TVA")


