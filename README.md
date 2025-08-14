# 🎯 AI Trading Assistant - Powered by Claude Code

[![YouTube Channel](https://img.shields.io/badge/YouTube-AI%20Business%20Lab-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/@aibusiness-lab)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Built with Claude](https://img.shields.io/badge/Built%20with-Claude%20AI-purple?style=for-the-badge)](https://claude.ai)

**Build your own AI-powered trading system with Claude Code's specialized agents!**

## 📺 Follow the Journey

This is a live trading experiment with real money! Follow along on YouTube:
**[AI Business Lab](https://www.youtube.com/@aibusiness-lab)**

## 🎮 The Challenge

Starting with **$1,000 CAD** in a TFSA account, we're using AI-powered analysis to trade small-cap stocks. Every trade, decision, and lesson learned is documented here and on the YouTube channel.

### 📈 Live Performance (Updated: Aug 14, 2025 - Day 2)
- **Starting Balance:** $1,000 CAD
- **Current Value:** $1,043.32 (+4.33%) 🚀
- **Benchmark Performance:** Beating SPY by 4%, IWM by 2.4%
- **Win Rate:** 100% (4/4 positions green)

### 🎯 Monthly Goal: 15% Returns
- **Current Progress:** 4.33% / 15% (28.9% complete)
- **Days Elapsed:** 2 / 30
- **Target Portfolio Value:** $1,200
- **On Track:** ✅ YES (Ahead of schedule!)

### 💼 Current Positions
| Symbol | Shares | Entry | Current | P&L | Status |
|--------|--------|-------|---------|-----|--------|
| CHPT | 26 | $10.78 | $12.05 | +11.7% | 🚀 Strong |
| EVGO | 82 | $3.63 | $3.94 | +8.6% | ⭐ Steady |
| TDUP | 19 | $10.45 | $10.51 | +0.6% | 🆕 New |
| FUBO | 55 | $3.67 | $3.76 | +2.5% | 🆕 Momentum |

### 📊 Completed Trades
- **FCEL:** Sold at $4.26 (+3.4%) - Profit: $13.42

### 🎲 Strategy Updates
- **Focus:** High-growth momentum plays + aggressive position management
- **New Goal:** 10x portfolio in 6 months ($1,000 → $10,000)
- **Risk Management:** Trailing stops on winners, -5% fixed stops on new entries
- **Next Targets:** IONQ (quantum computing), ASTS (satellite)

## 🤖 Built with Claude Code

This project leverages [Claude Code](https://claude.ai/code) AI agents for:
- **Market Analysis** - Screening small-cap opportunities
- **Risk Management** - Position sizing and stop-loss management
- **Technical Analysis** - Entry/exit signals
- **Order Generation** - Daily trade planning

### 📊 Real-Time Data Access
- **Alpha Vantage MCP** - Live stock quotes, technical indicators, and market data
- Use `scripts/alpha_vantage_client.py` for programmatic access
- Real-time price updates for portfolio tracking

## 🔄 Inspired By

This project is a riff on [ChatGPT Micro Cap Experiment](https://github.com/LuckyOne7777/ChatGPT-Micro-Cap-Experiment) by LuckyOne7777, adapted for:
- Canadian TFSA trading rules
- Claude Code AI agents (instead of ChatGPT)
- CIBC Investor's Edge platform
- Risk-managed position sizing with trailing stops

## ✨ Features

### 📊 Real-Time Dashboard
```bash
open dashboard.html
```
- Live position tracking with P&L
- **Market comparison vs Russell 2000 (IWM) and S&P 500 (SPY)**
- Dark mode for any-time monitoring
- Position management tracker with action triggers
- Daily trading checklist
- Automatic benchmark tracking shows if we're beating the market

### 🤖 AI Trading Agents
- `small-cap-screener` - Finds momentum opportunities
- `risk-manager` - Enforces position limits
- `quant-analyst` - Technical indicators & signals
- `market-researcher` - Fundamental analysis

### 📈 Automated Workflows
```bash
# Record trades from broker (automatically tracks benchmarks!)
python PASTE_TRADES_HERE.py

# View benchmark comparison
python scripts/benchmark_summary.py

# Generate daily orders
python scripts/order_generator.py

# Screen for opportunities
python scripts/stock_screener.py
```

### 🎯 Automatic Benchmark Tracking
Every trade automatically captures IWM and SPY prices for real-time performance comparison:
- Records benchmark prices at exact trade time
- Calculates equivalent benchmark shares
- Shows if you're beating the market (alpha)
- Updates dashboard with live comparison

## 🚀 Quick Start (5 Minutes)

### Automated Setup
```bash
# Clone and setup
git clone https://github.com/SteppieD/tradinggame.git
cd tradinggame
python setup.py  # Interactive setup wizard
```

### Quick Links
- **⚡ [QUICK_START.md](QUICK_START.md)** - Get trading in 5 minutes
- **📖 [SETUP.md](SETUP.md)** - Complete setup guide  
- **🤖 [CLAUDE_AGENTS.md](CLAUDE_AGENTS.md)** - AI agent documentation

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
- **Original Inspiration:** [ChatGPT Micro Cap Experiment](https://github.com/LuckyOne7777/ChatGPT-Micro-Cap-Experiment)
- **Claude Code:** [claude.ai/code](https://claude.ai/code)
- **This Repo:** [github.com/SteppieD/tradinggame](https://github.com/SteppieD/tradinggame)

---

*Building AI trading systems, one experiment at a time. Subscribe to follow the journey!* 🚀