@echo off
echo Updating Odoo modules to remove enterprise restrictions...
echo.
echo This will set all modules to to_buy=false in the database.
echo.

set PGPASSWORD=odoo
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U odoo -d odoo -f fix_modules.sql

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: All modules updated successfully!
    echo You can now restart Odoo and all modules will show "Activate" instead of "Upgrade"
) else (
    echo.
    echo ERROR: Failed to update modules. Please check the error above.
)

pause
