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
class wizard_res_four(models.Model):
    _inherit="account.voucher"

    def compute_ret(self):
        return 0
    taux = fields.Many2one('taux_rs', required=True,string="Taux")
    ret_val = fields.Float('Valeur de retenue' , readonly=True,compute=compute_ret)
    net = fields.Float('Net a payé ')
    #override the original voucher create method
    @api.v7
    def action_move_line_create(self, cr, uid, ids, context=None):
        '''
        Confirm the vouchers given in ids and create the journal entries for each of them
        '''
        print 'hi im the overrided method haha ^_^'
        if context is None:
            context = {}
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        for voucher in self.browse(cr, uid, ids, context=context):
            local_context = dict(
                context, force_company=voucher.journal_id.company_id.id)
            if voucher.move_id:
                continue
            company_currency = self._get_company_currency(
                cr, uid, voucher.id, context)
            current_currency = self._get_current_currency(
                cr, uid, voucher.id, context)
            # we select the context to use accordingly if it's a multicurrency case or not
            context = self._sel_context(cr, uid, voucher.id, context)
            # But for the operations made by _convert_amount, we always need to give the date in the context
            ctx = context.copy()
            ctx.update({'date': voucher.date})
            # Create the account move record.
            move_id = move_pool.create(cr, uid, self.account_move_get(
                cr, uid, voucher.id, context=context), context=context)
            # Get the name of the account_move just created
            name = move_pool.browse(cr, uid, move_id, context=context).name
            # Create the first line of the voucher
            move_line_id = move_line_pool.create(cr, uid, self.first_move_line_get(
                cr, uid, voucher.id, move_id, company_currency, current_currency, local_context), local_context)
            move_line_brw = move_line_pool.browse(
                cr, uid, move_line_id, context=context)
            line_total = move_line_brw.debit - move_line_brw.credit
            rec_list_ids = []
            if voucher.type == 'sale':
                line_total = line_total - \
                    self._convert_amount(
                        cr, uid, voucher.tax_amount, voucher.id, context=ctx)
            elif voucher.type == 'purchase':
                line_total = line_total + \
                    self._convert_amount(
                        cr, uid, voucher.tax_amount, voucher.id, context=ctx)
            # Create one move line per voucher line where amount is not 0.0
            line_total, rec_list_ids = self.voucher_move_line_create(
                cr, uid, voucher.id, line_total, move_id, company_currency, current_currency, context)

            # Create the writeoff line if needed
            ml_writeoff = self.writeoff_move_line_get(
                cr, uid, voucher.id, line_total, move_id, name, company_currency, current_currency, local_context)
            if ml_writeoff:
                move_line_pool.create(cr, uid, ml_writeoff, local_context)
            # We post the voucher.
            self.write(cr, uid, [voucher.id], {
                'move_id': move_id,
                'state': 'posted',
                'number': name,
            })
            if voucher.journal_id.entry_posted:
                move_pool.post(cr, uid, [move_id], context={})
            # We automatically reconcile the account move lines.
            reconcile = False
            for rec_ids in rec_list_ids:
                if len(rec_ids) >= 2:
                    reconcile = move_line_pool.reconcile_partial(
                        cr, uid, rec_ids, writeoff_acc_id=voucher.writeoff_acc_id.id, writeoff_period_id=voucher.period_id.id, writeoff_journal_id=voucher.journal_id.id)
        return True

