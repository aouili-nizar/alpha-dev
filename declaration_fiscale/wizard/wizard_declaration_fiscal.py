# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp import models, fields, api, _
from openerp.tools.translate import _
#-------------------------------------------------------------------------------
# wizard_resume_paie
#-------------------------------------------------------------------------------
class wizard_declaration_fiscal(models.TransientModel):
    _name = 'devplus_hr_payroll_tn.declaration_fiscal'
    fiscalyear_id = fields.Many2one('account.fiscalyear', string='Exercice fiscal', required=True)
    periode = fields.Many2one('account.period',string='Période',required=True)
    sum_vnt_loc = fields.Integer(required=True,string='Somme des ventes locale')
    sum_vnt_ext = fields.Integer(required=True,string='Somme des ventes export')
    @api.v7
    def print_report(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = False
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'devplus_hr_payroll_tn.declaration_fiscal_report',
            'datas': datas,
            'name': u'Rapport de declaration Fiscal',
            'context':context
            }
