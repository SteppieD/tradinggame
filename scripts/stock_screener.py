#!/usr/bin/env python3

import yfinance as yf
import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path
from technical_analysis import TechnicalAnalyzer
try:
    from alpha_vantage_client import AlphaVantageClient
    alpha_vantage = AlphaVantageClient()
except:
    alpha_vantage = None

class SmallCapScreener:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.technical_analyzer = TechnicalAnalyzer()
        
    def get_small_cap_tickers(self):
        """Get a list of small-cap stocks to analyze"""
        # Popular small-cap ETF holdings as a starting point
        # In production, this would connect to a proper screener API
        small_cap_etfs = ['IWM', 'IJR', 'VBR']  # Russell 2000, S&P SmallCap, Vanguard SmallCap
        
        # For now, return some known small-caps with good liquidity
        # These are examples - replace with actual screening logic
        return [
            'APPS', 'BBBY', 'CLOV', 'WISH', 'ATER', 'PROG', 'XELA', 'SDC',
            'GEVO', 'FCEL', 'PLUG', 'RIG', 'TLRY', 'SNDL', 'HEXO', 'ACB',
            'WKHS', 'RIDE', 'NKLA', 'HYLN', 'FSR', 'GOEV', 'ARVL', 'LCID',
            'RIVN', 'CHPT', 'EVGO', 'BLNK', 'VLDR', 'LAZR', 'AEVA', 'OUST'
        ]
    
    def screen_stocks(self, min_price=1, max_price=50, min_volume=500000):
        """Screen small-cap stocks based on criteria"""
        tickers = self.get_small_cap_tickers()
        screened = []
        
        for symbol in tickers:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                # Get basic screening data
                current_price = info.get('currentPrice', 0)
                market_cap = info.get('marketCap', 0)
                volume = info.get('volume', 0)
                avg_volume = info.get('averageVolume', 0)
                
                # Apply filters
                if (min_price <= current_price <= max_price and 
                    volume >= min_volume and
                    50_000_000 <= market_cap <= 2_000_000_000):  # $50M - $2B market cap
                    
                    # Get recent price action
                    hist = ticker.history(period="1mo")
                    if not hist.empty:
                        # Calculate momentum indicators
                        week_change = (hist['Close'][-1] / hist['Close'][-5] - 1) * 100 if len(hist) >= 5 else 0
                        month_change = (hist['Close'][-1] / hist['Close'][0] - 1) * 100
                        
                        # Volume spike detection
                        recent_volume = hist['Volume'][-5:].mean() if len(hist) >= 5 else volume
                        volume_spike = (volume / avg_volume - 1) * 100 if avg_volume > 0 else 0
                        
                        # Add technical analysis
                        tech_signals = self.technical_analyzer.generate_technical_signals(symbol)
                        
                        screened.append({
                            'symbol': symbol,
                            'price': current_price,
                            'market_cap': market_cap,
                            'volume': volume,
                            'avg_volume': avg_volume,
                            'volume_spike': round(volume_spike, 2),
                            'week_change': round(week_change, 2),
                            'month_change': round(month_change, 2),
                            'pe_ratio': info.get('trailingPE', None),
                            'sector': info.get('sector', 'Unknown'),
                            'industry': info.get('industry', 'Unknown'),
                            'technical_signal': tech_signals.get('overall_signal', 'NEUTRAL'),
                            'technical_confidence': tech_signals.get('confidence', 0),
                            'fibonacci_support': tech_signals['levels']['support_levels'][0] if tech_signals['levels'].get('support_levels') else None,
                            'fibonacci_resistance': tech_signals['levels']['resistance_levels'][0] if tech_signals['levels'].get('resistance_levels') else None
                        })
                        
                        print(f"✓ {symbol}: ${current_price:.2f}, MCap: ${market_cap/1e6:.0f}M")
                        
            except Exception as e:
                print(f"✗ Error screening {symbol}: {e}")
                continue
        
        # Sort by momentum + volume spike
        screened.sort(key=lambda x: x['week_change'] + (x['volume_spike'] / 10), reverse=True)
        
        return screened
    
    def save_screening_results(self, results):
        """Save screening results to JSON"""
        output_path = self.base_path / "data" / "screening_results.json"
        
        with open(output_path, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'date': str(datetime.now().date()),
                'results': results[:20]  # Top 20 opportunities
            }, f, indent=2)
        
        print(f"\nSaved {len(results[:20])} top opportunities to {output_path}")
        
        return results[:20]
    
    def get_congressional_movers(self):
        """Placeholder for congressional trading data"""
        # This would connect to QuiverQuant or Capitol Trades API
        # For now, return empty list
        return []
    
    def run(self):
        print("Screening small-cap stocks...")
        results = self.screen_stocks()
        
        if results:
            top_picks = self.save_screening_results(results)
            
            print("\n🎯 Top 5 Opportunities:")
            for i, stock in enumerate(top_picks[:5], 1):
                print(f"{i}. {stock['symbol']}: ${stock['price']:.2f} | "
                      f"Week: {stock['week_change']:+.1f}% | "
                      f"Vol Spike: {stock['volume_spike']:+.0f}%")
        else:
            print("No stocks passed screening criteria")
        
        return results

if __name__ == "__main__":
    screener = SmallCapScreener()
    screener.run()