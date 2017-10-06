# -*- coding: utf-8 -*-


from openerp.osv import fields, osv
from openerp.tools.translate import _

class wizard_journal_paie(osv.osv_memory):
    _name = 'wizard.journal.paie'
    _description = 'Wizard journal de paie'
    
    def _get_defaults_fiscal_year(self, cr, uid, data, context={}):
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        fisc = fiscalyear_obj.find(cr, uid)
        data['form'] = fisc
        return data['form']
    
    def _get_default_company(self, cr, uid, context=None):
        company_id = self.pool.get('res.users')._get_company(cr, uid, context=context)
        if not company_id:
            raise osv.except_osv(_('Error!'), _('There is no default company for the current user!'))
        return company_id
    
    
    def _get_month_id(self, cr, uid, context=None):
        """
        Return  default account period value
        """
        context = context or {}
        if context.get('period_id', False):
            return context['period_id']
        account_period_obj = self.pool.get('hr.month')
        ctx = dict(context, hr_month_prefer_normal=True)
        ids = account_period_obj.find(cr, uid, context=ctx)
        period_id = False
        if ids:
            period_id = ids[0]
        return period_id
    
    
    _columns ={
               'month_id':fields.many2one('hr.month','Periode',required=True),
               'company_id':fields.many2one('res.company',u'Société',required=True),

               }
    _defaults = {
            'company_id' : _get_default_company,
            'month_id' : _get_month_id,
        }
    
    
    def print_report(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard_journal_paie'
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        context['landscape']=True
        return self.pool['report'].get_action(cr, uid, [], 'devplus_hr_payroll_tn.report_journal_paie', data=datas, context=context)
    
    def print_report_excel(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard_journal_paie'
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        context['landscape']=True
        return self.pool['report'].get_action(cr, uid, [], 'devplus_hr_payroll_tn.report_journal_paie', data=datas, context=context)    
    
wizard_journal_paie()