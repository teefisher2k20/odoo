#!/usr/bin/env python3
# Script to update all modules to set to_buy=False

import sys
sys.path.insert(0, '.')

import odoo
from odoo import api, SUPERUSER_ID

# Configuration
DB_NAME = 'odoo'
CONFIG_FILE = 'odoo_local.conf'

# Load Odoo configuration
odoo.tools.config.parse_config(['-c', CONFIG_FILE])

# Connect to database
with odoo.api.Environment.manage():
    registry = odoo.registry(DB_NAME)
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Find all modules with to_buy=True
        modules = env['ir.module.module'].search([('to_buy', '=', True)])
        
        print(f"Found {len(modules)} modules with to_buy=True")
        print("Updating modules:")
        for module in modules:
            print(f"  - {module.name}: {module.shortdesc}")
        
        # Update all modules to set to_buy=False
        modules.write({'to_buy': False})
        
        # Commit the changes
        cr.commit()
        
        print(f"\nSuccessfully updated {len(modules)} modules!")
        print("All modules now have to_buy=False")
