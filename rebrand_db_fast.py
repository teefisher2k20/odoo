
import psycopg2
import configparser

def run_script():
    config = configparser.ConfigParser()
    config.read('odoo_local.conf')
    
    db_name = config.get('options', 'db_name', fallback='odoo')
    db_user = config.get('options', 'db_user', fallback='odoo')
    db_password = config.get('options', 'db_password', fallback='odoo')
    db_host = config.get('options', 'db_host', fallback='127.0.0.1')
    db_port = config.get('options', 'db_port', fallback='5432')
    
    print(f"Connecting to database: {db_name}")
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.autocommit = True
    cur = conn.cursor()

    try:
        print("Updating SystemBot (OdooBot)...")
        cur.execute("UPDATE res_partner SET name = 'SystemBot' WHERE name = 'OdooBot'")
        cur.execute("UPDATE res_users SET login = 'systembot' WHERE login = 'odoobot'")
        
        print("Updating mail messages...")
        cur.execute("UPDATE mail_message SET body = REPLACE(body, 'Install Odoo', 'Install System') WHERE body LIKE '%Install Odoo%'")
        cur.execute("UPDATE mail_message SET body = REPLACE(body, 'OdooBot', 'SystemBot') WHERE body LIKE '%OdooBot%'")
        
        # Check for ir_translation table (Old Odoo version or translations)
        cur.execute("SELECT count(*) FROM information_schema.tables WHERE table_name = 'ir_translation'")
        if cur.fetchone()[0] > 0:
            print("Updating ir_translation table...")
            cur.execute("UPDATE ir_translation SET value = REPLACE(value, 'Odoo', 'System') WHERE value LIKE '%Odoo%'")
            cur.execute("UPDATE ir_translation SET src = REPLACE(src, 'Odoo', 'System') WHERE src LIKE '%Odoo%'")
        
        # In Odoo 17, many fields are jsonb. Let's try to update them with casting.
        tables_to_update = [
            ('ir_ui_menu', 'name'),
            ('ir_act_window', 'name'),
            ('ir_actions', 'name'),
            ('res_groups', 'name'),
        ]
        
        for table, field in tables_to_update:
            try:
                print(f"Checking {table}.{field}...")
                cur.execute(f"SELECT count(*) FROM information_schema.columns WHERE table_name = '{table}' AND column_name = '{field}'")
                if cur.fetchone()[0] > 0:
                    # Check if it is jsonb
                    cur.execute(f"SELECT data_type FROM information_schema.columns WHERE table_name = '{table}' AND column_name = '{field}'")
                    data_type = cur.fetchone()[0]
                    if data_type == 'jsonb':
                        print(f"Updating {table}.{field} (jsonb)...")
                        cur.execute(f"UPDATE {table} SET {field} = REPLACE({field}::text, 'Odoo', 'System')::jsonb WHERE {field}::text LIKE '%Odoo%'")
                    else:
                        print(f"Updating {table}.{field} (text)...")
                        cur.execute(f"UPDATE {table} SET {field} = REPLACE({field}, 'Odoo', 'System') WHERE {field} LIKE '%Odoo%'")
            except Exception as e:
                print(f"Could not update {table}.{field}: {e}")

        # Clear JS/CSS assets cache
        print("Clearing assets cache...")
        cur.execute("DELETE FROM ir_attachment WHERE name LIKE '/web/content/%'")
        
        print("Done!")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    run_script()
