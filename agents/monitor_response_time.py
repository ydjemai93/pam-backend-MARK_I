"""
Agent Response Time Monitor

Tracks the critical metric: Time from user stops speaking → agent starts responding

This is the key UX metric for conversational AI quality.

Usage:
    python monitor_response_time.py <log_file>
    python monitor_response_time.py logs/agent_820.err

Author: PAM Team
Date: October 2025
"""

import sys
import re
from pathlib import Path
from datetime import datetime

def parse_turn_metrics(log_file):
    """Extract turn completion metrics from agent logs"""
    
    turns = []
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Look for turn completion lines
            # Format: 🎯 TURN COMPLETE - speech_XXX: STT=X.XXXs, LLM_TTFT=X.XXXs, TTS_TTFB=X.XXXs, Total_Latency=X.XXXs
            if '🎯 TURN COMPLETE' in line:
                # Extract speech_id
                speech_match = re.search(r'speech_([a-f0-9]+)', line)
                
                # Extract metrics
                stt_match = re.search(r'STT=([\d.]+)s', line)
                llm_ttft_match = re.search(r'LLM_TTFT=([\d.]+)s', line)
                tts_ttfb_match = re.search(r'TTS_TTFB=([\d.]+)s', line)
                total_match = re.search(r'Total_Latency=([\d.]+)s', line)
                
                if all([speech_match, stt_match, llm_ttft_match, tts_ttfb_match, total_match]):
                    turns.append({
                        'speech_id': speech_match.group(1),
                        'eou_delay': float(stt_match.group(1)),
                        'llm_ttft': float(llm_ttft_match.group(1)),
                        'tts_ttfb': float(tts_ttfb_match.group(1)),
                        'total_response_time': float(total_match.group(1))
                    })
    
    return turns

