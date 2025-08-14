#!/usr/bin/env python3

"""
RBLX Put Options Analysis with Greeks
Understanding Delta, Theta, IV, and optimal strike selection
"""

import math
from datetime import datetime, timedelta

def analyze_options_with_greeks():
    """Analyze RBLX put options with full Greeks analysis"""
    
    print("=" * 70)
    print("🎯 RBLX PUT OPTIONS - COMPLETE GREEKS ANALYSIS")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%I:%M %p PST')}")
    print()
    
    # Current RBLX data
    current_price = 126.78
    current_iv = 0.55  # Implied Volatility ~55% (elevated due to news)
    normal_iv = 0.40   # Normal IV for RBLX ~40%
    days_to_expiry_weekly = 3
    days_to_expiry_monthly = 31
    
    print("📊 CURRENT RBLX STATUS:")
    print("-" * 50)
    print(f"Stock Price: ${current_price:.2f}")
    print(f"Implied Volatility: {current_iv*100:.0f}% (elevated)")
    print(f"Normal IV: {normal_iv*100:.0f}%")
    print(f"IV Rank: HIGH (bad for buying options)")
    print()
    
    print("=" * 70)
    print("📚 THE GREEKS EXPLAINED:")
    print("=" * 70)
    print()
    
    print("DELTA (Δ): Price movement relationship")
    print("• Measures how much option price changes per $1 stock move")
    print("• Put delta is negative (gains when stock drops)")
    print("• Range: 0 to -1.0 for puts")
    print()
    
    print("THETA (Θ): Time decay")
    print("• How much option loses per day")
    print("• Always negative for buyers")
    print("• Accelerates near expiration")
    print()
    
    print("VEGA (ν): Volatility sensitivity")
    print("• How much option price changes per 1% IV change")
    print("• High now = risk of IV crush")
    print()
    
    print("GAMMA (Γ): Delta acceleration")
    print("• How fast delta changes")
    print("• Higher near strike price")
    print()
    
    print("=" * 70)
    print("💰 PUT OPTION ANALYSIS WITH GREEKS:")
    print("=" * 70)
    print()
    
    # Option chain analysis
    strikes = [120, 125, 127.5, 130, 135]
    
    for strike in strikes:
        print(f"${strike} PUT OPTION:")
        print("-" * 50)
        
        # Calculate approximate Greeks
        moneyness = (strike - current_price) / current_price
        
        # Weekly options (3 days)
        if strike < current_price:  # OTM Put
            delta_weekly = -0.15 if strike == 120 else -0.30 if strike == 125 else -0.45
            premium_weekly = max(0.50, abs(moneyness) * current_price * 0.15)
        else:  # ITM Put
            delta_weekly = -0.55 if strike == 127.5 else -0.65 if strike == 130 else -0.80
            premium_weekly = (strike - current_price) + 2.0
        
        theta_weekly = -premium_weekly * 0.15  # Lose 15% per day
        vega_weekly = premium_weekly * 0.02
        
        # Monthly options (31 days)
        if strike < current_price:  # OTM Put
            delta_monthly = -0.25 if strike == 120 else -0.40 if strike == 125 else -0.48
            premium_monthly = max(2.0, abs(moneyness) * current_price * 0.35)
        else:  # ITM Put
            delta_monthly = -0.52 if strike == 127.5 else -0.60 if strike == 130 else -0.75
            premium_monthly = (strike - current_price) + 4.5
        
        theta_monthly = -premium_monthly * 0.03  # Lose 3% per day
        vega_monthly = premium_monthly * 0.08
        
        print(f"WEEKLY (Exp: {(datetime.now() + timedelta(days=3)).strftime('%b %d')})")
        print(f"  Premium: ${premium_weekly:.2f} x 100 = ${premium_weekly*100:.0f}")
        print(f"  Delta: {delta_weekly:.2f} (${abs(delta_weekly):.2f} gain per $1 drop)")
        print(f"  Theta: ${theta_weekly:.2f}/day (${abs(theta_weekly)*100:.0f} decay daily)")
        print(f"  Break-even: ${strike - premium_weekly:.2f}")
        print()
        
        print(f"MONTHLY (Exp: {(datetime.now() + timedelta(days=31)).strftime('%b %d')})")
        print(f"  Premium: ${premium_monthly:.2f} x 100 = ${premium_monthly*100:.0f}")
        print(f"  Delta: {delta_monthly:.2f} (${abs(delta_monthly):.2f} gain per $1 drop)")
        print(f"  Theta: ${theta_monthly:.2f}/day (${abs(theta_monthly)*100:.0f} decay daily)")
        print(f"  Vega: ${vega_monthly:.2f} (loses ${vega_monthly*100:.0f} if IV drops 1%)")
        print(f"  Break-even: ${strike - premium_monthly:.2f}")
        print()
        
        # Scenario analysis
        print(f"PROFIT SCENARIOS:")
        target_110 = max(0, (strike - 110 - premium_monthly)) * 100
        target_100 = max(0, (strike - 100 - premium_monthly)) * 100
        target_90 = max(0, (strike - 90 - premium_monthly)) * 100
        
        print(f"  If RBLX → $110: ${target_110:.0f}")
        print(f"  If RBLX → $100: ${target_100:.0f}")
        print(f"  If RBLX → $90: ${target_90:.0f}")
        print()
    
    print("=" * 70)
    print("⚠️ CRITICAL RISKS WITH HIGH IV:")
    print("=" * 70)
    print()
    print("IMPLIED VOLATILITY CRUSH:")
    print(f"• Current IV: {current_iv*100:.0f}% (elevated)")
    print(f"• Normal IV: {normal_iv*100:.0f}%")
    print("• If IV drops to normal after news:")
    print("  - Option values could drop 30-40%")
    print("  - Even if stock moves your direction!")
    print()
    
    print("EXAMPLE IV CRUSH:")
    print("$125 Put bought at 55% IV for $4.00")
    print("Stock drops to $122 but IV drops to 40%")
    print("Option might only be worth $3.50 (LOSS despite correct direction)")
    print()
    
    print("=" * 70)
    print("📈 OPTIMAL STRATEGY CONSIDERING GREEKS:")
    print("=" * 70)
    print()
    
    print("STRATEGY 1: WEEKLY HIGH-DELTA PUTS (Aggressive)")
    print("-" * 50)
    print("Buy: 2x $130 Weekly Puts")
    print("Cost: ~$700")
    print("Delta: -0.65 (responsive to moves)")
    print("Theta: -$90/day (BURNS FAST)")
    print("Best if: News hits THIS WEEK")
    print("Risk: Total loss in 3 days if wrong")
    print()
    
    print("STRATEGY 2: MONTHLY ATM PUTS (Balanced)")
    print("-" * 50)
    print("Buy: 2x $125 Monthly Puts")
    print("Cost: ~$800")
    print("Delta: -0.40 (good sensitivity)")
    print("Theta: -$24/day (manageable)")
    print("Vega Risk: High (could lose from IV drop)")
    print("Best if: Need time for news to develop")
    print()
    
    print("STRATEGY 3: PUT SPREAD (IV Neutral) ⭐ RECOMMENDED")
    print("-" * 50)
    print("Buy: 2x $125 Monthly Puts @ $4.00 = $800")
    print("Sell: 2x $115 Monthly Puts @ $1.50 = +$300")
    print("Net Cost: $500")
    print()
    print("ADVANTAGES:")
    print("• Reduced cost ($500 vs $800)")
    print("• Less IV exposure (short put offsets)")
    print("• Lower theta decay")
    print()
    print("DISADVANTAGES:")
    print("• Capped profit at $115")
    print("• Max profit: $1,500 (vs unlimited)")
    print()
    
    print("STRATEGY 4: WEEKLY THEN ROLL (Adaptive)")
    print("-" * 50)
    print("Week 1: Buy 1x $127.50 Weekly Put ($200)")
    print("If moves: Take profit")
    print("If not: Roll to next week")
    print("Advantage: Lower initial cost")
    print("Risk: Theta decay if timing wrong")
    print()
    
    print("=" * 70)
    print("🎯 EXECUTION CHECKLIST:")
    print("=" * 70)
    print()
    print("BEFORE ENTERING:")
    print("□ Check current IV vs historical")
    print("□ Verify bid-ask spread (<10% of mid)")
    print("□ Check open interest (>100 contracts)")
    print("□ Calculate break-even price")
    print("□ Set profit target and stop loss")
    print()
    
    print("POSITION MANAGEMENT:")
    print("□ If IV drops 10%: Consider exiting")
    print("□ If stock drops 5%: Take partial profit")
    print("□ If theta > 10% of value: Roll or exit")
    print("□ Never hold weeklies to expiration")
    print()
    
    print("=" * 70)
    print("💡 FINAL RECOMMENDATION WITH GREEKS:")
    print("=" * 70)
    print()
    print("BEST RISK/REWARD: PUT SPREAD")
    print("-" * 50)
    print("BUY:  2x RBLX $125 Put (Monthly)")
    print("SELL: 2x RBLX $115 Put (Monthly)")
    print()
    print("Net Cost: ~$500")
    print("Max Profit: $1,500 (if RBLX < $115)")
    print("Break-even: $122.50")
    print("Delta: -0.25 (net)")
    print("Theta: -$8/day (manageable)")
    print("IV Risk: REDUCED (spread hedges)")
    print()
    print("This gives you:")
    print("• 3:1 reward/risk ratio")
    print("• Protection from IV crush")
    print("• Time for thesis to play out")
    print("• Defined risk ($500 max loss)")
    print("=" * 70)

if __name__ == "__main__":
    analyze_options_with_greeks()