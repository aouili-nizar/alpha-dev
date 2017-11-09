# -*- coding: utf-8 -*-
# Copyright 2009-2016 Noviat
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import xlwt
from datetime import datetime
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import rowcol_to_cell
from openerp.addons.account_financial_report_webkit.report.general_ledger \
    import GeneralLedgerWebkit
from openerp.tools.translate import _
# import logging
# _logger = logging.getLogger(__name__)

_column_sizes = [
    ('matricule', 12),
    ('name', 30),
    ('regime', 20),
    ('salaire_base', 15),
    ('salaire_brut', 15),
    ('retenu_cnss', 15),
    ('salaire_imposable', 15),
    ('irpp', 15),
    ('salaire_net', 15),
    ('avance_pret', 15),
    ('net_paye', 15),
]

class journal_xls(report_xls):
    column_sizes = [x[1] for x in _column_sizes]
    
    def generate_xls_report(self, _p, _xs, data, objects, wb):
        
        ws = wb.add_sheet(_p.report_name[:31])
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0
        
        # set print header/footer
        ws.header_str = self.xls_headers['standard']
        ws.footer_str = self.xls_footers['standard']

        # cf. account_report_general_ledger.mako
        initial_balance_text = {'initial_balance': _('Computed'),
                                'opening_balance': _('Opening Entries'),
                                False: _('No')}

        # Title
        cell_style = xlwt.easyxf(_xs['xls_title'])
        report_name = ' - '.join([_p.report_name.upper(),
                                 _p.company.partner_id.name,
                                 _p.company.currency_id.name])
        c_specs = [
            ('report_name', 1, 0, 'text', report_name),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        # write empty row to define column sizes
        c_sizes = self.column_sizes
        c_specs = [('empty%s' % i, 1, c_sizes[i], 'text', None)
                   for i in range(0, len(c_sizes))]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, set_column_size=True)
        
        # Header Table
        cell_format = _xs['bold'] + _xs['fill_blue'] + _xs['borders_all']
        cell_style = xlwt.easyxf(cell_format)
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])
        c_specs = [
            ('coa', 2, 0, 'text', _('Chart of Account')),
            ('fy', 1, 0, 'text', _('Fiscal Year')),
            ('df', 3, 0, 'text', _p.filter_form(data) ==
             'filter_date' and _('Dates Filter') or _('Periods Filter')),
            ('af', 1, 0, 'text', _('Accounts Filter')),
            ('tm', 2, 0, 'text', _('Target Moves')),
            ('ib', 2, 0, 'text', _('Initial Balance')),

        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style_center)
        
        cell_format = _xs['borders_all']
        cell_style = xlwt.easyxf(cell_format)
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])
        c_specs = [
            ('coa', 2, 0, 'text', _p.journal.name),
            ('fy', 1, 0, 'text', _p.fiscalyear.name if _p.fiscalyear else '-'),
        ]
        df = _('From') + ': '
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style_center)
        ws.set_horz_split_pos(row_pos)
        row_pos += 1
        # Column Title Row
        cell_format = _xs['bold']
        c_title_cell_style = xlwt.easyxf(cell_format)

        # Column Header Row
        cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
        c_hdr_cell_style = xlwt.easyxf(cell_format)
        c_hdr_cell_style_right = xlwt.easyxf(cell_format + _xs['right'])
        c_hdr_cell_style_center = xlwt.easyxf(cell_format + _xs['center'])
        c_hdr_cell_style_decimal = xlwt.easyxf(
            cell_format + _xs['right'],
            num_format_str=report_xls.decimal_format)
        # Column Initial Balance Row
        cell_format = _xs['italic'] + _xs['borders_all']
        c_init_cell_style = xlwt.easyxf(cell_format)
        c_init_cell_style_decimal = xlwt.easyxf(
            cell_format + _xs['right'],
            num_format_str=report_xls.decimal_format)
        
        c_specs = [
            ('matricule', 1, 0, 'text', _('Matricule'), None, c_hdr_cell_style),
            ('name', 1, 0, 'text', _('Entry'), None, c_hdr_cell_style),
            ('regime', 1, 0, 'text', _('Journal'), None, c_hdr_cell_style),
            ('salaire_base', 1, 0, 'text', _('Salaire Base'), None, c_hdr_cell_style_right),
            ('salaire_brut', 1, 0, 'text', _('Salaire Brut'), None, c_hdr_cell_style_right),
            ('retenu_cnss', 1, 0, 'text', _('Retenu CNSS'), None, c_hdr_cell_style_right),
            ('salaire_imposable', 1, 0, 'text', _('Salaire Imposable'), None, c_hdr_cell_style_right),
            ('irpp', 1, 0, 'text', _('IRPP'), None, c_hdr_cell_style_right),
            ('avance_pret', 1, 0, _('Avance et Pret'), None, c_hdr_cell_style_right),
            ('net_paye', 1, 0, 'text', _(u'Net à payer'), None, c_hdr_cell_style_right),
          
        ]
        
        c_hdr_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])

        # cell styles for ledger lines
        ll_cell_format = _xs['borders_all']
        ll_cell_style = xlwt.easyxf(ll_cell_format)
        ll_cell_style_center = xlwt.easyxf(ll_cell_format + _xs['center'])
        ll_cell_style_date = xlwt.easyxf(
            ll_cell_format + _xs['left'],
            num_format_str=report_xls.date_format)
        ll_cell_style_decimal = xlwt.easyxf(
            ll_cell_format + _xs['right'],
            num_format_str=report_xls.decimal_format)
        
        cnt = 0
        for account in objects:

            display_initial_balance = _p['init_balance'][account.id] and \
                (_p['init_balance'][account.id].get(
                    'debit', 0.0) != 0.0 or
                    _p['init_balance'][account.id].get('credit', 0.0) != 0.0)
            display_ledger_lines = _p['ledger_lines'][account.id]
            
            if _p.display_account_raw(data) == 'all' or \
                    (display_ledger_lines or display_initial_balance):
                # TO DO : replace cumul amounts by xls formulas
                cnt += 1
                cumul_debit = 0.0
                cumul_credit = 0.0
                cumul_balance = 0.0
                cumul_balance_curr = 0.0
                c_specs = [
                    ('acc_title', 11, 0, 'text',
                     ' - '.join([account.code, account.name])),
                ]
                row_data = self.xls_row_template(
                    c_specs, [x[0] for x in c_specs])
                row_pos = self.xls_write_row(
                    ws, row_pos, row_data, c_title_cell_style)
                row_pos = self.xls_write_row(ws, row_pos, c_hdr_data)
                row_start = row_pos
                
                if display_initial_balance:
                    init_balance = _p['init_balance'][account.id]
                    cumul_debit = init_balance.get('debit') or 0.0
                    cumul_credit = init_balance.get('credit') or 0.0
                    cumul_balance = init_balance.get('init_balance') or 0.0
                    cumul_balance_curr = init_balance.get(
                        'init_balance_currency') or 0.0
                    c_specs = [('empty%s' % x, 1, 0, 'text', None)
                               for x in range(7)]
                    c_specs += [
                        ('init_bal', 1, 0, 'text', _('Initial Balance')),
                        ('counterpart', 1, 0, 'text', None),
                        ('debit', 1, 0, 'number', cumul_debit,
                         None, c_init_cell_style_decimal),
                        ('credit', 1, 0, 'number', cumul_credit,
                         None, c_init_cell_style_decimal),
                        ('cumul_bal', 1, 0, 'number', cumul_balance,
                         None, c_init_cell_style_decimal),
                    ]
                    if _p.amount_currency(data):
                        c_specs += [
                            ('curr_bal', 1, 0, 'number', cumul_balance_curr,
                             None, c_init_cell_style_decimal),
                            ('curr_code', 1, 0, 'text', None),
                        ]
                    row_data = self.xls_row_template(
                        c_specs, [x[0] for x in c_specs])
                    row_pos = self.xls_write_row(
                        ws, row_pos, row_data, c_init_cell_style)
                for line in _p['ledger_lines'][account.id]:
            
        

        