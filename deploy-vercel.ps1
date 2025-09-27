# Vercel Deployment Script - FastAPI to Serverless
# Prepares the project for Vercel deployment

Write-Host "🚀 Preparing Vercel deployment..." -ForegroundColor Green

# Backup current requirements.txt
if (Test-Path "requirements.txt") {
    Copy-Item "requirements.txt" "requirements.railway.backup.txt"
    Write-Host "✅ Backed up Railway requirements.txt" -ForegroundColor Yellow
}

# Copy Vercel-optimized requirements
Copy-Item "requirements.vercel.txt" "requirements.txt"
Write-Host "✅ Switched to Vercel-optimized requirements.txt" -ForegroundColor Green

Write-Host ""
Write-Host "📋 Vercel Deployment Checklist:" -ForegroundColor Cyan
Write-Host "1. ✅ vercel.json configured for FastAPI"
Write-Host "2. ✅ requirements.txt optimized for serverless"
Write-Host "3. ✅ Lighter dependencies (no heavy packages)"
Write-Host "4. 🔄 Ready to deploy with Vercel CLI"
Write-Host ""

Write-Host "🔧 Environment Variables Needed:" -ForegroundColor Yellow
Write-Host "You'll need to set these in Vercel dashboard:"
Write-Host "- SUPABASE_URL"
Write-Host "- SUPABASE_ANON_KEY" 
Write-Host "- SUPABASE_SERVICE_ROLE_KEY"
Write-Host "- OPENAI_API_KEY"
Write-Host "- ELEVENLABS_API_KEY"
Write-Host "- DEEPGRAM_API_KEY"
Write-Host "- (and any other env vars from your .env file)"
Write-Host ""

Write-Host "Commands to run:" -ForegroundColor Yellow
Write-Host "1. vercel login"
Write-Host "2. vercel --prod"
Write-Host ""
Write-Host "OR via GitHub:"
Write-Host "1. Commit changes: git add . && git commit -m 'Vercel deployment setup'"
Write-Host "2. Push to GitHub: git push origin main"
Write-Host "3. Connect GitHub repo in Vercel dashboard"
Write-Host ""

Write-Host "⚠️  To restore Railway setup:" -ForegroundColor Red
Write-Host "Copy-Item 'requirements.railway.backup.txt' 'requirements.txt'"
