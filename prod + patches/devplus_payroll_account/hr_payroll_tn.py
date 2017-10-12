# -*- coding: utf-8 -*-

import time

import openerp.addons.decimal_precision as dp
from openerp.osv import osv, fields
from openerp.tools.translate import _




class hr_payroll_tn(osv.osv):
    _inherit = "hr.payroll"
    _columns = {
        'move_id': fields.many2one('account.move', u'Pièce comptable', readonly=True),
    }
    
    def draft_cb(self, cr, uid, ids, context=None):
        for sal in self.browse(cr, uid, ids):
            if sal.move_id:
                raise osv.except_osv(_('Error !'), _(
                    u'Veuillez d\'abord supprimer les écritures comptables associés'))
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
    
    def confirm_cb(self, cr, uid, ids, context=None):
        super(hr_payroll_tn, self).confirm_cb(cr, uid, ids, context=context)
        # pour generer les ecritures
        self.action_move_create(cr, uid, ids)
        return self.write(cr, uid, ids, {'state': 'confirmed'}, context=context)
    
    def cancel_cb(self, cr, uid, ids, context=None):
        super(hr_payroll_tn, self).cancel_cb(cr, uid, ids, context=context)
        self.action_move_create_net_paye(cr, uid, ids)
        return self.write(cr, uid, ids, {'state': 'paid'}, context=context)
    
    def _convert_amount(self, cr, uid, amount, currency_id,currency_company_id, context=None):
        '''
        This function convert the amount given in company currency. It takes   the rate encoded in the system.

        :param amount: float. The amount to convert
        :param currency_id: the currency of salary
        :param currency_company_id: the currency of company
        :param context: to context to use for the conversion. It may contain the key 'date' set to the salary date
            field in order to select the good rate to use.
        :return: the amount in the currency of the salary company
        :rtype: float
        '''
        if context is None:
            context = {}
        currency_obj = self.pool.get('res.currency')
        
        return currency_obj.compute(cr, uid, currency_id,currency_company_id, amount, context=context)
    
    
        
    
    # generation des ecriture comptable
    def action_move_create(self, cr, uid, ids):
        #for not employee_id.create_move create one move
        bulletin_lines=[]
        for sal in self.browse(cr, uid, ids):
            for bulletin in sal.bulletin_line_ids:
                if not bulletin.employee_id.create_move:
                    bulletin_lines.append(bulletin)
        if bulletin_lines:
            self._move_create(cr, uid, ids, bulletin_lines,True)

        # create   move for each employee have option  create_move
        for sal in self.browse(cr, uid, ids):
            for bulletin in sal.bulletin_line_ids:
                if bulletin.employee_id.create_move:
                    self._move_create(cr, uid, ids, [bulletin],False)   
                            
    # generation des ecriture comptable pour le salaire payé ( net à payer)
    def action_move_create_net_paye(self, cr, uid, ids):
        #for not employee_id.create_move create one move
        bulletin_lines=[]
        for sal in self.browse(cr, uid, ids):
            for bulletin in sal.bulletin_line_ids:
                if not bulletin.employee_id.create_move:
                    bulletin_lines.append(bulletin)
        if bulletin_lines:
            self._move_create_net_paye(cr, uid, ids, bulletin_lines,True)
        # create   move for each employee have option  create_move
        for sal in self.browse(cr, uid, ids):
            for bulletin in sal.bulletin_line_ids:
                if bulletin.employee_id.create_move:
                    self._move_create_net_paye(cr, uid, ids, [bulletin],False)                            
        
        
        
            
            
        
        
    # generation des ecriture comptable
    def _move_create(self, cr, uid, ids,bulletin_lines,update):
        
        context = {}
        for sal in self.browse(cr, uid, ids):
            # parametres account
            params = self.pool.get('hr.payroll.parametres')
            ids_params = params.search(cr, uid, [('fiscalyear_id', '=', sal.period_id.fiscalyear_id.id)])
            if not ids_params:
                raise osv.except_osv(_('Erreur !'), _(u"Veuillez vérifier les paramétres de paie pour l'année Fiscal courante"))
            dict_param = params.read(cr, uid, ids_params[0])
            # Journal  and currency
            journal_id = dict_param['account_journal_id'][0]
            if not journal_id:
                raise osv.except_osv(_('UserError'), _('Veuillez indiquer un journal des salaires dans le paramétrage de la comptabilité de la paie. '))
            journal = self.pool.get('account.journal').browse(cr, uid, journal_id, context=context)
            if journal.centralisation:
                raise osv.except_osv(
                    _('UserError'), _('Cannot create salary move on centralised journal'))

            
            # currency_id = journal.currency and journal.currency.id or journal.company_id.currency_id.id
            currency_id = journal.currency and journal.currency.id or journal.company_id.currency_id.id
            currency_company_id= sal.company_id.currency_id.id
            ctx = context.copy()
            ctx.update({'date': sal.date_salary})
            
            # date and period
            date_move = sal.date_salary or time.strftime('%Y-%m-%d')
            period_id = sal.period_id and sal.period_id.id or False

            if not period_id:
                raise osv.except_osv(_('UserError'), _(u'Période obligatoire'))
            
            period = self.pool.get('account.period').browse(cr, uid, period_id, context=context)
            # name
            name_move = "Salaire " + period.name
                        
            #--------------cotisations TODO not get[0]-------------------------
