# -*- coding: utf-8 -*-
{
    'name': "declaration_fiscale",

    'summary': """
        Declaration fiscale tunisienne""",

    'description': """
        Ce module ajoute la fonctionnalitées d'extraire la declaration fiscale depuis le module comptabilitée
    """,

    'author': "alpha engineering ",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','devplus_hr_payroll_tn'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'templates.xml',
        'views/account_fisc_config.xml',
        'wizard/wizard_declaration_fiscal.xml',
        'reportXml/report_declaration_fiscal.xml',
        'reportXml/report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo.xml',
    ],
}