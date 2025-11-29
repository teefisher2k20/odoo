# PowerShell script to create Odoo database user
$env:PGPASSWORD = "admin"
$psqlPath = "C:\Program Files\PostgreSQL\15\bin\psql.exe"

Write-Host "Attempting to create/fix odoo user in PostgreSQL..." -ForegroundColor Cyan
Write-Host ""

# Try to drop and recreate the user
$command = "DROP USER IF EXISTS odoo; CREATE USER odoo WITH PASSWORD 'odoo' CREATEDB;"

try {
    & $psqlPath -U postgres -c $command 2>&1 | Write-Host
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "SUCCESS: User 'odoo' created successfully!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "First attempt failed. Trying with different postgres password..." -ForegroundColor Yellow
        
        # Try with 'postgres' as password
        $env:PGPASSWORD = "postgres"
        & $psqlPath -U postgres -c $command 2>&1 | Write-Host
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "SUCCESS: User 'odoo' created successfully!" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "ERROR: Could not create user. Please enter your postgres password manually." -ForegroundColor Red
            Write-Host "Run this command in Command Prompt:" -ForegroundColor Yellow
            Write-Host 'fix_db_user.bat' -ForegroundColor White
        }
    }
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# Test the connection
Write-Host ""
Write-Host "Testing connection with odoo user..." -ForegroundColor Cyan
$env:PGPASSWORD = "odoo"
& $psqlPath -U odoo -d postgres -c "SELECT version();" 2>&1 | Select-Object -First 3 | Write-Host

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS: Odoo user can connect to PostgreSQL!" -ForegroundColor Green
    Write-Host "You can now run Odoo with: run_odoo.bat" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "Connection test failed. Please check the setup." -ForegroundColor Red
}
