# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#
#
#----------------------------------------------------------------------------
 
from openerp.osv import fields, osv
from openerp.tools.translate import _

class wizard_ordre_virement(osv.osv_memory):
    _name = 'wizard.ordre.virement'
    _description = 'Wizard ordre de virement'

    def _get_default_company(self, cr, uid, context=None):
        company_id = self.pool.get('res.users')._get_company(cr, uid, context=context)
        if not company_id:
            raise osv.except_osv(_('Error!'), _('There is no default company for the current user!'))
        return company_id

    def _get_default_period(self, cr, uid, context=None):
        """
        Return  default account period value
        """
        context = context or {}
        if context.get('period_id', False):
            return context['period_id']
        account_period_obj = self.pool.get('account.period')
        ctx = dict(context, account_period_prefer_normal=True)
        ids = account_period_obj.find(cr, uid, context=ctx)
        period_id = False
        if ids:
            period_id = ids[0]
        return period_id


    _columns = {
         'period_id':fields.many2one('account.period', 'Periode', required=True),
         'company_id':fields.many2one('res.company', u'Société', required=True),
         'bank_id':fields.many2one('res.bank', 'Banque', required=True),
       }

    _defaults = {
        'company_id' : _get_default_company,
        'period_id' : _get_default_period,

    }


    def print_report(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard_ordre_virement'
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        return self.pool['report'].get_action(cr, uid, [], 'devplus_hr_payroll_tn.report_ordre_virement', data=datas, context=context)
 

wizard_ordre_virement()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

