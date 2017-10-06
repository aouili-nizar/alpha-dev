# -*- coding: utf-8 -*-


from openerp.osv import fields, osv
from tempfile import TemporaryFile
import base64
from openerp.tools.translate import _


LEN_MATR_EMPLOYEUR = 8
LEN_CLE_EMPLOYEUR = 2
LEN_CODE_EXPLOITATION = 4
LEN_TRIMESTRE=1
LEN_ANNEE=4
LEN_NUM_PAGE=3
LEN_NUM_LIGNE=2
LEN_MAT_ASSURE=8
LEN_CLE_ASSURE=2
LEN_IDENTITE_ASSURE=60
LEN_CARTE_IDENTITE=8
LEN_SALAIRE=10
LEN_ZONE_VIERGE=10



class wizard_declaration_cnss(osv.osv_memory):
    _name = 'wizard_declaration_cnss'
    _description = u'Déclaration CNSS  For'
    
    TRIMESTER = [
            ('1', u'1er trimestre'),
            ('2', u'2e trimestre'),
            ('3', u'3e trimestre'),
            ('4', u'4e trimestre'),
           
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
        return self.pool['report'].get_action(cr, uid, [], 'devplus_hr_payroll_tn.report_declaration_cnss', data=datas, context=context)

    def print_report_recapitulatif(self, cr, uid, ids, context=None):
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard_declaration_cnss'
        datas['form'] = self.read(cr, uid, ids, context=context)[0]
        return self.pool['report'].get_action(cr, uid, [], 'devplus_hr_payroll_tn.report_recapitulatif_cnss', data=datas, context=context)
    
    def _get_lines(self,cr,uid, company_id,fiscalyear_id,trimester):
        period_ids=self.pool.get('account.period').search(cr,uid,[('fiscalyear_id','=',fiscalyear_id)])
        
        # if existe periode ouverture period_ids=13 else period_ids=12
        if period_ids==12 :
            if trimester =='1' : 
                mois1=period_ids[0]
                mois2=period_ids[1]
                mois3=period_ids[2]
            elif trimester =='2' : 
                mois1=period_ids[3]
                mois2=period_ids[4]
                mois3=period_ids[5]           
            elif trimester =='3' : 
                mois1=period_ids[6]
                mois2=period_ids[7]
                mois3=period_ids[8]             
            else : 
                mois1=period_ids[9]
                mois2=period_ids[10]
                mois3=period_ids[11]  
        else :
            if trimester =='1' : 
                mois1=period_ids[1]
                mois2=period_ids[2]
                mois3=period_ids[3]
            elif trimester =='2' : 
                mois1=period_ids[4]
                mois2=period_ids[5]
                mois3=period_ids[6]           
            elif trimester =='3' : 
                mois1=period_ids[7]
                mois2=period_ids[8]
                mois3=period_ids[9]             
            else : 
                mois1=period_ids[10]
                mois2=period_ids[11]
                mois3=period_ids[12]            
           
        
                
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



                      
        cle_employeur='00'
        if len(cnss_employeur)==2:
            matricule_employeur=cnss_employeur[0]
            cle_employeur=cnss_employeur[1]
        matricule_employeur= (matricule_employeur[0:LEN_MATR_EMPLOYEUR]).ljust(LEN_MATR_EMPLOYEUR,'0')
        cle_employeur= (cle_employeur[0:LEN_CLE_EMPLOYEUR]).ljust(LEN_CLE_EMPLOYEUR,'0')
        if company.code_exploitation : 
            code_exploitation= company.code_exploitation
        code_exploitation=((code_exploitation)[0:LEN_CODE_EXPLOITATION]).ljust(LEN_CODE_EXPLOITATION,'0')
        trimester=trimester.ljust(LEN_TRIMESTRE)
        annee=((fiscalyear.code)[0:LEN_ANNEE]).ljust(LEN_ANNEE)
        #get all line
        all_lines=self._get_lines(cr,uid,company_id,fiscalyear_id,trimester)
        file_dec=''
        for line_cnss in all_lines:
            #controle
            if not line_cnss['cin']:
                raise osv.except_osv(_('Attention!'), _(u"Veuillez remplir le CIN de l'employé %s"%line_cnss['name']))
            num_page=line_cnss['num_page']  
            num_page=str(num_page).zfill(LEN_NUM_PAGE)   
            num_line=line_cnss['num_line'] 
            num_line=str(num_line).zfill(LEN_NUM_LIGNE)  
            #cnss employee
            matricule_employee='00000000'
            cle_employee='00'
            cnss= line_cnss['cnss']
            cnss=cnss.split('-')
            if len(cnss)==2:
                matricule_employee=cnss[0]
                cle_employee=cnss[1]
            matricule_employee= (matricule_employee[0:LEN_MAT_ASSURE]).ljust(LEN_MAT_ASSURE,'0')
            cle_employee= (cle_employee[0:LEN_CLE_ASSURE]).ljust(LEN_CLE_ASSURE,'0')
            identite_assure=line_cnss['name'].upper()
            identite_assure=identite_assure.ljust(LEN_IDENTITE_ASSURE)
            cin=line_cnss['cin']
            cin=(cin[0:LEN_CARTE_IDENTITE]).ljust(LEN_CARTE_IDENTITE,'0')
            salaire=str(line_cnss['total']).replace('.','').replace(',','')
            salaire=str(salaire).zfill(LEN_SALAIRE)   
            zone_vierge=''.ljust(LEN_ZONE_VIERGE)
            
            #file_dec+=str(str(matricule_employeur)+str(cle_employeur)+str(code_exploitation)+str(trimester)+str(annee) + \
                 #str(num_page)+str(num_line)+str(matricule_employee)+str(cle_employee)+str(identite_assure)+str(cin)+str(salaire)+str(zone_vierge)) \
                 #+str('\n')
                             
            file_dec+='%s%s%s%s%s%s%s%s%s%s%s%s%s%s'%(matricule_employeur,cle_employeur,code_exploitation,trimester,annee, \
                 num_page,num_line,matricule_employee,cle_employee,identite_assure,cin,salaire,zone_vierge ,'\n')
                 
        file_dec=file_dec[0:len(file_dec)-1]
        fp.write(file_dec.encode('utf-8'))
        fp.seek(0)
        fp_name= 'DS'+str(matricule_employeur)+str(cle_employeur)+str(code_exploitation)+'.'+str(trimester)+str(annee)+'.txt'
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
        