# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class hr_rubrique(osv.osv):
    _name='hr.payroll.rubrique'
    _description='hr.payroll.rubriques'
    
    
    _columns={
              'name' : fields.char('Nom de la rubrique', size=64, required=True),
              'code':fields.char('Code', size=64),
              'regime' : fields.selection([('horaire', 'Horaire'),
                                     ('journalier', u'Journalier'),
                                      ('mensuel', u'Mensuel') ], 'Regime', required=True),
#               'categorie' : fields.selection([('majoration', 'Majoration'),
#                                         ('deduction', 'Deduction'),
#                                         ], u'Catégorie'),
              
              'categorie' : fields.selection([('majoration', 'Allocation'),
                                        ('deduction', 'Deduction'),
                                        ], u'Catégorie'),
              'sequence': fields.integer(u'Séquence', help='Ordre d\'affichage dans le bulletin de paie'),
              'type':fields.selection([ ('prime', 'Prime'),
                                 ('indemnite', 'Indemnite'),
                                 ('avantage', 'Avantage'), ], 'Type'),
              'imposable':fields.boolean('Imposable',),
              'cotisable':fields.boolean('Cotisable',),
              'afficher':fields.boolean('Afficher', help='Afficher cette rubrique sur le bulletin de paie'),
              'absence' :fields.boolean('Absence',),
              'note' : fields.text('Commentaire'),
              
              
              }
    
    _defaults = {
                 'sequence': lambda * a: 1,
                 'absence': lambda * a: True,
             #    'imposable': lambda * a: True,
            #     'cotisable': lambda * a: True,
                 'afficher': lambda * a: True,
                 'type': lambda * a: 'prime',
                 'categorie': lambda * a: 'majoration',
                 }

    
hr_rubrique()


class hr_ligne_rubrique(osv.osv):
    
    def _sel_rubrique(self, cr, uid, context=None):
        obj = self.pool.get('hr.payroll.rubrique')
        ids = obj.search(cr, uid, [])
        res = obj.read(cr, uid, ids, ['name', 'id'], context)
        res = [(r['id'], r['name']) for r in res]
        return res
    
    
    _name = 'hr.payroll.ligne_rubrique'
    _description = 'Ligne rubrique'
    
    _columns ={
               'rubrique_id' : fields.many2one('hr.payroll.rubrique', 'Rubrique', selection=_sel_rubrique, required=True),
               'id_contract': fields.many2one('hr.contract', 'Contrat', ondelete='cascade', select=True),
               'montant' : fields.float('Montant', digits_compute=dp.get_precision('Montant Paie'), required=True),
               'period_id': fields.many2one('account.period', u'Période', domain=[('state', '<>', 'done')]),
               'permanent' : fields.boolean('Rubrique Permanante'),
               'date_start': fields.date(u'Date début'),
               'date_stop': fields.date('Date fin'),
               'note' : fields.text('Commentaire'),
               
               
               }
    
    def _check_date(self, cr, uid, ids):
        for obj in self.browse(cr, uid, ids):
            if obj.date_start > obj.date_stop :
                return False
        return True
    
        _order = 'date_start' 
    _constraints = [
        (_check_date, 'Date début doit etre inferieur a date fin', ['date_stop'])
        ]
    
    def onchange_rubrique_id(self, cr, uid, ids, rubrique_id):
        rubrique = self.pool.get('hr.payroll.rubrique').browse(cr, uid, rubrique_id)
        result = {'value': {
                            'montant' : rubrique.plafond,
                        }
                    }
        return result

    def onchange_period_id(self, cr, uid, ids, period_id=False):
        result = {}
        if period_id :
            period = self.pool.get('account.period').browse(cr, uid, period_id)
            result = {'value': {
                            'date_start' :   period.date_start,
                            'date_stop' : period.date_stop
                            }
                    }

        return result
  
hr_ligne_rubrique()
    
    