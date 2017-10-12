# -*- coding: utf-8 -*-

import time

import openerp.addons.decimal_precision as dp
from openerp.osv import osv, fields
from openerp.tools.translate import _

class hr_employee_account(osv.osv):
    _inherit = 'hr.employee'
    
    _columns = {
                        # a la charge de  employee 
                    'account_banque_employeur_id': fields.many2one('account.account', u"Compte Bancaire de l'employeur",),
                    'cpt_cot_acc_tra': fields.many2one('account.account', string='Cotisation accident de travail'),
   					'cpt_cot_patr': fields.many2one('account.account', string='Cotisation patronale sécurité sociale'),
   					'cpt_cnss_acc_tra': fields.many2one('account.account', string='CNSS Accident de travail'),
   					'cpt_cnss_chg_pat': fields.many2one('account.account', string='CNSS Charge patronale'),
   					'categ_professionnelle': fields.char('Categ Professionnelle'),
                    'account_banque_id': fields.many2one('account.account', u"Compte Bancaire",),
                    'account_cotisation_id': fields.many2one('account.account', u'Declaration',),

                }
hr_employee_account()
