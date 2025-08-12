# 🚀 Setup Guide - AI Trading Assistant

This guide will help you set up your own AI-powered trading assistant using Claude Code.

## Prerequisites

- **Claude Code** installed ([claude.ai/code](https://claude.ai/code))
- **Python 3.8+** installed
- **Git** installed
- A brokerage account (supports any broker)
- **Alpha Vantage API key** (free at [alphavantage.co](https://www.alphavantage.co/support/#api-key))

## 🎯 Quick Start (5 minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/SteppieD/tradinggame.git
cd tradinggame
```

### 2. Run Setup Script

```bash
python setup.py
```

This will:
- Install Python dependencies
- Create necessary directories
- Initialize your portfolio
- Configure your broker settings
- Set up API connections

### 3. Configure Your Broker

Edit `config/broker_settings.json` with your broker's information:

```json
{
  "broker_name": "Your Broker Name",
  "account_type": "TFSA/RRSP/Cash/Margin",
  "commission_per_trade": 6.95,
  "currency": "CAD",
  "starting_balance": 1000
}
```

### 4. Add Alpha Vantage API Key

Create a `.env` file in the root directory:

```bash
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

### 5. Launch the Dashboard

```bash
open dashboard.html
```

## 📊 Using Claude Code Agents

### Available AI Agents

The system includes specialized Claude Code agents for different tasks:

#### Market Analysis
- **small-cap-screener** - Finds momentum opportunities in small-cap stocks
- **market-researcher** - Performs fundamental analysis and sector research
- **quant-analyst** - Generates technical signals and chart patterns
- **earnings-calendar** - Tracks earnings events and analyzes reactions

#### Risk Management
- **risk-manager** - Portfolio risk assessment and position sizing
- **trading-journal** - Records and analyzes your trading patterns

#### News & Sentiment
- **news-sentiment** - Real-time news monitoring and sentiment analysis

### How to Use Agents with Claude Code

1. **Open Claude Code** in your project directory:
```bash
cd tradinggame
claude-code
```

2. **Ask Claude to run analysis**:
```
"Use the small-cap-screener agent to find today's momentum plays"
```

3. **Generate daily orders**:
```
"Generate today's trading orders based on our strategy"
```

4. **Review positions**:
```
"Analyze my current positions and suggest stop-loss adjustments"
```

## 📝 Daily Workflow

### Morning Routine (Before Market Open)

1. **Run Market Analysis**
```bash
# In Claude Code
"Screen for today's opportunities and generate orders"
```

2. **Review Generated Orders**
```bash
python scripts/order_generator.py
```

3. **Check Position Management**
- Open `dashboard.html`
- Review Position Management Tracker
- Note any positions approaching action levels

### During Trading Hours

1. **Record Your Trades**
- Copy trade confirmations from your broker
- Paste into `PASTE_TRADES_HERE.py`
- Run: `python PASTE_TRADES_HERE.py`

2. **Monitor Positions**
- Dashboard auto-updates with real-time prices
- Watch for stop-loss and profit target alerts

### End of Day

1. **Review Performance**
```bash
python scripts/benchmark_summary.py
```

2. **Update Journal**
```bash
# In Claude Code
"Update my trading journal with today's lessons"
```

## 🛠️ Customization

### Modify Trading Strategy

Edit `config/risk_rules.json`:

```json
{
  "max_position_size_percent": 10,
  "max_concurrent_positions": 5,
  "stop_loss_percent": 10,
  "break_even_trigger": 5,
  "trailing_stop_percent": 10,
  "profit_target_percent": 15
}
```

### Add Custom Screening Criteria

Edit `scripts/stock_screener.py` to add your criteria:
- Market cap ranges
- Volume requirements
- Technical indicators
- Sector preferences

### Customize Dashboard

Edit `dashboard.html` to:
- Change color schemes
- Add new metrics
- Modify position trackers
- Include additional charts

## 🔄 Connecting Your Broker

### Supported Features by Broker Type

| Feature | Manual Entry | API Connected |
|---------|--------------|---------------|
| Trade Recording | ✅ Copy/Paste | ✅ Automatic |
| Real-time Prices | ✅ Alpha Vantage | ✅ Broker Feed |
| Order Generation | ✅ Manual Execute | ✅ Auto Submit |
| Stop-Loss Tracking | ✅ Manual Track | ✅ Auto Monitor |

### Manual Trading (Default)
- Copy trades from broker
- Paste into `PASTE_TRADES_HERE.py`
- Execute generated orders manually

### API Integration (Advanced)
For brokers with APIs (Interactive Brokers, Alpaca, etc.):
1. Install broker's Python library
2. Add credentials to `.env`
3. Enable auto-trading in `config/broker_settings.json`

## 📈 Performance Tracking

### Automatic Benchmark Comparison
- Tracks your performance vs S&P 500 (SPY) and Russell 2000 (IWM)
- Automatically captures benchmark prices when you record trades
- Shows real-time alpha generation

### View Reports
```bash
# Performance summary
python scripts/benchmark_summary.py

# Detailed analytics
python scripts/portfolio_tracker.py --report
```

## 🤖 Advanced Claude Code Usage

### Custom Analysis Prompts

```
"Analyze NEWS for my positions and suggest if I should adjust stops"

"Compare my portfolio sector allocation to the Russell 2000"

"Find correlations between my winning and losing trades"

"Generate a weekly performance report with insights"
```

### Batch Operations

```
"For each position, calculate the optimal trailing stop based on volatility"

"Screen all clean energy stocks under $5 with momentum"

"Update all stop losses to break-even for positions up >5%"
```

## 🐛 Troubleshooting

### Common Issues

**Dashboard won't update prices**
- Check Alpha Vantage API key in `.env`
- Verify you haven't exceeded 25 daily API calls
- Try: `python scripts/alpha_vantage_client.py --test`

**Trades not recording**
- Ensure trade format matches examples
- Check `data/` directory permissions
- Review `logs/trade_parser.log`

**Claude Code agents not working**
- Update Claude Code: `claude-code --update`
- Verify agent names in prompts
- Check `agents/` directory exists

## 🎓 Learning Resources

### Video Tutorials
- [YouTube: AI Business Lab](https://www.youtube.com/@aibusiness-lab) - Follow the live trading journey

### Strategy Guides
- `docs/strategies/momentum_trading.md` - Momentum strategy explained
- `docs/strategies/risk_management.md` - Position sizing and stops
- `docs/strategies/small_cap_selection.md` - Screening criteria

### Community
- Open issues on [GitHub](https://github.com/SteppieD/tradinggame/issues)
- Share your modifications via Pull Requests
- Join discussions in YouTube comments

## 🚨 Disclaimer

**IMPORTANT**: This tool is for educational purposes. Trading involves substantial risk of loss. Past performance doesn't guarantee future results. Always:
- Start with small positions
- Use stop losses
- Never trade money you can't afford to lose
- Do your own research
- Consider paper trading first

## 📜 License

MIT License - Free to use, modify, and share!

---

Ready to start? Run `python setup.py` and let's begin your AI-assisted trading journey! 🚀