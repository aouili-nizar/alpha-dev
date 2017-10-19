# -*- coding: utf-8 -*-

from openerp.osv import fields,osv

class partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {

            'property_account_payable':fields.many2one('account.account',required=False),
            'property_account_receivable':fields.many2one('account.account',required=False),






    }
partner()
