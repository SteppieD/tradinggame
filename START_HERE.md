# 🚀 Claude Trading System - Quick Start Guide

## Your Trading Dashboard is Ready!

### 📊 View Your Dashboard
The dashboard is currently running at: http://localhost:8080/dashboard.html

To restart the dashboard anytime:
```bash
python run_dashboard.py
```

## 💼 Today's Trading Orders (August 12, 2025)

### Execute at 9:35 AM ET:
1. **BUY 49 SNDL** @ $2.03 limit (~$99)
2. **BUY 19 ACB** @ $5.26 limit (~$100)
3. **BUY 3 OUST** @ $28.16 limit (~$84)

**Total Investment:** $284 of your $1,000 capital

## 🔄 Daily Workflow

### Morning (Pre-Market)
1. Run the screener to find opportunities:
   ```bash
   python scripts/stock_screener.py
   ```

2. Generate trading orders:
   ```bash
   python scripts/order_generator.py
   ```

3. View orders in `orders/TODAYS_TRADES.md`

### During Market Hours
- Execute orders manually at specified times
- Monitor positions on dashboard
- Set stop-losses after fills

### End of Day
- Run analysis:
   ```bash
   python scripts/daily_analysis.py
   ```

## 📁 Project Structure
- **dashboard.html** - Visual interface for trades
- **orders/** - Daily trading instructions
- **data/** - Portfolio and screening results
- **scripts/** - Analysis and order generation
- **config/** - Risk rules and settings

## 🎯 Current Strategy
- **Focus:** Small-cap momentum stocks ($50M-$2B)
- **Signals:** Volume spikes + price momentum
- **Risk:** 10% position size, 10% stop-loss
- **Capital:** $1,000 starting balance

## 📈 Top Opportunities Found
1. **SNDL** - Cannabis, +21% weekly, 491% volume spike
2. **ACB** - Cannabis, +13% weekly, 512% volume spike
3. **OUST** - LiDAR tech, +16% weekly, 47% volume spike

## ⚠️ Risk Management
- Maximum 10% per position
- 10% stop-loss on all trades
- Maximum 5% daily portfolio loss
- Keep 70% cash initially

## 🔮 Next Features to Add
- Congressional trading tracker (QuiverQuant API)
- News sentiment analysis
- Automated performance tracking
- Trading journal with lessons learned

---

**Remember:** This is an experiment. Start small, track everything, and learn from each trade!