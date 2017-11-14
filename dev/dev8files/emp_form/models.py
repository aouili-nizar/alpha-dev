# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp import models, fields, api, _
from openerp.tools.translate import _
import time
from openerp.report import report_sxw
import datetime
import hr_convertion
from openerp.exceptions import except_orm, Warning, RedirectWarning


#-------------------------------------------------------------------------------
# attestation de stage(normal)
#-------------------------------------------------------------------------------
class wizard_att_stage(models.TransientModel):
    _name = 'att.stage'


    
    emp1 = fields.Many2one('hr.stagiaires', string='Stagiaire', required=True)
    ref = fields.Char('Réf. : ')
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
            'get_user_work':self.get_user_work,
            'get_date_start': self.get_date_start,
            'get_date_end' : self.get_date_end,
            'get_stag_work': self.get_stag_work,
            'get_e':self.get_e,
            })
    def get_e(self,a):
        z = ""
    	obj = self.pool.get('hr.stagiaires')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.gender
    	if z == 'Feminin':
            return 'e'
        else:
            pass
    def get_stag_work(self,a):
    	z = ""
    	obj = self.pool.get('hr.stagiaires')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.theme
    	return z
    def get_date_end(self,a):
    	z = ""
    	obj = self.pool.get('hr.stagiaires')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.date_fin
    	return datetime.datetime.strptime(z, '%Y-%m-%d').strftime('%d-%m-%Y')
    def get_date_start(self,a):
    	z = ""
    	obj = self.pool.get('hr.stagiaires')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.date_entre
    	return datetime.datetime.strptime(z, '%Y-%m-%d').strftime('%d-%m-%Y')
    def get_user_work(self,a):
    	z = ""
    	obj = self.pool.get('hr.stagiaires')
    	ids = obj.search(self.cr,self.uid,[('id','=',a[0])])
    	for x in obj.browse(self.cr,self.uid,ids):
    		z = x.job.name
    	return z
    def get_gender(self,a):
    	z = ""
    	obj = self.pool.get('hr.stagiaires')
    	ids = obj.search(self.cr,self.uid,[('id','=',a[0])])
    	for x in obj.browse(self.cr,self.uid,ids):
    		z = x.gender
    		z1  = x.etciv
    	if z == "Masculin":
    		return "Mr"
    	elif z == "Feminin" and z1 == "Marié":
    		return "Mme"
    	else :
    		return "Mlle"
    def get_boss_gender(self,a):
    	return 'Monsieur'
    def get_boss_name(self,a):
    	return 'Zied'
    def get_name(self,a):
    	z = ""
    	obj = self.pool.get('hr.stagiaires')
    	ids = obj.search(self.cr,self.uid,[('id','=',a[0])])
    	for x in obj.browse(self.cr,self.uid,ids):
    		z = x.name
    	return z
    def get_work(self,a):
    	return "Gérant"
    def get_cin(self,a):
    	z = ""
    	obj = self.pool.get('hr.stagiaires')
    	ids = obj.search(self.cr,self.uid,[('id','=',a[0])])
    	for x in obj.browse(self.cr,self.uid,ids):
    		z = x.cin
    	return z
    def get_deliv(self,a):
    	z = ""
    	obj = self.pool.get('hr.stagiaires')
    	ids = obj.search(self.cr,self.uid,[('id','=',a[0])])
    	for x in obj.browse(self.cr,self.uid,ids):
    		z = x.deliv
    	return z 
class att_sage(models.AbstractModel):
    _name = 'report.emp_form.att_stage_report'
    _inherit = 'report.abstract_report'
    _template = 'emp_form.att_stage_report'
    _wrapped_report_class = att

#-------------------------------------------------------------------------------
# attestation de salaire
#-------------------------------------------------------------------------------


class wizard_att_salaire(models.TransientModel):
    _name = 'att.salaire'
    emp = fields.Many2one('hr.employee', string='Employé', required=True)
    ref = fields.Char('Réf. : ')

    @api.v7
    def print_report(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = False
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'emp_form.att_slaire_report',
            'datas': datas,
            'name': u'Attestation de salaire',
            'context': context
        }
