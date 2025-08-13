#!/usr/bin/env python3

"""
Smart Stop Loss Calculator
Uses volatility, Fibonacci levels, and position P&L to calculate optimal stops
"""

import math
from typing import Dict, Tuple

def calculate_fibonacci_levels(entry_price: float, current_price: float) -> Dict[str, float]:
    """
    Calculate Fibonacci retracement levels from entry to current price
    """
    price_range = current_price - entry_price
    
    levels = {
        'current': current_price,
        'fib_236': current_price - (price_range * 0.236),  # 23.6% retracement
        'fib_382': current_price - (price_range * 0.382),  # 38.2% retracement
        'fib_500': current_price - (price_range * 0.500),  # 50% retracement
        'fib_618': current_price - (price_range * 0.618),  # 61.8% retracement
        'entry': entry_price,
        'fib_786': current_price - (price_range * 0.786),  # 78.6% retracement
    }
    
    return levels

def estimate_volatility(symbol: str, current_price: float) -> float:
    """
    Estimate daily volatility for small-cap EV/clean energy stocks
    Returns percentage volatility
    """
    # Base volatility for small-cap clean energy
    base_volatility = {
        'CHPT': 0.045,  # ~4.5% daily volatility
        'EVGO': 0.055,  # ~5.5% daily volatility  
        'FCEL': 0.060,  # ~6% daily volatility
    }
    
    # Adjust for price level (lower prices = higher % volatility)
    if current_price < 5:
        volatility_multiplier = 1.3
    elif current_price < 10:
        volatility_multiplier = 1.1
    else:
        volatility_multiplier = 1.0
    
    return base_volatility.get(symbol, 0.05) * volatility_multiplier

def calculate_smart_stop(
    symbol: str,
    entry_price: float, 
    current_price: float,
    quantity: int
) -> Dict[str, any]:
    """
    Calculate intelligent stop loss based on multiple factors
    """
    # Calculate P&L
    pnl_dollars = (current_price - entry_price) * quantity
    pnl_percent = ((current_price - entry_price) / entry_price) * 100
    
    # Get Fibonacci levels
    fib_levels = calculate_fibonacci_levels(entry_price, current_price)
    
    # Estimate volatility
    daily_volatility = estimate_volatility(symbol, current_price)
    atr_stop = current_price * (1 - daily_volatility * 1.5)  # 1.5x ATR
    
    # Determine stop strategy based on P&L
    if pnl_percent < 0:
        # Position is at a loss - use wider stop
        stop_price = entry_price * 0.90  # -10% from entry
        stop_strategy = "PROTECT_CAPITAL"
        stop_reason = "Position at loss - using -10% disaster stop"
        
    elif pnl_percent < 2:
        # Small gain - protect against full loss
        stop_price = max(
            entry_price * 0.95,  # -5% from entry
            atr_stop  # Or ATR-based stop
        )
        stop_strategy = "TIGHT_STOP"
        stop_reason = f"Small gain ({pnl_percent:.1f}%) - tight stop at -5% from entry"
        
    elif pnl_percent < 5:
        # Moderate gain - use Fibonacci or ATR
        fib_stop = fib_levels['fib_618']  # 61.8% retracement
        stop_price = max(
            fib_stop,
            entry_price,  # Never below break-even
            atr_stop
        )
        stop_strategy = "FIBONACCI_STOP"
        stop_reason = f"Moderate gain ({pnl_percent:.1f}%) - stop at 61.8% Fib or break-even"
        
    elif pnl_percent < 10:
        # Good gain - trail more aggressively
        fib_stop = fib_levels['fib_382']  # 38.2% retracement
        trail_stop = current_price * 0.95  # 5% trail
        stop_price = max(
            fib_stop,
            trail_stop,
            entry_price * 1.02  # Lock in 2% profit minimum
        )
        stop_strategy = "TRAIL_STOP"
        stop_reason = f"Good gain ({pnl_percent:.1f}%) - trailing at 38.2% Fib"
        
    else:
        # Excellent gain - tight trail
        trail_stop = current_price * 0.97  # 3% trail
        stop_price = max(
            trail_stop,
            entry_price * 1.05  # Lock in 5% profit minimum
        )
        stop_strategy = "TIGHT_TRAIL"
        stop_reason = f"Excellent gain ({pnl_percent:.1f}%) - tight 3% trail"
    
    # Calculate limit price (slightly below stop for slippage)
    limit_price = stop_price * 0.995
    
    # Calculate risk metrics
    distance_from_current = ((current_price - stop_price) / current_price) * 100
    risk_dollars = (current_price - stop_price) * quantity
    
    return {
        'symbol': symbol,
        'current_price': current_price,
        'entry_price': entry_price,
        'stop_price': round(stop_price, 2),
        'limit_price': round(limit_price, 2),
        'strategy': stop_strategy,
        'reason': stop_reason,
        'pnl_percent': round(pnl_percent, 2),
        'distance_percent': round(distance_from_current, 1),
        'risk_dollars': round(risk_dollars, 2),
        'fib_levels': {k: round(v, 2) for k, v in fib_levels.items()},
        'daily_volatility': round(daily_volatility * 100, 1),
        'quantity': quantity
    }

def get_stop_recommendations(positions: list, prices: dict) -> list:
    """
    Get stop recommendations for all positions
    """
    recommendations = []
    
    for position in positions:
        symbol = position['symbol']
        if symbol in prices:
            stop_data = calculate_smart_stop(
                symbol=symbol,
                entry_price=position['entry_price'],
                current_price=prices[symbol]['price'],
                quantity=position['quantity']
            )
            recommendations.append(stop_data)
    
    return recommendations

# Example usage
if __name__ == "__main__":
    # Test with current positions
    positions = [
        {'symbol': 'CHPT', 'entry_price': 10.7845, 'quantity': 26},
        {'symbol': 'EVGO', 'entry_price': 3.6271, 'quantity': 82},
        {'symbol': 'FCEL', 'entry_price': 4.05, 'quantity': 97}
    ]
    
    prices = {
        'CHPT': {'price': 11.08},
        'EVGO': {'price': 3.76},
        'FCEL': {'price': 4.09}
    }
    
    print("=" * 60)
    print("SMART STOP LOSS RECOMMENDATIONS")
    print("=" * 60)
    
    recommendations = get_stop_recommendations(positions, prices)
    
    for rec in recommendations:
        print(f"\n{rec['symbol']}:")
        print(f"  Current: ${rec['current_price']:.2f} (Entry: ${rec['entry_price']:.2f})")
        print(f"  P&L: {rec['pnl_percent']:+.1f}%")
        print(f"  Daily Volatility: ±{rec['daily_volatility']}%")
        print(f"  Strategy: {rec['strategy']}")
        print(f"  Stop: ${rec['stop_price']} (Limit: ${rec['limit_price']})")
        print(f"  Distance: -{rec['distance_percent']}% from current")
        print(f"  Risk: ${rec['risk_dollars']}")
        print(f"  Reason: {rec['reason']}")
        print(f"  Key Levels:")
        print(f"    - 38.2% Fib: ${rec['fib_levels']['fib_382']}")
        print(f"    - 50% Fib: ${rec['fib_levels']['fib_500']}")
        print(f"    - 61.8% Fib: ${rec['fib_levels']['fib_618']}")