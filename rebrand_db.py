
import odoo
from odoo import api, fields, models, SUPERUSER_ID

def run_script():
    config_file = 'odoo_local.conf'
    odoo.tools.config.parse_config(['-c', config_file])
    db_name = odoo.tools.config['db_name'] or 'odoo'
    
    registry = odoo.registry(db_name)
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print(f"Updating database: {db_name}")

        # Update SystemBot (OdooBot)
        cr.execute("UPDATE res_partner SET name = 'SystemBot' WHERE name = 'OdooBot'")
        cr.execute("UPDATE res_users SET login = 'systembot' WHERE login = 'odoobot'")
        
        # Update mail messages
        cr.execute("UPDATE mail_message SET body = REPLACE(body, 'Install Odoo', 'Install System') WHERE body LIKE '%Install Odoo%'")
        cr.execute("UPDATE mail_message SET body = REPLACE(body, 'OdooBot', 'SystemBot') WHERE body LIKE '%OdooBot%'")
        
        # Check for ir_translation table
        cr.execute("SELECT count(*) FROM information_schema.tables WHERE table_name = 'ir_translation'")
        if cr.fetchone()[0] > 0:
            print("Updating ir_translation table...")
            # Update values
            cr.execute("UPDATE ir_translation SET value = REPLACE(value, 'Odoo', 'System') WHERE value LIKE '%Odoo%'")
            cr.execute("UPDATE ir_translation SET src = REPLACE(src, 'Odoo', 'System') WHERE src LIKE '%Odoo%'")
            
            # Specific common strings
            cr.execute("UPDATE ir_translation SET value = 'My Account' WHERE value = 'My Odoo.com account'")
            cr.execute("UPDATE ir_translation SET value = 'Install System' WHERE value = 'Install Odoo'")
        
        # Clear JS/CSS assets cache
        print("Clearing assets cache...")
        cr.execute("DELETE FROM ir_attachment WHERE name LIKE '/web/content/%'")
        
        cr.commit()
        print("Done!")

if __name__ == "__main__":
    run_script()
