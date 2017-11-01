# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import float_compare
from openerp.report import report_sxw
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

    @api.v7
    def _paid_amount_in_company_currency(self, cr, uid, ids, name, args, context=None):
        if context is None:
            context = {}
        res = {}
        ctx = context.copy()
        for v in self.browse(cr, uid, ids, context=context):
            ctx.update({'date': v.date})
            #make a new call to browse in order to have the right date in the context, to get the right currency rate
            voucher = self.browse(cr, uid, v.id, context=ctx)
            ctx.update({
                'voucher_special_currency': voucher.payment_rate_currency_id and voucher.payment_rate_currency_id.id or False,
                'voucher_special_currency_rate': voucher.currency_id.rate * voucher.payment_rate, })
            res[voucher.id] = self.pool.get('res.currency').compute(
                cr, uid, voucher.currency_id.id, voucher.company_id.currency_id.id, voucher.net, context=ctx)
        print 'hi here net got called'
        return res
    def compute_ret(self):
        return 0
    taux = fields.Many2one('taux_rs',string="Taux")
    ret_val = fields.Float('Valeur de retenue' ,digits=(12,3),default=compute_ret,store=True)
    net = fields.Float('Net a payé ',store=True,digits=(12,3))
    ftimbre = fields.Float('Timbre fiscal', store=True, digits=(12, 3))

    @api.onchange('taux')
    def change_ret(self):
        for vouchers in self:
            if vouchers.taux:
                ret_val = ((vouchers.amount - vouchers.ftimbre)  / 100 ) * self.env['taux_rs'].search([('code','=',vouchers.taux.code)]).value
                print (vouchers.amount - vouchers.ftimbre)
                print ret_val
                vouchers.update({
                    'ret_val':ret_val,
                    'net': vouchers.amount - ret_val
                })
            else:
                vouchers.update({

                    'ret_val':0,
                    'net': vouchers.amount 
                })

    @api.v7
    def res_move_line_get(self, cr, uid, voucher_id, move_id, company_currency, current_currency, context=None):
        voucher = self.pool.get('account.voucher').browse(cr,uid,voucher_id,context)
        debit = credit = 0.0
        if voucher.type in ('purchase', 'payment'):
            credit = voucher.ret_val
        elif voucher.type in ('sale', 'receipt'):
            debit = voucher.ret_val
        if debit < 0:
            credit = -debit
            debit = 0.0
        if credit < 0:
            debit = -credit
            credit = 0.0
        sign = debit - credit < 0 and -1 or 1
        move_line = {
            'name': '/retenue a la source',
            'debit': debit,
            'credit': credit,
            'account_id': voucher.taux.account.id,
            'move_id': move_id,
            'journal_id': voucher.journal_id.id,
            'period_id': voucher.period_id.id,
            'partner_id': voucher.partner_id.id,
            'currency_id': company_currency <> current_currency and current_currency or False,
            'amount_currency': (sign * abs(voucher.amount)  # amount < 0 for refunds
                                    if company_currency != current_currency else 0.0),
            'date': voucher.date,
            'date_maturity': voucher.date_due
        }
        print move_line
        return move_line
    #overrriding the original move line first 
    @api.v7
    def first_move_line_get(self, cr, uid, voucher_id, move_id, company_currency, current_currency, context=None):
        '''
        Return a dict to be use to create the first account move line of given voucher.

        :param voucher_id: Id of voucher what we are creating account_move.
        :param move_id: Id of account move where this line will be added.
        :param company_currency: id of currency of the company to which the voucher belong
        :param current_currency: id of currency of the voucher
        :return: mapping between fieldname and value of account move line to create
        :rtype: dict
        '''
        print ' -------------------------------- here we found the first move -------------------- '
        voucher = self.pool.get('account.voucher').browse(
            cr, uid, voucher_id, context)
        debit = credit = 0.0
        # TODO: is there any other alternative then the voucher type ??
        # ANSWER: We can have payment and receipt "In Advance".
        # TODO: Make this logic available.
        # -for sale, purchase we have but for the payment and receipt we do not have as based on the bank/cash journal we can not know its payment or receipt
        if voucher.type in ('purchase', 'payment'):
            credit = voucher.net
        elif voucher.type in ('sale', 'receipt'):
            debit = voucher.net
        if debit < 0:
            credit = -debit
            debit = 0.0
        if credit < 0:
            debit = -credit
            credit = 0.0
        sign = debit - credit < 0 and -1 or 1
        #set the first line of the voucher
        move_line = {
            'name': voucher.name or '/',
            'debit': debit,
            'credit': credit,
            'account_id': voucher.account_id.id,
            'move_id': move_id,
            'journal_id': voucher.journal_id.id,
            'period_id': voucher.period_id.id,
            'partner_id': voucher.partner_id.id,
            'currency_id': company_currency <> current_currency and current_currency or False,
            'amount_currency': (sign * abs(voucher.amount)  # amount < 0 for refunds
                                    if company_currency != current_currency else 0.0),
            'date': voucher.date,
            'date_maturity': voucher.date_due
        }
        print move_line
        return move_line

    def voucher_move_line_create(self, cr, uid, voucher_id, line_total, move_id, company_currency, current_currency, context=None):
        '''
        Create one account move line, on the given account move, per voucher line where amount is not 0.0.
        It returns Tuple with tot_line what is total of difference between debit and credit and
        a list of lists with ids to be reconciled with this format (total_deb_cred,list_of_lists).

        :param voucher_id: Voucher id what we are working with
        :param line_total: Amount of the first line, which correspond to the amount we should totally split among all voucher lines.
        :param move_id: Account move wher those lines will be joined.
        :param company_currency: id of currency of the company to which the voucher belong
        :param current_currency: id of currency of the voucher
        :return: Tuple build as (remaining amount not allocated on voucher lines, list of account_move_line created in this method)
        :rtype: tuple(float, list of int)
        '''
        print '----------------------------------------- me voucher line create ----------------------'
        if context is None:
            context = {}
        move_line_obj = self.pool.get('account.move.line')
        currency_obj = self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        print 'tot line first occurence of tot line-------------------------'
        tot_line = line_total
        print tot_line
        rec_lst_ids = []

        date = self.read(cr, uid, [voucher_id], [
                         'date'], context=context)[0]['date']
        ctx = context.copy()
        ctx.update({'date': date})
        voucher = self.pool.get('account.voucher').browse(
            cr, uid, voucher_id, context=ctx)
        voucher_currency = voucher.journal_id.currency or voucher.company_id.currency_id
        ctx.update({
            'voucher_special_currency_rate': voucher_currency.rate * voucher.payment_rate,
            'voucher_special_currency': voucher.payment_rate_currency_id and voucher.payment_rate_currency_id.id or False, })
        prec = self.pool.get('decimal.precision').precision_get(
            cr, uid, 'Account')
        for line in voucher.line_ids:
            #create one move line per voucher line where amount is not 0.0
            # AND (second part of the clause) only if the original move line was not having debit = credit = 0 (which is a legal value)
            if not line.amount and not (line.move_line_id and not float_compare(line.move_line_id.debit, line.move_line_id.credit, precision_digits=prec) and not float_compare(line.move_line_id.debit, 0.0, precision_digits=prec)):
                continue
            # convert the amount set on the voucher line into the currency of the voucher's company
            # this calls res_curreny.compute() with the right context, so that it will take either the rate on the voucher if it is relevant or will use the default behaviour
            amount = self._convert_amount(
                cr, uid,  line.amount, voucher.id, context=ctx)
            # if the amount encoded in voucher is equal to the amount unreconciled, we need to compute the
            # currency rate difference
            if line.amount == line.amount_unreconciled:
                if not line.move_line_id:
                    raise osv.except_osv(_('Wrong voucher line'), _(
                        "The invoice you are willing to pay is not valid anymore."))
                sign = line.type == 'dr' and -1 or 1
                currency_rate_difference = sign * \
                    (line.move_line_id.amount_residual - amount)
            else:
                currency_rate_difference = 0.0
            move_line = {
                'journal_id': voucher.journal_id.id,
                'period_id': voucher.period_id.id,
                'name': line.name or '/',
                'account_id': line.account_id.id,
                'move_id': move_id,
                'partner_id': voucher.partner_id.id,
                'currency_id': line.move_line_id and (company_currency <> line.move_line_id.currency_id.id and line.move_line_id.currency_id.id) or False,
                'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
                'quantity': 1,
                'credit': 0.0,
                'debit': 0.0,
                'date': voucher.date
            }
            print '------------------------- voucher line create first move ---------------'
            print move_line
            if amount < 0:
                amount = -amount
                if line.type == 'dr':
                    line.type = 'cr'
                else:
                    line.type = 'dr'

            if (line.type == 'dr'):
                tot_line += amount
                print 'tot line second occurence  tot line += amount'
                print tot_line
                print amount 
                move_line['debit'] = amount
            else:
                tot_line -= amount
                move_line['credit'] = amount
                print '-------------- normally here totline - amount '
                print tot_line
                print '-----------------------this is the aùmount '
                print amount
            if voucher.tax_id and voucher.type in ('sale', 'purchase'):
                move_line.update({
                    'account_tax_id': voucher.tax_id.id,
                })
            print '------------------------- voucher line create first move ---------------'
            print move_line
            # compute the amount in foreign currency
            foreign_currency_diff = 0.0
            amount_currency = False
            if line.move_line_id:
                # We want to set it on the account move line as soon as the original line had a foreign currency
                if line.move_line_id.currency_id and line.move_line_id.currency_id.id != company_currency:
                    # we compute the amount in that foreign currency.
                    if line.move_line_id.currency_id.id == current_currency:
                        # if the voucher and the voucher line share the same currency, there is no computation to do
                        sign = (move_line['debit'] -
                                move_line['credit']) < 0 and -1 or 1
                        amount_currency = sign * (line.amount)
                    else:
                        # if the rate is specified on the voucher, it will be used thanks to the special keys in the context
                        # otherwise we use the rates of the system
                        amount_currency = currency_obj.compute(
                            cr, uid, company_currency, line.move_line_id.currency_id.id, move_line['debit'] - move_line['credit'], context=ctx)
                if line.amount == line.amount_unreconciled:
                    foreign_currency_diff = line.move_line_id.amount_residual_currency - \
                        abs(amount_currency)

            move_line['amount_currency'] = amount_currency
            voucher_line = move_line_obj.create(cr, uid, move_line)
            rec_ids = [voucher_line, line.move_line_id.id]

            if not currency_obj.is_zero(cr, uid, voucher.company_id.currency_id, currency_rate_difference):
                # Change difference entry in company currency
                exch_lines = self._get_exchange_lines(
                    cr, uid, line, move_id, currency_rate_difference, company_currency, current_currency, context=context)
                new_id = move_line_obj.create(cr, uid, exch_lines[0], context)
                move_line_obj.create(cr, uid, exch_lines[1], context)
                rec_ids.append(new_id)

            if line.move_line_id and line.move_line_id.currency_id and not currency_obj.is_zero(cr, uid, line.move_line_id.currency_id, foreign_currency_diff):
                # Change difference entry in voucher currency
                move_line_foreign_currency = {
                    'journal_id': line.voucher_id.journal_id.id,
                    'period_id': line.voucher_id.period_id.id,
                    'name': _('change') + ': ' + (line.name or '/'),
                    'account_id': line.account_id.id,
                    'move_id': move_id,
                    'partner_id': line.voucher_id.partner_id.id,
                    'currency_id': line.move_line_id.currency_id.id,
                    'amount_currency': (-1 if line.type == 'cr' else 1) * foreign_currency_diff,
                    'quantity': 1,
                    'credit': 0.0,
                    'debit': 0.0,
                    'date': line.voucher_id.date,
                }
                print '-----------------------the second move mline ------------------'
                print move_line_foreign_currency
                new_id = move_line_obj.create(
                    cr, uid, move_line_foreign_currency, context=context)
                rec_ids.append(new_id)
            if line.move_line_id.id:
                rec_lst_ids.append(rec_ids)
        print '------------------------------- tot line + rec lst ids '
        print tot_line
        print rec_lst_ids
        return (tot_line, rec_lst_ids)
    #create the retenue a la source 

    
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
        print ' im the account move '
        print move_pool
        move_line_pool = self.pool.get('account.move.line')
        print 'im the move line pool '
        print move_line_pool
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
            move_line_res_id = move_line_pool.create(cr,uid,self.res_move_line_get(cr,uid,voucher.id,move_id,company_currency,current_currency,local_context),local_context)
            move_line_res_brw = move_line_pool.browse(
                cr, uid, move_line_res_id, context=context)
            move_line_brw = move_line_pool.browse(
                cr, uid, move_line_id, context=context)
            line_total = (move_line_brw.debit - move_line_brw.credit) + (move_line_res_brw.debit - move_line_res_brw.credit)
            rec_list_ids = []
            if voucher.type == 'sale':
                line_total = line_total - \
                    self._convert_amount(
                        cr, uid, voucher.tax_amount, voucher.id, context=ctx)
                print line_total
            elif voucher.type == 'purchase':
                line_total = line_total + \
                    self._convert_amount(
                        cr, uid, voucher.tax_amount, voucher.id, context=ctx)
                print line_total
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

