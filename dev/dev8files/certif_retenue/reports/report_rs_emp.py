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


class report_certif_emp(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
            super(report_certif_emp, self).__init__(
                cr, uid, name, context=context)
            self.localcontext.update({
            'time': time,
        })

class declaration_employer_report(osv.AbstractModel):
    _name = 'report.certif_retenue.certif_retenue_report'
    _inherit = 'report.abstract_report'
    _template = 'certif_retenue.certif_retenue_report'
    _wrapped_report_class = report_certif_emp
