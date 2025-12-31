import base64
import json
import io
import pandas as pd
from odoo import models, fields, api, _
from odoo.exceptions import UserError

# Import connectors
try:
    import mysql.connector
except ImportError:
    mysql = None

try:
    import pymssql
except ImportError:
    pymssql = None

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    gspread = None

class ExternalConnection(models.Model):
    _name = 'external.connection'
    _description = 'External Database Connection'

    name = fields.Char(string='Connection Name', required=True)
    connection_type = fields.Selection([
        ('mysql', 'MySQL / MariaDB'),
        ('mssql', 'Microsoft SQL Server'),
        ('google_sheets', 'Google Sheets'),
        ('excel', 'Excel File (Upload)'),
    ], string='Type', required=True, default='mysql')

    # Database Fields
    host = fields.Char(string='Host')
    port = fields.Integer(string='Port')
    user = fields.Char(string='User')
    password = fields.Char(string='Password')
    db_name = fields.Char(string='Database Name')

    # Google Sheets Fields
    google_json_key = fields.Text(string='Google Service Account JSON')
    spreadsheet_url = fields.Char(string='Spreadsheet URL')

    # Excel Fields
    excel_file = fields.Binary(string='Excel File')
    excel_filename = fields.Char(string='Filename')

    # --- HELPER METHODS ---
    def _get_google_credentials(self):
        """Helper to get Google credentials from stored JSON."""
        self.ensure_one()
        if not self.google_json_key:
            return None
        try:
            creds_dict = json.loads(self.google_json_key)
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.readonly'
            ]
            return Credentials.from_service_account_info(creds_dict, scopes=scopes)
        except (json.JSONDecodeError, TypeError):
            raise UserError("Invalid Google Service Account JSON key.")

    # --- ACTION METHODS ---
    def test_connection(self):
        self.ensure_one()
        status = False
        message = ""

        try:
            if self.connection_type == 'mysql':
                if not mysql:
                    raise UserError("MySQL driver not installed.")
                conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.db_name,
                    port=self.port
                )
                if conn.is_connected():
                    status = True
                    message = "Successfully connected to MySQL!"
                    conn.close()

            elif self.connection_type == 'mssql':
                if not pymssql:
                    raise UserError("MSSQL driver not installed.")
                conn = pymssql.connect(
                    server=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.db_name,
                    port=self.port or 1433
                )
                status = True
                message = "Successfully connected to MSSQL!"
                conn.close()

            elif self.connection_type == 'google_sheets':
                if not gspread:
                    raise UserError("Google Sheets library not installed.")

                creds = self._get_google_credentials()
                if not creds:
                    raise UserError("Google JSON key is missing or invalid.")

                client = gspread.authorize(creds)

                if self.spreadsheet_url:
                    sheet = client.open_by_url(self.spreadsheet_url)
                    message = f"Successfully connected to Sheet: {sheet.title}"
                else:
                    message = "Authenticated with Google, but no URL provided to test open."
                status = True

            elif self.connection_type == 'excel':
                if not self.excel_file:
                    raise UserError("Please upload a file.")

                file_content = base64.b64decode(self.excel_file)
                df = pd.read_excel(io.BytesIO(file_content))
                message = f"Successfully read Excel file. Columns: {', '.join(df.columns)}"
                status = True

        except Exception as e:
            raise UserError(f"Connection Failed: {str(e)}")

        if status:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': message,
                    'type': 'success',
                    'sticky': False,
                }
            }

    def fetch_preview_data(self, limit=10):
        """Fetches a preview of data (first N rows)"""
        self.ensure_one()
        data = []
        columns = []

        try:
            if self.connection_type == 'mysql':
                conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.db_name,
                    port=self.port
                )
                cursor = conn.cursor()
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                if tables:
                    first_table = tables[0][0]
                    cursor.execute(f"SELECT * FROM {first_table} LIMIT {limit}")
                    columns = [i[0] for i in cursor.description]
                    data = cursor.fetchall()
                conn.close()

            elif self.connection_type == 'mssql':
                conn = pymssql.connect(
                    server=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.db_name,
                    port=self.port or 1433
                )
                cursor = conn.cursor()
                # Get first table
                cursor.execute("SELECT TOP 1 TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
                row = cursor.fetchone()
                if row:
                    table_name = row[0]
                    cursor.execute(f"SELECT TOP {limit} * FROM {table_name}")
                    columns = [i[0] for i in cursor.description]
                    data = cursor.fetchall()
                conn.close()

            elif self.connection_type == 'google_sheets':
                creds = self._get_google_credentials()
                if not creds:
                    raise UserError("Google JSON key is missing or invalid.")
                client = gspread.authorize(creds)
                sheet = client.open_by_url(self.spreadsheet_url).sheet1
                all_values = sheet.get_all_values()
                if all_values:
                    columns = all_values[0]
                    data = all_values[1:limit+1]

            elif self.connection_type == 'excel':
                file_content = base64.b64decode(self.excel_file)
                df = pd.read_excel(io.BytesIO(file_content))
                columns = list(df.columns)
                data = df.head(limit).values.tolist()

        except Exception as e:
            return f"Error: {str(e)}", []

        # Format data for display
        return columns, data
