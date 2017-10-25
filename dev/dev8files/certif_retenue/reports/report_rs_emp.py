# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#
#    Copyright (C) 2017  .
#    Coded by : Aouili Nizar & Mbarek sabrine
#
#----------------------------------------------------------------------------
from openerp.report import report_sxw
import time
from openerp.osv import osv
from openerp import fields,models,api


class report_certif_emp(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
            super(report_certif_emp, self).__init__(
                cr, uid, name, context=context)
            self.localcontext.update({
            'time': time,
            'worked_period':self.get_worked,
            'sum_brut_imp':self.sum_brut_imp,
            'sum_brut':self.sum_brut,
            'sum_irpp':self.sum_irpp,
            'sum_net':self.sum_net,
        })

    def sum_brut_imp(self, fiscalyear_id, emp_id, context=None):
        obj = self.pool.get('hr.payroll.bulletin')
        search_ids = obj.search(self.cr, self.uid, [('period_id.fiscalyear_id', '=', fiscalyear_id), ('employee_id.name', '=', emp_id)], context)
        i = 0
        print(search_ids)
        for x in obj.browse(self.cr, self.uid, search_ids):
            i = x.salaire_brute_imposable 
        return i *12
    def sum_brut(self, fiscalyear_id, emp_id, context=None):
        obj = self.pool.get('hr.payroll.bulletin')
        search_ids = obj.search(self.cr, self.uid, [('period_id.fiscalyear_id', '=', fiscalyear_id), ('employee_id.name', '=', emp_id)], context)
        i = 0
        print(search_ids)
        for x in obj.browse(self.cr, self.uid, search_ids):
            i = x.salaire_brute
        return i *12
    def sum_irpp(self, fiscalyear_id, emp_id, context=None):
        obj = self.pool.get('hr.payroll.bulletin')
        search_ids = obj.search(self.cr, self.uid, [('period_id.fiscalyear_id', '=', fiscalyear_id), ('employee_id.name', '=', emp_id)], context)
        i = 0
        print(search_ids)
        for x in obj.browse(self.cr, self.uid, search_ids):
            i = x.igr
        return i *12
    def sum_net(self, fiscalyear_id, emp_id, context=None):
        obj = self.pool.get('hr.payroll.bulletin')
        search_ids = obj.search(self.cr, self.uid, [('period_id.fiscalyear_id', '=', fiscalyear_id),('employee_id.name','=',emp_id)], context)
        i = 0
        print(search_ids)
        for x in obj.browse(self.cr, self.uid, search_ids):
            i = x.salaire_net
        return i *12
    def get_worked(self, fiscalyear_id,emp_id, context=None):
        obj = self.pool.get('hr.payroll.bulletin')
        search_ids = obj.search(self.cr, self.uid, [('period_id.fiscalyear_id', '=', fiscalyear_id),('employee_id.name','=',emp_id)], context)
        i = 0
        print(search_ids)
        for x in obj.browse(self.cr, self.uid, search_ids):
            i = i+1
        return i
class declaration_employer_report(osv.AbstractModel):
    _name = 'report.certif_retenue.certif_retenue_report'
    _inherit = 'report.abstract_report'
    _template = 'certif_retenue.certif_retenue_report'
    _wrapped_report_class = report_certif_emp
