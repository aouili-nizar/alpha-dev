# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv 
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from datetime import date, datetime


 

class hr_payroll(osv.osv):
    
    STATE = [
            ('draft', 'Brouillon'),
            ('confirmed', u'Confirmé'),
            ('paid', u'Payé'),
            ('declared', u'Declaré'),
            ('versed', u'Versé'),
           # ('cancelled', u'Annulé')
            ]
#  
#     def unlink(self, cr, uid, ids, context=None):
#         saisie_mensuelles = self.read(cr, uid, ids, ['state'], context=context)
#         unlink_ids = []
#         for s in saisie_mensuelles:
#             if s['state'] in ['draft', 'cancelled']:
#                 unlink_ids.append(s['id'])
#             else:
#                 raise osv.except_osv(_('Action non valide  !'), _('Vous ne pouvez pas supprimer les saisies mensuelles confirmées !'))
#         return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)



    def _get_currency(self, cr, uid, context):
        if context is None:
            context = {}
        currency_obj = self.pool.get('res.currency')
        res = currency_obj.search(cr, uid, [('symbol', '=', 'DH')], limit=1)
        if res:
            return res[0]
        else:
            return False



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
            
    def _total_net(self, cr, uid, ids, name, arg, context={}):
        result = {}
        for payroll in self.browse(cr, uid, ids, context):
            net = 0
            for line in payroll.bulletin_line_ids:
                net += line.salaire_net_a_payer
            result[payroll.id] = net
        return result

    def _bulletin_count_(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for payroll in self.browse(cr, uid, ids):
            res[payroll.id]=len(payroll.bulletin_line_ids)
        return res
    
    
    _name = "hr.payroll"
    _inherit = ['mail.thread']
    _description = 'Saisie des bulletins'
    _order = "number"
    _columns = {
        'name': fields.char('Description', size=64, readonly=True, states={'draft':[('readonly', False)]}),
        'number': fields.char('Numero du salaire', size=32, readonly=False),
        'date_salary': fields.date('Date salaire', readonly=True, states={'draft':[('readonly', False)]}),
        'company_id': fields.many2one('res.company', u'Société', change_default=True, readonly=True, required=True, states={'draft':[('readonly', False)]}),
        'month_id': fields.many2one('hr.month', 'Mois', readonly=True, required=True, states={'draft':[('readonly', False)]}, select=1),
        'period_id': fields.many2one('account.period',u'Période Comptable', domain=[('state', '<>', 'done')], readonly=True, required=True, states={'draft':[('readonly', False)]}, select=1),
        'bulletin_line_ids': fields.one2many('hr.payroll.bulletin', 'id_payroll', 'Bulletins', readonly=True, states={'draft':[('readonly', False)]}),
        'move_id': fields.many2one('account.move', 'salary Movement', readonly=True, help="Link to the automatically generated account moves."),
        'state': fields.selection(STATE, 'Etat', select=True, readonly=True),
        'total_net': fields.function(_total_net, method=True, type='float', digits_compute=dp.get_precision('Montant Paie'), string='Total net'),
        'bulletinn_count': fields.function(_bulletin_count_, type='integer', string="Bulletins" ),
        }
    def _name_get_default(self, cr, uid, context=None):
            return self.pool.get('ir.sequence').get(cr, uid, 'hr.payroll')
    _defaults = {
        'number': _name_get_default,
        'date_salary': lambda * a: time.strftime('%Y-%m-%d'),
        'state': lambda * a: 'draft',
        'month_id' :_get_month_id,
        'company_id': _get_company_id,

    }
 
    def onchange_month_id(self, cr, uid, ids, month_id, company_id):
        result={}
        if  month_id and  company_id:
            #TODO: you cannot test by month_id because user can put the month in two year
            #must use month_id and period_id
            count=self.search_count(cr,uid,[('month_id','=',month_id),('company_id','=',company_id)] )
            if count > 0 :
                warning = {'title':_('Attention'), 'message':_(u'Le saisie de paie  d\'une période doit être unique par société!')}
                value = {'period_id': False,'month_id':False}
                return {'warning': warning, 'value': value}
            company = self.pool.get('res.company').browse(cr, uid, company_id)
            month = self.pool.get('hr.month').browse(cr, uid, month_id)
            result = {'value': 
                             {  'name' :   _(u'Salaires %s du mois %s') % (company.name, month.name), 
                                 'period_id' : month.period_id.id
                              }
                    }
        return result  
        

    def draft_cb(self, cr, uid, ids, context=None):
        for sal in self.browse(cr, uid, ids):
            if sal.move_id:
                raise osv.except_osv(_('Error !'), _(u'Veuillez d\'abord supprimer les écritures comptables associés'))
        for sal in self.browse(cr, uid, ids):
            bulletins = self.pool.get('hr.payroll.bulletin').search(cr, uid, [('id_payroll', '=', sal.id)])
            print bulletins
            bulletins2 = self.pool.get('hr.payroll.bulletin').browse(cr, uid, bulletins)
            for bul in bulletins2:
                bul.draft_bulletin()
        return self.write(cr, uid, ids, {'state':'draft'}, context=context)
    
    def draft_pb(self, cr, uid, ids, context=None):
        for sal in self.browse(cr, uid, ids):
            if sal.move_id:
                raise osv.except_osv(_('Error !'), _(u'Veuillez d\'abord supprimer les écritures comptables associés'))
        for sal in self.browse(cr, uid, ids):
            bulletins = self.pool.get('hr.payroll.bulletin').search(cr, uid, [('id_payroll', '=', sal.id)])
            print bulletins
            bulletins2 = self.pool.get('hr.payroll.bulletin').browse(cr, uid, bulletins)
            for bul in bulletins2:
                bul.cancel_bulletin()
        return self.write(cr, uid, ids, {'state':'draft'}, context=context)
    
    def draft_db(self, cr, uid, ids, context=None):
        for sal in self.browse(cr, uid, ids):
            if sal.move_id:
                raise osv.except_osv(_('Error !'), _(u'Veuillez d\'abord supprimer les écritures comptables associés'))
        for sal in self.browse(cr, uid, ids):
            bulletins = self.pool.get('hr.payroll.bulletin').search(cr, uid, [('id_payroll', '=', sal.id)])
            print bulletins
            bulletins2 = self.pool.get('hr.payroll.bulletin').browse(cr, uid, bulletins)
            for bul in bulletins2:
                bul.draft_bulletin()
        return self.write(cr, uid, ids, {'state':'draft'}, context=context)
    def draft_vb(self, cr, uid, ids, context=None):
        for sal in self.browse(cr, uid, ids):
            if sal.move_id:
                raise osv.except_osv(_('Error !'), _(u'Veuillez d\'abord supprimer les écritures comptables associés'))
        for sal in self.browse(cr, uid, ids):
            bulletins = self.pool.get('hr.payroll.bulletin').search(cr, uid, [('id_payroll', '=', sal.id)])
            print bulletins
            bulletins2 = self.pool.get('hr.payroll.bulletin').browse(cr, uid, bulletins)
            for bul in bulletins2:
                bul.draft_bulletin()
        return self.write(cr, uid, ids, {'state':'draft'}, context=context)
    

    def declar_db(self, cr, uid, ids, context=None):
        for sal in self.browse(cr, uid, ids):
            bulletins = self.pool.get('hr.payroll.bulletin').search(cr, uid, [('id_payroll', '=', sal.id)])
            print bulletins
            bulletins2 = self.pool.get('hr.payroll.bulletin').browse(cr, uid, bulletins)
            for bul in bulletins2:
                bul.declar_bulletin()

        return self.write(cr, uid, ids, {'state':'declared'}, context=context)
    
    def verse_vb(self, cr, uid, ids, context=None):
        for sal in self.browse(cr, uid, ids):
            bulletins = self.pool.get('hr.payroll.bulletin').search(cr, uid, [('id_payroll', '=', sal.id)])
            print bulletins
            bulletins2 = self.pool.get('hr.payroll.bulletin').browse(cr, uid, bulletins)
            for bul in bulletins2:
                bul.verse_bulletin()

        return self.write(cr, uid, ids, {'state':'versed'}, context=context)


    
    def cancel_cb(self, cr, uid, ids, context=None):
        for sal in self.browse(cr, uid, ids):
            bulletins = self.pool.get('hr.payroll.bulletin').search(cr, uid, [('id_payroll', '=', sal.id)])
            print bulletins
            bulletins2 = self.pool.get('hr.payroll.bulletin').browse(cr, uid, bulletins)
            for bul in bulletins2:
                bul.cancel_bulletin()
        return self.write(cr, uid, ids, {'state':'paid'}, context=context)
    
    



    def confirm_cb(self, cr, uid, ids, context=None):
        #self.action_move_create(cr, uid, ids)
        for sal in self.browse(cr, uid, ids):
            bulletins = self.pool.get('hr.payroll.bulletin').search(cr, uid, [('id_payroll', '=', sal.id)])
            bulletins2 = self.pool.get('hr.payroll.bulletin').browse(cr, uid, bulletins)
            for bul in bulletins2:
                bul.confirm_bulletin()
        self.write(cr, uid, ids, {'state':'confirmed'}, context=context)
        return True
    


    def compute_all_lines(self, cr, uid, ids, context={}):
        for sal in self.browse(cr, uid, ids):
            bulletins = self.pool.get('hr.payroll.bulletin').search(cr, uid, [('id_payroll', '=', sal.id)])
            bulletins2 = self.pool.get('hr.payroll.bulletin').browse(cr, uid, bulletins)
            for bul in bulletins2:
                bul.compute_all_lines()
        return True

    def generate_employees(self, cr, uid, ids, context={}):
        pointage_obj = self.pool.get('hr.pointage')
        payroll = self.pool.get('hr.payroll').browse(cr, uid, ids[0])
        # get employe  have pointage from this periode
        pointage_ids = pointage_obj.search(cr, uid, [('period_id', '=', payroll.period_id.id)]) 
        if not pointage_ids:
            raise osv.except_osv(_(u'Pointage non définie !'), _(u"Vous devez  saisir le pointage de cet période !"))
        pointage = pointage_obj.browse(cr, uid, pointage_ids[0])
        if pointage.state != 'confirmed' :
            raise osv.except_osv(_(u'Pointage non validé !'), _(u"Veuillez valider le pointage de cet période  !"))
        # delete old bulletin
        sql = '''   DELETE from hr_payroll_bulletin  where id_payroll = %s '''
        cr.execute(sql, (payroll.id,))
        #
        all_bulletin = []
        for  pointage_line in pointage.pointage_line_ids :  
            val = (0, 0, {'employee_id':  pointage_line.employee_id.id,
                          'employee_contract_id': pointage_line.employee_id.contract_id.id,
                          'pointage' : pointage_line.nb_pointage,
                          'salaire_base' :pointage_line.employee_id.contract_id.wage,
                          'pointage_line_id':pointage_line.id,
                          'month_id':payroll.month_id.id
                          
                          }
                    )
            all_bulletin.append(val)            
        value = {  'bulletin_line_ids': all_bulletin }   
        self.write(cr, uid, payroll.id, value, context=context)
        return True


    def action_move_create(self, cr, uid, ids):
        return True

hr_payroll()



 

#===============================================================================
# hr_payroll_bulletin
#===============================================================================
class hr_payroll_bulletin(osv.osv):
    _name = "hr.payroll.bulletin"
    _description = 'bulletin'
    _rec_name = 'employee_id' 
    _order ="id desc"
    _columns = {
        'name': fields.char('Numero du salaire', size=32, readonly=False),
        'date_salary': fields.date('Date salaire', select=1, readonly=True, states={'draft':[('readonly', False)]}),
        'employee_id': fields.many2one('hr.employee', u'Employé', change_default=True, readonly=True, required=True, select=1),
        'period_id': fields.many2one('account.period', u'Période', select=1, readonly=True, states={'draft':[('readonly', False)]}),
        'month_id': fields.many2one('hr.month', 'Mois',  readonly=True, states={'draft':[('readonly', False)]}),
        'salary_line_ids': fields.one2many('hr.payroll.bulletin.line', 'id_bulletin', 'Lignes de salaire', readonly=True),
        'employee_contract_id' : fields.many2one('hr.contract', u'Contrat de travail', required=True, readonly=True, states={'draft':[('readonly', False)]}),
        'id_payroll': fields.many2one('hr.payroll', 'Ref Salaire', ondelete='cascade', select=True),
        'salaire_base' : fields.float('Salaire de base', digits_compute=dp.get_precision('Montant Paie'), readonly=True, states={'draft':[('readonly', False)]}),
        # 'normal_hours' : fields.float('Heures travaillee durant le mois'),
        # 'hour_base' : fields.float('Salaire heure'),
        'comment': fields.text('Informations complementaires'),
        'salaire':fields.float('Salaire Base', digits_compute=dp.get_precision('Montant Paie'), readonly=True, states={'draft':[('readonly', False)]}),
        'salaire_brute':fields.float('Salaire Brute', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'salaire_base_brut':fields.float('Salaire Brute', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'salaire_brute_imposable':fields.float('Salaire brute imposable', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'salaire_net':fields.float('Salaire Net', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'salaire_net_a_payer':fields.float(u'Salaire net à payer', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'salaire_brute_cotisable':fields.float('Salaire brute cotisable', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'cotisations_employee':fields.float('Cotisations Employé', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'cotisations_employer':fields.float('Cotisations Employeur', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'igr':fields.float('IRPP', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'mnt_redevance':fields.float('Redevance de compensation', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'mnt_conge_paye':fields.float(u'Montant congé payé', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'mnt_conge_rubriques_paye':fields.float(u'Montant congé rubriques payé', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'prime':fields.float('Primes', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'indemnite':fields.float('Indemnites', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'avantage':fields.float('Avantages', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'exoneration':fields.float('Exonerations', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'deduction':fields.float('Deductions', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'pointage' : fields.float('Jours travaillé', size=64, digits_compute=dp.get_precision('Montant Paie'), readonly=True, states={'draft':[('readonly', False)]}),
        'loan_amount':fields.float('Montant Prets', readonly=True, digits_compute=dp.get_precision('Montant Paie')),
        'pointage_line_id': fields.many2one('hr.pointage.line', u'Ligne de Pointage',),
        'note': fields.text('Note',),
        'montant_text' :fields.char(string='Montant en toutes  lettres '),
        
        'frais_pro': fields.float('Frais professionnels', size=64, digits_compute=dp.get_precision('Montant Paie')),
        'state': fields.selection([
            ('draft', 'Brouillon'),
            ('confirmed', 'Confirmé'),
            ('paid', u'Payé'),
            ('declared', u'Declaré'),
            ('versed', u'Versé')
        ], 'Etat', select=2, readonly=True),
            
        #conge
        'nb_jours_cp_attribue': fields.float(u'CP attribués',),
        'nb_jours_cp_pris': fields.float(u'CP pris ce mois',),  
        'nb_jours_cp_total_pris': fields.float(u'Total CP pris',),       
        'nb_jours_cp_total': fields.float('Total CP',),
        'nb_jours_cp_solde': fields.float('Solde Congé',),
         
        }
    

    

    
    def _name_get_default(self, cr, uid, context=None):
            return self.pool.get('ir.sequence').get(cr, uid, 'hr.payroll.bulletin')
    _defaults = {
        'name': _name_get_default,
        'state' :'draft',

    }
    def _check_unicite(self, cr, uid, ids):
        for unicite in self.browse(cr, uid, ids):
            unicite_id = self.search(cr, uid, [('period_id', '=', int(unicite.period_id)), ('employee_id', '=', int(unicite.employee_id)) ])
            if len(unicite_id) > 1:
                return False
        return True

    _constraints = [
        (_check_unicite, u'Un bulletin de paie est repété pour un même employé', ['period', 'employee'])
        ]
    def onchange_contract_id(self, cr, uid, ids, contract_id):
        salaire_base = 0
        if contract_id:
            contract = self.pool.get('hr.contract').browse(cr, uid, contract_id)
            salaire_base = contract.wage
        result = {'value': { 'salaire_base' : salaire_base,} }
        return result

    def cancel_bulletin(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'paid'}, context=context)

    def draft_bulletin(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'draft'}, context=context)

    def confirm_bulletin(self, cr, uid, ids, context=None):

        #create attribution Droit à des congés payés
#         params_obj= self.pool.get('hr.payroll.parametres')
#         hr_employee_obj = self.pool.get('hr.employee')
#         hr_holidays = self.pool.get('hr.holidays')
#         hr_holidays_status = self.pool.get('hr.holidays.status')
#         status_search_ids=hr_holidays_status.search(cr, uid, [('payed','=',True)],context)        
#         for bulletin in self.browse(cr, uid, ids, context=None):
#             ids_params = params_obj.search(cr, uid, [('fiscalyear_id', '=', bulletin.period_id.fiscalyear_id.id)])
#             params = params_obj.read(cr, uid, ids_params[0])
#            
#             return True             
        
        return self.write(cr, uid, ids, {'state':'confirmed'}, context=context)
    
    def declar_bulletin(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'declared'}, context=context)
    
    def verse_bulletin(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'versed'}, context=context)
    

    def onchange_employee_id(self, cr, uid, ids, employee_id, period_id):
        if not employee_id :
            return {}
        if not period_id:
            raise osv.except_osv(_(u'Période non définie !'), _(u"Vous devez d\'abord spécifier une période !"))
        if period_id and employee_id :
            
            period = self.pool.get('account.period').browse(cr, uid, period_id)
            params = self.pool.get('hr.payroll.parametres')
            ids_params = params.search(cr, uid, [('fiscalyear_id', '=',period.fiscalyear_id.id)])
            if not ids_params:
                raise osv.except_osv(_('Attention  !'), _(u'''Veuillez définir les paramétres de paie pour l'exercice courant : 
                                                         Menu Configuration>>Paie>>Paramètres !'''))
            dictionnaire = params.read(cr, uid, ids_params[0])
            
            parms = self.pool.get('hr.payroll.parametres')
            fiscalyear_id = self.pool.get('account.fiscalyear').find(cr, uid)
            ids_parms = parms.search(cr, uid, [('fiscalyear_id', '=', fiscalyear_id)])
            dictionnaire = parms.read(cr, uid, ids_parms[0])
                        
#             nb_jour=22
            nb_jour = dictionnaire['nb_jour_5j']
            if dictionnaire['regime'] == '48' :
                nb_jour = dictionnaire['nb_jour_6j']
#                 nb_jour=26
            print'***nombre_jour*',nb_jour
            employee = self.pool.get('hr.employee').browse(cr, uid, employee_id)
            if not employee.contract_id:
                raise osv.except_osv(_(u'Pas de contrat !'), _(u"Vous devez d\'abord saisir un contrat pour cet employé !"))

            sql = '''select sum(number_of_days) from hr_holidays h
                left join hr_holidays_status s on (h.holiday_status_id=s.id)
                where date_from >= '%s' and date_to <= '%s' 
                and employee_id = %s 
                and state = 'validate' 
                and s.payed=False''' % (period.date_start, period.date_stop, employee_id)
            cr.execute(sql)
            res = cr.fetchone()
            if res[0] == None:
                days = 0
            else :
                days = res[0]
                                
            result = {'value': {
                            'employee_contract_id' : employee.contract_id.id,
                            'salaire_base' : employee.contract_id.wage,
                             # 'hour_base' : employee.contract_id.hour_salary,
                             # 'normal_hours' : employee.contract_id.monthly_hour_number,
                            'pointage' : nb_jour - abs(days),
                            'period_id' : period_id
                        }
                    }

            return result



    def get_irpp(self, cr, uid, employee_id, salaire_brute_imposable):
        '''
        Fonction de calcul de IRPP
        :param cr:
        :param uid:
        :param employee_id:
        :param salaire_brute_imposable:
        @return: montant Impot
        '''
        params = self.pool.get('hr.payroll.parametres')
        fiscalyear_id = self.pool.get('account.fiscalyear').find(cr, uid)
        ids_params = params.search(cr, uid, [('fiscalyear_id', '=', fiscalyear_id)])
        if not ids_params:
            raise osv.except_osv(_('Attention  !'), _(u'''Veuillez définir les paramétres de paie pour l'exercice courant : 
                                                         Menu Configuration>>Paie>>Paramètres !'''))
        
        mntImpot=0.0
        employee = self.pool.get('hr.employee').browse(cr, uid, employee_id)
        if employee.contract_id.type_id and  not employee.contract_id.type_id.irpp:
            return mntImpot
            
        dictionnaire = params.read(cr, uid, ids_params[0])
        salaire_net_imposable = salaire_brute_imposable * 12 
        
        if salaire_net_imposable > 5000.0 :#TODO: do it configurable
            # parent a charge
            salaire_net_imposable -= ( employee.nb_parents * (dictionnaire['parent_charge'] or 0))
            # fraispro
            mnt_FP=salaire_net_imposable * dictionnaire['fraispro'] / 100
            if mnt_FP > 2000.0:
                mnt_FP = 2000.0
            salaire_net_imposable -= mnt_FP
            # assurance vie
            if(employee.assurance) : 
                salaire_net_imposable -= (employee.amount_assurance )
            # Chef de famille
            if(employee.chef_famille) : 
                salaire_net_imposable -= dictionnaire['chef_famille']
              
            # nb enfant 
            children = employee.children
            mnt_enfant = 0.0
            if(children == 1) :
                mnt_enfant = dictionnaire['enfant1']   
            elif (children == 2) :
                mnt_enfant = dictionnaire['enfant1'] + dictionnaire['enfant2']  
            elif (children == 3) :
                mnt_enfant = dictionnaire['enfant1'] + dictionnaire['enfant2'] + dictionnaire['enfant3']         
            elif (children >= 4) :
                mnt_enfant = dictionnaire['enfant1'] + dictionnaire['enfant2'] + dictionnaire['enfant3'] + dictionnaire['enfant4']     
            salaire_net_imposable -= mnt_enfant
             
            #etudiants
            salaire_net_imposable -= (employee.nb_enfant_etudiant * dictionnaire['enfant_etudiant'])
            
            #handicape 
            salaire_net_imposable -= (employee.nb_enfant_handicape * dictionnaire['enfant_handicape'])        
             
            # ir      
            objet_ir = self.pool.get('hr.payroll.ir')
            id_ir = objet_ir.search(cr, uid, [])
            liste = objet_ir.read(cr, uid, id_ir, ['debuttranche', 'fintranche', 'taux'])
            i = 0
            mntPrev = 0.0
            mntSup = 0.0
            mntImpot = 0.0
            while (i < len(liste)) :
                TranchesImpot = liste[i]  
                if (salaire_net_imposable > mntPrev) :
                    if(salaire_net_imposable > TranchesImpot['fintranche']) : 
                        mntSup = TranchesImpot['fintranche']
                    else : 
                        mntSup = salaire_net_imposable
                    mntImpot += (mntSup - mntPrev) / 100 * TranchesImpot['taux']
                mntPrev = TranchesImpot['fintranche']
                i += 1
            mntImpot = mntImpot / 12    
            salaire_net_imposable = salaire_net_imposable / 12
            
        return mntImpot

    def get_cotisations(self, cr, uid, employee_id, salaire_brute_cotisable):
        '''
        Calculer Cotisations
        :param cr:
        :param uid:
        :param employee_id:
        :param salaire_brute_cotisable:
        @return: lignes de cotisations, montant cotisations employee,montant cotisations employer    
        '''
        employee = self.pool.get('hr.employee').browse(cr, uid, employee_id)
        cotisations = employee.contract_id.type_id.cotisation.cotisation_ids
        base = salaire_brute_cotisable
        cotisations_employee=0.0
        cotisations_employer=0.0
        res=[]
        for cot in cotisations :
            cotisation_line = {
                            'name' : cot.name,
                            'base' : base,
                            'taux' : cot.tauxsalarial,
                            'rate_employer' : cot.tauxpatronal,
                            'retenu':base * cot.tauxsalarial / 100,
                            'subtotal_employer':base * cot.tauxpatronal / 100,
                            } 
            res.append(cotisation_line)
            cotisations_employee += base * cot['tauxsalarial'] / 100
            cotisations_employer += base * cot['tauxpatronal'] / 100
        return res,cotisations_employee,cotisations_employer             
                        
    def get_prets(self, cr, uid, pointage_line):
        '''
        Les prets
        :param cr:
        :param uid:
        :param pointage_line:
        '''
        #gestion des avances 
        all_pret=[]
        avance_line_obj = self.pool.get('hr.avance.line')
        avance_line_ids = avance_line_obj.search(cr, uid, [('avance_id.month_id', '=', pointage_line.pointage_id.month_id.id) ,
                                                       ('employee_id', '=', pointage_line.employee_id.id) ,
                                                       ])
        for  avance_line in  avance_line_obj.browse(cr, uid, avance_line_ids) :
            avance = {'name' : _(u'Avance n° : ')+avance_line.avance_id.name,
                      'montant':avance_line.amount,
                     }
            all_pret.append(avance)        
        return all_pret
    
    def get_heure_supplementaire(self, cr, uid, pointage_line, base):
        '''
        Get Heures supplementaire
        :param cr:
        :param uid:
        :param pointage_line:
        :param base:
        '''
        res = []
        if pointage_line.hs100:
            line_hs100 = {
                    'name' : _(u'Heures supplémentaires : HS100'),
                    'base' :  base ,
                    'taux' :  pointage_line.hs100  ,
                    'gain': float(base * pointage_line.hs100 * 1),
                   }  
            res.append(line_hs100)
         
        if pointage_line.hs125:
            line_hs125 = {
                    'name' : _(u'Heures supplémentaires : HS125'),
                    'base' :  base ,
                    'taux' :  pointage_line.hs125  ,
                    'gain': float(base * pointage_line.hs125 * 1.25),
                   }
            res.append(line_hs125)
                            
        if pointage_line.hs150:
            line_hs150 = {
                    'name' : _(u'Heures supplémentaires : HS150'),
                    'base' :  base ,
                    'taux' :  pointage_line.hs150  ,
                    'gain': float(base * pointage_line.hs150 * 1.50),
                   } 
            res.append(line_hs150)              
                
        if pointage_line.hs175:
            line_hs175 = {
                    'name' : _(u'Heures supplémentaires : HS175'),
                    'base' :  base ,
                    'taux' :  pointage_line.hs175  ,
                    'gain': float(base * pointage_line.hs175 * 1.75),
                   }   
            res.append(line_hs175)
                 
        if pointage_line.hs200:
            line_hs200 = {
                    'name' : _(u'Heures supplémentaires : HS200'),
                    'base' :  base ,
                    'taux' :  pointage_line.hs200  ,
                    'gain': float(base * pointage_line.hs200 * 2.0),
                   }                   
            res.append(line_hs200)
                            
        return res                 
 
    def get_info_base(self, cr, uid, regime, salaire_base):
        '''
        Get Heures supplementaire
        :param cr:
        :param uid:
        :param pointage_line:
        :param base:
        '''
        regime_contact = regime.type_regime
        
        params = self.pool.get('hr.payroll.parametres')
        fiscalyear_id = self.pool.get('account.fiscalyear').find(cr, uid)
        ids_params = params.search(cr, uid, [('fiscalyear_id', '=', fiscalyear_id)])
        dictionnaire = params.read(cr, uid, ids_params[0])
        
        nb_jour = dictionnaire['nb_jour_5j']
#         nb_jour=22
        if regime_contact=='mensuel':
            if regime.hours_mensuel == '48':
#                nb_jour=26
                nb_jour = dictionnaire['nb_jour_6j']
        print '**nb_jour*',nb_jour        
                
        if regime_contact == 'horaire':
            base = base_heure=  salaire_base
        elif regime_contact == 'journalier' :
            base = salaire_base
            base_heure= base /8.0
            base_heure= round(base_heure, self.pool.get('decimal.precision').precision_get(cr, uid, 'Montant Paie'))
        else :
            base = salaire_base / nb_jour  # old :salaire_base / taux
            base_heure= base /8.0
            base_heure= round(base_heure, self.pool.get('decimal.precision').precision_get(cr, uid, 'Montant Paie')) 
        
        return   nb_jour,base,base_heure,salaire_base      
        

   
    def compute_all_lines(self, cr, uid, ids, context={}):
        bulletin_line_obj = self.pool.get('hr.payroll.bulletin.line')
        id_bulletin = ids[0]
        bulletin = self.pool.get('hr.payroll.bulletin').browse(cr, uid, id_bulletin)
        self.write(cr, uid, [bulletin.id], {'period_id' : bulletin.id_payroll.period_id.id})
        sql = '''
        DELETE from hr_payroll_bulletin_line where id_bulletin = %s
        '''
        cr.execute(sql, (id_bulletin,))
        salaire_base = bulletin.salaire_base
        salaire_base_brut =0.0
        salaire_brute = 0.0
        prime = 0.0
        indemnite = 0.0
        avantage = 0.0
        mnt_rubriques=0.0
        exoneration_irpp = 0.0
        exoneration_cotisable = 0.0
        deduction = 0.0
        loan_amount= 0.0
        mnt_Impot=0.0
        mnt_redevance=0.0
        base = 0.0
        base_heure=0.0
        regime= bulletin.employee_contract_id.regime_id
        regime_contact = regime.type_regime
        base_conge_rubriques = 0.0
        mnt_conge_paye=0.0
        mnt_conge_rubriques_paye =0.0

        
        params_obj= self.pool.get('hr.payroll.parametres')
        ids_params = params_obj.search(cr, uid, [('fiscalyear_id', '=', bulletin.period_id.fiscalyear_id.id)])
        params = params_obj.read(cr, uid, ids_params[0])

 
 
        if salaire_base :
        #--------------salaire_base-------------------------------------------------
        #-------salaire_base_brut pour comtabilisé le jour impayé-------------------
            taux = bulletin.pointage
            
            nb_jour,base,base_heure,salaire_base =self.get_info_base(cr, uid, regime, salaire_base)   
            nb_imp_days_holiday=bulletin.pointage_line_id.nb_imp_days_holiday
            salaire_base_line = {
                    'name' : _(u'Salaire de base'),
                    'id_bulletin' : id_bulletin,
                    'type' : 'brute',
                    'base' :  base ,
                    'taux' :  taux  ,
                    'gain':  taux * base,
                    'retenu':0.0,
                    'sequence':1
                   }
            salaire_brute += taux * base
            salaire_base_brut +=nb_imp_days_holiday *base
            print '****salaire_base_brut***',salaire_base_brut
            bulletin_line_obj.create(cr, uid, salaire_base_line)
            


        #--------------conge paye-------------------------------------------------      
            nb_jours_cp_solde=bulletin.pointage_line_id.total_days_restante
            nb_days_holiday=bulletin.pointage_line_id.nb_days_holiday 
#             if nb_days_holiday != 0 :
#                 conge_pay_line = {
#                         'name' : _(u'Congés payés'),
#                         'id_bulletin' : id_bulletin,
#                         'type' : 'brute',
#                         'base' :  base ,
#                         'taux' : nb_days_holiday ,
#                         'gain':  nb_days_holiday * base,
#                         'sequence':3
#                        }
#                 salaire_brute += nb_days_holiday * base
#                 bulletin_line_obj.create(cr, uid, conge_pay_line)            
        nb_jours_cp_pris = nb_days_holiday  
        nb_jours_cp_solde = nb_jours_cp_solde
        #--------------Heure supplementaire------------------------------------------------- 
        #base   TODO: pourqoui ce 'base ' sans valeur       
        res_hs = self.get_heure_supplementaire(cr, uid, bulletin.pointage_line_id, base_heure)
        if  res_hs:
            for hs in res_hs :
                line_hs = {
                    'name' : hs['name'],
                    'id_bulletin' : id_bulletin,
                    'type' : 'hs',
                    'base' :  hs['base'] ,
                    'taux' :  hs['taux']  ,
                    'gain':  hs['gain'],
                    'sequence':5
                   }
                salaire_brute += hs['gain']          
                bulletin_line_obj.create(cr, uid, line_hs)
            
        #--------------rubriques-------------------------------------------------
        query = '''
        SELECT l.montant, r.name,r.categorie,r.type,r.regime, r.afficher,r.sequence,r.imposable,r.cotisable,r.absence
        FROM hr_payroll_ligne_rubrique l
        LEFT JOIN hr_payroll_rubrique r on (l.rubrique_id=r.id)
        WHERE 
        (l.id_contract=%s and l.permanent=True) OR 
        (l.id_contract=%s and l.date_start <= '%s' and l.date_stop >= '%s')
        order by r.sequence
        ''' % (bulletin.employee_contract_id.id, bulletin.employee_contract_id.id, bulletin.id_payroll.period_id.date_start, bulletin.id_payroll.period_id.date_stop)
        
        cr.execute(query)
        rubriques = cr.dictfetchall()
        #--------------rubriques  majoration -------------------------------------------------
        for rubrique in rubriques :
            if(rubrique['categorie'] == 'majoration'):
                
                regime_rubrique = rubrique['regime']
                taux = bulletin.pointage
                montant = rubrique['montant']
                if regime_contact in ('journalier', 'mensuel') :
                    if regime_rubrique == 'mensuel' :
                        if rubrique['absence'] :
                            taux = bulletin.pointage  / nb_jour
                            base_conge_rubriques +=montant/nb_jour
                        else :
                            taux = 1
#                             nb_imp_days_holiday=bulletin.pointage_line_id.nb_imp_days_holiday 
#                             taux = (nb_jour - nb_imp_days_holiday) / nb_jour
                    elif regime_rubrique == 'journalier' :
                        taux = bulletin.pointage 
                    else :
                        taux = bulletin.pointage * 8.0
                else :  # regime_contact = horaire
                    if regime_rubrique == 'mensuel' :
                        taux = bulletin.pointage * (1.0 / nb_jour / 8.0)
                        taux = round(taux, self.pool.get('decimal.precision').precision_get(cr, uid, 'Montant Paie'))  
                    elif regime_rubrique == 'journalier' :
                        taux = bulletin.pointage * float(1.0 / 8.0)
                        taux = round(taux, self.pool.get('decimal.precision').precision_get(cr, uid, 'Montant Paie'))  
                    else :
                        taux = bulletin.pointage * 1.0
               
                gain = montant* taux 
                
                
                if not rubrique['cotisable']:
                    exoneration_cotisable+= gain 
                

                #Documeny utilisé : docs/calcul_cnss_irpp.ods
                if not rubrique['imposable']:
                    # salaire_brute_imposable += montant 
                    if rubrique['cotisable'] :
                        exoneration_irpp += (gain*(1-0.0918))#TODO: get taux from params
                        
                    else :
                        exoneration_irpp += gain
              
                mnt_rubriques += gain
                
                if rubrique['type'] == 'prime':
                        prime += gain
                        print '**prime*',prime 
                elif rubrique['type'] == 'indemnite':
                        indemnite += gain
                elif rubrique['type'] == 'avantage':
                        avantage += gain
                        print '**avantage*',avantage 
                
                        
                majoration_line = {
                                'name' : rubrique['name'],
                                'id_bulletin' : id_bulletin,
                                'type' : 'brute',
                                'base' : montant,
                                'taux' : taux ,
                                'gain':gain,
                                'afficher' : rubrique['afficher'],
                                'sequence':7
                                }
                bulletin_line_obj.create(cr, uid, majoration_line)
        #salaire_brute += prime + indemnite + avantage
        salaire_brute += mnt_rubriques
         
        #create line salaire brute info
        #--------------total congé ------------------------- 
        nb_days_holiday=bulletin.pointage_line_id.nb_days_holiday 
        if nb_days_holiday != 0 :
                conge_pay_line_t = {
                        'name' : _(u'Congés payés'),
                        'id_bulletin' : id_bulletin,
                        'type' : 'brute',
                        'base' :  base_conge_rubriques+base,
                        'taux' : nb_days_holiday ,
                        'gain':  nb_days_holiday*(base_conge_rubriques+base) ,
                        'sequence':3
                       }
                salaire_brute +=nb_days_holiday * (base_conge_rubriques+base)
                mnt_conge_paye +=nb_days_holiday * (base_conge_rubriques+base)
                mnt_conge_rubriques_paye +=nb_days_holiday*base_conge_rubriques
                print '**mnt_conge_rubriques_paye**',mnt_conge_rubriques_paye
                bulletin_line_obj.create(cr, uid, conge_pay_line_t) 
        
        salaire_brute_line = {
                    'name' : _('Salaire brut'),
                    'id_bulletin' : id_bulletin,
                    'type' : 'info',
                    'base' :  False ,
                    'taux' :  False  ,
                    'gain':  salaire_brute,
                    'retenu':0.0,
                    'sequence':8
                   }  
        bulletin_line_obj.create(cr, uid, salaire_brute_line)      
        salaire_brute_cotisable =  salaire_brute  - exoneration_cotisable  
        
  

        
        #--------------cotisations-------------------------
        res_cotisations,cotisations_employee,cotisations_employer = self.get_cotisations(cr, uid, bulletin.employee_id.id, salaire_brute_cotisable )
        for cot in res_cotisations:
            if cot['retenu']:
                cotisation_line = {
                                'name' : cot['name'],
                                'id_bulletin' : id_bulletin,
                                'type' : 'cotisation',
                                'base' : cot['base'],
                                'taux' : cot['taux'],
                                'rate_employer' : cot['rate_employer'],
                                'gain':0.0,
                                'retenu':cot['retenu'],
                                'subtotal_employer':cot['subtotal_employer'],
                                'sequence':9
                                } 
                bulletin_line_obj.create(cr, uid, cotisation_line)
        salaire_brute_imposable = salaire_brute - exoneration_irpp-cotisations_employee   
        #create line salaire_brute_imposable : info 
#         if bulletin.employee_id.specific:
#             salaire_brute_imposable = bulletin.employee_id.salaire_brute_imposable

#         if bulletin.employee_id.assurance:
#             salaire_brute_imposable = salaire_brute_imposable - (bulletin.employee_id.amount_assurance / 12)
            
        salaire_brute_imposable_line = {
                    'name' : _('Salaire brut imposable'),
                    'id_bulletin' : id_bulletin,
                    'type' : 'info',
                    'base' :  False ,
                    'taux' :  False  ,
                    'gain':  salaire_brute_imposable,
                    'retenu':False,
                    'sequence':10
                   }  
        bulletin_line_obj.create(cr, uid, salaire_brute_imposable_line)            
        #--------------irpp-------------------------------------------------------
        if bulletin.employee_id.irpp :
            mnt_Impot = self.get_irpp(cr, uid, bulletin.employee_id.id, salaire_brute_imposable )
            ir_line = {
                    #'name' : _('Impot sur le revenu'),
                    'name' : _('IRPP'),
                    'id_bulletin' : id_bulletin,
                    'type' : 'ir',
                    'base' : salaire_brute_imposable,
                    'taux' : 0.0,
                    'retenu' : mnt_Impot,
                    'sequence':11
                    }
            bulletin_line_obj.create(cr, uid, ir_line)
            
        salaire_net = salaire_brute -mnt_Impot - cotisations_employee
        
        #--------------redevance de compensation--------------------------------
#         salaire_net_annuel=salaire_net*12.0
#         if salaire_net_annuel >=  params['redevance_from'] :
#             mnt_redevance=salaire_net * params['redevance_taux'] / 100.0
#             redevance_line = {
#                         'name' : _(u'Redevance de compensation'),
#                         'id_bulletin' : id_bulletin,
#                         'type' : 'redevance',
#                         'base' : salaire_net,
#                         'taux' : 1,
#                         'retenu':mnt_redevance,
#                         'gain':0.0,
#                         'afficher' : True,
#                         'sequence':13
#                          }
#             bulletin_line_obj.create(cr, uid, redevance_line)
#         salaire_net -= mnt_redevance
               
        #--------------deduction------------------------------------------------
        for rubrique in rubriques :
            if(rubrique['categorie'] == 'deduction'):
                    deduction += rubrique['montant']
                    deduction_line = {
                        'name' : rubrique['name'],
                        'id_bulletin' : id_bulletin,
                        'type' : 'retenu',
                        'base' : rubrique['montant'],
                        'taux' : 100,
                        'retenu':rubrique['montant'],
                        'gain':0.0,
                        'afficher' : rubrique['afficher'],
                        'sequence':15
                         }
                    bulletin_line_obj.create(cr, uid, deduction_line)
          
        #------------- pret     -------------  
        prets = self.get_prets(cr, uid, bulletin.pointage_line_id)
        if prets :
            for pret in prets :
                deduction += pret['montant']
                loan_amount += pret['montant']
                pret_line = {
                    'name' : pret['name'],
                    'id_bulletin' : id_bulletin,
                    'type' : 'retenu',
                    'base' : pret['montant'],
                    'taux' :  '',
                    'unite_rate_employee' :  ' ',
                    'gain':0.0,
                    'retenu':pret['montant'],
                    'afficher' : True,
                    'sequence':17
                     }                 
                bulletin_line_obj.create(cr, uid, pret_line)
        salaire_net_a_payer = salaire_net - deduction
       
        #create line salaire_net_a_payer : info 
        salaire_net_a_payer_line = {
                    'name' : _(u'Salaire net à payer'),
                    'id_bulletin' : id_bulletin,
                    'type' : 'info',
                    'base' :  False ,
                    'taux' :  False  ,
                    'gain':  salaire_net_a_payer,
                    'retenu':False,
                    'sequence':20
                   }  
        bulletin_line_obj.create(cr, uid, salaire_net_a_payer_line)
            
        #--------Montant text : salaire_net_a_payer --------------------
        convertion = self.pool.get('hr.convertion').browse(cr, uid, uid, context=context) 
        salaire_net_a_payer=round(salaire_net_a_payer, self.pool.get('decimal.precision').precision_get(cr, uid, 'Montant Paie'))
        print'****salaire_net_a_payer***',salaire_net_a_payer
        montant_text =  convertion.trad(salaire_net_a_payer, 'Dinar', 'Millime') 
               
        #--------------save  bulletin---------------------------------------------------
        self.write(cr, uid, [bulletin.id], {   
                                            
                                               'salaire_brute' : salaire_brute,
                                               'salaire_base_brut':salaire_base_brut,
                                               'salaire_brute_cotisable':salaire_brute_cotisable,
                                               'salaire_brute_imposable':salaire_brute_imposable,
                                               'salaire_net':salaire_net,
                                               'salaire_net_a_payer':salaire_net_a_payer,
                                               'montant_text':montant_text,
                                               'cotisations_employee':cotisations_employee,
                                               'cotisations_employer':cotisations_employer,
                                               'igr':mnt_Impot,
                                               'prime':prime,
                                               'indemnite':indemnite,
                                               'avantage':avantage,
                                               'mnt_redevance':mnt_redevance,
                                               'mnt_conge_paye':mnt_conge_paye,
                                               'mnt_conge_rubriques_paye':mnt_conge_rubriques_paye,
                                               'deduction':deduction,
                                               'loan_amount':loan_amount,
                                               'exoneration':exoneration_irpp,
                                               'frais_pro': params['fraispro'],
                                               'nb_jours_cp_pris':nb_jours_cp_pris,
                                               'nb_jours_cp_solde':nb_jours_cp_solde,
                                               
                                                }) 
        



        
        return True
    
        

#     def unlink(self, cr, uid, ids, context=None):
#         bulletins_mensuelles = self.read(cr, uid, ids, ['state'], context=context)
#         unlink_ids = []
#         for s in bulletins_mensuelles:
#             if s['state'] in ['draft', 'cancelled']:
#                 unlink_ids.append(s['id'])
#             else:
#                 raise osv.except_osv(_('Action non valide  !'), _('Vous ne pouvez pas supprimer les bulletins de paie confirmés !'))
#         return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)




hr_payroll_bulletin()
 

#===============================================================================
# hr_payroll_bulletin_line
#===============================================================================
class hr_payroll_bulletin_line(osv.osv):
    _name = "hr.payroll.bulletin.line"
    _description = "ligne de salaire"
    _order = 'id,sequence' 
    _columns = {
        'name': fields.char('Description', size=256, required=True),
        'id_bulletin': fields.many2one('hr.payroll.bulletin', 'Ref Salaire', ondelete='cascade', select=True),
        'type': fields.char('Type', size=64,),
        'credit_account_id': fields.many2one('account.account', 'Credit account', domain=[('type', '<>', 'view'), ('type', '<>', 'closed')]),
        'debit_account_id': fields.many2one('account.account', 'Debit account', domain=[('type', '<>', 'view'), ('type', '<>', 'closed')]),
        'base': fields.float('Base', required=True, digits_compute=dp.get_precision('Montant Paie')),
        'gain': fields.float('Gain', digits_compute=dp.get_precision('Montant Paie')),
        'retenu': fields.float('Retenu', digits_compute=dp.get_precision('Montant Paie')),
        'subtotal_employer': fields.float('Montant Employeur', digits_compute=dp.get_precision('Montant Paie')),
        'taux' : fields.float('Taux',digits_compute=dp.get_precision('Taux Paie')),
        'rate_employer' : fields.float('Taux Employeur',digits_compute=dp.get_precision('Taux Paie')),
        'note': fields.text('Notes'),
        'afficher' : fields.boolean('Afficher'),
        'sequence': fields.integer(u'Séquence') 
        
    }
    _defaults = {
        'afficher': lambda *a: True,
        'retenu' :0.0,
        'sequence':5
        
    }
    

hr_payroll_bulletin_line()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
