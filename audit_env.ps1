# Check .env file contents (safely)
if (Test-Path ".env") {
    Write-Host "✅ .env file exists"
    $envContent = Get-Content ".env"
    
    $requiredVars = @("TELEGRAM_BOT_TOKEN", "DATABASE_URL")
    foreach ($var in $requiredVars) {
        if ($envContent -like "*${var}=*") {
            Write-Host "✅ $var - CONFIGURED"
        } else {
            Write-Host "❌ $var - MISSING"
        }
    }
} else {
    Write-Host "❌ .env file missing"
}