#             taux_tfp = dict_param['taux_tfp']/100.0
#             taux_accident_travail = dict_param['taux_accident_travail']/100.0
#             taux_foprolos = dict_param['taux_foprolos']/100.0
            
            salaire_net_a_payer = 0.0
            irpp = 0.0
            avantage =0.0
            deduction = 0.0
            salaire_base = 0.0
            salaire_base_brut =0.0
            mnt_conge_paye =0.0
            mnt_conge_rubriques_paye =0.0
            prime = 0.0
           # foprolos =0.0
            cotisations_employer =0.0
           # accident_travail = 0.0
            cotisations_employee =0.0
            loan_amount =0.0
#             cotisations_employee_cnrps=0.0
#             cotisations_employer_cnrps =0.0
#             amount_juge=0.0
#             if juge_ok :  amount_juge = 121.541 #TODO:
            
            for bulletin in bulletin_lines:
                salaire_net_a_payer += bulletin.salaire_net_a_payer
                irpp += bulletin.igr
                avantage +=bulletin.avantage
                deduction += bulletin.deduction
                salaire_base += bulletin.salaire_base
                salaire_base_brut +=bulletin.salaire_base_brut
                
                prime += bulletin.prime
                mnt_conge_paye +=bulletin.mnt_conge_paye
                mnt_conge_rubriques_paye +=bulletin.mnt_conge_rubriques_paye
                
               # print '**prime**',prime
                #foprolos
#                 if bulletin.employee_id.cnss5 or bulletin.employee_id.cnrps6:
#                     foprolos += bulletin.salaire_brute * taux_foprolos
                #add specific to foprolos
#                 if bulletin.employee_id.specific : 
#                     foprolos += bulletin.employee_id.amount_logement
                
                salaire_base = salaire_base+mnt_conge_rubriques_paye -mnt_conge_paye -salaire_base_brut
                
                if bulletin.employee_id.cnss5:
                    cotisations_employer += bulletin.cotisations_employer*0.1657/0.1697
#                     accident_travail += bulletin.cotisations_employer*taux_accident_travail/0.1697
                    cotisations_employee += bulletin.cotisations_employee
                loan_amount += bulletin.loan_amount
#                 if bulletin.employee_id.cnrps6:
#                     cotisations_employee_cnrps += bulletin.cotisations_employer
#                     cotisations_employer_cnrps += bulletin.cotisations_employee
                 
            amount_debit=salaire_net_a_payer+irpp+cotisations_employer+cotisations_employee+ \
                        loan_amount
            # move_lines
            move = {}
            move_lines = []
#             if not dict_param['account_net_paye_id']  or not dict_param['account_irpp_id'] \
#                 or not dict_param['account_cnss_id'] or not dict_param['account_loan_id']   \
#                  or not dict_param['account_brut_id']:
#                 raise osv.except_osv(_('Erreur'), _('Veuillez vérifier les comptes comptable dans le paramétrage de la comptabilité de la paie'))

            # 12 Salaire de base
            
            name_move = u'Bruts Salaire de Base'
            val = {
                #'account_id': dict_param['account_salaire_base_id'][0],
                'account_id': bulletin.employee_id.account_salaire_base_id.id,
                'period_id': period_id,
                'journal_id': journal_id,
                'date': date_move,
                'name': name_move,
                'amount_currency':self._convert_amount(cr, uid,salaire_base,currency_id, currency_company_id, context=ctx),
                'debit': salaire_base,
                'credit': 0.0 ,
                'currency_id': currency_id,
                'state': 'valid'
            }
            move_lines.append((0, 0, val)) 
            #11 
