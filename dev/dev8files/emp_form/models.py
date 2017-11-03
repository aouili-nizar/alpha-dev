# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp import models, fields, api, _
from openerp.tools.translate import _
import time
from openerp.report import report_sxw
#-------------------------------------------------------------------------------
# attestation de stage
#-------------------------------------------------------------------------------
class wizard_att_stage(models.TransientModel):
    _name = 'att.stage'
    emp = fields.Many2one('hr.employee', string='Employé', required=True)
    ds = fields.Date('Date debut')
    de = fields.Date('Date fin')
    boss = fields.Many2one('hr.employee' ,string="Gérant",required=True)
    @api.v7
    def print_report(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = False
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'emp_form.att_stage_report',
            'datas': datas,
            'name': u'Attestation de stage',
            'context':context
            }

class att(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
            super(att, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({
            'time': time,
            'get_boss_gender':self.get_boss_gender,
            'get_boss_name':self.get_boss_name,
            'get_gender':self.get_gender,
            'get_name':self.get_name,
            'get_work':self.get_work,
            'get_cin':self.get_cin,
            'get_deliv':self.get_deliv,
            'get_user_work':self.get_user_work
            })
    def get_user_work(self,a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr,self.uid,[('user_id','=',a)])
    	for x in obj.browse(self.cr,self.uid,ids):
    		z = x.job_id.name
    	return z
    def get_gender(self,a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr,self.uid,[('id','=',a[0])])
    	for x in obj.browse(self.cr,self.uid,ids):
    		z = x.gender
    		z1  = x.marital
    	if z =="male":
    		return "Mr"
    	elif z == "female" and z1 == "m":
    		return "Mme"
    	else :
    		return "Mlle"
    def get_boss_gender(self,a):
    	return 'Monsieur'
    def get_boss_name(self,a):
    	return 'Zied'
    def get_name(self,a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr,self.uid,[('id','=',a[0])])
    	for x in obj.browse(self.cr,self.uid,ids):
    		z = x.name
    	return z
    def get_work(self,a):
    	return "Gérant"
    def get_cin(self,a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr,self.uid,[('id','=',a[0])])
    	for x in obj.browse(self.cr,self.uid,ids):
    		z = x.cin
    	return z
    def get_deliv(self,a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr,self.uid,[('id','=',a[0])])
    	for x in obj.browse(self.cr,self.uid,ids):
    		z = x.deliv
    	return z   	
class att_sage(osv.AbstractModel):
    _name = 'report.emp_form.att_stage_report'
    _inherit = 'report.abstract_report'
    _template = 'emp_form.att_stage_report'
    _wrapped_report_class = att
class deliv(models.Model):
	_inherit="hr.employee"

	deliv = fields.Date('Date delivrance Cin')

#-------------------------------------------------------------------------------
# attestation de salaire
#-------------------------------------------------------------------------------
