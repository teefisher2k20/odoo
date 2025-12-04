# -*- coding: utf-8 -*-
{
    'name': 'My Custom Logo',
    'version': '1.0',
    'category': 'Customization',
    'summary': 'Replace Odoo logo with custom logo',
    'description': 'This module replaces the default Odoo logo with a custom one.',
    'depends': ['base'],
    'data': [
        'data/logo.xml',
    ],
    'installable': True,
    'application': False,
}