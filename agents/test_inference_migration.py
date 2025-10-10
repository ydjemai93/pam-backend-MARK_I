"""
LiveKit Inference vs Plugin Mode - Latency Comparison Test Script

This script helps compare performance between Inference and Plugin modes
before full migration.

Usage:
    1. Set USE_LIVEKIT_INFERENCE=false in .env
    2. Run: python test_inference_migration.py --mode plugin
    3. Set USE_LIVEKIT_INFERENCE=true in .env
    4. Run: python test_inference_migration.py --mode inference
    5. Compare results in test_results.json

Author: PAM Team
Date: October 2025
"""

import os
import sys
import json
import time
import asyncio
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Test configuration
TEST_RESULTS_FILE = "inference_test_results.json"
TEST_AUDIO_TEXT = "Bonjour, je suis Pam de TechSolutions Pro. Comment puis-je vous aider aujourd'hui?"

def load_test_results():
    """Load existing test results"""
    if Path(TEST_RESULTS_FILE).exists():
        with open(TEST_RESULTS_FILE, 'r') as f:
            return json.load(f)
    return {"tests": []}

def save_test_result(result):
    """Save test result to file"""
    results = load_test_results()
    results["tests"].append(result)
    with open(TEST_RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results saved to {TEST_RESULTS_FILE}")

def check_environment():
    """Check required environment variables"""
    print("\n" + "="*60)
    print("ENVIRONMENT CHECK")
    print("="*60)
    
    inference_mode = os.getenv('USE_LIVEKIT_INFERENCE', 'false').lower() in ('true', '1', 'yes', 'on')
    
    print(f"USE_LIVEKIT_INFERENCE: {os.getenv('USE_LIVEKIT_INFERENCE', 'not set')}")
    print(f"Mode: {'🚀 INFERENCE' if inference_mode else '🔌 PLUGIN'}")
    print(f"\nLIVEKIT_API_KEY: {'✅ Set' if os.getenv('LIVEKIT_API_KEY') else '❌ Not set'}")
    print(f"LIVEKIT_API_SECRET: {'✅ Set' if os.getenv('LIVEKIT_API_SECRET') else '❌ Not set'}")
    
    if not inference_mode:
        print(f"\nPLUGIN MODE - Additional keys required:")
        print(f"OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not set'}")
        print(f"DEEPGRAM_API_KEY: {'✅ Set' if os.getenv('DEEPGRAM_API_KEY') else '❌ Not set'}")
        print(f"CARTESIA_API_KEY: {'✅ Set' if os.getenv('CARTESIA_API_KEY') else '❌ Not set'}")
    
    return inference_mode

def analyze_results():
    """Analyze and compare test results"""
    results = load_test_results()
    
    if len(results.get("tests", [])) < 2:
        print("\n⚠️  Not enough test runs to compare. Run tests in both modes.")
        return
    
    print("\n" + "="*60)
    print("LATENCY COMPARISON ANALYSIS")
    print("="*60)
    
    plugin_tests = [t for t in results["tests"] if t["mode"] == "plugin"]
    inference_tests = [t for t in results["tests"] if t["mode"] == "inference"]
    
    if plugin_tests and inference_tests:
        print(f"\n📊 Plugin Mode ({len(plugin_tests)} tests):")
        print(f"   Latest test: {plugin_tests[-1]['timestamp']}")
        
        print(f"\n📊 Inference Mode ({len(inference_tests)} tests):")
        print(f"   Latest test: {inference_tests[-1]['timestamp']}")
        
        print("\n" + "="*60)
        print("⚡ EXPECTED IMPROVEMENTS:")
        print("="*60)
        print("STT:   70-100ms faster  (100-150ms → 30-50ms)")
        print("TTS:   60-80ms faster   (80-120ms → 20-40ms)")
        print("LLM:   100-150ms faster (200-300ms → 100-150ms)")
        print("TOTAL: 230-330ms faster (400-600ms → 150-250ms)")
    else:
        if not plugin_tests:
            print("\n⚠️  No plugin mode tests found. Run with USE_LIVEKIT_INFERENCE=false")
        if not inference_tests:
            print("\n⚠️  No inference mode tests found. Run with USE_LIVEKIT_INFERENCE=true")

async def run_mock_test(mode: str):
    """
    Mock test to demonstrate the testing framework.
    
    In production, this would:
    1. Initialize agent with current mode
    2. Run STT/TTS/LLM operations
    3. Measure actual latencies
    4. Return real metrics
    """
    print("\n" + "="*60)
    print(f"RUNNING MOCK TEST - {mode.upper()} MODE")
    print("="*60)
    
    print("\n⚠️  NOTE: This is a MOCK test for demonstration.")
    print("To run real tests, you need to:")
    print("1. Make an actual call with the agent")
    print("2. Check the logs in agents/logs/agent_*.log")
    print("3. Extract STT/TTS/LLM metrics from the call")
    
    print(f"\n🧪 Simulating {mode} mode test...")
    await asyncio.sleep(2)  # Simulate processing
    
    # Mock metrics (replace with real metrics from actual calls)
    result = {
        "mode": mode,
        "timestamp": datetime.now().isoformat(),
        "note": "MOCK TEST - Replace with real call metrics",
        "instructions": [
            "1. Start agent with current .env setting",
            "2. Make a test call",
            "3. Find call log in agents/logs/",
            "4. Extract metrics from log",
            "5. Record actual latency values here"
        ],
        "expected_metrics": {
            "stt_latency_ms": "30-50" if mode == "inference" else "100-150",
            "tts_latency_ms": "20-40" if mode == "inference" else "80-120",
            "llm_latency_ms": "100-150" if mode == "inference" else "200-300",
            "total_turn_ms": "150-250" if mode == "inference" else "400-600"
        }
    }
    
    save_test_result(result)
    
    print("\n✅ Mock test completed")
    print(f"📝 Recorded expected metrics for {mode} mode")
    return result

def main():
    parser = argparse.ArgumentParser(
        description="Test LiveKit Inference vs Plugin mode latency"
    )
    parser.add_argument(
        "--mode",
        choices=["plugin", "inference", "check", "analyze"],
        default="check",
        help="Test mode: plugin, inference, check (env), or analyze (results)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("LiveKit Inference Migration - Test Script")
    print("="*60)
    
    if args.mode == "check":
        check_environment()
        print("\n💡 Next steps:")
        print("1. Run: python test_inference_migration.py --mode plugin")
        print("2. Change .env: USE_LIVEKIT_INFERENCE=true")
        print("3. Run: python test_inference_migration.py --mode inference")
        print("4. Run: python test_inference_migration.py --mode analyze")
        
    elif args.mode == "analyze":
        analyze_results()
        
    else:
        # Run test
        current_mode = check_environment()
        expected_mode = args.mode == "inference"
        
        if current_mode != expected_mode:
            print(f"\n⚠️  WARNING: Mode mismatch!")
            print(f"   You requested: {args.mode}")
            print(f"   .env setting: {'inference' if current_mode else 'plugin'}")
            print(f"\n   Update .env: USE_LIVEKIT_INFERENCE={'true' if expected_mode else 'false'}")
            sys.exit(1)
        
        asyncio.run(run_mock_test(args.mode))

if __name__ == "__main__":
    main()

