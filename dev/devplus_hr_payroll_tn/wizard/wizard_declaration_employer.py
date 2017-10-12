# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp.tools.translate import _
#-------------------------------------------------------------------------------
# wizard_resume_paie
#-------------------------------------------------------------------------------
class wizard_declaration_employer(osv.osv_memory):
    _name = 'devplus_hr_payroll_tn.declaration_employer'


    _columns = {
              
               'fiscalyear_id':fields.many2one('account.fiscalyear', u'Exercice fiscal', required=True),
               'comptable_id': fields.many2one('res.partner','Comptable',required=True),
             
                }
 
#     def print_report(self, cr, uid, ids, context=None):
#         datas = {'ids': context.get('active_ids', [])}
#         datas['model'] = False
#         datas['form'] = self.read(cr, uid, ids, context=context)[0]
#         return {
#             'type': 'ir.actions.report.xml',
#             'report_name': 'devplus_hr_payroll_tn.declaration_employer_report',
#             'datas': datas,
#             'name': u'Rapport de declaration employer',
#             'context':context
#             }   
        
    def print_report(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'devplus_hr_payroll_tn_declaration_employer'
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        return self.pool['report'].get_action(cr, uid, [], 'devplus_hr_payroll_tn.declaration_employer_report', data=datas, context=context)        
          
wizard_declaration_employer()  