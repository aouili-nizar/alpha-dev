# -*- coding: utf-8 -*-


from openerp.osv import fields, osv
from openerp.tools.translate import _

class res_company(osv.osv):
    _inherit = "res.company"


    _columns = {
              'BR':fields.char(u"BR"),

              }
