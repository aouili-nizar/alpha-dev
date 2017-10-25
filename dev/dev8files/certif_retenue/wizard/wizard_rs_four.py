# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp import models, fields, api, _
from openerp.tools.translate import _
#-------------------------------------------------------------------------------
# wizard_resume_paie
#-------------------------------------------------------------------------------


class wizard_res_four(models.TransientModel):
    _name = 'rs_four'
    fiscalyear_id = fields.Many2one('account.fiscalyear', string='Exercice fiscal', required=True)
    four = fields.Many2one('res.partner', string='Fournisseur', required=True)
    libel = fields.Char('Libellé')
    journal = fields.Many2one('account.journal',string="Journale")
    taux = fields.Float('Taux')
    move_line = fields.Many2one('account.move',string="Piéce comptable")


    @api.v7
    def print_report(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = False
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'certif_retenue.certif_retenue_four_report',
            'datas': datas,
            'name': u"Certificat de retenue d'impot sur le revenue/fournisseur",
            'context': context
        }
