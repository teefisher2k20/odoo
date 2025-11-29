@echo off
echo Starting Odoo Server...
.venv\Scripts\python.exe odoo-bin -c odoo_local.conf
pause
