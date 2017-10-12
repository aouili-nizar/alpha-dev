# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#
#    Copyright (C) 2017  .
#    Coded by : Aouili Nizar & Mbarek sabrine
#
#----------------------------------------------------------------------------
from openerp.report import report_sxw
import time
from openerp.osv import osv


class report_declaration_fiscal(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
            super(report_declaration_fiscal, self).__init__(cr, uid, name, context=context)
            self.localcontext.update({
            'time': time,
            'get_declaration_employer':self._get_declaration_fiscal,
            'sum_impo_sal':self._get_total_salaire_imposable,
            'get_irpp' : self._get_irpp,
            'get_sum_brut' : self.get_sum_brut,
            'get_tfp_taux' : self.get_tfp_taux,
            'get_tfp' : self.get_tfp,
            'get_irpp_cpt' :self.get_irpp_cpt,
            'get_loyer':self.get_loyer,
            'get_honoraire':self.get_honoraire,
            'sum_15':self.sum_15,
            'get_hon5':self.get_hon5,
            'get_market':self.get_market,
            'get_total_source':self.get_total_source,
            'get_report_tfp':self.get_report_tfp,
            'get_total_tfp':self.get_total_tfp,
            'get_taux_fop':self.get_taux_fop,
            'get_fop':self.get_fop,
            'get_cl6':self.get_cl6,
            'get_cl18':self.get_cl18,
            'get_cl12':self.get_cl12,
            'get_totcol':self.get_totcol,
            'get_ded6':self.get_ded6,
            'get_ded12':self.get_ded12,
            'get_ded18':self.get_ded18,
            'get_mmo6':self.get_mmo6,
            'get_mmo12':self.get_mmo12,
            'get_mmo18':self.get_mmo18,
            'get_tvars':self.get_tvars,
            'get_totded':self.get_totded,
            'get_relq':self.get_relq,
            'get_repder':self.get_repder,
            'get_tvarep':self.get_tvarep,
            'get_nbrfact':self.get_nbrfact,
            'get_totdr':self.get_totdr,
            'get_big_sum':self.get_big_sum,
            'get_loc_taux':self.get_loc_taux,
            'get_loc_tcl':self.get_loc_tcl,
            'get_exp_taux':self.get_exp_taux,
            'get_expr_tcl':self.get_expr_tcl,
            'get_sum_tcl':self.get_sum_tcl,
            'get_fact':self.get_fact,
            'getb1':self.getb1,
            'getb2':self.getb2,
            'getb3':self.getb3,
            'getd':self.getd,
            'getc':self.getc,
            'gettloy':self.gettloy,
            'getthon15':self.getthon15,
            'getthon5':self.getthon5,
            'gettcol6':self.gettcol6,
            'gettcol12':self.gettcol12,
            'gettcol18':self.gettcol18,
            'gettded6':self.gettded6,
            'gettded12':self.gettded12,
            'gettded18':self.gettded18,
            'gettmmo6':self.gettmmo6,
            'gettmmo12':self.gettmmo12,
            'gettmmo18':self.gettmmo18,
            'getttvasrc':self.getttvasrc,
            'gettmar':self.gettmar,
            'getc6':self.getc6,
            'getc12':self.getc12,
            'getc18':self.getc18,
            'getd6':self.getd6,
            'getd12':self.getd12,
            'getd18':self.getd18,
            'getmm6':self.getmm6,
            'getmm12':self.getmm12,
            'getmm18':self.getmm18,
            'gettc':self.gettc,
            'getsrc25':self.getsrc25,
            'getgtt':self.getgtt,
            'get_fisc':self.get_fisc,

        })

    def gettloy(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_loy

        print taux_tfp
        return round(taux_tfp ,3)
    def getthon15(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_hon15

        print taux_tfp
        return round(taux_tfp ,3)        
    def getthon5(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_hon5

        print taux_tfp
        return round(taux_tfp ,3)        
    def gettmar(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_mar

        print taux_tfp
        return round(taux_tfp ,3)        
    def gettcol6(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_col6
        print 'this is taux 6'
        print taux_tfp
        return round(taux_tfp ,3)        
    def gettcol12(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_col12

        print taux_tfp
        return round(taux_tfp ,3)        
    def gettcol18(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_col18

        print taux_tfp
        return round(taux_tfp ,3)        
    def gettded6(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_ded6

        print taux_tfp
        return round(taux_tfp ,3)        
    def gettded12(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_ded12

        print taux_tfp
        return round(taux_tfp, 3)
    def gettded18(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_ded18

        print taux_tfp
        return round(taux_tfp ,3)        
    def gettmmo6(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_mmo6

        print taux_tfp
        return round(taux_tfp ,3)        
    def gettmmo12(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_mmo12

        print taux_tfp
        return round(taux_tfp ,3)        
    def gettmmo18(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_mmo18

        print taux_tfp
        return round(taux_tfp ,3)        
    def getttvasrc(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_retsrc

        print taux_tfp
        return round(taux_tfp, 3)
    def get_sum_tcl(self,a,b,fiscalyear_id,context=None):
        return round(a+b , 3 )
    def get_cl6(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print 'this is ids 6'
        print(ids)
        account = None
        balance = 0
        print 'this is obj 6'
        print obj
        print b
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_col_6
            print 'this is acc6 val and b '
            print x.tva_col_6.balance
        balance = account.balance
        if balance != 0:
            print'this is the result of cl 6'
            print round((balance/((balance/100)*b)),3)
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0
    def get_cl12(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_col_12
        balance = account.balance
        if balance != 0:
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0
    def get_cl18(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_col_18
        balance = account.balance
        if balance != 0:
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0
    def get_totcol(self,a,b,c,context=None):
        print('this is tot col')
        print a 
        print b 
        print c
        return a+b+c
    def get_ded6(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_ded_6
        balance = account.balance
        if balance != 0:
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0
    def get_ded12(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_ded_12
        balance = account.balance
        if balance != 0:
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0
    def get_ded18(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_ded_18
        balance = account.balance
        if balance != 0:
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0
    def get_mmo6(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_mmo_6
        balance = account.balance
        if balance != 0:
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0
    def get_mmo12(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_mmo_12
        balance = account.balance
        if balance != 0:
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0
    def get_mmo18(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_mmo_18
        balance = account.balance
        if balance != 0:
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0
    def get_tvars(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_ret_src
        balance = account.balance
        if balance != 0:
            return (balance/((balance/100)*b))
        elif balance == 0:
            return 0

    def get_totded(self,a,b,c,d,e,f,g,context=None):
        return a+b+c+d+e+f+g
    def getc6(self,fiscalyear_id,context=None):
        #c 6%
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        c6 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_col_6
        c6 = account.balance
        print 'this is c6'
        print c6
        return round(-1 * c6, 3) if c6 != 0 else 0
    def getc12(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        c12 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_col_12
        c12 = account.balance
        return round(-1 * c12, 3) if c12 != 0 else 0
    def getc18(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        c18 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_col_18
        c18 = account.balance
        return round(-1 * c18,3) if c18 != 0 else 0
    def getd6(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        d6 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_ded_6
        d6 = account.balance
        return round(-1 * d6, 3) if d6 != 0 else 0
    def getd12(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        d12 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_ded_12
        d12 = account.balance
        return round(-1 * d12,3) if d12 != 0 else 0
    def getd18(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        d18 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_ded_18
        d18 = account.balance
        return round(-1 * d18, 3) if d18 != 0 else 0
    def getmm6(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        m6 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_mmo_6
        m6 = account.balance
        return round(-1 * m6, 3) if m6 != 0 else 0
    def getmm12(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        m12 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_mmo_12
        m12 = account.balance
        return round(-1 * m12, 3) if m12 != 0 else 0
    def getmm18(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        m18 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_mmo_18
        m18 = account.balance
        return round(-1 * m18, 3) if m18 != 0 else 0
    def gettc(self,a,b,c,context=None):
        return a+b+c
    def getsrc25(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        s25 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_ret_src
        s25 = account.balance
        return round(-1 * s25, 3) if s25 != 0 else 0
    def getgtt(self,a,b,c,d,e,f,context=None):
        return a+b+c+d+e+f
                                                   
    def get_relq(self,fiscalyear_id,context=None):
        #c 6%
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        c6 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_col_6
        c6 = -1 * account.balance
        # c 12%
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        c12 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_col_12
        c12 = -1 * account.balance
        # c 18%
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        c18 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_col_18
        c18 = -1 * account.balance



        # d 6%
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        d6 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_ded_6
        d6 = -1 * account.balance

        # d 12%
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        d12 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_ded_12
        d12 = -1 *  account.balance

        # d 18%
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        d18 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_ded_18
        d18 = -1 *  account.balance

        # m 6%
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        m6 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_mmo_6
        m6 =  -1 * account.balance

        # m 12%
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        m12 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_mmo_12
        m12 = -1 * account.balance

        # m 18%
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        m18 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_mmo_18
        m18 = -1 * account.balance
        # s 12%
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        s25 = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tva_ret_src
        s25 = -1 * account.balance
        return round(((c6+c12+c18)-(d6+d12+d18+m6+m12+m18+s25)),3) if ((c6+c12+c18)-(d6+d12+d18+m6+m12+m18+s25)) != 0 else 0

    def get_repder(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.report_tva
        balance = account.balance
        return round((0-balance),3) if balance != 0 else 0
    def get_tvarep(self,a,b,context=None):
        print('this is tvarp a')
        print(a)
        print(b)
        return a+b
    def get_nbrfact(self,a,context=None):
        obj = self.pool.get('account.invoice')
        ids = obj.search(self.cr,self.uid,[('period_id.code','=',a)])
        i = 0 
        for x in obj.browse(self.cr,self.uid,ids):
            i = i+1
        return i
    def get_fisc(self,a,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            balance = x.taux_dr_fisc
        if a != 0  :
            return round(a/balance,3)
        elif balance == 0 :
            return 0 
    def get_fact(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print('these r fact ids')
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            print('these r fact shit')
            print x
            print x.cpt_fact.balance
            account  = x.cpt_fact
        balance = account.balance
        return round(-1 *  balance,3) if balance !=0 else 0
    def get_totdr(self,context=None):
        pass

    def get_big_sum(self,a,b,c,d,e,f,context=None):
        print('this is a')
        print a
        print('this is b')
        print b
        print('this is c')
        print c
        print('this is d')
        print d
        print('this is e')
        print e
        print('this is f')
        print f
        return a+b+c+d+e+f

    def get_loyer(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print "this is loy"
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_loy
        balance = account.balance
        if balance != 0:
            print "this is loy result positive"
            print (balance/((balance/100)*b))
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0

    def get_honoraire(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_hon
        balance = account.balance
        if balance != 0:
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0
    def sum_15(self,a,b,context=None):
        print'this is sum 15'
        print a
        print b
        return a+b
    def get_hon5(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_hon_5
        balance = account.balance
        if balance != 0:
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0
    def get_market(self,fiscalyear_id,b,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tfp
        balance = account.balance
        if balance != 0:
            return round((balance/((balance/100)*b)),3)
        elif balance == 0:
            return 0
    def getb1(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        loy = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_loy
        loy = -1 * account.balance
        return round(loy,3) if loy !=0 else 0
    def getb2(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        hon = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_hon
        hon = -1 * account.balance
        return round(hon,3) if hon !=0 else 0
    def getb3(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        loy = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_loy
        loy = account.balance
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        hon = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_hon
        hon = account.balance
        b3 = 0
        b3 = loy + hon
        return round(-1 * b3, 3) if b3 != 0 else 0
    def getc(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        c = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_hon_5
        c = account.balance
        return round(-1* c ,3) if c != 0 else 0
    def getd(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        d= 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_hon_5
        d= account.balance
        return round(-1 * d ,3)  if d != 0 else 0
    def get_total_source(self,a,fiscalyear_id,context=None):
        # b3
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        loy = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_loy
        loy = account.balance
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        hon = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_hon
        hon = account.balance
        b3 = 0
        b3 = loy + hon
        # c
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        c = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_hon_5
        c = account.balance
        # d
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        d= 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_source_hon_5
        d= account.balance
        return -1* (a+b3+c+d)
    def get_report_tfp(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.tfp
        return round(-1 * account.balance ,3) if account.balance != 0 else 0
    def get_total_tfp(self,a,b,context=None):
        if b>a:
            return 0
        else :
            return a-b

    def get_taux_fop(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_fps

        print taux_tfp
        return round(taux_tfp ,3)
    def get_loc_taux(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.tcl_loc

        print taux_tfp
        return round(taux_tfp,3)
    def get_exp_taux(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_exr
        print taux_tfp
        return taux_tfp
    def get_loc_tcl(self,a,b,context=None):
        return round(b * a ,3)
    def get_expr_tcl(self,a,b,context=None):
        return round(b * a ,3)
    def get_fop(self,a,b,context=None):
        res = (a/100)*b
        return round(res ,3)
    def get_irpp_cpt(self,fiscalyear_id,context=None):
        obj = self.pool.get('declaration.fiscal.config')
        ids = obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(ids)
        account = None
        balance = 0
        for x in obj.browse(self.cr,self.uid,ids):
            account  = x.ret_sal
        return round((-1 * account.balance),3) if account.balance !=0 else 0
    def get_tfp_taux(self,fiscalyear_id,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        print(search_ids)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_tfp

        print taux_tfp
        return round(taux_tfp ,3)
    def get_tfp(self,fiscalyear_id,brut,context=None):
        taux_obj = self.pool.get('declaration.fiscal.config')
        search_ids=taux_obj.search(self.cr,self.uid,[('year','=',fiscalyear_id)],context)
        for x in taux_obj.browse(self.cr,self.uid,search_ids):
            taux_tfp = x.taux_tfp
        taxres = (brut/100) * taux_tfp
        return round(taxres,3)
    def get_sum_brut(self,fiscalyear_id,periode_id,context=None):
        salaire_obj=self.pool.get('hr.payroll.bulletin')
        search_ids=salaire_obj.search(self.cr,self.uid,[('month_id.period_id.fiscalyear_id','=',fiscalyear_id[1]),('period_id.name','=',periode_id[1]),('employee_contract_id.type_id.name','!=','SIVP')],context)
        total=0.0
        for line in salaire_obj.browse(self.cr,self.uid,search_ids) :
            total += line.salaire_brute
        print(total)
        return total
    def _get_irpp(self,fiscalyear_id,periode_id,context=None):
        salaire_obj=self.pool.get('hr.payroll.bulletin')
        search_ids=salaire_obj.search(self.cr,self.uid,[('period_id.fiscalyear_id','=',fiscalyear_id),('period_id.name','=',periode_id),('employee_contract_id.type_id.name','!=','SIVP')],context)
        total=0.0
        print "this is the result of the search  irpp ^_^ and it's parameters"
        print(search_ids)
        print'------'
        print(fiscalyear_id)
        print'-------'
        print(periode_id[1])
        for line in salaire_obj.browse(self.cr,self.uid,search_ids) :
            total += line.igr
        print"this is the total of irpp ^_^"
        print(total)
        return total
    def _get_total_salaire_imposable(self,fiscalyear_id,periode_id,context=None):
        salaire_obj=self.pool.get('hr.payroll.bulletin')
        search_ids=salaire_obj.search(self.cr,self.uid,[('month_id.period_id.fiscalyear_id','=',fiscalyear_id),('period_id.name','=',periode_id),('employee_contract_id.type_id.name','!=','SIVP')],context)
        total=0.0
        for line in salaire_obj.browse(self.cr,self.uid,search_ids) :
            total += line.salaire_brute_imposable
        print(total)
        return total


    def _get_declaration_fiscal(self,fiscalyear_id,context=None):
        salaire_obj=self.pool.get('hr.payroll.bulletin')
        search_ids=salaire_obj.search(self.cr,self.uid,[('month_id.period_id.fiscalyear_id','=',fiscalyear_id)],context)
        employees={}
        for sal in salaire_obj.browse(self.cr,self.uid,search_ids) :
            if sal.employee_id.id in employees:
                employees[sal.employee_id.id]['salaire_brute_imposable'] += sal.salaire_brute_imposable
                employees[sal.employee_id.id]['irpp'] += sal.igr
            else :
                val={'employee_id':sal.employee_id.name,'salaire_brute_imposable':sal.salaire_brute_imposable,'irpp':sal.igr}
                employees[sal.employee_id.id] = val

        result=[]
        for key, val in employees.items():
            result.append(val)


        return result



class declaration_employer_report(osv.AbstractModel):
    _name = 'report.declaration_fiscale.declaration_fiscal_report'
    _inherit = 'report.abstract_report'
    _template = 'declaration_fiscale.declaration_fiscal_report'
    _wrapped_report_class = report_declaration_fiscal
