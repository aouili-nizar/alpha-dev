# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

class hr_payroll_parametres(osv.osv):
    _name='hr.payroll.parametres'
    _description = 'Parametres'
    _columns={
             'smig' : fields.float('SMIG', digits_compute=dp.get_precision('Montant Paie')),
             'month_by_year' : fields.float(u'NB Mois/Année'),
             'fraispro' : fields.float(u'Frais Professionnels en %'),
             'taux_accident_travail' : fields.float(u'Accident du travail en %'),
             'parent_charge' : fields.float(u' Taux parent(s) à charge', digits_compute=dp.get_precision('Montant Paie')),
             'chef_famille' : fields.float('Chef de famille', digits_compute=dp.get_precision('Montant Paie')),
             'enfant1' : fields.float(u'Enfant 1 ', digits_compute=dp.get_precision('Montant Paie')),
             'enfant2' : fields.float(u'Enfant 2 ', digits_compute=dp.get_precision('Montant Paie')),
             'enfant3' : fields.float(u'Enfant 3 ', digits_compute=dp.get_precision('Montant Paie')),
             'enfant4' : fields.float(u'Enfant 4 ', digits_compute=dp.get_precision('Montant Paie')),
             'enfant_etudiant' : fields.float(u'Enfant étudiant ', digits_compute=dp.get_precision('Montant Paie')),
             'enfant_handicape' : fields.float(u'Enfant handicapé ', digits_compute=dp.get_precision('Montant Paie')),
             'fiscalyear_id': fields.many2one('account.fiscalyear', u'Année fiscale', required=True),
             #'nb_jour' : fields.float(u' Nombre de jours par mois  '),
             'nb_jour_5j' : fields.float(u'Nombre de jours de travail par mois (régime 5 jours)'),
             'nb_jour_6j' : fields.float(u'Nombre de jours de travail par mois (régime 6 jours)'),
             'auto_droit_conge' : fields.boolean(u'Affecter automatiquement droit des congés payés'),
             'redevance_taux' : fields.float('Taux',),
             'redevance_from' : fields.float(u'Applicables à partir du', digits_compute=dp.get_precision('Montant Paie')),
             'redevance_max' : fields.float(u'Montant maximum', digits_compute=dp.get_precision('Montant Paie')),
             'month_ids':fields.one2many('hr.month','parametre_id',u'Paramétre'),
             'autorisation_delay':fields.float(u"Durée d'autorisation"),
             'company_id': fields.many2one('res.country', u'Pays'),
             }

    _defaults = {
        'nb_jour_5j': 22,
        'nb_jour_6j': 26,
    }
hr_payroll_parametres()



#===============================================================================
# hr_ir
#===============================================================================
class hr_ir(osv.osv):
    _name='hr.payroll.ir'
    _description='IR'
    _columns={

              'debuttranche' : fields.float(u'Début Tranche', digits_compute=dp.get_precision('Montant Paie')),
              'fintranche' : fields.float(u'Fin Tranche', digits_compute=dp.get_precision('Montant Paie')),
              'taux' : fields.float('Taux', digits_compute=dp.get_precision('Montant Paie')),
              'somme' : fields.float('Somme à deduire', digits_compute=dp.get_precision('Montant Paie')),
              }
hr_ir()




#===============================================================================
# hr_cotisation
#===============================================================================
class hr_cotisation(osv.osv):
    _name="hr.payroll.cotisation"
    _description="Les cotisations"

    _columns ={
               'code' : fields.char('Code', size=64, required=True),
               'name' : fields.char(u'Désignation', size=64, required=True),
               'tauxsalarial' : fields.float('Taux Salarial'),
               'tauxpatronal' : fields.float('Taux Patronal'),
               'tauxTotal' : fields.float("Taux Total"),
               'tauxAT' : fields.float("Taux Accident de travail"),
               #'cotisation_id':fields.many2one('hr.payroll.cotisation.type','Types'),

               }


    def onchange_taux(self, cr, uid, ids, tauxsalarial, tauxpatronal, context=None):
        res={}
        tauxTotal=0
        if tauxsalarial and   tauxpatronal:
            print '***Taux Salarial est ***',tauxsalarial, '\n'  ,'***Taux Patronal est :***',tauxpatronal
            tauxTotal=tauxsalarial+tauxpatronal
            print '***somme***',tauxTotal
        res['value']={'tauxTotal':tauxTotal,}

        return res


hr_cotisation()




#===============================================================================
# hr_cotisation_type
#===============================================================================
class hr_cotisation_type(osv.osv):
    _name="hr.payroll.cotisation.type"
    _description = 'Les types de cotisation'
    _columns ={
               'name':fields.char(U'Désignation', required=1),
               'code':fields.char('Code'),
               'cotisation_ids' : fields.many2many('hr.payroll.cotisation', 'salary_cotisation', 'cotisation_id', 'cotisation_type_id', 'Cotisations'),

               }
hr_cotisation_type()
