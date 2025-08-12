#!/usr/bin/env python3

import json
import datetime
import yfinance as yf
from pathlib import Path
import pandas as pd

class DailyTradingAnalysis:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.today = datetime.date.today()
        self.analysis_path = self.base_path / "analysis" / str(self.today)
        self.analysis_path.mkdir(parents=True, exist_ok=True)
        
        with open(self.base_path / "config" / "risk_rules.json") as f:
            self.risk_rules = json.load(f)
        
        with open(self.base_path / "data" / "portfolio.json") as f:
            self.portfolio = json.load(f)
    
    def fetch_market_data(self, symbols):
        data = {}
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1mo")
            
            data[symbol] = {
                "current_price": info.get("currentPrice", 0),
                "market_cap": info.get("marketCap", 0),
                "volume": info.get("volume", 0),
                "avg_volume": info.get("averageVolume", 0),
                "52_week_high": info.get("fiftyTwoWeekHigh", 0),
                "52_week_low": info.get("fiftyTwoWeekLow", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "recent_prices": hist["Close"].tolist()[-5:] if not hist.empty else []
            }
        return data
    
    def screen_small_caps(self):
        # This would connect to a screener API
        # For now, return sample watchlist
        return ["AAPL", "MSFT", "GOOGL"]  # Replace with actual small-cap screening
    
    def check_congressional_trades(self):
        # This would connect to QuiverQuant or Capitol Trades API
        # For now, return sample data
        return {
            "recent_buys": [],
            "recent_sells": []
        }
    
    def analyze_positions(self):
        analysis = {
            "date": str(self.today),
            "portfolio_value": self.portfolio["cash_balance"],
            "positions": [],
            "recommendations": []
        }
        
        for position in self.portfolio["positions"]:
            symbol = position["symbol"]
            ticker = yf.Ticker(symbol)
            current_price = ticker.info.get("currentPrice", position["entry_price"])
            
            pnl = (current_price - position["entry_price"]) * position["quantity"]
            pnl_percent = ((current_price / position["entry_price"]) - 1) * 100
            
            # Check stop loss
            if pnl_percent <= -self.risk_rules["stop_loss"]["default_stop_loss_percent"]:
                analysis["recommendations"].append({
                    "action": "SELL",
                    "symbol": symbol,
                    "reason": "Stop loss triggered",
                    "quantity": position["quantity"]
                })
            
            analysis["positions"].append({
                "symbol": symbol,
                "quantity": position["quantity"],
                "entry_price": position["entry_price"],
                "current_price": current_price,
                "pnl": pnl,
                "pnl_percent": pnl_percent
            })
            
            analysis["portfolio_value"] += current_price * position["quantity"]
        
        return analysis
    
    def generate_opportunities(self):
        opportunities = []
        watchlist = self.screen_small_caps()
        market_data = self.fetch_market_data(watchlist)
        congressional = self.check_congressional_trades()
        
        for symbol, data in market_data.items():
            # Simple momentum check
            if len(data["recent_prices"]) >= 2:
                momentum = (data["recent_prices"][-1] / data["recent_prices"][0] - 1) * 100
                
                if momentum > 5 and data["volume"] > data["avg_volume"] * 1.5:
                    opportunities.append({
                        "symbol": symbol,
                        "signal": "momentum_volume",
                        "strength": "medium",
                        "current_price": data["current_price"],
                        "market_cap": data["market_cap"],
                        "momentum_5d": momentum
                    })
        
        return opportunities
    
    def save_analysis(self, analysis, opportunities):
        with open(self.analysis_path / "analysis.json", "w") as f:
            json.dump({
                "portfolio_analysis": analysis,
                "opportunities": opportunities,
                "timestamp": datetime.datetime.now().isoformat()
            }, f, indent=2)
    
    def run(self):
        print(f"Running daily analysis for {self.today}")
        
        analysis = self.analyze_positions()
        opportunities = self.generate_opportunities()
        
        self.save_analysis(analysis, opportunities)
        
        print(f"Portfolio value: ${analysis['portfolio_value']:,.2f}")
        print(f"Found {len(opportunities)} opportunities")
        print(f"Generated {len(analysis['recommendations'])} recommendations")
        
        return analysis, opportunities

if __name__ == "__main__":
    analyzer = DailyTradingAnalysis()
    analyzer.run()