# -*- coding: utf-8 -*-

from openerp.osv import fields,osv

class company(osv.osv):
    _inherit = 'res.company'

    _columns = {
            'SAS_capital':fields.char('SAS au capital de'),

    }
company()
