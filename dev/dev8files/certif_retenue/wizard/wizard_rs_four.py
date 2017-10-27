# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp import models, fields, api, _
from openerp.tools.translate import _
import datetime
#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------

class var(models.Model):
    _inherit="account.invoice"
    def openwiz(self,b,c,d,e):



        return{
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rs_four',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context':e
    
    }
class wizard_res_four(models.TransientModel):
    _name = 'rs_four'
    def init_rs(self):
        return "RS"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    @api.one
    @api.onchange('taux')
    def compute_ret(self):
        if(self.taux):  
            fact = self.env.context.get('amount_total')
            x=0
            x =  fact * (self.taux.value / 100)
            self.update({
                'ret_val': x
            })
        else:
            self.update({
                'ret_val' : 0
            })
    periode = fields.Many2one('account.period', string='Periode', required=True,default=lambda self: self.env.context.get('period_id'))
    four = fields.Many2one('res.partner', string='Fournisseur',readonly=True, required=True, default=lambda self: self.env.context.get('partner'))
    libel = fields.Char('Libellé', required=True,default=init_rs)
    journal = fields.Many2one('account.journal', string="Journal", required=True,default=lambda self: self.env['account.journal'].search([('code','=','OD')]).id)
    taux = fields.Many2one('taux_rs', required=True,string="Taux")
    ret_val = fields.Float('Valeur de retenue' , readonly=True,compute=compute_ret)
    reference = fields.Char('Reference ',default="/")
    @api.one
    def rs_pay(self):
        move = {}
        moveline = []
        objc1={}
        vouch = {}
        dr=[]
        cr=[]
        currency_id = self.journal.currency and self.journal.currency.id or self.journal.company_id.currency_id.id
        company_currency = self.journal.company_id.currency_id.id

        fact = self.env.context.get('amount_total')
        c1 = -1 * ((fact / 100) * self.taux.value)
        objc1 = {
             'account_id': self.taux.account.id,
             'period_id': self.periode.id,
             'journal_id': self.journal.id,
             'date': datetime.datetime.today(),
             'name': self.libel,
             'debit': 0.0,
             'partner_id':self.env.context.get('partner'),
             'credit': 1 * fact * (self.taux.value / 100),
             'state': 'valid',
         }
        moveline.append((0,0,objc1))
        objd = {
            'account_id': self.env.context.get('account_id'),
            'period_id': self.periode.id,
            'journal_id': self.journal.id,
            'date': datetime.datetime.today(),
            'name': self.libel,
            'partner_id': self.env.context.get('partner'),
            'debit': 1 * fact * (self.taux.value / 100),
            'credit': 0.0,
            'state': 'valid',
        }
        moveline.append((0,0,objd))
        move = {
            'ref': self.reference,
            'period_id':self.periode.id,
            'journal_id':self.journal.id,
            'date':datetime.datetime.today(),
            'state':'draft',
            'name':'/',
            'line_id':moveline
        }

        vouch = {
            'partner_id': self.env.context.get('partner'),
            'date': datetime.datetime.today(),
            'amount': fact * (self.taux.value / 100),
            'journal_id' : self.journal.id,
            'payement_option' : 'without_writeoff',
            'line_dr_ids':dr,
            'line_cr_ids':cr,
        }
        self.env['account.move'].create(move)
        
