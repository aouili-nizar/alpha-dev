# -*- coding: utf-8 -*-
from openerp.report import report_sxw
import time
#import convertion
from openerp.osv import osv

class bulletin(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(bulletin, self).__init__(cr, uid, name, context)
        self.localcontext.update({
                                  'get_situation_faml' : self.get_situation_faml,
                                  'gross_wage_line' : self.gross_wage_line,
                                  'get_hs_line' : self.get_hs_line,
                                  'cotisation_line' : self.cotisation_line,
                                  'ir_line' :   self.ir_line,
                                  'redevance_line':self.redevance_line,
                                  'get_retenu_line':self.get_retenu_line,
                                  
                                  })

        
        
     

  
     
     
    def get_situation_faml(self, situation):
        situation_faml = ""
        if situation == 'm'   :
            situation_faml = u'Marié'
        elif  situation == 'c'   :  
            situation_faml = u'Célibataire'
        elif  situation == 'v'   :  
            situation_faml = u'Veuf'
        elif  situation == 'd'   :  
            situation_faml = u'Divorcé'                        
        return   situation_faml      
    
    def gross_wage_line(self, salary_line_ids) :
        listt = []
        for line in salary_line_ids :
            if line.type == 'brute' and line.afficher:
                dictt = {'name' : line.name,
                      'base' : line.base,
                      'taux' : float(line.taux),
                      'gain' :  round(line.gain, self.pool.get('decimal.precision').precision_get(self.cr, self.uid, 'Montant Paie')),
                      'retenu': line.retenu,
                      }
                listt.append(dictt)
        return listt  
    def get_hs_line(self, salary_line_ids):    
        listt = []
        for line in salary_line_ids :
            if   line.afficher and line.type == 'hs' :
                dictt = {'name' : line.name,
                      'base' : line.base,
                      'taux' : line.taux,
                      'gain' : line.gain,
                      'rate_employer' : line.rate_employer,
                      'subtotal_employer' : line.subtotal_employer,
                      } 
                listt.append(dictt)
        return listt
    
    def cotisation_line(self, salary_line_ids):    
        listt = []
        for line in salary_line_ids :
            if  line.afficher and line.type == 'cotisation' :
                dictt = {'name' : line.name,
                      'base' : line.base,
                      'taux' : line.taux,
                      'gain' : line.gain,
                      'retenu' : line.retenu,
                      'rate_employer' : line.rate_employer,
                      'subtotal_employer' : line.subtotal_employer,
                      } 
                listt.append(dictt)
        return listt
    
    def ir_line(self, salary_line_ids):    
        listt = []
        for line in salary_line_ids :
            if  line.afficher and line.type == 'ir' :
                dictt = {'name' : line.name,
                      'base' : line.base,
                      'taux' : '-',
                      'gain' : line.gain,
                      'retenu' : line.retenu,
                      'rate_employer' : '-',
                      'subtotal_employer' : line.subtotal_employer,
                      } 
                listt.append(dictt)
        return listt
    
    def redevance_line(self, salary_line_ids):    
        listt = []
        for line in salary_line_ids :
            if  line.afficher and line.type == 'redevance' :
                dictt = {'name' : line.name,
                      'base' : line.base,
                      'taux' : line.taux,
                      'gain' : line.gain,
                      'retenu' : line.retenu, 
                      } 
                listt.append(dictt)
        return listt
    def get_retenu_line(self, salary_line_ids):    
        listt = []
        for line in salary_line_ids :
            if   line.afficher and line.type == 'retenu' :
                dictt = {'name' : line.name,
                        'base' : line.base,
                        'taux' : 1.0,
                        'gain' :  line.gain,
                       'retenu': round(line.retenu, self.pool.get('decimal.precision').precision_get(self.cr, self.uid, 'Montant Paie')),
                      } 
                listt.append(dictt)
        return listt
        
class report_bulletin(osv.AbstractModel):
    _name = 'report.devplus_hr_payroll_tn.bulletin_report'
    _inherit = 'report.abstract_report'
    _template = 'devplus_hr_payroll_tn.bulletin_report'
    _wrapped_report_class = bulletin