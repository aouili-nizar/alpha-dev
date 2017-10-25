# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class company(osv.osv):
    _inherit = 'res.company'
    _columns={
		'SARL_capital':fields.char('S.A.R.L au capital de'),
		}
company()
