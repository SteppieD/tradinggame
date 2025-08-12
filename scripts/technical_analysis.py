#!/usr/bin/env python3

import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import json

class TechnicalAnalyzer:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        
        # Fibonacci retracement levels
        self.fib_levels = {
            '0%': 0.0,
            '23.6%': 0.236,
            '38.2%': 0.382,
            '50%': 0.5,
            '61.8%': 0.618,
            '78.6%': 0.786,
            '100%': 1.0
        }
        
        # Common moving averages
        self.ma_periods = {
            'short': 20,   # 20-day
            'medium': 50,  # 50-day
            'long': 200    # 200-day
        }
    
    def calculate_fibonacci_levels(self, symbol, period='3mo'):
        """Calculate Fibonacci retracement levels for support and resistance"""
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            return None
        
        # Find swing high and low
        high = hist['High'].max()
        low = hist['Low'].min()
        diff = high - low
        
        # Calculate Fibonacci levels
        fib_data = {
            'symbol': symbol,
            'period': period,
            'swing_high': high,
            'swing_low': low,
            'current_price': hist['Close'].iloc[-1],
            'levels': {}
        }
        
        # Calculate each Fibonacci level
        for name, ratio in self.fib_levels.items():
            level = high - (diff * ratio)
            fib_data['levels'][name] = round(level, 2)
        
        # Determine current position relative to Fib levels
        current = fib_data['current_price']
        
        # Find nearest support and resistance
        support = None
        resistance = None
        
        for name, level in fib_data['levels'].items():
            if level < current and (support is None or level > support['price']):
                support = {'level': name, 'price': level}
            elif level > current and (resistance is None or level < resistance['price']):
                resistance = {'level': name, 'price': level}
        
        fib_data['nearest_support'] = support
        fib_data['nearest_resistance'] = resistance
        
        # Calculate position strength (0-100 scale)
        if support and resistance:
            position_in_range = (current - support['price']) / (resistance['price'] - support['price'])
            fib_data['position_strength'] = round(position_in_range * 100, 1)
        
        return fib_data
    
    def calculate_moving_averages(self, symbol, period='6mo'):
        """Calculate various moving averages"""
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            return None
        
        ma_data = {
            'symbol': symbol,
            'current_price': hist['Close'].iloc[-1],
            'moving_averages': {}
        }
        
        # Calculate each MA
        for name, days in self.ma_periods.items():
            if len(hist) >= days:
                ma = hist['Close'].rolling(window=days).mean().iloc[-1]
                ma_data['moving_averages'][f'MA{days}'] = round(ma, 2)
                
                # Check if price is above or below MA
                ma_data[f'above_MA{days}'] = ma_data['current_price'] > ma
        
        # Golden Cross / Death Cross detection
        if 'MA50' in ma_data['moving_averages'] and 'MA200' in ma_data['moving_averages']:
            ma50_prev = hist['Close'].rolling(window=50).mean().iloc[-2] if len(hist) > 50 else None
            ma200_prev = hist['Close'].rolling(window=200).mean().iloc[-2] if len(hist) > 200 else None
            
            if ma50_prev and ma200_prev:
                # Golden Cross: MA50 crosses above MA200
                if ma50_prev < ma200_prev and ma_data['moving_averages']['MA50'] > ma_data['moving_averages']['MA200']:
                    ma_data['signal'] = 'GOLDEN_CROSS'
                # Death Cross: MA50 crosses below MA200
                elif ma50_prev > ma200_prev and ma_data['moving_averages']['MA50'] < ma_data['moving_averages']['MA200']:
                    ma_data['signal'] = 'DEATH_CROSS'
        
        return ma_data
    
    def calculate_rsi(self, symbol, period='1mo', window=14):
        """Calculate Relative Strength Index"""
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty or len(hist) < window:
            return None
        
        # Calculate price changes
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        # Calculate RS and RSI
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        current_rsi = rsi.iloc[-1]
        
        rsi_data = {
            'symbol': symbol,
            'rsi': round(current_rsi, 2),
            'condition': 'OVERBOUGHT' if current_rsi > 70 else 'OVERSOLD' if current_rsi < 30 else 'NEUTRAL'
        }
        
        return rsi_data
    
    def calculate_bollinger_bands(self, symbol, period='1mo', window=20, num_std=2):
        """Calculate Bollinger Bands"""
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty or len(hist) < window:
            return None
        
        # Calculate bands
        sma = hist['Close'].rolling(window=window).mean()
        std = hist['Close'].rolling(window=window).std()
        
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        
        current_price = hist['Close'].iloc[-1]
        current_upper = upper_band.iloc[-1]
        current_lower = lower_band.iloc[-1]
        current_sma = sma.iloc[-1]
        
        # Calculate band width and position
        band_width = current_upper - current_lower
        position_in_band = (current_price - current_lower) / band_width if band_width > 0 else 0.5
        
        bb_data = {
            'symbol': symbol,
            'current_price': round(current_price, 2),
            'upper_band': round(current_upper, 2),
            'middle_band': round(current_sma, 2),
            'lower_band': round(current_lower, 2),
            'band_width': round(band_width, 2),
            'position_percent': round(position_in_band * 100, 1),
            'signal': 'OVERBOUGHT' if position_in_band > 0.95 else 'OVERSOLD' if position_in_band < 0.05 else 'NEUTRAL'
        }
        
        return bb_data
    
    def analyze_volume_profile(self, symbol, period='1mo'):
        """Analyze volume patterns"""
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if hist.empty:
            return None
        
        avg_volume = hist['Volume'].mean()
        recent_volume = hist['Volume'].iloc[-5:].mean()  # Last 5 days
        current_volume = hist['Volume'].iloc[-1]
        
        # Volume spike detection
        volume_spike = (current_volume / avg_volume - 1) * 100 if avg_volume > 0 else 0
        
        # Price-volume correlation
        price_change = (hist['Close'].iloc[-1] / hist['Close'].iloc[-2] - 1) * 100
        
        volume_data = {
            'symbol': symbol,
            'current_volume': int(current_volume),
            'avg_volume': int(avg_volume),
            'recent_avg_volume': int(recent_volume),
            'volume_spike_percent': round(volume_spike, 1),
            'price_change_percent': round(price_change, 2),
            'volume_trend': 'INCREASING' if recent_volume > avg_volume * 1.2 else 'DECREASING' if recent_volume < avg_volume * 0.8 else 'STABLE',
            'signal': 'BULLISH' if volume_spike > 50 and price_change > 0 else 'BEARISH' if volume_spike > 50 and price_change < 0 else 'NEUTRAL'
        }
        
        return volume_data
    
    def get_support_resistance_levels(self, symbol):
        """Combine Fibonacci with other methods to find key levels"""
        fib = self.calculate_fibonacci_levels(symbol)
        ma = self.calculate_moving_averages(symbol)
        
        levels = {
            'symbol': symbol,
            'support_levels': [],
            'resistance_levels': [],
            'current_price': fib['current_price'] if fib else 0
        }
        
        if fib:
            # Add Fibonacci support levels
            if fib.get('nearest_support'):
                levels['support_levels'].append({
                    'type': 'FIBONACCI',
                    'level': fib['nearest_support']['level'],
                    'price': fib['nearest_support']['price'],
                    'strength': 'STRONG' if fib['nearest_support']['level'] in ['38.2%', '50%', '61.8%'] else 'MEDIUM'
                })
            
            # Add Fibonacci resistance levels
            if fib.get('nearest_resistance'):
                levels['resistance_levels'].append({
                    'type': 'FIBONACCI',
                    'level': fib['nearest_resistance']['level'],
                    'price': fib['nearest_resistance']['price'],
                    'strength': 'STRONG' if fib['nearest_resistance']['level'] in ['38.2%', '50%', '61.8%'] else 'MEDIUM'
                })
        
        if ma and ma.get('moving_averages'):
            # Add MA support/resistance
            current = levels['current_price']
            for ma_name, ma_value in ma['moving_averages'].items():
                if ma_value < current:
                    levels['support_levels'].append({
                        'type': 'MOVING_AVG',
                        'level': ma_name,
                        'price': ma_value,
                        'strength': 'STRONG' if ma_name == 'MA200' else 'MEDIUM'
                    })
                else:
                    levels['resistance_levels'].append({
                        'type': 'MOVING_AVG',
                        'level': ma_name,
                        'price': ma_value,
                        'strength': 'STRONG' if ma_name == 'MA200' else 'MEDIUM'
                    })
        
        # Sort levels by distance from current price
        levels['support_levels'].sort(key=lambda x: x['price'], reverse=True)
        levels['resistance_levels'].sort(key=lambda x: x['price'])
        
        return levels
    
    def generate_technical_signals(self, symbol):
        """Generate comprehensive technical analysis signals"""
        signals = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'indicators': {},
            'signals': [],
            'overall_signal': 'NEUTRAL',
            'confidence': 0
        }
        
        # Fibonacci Analysis
        fib = self.calculate_fibonacci_levels(symbol)
        if fib:
            signals['indicators']['fibonacci'] = fib
            if fib.get('position_strength'):
                if fib['position_strength'] < 30:
                    signals['signals'].append({
                        'type': 'FIBONACCI',
                        'signal': 'BUY',
                        'reason': f"Near Fibonacci support at {fib['nearest_support']['level']}",
                        'strength': 'STRONG' if fib['position_strength'] < 20 else 'MEDIUM'
                    })
                elif fib['position_strength'] > 70:
                    signals['signals'].append({
                        'type': 'FIBONACCI',
                        'signal': 'SELL',
                        'reason': f"Near Fibonacci resistance at {fib['nearest_resistance']['level']}",
                        'strength': 'STRONG' if fib['position_strength'] > 80 else 'MEDIUM'
                    })
        
        # Moving Averages
        ma = self.calculate_moving_averages(symbol)
        if ma:
            signals['indicators']['moving_averages'] = ma
            if ma.get('signal') == 'GOLDEN_CROSS':
                signals['signals'].append({
                    'type': 'MA_CROSS',
                    'signal': 'BUY',
                    'reason': 'Golden Cross detected (MA50 > MA200)',
                    'strength': 'STRONG'
                })
            elif ma.get('signal') == 'DEATH_CROSS':
                signals['signals'].append({
                    'type': 'MA_CROSS',
                    'signal': 'SELL',
                    'reason': 'Death Cross detected (MA50 < MA200)',
                    'strength': 'STRONG'
                })
        
        # RSI
        rsi = self.calculate_rsi(symbol)
        if rsi:
            signals['indicators']['rsi'] = rsi
            if rsi['condition'] == 'OVERSOLD':
                signals['signals'].append({
                    'type': 'RSI',
                    'signal': 'BUY',
                    'reason': f"RSI oversold at {rsi['rsi']}",
                    'strength': 'MEDIUM'
                })
            elif rsi['condition'] == 'OVERBOUGHT':
                signals['signals'].append({
                    'type': 'RSI',
                    'signal': 'SELL',
                    'reason': f"RSI overbought at {rsi['rsi']}",
                    'strength': 'MEDIUM'
                })
        
        # Bollinger Bands
        bb = self.calculate_bollinger_bands(symbol)
        if bb:
            signals['indicators']['bollinger_bands'] = bb
            if bb['signal'] == 'OVERSOLD':
                signals['signals'].append({
                    'type': 'BOLLINGER',
                    'signal': 'BUY',
                    'reason': 'Price at lower Bollinger Band',
                    'strength': 'MEDIUM'
                })
            elif bb['signal'] == 'OVERBOUGHT':
                signals['signals'].append({
                    'type': 'BOLLINGER',
                    'signal': 'SELL',
                    'reason': 'Price at upper Bollinger Band',
                    'strength': 'MEDIUM'
                })
        
        # Volume Analysis
        volume = self.analyze_volume_profile(symbol)
        if volume:
            signals['indicators']['volume'] = volume
            if volume['signal'] == 'BULLISH':
                signals['signals'].append({
                    'type': 'VOLUME',
                    'signal': 'BUY',
                    'reason': f"Volume spike {volume['volume_spike_percent']:.1f}% with positive price action",
                    'strength': 'MEDIUM'
                })
        
        # Calculate overall signal
        buy_signals = [s for s in signals['signals'] if s['signal'] == 'BUY']
        sell_signals = [s for s in signals['signals'] if s['signal'] == 'SELL']
        
        strong_buys = [s for s in buy_signals if s['strength'] == 'STRONG']
        strong_sells = [s for s in sell_signals if s['strength'] == 'STRONG']
        
        if len(strong_buys) > len(strong_sells):
            signals['overall_signal'] = 'STRONG_BUY'
            signals['confidence'] = min(95, 50 + len(strong_buys) * 15)
        elif len(buy_signals) > len(sell_signals):
            signals['overall_signal'] = 'BUY'
            signals['confidence'] = min(80, 40 + len(buy_signals) * 10)
        elif len(strong_sells) > len(strong_buys):
            signals['overall_signal'] = 'STRONG_SELL'
            signals['confidence'] = min(95, 50 + len(strong_sells) * 15)
        elif len(sell_signals) > len(buy_signals):
            signals['overall_signal'] = 'SELL'
            signals['confidence'] = min(80, 40 + len(sell_signals) * 10)
        else:
            signals['overall_signal'] = 'NEUTRAL'
            signals['confidence'] = 50
        
        # Get support/resistance levels
        signals['levels'] = self.get_support_resistance_levels(symbol)
        
        return signals
    
    def save_analysis(self, symbol, analysis):
        """Save technical analysis to file"""
        output_path = self.base_path / "analysis" / "technical" / f"{symbol}_{datetime.now().date()}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert numpy types to Python types for JSON serialization
        def convert_to_serializable(obj):
            if isinstance(obj, np.bool_):
                return bool(obj)
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_serializable(item) for item in obj]
            return obj
        
        serializable_analysis = convert_to_serializable(analysis)
        
        with open(output_path, 'w') as f:
            json.dump(serializable_analysis, f, indent=2, default=str)
        
        return output_path
    
    def analyze_multiple(self, symbols):
        """Analyze multiple symbols"""
        results = []
        
        for symbol in symbols:
            print(f"Analyzing {symbol}...")
            analysis = self.generate_technical_signals(symbol)
            results.append(analysis)
            self.save_analysis(symbol, analysis)
            
            # Print summary
            print(f"  Signal: {analysis['overall_signal']} (Confidence: {analysis['confidence']}%)")
            if analysis['levels']['support_levels']:
                support = analysis['levels']['support_levels'][0]
                print(f"  Support: ${support['price']:.2f} ({support['type']})")
            if analysis['levels']['resistance_levels']:
                resistance = analysis['levels']['resistance_levels'][0]
                print(f"  Resistance: ${resistance['price']:.2f} ({resistance['type']})")
        
        return results

