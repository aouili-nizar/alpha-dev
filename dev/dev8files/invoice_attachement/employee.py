# -*- coding: utf-8 -*-
from openerp import fields, models, api


class attach(models.Model):
    _inherit = "hr.employee"

    attach = fields.Binary(string='Piéce jointe', required="true" , help="si vous avez plusieur ficher , scanner les  dans un seule . ")
    tva1 = fields.Char("TVA")


