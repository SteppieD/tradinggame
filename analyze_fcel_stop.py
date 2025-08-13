#!/usr/bin/env python3

"""
Analyze FCEL Stop Loss - Was it too tight?
"""

import json
from datetime import datetime

def analyze_fcel_stop():
    """Analyze if FCEL stop was too tight"""
    
    print("=" * 70)
    print("🔍 FCEL STOP LOSS ANALYSIS")
    print("=" * 70)
    print()
    
    # FCEL data
    entry_price = 4.05
    morning_price = 6.08  # What we thought it was
    stop_executed = 4.26  # Where it actually sold
    
    # Calculate what happened
    print("📊 WHAT HAPPENED:")
    print("-" * 50)
    print(f"Entry Price: ${entry_price:.2f}")
    print(f"Morning Quote: ${morning_price:.2f} (possibly stale data)")
    print(f"Stop Executed: ${stop_executed:.2f}")
    print(f"Actual Gain: ${stop_executed - entry_price:.2f} (+{((stop_executed - entry_price)/entry_price)*100:.1f}%)")
    print()
    
    # Stop strategy analysis
    print("🎯 STOP STRATEGY USED:")
    print("-" * 50)
    print("Morning calculation showed +50% gain, so we used:")
    print("  • Strategy: TIGHT_TRAIL for big winners")
    print("  • Trigger Delta: $0.18 (very tight)")
    print("  • Stop at: ~$5.90")
    print("  • Actual trigger: Stock fell through $5.90 to $4.26")
    print()
    
    # The problem
    print("⚠️ THE ISSUE:")
    print("-" * 50)
    print("1. We had BAD PRICE DATA")
    print("   - Thought FCEL was at $6.08")
    print("   - It was probably around $4.09 (Aug 12 close)")
    print("   - Stop at $5.90 was ABOVE the actual price!")
    print()
    print("2. STOP TRIGGERED IMMEDIATELY")
    print("   - Market opened with FCEL below our stop")
    print("   - Sold at market price of $4.26")
    print("   - Now it's recovering in after-hours")
    print()
    
    # What we should have done
    print("✅ WHAT WE SHOULD HAVE DONE:")
    print("-" * 50)
    print("1. VERIFY PRICES before setting stops")
    print("   - Check broker app for actual closing prices")
    print("   - Don't rely on stale web data")
    print()
    print("2. CORRECT STOP CALCULATION:")
    print(f"   - If FCEL was actually ~$4.09")
    print(f"   - Entry: $4.05")
    print(f"   - Gain: ~1%")
    print(f"   - Should use TIGHT_STOP strategy")
    print(f"   - Stop around $3.85-$3.90 (protect capital)")
    print()
    
    # Lessons learned
    print("=" * 70)
    print("📚 LESSONS LEARNED:")
    print("=" * 70)
    print()
    print("1. ALWAYS verify closing prices from broker before bed")
    print("2. NEVER set stops based on stale data")
    print("3. Check pre-market prices before setting morning stops")
    print("4. For small gains (<5%), use wider stops to avoid whipsaws")
    print("5. For volatile stocks, consider 10-15% stops, not 3-5%")
    print()
    print("🤔 BOTTOM LINE:")
    print("-" * 50)
    print("YES, the stop was too tight because:")
    print("  • Based on incorrect price data ($6.08 vs actual ~$4.09)")
    print("  • Didn't account for normal volatility")
    print("  • Triggered immediately at market open")
    print()
    print("BUT, you still made 3.42% profit, which beats:")
    print("  • Holding and watching it go negative")
    print("  • The -0.80% your portfolio would show without this gain")
    print()
    print("💡 GOING FORWARD:")
    print("-" * 50)
    print("Tomorrow morning routine MUST include:")
    print("  1. Check ACTUAL closing prices in CIBC app")
    print("  2. Check pre-market movement")
    print("  3. Set stops based on REAL prices, not estimates")
    print("  4. Use wider stops for volatile small-caps (8-12%)")
    print("=" * 70)

if __name__ == "__main__":
    analyze_fcel_stop()