class attsal(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
            super(attsal, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({
                'time': time,
                'get_boss_gender': self.get_boss_gender,
                'get_boss_name': self.get_boss_name,
                'get_gender': self.get_gender,
                'get_name': self.get_name,
                'get_work': self.get_work,
                'get_cin': self.get_cin,
                'get_deliv': self.get_deliv,
                'get_user_work': self.get_user_work,
                'get_emp_work': self.get_emp_work,
                'get_emp_contract_start': self.get_emp_contract_start,
                'get_emp_sal_string': self.get_emp_sal_string,
                'get_emp_sal_number': self.get_emp_sal_number,
                'get_e':self.get_e
            })

    def get_e(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.gender
    	if z == 'female':
            return 'e'
        else:
            pass
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
    	return datetime.datetime.strptime(z, '%Y-%m-%d').strftime('%d-%m-%Y')

    def get_emp_work(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.job_id.name
        return z
    def get_emp_contract_start(self,a):
        z = ''
        start =''
        obj = self.pool.get('hr.contract')
        recs = obj.search(self.cr, self.uid, [('employee_id', '=', a[0])])
        for x in obj.browse(self.cr, self.uid, recs):
            start = x.date_start
            if datetime.datetime.strptime(start,'%Y-%M-%d') < datetime.datetime.now():
                z = x.date_start
        return z
    def get_emp_sal_string(self,a):
        z = 0
        convertion = self.pool.get('hr.convertion').browse(
            self.cr, self.uid, self.uid)
        obj = self.pool.get('hr.payroll.bulletin')
        ids = obj.search(self.cr, self.uid, [
                         ('employee_id', '=', a[0]), ('period_id.fiscalyear_id', '=', datetime.datetime.strftime(datetime.datetime.now(), '%Y'))])
        sr = 0
        cr = 0
        base = 0
        brute = 0
        ct = 0
        ctrobj = self.pool.get('hr.contract')
        ctrids = ctrobj.search(self.cr, self.uid, [('employee_id.id', '=', a[0])])
        for w in ctrobj.browse(self.cr, self.uid, ctrids):
            brute = w.salaire_b
        for x in obj.browse(self.cr, self.uid, ids):
            sr = 0
            if x.employee_contract_id.rubrique_ids:
                for y in x.employee_contract_id.rubrique_ids:
                    sr = sr + y.montant
            base = x.salaire_base
            z = z + (base + sr)
            ct = ct + 1
        if ct < 12:
            z = z + (brute * (12 - ct))
        return convertion.trad(z, 'Dinar', 'Millime')
    def get_emp_sal_number(self,a):
        z = 0
        convertion = self.pool.get('hr.convertion').browse(
            self.cr, self.uid, self.uid)
        obj = self.pool.get('hr.payroll.bulletin')
        ids = obj.search(self.cr, self.uid, [
                         ('employee_id', '=', a[0]), ('period_id.fiscalyear_id', '=', datetime.datetime.strftime(datetime.datetime.now(), '%Y'))])
        sr = 0
        cr = 0
        base = 0
        brute = 0
        ct = 0
        ctrobj = self.pool.get('hr.contract')
        ctrids = ctrobj.search(self.cr, self.uid, [('employee_id.id', '=', a[0])])
        for w in ctrobj.browse(self.cr,self.uid,ctrids):
            brute = w.salaire_b
        for x in obj.browse(self.cr, self.uid, ids):
            sr = 0
            if x.employee_contract_id.rubrique_ids:
                for y in x.employee_contract_id.rubrique_ids:
                    sr = sr + y.montant
            base = x.salaire_base
            z = z + (base + sr)
            ct = ct + 1
        if ct < 12:
            z = z + (brute * (12 - ct))
        return round(z, 3)
class att_salaire(models.AbstractModel):
    _name = 'report.emp_form.att_slaire_report'
    _inherit = 'report.abstract_report'
    _template = 'emp_form.att_slaire_report'
    _wrapped_report_class = attsal

#-------------------------------------------------------------------------------
# attestation de travail
#-------------------------------------------------------------------------------


class wizard_att_travail(models.TransientModel):
    _name = 'att.travail'
    emp = fields.Many2one('hr.employee', string='Employé', required=True)
    ref = fields.Char('Réf. : ')

    @api.v7
    def print_report(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = False
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'emp_form.att_travail_report',
            'datas': datas,
            'name': u'Attestation de travail',
            'context': context
        }
class atttra(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
            super(atttra, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({
                'time': time,
                'get_boss_gender': self.get_boss_gender,
                'get_boss_name': self.get_boss_name,
                'get_gender': self.get_gender,
                'get_name': self.get_name,
                'get_work': self.get_work,
                'get_cin': self.get_cin,
                'get_deliv': self.get_deliv,
                'get_user_work': self.get_user_work,
                'get_emp_work': self.get_emp_work,
                'get_emp_contract_start': self.get_emp_contract_start,
                'get_emp_contract_type': self.get_emp_contract_type,
                'get_e': self.get_e
            })

    def get_e(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.gender
    	if z == 'female':
            return 'e'
        else:
            pass
    def get_user_work(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('user_id', '=', a)])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.job_id.name
    	return z

    def get_gender(self, a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.gender
    		z1 = x.marital
    	if z == "male":
    		return "Mr"
    	elif z == "female" and z1 == "m":
    		return "Mme"
    	else:
    		return "Mlle"

    def get_boss_gender(self, a):
    	return 'Monsieur'

    def get_boss_name(self, a):
    	return 'Zied'

    def get_name(self, a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.name
    	return z

    def get_work(self, a):
    	return "Gérant"

    def get_cin(self, a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.cin
    	return z

    def get_deliv(self, a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
            print x.deliv
            z = x.deliv
    	return datetime.datetime.strptime(z, '%Y-%m-%d').strftime('%d-%m-%Y')

    def get_emp_work(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
            z = x.job_id.name
            print  '---------------------------------------------------------------------------------------------------------'
            print ' '
            print ' '
            print 'the job is ',z
            print ' the employee  is',x.name_related
            print ' aaaaaaaaaaaaaand ids is', ids
            print ' '
            print ' '
            print '-----------------------------------------------------------------------------------------------------------'
        return z

    def get_emp_contract_start(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
            z = x.date_entree
        return datetime.datetime.strptime(z, '%Y-%m-%d').strftime('%d-%m-%Y')
    def get_emp_contract_type(self,a):
        z = ''
        start = ''
        obj = self.pool.get('hr.contract')
        recs = obj.search(self.cr, self.uid, [('employee_id', '=', a[0])])
        for x in obj.browse(self.cr, self.uid, recs):
            start = x.date_start
            if datetime.datetime.strptime(start, '%Y-%M-%d') < datetime.datetime.now():
                z = x.type_id.name
        return z
class att_travail(models.AbstractModel):
    _name = 'report.emp_form.att_travail_report'
    _inherit = 'report.abstract_report'
    _template = 'emp_form.att_travail_report'
    _wrapped_report_class = atttra

#-------------------------------------------------------------------------------
# attestation de stage(sivp)
#-------------------------------------------------------------------------------

class wizard_att_sivp(models.TransientModel):
    _name = 'att.sivp'
    emp = fields.Many2one('hr.employee', string='Employé', required=True)
    ref = fields.Char('Réf. : ')
    @api.one
    @api.onchange('emp')
    def control_emp(self):
        if self.emp:
            contr = self.env['hr.contract'].search([('employee_id.id','=',self.emp.id)]).type_id.name
            if not contr == 'SIVP':
                raise osv.except_osv(('Attention'), ('Vous devez selection un employé avec un contrat SIVP'))
    @api.v7
    def print_report(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = False
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'emp_form.att_sivp_report',
            'datas': datas,
            'name': u'Attestation de Stage (SIVP)',
            'context': context
        }
class attsivp(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
            super(attsivp, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({
                'time': time,
                'get_boss_gender': self.get_boss_gender,
                'get_boss_name': self.get_boss_name,
                'get_gender': self.get_gender,
                'get_name': self.get_name,
                'get_work': self.get_work,
                'get_cin': self.get_cin,
                'get_deliv': self.get_deliv,
                'get_user_work': self.get_user_work,
                'get_emp_work': self.get_emp_work,
                'get_emp_contract_start': self.get_emp_contract_start,
                'get_emp_contract_type': self.get_emp_contract_type,
                'get_e': self.get_e
            })

    def get_e(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.gender
    	if z == 'female':
            return 'e'
        else:
            pass
    def get_user_work(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('user_id', '=', a)])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.job_id.name
    	return z

    def get_gender(self, a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.gender
    		z1 = x.marital
    	if z == "male":
    		return "Mr"
    	elif z == "female" and z1 == "m":
    		return "Mme"
    	else:
    		return "Mlle"

    def get_boss_gender(self, a):
    	return 'Monsieur'

    def get_boss_name(self, a):
    	return 'Zied'

    def get_name(self, a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.name
    	return z

    def get_work(self, a):
    	return "Gérant"

    def get_cin(self, a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.cin
    	return z

    def get_deliv(self, a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.deliv
    	return datetime.datetime.strptime(z, '%Y-%m-%d').strftime('%d-%m-%Y')

    def get_emp_work(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.job_id.name
        return z

    def get_emp_contract_start(self, a):
        z = ''
        start = ''
        obj = self.pool.get('hr.contract')
        recs = obj.search(self.cr, self.uid, [('employee_id', '=', a[0])])
        for x in obj.browse(self.cr, self.uid, recs):
            start = x.date_start
            if datetime.datetime.strptime(start, '%Y-%M-%d') < datetime.datetime.now():
                z = x.date_start
        return datetime.datetime.strptime(z, '%Y-%m-%d').strftime('%d-%m-%Y')

    def get_emp_contract_type(self, a, b):
        z = ''
        start = ''
        obj = self.pool.get('hr.contract')
        recs = obj.search(self.cr, self.uid, [('employee_id', '=', a[0])])
        for x in obj.browse(self.cr, self.uid, recs):
            start = x.date_start
            if datetime.datetime.strptime(start, '%Y-%M-%d') < datetime.datetime.now():
                z = x.type_id.name
        return z
class att_sivp(models.AbstractModel):
    _name = 'report.emp_form.att_sivp_report'
    _inherit = 'report.abstract_report'
    _template = 'emp_form.att_sivp_report'
    _wrapped_report_class = attsivp


#-------------------------------------------------------------------------------
# Certificat de travail
#-------------------------------------------------------------------------------
class wizard_cert_travail(models.TransientModel):
    _name = 'cert.travail'
    emp = fields.Many2one('hr.employee', string='Employé', required=True)
    ref = fields.Char('Réf. : ')

    @api.v7
    def print_report(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = False
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'emp_form.cert_travail_report',
            'datas': datas,
            'name': u'Certificat de travail',
            'context': context
        }


class certtra(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
            super(certtra, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({
                'time': time,
                'get_boss_gender': self.get_boss_gender,
                'get_boss_name': self.get_boss_name,
                'get_gender': self.get_gender,
                'get_name': self.get_name,
                'get_work': self.get_work,
                'get_cin': self.get_cin,
                'get_deliv': self.get_deliv,
                'get_user_work': self.get_user_work,
                'get_emp_work': self.get_emp_work,
                'get_emp_contract_start': self.get_emp_contract_start,
                'get_emp_contract_end': self.get_emp_contract_end,
                'get_emp_contract_type': self.get_emp_contract_type,
                'get_e': self.get_e
            })

    def get_e(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.gender
    	if z == 'female':
            return 'e'
        else:
            pass

    def get_user_work(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('user_id', '=', a)])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.job_id.name
    	return z

    def get_gender(self, a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.gender
    		z1 = x.marital
    	if z == "male":
    		return "Mr"
    	elif z == "female" and z1 == "m":
    		return "Mme"
    	else:
    		return "Mlle"

    def get_boss_gender(self, a):
    	return 'Monsieur'

    def get_boss_name(self, a):
    	return 'Zied'

    def get_name(self, a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.name
    	return z

    def get_work(self, a):
    	return "Gérant"

    def get_cin(self, a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.cin
    	return z

    def get_deliv(self, a):
    	z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
            z = x.deliv
            print  '---------------------------------------------------------------------------------------------------------'
            print ' '
            print ' '
            print 'the deliv  is ',z
            print ' the employee  is',x.name_related
            print ' aaaaaaaaaaaaaand ids is' , ids
            print ' '
            print ' '
            print '-----------------------------------------------------------------------------------------------------------'
    	return datetime.datetime.strptime(z, '%Y-%m-%d').strftime('%d-%m-%Y')

    def get_emp_work(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.job_id.name
        return z

    def get_emp_contract_start(self, a):
        z = ""
    	obj = self.pool.get('hr.employee')
    	ids = obj.search(self.cr, self.uid, [('id', '=', a[0])])
    	for x in obj.browse(self.cr, self.uid, ids):
    		z = x.date_entree
        return z
        return datetime.datetime.strptime(z, '%Y-%m-%d').strftime('%d-%m-%Y')

    def get_emp_contract_end(self, a):
        z = ''
        start = ''
        obj = self.pool.get('hr.contract')
        recs = obj.search(self.cr, self.uid, [('employee_id', '=', a[0])])
        for x in obj.browse(self.cr, self.uid, recs):
            end = x.date_end
            
            z = end
        return datetime.datetime.strptime(z, '%Y-%m-%d').strftime('%d-%m-%Y')
    def get_emp_contract_type(self, a):
        z = ''
        start = ''
        obj = self.pool.get('hr.contract')
        recs = obj.search(self.cr, self.uid, [('employee_id', '=', a[0])])
        for x in obj.browse(self.cr, self.uid, recs):
            start = x.date_start
            if datetime.datetime.strptime(start, '%Y-%M-%d') < datetime.datetime.now():
                z = x.type_id.name
        return z


class cert_travail(models.AbstractModel):
    _name = 'report.emp_form.cert_travail_report'
    _inherit = 'report.abstract_report'
    _template = 'emp_form.cert_travail_report'
    _wrapped_report_class = certtra
