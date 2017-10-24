# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp import models, fields, api, _
from openerp.tools.translate import _
#-------------------------------------------------------------------------------
# wizard_resume_paie
#-------------------------------------------------------------------------------
class wizard_res_emp(models.TransientModel):
    _name = 'rs_emp'
    fiscalyear_id = fields.Many2one('account.fiscalyear', string='Exercice fiscal', required=True)
    emp = fields.Many2one('hr.employee',string='Employé',required=True)
    @api.v7
    def print_report(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = False
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'certif_retenue.certif_retenue_report',
            'datas': datas,
            'name': u"Certificat de retenue d'impot sur le revenue/employe",
            'context':context
            }
