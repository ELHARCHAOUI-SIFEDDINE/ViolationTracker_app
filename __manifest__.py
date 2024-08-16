# -*- coding: utf-8 -*-
{
    'name': "Bilan mensuel",  # The name of the module
    'summary': """
        Ajoute une formulaire de génération de bilan mensuel détaillé.""",  # A brief summary of the module's purpose
    'description': """
        Ce module ajoute une formulaire à Odoo pour générer un bilan mensuel détaillé, 
        fournissant un aperçu complet des activités et des transactions sur une base mensuelle.""",  # A detailed description of the module
    'author': "Oussama Ben Mchiche",  # The author of the module
    'category': '',  # The category under which the module falls
    'version': '1.0',  # The version of the module
    'depends': ['base', 'web', 'multi_branch_base'],  # The dependencies that this module requires to work properly
    'data': [  # List of data files that are loaded in a specific order
        'security/ir.model.access.csv',  # Security access control file
        'security/security.xml',  # Security rules file
        'views/menu.xml',  # Menu definitions
        'views/bilan.xml',  # View definitions for the 'bilan' model
        'report/report_bilan_template.xml',  # Report templates
        'wizard/bilan_report_wizard_view.xml'  # Wizard view definitions
    ],
    'demo': [  # List of demo data files (usually empty for production modules)
        # No demo data files specified
    ],
    'installable': True,  # Specifies whether the module can be installed
    'application': True,  # Specifies whether the module should be considered as a standalone application
    'auto_install': False,  # Specifies whether the module should be automatically installed if its dependencies are met
}
