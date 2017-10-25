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
from openerp import fields, models, api


class report_certif_four(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
            super(report_certif_four, self).__init__(
                cr, uid, name, context=context)
            self.localcontext.update({
                'time': time,
            })


class declaration_four_report(osv.AbstractModel):
    _name = 'report.certif_retenue.certif_retenue_four_report'
    _inherit = 'report.abstract_report'
    _template = 'certif_retenue.certif_retenue_four_report'
    _wrapped_report_class = report_certif_four
