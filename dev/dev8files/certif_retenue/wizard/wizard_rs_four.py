# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp import models, fields, api, _
from openerp.tools.translate import _
import datetime
#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------

class var(models.Model):
    _inherit="account.invoice"
    def openwiz(self,b,c,d,e):
        return{
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rs_four',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context':e
    
    }
class wizard_res_four(models.TransientModel):
    _name = 'rs_four'
    periode = fields.Many2one('account.period', string='Periode', required=True)
    four = fields.Many2one('res.partner', string='Fournisseur', required=True)
    libel = fields.Char('Libellé', required=True)
    journal = fields.Many2one('account.journal', string="Journal", required=True)
    taux = fields.Many2one('taux_rs', required=True,string="Taux")
    reference = fields.Char('Reference ',default="/")

    @api.one
    def print_report(self):
        # insertion du payement 
        move = {}
        
        print self.env.context.get('amount_total')

        datas = {'ids': self.id}
        datas['model'] = False
        datas['form'] = self.read()[0]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'certif_retenue.certif_retenue_four_report',
            'datas': datas,
            'name': u"Certificat de retenue d'impot sur le revenue/fournisseur",
            'context': self.env.context
        }
