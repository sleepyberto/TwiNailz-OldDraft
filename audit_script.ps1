# Comprehensive Codebase Audit Script
# Run this from your project root directory

Write-Host "🔍 Starting Comprehensive Codebase Audit..." -ForegroundColor Green

# Create audit report directory
$auditDir = "audit_results_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Force -Path $auditDir
$reportFile = "$auditDir\audit_report.txt"

# Initialize report
"CODEBASE AUDIT REPORT - $(Get-Date)" | Out-File $reportFile
"=" * 50 | Out-File $reportFile -Append

# 1. FILE & PROJECT CLEANUP
Write-Host "🧹 1. File & Project Cleanup..." -ForegroundColor Yellow

# Find duplicate files
Write-Host "  - Scanning for duplicate files..."
"DUPLICATE FILES:" | Out-File $reportFile -Append
Get-ChildItem -Recurse -File | Group-Object Length | Where-Object Count -gt 1 | 
    ForEach-Object { $_.Group | Get-FileHash | Group-Object Hash | Where-Object Count -gt 1 } |
    Out-File $reportFile -Append

# Find large files that might be unnecessary
Write-Host "  - Finding large files (>10MB)..."
"LARGE FILES (>10MB):" | Out-File $reportFile -Append
Get-ChildItem -Recurse -File | Where-Object Length -gt 10MB | 
    Select-Object Name, Directory, @{Name="SizeMB";Expression={[math]::Round($_.Length/1MB,2)}} |
    Out-File $reportFile -Append

# Find temporary and cache files
Write-Host "  - Scanning for temporary files..."
"TEMPORARY/CACHE FILES TO CONSIDER REMOVING:" | Out-File $reportFile -Append
$tempPatterns = @("*.tmp", "*.temp", "*.cache", "*.pyc", "*.pyo", "__pycache__", "*.log", ".DS_Store", "Thumbs.db", "node_modules", ".pytest_cache", ".coverage", "*.egg-info")
foreach ($pattern in $tempPatterns) {
    Get-ChildItem -Recurse -Force -Name $pattern -ErrorAction SilentlyContinue | Out-File $reportFile -Append
}

Write-Host "✅ File cleanup scan complete" -ForegroundColor Green