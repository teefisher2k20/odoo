{
    'name': 'External Data Source Connector',
    'version': '1.0',
    'summary': 'Connect to MySQL, MSSQL, Google Sheets, and Excel',
    'description': """
        This module allows Odoo to connect to external data sources including:
        - MySQL
        - Microsoft SQL Server
        - Google Sheets
        - Excel Files (Upload)

        It provides a connection manager and a viewer to test connections.
    """,
    'category': 'Tools',
    'author': 'Jules',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/external_connection_views.xml',
        'wizards/external_selector_views.xml',
        'views/external_connector_menus.xml',
    ],
    'installable': True,
    'application': True,
}
