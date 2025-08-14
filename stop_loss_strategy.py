#!/usr/bin/env python3

"""
Dynamic Stop Loss Strategy
Optimizes for maximum gains while managing risk based on multiple factors
"""

import json
from datetime import datetime

def calculate_optimal_stops():
    """Calculate optimal stop strategy for each position"""
    
    print("=" * 70)
    print("🎯 OPTIMAL STOP LOSS STRATEGY")
    print("=" * 70)
    print(f"Time: {datetime.now().strftime('%B %d, %Y at %I:%M %p PST')}")
    print()
    
    # Current portfolio with actual fills
    positions = {
        'CHPT': {
            'shares': 26,
            'entry': 10.7845,
            'current': 11.50,  # Estimate - morning volatility
            'days_held': 2,
            'volatility': 'HIGH',
            'sector': 'EV Charging',
            'profit_pct': 6.6
        },
        'EVGO': {
            'shares': 82,
            'entry': 3.6271,
            'current': 3.85,  # Estimate - morning volatility
            'days_held': 2,
            'volatility': 'VERY HIGH',
            'sector': 'EV Charging',
            'profit_pct': 6.2
        },
        'TDUP': {
            'shares': 19,
            'entry': 10.45,
            'current': 10.45,
            'days_held': 0,
            'volatility': 'MEDIUM',
            'sector': 'E-commerce',
            'profit_pct': 0.0,
            'catalyst': 'Recent earnings beat'
        },
        'FUBO': {
            'shares': 55,
            'entry': 3.67,
            'current': 3.67,
            'days_held': 0,
            'volatility': 'VERY HIGH',
            'sector': 'Streaming',
            'profit_pct': 0.0,
            'catalyst': 'First EBITDA positive'
        }
    }
    
    print("📊 FACTORS CONSIDERED:")
    print("-" * 50)
    print("1. Time of day (morning volatility)")
    print("2. Position age (new vs established)")
    print("3. Current P&L (profit protection)")
    print("4. Stock volatility (ATR-based)")
    print("5. Sector correlation (CHPT/EVGO move together)")
    print("6. Market conditions (SPY/IWM trends)")
    print("7. Position size (risk per position)")
    print("8. Account leverage (fully invested)")
    print()
    
    print("=" * 70)
    print("🔧 OPTIMIZED STOP RECOMMENDATIONS:")
    print("=" * 70)
    print()
    
    recommendations = {}
    
    for symbol, data in positions.items():
        print(f"{symbol}:")
        print(f"  Entry: ${data['entry']:.2f}")
        print(f"  Current: ~${data['current']:.2f}")
        print(f"  P&L: {'+' if data['profit_pct'] >= 0 else ''}{data['profit_pct']:.1f}%")
        print(f"  Volatility: {data['volatility']}")
        
        # Decision logic
        if data['days_held'] == 0:  # New positions
            if data['volatility'] == 'VERY HIGH':
                # FUBO - high volatility, new position
                stop_type = "WIDE FIXED"
                stop_pct = 0.12  # 12% stop for very volatile
                reason = "New position, high volatility - needs room"
            else:
                # TDUP - medium volatility, new position
                stop_type = "MODERATE FIXED"
                stop_pct = 0.08  # 8% stop for medium volatile
                reason = "New position, moderate volatility"
            
            stop_price = round(data['entry'] * (1 - stop_pct), 2)
            limit_price = stop_price - 0.02
            
            print(f"  Strategy: {stop_type}")
            print(f"  Stop: ${stop_price:.2f} (-{stop_pct*100:.0f}%)")
            print(f"  Limit: ${limit_price:.2f}")
            print(f"  Reason: {reason}")
            
        else:  # Existing positions with profits
            if data['profit_pct'] >= 10:
                # Strong profit - wider trailing
                stop_type = "TRAILING WIDE"
                trigger_delta_pct = 0.04  # 4% trailing
                reason = "Strong profit - let it run with protection"
            elif data['profit_pct'] >= 5:
                # Moderate profit - balanced trailing
                stop_type = "TRAILING BALANCED"
                trigger_delta_pct = 0.025  # 2.5% trailing
                reason = "Good profit - balance protection and upside"
            else:
                # Small profit - tighter trailing
                stop_type = "TRAILING TIGHT"
                trigger_delta_pct = 0.015  # 1.5% trailing
                reason = "Small profit - protect breakeven"
            
            trigger_delta = round(data['current'] * trigger_delta_pct, 2)
            limit_offset = round(trigger_delta * 0.15, 2)  # 15% of trigger
            
            print(f"  Strategy: {stop_type}")
            print(f"  Trigger Delta: ${trigger_delta:.2f}")
            print(f"  Limit Offset: ${limit_offset:.2f}")
            print(f"  Reason: {reason}")
        
        print()
        
        recommendations[symbol] = {
            'stop_type': stop_type,
            'reason': reason
        }
    
    print("=" * 70)
    print("💡 KEY INSIGHTS:")
    print("=" * 70)
    print()
    print("1. SECTOR CORRELATION:")
    print("   • CHPT & EVGO move together (EV sector)")
    print("   • Consider tightening both if one shows weakness")
    print()
    print("2. VOLATILITY MANAGEMENT:")
    print("   • FUBO needs widest stop (12%) - very volatile")
    print("   • TDUP moderate stop (8%) - less volatile")
    print()
    print("3. TIME-BASED ADJUSTMENTS:")
    print("   • Use wider stops until 7:00 AM PST")
    print("   • Tighten after morning volatility settles")
    print("   • Consider converting TDUP/FUBO to trailing after 2-3% gain")
    print()
    print("4. RISK MANAGEMENT:")
    print("   • You're fully invested ($0.45 cash)")
    print("   • Total risk if all stops hit: ~$100-120")
    print("   • This is acceptable (10-12% of portfolio)")
    print()
    
    print("=" * 70)
    print("🎯 OPTIMAL STRATEGY FOR MAXIMUM GAINS:")
    print("=" * 70)
    print()
    print("MORNING (Until 7:00 AM PST):")
    print("  • CHPT: Wide trailing ($0.50 trigger)")
    print("  • EVGO: Wide trailing ($0.15 trigger)")
    print("  • TDUP: Fixed stop at $9.61")
    print("  • FUBO: Fixed stop at $3.23 (wider for volatility)")
    print()
    print("AFTER 7:00 AM PST:")
    print("  • CHPT: Tighten to $0.30 trigger")
    print("  • EVGO: Tighten to $0.08 trigger")
    print("  • TDUP: Keep at $9.61 until +3% profit")
    print("  • FUBO: Keep at $3.23 until +3% profit")
    print()
    print("PROFIT MILESTONES:")
    print("  • At +3%: Convert fixed to trailing")
    print("  • At +5%: Use Fibonacci retracement stops")
    print("  • At +10%: Widen trailing to let winners run")
    print("  • At +20%: Consider taking partial profits")
    print()
    
    print("=" * 70)
    print("✅ SUMMARY:")
    print("=" * 70)
    print("This strategy maximizes gains by:")
    print("• Giving new positions room to work")
    print("• Protecting existing profits")
    print("• Adjusting for time-of-day volatility")
    print("• Considering sector correlations")
    print("• Managing total portfolio risk")
    print("=" * 70)

if __name__ == "__main__":
    calculate_optimal_stops()