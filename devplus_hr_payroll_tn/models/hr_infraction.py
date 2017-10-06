# -*- coding: utf-8 -*-

import datetime
import math
import time
from openerp.osv import osv,fields
import openerp.addons.decimal_precision as dp


#===============================================================================
# hr_infraction
#===============================================================================
class hr_infraction(osv.osv):
    _name = 'hr.infraction'
    _order = 'id desc' 
    _rec_name = 'employer_id' 
    
    
    _columns = {
                    'employer_id':fields.many2one('hr.employee', u'Employé', required=True ,readonly=True, states={'new':[('readonly', False)]}),
                    'date': fields.date('Date',required=True ,readonly=True, states={'new':[('readonly', False)]}),
                    'warning':fields.text('Description' ,readonly=True, states={'new':[('readonly', False)]}  ),
                    'type_id':fields.many2one('hr.infraction.type', 'Type',required=True ,readonly=True, states={'new':[('readonly', False)]}),
                    'number_of_days_temp':fields.float('Nombre de jours' ,readonly=True),
                    'date_from': fields.datetime('Start Date' ,readonly=True, states={'new':[('readonly', False)]}),
                    'date_to': fields.datetime('End Date',readonly=True, states={'new':[('readonly', False)]}),
                    'code':fields.char('Code'), 
                    'state':fields.selection([('new','Brouillon'), ('done','Confirmé'),], 'Etat'),
                }
    
    _defaults = {
                 'code':'0',
                 'date': fields.date.context_today,
                 'state':  'new',
                 }
    
    def action_terminer(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids[0],{'state': 'done'},context)
        return True
    
    
    def _get_number_of_days(self, date_from, date_to):
        """Returns a float equals to the timedelta between two dates given as string."""

        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        from_dt = datetime.datetime.strptime(date_from, DATETIME_FORMAT)
        to_dt = datetime.datetime.strptime(date_to, DATETIME_FORMAT)
        timedelta = to_dt - from_dt
        diff_day = timedelta.days + float(timedelta.seconds) / 86400
        return diff_day
    
    
    def on_change_date(self, cr, uid, ids, date_from,date_to):
        if (date_from and date_to) and (date_from > date_to):
            raise osv.except_osv(_('Warning!'),_('The start date must be anterior to the end date.'))

        result = {'value': {}}

        if (date_to and date_from) and (date_from <= date_to):
            diff_day = self._get_number_of_days(date_from, date_to)
            result['value']['number_of_days_temp'] = round(math.floor(diff_day))+1
        else:
            result['value']['number_of_days_temp'] = 0

        return result
    
    def on_change_type_id(self, cr, uid,ids,type_id, context=None):
        res ={}
        if type_id :
            record = self.pool.get('hr.infraction.type').browse(cr,uid,type_id)
            if record.type == 'nb_days':
                res = {'code':'1'}
            else :
                res = {'code':'0'}
        return {'value': res}
   
    
    
    def onchange_period_id(self, cr, uid,ids,period_id, context=None):
        res ={}
        if period_id :
            account_obj = self.pool.get('account.period')
            period=account_obj.browse(cr,uid,period_id)
            val = {'date_start':period.date_start,'date_stop': period.date_stop }
            res = {'value': val}
        return  res
            
   
hr_infraction()

#===============================================================================
# hr_infraction_type
#===============================================================================
class hr_infraction_type(osv.Model):
    _name = 'hr.infraction.type'
    _columns = {
               'name':fields.char('Nom',required=True),
               
               
               'type':fields.selection([
                    ('no_deduction',u'Sans déduction'),
                    ('nb_days','Nombre de jours'),
                     ],    'Type', select=True, required=True),
                
                'amount':fields.float('Montant', digits_compute=dp.get_precision('Account')),
                'percentage':fields.float('Pourcentage'),
               
               }
    _defaults = {  
        'type': 'no_deduction',  
        }
    
    
    
   
hr_infraction_type()
