# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp import models, fields, api, _
from openerp.tools.translate import _
#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------


class add_comp(models.Model):
    _inherit="res.company"

    catg = fields.Integer('Code cetégorie')
    nsec = fields.Integer('Numero etablissement secondaire')

class add_part(models.Model):
    _inherit="res.partner"

    cin = fields.Integer('Numero Cin')
    passport = fields.Integer('Numero passeport')
    tva = fields.Integer('Code TVA')
    catg = fields.Integer('Code catégorie')
    nsec = fields.Integer('Numero etablissement secondaire')

