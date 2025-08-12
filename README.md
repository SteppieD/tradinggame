# 🎯 Trading Game - $1000 Small-Cap Challenge

[![YouTube Channel](https://img.shields.io/badge/YouTube-AI%20Business%20Lab-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/@aibusiness-lab)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Built with Claude](https://img.shields.io/badge/Built%20with-Claude%20AI-purple?style=for-the-badge)](https://claude.ai)

## 📺 Follow the Journey

This is a live trading experiment with real money! Follow along on YouTube:
**[AI Business Lab](https://www.youtube.com/@aibusiness-lab)**

## 🎮 The Challenge

Starting with **$1,000 CAD** in a TFSA account, we're using AI-powered analysis to trade small-cap stocks. Every trade, decision, and lesson learned is documented here and on the YouTube channel.

### Current Status (Aug 12, 2025)
- **Starting Balance:** $1,000
- **Current Positions:** 3 (CHPT, EVGO, FCEL)
- **Strategy:** Clean tech momentum plays
- **Risk Management:** 10% trailing stops on all positions

## 🤖 Built with Claude Code

This project leverages [Claude Code](https://claude.ai/code) AI agents for:
- **Market Analysis** - Screening small-cap opportunities
- **Risk Management** - Position sizing and stop-loss management
- **Technical Analysis** - Entry/exit signals
- **Order Generation** - Daily trade planning

## 🔄 Inspired By

This project is a riff on [ChadGPT Day Trader](https://github.com/turing-machines/ChadGPT-DayTrader) by Turing Machines, adapted for:
- Canadian TFSA trading rules
- Small-cap focus ($50M-$2B market cap)
- CIBC Investor's Edge platform
- Risk-managed position sizing

## ✨ Features

### 📊 Real-Time Dashboard
```bash
open dashboard.html
```
- Live position tracking with P&L
- Dark mode for any-time monitoring
- Position management tracker with action triggers
- Daily trading checklist

### 🤖 AI Trading Agents
- `small-cap-screener` - Finds momentum opportunities
- `risk-manager` - Enforces position limits
- `quant-analyst` - Technical indicators & signals
- `market-researcher` - Fundamental analysis

### 📈 Automated Workflows
```bash
# Record trades from broker
python PASTE_TRADES_HERE.py

# Generate daily orders
python scripts/order_generator.py

# Screen for opportunities
python scripts/stock_screener.py
```

## 🚀 Quick Start

1. **Clone the repo**
```bash
git clone https://github.com/SteppieD/tradinggame.git
cd tradinggame
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **View the dashboard**
```bash
open dashboard.html
```

## 📁 Project Structure

```
tradinggame/
├── dashboard.html          # Trading dashboard with position tracker
├── PASTE_TRADES_HERE.py    # Easy trade entry system
├── scripts/
│   ├── stock_screener.py   # Find momentum plays
│   ├── order_generator.py  # Create daily orders
│   └── portfolio_tracker.py # Track performance
├── agents/                 # Claude Code AI agents
└── data/                   # Portfolio & market data
```

## 📋 Trading Rules

### Position Sizing
- Maximum 10% of portfolio per position
- No more than 3-5 concurrent positions
- $6.95 commission per trade (CIBC)

### Risk Management
- 10% trailing stop-loss on all positions
- Move stop to break-even at +5%
- Trail stop 5% below high at +10%
- Consider profits at +15%

### Current Focus
- Clean energy sector (EV charging, hydrogen)
- Momentum plays with volume spikes
- Small-caps with institutional interest

## 📺 Episode Schedule

New videos posted regularly on [AI Business Lab](https://www.youtube.com/@aibusiness-lab):
- Trade recaps and analysis
- AI agent development
- Strategy discussions
- Win/loss breakdowns

## ⚠️ Disclaimer

This is an educational experiment with real money at risk. This is not financial advice. Trading involves substantial risk of loss. Past performance does not guarantee future results. Always do your own research.

## 🤝 Contributing

Have ideas for improving the trading system? Feel free to:
- Open an issue
- Submit a pull request
- Comment on the YouTube videos
- Share your own trading experiments

## 📜 License

MIT License - feel free to fork and adapt for your own trading experiments!

## 🔗 Links

- **YouTube:** [AI Business Lab](https://www.youtube.com/@aibusiness-lab)
- **Original Inspiration:** [ChadGPT Day Trader](https://github.com/turing-machines/ChadGPT-DayTrader)
- **Claude Code:** [claude.ai/code](https://claude.ai/code)
- **This Repo:** [github.com/SteppieD/tradinggame](https://github.com/SteppieD/tradinggame)

---

*Building AI trading systems, one experiment at a time. Subscribe to follow the journey!* 🚀