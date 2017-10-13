# -*- coding: utf-8 -*-


from openerp.osv import fields, osv
from openerp.tools.translate import _

class res_company(osv.osv):
    _inherit = "res.company"

    def _check_length_company_registry(self, cr, uid, ids, context=None):
        record = self.browse(cr, uid, ids, context=context)
        for data in record:
            if data.company_registry and  (len(data.company_registry) != 8):
                return False
            return True
    def _check_length_code_exploitation(self, cr, uid, ids, context=None):
        record = self.browse(cr, uid, ids, context=context)
        for data in record:
            if data.code_exploitation and  (len(data.code_exploitation) != 2):
                return False
            return True

    _columns = {
                'cnss' : fields.char ('CNSS', size =11),
                'code_exploitation': fields.char(u"Code d'exploiation" , size=4),
                }
    _sql_constraints = [
        ('company_registry_uniq', 'unique (company_registry)', 'Matricule employeur doit etre  unique !'),
        ('code_exploitation_uniq', 'UNIQUE(code_exploitation)', u'Code exploiation existe déjà !'),
    ]

    _constraints = [(_check_length_company_registry, u'Erreur: Le matricule employeur doit être composé de huit chiffres', ['company_registry']),
                    (_check_length_code_exploitation, u'Erreur: Le Code exploitation doit être composé de deux chiffres', ['code_exploitation']),]

res_company()
