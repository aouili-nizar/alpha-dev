# -*- coding: utf-8 -*-
{
    'name': "emp_form",

    'summary': """
        Attestation de travail , salaire , stage , stage SIVP , certificat de travail """,

    'description': """
        
    """,

    'author': "Alpha engineering",
    'website': "",

    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','devplus_hr_payroll_tn'],

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