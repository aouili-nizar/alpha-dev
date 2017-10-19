# -*- coding: utf-8 -*-


from openerp.osv import fields, osv
from tempfile import TemporaryFile
import base64
import datetime
import time
from openerp.tools.translate import _

LEN_NUM_PAGE=3
LEN_NUM_LIGNE=2
LEN_SALAIRE=8
LEN_IDENTITE_ASSURE=34

class wizard_declaration_cnss(osv.osv_memory):
    _name = 'wizard_declaration_cnss'
    _description = u'Déclaration CNSS  For'

    TRIMESTER = [
            ('0', u'1er trimestre'),
            ('1', u'2e trimestre'),
            ('2', u'3e trimestre'),
            ('3', u'4e trimestre'),

            ]

    def _get_default_fiscalyear_id(self, cr, uid, context=None):
        fiscalyear_id = self.pool.get('account.fiscalyear').find(cr, uid)
        return fiscalyear_id

    def _get_default_company(self, cr, uid, context=None):
        company_id = self.pool.get('res.users')._get_company(cr, uid, context=context)
        if not company_id:
            raise osv.except_osv(_('Error!'), _('There is no default company for the current user!'))
        return company_id


    _columns ={
               'fiscalyear_id':fields.many2one('account.fiscalyear', 'Exercice fiscal' , required=True),
               'company_id':fields.many2one('res.company', u'Société', required=True),
               'trimester':fields.selection(TRIMESTER,'Trimestre', select=True, required=True),
               'state': fields.selection([('choose', 'choose'),
                                       ('get', 'get')])     ,
                'data': fields.binary('Fichier CNSS', readonly=True),
                'name': fields.char('Nom'),

               }


    _defaults = {
                'fiscalyear_id':_get_default_fiscalyear_id,
                'company_id':_get_default_company,
                'state': 'choose',
              }

    def print_report(self, cr, uid, ids, context=None):
        datas = {'ids': []}
        datas['model'] = 'wizard_declaration_cnss'
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        context['landscape']=True
        return self.pool['report'].get_action(cr, uid, [], 'devplus_hr_payroll_declaration_cnss_tn.report_declaration_cnss', data=datas, context=context)

    def print_report_recapitulatif(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard_declaration_cnss'
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        return self.pool['report'].get_action(cr, uid, [], 'devplus_hr_payroll_declaration_cnss_tn.report_recapitulatif_cnss', data=datas, context=context)

    def _get_lines(self,cr,uid, company_id,fiscalyear_id,trimester):
        period_ids=self.pool.get('account.period').search(cr,uid,[('fiscalyear_id','=',fiscalyear_id)])

        obj = self.pool.get('account.period')
        # if existe periode ouverture period_ids=13 else period_ids=12
        # if period_ids==12 :
        for per in obj.browse(cr,uid,period_ids):
            if trimester =='0' :
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==1)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day)):
                    mois1=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==2)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois2=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==3)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois3=per.id
            elif trimester =='1' :
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==4)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day)):
                    mois1=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==5)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois2=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==6)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois3=per.id
            elif trimester =='2' :
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==7)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day)):
                    mois1=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==8)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois2=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==9)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois3=per.id

            else :
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==10)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois1=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==11)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day)):
                    mois2=per.id
                if((datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").month==12)and(datetime.datetime.strptime(per.date_stop ,"%Y-%m-%d").day+1-datetime.datetime.strptime(per.date_start ,"%Y-%m-%d").day>=28)):
                    mois3=per.id


        sql = '''
               SELECT e.id ,e.matricule,e.cnss,SUBSTRING(r.name, 0, 60) as name,e.cin,

             ( select  b1.salaire_brute_cotisable  from hr_payroll_bulletin  b1 where
               b1.period_id = %s and b1.employee_id=e.id
                ) as mois1,

             ( select  b2.salaire_brute_cotisable  from hr_payroll_bulletin  b2 where
               b2.period_id = %s and b2.employee_id=e.id
                ) as mois2,

             ( select  b3.salaire_brute_cotisable  from hr_payroll_bulletin  b3 where
               b3.period_id = %s and b3.employee_id=e.id
                ) as mois3 ,

            (select  sum(b4.salaire_brute_cotisable)  from hr_payroll_bulletin  b4 where
               b4.period_id  in(%s,%s,%s)  and b4.employee_id=e.id) as total

            From  hr_employee e
            LEFT JOIN resource_resource r on (r.id=e.resource_id)
             where r.active=true and e.cnss5 is true
             and ((select count(*) from hr_contract hc where  hc.employee_id=e.id)>0)
            ''' % (mois1, mois2, mois3, mois1, mois2, mois3)

        print '-------sql------',sql
        cr.execute(sql)
        declaration_cnss = cr.dictfetchall()

        num_page=1
        num_line=1
        resultats=[]
        for declaration in declaration_cnss:
            declaration.update({'num_page':num_page,'num_line':num_line})
            if num_line == 12 :
                num_page += 1
                num_line =1
            else :
                num_line += 1
            resultats.append(declaration)
        return resultats
    #testé la structure de fichier text de déclaration des salaires(N° Employeur:8,code exploitation:2, N° assurré sociale:10,
    #Trimestre:1, Année:2,Salaire Trimestriel:8,Numéro chez Employeur:6,Identité:34,N° Page:3 ,N° Ligne:2,Zone Vierge:4)
    def generate_file(self, cr, uid, ids, context=None):

        datas = self.read(cr, uid, ids, context=context)[0]
        this = self.browse(cr, uid, ids)[0]
        company_id=datas['company_id'][0]
        fiscalyear_id=datas['fiscalyear_id'][0]
        trimester=datas['trimester']
        fiscalyear = self.pool.get('account.fiscalyear').browse(cr,uid,fiscalyear_id,context)
        company = self.pool.get('res.company').browse(cr,uid,company_id,context)
        fp = TemporaryFile()

        #cnss employeur
        cnss_employeur=company.cnss
        if not cnss_employeur:
            raise osv.except_osv(_('Attention!'), _(u"Veuillez remplir le CNSS de la société dans la fiche du société"))
        cnss_employeur=cnss_employeur.split('-')
        if  len(cnss_employeur) != 2  :
            raise osv.except_osv(_('Attention!'), _(u"Format CNSS de la société est incorrecte : xxxxxxxx-yy "))
        if not company.code_exploitation :
            raise osv.except_osv(_('Attention!'), _(u"Veuillez remplir le Code d'exploitation de la société dans la fiche du société"))



        code_exploitation= company.code_exploitation
        matricule_employeur=company.company_registry
        annee=fiscalyear.code[2:4]
        #get all line
        all_lines=self._get_lines(cr,uid,company_id,fiscalyear_id,trimester)
        file_dec=''
        for line_cnss in all_lines:
            #controle
            if not line_cnss['cin']:
                raise osv.except_osv(_('Attention!'), _(u"Veuillez remplir le CIN de l'employé %s"%line_cnss['name']))
            cin=line_cnss['cin']
            cnss= line_cnss['cnss']
            num_page=line_cnss['num_page']
            num_page=str(num_page).zfill(LEN_NUM_PAGE)
            num_line=line_cnss['num_line']
            num_line=str(num_line).zfill(LEN_NUM_LIGNE)
            #cnss employee
            matricule_employee=line_cnss['matricule']
            identite_assure=line_cnss['name']
            identite_assure=identite_assure.ljust(LEN_IDENTITE_ASSURE)
            salaire=str(line_cnss['total']).replace('.','').replace(',','')
            salaire=str(salaire).ljust(LEN_SALAIRE,'0')

            file_dec+='%s%s%s%s%s%s%s%s%s%s%s'%(matricule_employeur,code_exploitation,cnss,trimester,annee, \
                 salaire,matricule_employee,identite_assure,num_page,num_line,'\r\n')

        file_dec=file_dec[0:len(file_dec)-1]
        fp.write(file_dec.encode('utf-8'))
        fp.seek(0)
        fp_name= 'DS'+str(matricule_employeur)+str(code_exploitation)+'.'+str(trimester)+str(annee)+'.txt'
        self.write(cr, uid, ids, {'state': 'get',
                                  'data': base64.encodestring(fp.read()),
                                  'name':fp_name}, context=context)
        fp.close()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard_declaration_cnss',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }




wizard_declaration_cnss()
