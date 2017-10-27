from openerp import fields, models, api


class attach(models.Model):
    _inherit = "account.invoice"

    attach = fields.Binary(string='Fichier de justification', required="true")
