# ⚡ Quick Start Guide - 5 Minutes to Trading

Get up and running with AI-powered trading in 5 minutes!

## 🚀 Minute 1: Clone & Setup

```bash
# Clone the repository
git clone https://github.com/SteppieD/tradinggame.git
cd tradinggame

# Run automated setup
python setup.py
```

Follow the prompts:
- Enter broker name (or press Enter for default)
- Select account type (1-5)
- Enter commission (e.g., 6.95)
- Select currency (1-4)
- Enter starting balance (e.g., 1000)

## 🔑 Minute 2: Add API Key

1. Get free API key: https://www.alphavantage.co/support/#api-key
2. Add to `.env` file:

```bash
echo "ALPHA_VANTAGE_API_KEY=your_key_here" > .env
```

## 📊 Minute 3: Open Dashboard

```bash
# Open in default browser
open dashboard.html

# Or on Windows
start dashboard.html

# Or on Linux
xdg-open dashboard.html
```

You'll see:
- Portfolio tracker (currently empty)
- Market comparison (vs S&P 500 & Russell 2000)
- Position management guide
- Daily checklist

## 🤖 Minute 4: Launch Claude Code

```bash
# In the tradinggame directory
claude-code
```

Ask Claude:
> "Screen for today's small-cap momentum opportunities"

Claude will:
1. Use the `small-cap-screener` agent
2. Find stocks with unusual volume/price action
3. Present top opportunities
4. Suggest position sizes

## 💰 Minute 5: Make Your First Trade

### Option A: Paper Trade (Recommended for Beginners)

Ask Claude:
> "Let's paper trade 100 shares of AAPL at current price"

### Option B: Real Trade

1. **Execute trade in your broker**
2. **Copy trade confirmation**
3. **Record in the system**:

```bash
# Open the trade recorder
nano PASTE_TRADES_HERE.py

# Paste between the quotes:
trades = """
BUY 100 AAPL @ 150.25
"""

# Save and run
python PASTE_TRADES_HERE.py
```

4. **Check dashboard** - Your position appears!

## 📝 Your First Day Checklist

### ☀️ Morning (9:00-9:30 AM ET)

```bash
# In Claude Code, ask:
"Run my morning routine: 
1. Screen for opportunities
2. Check overnight news
3. Generate today's orders"
```

### 📈 Market Hours (9:30 AM - 4:00 PM ET)

Monitor dashboard for:
- ⬆️ Positions up 5% → Move stop to break-even
- ⬆️ Positions up 10% → Trail stop by 5%
- ⬆️ Positions up 15% → Consider taking profits
- ⬇️ Positions at stop → Exit position

### 🌙 After Close (4:00 PM+)

```bash
# In Claude Code, ask:
"Run end of day review:
1. Update trading journal
2. Analyze today's performance
3. Prepare tomorrow's watchlist"
```

## 🎯 Essential Commands

### Finding Opportunities
```
"Find small-caps with >100% volume increase"
"Screen for clean energy momentum plays"
"Show me stocks breaking 52-week highs under $10"
```

### Managing Positions
```
"Analyze my current positions"
"Should I adjust any stop losses?"
"Calculate position size for TSLA with 2% risk"
```

### Performance Review
```
"How am I doing vs the market?"
"Show my win/loss ratio"
"What mistakes did I make this week?"
```

## 🛠️ Quick Customization

### Change Risk Settings

Edit `config/risk_rules.json`:

```json
{
  "max_position_size_percent": 10,  // Max 10% per position
  "stop_loss_percent": 10,           // 10% stop loss
  "profit_target_percent": 15        // 15% profit target
}
```

### Modify Screening Criteria

Ask Claude:
```
"Update small-cap-screener to focus on:
- Price: $2-10
- Volume: >1M shares
- Sector: Technology only"
```

## 📱 Mobile Access

View dashboard on phone:
1. Get your computer's IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. On phone browser: `http://YOUR_IP:8000/dashboard.html`
3. Or use GitHub Pages for cloud access

## 🆘 Quick Fixes

### "API limit reached"
- Wait until tomorrow (25 calls/day limit)
- Or upgrade to paid Alpha Vantage plan

### "Can't find stocks"
- Markets closed? Check pre/post market
- Try broader criteria
- Verify API key is set

### "Dashboard not updating"
- Refresh browser (Ctrl+F5)
- Check `.env` has API key
- Run: `python scripts/alpha_vantage_client.py --test`

## 📚 Next Steps

**After your first successful trade:**

1. **Read Full Documentation**
   - `SETUP.md` - Complete setup guide
   - `CLAUDE_AGENTS.md` - Master the AI agents
   - `README.md` - Project overview

2. **Watch YouTube Tutorials**
   - [AI Business Lab](https://www.youtube.com/@aibusiness-lab)
   - See live trading sessions
   - Learn from real examples

3. **Join the Community**
   - Star the [GitHub repo](https://github.com/SteppieD/tradinggame)
   - Report issues or suggest features
   - Share your modifications

## ⚠️ Important Reminders

1. **Start Small** - Trade tiny positions while learning
2. **Use Stops** - Always set stop losses
3. **Paper Trade** - Practice without real money first
4. **Track Everything** - Record all trades for analysis
5. **Learn Daily** - Review mistakes and successes

---

**Ready to trade?** You now have everything needed to start your AI-assisted trading journey! 

Remember: *Trade responsibly, start small, and always use stop losses!* 🚀

---

**Need help?** Ask Claude: "How do I..." and it will guide you!