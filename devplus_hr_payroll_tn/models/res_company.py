# -*- coding: utf-8 -*-


from openerp.osv import fields, osv
from openerp.tools.translate import _

class res_company(osv.osv):
    _inherit = "res.company"
    _columns = {
                'cnss' : fields.char ('CNSS', size =11),
                'code_exploitation': fields.char(u"Code d'exploiation" , size=4),
                
                
                }
res_company()    