if __name__ == "__main__":
    analyzer = TechnicalAnalyzer()
    
    # Test with some symbols
    test_symbols = ['SNDL', 'ACB', 'OUST']
    
    print("📊 Technical Analysis with Fibonacci Retracements")
    print("=" * 50)
    
    for symbol in test_symbols:
        print(f"\n{symbol} Analysis:")
        print("-" * 30)
        
        # Get full analysis
        signals = analyzer.generate_technical_signals(symbol)
        
        # Print Fibonacci levels
        if 'fibonacci' in signals['indicators']:
            fib = signals['indicators']['fibonacci']
            print(f"Current Price: ${fib['current_price']:.2f}")
            if fib.get('nearest_support'):
                print(f"Fibonacci Support: ${fib['nearest_support']['price']:.2f} ({fib['nearest_support']['level']})")
            if fib.get('nearest_resistance'):
                print(f"Fibonacci Resistance: ${fib['nearest_resistance']['price']:.2f} ({fib['nearest_resistance']['level']})")
            if fib.get('position_strength'):
                print(f"Position Strength: {fib['position_strength']:.1f}%")
        
        # Print overall signal
        print(f"\nOverall Signal: {signals['overall_signal']}")
        print(f"Confidence: {signals['confidence']}%")
        
        # Print individual signals
        if signals['signals']:
            print("\nSignals:")
            for sig in signals['signals']:
                print(f"  • {sig['type']}: {sig['signal']} - {sig['reason']}")
        
        # Save analysis
        analyzer.save_analysis(symbol, signals)