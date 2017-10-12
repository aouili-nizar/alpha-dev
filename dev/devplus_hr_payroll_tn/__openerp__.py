# -*- encoding: utf-8 -*-
#----------------------------------------------------------------------------
#
#
#----------------------------------------------------------------------------

{
    "name": "Paie-Tunisienne",
    "version": "1.0",
    "depends": ['base', 'hr', 'hr_contract', 'hr_holidays', 'account','devplus_report_style'],
    "author": "Alpha engineernig",
    "category": "training",
    "description": """
    This module provide :



    """,
    "init_xml": [],
    'data': [
             'security/payroll_security.xml',
             'security/ir.model.access.csv',
             'data/hr_payroll_tn_data.xml',

#              'view/hr_payroll_menuitem.xml',
#              'view/hr_view.xml',
#              'view/hr_payroll_config_view.xml',
#              'view/hr_infraction.xml',
#              'view/hr_autorisation_view.xml',
#              'view/hr_payroll_rubriques_view.xml',
#              'view/hr_payroll_tn_view.xml',
#              'view/hr_avance_view.xml',
#              'view/hr_pointage_view.xml',
             'view/hr_payroll_menuitem.xml',
             'view/hr_view.xml',
             'view/hr_payroll_config_view.xml',
             'view/hr_payroll_rubriques_view.xml',
             'view/hr_payroll_tn_view.xml',
             'view/hr_infraction_view.xml',
             'view/hr_autorisation_view.xml',
             'view/hr_avance_view.xml',
             'view/hr_pointage_view.xml',
             'view/hr_payroll_inverse_view.xml',
             'view/res_company.xml',


            'wizard/wizard_journal_paie_view.xml',
            'wizard/wizard_declaration_employer.xml',
            'wizard/wizard_ordre_virement.xml',

            'views/report_bulletin.xml',
            'views/report_journal_paie.xml',
            'views/report_declaration_employer.xml',
            'views/report_ordre_virement.xml',
            'views/report.xml',
],


    'demo_xml': [],
    'installable': True,
    'active' : False,

#    'certificate': 'certificate',
}
