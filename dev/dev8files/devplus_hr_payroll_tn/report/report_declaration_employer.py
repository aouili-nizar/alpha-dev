# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#
#    Copyright (C) 2017  .
#    Coded by : Mohsen Dhifallah
#
#----------------------------------------------------------------------------
from openerp.report import report_sxw
import time
from openerp.osv import osv


class report_declaration_employer(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
            super(report_declaration_employer, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({
            'time': time,
            'get_declaration_employer':self._get_declaration_employer
          #  'get_foprolos':self._get_foprolos,
        })

#     def _get_declaration_employer(self,fiscalyear_id) :
#         bulletin_obj = self.pool.get('hr.payroll.bulletin')
#         bulletin_ids = bulletin_obj.search(self.cr, self.uid,
#                                            [('month_id.period_id.fiscalyear_id','=',fiscalyear_id)],
#                                       
#                                            )
#         salaire_brute_imposable=0.0
#         total_salaire_brute_imposable=0.0
#    
#         for line in bulletin_obj.browse(self.cr,self.uid,bulletin_ids) :
#             employee_id = line.employee_id.name
#             salaire_brute_imposable += line.salaire_brute_imposable
#             total_salaire_brute_imposable += line.salaire_brute_imposable
#              
#         return { 'employee_id' : employee_id,
#                 'salaire_brute_imposable' : salaire_brute_imposable,
#                 'total_salaire_brute_imposable' : salaire_brute_imposable,
#                          
#               }
           
    def _get_total_salaire_imposable(self,fiscalyear_id,context=None):
        salaire_obj=self.pool.get('hr.payroll.bulletin')
        search_ids=salaire_obj.search(self.cr,self.uid,[('month_id.period_id.fiscalyear_id','=',fiscalyear_id)],context)
        total=0.0
        for line in salaire_obj.browse(self.cr,self.uid,search_ids) :
            total += line.salaire_brute_imposable
        return total      
           
            
    def _get_declaration_employer(self,fiscalyear_id,context=None):
        salaire_obj=self.pool.get('hr.payroll.bulletin')
        search_ids=salaire_obj.search(self.cr,self.uid,[('month_id.period_id.fiscalyear_id','=',fiscalyear_id)],context)
        employees={}
        for sal in salaire_obj.browse(self.cr,self.uid,search_ids) :
            if sal.employee_id.id in employees:
                employees[sal.employee_id.id]['salaire_brute_imposable'] += sal.salaire_brute_imposable
                employees[sal.employee_id.id]['irpp'] += sal.igr
            else :
                val={'employee_id':sal.employee_id.name,'salaire_brute_imposable':sal.salaire_brute_imposable,'irpp':sal.igr}
                employees[sal.employee_id.id] = val
                
        result=[]
        for key, val in employees.items():
            result.append(val)    
              
        
        return result
    
#     def _get_foprolos(self,month_id,context=None):
#         payement_obj=self.pool.get('hr.payroll.bulletin')
#         search_ids=payement_obj.search(self.cr,self.uid,[('month_id', '=', month_id[0])],context)
#         total=0.0
#         for paymnt in payement_obj.browse(self.cr,self.uid,search_ids) :
#             total += paymnt.salaire_brute/100
#         return total

        

    

class declaration_employer_report(osv.AbstractModel):
    _name = 'report.devplus_hr_payroll_tn.declaration_employer_report'
    _inherit = 'report.abstract_report'
    _template = 'devplus_hr_payroll_tn.declaration_employer_report'
    _wrapped_report_class = report_declaration_employer
