#!/usr/bin/env python3

import json
import datetime
from pathlib import Path
import yfinance as yf

class OrderGenerator:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.today = datetime.date.today()
        self.orders_path = self.base_path / "orders"
        self.orders_path.mkdir(exist_ok=True)
        
        # Load portfolio and risk rules
        with open(self.base_path / "data" / "portfolio.json") as f:
            self.portfolio = json.load(f)
        
        with open(self.base_path / "config" / "risk_rules.json") as f:
            self.risk_rules = json.load(f)
    
    def calculate_position_size(self, price, total_capital):
        """Calculate position size based on risk rules"""
        max_position_pct = self.risk_rules["position_sizing"]["max_position_size_percent"]
        max_position_dollars = self.risk_rules["position_sizing"]["max_position_size_dollars"]
        min_position_dollars = self.risk_rules["position_sizing"]["min_position_size_dollars"]
        
        # Calculate 2% of portfolio
        position_value = total_capital * (max_position_pct / 100)
        
        # Apply min/max constraints
        position_value = min(position_value, max_position_dollars)
        position_value = max(position_value, min_position_dollars)
        
        # Calculate shares
        shares = int(position_value / price)
        
        return shares, position_value
    
    def generate_orders(self):
        """Generate buy/sell orders based on analysis"""
        orders = []
        
        # Load screening results
        try:
            with open(self.base_path / "data" / "screening_results.json") as f:
                screening = json.load(f)
        except FileNotFoundError:
            print("No screening results found. Run stock_screener.py first.")
            return []
        
        # Load today's analysis if exists
        analysis_path = self.base_path / "analysis" / str(self.today) / "analysis.json"
        recommendations = []
        if analysis_path.exists():
            with open(analysis_path) as f:
                analysis = json.load(f)
                recommendations = analysis.get("portfolio_analysis", {}).get("recommendations", [])
        
        # Process SELL orders first (from recommendations)
        for rec in recommendations:
            if rec["action"] == "SELL":
                # SELL orders should be executed immediately at market open
                tomorrow = self.today + datetime.timedelta(days=1)
                if tomorrow.weekday() >= 5:  # If weekend, move to Monday
                    days_ahead = 7 - tomorrow.weekday()
                    tomorrow = tomorrow + datetime.timedelta(days=days_ahead)
                
                orders.append({
                    "action": "SELL",
                    "symbol": rec["symbol"],
                    "quantity": rec["quantity"],
                    "order_type": "MARKET",
                    "execute_by": f"{tomorrow} 09:30 AM ET",  # At market open
                    "reason": rec["reason"],
                    "priority": "HIGH"
                })
        
        # Calculate available cash after sells
        available_cash = self.portfolio["cash_balance"]
        
        # Process BUY opportunities (limit to 3 new positions)
        current_positions = len(self.portfolio["positions"])
        max_new_positions = min(3, self.risk_rules["diversification"]["max_positions"] - current_positions)
        
        top_opportunities = screening["results"][:max_new_positions]
        
        for opp in top_opportunities:
            if available_cash < self.risk_rules["position_sizing"]["min_position_size_dollars"]:
                break
            
            # Get current price
            ticker = yf.Ticker(opp["symbol"])
            current_price = ticker.info.get("currentPrice", opp["price"])
            
            # Calculate position size
            shares, position_value = self.calculate_position_size(current_price, self.portfolio["starting_balance"])
            
            if position_value <= available_cash:
                # Set execution time based on order priority
                # Opening bell orders for best liquidity
                tomorrow = self.today + datetime.timedelta(days=1)
                if tomorrow.weekday() >= 5:  # If weekend, move to Monday
                    days_ahead = 7 - tomorrow.weekday()
                    tomorrow = tomorrow + datetime.timedelta(days=days_ahead)
                
                execute_time = f"{tomorrow} 09:35 AM ET"  # 5 mins after market open
                
                orders.append({
                    "action": "BUY",
                    "symbol": opp["symbol"],
                    "quantity": shares,
                    "price": current_price,
                    "order_type": "LIMIT",
                    "limit_price": round(current_price * 1.01, 2),  # 1% above current
                    "execute_by": execute_time,
                    "valid_until": f"{tomorrow} 04:00 PM ET",
                    "reason": f"Momentum signal: {opp['week_change']:+.1f}% weekly, Volume spike: {opp['volume_spike']:+.0f}%",
                    "priority": "MEDIUM",
                    "metrics": {
                        "market_cap": opp["market_cap"],
                        "week_change": opp["week_change"],
                        "volume_spike": opp["volume_spike"]
                    }
                })
                
                available_cash -= position_value
        
        return orders
    
    def save_orders(self, orders):
        """Save orders to JSON and Markdown files"""
        # Save JSON
        json_path = self.orders_path / f"{self.today}.json"
        with open(json_path, 'w') as f:
            json.dump({
                "date": str(self.today),
                "generated_at": datetime.datetime.now().isoformat(),
                "orders": orders
            }, f, indent=2)
        
        # Save Markdown for easy reading
        md_path = self.orders_path / f"{self.today}.md"
        with open(md_path, 'w') as f:
            f.write(f"# Trading Orders for {self.today}\n\n")
            f.write(f"Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if not orders:
                f.write("No orders for today.\n")
            else:
                # Separate by priority
                high_priority = [o for o in orders if o.get("priority") == "HIGH"]
                medium_priority = [o for o in orders if o.get("priority") == "MEDIUM"]
                
                if high_priority:
                    f.write("## 🔴 HIGH PRIORITY (Execute First)\n\n")
                    for order in high_priority:
                        f.write(f"### {order['action']} {order['symbol']}\n")
                        f.write(f"- **Execute by:** {order['execute_by']}\n")
                        f.write(f"- Quantity: {order['quantity']} shares\n")
                        f.write(f"- Type: {order['order_type']}\n")
                        f.write(f"- Reason: {order['reason']}\n\n")
                
                if medium_priority:
                    f.write("## 🟡 MEDIUM PRIORITY\n\n")
                    for order in medium_priority:
                        f.write(f"### {order['action']} {order['symbol']}\n")
                        f.write(f"- **Execute by:** {order['execute_by']}\n")
                        f.write(f"- **Valid until:** {order.get('valid_until', 'End of day')}\n")
                        f.write(f"- Quantity: {order['quantity']} shares\n")
                        f.write(f"- Type: {order['order_type']}\n")
                        if order['order_type'] == 'LIMIT':
                            f.write(f"- Limit Price: ${order.get('limit_price', 'N/A')}\n")
                        f.write(f"- Reason: {order['reason']}\n\n")
        
        print(f"Orders saved to {json_path} and {md_path}")
        return json_path, md_path
    
    def run(self):
        print(f"Generating orders for {self.today}...")
        
        orders = self.generate_orders()
        
        if orders:
            print(f"\n📊 Generated {len(orders)} orders:")
            for order in orders:
                emoji = "🔴" if order["action"] == "SELL" else "🟢"
                print(f"{emoji} {order['action']} {order['quantity']} {order['symbol']} - {order['reason'][:50]}...")
            
            self.save_orders(orders)
        else:
            print("No orders generated for today.")
            self.save_orders([])
        
        return orders

if __name__ == "__main__":
    generator = OrderGenerator()
    generator.run()