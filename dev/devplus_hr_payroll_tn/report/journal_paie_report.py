# -*- coding: utf-8 -*-


from openerp.report import report_sxw
import time
from openerp.osv import osv


class journal_paie_report(report_sxw.rml_parse):
    _name = 'report.journal.paie'
    
    def __init__(self, cr, uid, name, context):
        super(journal_paie_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'get_journal' : self.get_journal,
            'get_total' : self.get_total,
        })
        
        #--------------rubriques-------------------------------------------------
#         query = '''
#         SELECT l.montant, r.name,r.categorie,r.type,r.regime, r.afficher,r.sequence,r.imposable,r.cotisable,r.absence
#         FROM hr_payroll_ligne_rubrique l
#         LEFT JOIN hr_payroll_rubrique r on (l.rubrique_id=r.id)
#         WHERE 
#         (l.id_contract=%s and l.permanent=True) OR 
#         (l.id_contract=%s and l.date_start <= '%s' and l.date_stop >= '%s')
#         order by r.sequence
#         ''' % (bulletin.employee_contract_id.id, bulletin.employee_contract_id.id, bulletin.id_payroll.period_id.date_start, bulletin.id_payroll.period_id.date_stop)
#         
#         cr.execute(query)
#         rubriques = cr.dictfetchall()
        
    def get_journal(self, month_id, company_id):
        #TODO: ajouter le pointage dans le journal 
        sql = '''
          SELECT e.matricule ,e.name_related as e_name_related,r.name,b.salaire_base,b.salaire_brute,
        b.cotisations_employee,b.cotisations_employer,    
        b.salaire_brute_cotisable,
        b.salaire_net,b.salaire_brute_imposable,b.salaire_brute_cotisable,
        b.igr,
        b.indemnite,b.avantage,b.exoneration,b.deduction,        
       
        b.prime,
        b.salaire_net_a_payer,
            b.frais_pro,
        e.identification_id,e.birthday,
            b.employee_contract_id as contract
        
        FROM hr_payroll_bulletin b
        
        LEFT JOIN hr_contract c on (b.employee_contract_id=c.id)
        LEFT JOIN hr_employee e on (b.employee_id=e.id)
        LEFT JOIN hr_contract_regime r on (c.regime_id=r.id)
        WHERE
        (b.month_id=%s )  
        ''' % (month_id[0])
        #TODO: ajouter le test su r ((select count(*) from hr_pointage_line pl where  pl.employee_id=e.id and >0)     
        self.cr.execute(sql)
        res = self.cr.dictfetchall()
        return res
    
    def get_total(self, month_id):

        salaire_base = 0
        salaire_brute = 0
        salaire_brute_imposable = 0
        salaire_brute_cotisable = 0
        salaire_net_a_payer = 0
        cotisations_employee = 0
        cotisations_employer = 0
        # avantage en nature pour ticket repas 
        avantage_nature =0
        igr = 0
        salaire_net = 0
        prime = 0
        indemnite = 0
        avantage = 0
        exoneration = 0
        deduction = 0
        normal_hours = 0
        prime_anciennete = 0
        working_unite = 0
        frais_pro = 0
        personnes = 0
        absence = 0
        bulletins = self.pool.get('hr.payroll.bulletin')
        # bulletins_ids=bulletins.search(self.cr,self.uid,[('period_id','=',int(period_id))])
        bulletins_ids = bulletins.search(self.cr, self.uid, [('month_id', '=', month_id[0])])
        liste = bulletins.read(self.cr, self.uid, bulletins_ids, [])
        for b in liste:
            salaire_base += b['salaire_base']
            salaire_brute += b['salaire_brute']
            salaire_brute_imposable += b['salaire_brute_imposable']
            salaire_brute_cotisable += b['salaire_brute_cotisable']
            avantage_nature +=(b['salaire_brute']-b['salaire_brute_cotisable'])
            salaire_net_a_payer += b['salaire_net_a_payer']
            cotisations_employee += b['cotisations_employee']
            cotisations_employer += b['cotisations_employer']
            salaire_net += b['salaire_net']
            
            igr += b['igr']
            prime += b['prime']
            indemnite += b['indemnite']
            avantage += b['avantage']
            exoneration += b['exoneration']
            deduction += b['deduction']
            normal_hours += 0  # b['normal_hours']
            prime_anciennete += 0  # b['prime_anciennete']
            working_unite += 0  # b['working_unite']
            frais_pro += b['frais_pro']
            personnes += 0  # b['personnes']
            absence += 0  # b['absence']
            
        liste = []
        total_line = {
            'salaire_base':salaire_base,
            'salaire_brute':salaire_brute,
            'salaire_brute_imposable':salaire_brute_imposable,
            'salaire_brute_cotisable':salaire_brute_cotisable,
            'avantage_nature':avantage_nature,
            'salaire_net_a_payer':salaire_net_a_payer,
            'cotisations_employee':cotisations_employee,
            'cotisations_employer':cotisations_employer,
            'salaire_net' : salaire_net,
            'igr':igr,
            'prime':prime,
            'indemnite':indemnite,
            'avantage':avantage,
            'exoneration':exoneration,
            'deduction':deduction,
            'normal_hours':normal_hours,
            'prime_anciennete':prime_anciennete,
            'working_unite':working_unite,
            'frais_pro':frais_pro,
            'personnes':personnes,
            'absence':absence,
            }
        liste.append(total_line)
        return liste
    
    
    
class report_journal_paie(osv.AbstractModel):
    _name = 'report.devplus_hr_payroll_tn.report_journal_paie'
    _inherit = 'report.abstract_report'
    _template = 'devplus_hr_payroll_tn.report_journal_paie'
    _wrapped_report_class = journal_paie_report  