####################################################################################################################             
#             name_move = u'Bruts'
#             val = {
#                 'account_id': dict_param['account_brut_id'][0],
#                 'period_id': period_id,
#                 'journal_id': journal_id,
#                 'date': date_move,
#                 'name': name_move,
#                 'amount_currency':amount_debit,
#                 'debit': self._convert_amount(cr, uid,amount_debit,currency_id, currency_company_id, context=ctx),
#                 'credit': 0.0 ,
#                 'currency_id': currency_id,
#                 'state': 'valid'
#             }
#             move_lines.append((0, 0, val)) 
####################################################################################################################
            #10
         
            # 9
        
            # 8

  
            #7
            if loan_amount :
                name_move = u'Pret'
                val = {
                    #'account_id': dict_param['account_loan_id'][0],
                    'account_id': bulletin.employee_id.account_loan_id.id,
                    'period_id': period_id,
                    'journal_id': journal_id,
                    'date': date_move,
                    'name': name_move,
                    'amount_currency':-1*loan_amount,
                    'debit':0.0,
                    'credit':  self._convert_amount(cr, uid,loan_amount,currency_id, currency_company_id, context=ctx),
                    'currency_id': currency_id,
                    'state': 'valid'
                }
                move_lines.append((0, 0, val))             
            #  6
            if cotisations_employee:
                name_move = u'CNSS'
                val = {
                    #'account_id': dict_param['account_cnss_id'][0],
                    'account_id': bulletin.employee_id.account_cnss_id.id,
                    'period_id': period_id,
                    'journal_id': journal_id,
                    'date': date_move,
                    'name': name_move,
                    'amount_currency':-1*cotisations_employee,
                    'debit':0.0,
                    #'credit':  self._convert_amount(cr, uid,cotisations_employee,currency_id, currency_company_id, context=ctx),
                    'credit':cotisations_employee,
                    'currency_id': currency_id,
                    'state': 'valid'
                }
                move_lines.append((0, 0, val))
            # 5
            if prime:
                name_move = u'Prime'
                val = {
                    #'account_id': dict_param['account_prime_id'][0],
                    'account_id': bulletin.employee_id.account_prime_id.id,
                    'period_id': period_id,
                    'journal_id': journal_id,
                    'date': date_move,
                    'name': name_move,
                    'amount_currency':self._convert_amount(cr, uid,prime,currency_id, currency_company_id, context=ctx),
                    'debit':prime,
                    'credit':0.0,
                    'currency_id': currency_id,
                    'state': 'valid'
                }
                move_lines.append((0, 0, val))
                
####################################################################
            #51
            if mnt_conge_paye:
                name_move = u'Congés payés'
                val = {
                    #'account_id': dict_param['account_prime_id'][0],
                    'account_id': bulletin.employee_id.account_holiday_id.id,
                    'period_id': period_id,
                    'journal_id': journal_id,
                    'date': date_move,
                    'name': name_move,
                    'amount_currency':self._convert_amount(cr, uid,mnt_conge_paye,currency_id, currency_company_id, context=ctx),
                    'debit':mnt_conge_paye,
                    'credit':0.0,
                    'currency_id': currency_id,
                    'state': 'valid'
                }
                move_lines.append((0, 0, val))


###################################################################
         
            # 4
