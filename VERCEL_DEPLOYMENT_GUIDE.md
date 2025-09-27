# FastAPI → Vercel Deployment Guide

## 🎯 Why Vercel Will Work Better

- ✅ **Serverless Functions** → No container compatibility issues
- ✅ **Better Python dependency handling** → Handles Windows dev environment better
- ✅ **No Docker/Linux issues** → Runs in managed serverless environment
- ✅ **Automatic scaling** → No need to manage containers
- ✅ **Built-in CI/CD** → GitHub integration

## 📋 Deployment Process

### Option A: Vercel CLI (Direct)

```powershell
# 1. Install Vercel CLI
npm install -g vercel

# 2. Prepare deployment
.\deploy-vercel.ps1

# 3. Login to Vercel
vercel login

# 4. Deploy
vercel --prod
```

### Option B: GitHub Integration (Recommended)

```powershell
# 1. Prepare deployment files
.\deploy-vercel.ps1

# 2. Commit changes
git add .
git commit -m "Vercel deployment setup"
git push origin main

# 3. Go to vercel.com
# 4. Import GitHub repository
# 5. Set environment variables
# 6. Deploy automatically
```

## 🔧 Environment Variables Setup

In Vercel dashboard, add these environment variables:

```
SUPABASE_URL=https://ioddvuvaxqywbzfcjmpi.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
DEEPGRAM_API_KEY=your_deepgram_key
TELNYX_API_KEY=your_telnyx_key
LIVEKIT_API_KEY=your_livekit_key
LIVEKIT_API_SECRET=your_livekit_secret
LIVEKIT_URL=your_livekit_url
FRONTEND_URL=your_frontend_url
```

## 📁 File Structure

```
MARK_I/backend_python/
├── vercel.json              ← Vercel configuration
├── requirements.txt         ← Serverless-optimized dependencies
├── api/
│   ├── main.py             ← FastAPI app (entry point)
│   ├── routes/             ← API routes
│   └── ...                 ← Other modules
└── ...
```

## 🎯 Key Advantages Over Railway

| Aspect | Vercel ✅ | Railway ❌ |
|--------|-----------|------------|
| Dependency Issues | Handled by platform | six.moves._thread errors |
| Windows Compatibility | Native support | Container compatibility issues |
| Deployment Speed | ~30 seconds | ~2-3 minutes |
| Cold Start | ~200ms | N/A (always running) |
| Scaling | Automatic | Manual |
| Cost | Pay per request | Monthly fee |

## 🔄 If Issues Occur

1. **Import Errors**: Vercel handles most Python dependencies better than containers
2. **Memory Issues**: Increase maxLambdaSize in vercel.json
3. **Timeout Issues**: Increase maxDuration in vercel.json
4. **Environment Variables**: Double-check in Vercel dashboard

## 🚀 Expected Result

```
✅ Deploying FastAPI to Vercel...
✅ Installing Python dependencies...
✅ Building serverless functions...
✅ Deployment successful!
🌐 Your API: https://your-project.vercel.app
```

## 🔄 Rollback to Railway

```powershell
# Restore Railway setup
Copy-Item "requirements.railway.backup.txt" "requirements.txt"
git add requirements.txt
git commit -m "Restore Railway setup"
git push origin main
```

## 🎉 Why This Should Work

- **No container dependency conflicts** → Serverless environment
- **Better Windows → Cloud compatibility** → Vercel optimized for this
- **Managed Python environment** → No six.moves._thread issues
- **Proven FastAPI support** → Many FastAPI apps on Vercel
