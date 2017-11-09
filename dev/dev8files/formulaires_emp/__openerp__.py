# -*- coding: utf-8 -*-
{
    'name': "alpha_header",

    'summary': """
       entéte alpha""",

    'description': """
        
    """,

    'author': "Aouili nizar - Alpha engineering",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','devplus_hr_payroll_tn'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'reportxml/special_header.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo.xml',
    ],
}