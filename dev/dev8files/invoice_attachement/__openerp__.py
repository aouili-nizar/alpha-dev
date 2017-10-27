# -*- coding: utf-8 -*-
{
    'name': "invoice_attachement",

    'summary': """
        """,

    'description': """
       add attachement to : invoice ,employee 
    """,

    'author': "alpha - engineering",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'employee.xml',
        'sale_order.xml',
        'incoice.xml',
        #'quotation.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo.xml',
    ],
}