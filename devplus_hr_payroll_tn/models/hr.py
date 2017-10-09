# -*- coding: utf-8 -*-
import datetime
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from datetime import date, datetime
from datetime import datetime, timedelta

class hr_employee(osv.osv):
    _inherit = 'hr.employee'
    _order = 'matricule'

    def _check_length_cin(self, cr, uid, ids, context=None):
        record = self.browse(cr, uid, ids, context=context)
        for data in record:
            if data.cin and  (len(data.cin) != 8):
                return False
            return True

    def _action_count_autorisation(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for employee in self.browse(cr,uid,ids):
            result[employee.id] = len(employee.autorisation_ids)
        return result


    _columns = {
        'matricule' : fields.char('Matricule', size=64, select=True,required=True),
        'cnss' : fields.char('CNSS', size=11),
        'cnrps' : fields.char('CNRPS', size=10),
        'cin' : fields.char('CIN', size=8,required=True ),
        'date_entree': fields.date(u'Date  entrée'),
        'date_avancement': fields.date('Date avancement'),
        'nb_parents' : fields.integer(u'Nombre parents à charge'),
        'nb_enfant_etudiant' : fields.integer(u'Nombre enfants étudiants'),
        'nb_enfant_handicape' : fields.integer(u'Nombre enfants handicapés'),
        'chef_famille': fields.boolean('Chef de famille'),
        'mode_reglement' : fields.selection([('virement', 'Virement'), ('cheque', u'Chèque'), ('espece', u'Espèce'), ], u'Mode de règlement'),
        'address_home' : fields.char('Adresse Personnelle', size=128),
        'address' : fields.char('Adresse Professionnelle', size=128),
        'res_bank_id': fields.many2one('res.bank', 'Banque'),
        'numero_compte' : fields.char(u'Numéro de compte', size=64,),
        'marital': fields.selection([('c', u'Célibataire'), ('m', u'Marié'), ('v', 'Veuf'), ('d', u'Divorcé')], 'Situation familiale'),
        'irpp': fields.boolean(u'IRPP ?'),
        'avance': fields.boolean('Autoriser une avance sur salaire'),
        'action_count_autorisation': fields.function(_action_count_autorisation, type='float', string="Nombre d'autorisation"),
        'autorisation_ids':fields.one2many('hr.autorisation', 'employee_id', 'Autorisations'),
        'numero_compte' :fields.char('Numéro de compte',size=20),
        'specific': fields.boolean(u'Cas particulier'),
        'salaire_brute_imposable':fields.float('Salaire brute imposable',  digits_compute=dp.get_precision('Montant Paie')),
        'amount_logement':fields.float("Contribution à l'avancement des fonds de logement",  digits_compute=dp.get_precision('Montant Paie')),
        'create_move' : fields.boolean(u'Créer une écriture comptable'),
#         'mat_cnss':fields.char('Matricule CNSS', size=64, select=True,required=True),
#         'num_chezemployeur':fields.char('Numero chez l\'employeur'),
#         'cin':fields.char('CIN', size=8,required=True ),
       'cnss5' : fields.boolean(u'Cnss'),
       'last_remaining_leaves':fields.float("Solde congé de l'année précedent "),
       'right_leaves':fields.float("Droit de congé"),
       'address_personnel': fields.text('Adresse personnelle'),
        'assurance': fields.boolean(u'Assurance vie'),
        'amount_assurance':fields.float("Montant assurance", digits_compute=dp.get_precision('Montant Paie')),
        'categ_professionnelle':fields.char('Categ Professionnelle'),


    }

    def action_confirmed(self,cr,uid,ids,context=None):

        obj=self.browse(cr, uid, ids)
        right_leaves=obj.right_leaves
        remaining_leaves=obj.remaining_leaves
        return  self.write(cr,uid,ids,{'remaining_leaves':remaining_leaves + right_leaves},context=context)

    def onchange_right_leave(self,cr,uid,ids,right_leaves,last_remaining_leaves, context= None):

        date_now=datetime.now()
        print '******',date_now
        diff_day = date_now.day
        print '***diff_day****',diff_day

        convertion = self.pool.get('hr.convertion').browse(cr, uid, uid, context=context)
        #montant_text =  convertion.trad(salaire_net_a_payer, 'Dinar', 'Millime')
        print 1020.00, convertion.trad(1020.00, 'Dinar', 'Millime')

  #      if right_leaves and (diff_day==1):
        if right_leaves  :
                result = {'value': {
                             'last_remaining_leaves' : last_remaining_leaves + right_leaves,
                         }
                     }
                print "***result****",result
                return result


    _defaults = {
            'date_entree' : lambda * a: time.strftime('%Y-%m-%d'),
            'cnss':'0000000000',
             'irpp':True ,
             'create_move':True,
             'cnss5' : True
    }
    _sql_constraints = [
        ('cin_uniq', 'unique (cin)', ' cin doit etre  unique !'),
    ]

    _constraints = [(_check_length_cin, u'Erreur: Le CIN doit être composé de huit chiffres', ['cin'])]



    _sql_constraints = [
         ('matricule_employee_uniq', 'UNIQUE(matricule)', u'Matricule existe déjà !')
     ]



    def _get_nb_days_cp_by_period(self, cr, uid, employee_id, period_id, context=None):
        period_obj = self.pool.get('account.period')
        period = period_obj.browse(cr, uid, period_id, context=context)
        date_start = period.date_start
        date_stop = period.date_stop

#         holidays_obj = self.pool.get('hr.holidays')
#         ids = holidays_obj.search(cr, uid, [])
#         date_from = holidays_obj.browse(cr,uid,ids[0],context=context)
#         date_to = holidays_obj.browse(cr,uid,ids[0],context=context)
#         DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
#         from_dt = datetime.strptime(date_from, DATETIME_FORMAT)
#         to_dt = datetime.strptime(date_to, DATETIME_FORMAT)
#         #d=datetime.strptime
#         timedelta = to_dt - from_dt
#         diff_day = timedelta.days + float(timedelta.seconds) / 86400
#         print'**diff_day***##',diff_day
        # get nb congé payé par periode h.number_of_days  as days,
        cr.execute("""SELECT
                h.id,
                h.employee_id,
                h.number_of_days_temp
            from
                hr_holidays h
                join hr_holidays_status s on (s.id=h.holiday_status_id)
            where
                h.state='validate' and
                s.payed=True and
                h.employee_id = %s and
                h.date_from  >    '%s' and
                h.date_from  <    '%s'
             """ % (employee_id, date_start, date_stop))
        res = cr.dictfetchall()
        days = 0

        for r in res :
            days= days+ (r['number_of_days_temp'] or 0)
        return days
    def _get_nb_days_c_impaye_by_period(self, cr, uid, employee_id, period_id, context=None):
        period_obj = self.pool.get('account.period')
        period = period_obj.browse(cr, uid, period_id, context=context)
        date_start = period.date_start
        date_stop = period.date_stop
        # get nb congé payé par periode h.number_of_days  as days,
        cr.execute("""SELECT
                h.id,
                h.employee_id,
                h.number_of_days_temp
            from
                hr_holidays h
                join hr_holidays_status s on (s.id=h.holiday_status_id)
            where
                h.state='validate' and
                s.payed=False and
                h.employee_id = %s and
                h.date_from  >    '%s' and
                h.date_from  <    '%s'
             """ % (employee_id, date_start, date_stop))
        res = cr.dictfetchall()
        days = 0
        for r in res :
            days= days+ (r['number_of_days_temp'] or 0)
        return days

    def _get_total_days_conge_paye_attribue(self, cr, uid, employee_id, context=None):
        cr.execute("""SELECT
                  sum(h.number_of_days) as days,
                h.employee_id
            from
                hr_holidays h
                join hr_holidays_status s on (s.id=h.holiday_status_id)
            where
                h.state='validate' and
                 h.type = 'add' and
                s.payed=True and
                h.employee_id = %s
                group by h.employee_id
             """ % (employee_id))
        res = cr.dictfetchall()

        return abs((res and res[0]['days'])  or 0)

    def _get_total_days_conge_pris(self, cr, uid, employee_id, context=None):
        cr.execute("""SELECT
                  sum(h.number_of_days) as days,
                h.employee_id
            from
                hr_holidays h
                join hr_holidays_status s on (s.id=h.holiday_status_id)
            where
                h.state='validate' and
                 h.type = 'remove' and
                s.payed=True and
                h.employee_id = %s
                group by h.employee_id
             """ % (employee_id))
        res = cr.dictfetchall()
        return abs((res and res[0]['days'])  or 0)

    def _get_total_days_restante(self, cr, uid, employee_id, context=None):
        days_all = self._get_total_days_conge_paye_attribue(cr, uid, employee_id, context=context)
        pris = self._get_total_days_conge_pris(cr, uid, employee_id, context=context)
        return (days_all - pris)

hr_employee()



#===============================================================================
# hr_contract_type
#===============================================================================
class hr_contract_type(osv.osv):
    _inherit = 'hr.contract.type'
    _columns = {
                'irpp': fields.boolean(u"Calculer l'impôt?"),
                'cotisation':fields.many2one('hr.payroll.cotisation.type', 'Type cotisations', required=True),
                }

#===============================================================================
# hr_contract_regime
#===============================================================================
class hr_contract_regime(osv.osv):
    _name ='hr.contract.regime'

    _columns={
              'name':fields.char('Nom'),
              'type_regime' : fields.selection([('horaire', 'Horaire'),
                                                  ('mensuel', 'Mensuel') ], u'Régime', required=True),
              'hours_horaire':fields.integer(u"Nombre d'heure"),
              'hours_mensuel':fields.selection([('40','40 H'), ('48','48 H')], u"Nombre d'heure"),

              }


class hr_contract(osv.osv):
    _inherit= "hr.contract"
    _description ="employee contract"


    _columns ={
               'cotisation':fields.many2one('hr.payroll.cotisation.type', 'Type cotisations'),
               'rubrique_ids': fields.one2many('hr.payroll.ligne_rubrique', 'id_contract', 'Les rubriques'),
               'type_id': fields.many2one('hr.contract.type', "Contract Type", required=True),
               'num': fields.char(u'Numéro'),
               'wage': fields.float('Wage', digits_compute=dp.get_precision('Montant Paie'), required=True),
               'salaire_net': fields.float('Salaire Net', digits_compute=dp.get_precision('Montant Paie')),
               'regime_id': fields.many2one('hr.contract.regime', u"Régime", required=True),
               }



    def create(self, cr, uid, vals, context=None):
        if not vals.get('num', False):
            vals['num'] = self.pool.get('ir.sequence').get(cr, uid, 'hr.contract', context=context) or '/'
        return super(hr_contract, self).create(cr, uid, vals, context=context)
    def net_to_brute(self, cr, uid, ids, context={}):
        '''
        Calculer Brut  apartir du Net
        :param cr:
        :param uid:
        :param ids:
        :param context:
        '''
        contract = self.browse(cr, uid, ids[0])
        #if field   irpp  in contract is false retrun salaire net
        if  contract.type_id and  not contract.type_id.irpp:
            self.write(cr, uid, [contract.id], {'wage' :contract.salaire_net })
            return True

        bulletin_obj=self.pool.get('hr.payroll.bulletin')
        salaire_base = contract.salaire_net
        cotisation = contract.type_id.cotisation
        base = 0
        salaire_brute = salaire_base
        trouve=False
        trouve2=False
        while(trouve == False):
            salaire_brute_imposable=0
            cotisations_employee=0
            for cot in cotisation.cotisation_ids :
                base = salaire_brute
                cotisations_employee += base * cot['tauxsalarial'] / 100
            salaire_brute_imposable = salaire_brute - cotisations_employee
            mnt_Impot=bulletin_obj.get_irpp(cr, uid, contract.employee_id.id, salaire_brute_imposable)
            if(mnt_Impot < 0):mnt_Impot = 0
            salaire_net=salaire_brute - cotisations_employee - mnt_Impot
            if(int(salaire_net)==int(salaire_base) and trouve2==False):
                trouve2=True
                salaire_brute-=1
            if not trouve2:
                if salaire_base- round(salaire_net,3) > 1000 : salaire_brute +=999
                elif salaire_base-round(salaire_net,3) > 500 : salaire_brute +=499
                elif salaire_base-round(salaire_net,3) > 200 : salaire_brute +=199
                elif salaire_base-round(salaire_net,3) > 100 : salaire_brute +=99
                elif salaire_base-round(salaire_net,3) > 10 : salaire_brute +=9
            if(round(salaire_net,3)==salaire_base):trouve=True
            elif trouve2==False : salaire_brute+=0.9
            elif trouve2==True :
                if salaire_base- round(salaire_net,3) > 0.5 : salaire_brute +=0.5
                elif salaire_base- round(salaire_net,3) > 0.1 : salaire_brute +=0.1
                elif salaire_base- round(salaire_net,3) > 0.08 : salaire_brute +=0.08
                elif salaire_base- round(salaire_net,3) > 0.05 : salaire_brute +=0.05
                elif salaire_base- round(salaire_net,3) > 0.01 : salaire_brute +=0.01
                elif salaire_base- round(salaire_net,3) > 0.005 : salaire_brute +=0.005
                else : salaire_brute+=0.001
        self.write(cr, uid, [contract.id], {'wage' :salaire_brute })
        return True

hr_contract()

#===============================================================================
# hr_holidays_status
#===============================================================================
class hr_holidays_status(osv.osv):
    _inherit="hr.holidays.status"
    _description="Holidays"

    _columns={
              'payed':fields.boolean(u'Payé?')

              }
    _defaults = {
                 'payed': lambda * args: True
                 }
hr_holidays_status()






#===============================================================================
# hr_holidays
#===============================================================================
class hr_holidays(osv.osv):
    _inherit = "hr.holidays"

    _columns = { 'matricule':fields.char('Matricule'),
                'date': fields.date('Date'),
                'description':fields.text('description'),
                'yeaar': fields.char('Année'),
                }


    _defaults = {
                 'date': fields.date.context_today,
                 'yeaar' : datetime.now().year,
                 }
    def onchange_employee(self, cr, uid, ids, employee_id, context=None):
        res = super(hr_holidays, self).onchange_employee(cr, uid, ids, employee_id)
        employee=self.pool.get('hr.employee').browse(cr,uid,employee_id,context)
        res['value'].update({ 'matricule':employee.matricule})
        return res

    def check_holidays(self, cr, uid, ids, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            if record.holiday_type != 'employee' or record.type != 'remove' or not record.employee_id or record.holiday_status_id.limit:
                continue
            leave_days = self.pool.get('hr.holidays.status').get_days(cr, uid, [record.holiday_status_id.id], record.employee_id.id, context=context)[record.holiday_status_id.id]
#             if leave_days['remaining_leaves'] < 0 or leave_days['virtual_remaining_leaves'] < 0:
#                 # Raising a warning gives a more user-friendly feedback than the default constraint error
#                 raise Warning(_('The number of remaining leaves is not sufficient for this leave type.\n'
#                                 'Please verify also the leaves waiting for validation.'))
        return True




hr_holidays()
