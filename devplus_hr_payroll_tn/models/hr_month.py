# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
class hr_month(osv.osv):
    _name = 'hr.month'
    
    _columns = {
                'name': fields.char('Mois',required=True),
                'period_id': fields.many2one('account.period', u'Période Comptable',required=True),
                'date_start': fields.date('Date Début',required=True),
                'date_stop': fields.date('Date Fin',required=True),
                'nb_jour_5j' : fields.float(u' Nb/mois/(regime 5 jours )  '),
                'nb_jour_6j' : fields.float(u' Nb/mois/(regime 6 jours )  '),
                'parametre_id': fields.many2one('hr.payroll.parametres', u'Période'),
                }
    
    def find(self, cr, uid, dt=None, context=None):
        if context is None: context = {}
        if not dt:
            dt = fields.date.context_today(self, cr, uid, context=context)
        domain = [('date_start', '<=' ,dt), ('date_stop', '>=', dt)]
        result = self.search(cr, uid, domain, context=context)
        return result
    
    
    
    def onchange_period_id(self, cr, uid, ids, period_id, context=None):
        res={}
        if period_id:
            period_obj=self.pool.get('account.period')
            period=period_obj.browse(cr,uid,period_id)
            val={'date_start':period.date_start,
                'date_stop':period.date_stop
                    }
            res={'value':val }
        return res
    
#     def onchange_period_id(self, cr, uid,ids,period_id, context=None):
#         res ={}
#         if period_id :
#             account_obj = self.pool.get('account.period')
#             period=account_obj.browse(cr,uid,period_id)
#             val = {'date_start':period.date_start,'date_stop': period.date_stop }
#             res = {'value': val}
#         return  res
hr_month()