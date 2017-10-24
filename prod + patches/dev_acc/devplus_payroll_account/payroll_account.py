# -*- coding: utf-8 -*-

from openerp.osv import osv, fields


class payroll_account(osv.osv):
    _inherit = 'hr.payroll.parametres'
    _columns = {
        'account_journal_id': fields.many2one('account.journal', 'Journal de Paie',),
        'account_journal_bank_id': fields.many2one('account.journal', 'Journal de banque',),
        # a la charge de  employee 
#         'account_salaire_base_id': fields.many2one('account.account', 'Salaires et complément de salaire'),
#         'account_brut_id': fields.many2one('account.account', 'Brut'),
#         'account_net_paye_id': fields.many2one('account.account', u'Net à payer'),
#         'account_avantage_id': fields.many2one('account.account', u'Avantage en Nature'),
#         'account_deduction_id': fields.many2one('account.account', u'Deduction Avantage en Nature'),
#         'account_irpp_id': fields.many2one('account.account', u'IRPP'),
#         'account_cnss_id': fields.many2one('account.account', u'CNSS'),
#         'account_loan_id': fields.many2one('account.account', u'Loan'),
#         'account_prime_id': fields.many2one('account.account', u'Primes',),
#         'account_banque_employeur_id': fields.many2one('account.account', u"Compte Bancaire de l'employeur",),
#         'account_foprolos_id': fields.many2one('account.account', u'foprolos'),
#         'account_cnrps_id': fields.many2one('account.account', u'cnrps'),
#         'account_juge_id': fields.many2one('account.account', u'Juge'),
       # 'taux_tfp': fields.float('Taux TFP'), 
       # 'taux_accident_travail': fields.float('Taux Accident de travail'), 
       # 'taux_foprolos': fields.float('Taux FoProLos'), 
                          
    }
payroll_account()