@echo off
echo Fixing 'odoo' user in PostgreSQL...
echo You will be prompted for the 'postgres' user password (the one you set during installation).
echo.

echo Attempting to create user 'odoo'...
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -c "CREATE USER odoo WITH PASSWORD 'odoo' CREATEDB;"

if %errorlevel% neq 0 (
    echo.
    echo User creation failed (probably already exists). 
    echo Attempting to reset password for 'odoo' user...
    "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -c "ALTER USER odoo WITH PASSWORD 'odoo' CREATEDB;"
)

echo.
echo Done. If you saw "ALTER ROLE" or "CREATE ROLE", it succeeded.
pause
