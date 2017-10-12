# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#
#
#-------------------------------------------------------------------------------

from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp


#===============================================================================
# hr_avance
#===============================================================================
class hr_avance(osv.Model):
    _name = "hr.avance"

    def _get_month_id(self, cr, uid, context=None):
        """
        Return  default account period value
        """
        context = context or {}
        months_ids = self.pool.get('hr.month').find(cr, uid, context=context)
        return months_ids and months_ids[0] or False
    
    _columns = {
                'date':fields.date('Date'),
                'name': fields.char(u'Numéro'),
                'month_id': fields.many2one('hr.month', u'Mois', required=True ,readonly=True, states={'new':[('readonly', False)]}),
                'avance_ids': fields.one2many('hr.avance.line', 'avance_id',readonly=True, states={'new':[('readonly', False)]}),
                'state':fields.selection([('new','Brouillon'), ('done','Confirmé'),], 'Etat'),


                }
    
    _defaults = {
                 'date': fields.date.context_today,
                  'month_id': _get_month_id,
                  'state':  'new',
                 }
    
    
    def create(self, cr, uid, vals, context=None):
        if not vals.get('name', False):
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'hr.avance', context=context) or '/'
        return super(hr_avance, self).create(cr, uid, vals, context=context)
    
#     def action_draft(self, cr, uid, ids, context=None):
#         self.write(cr,uid,ids[0],{'state': 'new'},context)
#         return True
    

    def action_terminer(self, cr, uid, ids, context=None):
        self.write(cr,uid,ids[0],{'state': 'done'},context)
        return True

hr_avance()    


#===============================================================================
# hr_avance_line
#===============================================================================
class hr_avance_line(osv.Model):
    _name = "hr.avance.line"
    
    _columns = {
                
                'avance_id': fields.many2one('hr.avance',required=True),
                'amount': fields.float('Montant Souhaité',digits_compute=dp.get_precision('Montant Paie'),required=True),
                'amount_confirm': fields.float(u'Montant Confirmé',digits_compute=dp.get_precision('Montant Paie'),required=True),
                'employee_id': fields.many2one('hr.employee',u'Employé',required=True, domain="[('avance','=',True)]"),


                }
    
hr_avance_line() 