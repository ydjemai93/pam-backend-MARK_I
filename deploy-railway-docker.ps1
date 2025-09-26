# Railway Docker Deployment Script
# Uses custom Dockerfile to bypass all dependency hell

Write-Host "🐳 Preparing Railway deployment with custom Dockerfile..." -ForegroundColor Green

# Backup current requirements.txt
if (Test-Path "requirements.txt") {
    Copy-Item "requirements.txt" "requirements.local.backup.txt"
    Write-Host "✅ Backed up current requirements.txt" -ForegroundColor Yellow
}

# Copy optimized Dockerfile for Railway
Copy-Item "Dockerfile.railway" "Dockerfile"
Write-Host "✅ Switched to Railway-optimized Dockerfile" -ForegroundColor Green

# Keep original requirements.txt (Dockerfile handles dependency order)
Write-Host "✅ Using original requirements.txt with Docker dependency management" -ForegroundColor Green

Write-Host ""
Write-Host "📋 Railway Docker Deployment Checklist:" -ForegroundColor Cyan
Write-Host "1. ✅ Custom Dockerfile created (bypasses Nixpacks)"
Write-Host "2. ✅ Multi-stage build with dependency pre-installation"
Write-Host "3. ✅ Explicit six/dateutil handling"
Write-Host "4. ✅ Railway PORT environment variable support"
Write-Host "5. 🔄 Ready to commit and deploy"
Write-Host ""

Write-Host "🔧 Railway Configuration:" -ForegroundColor Yellow
Write-Host "- Build Method: Dockerfile (Railway auto-detects)"
Write-Host "- Root Directory: MARK_I/backend_python"  
Write-Host "- Start Command: (handled by Dockerfile CMD)"
Write-Host ""

Write-Host "Commands to run:" -ForegroundColor Yellow
Write-Host "git add ."
Write-Host "git commit -m 'Railway Docker deployment: Custom Dockerfile bypasses dependency hell'"
Write-Host "git push origin main"
Write-Host ""

Write-Host "🎯 Expected Behavior:" -ForegroundColor Cyan
Write-Host "- Railway detects Dockerfile automatically"
Write-Host "- Builds custom container with controlled dependencies"
Write-Host "- Bypasses Nixpacks entirely"
Write-Host "- No more six.moves._thread errors!"
Write-Host ""

Write-Host "⚠️  To restore local development:" -ForegroundColor Red
Write-Host ".\restore-local.ps1"
