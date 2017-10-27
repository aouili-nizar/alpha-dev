# -*- coding: utf-8 -*-
{
    'name': "certif_retenue",

    'summary': """
        certifcat de retenue d'impot sur les revenue employés et fournisseur""",

    'description': """
        Ce module ajoute la fonctionnalitées d'extraire la  certifcat de retenue d'impot sur les revenue employés ou fournisseur
    """,

    'author': "alpha engineering ",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'devplus_hr_payroll_tn', 'account', 'account_voucher'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'templates.xml',
        'wizard/wizard_rs_emp.xml',
        'reportXml/report_rs_emp.xml',
        'wizard/wizard_rs_four.xml',
        'reportXml/report_rs_four.xml',
        'reportXml/report.xml',
        'views/res_taux.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo.xml',
    ],
}
