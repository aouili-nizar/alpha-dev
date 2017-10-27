# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp import models, fields, api, _
from openerp.tools.translate import _
#-------------------------------------------------------------------------------
# wizard_resume_paie
#-------------------------------------------------------------------------------


class ret_taux(models.Model):
    _name="taux_rs"
    _rec_name="nom"
    code = fields.Integer('Code du taxe')
    nom = fields.Char('Nom du taux')
    account  = fields.Many2one('account.account',string="Compte")

    value = fields.Float('Valeur')

    
