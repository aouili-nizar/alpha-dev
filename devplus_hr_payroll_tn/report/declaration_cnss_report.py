# -*- coding: utf-8 -*-

from openerp.report import report_sxw
import convertion
from openerp.osv import osv
import datetime
import time
class declaration_cnss_report(report_sxw.rml_parse):
    _name = 'report.declaration.cnss'

    def __init__(self, cr, uid, name, context):
        if context is None:
            context = {}
        super(declaration_cnss_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_page' : self.get_page,
            'get_nb_page':self.get_nb_page,
            'get_nb_employees' : self.get_nb_employees,
            'get_total' : self.get_total,
            'get_total_page':self.get_total_page,
            'get_total_precedante':self.get_total_precedante,
        })

    def _get_lines(self, company_id,fiscalyear_id,trimester):
        period_ids=self.pool.get('account.period').search(self.cr,self.uid,[('fiscalyear_id','=',fiscalyear_id)])
        obj = self.pool.get('account.period')
        # if existe periode ouverture period_ids=13 else period_ids=12
        # if period_ids==12 :
        for per in obj.browse(self.cr,self.uid,period_ids):
            if trimester =='1' :
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==1)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day)):
                    mois1=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==2)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois2=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==3)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois3=per.id
            elif trimester =='2' :
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==4)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day)):
                    mois1=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==5)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois2=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==6)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois3=per.id
            elif trimester =='3' :
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==7)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day)):
                    mois1=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==8)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois2=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==9)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois3=per.id

            else :
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==10)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois1=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==11)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day)):
                    mois2=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==12)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois3=per.id



        sql = '''
               SELECT e.id ,e.matricule,e.cnss,e.categ_professionnelle,SUBSTRING(r.name, 0, 60) as name,e.cin,

             ( select  CASE WHEN b1.cotisations_employee > 0 THEN  b1.salaire_brute_cotisable ELSE 0  END   from hr_payroll_bulletin  b1 where
               b1.period_id = %s and b1.employee_id=e.id
                ) as mois1,

             ( select  CASE WHEN b2.cotisations_employee > 0 THEN  b2.salaire_brute_cotisable ELSE 0  END   from hr_payroll_bulletin  b2 where
               b2.period_id = %s and b2.employee_id=e.id
                ) as mois2,

             ( select  CASE WHEN b3.cotisations_employee > 0 THEN  b3.salaire_brute_cotisable ELSE 0  END   from hr_payroll_bulletin  b3 where
               b3.period_id = %s and b3.employee_id=e.id
                ) as mois3 ,

            (select  sum(CASE WHEN b4.cotisations_employee > 0 THEN  b4.salaire_brute_cotisable ELSE 0  END )  from hr_payroll_bulletin  b4 where
               b4.period_id  in(%s,%s,%s)  and b4.employee_id=e.id) as total

            From  hr_employee e
            LEFT JOIN resource_resource r on (r.id=e.resource_id)
             where r.active=true and e.cnss5 is true
             and ((select count(*) from hr_contract hc where  hc.employee_id=e.id)>0)ORDER BY e.matricule
            ''' % (mois1, mois2, mois3, mois1, mois2, mois3)


        self.cr.execute(sql)
        declaration_cnss = self.cr.dictfetchall()

        num_page=1
        num_line=1
        resultats=[]
        for declaration in declaration_cnss:
            if declaration['total']:
                declaration.update({'num_page':num_page,'num_line':num_line})
                if num_line == 12 :
                    num_page += 1
                    num_line =1
                else :
                    num_line += 1
                resultats.append(declaration)
        return resultats

    def get_page(self, company_id,fiscalyear_id,trimester,num_page):
        all_lines=self._get_lines(company_id,fiscalyear_id,trimester)
        res=[]
        num_line1=0
        id1=1

        for line_cnss in all_lines:
            if line_cnss['num_page'] == num_page :
                res.append(line_cnss)
                num_line1+=1

        if(num_line1<12) :
            while (num_line1<12):
                num_line1 += 1
                id1+=1
                line_vide={'id':id1,'num_line':num_line1,'cnss': '','name':"",'matricule':'','categ_professionnelle':'','mois1':'','mois2':'','mois3':'','total':''}
                res.append(line_vide)
        return res
    def get_total_page(self,company_id,fiscalyear_id,trimester,num_page):
        salaire_brute_cotisable_tot=0
        all_lines=self._get_lines(company_id,fiscalyear_id,trimester)
        res=[]

        liste_tot_page=0
        for line_cnss in all_lines:
            if line_cnss['num_page'] == num_page :
                salaire_brute_cotisable_tot+=line_cnss['total']
        res={
        'salaire_brute_cotisable_tot':salaire_brute_cotisable_tot,
        }
        return res
    def get_total_precedante(self,company_id,fiscalyear_id,trimester,num_page):
        i=1
        liste_tot_page=0
        i=num_page
        liste_tot_page=0
        while(0<i<=num_page):
            num_page=i
            liste_tot_page+=self.get_total_page(company_id,fiscalyear_id,trimester,num_page)['salaire_brute_cotisable_tot']
            i=i-1

        return liste_tot_page

    def get_nb_page(self, company_id,fiscalyear_id,trimester):
        all_lines=self._get_lines(company_id,fiscalyear_id,trimester)
        pages=[]
        for line in all_lines :
            if  pages.count(line['num_page']) ==0 :
                pages.append(line['num_page'])
        return pages


    def get_nb_employees(self, company_id,fiscalyear_id,trimester):
        all_lines=self._get_lines(company_id,fiscalyear_id,trimester)
        return len(all_lines)


    def get_total(self, company_id,fiscalyear_id,trimester):
        all_lines=self._get_lines(company_id,fiscalyear_id,trimester)
        total_mois1=total_mois2=total_mois3=salaire=ztotal_page=0.0
        for line in all_lines :
                total_mois1+=float(line['mois1']or 0.0)
                total_mois2+=float(line['mois2'] or 0.0 )
                total_mois3+=float(line['mois3'] or 0.0)
                salaire+=float(line['total'] or 0.0)


        params_obj= self.pool.get('hr.payroll.parametres')
        ids_params = params_obj.search(self.cr, self.uid, [('fiscalyear_id', '=', fiscalyear_id)])
        param = params_obj.read(self.cr, self.uid, ids_params[0])
        taux_accident_travail='taux_accident_travail' in param.keys() and param['taux_accident_travail']  or 0.5
        taux_cnss=25.75
        montant_accident_travail= salaire * taux_accident_travail/100.0
        montant_cnss= salaire * taux_cnss/100.0
        montant_total =  montant_cnss+montant_accident_travail
        total_page = total_mois1+total_mois2+total_mois3

        res = {
                'total_mois1' :total_mois1,
                'total_mois2' :total_mois2,
                'total_mois3' :total_mois3,
                'total_page' :total_page,
                'salaire' : salaire,
                'taux_cnss':taux_cnss,
                'taux_accident_travail':taux_accident_travail,
                'total_taux' : taux_cnss+taux_accident_travail,
                'montant_cnss' :montant_cnss,
                'montant_accident_travail':montant_accident_travail,
                'montant_total' :montant_total,
                'montant_total_text':convertion.trad(montant_total,'Dinar'),
                'montant_salaire_text':convertion.trad(salaire,'Dinar')
             }

        # print '**res**',res
        return res





class report_declaration_cnss(osv.AbstractModel):
    _name = 'report.devplus_hr_payroll_tn.report_declaration_cnss'
    _inherit = 'report.abstract_report'
    _template = 'devplus_hr_payroll_tn.report_declaration_cnss'
    _wrapped_report_class = declaration_cnss_report

class report_recapitulatif_cnss(osv.AbstractModel):
    _name = 'report.devplus_hr_payroll_tn.report_recapitulatif_cnss'
    _inherit = 'report.abstract_report'
    _template = 'devplus_hr_payroll_tn.report_recapitulatif_cnss'
    _wrapped_report_class = declaration_cnss_report
