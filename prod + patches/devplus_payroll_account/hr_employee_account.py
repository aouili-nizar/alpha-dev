# -*- coding: utf-8 -*-

import time

import openerp.addons.decimal_precision as dp
from openerp.osv import osv, fields
from openerp.tools.translate import _

class hr_employee_account(osv.osv):
    _inherit = 'hr.employee'
    
    _columns = {
                        # a la charge de  employee 
                    'account_salaire_base_id': fields.many2one('account.account', 'Salaires et complément de salaire'),
                    'account_brut_id': fields.many2one('account.account', 'Brut'),
                    'account_net_paye_id': fields.many2one('account.account', u'Net à payer'),
                    'account_avantage_id': fields.many2one('account.account', u'Avantage en Nature'),
                    'account_deduction_id': fields.many2one('account.account', u'Déduction Avantage en Nature'),
                    'account_irpp_id': fields.many2one('account.account', u'IRPP'),
                    'account_cnss_id': fields.many2one('account.account', u'CNSS'),
                    'account_loan_id': fields.many2one('account.account', u'Loan'),
                    'account_prime_id': fields.many2one('account.account', u'Primes',),
                    'account_holiday_id': fields.many2one('account.account', u'Congés',),
                    'account_banque_employeur_id': fields.many2one('account.account', u"Compte Bancaire de l'employeur",),
    
                }
hr_employee_account()