#########################################################################################################
#             if cotisations_employer :
#                 name_move = u'Prise ch.employer'
#                 val = {
#                     'account_id': dict_param['account_cnss_id'][0],
#                     'period_id': period_id,
#                     'journal_id': journal_id,
#                     'date': date_move,
#                     'name': name_move,
#                     'amount_currency':-1*cotisations_employer,
#                     'debit': 0.0,
#                     'credit':  self._convert_amount(cr, uid,cotisations_employer,currency_id, currency_company_id, context=ctx),
#                     'currency_id': currency_id,
#                     'state': 'valid'
#                 }
#                 move_lines.append((0, 0, val))    
###########################################################################################################
            # 3
            if deduction :
                name_move = u'Déduction Carnet repas'
                val = {
                    #'account_id': dict_param['account_deduction_id'][0],
                    'account_id': bulletin.employee_id.account_deduction_id.id,
                    'period_id': period_id,
                    'journal_id': journal_id,
                    'date': date_move,
                    'name': name_move,
                    'amount_currency':-1*deduction,
                    'debit': 0.0,
                    #'credit':  self._convert_amount(cr, uid,deduction,currency_id, currency_company_id, context=ctx),
                    'credit':deduction,
                    'currency_id': currency_id,
                    'state': 'valid'
                }
                move_lines.append((0, 0, val))            
            # 3
            if avantage :
                name_move = u'Carnet repas'
                val = {
                    #'account_id': dict_param['account_avantage_id'][0],
                    'account_id': bulletin.employee_id.account_avantage_id.id,
                    'period_id': period_id,
                    'journal_id': journal_id,
                    'date': date_move,
                    'name': name_move,
                    'amount_currency':self._convert_amount(cr, uid,avantage,currency_id, currency_company_id, context=ctx),
                    'debit':   avantage,
                    'credit':0.0,
                    'currency_id': currency_id,
                    'state': 'valid'
                }
                move_lines.append((0, 0, val))           

            # 2
            if irpp :
                name_move = u'IRPP'
                val = {
                    #'account_id': dict_param['account_irpp_id'][0],
                    'account_id': bulletin.employee_id.account_irpp_id.id,
                    'period_id': period_id,
                    'journal_id': journal_id,
                    'date': date_move,
                    'name': name_move,
                    'amount_currency':-1*irpp,
                    'debit': 0.0,
                    #'credit':  self._convert_amount(cr, uid,irpp,currency_id, currency_company_id, context=ctx),
                    'credit':irpp,
                    'currency_id': currency_id,
                    'state': 'valid'
                }
                move_lines.append((0, 0, val))            
            #1
            if salaire_net_a_payer :
                name_move = u'Nets payées'
                val = {
                    #'account_id': dict_param['account_net_paye_id'][0],
                    'account_id': bulletin.employee_id.account_net_paye_id.id,
                    'period_id': period_id,
                    'journal_id': journal_id,
                    #'partner':bulletin.employee_id.name ,
                    #'partner_id': bulletin.employee_id.id,
                    'date': date_move,
                    'name': name_move,
                    'amount_currency':-1*salaire_net_a_payer,
                    'debit': 0.0,
                    #'credit':  self._convert_amount(cr, uid,salaire_net_a_payer,currency_id, currency_company_id, context=ctx),
                    'credit':salaire_net_a_payer,
                    'currency_id': currency_id,
                    'state': 'valid'
                }
                print '***val**',val
                move_lines.append((0, 0, val)) 
            # move_lines.sort(cmp=None, key=None, reverse=True)
            # create move
            out = ' '
            move = {#'ref': sal.name + out +  bulletin.employee_id.name or '/',
                    'ref': 'Salaire' + out + sal.period_id.name+ out+ bulletin.employee_id.name or '/',
                    'period_id': period_id,
                    'journal_id': journal_id,
                    'date': date_move,
                    'state': 'draft',
                    'name':  '/',
                    'line_id': move_lines
                    }
           
            
            move_id = self.pool.get('account.move').create(
                cr, uid, move, context=context)
            self.pool.get('hr.payroll.bulletin').write(cr, uid,bulletin.id, {'move_id': move_id})
         
            # write move_id for this salaire
            
            if update:
                self.pool.get('hr.payroll').write(cr, uid, sal.id, {'move_id': move_id})

                
            return True
        
    # generation des ecriture comptable pour états payé
    def _move_create_net_paye(self, cr, uid, ids,bulletin_lines,update):
        
        context = {}
        for sal in self.browse(cr, uid, ids):
            # parametres account
            params = self.pool.get('hr.payroll.parametres')
            ids_params = params.search(cr, uid, [('fiscalyear_id', '=', sal.period_id.fiscalyear_id.id)])
            if not ids_params:
                raise osv.except_osv(_('Erreur !'), _(u"Veuillez vérifier les paramétres de paie pour l'année Fiscal courante"))
            dict_param = params.read(cr, uid, ids_params[0])
            # Journal  and currency
            journal_bank_id = dict_param['account_journal_bank_id'][0]
            if not journal_bank_id:
                raise osv.except_osv(_('UserError'), _('Veuillez indiquer un journal des virement salaires dans le paramétrage de la comptabilité de la paie. '))
            journal_bank = self.pool.get('account.journal').browse(cr, uid, journal_bank_id, context=context)
            if journal_bank.centralisation:
                raise osv.except_osv(
                    _('UserError'), _('Cannot create salary move on centralised journal'))

            
            # currency_id = journal.currency and journal.currency.id or journal.company_id.currency_id.id
            currency_id = journal_bank.currency and journal_bank.currency.id or journal_bank.company_id.currency_id.id
            currency_company_id= sal.company_id.currency_id.id
            ctx = context.copy()
            ctx.update({'date': sal.date_salary})
            
            # date and period
            date_move = sal.date_salary or time.strftime('%Y-%m-%d')
            period_id = sal.period_id and sal.period_id.id or False

            if not period_id:
                raise osv.except_osv(_('UserError'), _(u'Période obligatoire'))
            
            period = self.pool.get('account.period').browse(cr, uid, period_id, context=context)
            # name
            name_move = "Salaire " + period.name
            salaire_net_a_payer = 0.0
            
            for bulletin in bulletin_lines:
                salaire_net_a_payer += bulletin.salaire_net_a_payer
                
                 
            move_p = {}
            move_p_lines = []


            if salaire_net_a_payer :
                name_move = u'Nets payées'
                val = {
                    #'account_id': dict_param['account_net_paye_id'][0],
                    'account_id': bulletin.employee_id.account_net_paye_id.id,
                    'period_id': period_id,
                    'journal_id': journal_bank_id,
                    #'partner':bulletin.employee_id.name ,
                    #'partner_id': bulletin.employee_id.id ,
                    'date': date_move,
                    'name': name_move,
                    'amount_currency':-1*salaire_net_a_payer,
                    'debit': 0.0,
                    'credit':  self._convert_amount(cr, uid,salaire_net_a_payer,currency_id, currency_company_id, context=ctx),
                    'currency_id': currency_id,
                    'state': 'valid'
                }
                print '***val**',val
                move_p_lines.append((0, 0, val))   
                #2 instance : contre partie
            if salaire_net_a_payer :
                name_move = u'Paiement'
                val = {
                    #'account_id': dict_param['account_banque_employeur_id'][0],
                    'account_id': bulletin.employee_id.account_banque_employeur_id.id,
                    'period_id': period_id,
                    'journal_id': journal_bank_id,
                    #'partner':bulletin.employee_id.name ,
                    #'partner_id': bulletin.employee_id.id ,
                    'date': date_move,
                    'name': name_move,
                    'amount_currency':1*salaire_net_a_payer,
                    'debit': self._convert_amount(cr, uid,salaire_net_a_payer,currency_id, currency_company_id, context=ctx),
                    'credit': 0.0, 
                    'currency_id': currency_id,
                    'state': 'valid'
                }
                print '***val**',val
                move_p_lines.append((0, 0, val))                               
            # move_lines.sort(cmp=None, key=None, reverse=True)
            # create move
            move_p = {#'ref': u"Nets payées" + ' ' + sal.month_id.name + ' ' + bulletin.employee_id.name or '/',
                      'ref': u"Nets payées" + ' ' + sal.period_id.name + ' ' + bulletin.employee_id.name or '/',
                    'period_id': period_id,
                    'journal_id': journal_bank_id,
                    'date': date_move,
                    'state': 'draft',
                    'name':  '/',
                    'line_id': move_p_lines
                    }            
            

            
            move_p_id = self.pool.get('account.move').create(
                cr, uid, move_p, context=context)
            self.pool.get('hr.payroll.bulletin').write(cr, uid,bulletin.id, {'move_p_id': move_p_id})            
            # write move_id for this salaire
            
            if update:
                self.pool.get('hr.payroll').write(cr, uid, sal.id, {'move_id': move_p_id})

                
            return True
        
hr_payroll_tn()

class account_move_line(osv.osv):
    _inherit = "account.move.line"
        
    def _check_currency_company(self, cr, uid, ids, context=None):
        for l in self.browse(cr, uid, ids, context=context):
            if l.currency_id.id == l.company_id.currency_id.id:
                return True
        return True
        
    _columns = {
               #'partner': fields.char('Employée'),
            }
    _constraints = [
        (_check_currency_company, "You cannot provide a secondary currency if it is the same than the company one." , ['currency_id']),
    ]
    
                    
account_move_line()

class hr_payroll_bulletin_tn(osv.osv):
    _inherit = "hr.payroll.bulletin"
    _columns = {
        'move_id': fields.many2one('account.move', u'Pièce comptable', readonly=True),
        'move_p_id': fields.many2one('account.move', u'Pièce comptable(Payement)', readonly=True),
    }
    
    


hr_payroll_bulletin_tn()

                
            
    