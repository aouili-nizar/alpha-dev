# -*- coding: utf-8 -*-
{
    'name': "cand_form_edit",

    'summary': """
        ajout badge , adresse map dans candidature """,

    'description': """
        Long description of module's purpose
    """,

    'author': "aouili nizar-alpha engineering",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_recruitment'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}