#!/usr/bin/env python3

"""
RBLX Short Trade - Separate Budget Analysis
Independent trade outside of TFSA portfolio
"""

import requests
import json
from datetime import datetime

def analyze_separate_rblx_short():
    """Analyze RBLX short as a separate trade"""
    
    print("=" * 70)
    print("🔴 RBLX SHORT TRADE - SEPARATE BUDGET")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%I:%M %p PST')}")
    print("INDEPENDENT FROM YOUR TFSA PORTFOLIO")
    print()
    
    # Current data
    current_price = 126.78
    
    print("📊 CURRENT RBLX STATUS:")
    print("-" * 50)
    print(f"Price: ${current_price:.2f}")
    print(f"Day Change: -2.12%")
    print(f"Volume: 7.7M (elevated)")
    print(f"Key Support: $125.00")
    print(f"Key Resistance: $130.00")
    print()
    
    print("=" * 70)
    print("💰 POSITION SIZING OPTIONS:")
    print("=" * 70)
    print()
    
    # Different budget scenarios
    budgets = [500, 1000, 2000, 5000]
    
    for budget in budgets:
        print(f"WITH ${budget} BUDGET:")
        print("-" * 50)
        
        # Calculate position
        shares = int(budget / current_price)
        actual_cost = shares * current_price
        
        # Risk/Reward at different levels
        stop_loss = 133.12  # +5%
        target1 = 114.10    # -10%
        target2 = 101.42    # -20%
        target3 = 88.75     # -30%
        
        max_loss = shares * (stop_loss - current_price)
        profit_t1 = shares * (current_price - target1)
        profit_t2 = shares * (current_price - target2)
        profit_t3 = shares * (current_price - target3)
        
        print(f"Shares to Short: {shares}")
        print(f"Position Value: ${actual_cost:.2f}")
        print()
        print(f"Risk (if stopped at ${stop_loss:.2f}): -${max_loss:.2f}")
        print(f"Reward at T1 (${target1:.2f}): +${profit_t1:.2f}")
        print(f"Reward at T2 (${target2:.2f}): +${profit_t2:.2f}")
        print(f"Reward at T3 (${target3:.2f}): +${profit_t3:.2f}")
        print(f"Risk/Reward Ratio: 1:{(profit_t1/max_loss):.1f}")
        print()
    
    print("=" * 70)
    print("📈 TRADE EXECUTION PLAN:")
    print("=" * 70)
    print()
    
    print("ENTRY STRATEGY:")
    print("-" * 50)
    print("OPTION A - Immediate Entry (Aggressive)")
    print(f"  • Short at market (~${current_price:.2f})")
    print(f"  • Stop loss at ${stop_loss:.2f}")
    print("  • Rationale: Catch the move before news spreads")
    print()
    
    print("OPTION B - Wait for Breakdown (Conservative)")
    print("  • Wait for break below $125")
    print("  • Short on retest of $125 as resistance")
    print("  • Stop loss at $127")
    print("  • Rationale: Confirm technical breakdown")
    print()
    
    print("OPTION C - Scale In (Balanced)")
    print("  • Short 1/3 position now")
    print("  • Short 1/3 on break of $125")
    print("  • Short final 1/3 on bounce to $125")
    print("  • Average entry ~$125.50")
    print()
    
    print("=" * 70)
    print("⏰ TIME-SENSITIVE FACTORS:")
    print("=" * 70)
    print()
    print("• Pre-market: News could spread overnight")
    print("• 9:30 AM EST: Market open volatility")
    print("• 10:00 AM EST: Institutional reaction time")
    print("• 3:30 PM EST: Day trader exit time")
    print("• After-hours: Potential news release window")
    print()
    
    print("=" * 70)
    print("🎯 RECOMMENDED TRADE STRUCTURE:")
    print("=" * 70)
    print()
    
    recommended_budget = 1000
    recommended_shares = int(recommended_budget / current_price)
    
    print(f"BUDGET: ${recommended_budget}")
    print(f"SHARES: {recommended_shares}")
    print()
    print("ENTRY PLAN:")
    print(f"1. Short {recommended_shares//2} shares NOW at ~${current_price:.2f}")
    print(f"2. Short {recommended_shares//2} shares on break of $125")
    print()
    print("EXIT PLAN:")
    print(f"• Stop Loss: ${stop_loss:.2f} (risk ${recommended_shares * (stop_loss - current_price):.2f})")
    print(f"• Take 50% profit at ${target1:.2f} (+${(recommended_shares//2) * (current_price - target1):.2f})")
    print(f"• Take 25% profit at ${target2:.2f} (+${(recommended_shares//4) * (current_price - target2):.2f})")
    print(f"• Let 25% ride to ${target3:.2f} (+${(recommended_shares//4) * (current_price - target3):.2f})")
    print()
    print(f"TOTAL PROFIT POTENTIAL: ${profit_t1:.2f} to ${profit_t3:.2f}")
    print()
    
    print("=" * 70)
    print("⚠️ RISK MANAGEMENT RULES:")
    print("=" * 70)
    print()
    print("1. NEVER move stop loss higher (let winners run)")
    print("2. If news is debunked, EXIT IMMEDIATELY")
    print("3. If RBLX gaps up >3%, EXIT at open")
    print("4. Maximum hold time: 5 trading days")
    print("5. If no movement in 48 hours, reduce position")
    print()
    
    print("=" * 70)
    print("📱 MONITORING CHECKLIST:")
    print("=" * 70)
    print()
    print("□ Set price alerts at $125, $120, $115")
    print("□ Monitor news feeds for lawsuit updates")
    print("□ Watch for unusual options activity")
    print("□ Track social media sentiment")
    print("□ Monitor competitor stocks (MSFT, TTWO)")
    print()
    
    print("=" * 70)
    print("✅ GO/NO-GO DECISION:")
    print("=" * 70)
    print()
    print("GREEN LIGHTS (Short if you see):")
    print("✓ Major news outlet confirmation")
    print("✓ Heavy volume (>10M shares)")
    print("✓ Break below $125")
    print("✓ Weak broader market")
    print()
    print("RED FLAGS (Don't short if):")
    print("✗ No news confirmation by EOD")
    print("✗ Stock bounces off $125")
    print("✗ Unusual call buying")
    print("✗ Company issues denial")
    print()
    
    print("=" * 70)
    print("🚀 ACTION ITEMS:")
    print("=" * 70)
    print("1. Decide on budget (recommend $1000)")
    print("2. Place first short order (50% position)")
    print("3. Set stop loss order immediately")
    print("4. Set price alerts")
    print("5. Monitor news flow closely")
    print("=" * 70)

if __name__ == "__main__":
    analyze_separate_rblx_short()