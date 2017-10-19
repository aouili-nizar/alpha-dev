# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp.tools.translate import _
import time
import openerp.addons.decimal_precision as dp

#===============================================================================
# hr_pointage
#===============================================================================
class hr_pointage(osv.osv):
    
    STATES = [
              ('draft', 'Brouillon'),
              ('confirmed', u'Validé'),
            ]
    _name = 'hr.pointage'
    _inherit = ['mail.thread']
    _description = 'Saisie du pointage' 
    
    
    def _get_company_id(self, cr, uid, data, context={}):
        if context is None:
            context = {}
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        company_id = context.get('company_id', user.company_id.id)
        return  company_id 
    
    
    def _get_month_id(self, cr, uid, context=None):
        """
        Return  default account period value
        """
        context = context or {}
        period_ids = self.pool.get('hr.month').find(cr, uid, context=context)
        return period_ids and period_ids[0] or False
    
    _columns = {
               'name':fields.char('Description', size=64, readonly=True, states={'draft':[('readonly', False)]},),
               'date':fields.date('Date pointage', readonly=True, states={'draft':[('readonly', False)]}, select=1),
               'month_id': fields.many2one('hr.month', u'Mois',readonly=True, required=True, states={'draft':[('readonly', False)]}, select=1),
               'period_id': fields.many2one('account.period', u'Période Comptable', readonly=True, required=True, states={'draft':[('readonly', False)]}, select=1),
               'company_id': fields.many2one('res.company', u'Société',change_default=True, readonly=True, required=True, states={'draft':[('readonly', False)]}),
               'pointage_line_ids': fields.one2many('hr.pointage.line', 'pointage_id', 'Lignes Pointages',readonly=True, states={'draft':[('readonly', False)]}),
               'note': fields.text('Notes'),
               'state': fields.selection(STATES, 'Etat', select=True, readonly=True, track_visibility='onchange',),
               
              
              }

    
    def onchange_month_id(self, cr, uid, ids, month_id, company_id):
        result={}
        if  month_id and  company_id:
            #TODO: you cannot test by month_id because user can put the month in two year 
            #must use month_id and period_id
            count=self.search_count(cr,uid,[('month_id','=',month_id),('company_id','=',company_id)] )
            if count > 0 :
                warning = {'title':'Attention', 'message':_(u'Le pointage d\'une période doit être unique par société!')}
                value = {'period_id': False,'month_id':False}
                return {'warning': warning, 'value': value}
            company = self.pool.get('res.company').browse(cr, uid, company_id)
            month = self.pool.get('hr.month').browse(cr, uid, month_id)
            result = {'value':{ 'name' :   _(u'Pointage %s du mois %s') % (company.name, month.name), 'period_id' : month.period_id.id }}
        return result
    
    def action_confirm(self, cr, uid, ids, *args):
        '''
        validate pointage
        @return: True
        '''
        self.write(cr, uid, ids, {'state': 'confirmed'})
        return True
    
    def action_draft(self, cr, uid, ids, *args):
        '''
        cancelled to draft
        @return: True
        '''
        self.write(cr, uid, ids, {'state': 'draft'})
        return True
    
    
    def add_all_employees(self, cr, uid, ids, context={}):
        employee_obj = self.pool.get('hr.employee')
        pointage = self.browse(cr,uid,ids[0],context=context)
        
        #month_id=self.pool.get('hr.month')
        # tous les  employee ont des contract contract 
        ids_employees = employee_obj.search(cr, uid, [('active', '=', True), ('contract_ids', '!=', False)])

        sql = '''   DELETE from hr_pointage_line where pointage_id = %s '''
        cr.execute(sql, (pointage.id,))
        # creation d'un nouveau pointage
        all_pointage = []
        
        parms = self.pool.get('hr.payroll.parametres')
        fiscalyear_id = self.pool.get('account.fiscalyear').find(cr, uid)
        ids_parms = parms.search(cr, uid, [('fiscalyear_id', '=', fiscalyear_id)])
        dictionnaire = parms.read(cr, uid, ids_parms[0]) 
               
        for emp in employee_obj.browse(cr ,uid,ids_employees):
          
            #nb_pointage=22
            nb_pointage=dictionnaire['nb_jour_5j']
            print '****nb_pointage****',nb_pointage
            regime=emp.contract_id.regime_id
            if regime.type_regime =='horaire': 
                nb_pointage = regime.hours_horaire
            if regime.type_regime =='mensuel':
                if regime.hours_mensuel == '48' :
                    nb_pointage=dictionnaire['nb_jour_6j']
                    print '****nb_pointage****',nb_pointage
                    #nb_pointage = 26
                # calcul le nombre de congé payé 
            nb_days_holiday = employee_obj._get_nb_days_cp_by_period(cr, uid, emp.id, pointage.period_id.id, context=context)    
                # calcul le nombre de congé impayé   
            nb_days_holiday_impaye = employee_obj._get_nb_days_c_impaye_by_period(cr, uid, emp.id, pointage.period_id.id, context=context)    
                # calcul solde congé   
            total_days_restante = employee_obj._get_total_days_restante(cr, uid, emp.id, pointage.period_id.id)             
            val = (0, 0, {#'nb_pointage':nb_pointage ,
                          'nb_days_masse' : 20,
                          'nb_pointage':nb_pointage - nb_days_holiday-nb_days_holiday_impaye,
                          'employee_id': emp.id,
                          #'nb_days_holiday' : 0,
                          'total_days_restante':total_days_restante,
                          'nb_days_holiday' : nb_days_holiday,
                          'nb_imp_days_holiday' : nb_days_holiday_impaye ,
                          }
                    )
            all_pointage.append(val)
            
        value = {  'pointage_line_ids': all_pointage }   
        self.write(cr, uid, pointage.id, value, context=context)
        return True        
                
        

    
    _defaults = {  
                 'date': lambda *a: time.strftime('%Y-%m-%d'),
                 'state':'draft',
                 'company_id': _get_company_id,
                 'month_id':_get_month_id
                }
    
    
hr_pointage()


#===============================================================================
# hr_pointage_line
#===============================================================================
class hr_pointage_line(osv.osv):
    _name = 'hr.pointage.line'
    
    _columns = {
              'name':fields.char('Description'),
              'pointage_id': fields.many2one('hr.pointage', 'Pointage', ondelete='cascade', select=True),
              'nb_pointage': fields.float('Jours travaillés',),
              'nb_days_holiday': fields.float('Jours C.P',),
              'nb_imp_days_holiday': fields.float('Jours C.N.P',),
              'total_days_restante': fields.float('Solde congé',),
              'nb_days_right_leaves': fields.float('Droit de congé',),
              'nb_days_masse': fields.float('Jours masse',),
              'hs100': fields.float('HS100',),
              'hs125': fields.float('HS125',),
              'hs150': fields.float('HS150',),
              'hs175': fields.float('HS175',),
              'hs200': fields.float('HS200',),
              'employee_id': fields.many2one('hr.employee', u'Employé', required=True),
              'regime_id': fields.related('employee_id', 'contract_id' , 'regime_id', type='many2one', relation='hr.contract.regime', string=u'Régime', readonly=True),
              }
    
    def onchange_employee_id(self, cr, uid, ids, employee_id):
        res={}
        if employee_id :
            employee = self.pool.get('hr.employee').browse(cr, uid, employee_id)
            if not employee.contract_id :
                warning = {'title':'Attention', 'message':_(u"Veuillez d\'abord ajoutre un contract pour l'employée %s" % employee.name)}
                value = {'employee_id': False}
                res= {'warning': warning,
                        'value': value}
        return res
    
hr_pointage_line()