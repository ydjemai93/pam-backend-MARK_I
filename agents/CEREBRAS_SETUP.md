# Cerebras Integration - Setup Guide

## 🚀 Overview

Cerebras provides **world's fastest LLM inference** using wafer-scale chip architecture. This integration allows you to use **Llama 3.3 70B** and other open-source models with ultra-low latency.

**Expected Performance:**
- **LLM TTFT**: ~100-200ms (vs 791ms with GPT-4o-mini)
- **Total Response**: ~900-1100ms (vs 1,627ms current)
- **Speed Improvement**: 40-50% faster overall response time

---

## 📋 Setup Instructions

### **Step 1: Get Cerebras API Key**

1. Go to [https://cloud.cerebras.ai/](https://cloud.cerebras.ai/)
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `csk-...`)

### **Step 2: Add API Key to Environment**

Edit `MARK_I/backend_python/agents/.env`:

```bash
# Cerebras Configuration
USE_CEREBRAS=true
CEREBRAS_API_KEY="csk-your-api-key-here"  # Replace with your actual key
```

### **Step 3: Restart the Agent**

```bash
cd MARK_I/backend_python/agents
python outbound_agent.py start
```

---

## 🎯 **How It Works**

### **LLM Selection Priority:**

```
1. Cerebras (if USE_CEREBRAS=true) → Llama 3.3 70B
2. Inference (if USE_LIVEKIT_INFERENCE=true) → GPT-5-nano
3. Plugin (default) → GPT-4o-mini from database
```

### **What You'll See in Logs:**

**When Cerebras is ENABLED:**
```
🚀 Cerebras Mode: ✅ ENABLED
   → Model: Llama 3.3 70B (open-source)
   → Benefits: World's fastest inference, wafer-scale hardware

🚀 [CEREBRAS] Using Cerebras for ultra-low latency LLM (overriding all configs)
🚀 [CEREBRAS] Using Cerebras for LLM: llama-3.3-70b
   ✅ Cerebras LLM configured: llama-3.3-70b (world's fastest inference)
```

**When Cerebras is DISABLED:**
```
🚀 [INFERENCE] Forcing GPT-5-nano for optimal latency (overriding DB config)
```

---

## 🔄 **Testing Modes**

### **Mode 1: Cerebras (Fastest - Open Source)**
```bash
USE_CEREBRAS=true
USE_LIVEKIT_INFERENCE=false  # Ignored when Cerebras enabled
```
- Model: Llama 3.3 70B
- Expected TTFT: ~150ms
- Quality: Comparable to GPT-4o-mini

### **Mode 2: LiveKit Inference (GPT-5-nano)**
```bash
USE_CEREBRAS=false
USE_LIVEKIT_INFERENCE=true
```
- Model: GPT-5-nano (OpenAI)
- Expected TTFT: ~500-700ms
- Quality: OpenAI quality

### **Mode 3: Plugin Mode (Legacy)**
```bash
USE_CEREBRAS=false
USE_LIVEKIT_INFERENCE=false
```
- Model: GPT-4o-mini (from database)
- Expected TTFT: ~791ms
- Quality: Proven, tested

---

## 📊 **Performance Comparison**

| Mode | Model | TTFT | Total Response | Cost |
|------|-------|------|----------------|------|
| **Cerebras** | Llama 3.3 70B | ~150ms ⚡⚡ | ~950ms ⚡⚡ | Low |
| **Inference** | GPT-5-nano | ~600ms | ~1,400ms | Medium |
| **Plugin** | GPT-4o-mini | ~791ms | ~1,627ms | Medium |

---

## ⚠️ **Important Notes**

### **Model Differences:**
- **Cerebras uses Llama 3.3 70B** (open-source model, NOT GPT-4o-mini)
- You may need to adjust system prompts slightly
- Quality is comparable but behavior may differ

### **Fallback Behavior:**
If Cerebras fails to initialize:
1. Automatically falls back to Inference mode (if enabled)
2. Then falls back to Plugin mode
3. Logs error for troubleshooting

### **Cost Considerations:**
- Cerebras: Pay-per-token, open-source model pricing
- Generally cheaper than OpenAI for equivalent quality
- Check [Cerebras pricing](https://cloud.cerebras.ai/pricing)

---

## 🧪 **Testing Checklist**

After enabling Cerebras:

1. ✅ Check startup logs for "Cerebras Mode: ✅ ENABLED"
2. ✅ Make test call
3. ✅ Check turn metrics for LLM_TTFT (should be ~150-200ms)
4. ✅ Verify Total_Latency is under 1.2s
5. ✅ Test conversation quality (prompt adjustments if needed)

---

## 🔧 **Troubleshooting**

### **Issue: "CEREBRAS_API_KEY not set"**
**Solution:** Add your API key to `.env` file

### **Issue: "Failed to initialize Cerebras LLM"**
**Solution:** Check:
- API key is valid
- Internet connection
- Cerebras service status
- Agent will auto-fallback to Inference/Plugin

### **Issue: Response quality differs from GPT-4o-mini**
**Solution:** 
- Llama 3.3 70B is a different model
- May need to adjust system prompts
- Test and compare responses

---

## 📚 **Additional Resources**

- [Cerebras Documentation](https://docs.cerebras.ai/)
- [LiveKit Cerebras Integration](https://docs.livekit.io/agents/integrations/cerebras/)
- [Llama 3.3 Model Card](https://huggingface.co/meta-llama/Llama-3.3-70B)

---

## 🎯 **Recommendation**

1. **Get Cerebras API key**
2. **Enable Cerebras mode**
3. **Make test call** 
4. **Compare LLM_TTFT** with previous tests
5. **If faster and quality good → Keep Cerebras**
6. **If quality issues → Fallback to GPT-5-nano or GPT-4o-mini**

---

**Created:** October 2025  
**Status:** Ready for testing

