@echo off
echo Creating 'odoo' user in PostgreSQL...
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -c "CREATE USER odoo WITH PASSWORD 'odoo' CREATEDB;"
if %errorlevel% neq 0 (
    echo Failed to create user. Please check if the password is correct and PostgreSQL is running.
) else (
    echo User 'odoo' created successfully.
)
pause
