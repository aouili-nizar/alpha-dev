# -*- encoding: utf-8 -*-
#----------------------------------------------------------------------------
#
#
#----------------------------------------------------------------------------

{
    "name": "Declaration_cnss_Tunisienne",
    "version": "1.0",
    "depends": ['base', 'hr', 'hr_contract', 'hr_holidays', 'account','devplus_report_style','devplus_hr_payroll_tn'],
    "author": "Alpha engineernig",
    "category": "training",
    "description": """
    This module provide :



    """,
    "init_xml": [],
    'data': [
            
            'wizard/wizard_declaration_cnss_view.xml',         
            'views/report_declaration_cnss.xml',
            'views/report_recapitulatif_cnss.xml',
            'views/report.xml',
            'views/res_company.xml'
           
],


    'demo_xml': [],
    'installable': True,
    'active' : False,

#    'certificate': 'certificate',
}
