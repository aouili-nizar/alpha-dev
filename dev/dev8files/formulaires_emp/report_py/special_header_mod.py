from openerp import api, models  , fields


class attestation_salaire_report(models.Model):
    _inherit="res.company"

    capital = fields.Char('S.A.R.L au capital de ')
    adr_cor = fields.Char('Adresse de Correspondance ')
