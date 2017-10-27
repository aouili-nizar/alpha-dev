from openerp import fields, models , api

class attach(models.Model):
    _inherit="sale.order"



    attach = fields.Binary(string='Fichier de justification',required="true")