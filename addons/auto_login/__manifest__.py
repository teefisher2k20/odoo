{
    'name': 'Auto Login & Clean Interface',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Auto-login as admin and remove branding',
    'description': """
        Automatically logs in as admin user on local development.
        Removes Odoo branding from login screen.
    """,
    'depends': ['web'],
    'data': [
        'views/login_templates.xml',
    ],
    'installable': True,
    'auto_install': True,
}