def analyze_response_times(turns):
    """Analyze and display response time metrics"""
    
    if not turns:
        print("❌ No turn data found in log file")
        return
    
    print("\n" + "="*80)
    print("📊 AGENT RESPONSE TIME ANALYSIS")
    print("="*80)
    print(f"\nMetric: Time from USER STOPS SPEAKING → AGENT STARTS RESPONDING")
    print(f"Total Turns: {len(turns)}\n")
    
    # Display each turn
    print("Turn-by-Turn Breakdown:")
    print("-" * 80)
    print(f"{'Turn':<6} {'EOU':>10} {'LLM TTFT':>12} {'TTS TTFB':>12} {'TOTAL':>12} {'Rating':<10}")
    print("-" * 80)
    
    for i, turn in enumerate(turns, 1):
        eou = turn['eou_delay']
        llm = turn['llm_ttft']
        tts = turn['tts_ttfb']
        total = turn['total_response_time']
        
        # Rating based on total response time
        if total < 1.0:
            rating = "⭐⭐⭐ Excellent"
        elif total < 1.5:
            rating = "⭐⭐ Good"
        elif total < 2.0:
            rating = "⭐ Fair"
        else:
            rating = "⚠️  Slow"
        
        print(f"{i:<6} {eou:>9.3f}s {llm:>11.3f}s {tts:>11.3f}s {total:>11.3f}s {rating:<10}")
    
    print("-" * 80)
    
    # Calculate statistics
    eou_times = [t['eou_delay'] for t in turns]
    llm_times = [t['llm_ttft'] for t in turns]
    tts_times = [t['tts_ttfb'] for t in turns]
    total_times = [t['total_response_time'] for t in turns]
    
    avg_eou = sum(eou_times) / len(eou_times)
    avg_llm = sum(llm_times) / len(llm_times)
    avg_tts = sum(tts_times) / len(tts_times)
    avg_total = sum(total_times) / len(total_times)
    
    min_total = min(total_times)
    max_total = max(total_times)
    
    # Display averages
    print("\n📈 AVERAGE METRICS:")
    print("-" * 80)
    print(f"End-of-Utterance Detection: {avg_eou:.3f}s ({avg_eou/avg_total*100:.1f}% of total)")
    print(f"LLM First Token:           {avg_llm:.3f}s ({avg_llm/avg_total*100:.1f}% of total)")
    print(f"TTS First Byte:            {avg_tts:.3f}s ({avg_tts/avg_total*100:.1f}% of total)")
    print(f"\n{'AVERAGE RESPONSE TIME:':<30} {avg_total:.3f}s")
    print(f"{'BEST (fastest):':<30} {min_total:.3f}s")
    print(f"{'WORST (slowest):':<30} {max_total:.3f}s")
    
    # Recommendations
    print("\n💡 OPTIMIZATION RECOMMENDATIONS:")
    print("-" * 80)
    
    if avg_eou > 0.8:
        print(f"⚠️  EOU Detection is slow ({avg_eou:.3f}s avg)")
        print(f"   → Current endpointing setting may be too conservative")
        print(f"   → Consider reducing endpointing from current value to 150-200ms")
    elif avg_eou > 0.5:
        print(f"✅ EOU Detection is acceptable ({avg_eou:.3f}s avg)")
        print(f"   → Endpointing setting seems balanced")
    else:
        print(f"⭐ EOU Detection is excellent ({avg_eou:.3f}s avg)")
        print(f"   → Endpointing setting is well-tuned")
    
    if avg_llm > 0.8:
        print(f"⚠️  LLM Response is slow ({avg_llm:.3f}s avg)")
        print(f"   → Consider using a faster model or enabling caching")
    elif avg_llm > 0.5:
        print(f"✅ LLM Response is acceptable ({avg_llm:.3f}s avg)")
    else:
        print(f"⭐ LLM Response is excellent ({avg_llm:.3f}s avg)")
    
    if avg_tts > 0.3:
        print(f"⚠️  TTS Generation is slow ({avg_tts:.3f}s avg)")
        print(f"   → Consider using a faster voice model")
    elif avg_tts > 0.2:
        print(f"✅ TTS Generation is acceptable ({avg_tts:.3f}s avg)")
    else:
        print(f"⭐ TTS Generation is excellent ({avg_tts:.3f}s avg)")
    
    # Overall assessment
    print("\n🎯 OVERALL ASSESSMENT:")
    print("-" * 80)
    
    if avg_total < 1.0:
        grade = "A+ (Excellent)"
        feedback = "Response time feels natural and immediate!"
    elif avg_total < 1.5:
        grade = "A (Very Good)"
        feedback = "Response time is very good, users will be satisfied."
    elif avg_total < 2.0:
        grade = "B (Good)"
        feedback = "Response time is acceptable but has room for improvement."
    elif avg_total < 3.0:
        grade = "C (Fair)"
        feedback = "Response time is noticeable, optimization recommended."
    else:
        grade = "D (Poor)"
        feedback = "Response time is too slow, immediate optimization needed."
    
    print(f"Grade: {grade}")
    print(f"Feedback: {feedback}")
    print(f"\nTarget: < 1.0s for excellent UX")
    print(f"Current: {avg_total:.3f}s")
    
    if avg_total > 1.0:
        improvement_needed = (avg_total - 1.0) * 1000
        print(f"Improvement needed: -{improvement_needed:.0f}ms to reach target")
    
    print("="*80 + "\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python monitor_response_time.py <log_file>")
        print("\nExample:")
        print("  python monitor_response_time.py logs/agent_820.err")
        print("\nFind latest log:")
        print("  python monitor_response_time.py $(ls -t logs/agent_*.err | head -1)")
        sys.exit(1)
    
    log_file = Path(sys.argv[1])
    
    if not log_file.exists():
        print(f"❌ Log file not found: {log_file}")
        sys.exit(1)
    
    print(f"\n📂 Analyzing: {log_file}")
    
    turns = parse_turn_metrics(log_file)
    analyze_response_times(turns)

if __name__ == "__main__":
    main()

