# 🤖 Claude Code Agent Documentation

This document explains how to use Claude Code's specialized trading agents for maximum effectiveness.

## 📊 Trading Agents Overview

### Market Analysis Agents

#### `small-cap-screener`
**Purpose**: Identifies high-potential small-cap trading opportunities  
**Best For**: Finding momentum plays, unusual volume, breakouts  
**Usage**:
```
"Use the small-cap-screener agent to find stocks with unusual volume today"
"Screen for small-caps breaking out of consolidation patterns"
"Find clean energy small-caps with momentum"
```

#### `market-researcher`
**Purpose**: Fundamental analysis and sector research  
**Best For**: Company analysis, sector trends, catalyst identification  
**Usage**:
```
"Research the fundamentals of EVGO and its competitors"
"What catalysts are driving the EV charging sector?"
"Analyze institutional ownership changes in my positions"
```

#### `quant-analyst`
**Purpose**: Technical analysis and trading signals  
**Best For**: Chart patterns, entry/exit points, technical indicators  
**Usage**:
```
"Analyze the technical setup for CHPT"
"Find stocks with bullish MACD crossovers under $10"
"What's the RSI and support levels for my positions?"
```

### Risk Management Agents

#### `risk-manager`
**Purpose**: Portfolio risk assessment and position sizing  
**Best For**: Stop-loss management, position sizing, risk limits  
**Usage**:
```
"Calculate optimal position sizes for my watchlist"
"Should I adjust stops based on current volatility?"
"Analyze my portfolio's sector concentration risk"
```

#### `trading-journal`
**Purpose**: Track and analyze trading performance  
**Best For**: Pattern recognition, mistake analysis, improvement tracking  
**Usage**:
```
"Analyze my winning vs losing trades this month"
"What patterns exist in my trading mistakes?"
"Generate insights from my trading history"
```

### Information Agents

#### `news-sentiment`
**Purpose**: Real-time news and sentiment analysis  
**Best For**: Breaking news, sentiment shifts, social media tracking  
**Usage**:
```
"Check news sentiment for my positions"
"Any breaking news affecting clean energy stocks?"
"Track social media sentiment for FCEL"
```

#### `earnings-calendar`
**Purpose**: Earnings tracking and analysis  
**Best For**: Earnings plays, volatility events, reaction analysis  
**Usage**:
```
"When do my positions report earnings?"
"Find stocks with earnings this week under $20"
"Analyze historical earnings reactions for EVGO"
```

## 🎯 Effective Agent Workflows

### Daily Market Open Workflow
```
1. "Use small-cap-screener to find pre-market movers"
2. "Use news-sentiment to check overnight developments"
3. "Use quant-analyst to identify entry points for watchlist"
4. "Use risk-manager to calculate position sizes"
```

### Position Management Workflow
```
1. "Use market-researcher to check for new catalysts"
2. "Use quant-analyst to review technical levels"
3. "Use risk-manager to optimize stop-losses"
4. "Use news-sentiment for sentiment shifts"
```

### End of Day Review
```
1. "Use trading-journal to record today's lessons"
2. "Use quant-analyst to identify tomorrow's setups"
3. "Use earnings-calendar for upcoming events"
4. "Use risk-manager to review portfolio exposure"
```

## 🔄 Agent Chaining

Claude Code agents work best when chained together:

### Example: Complete Stock Analysis
```
"First use market-researcher to analyze PLUG fundamentals,
then use quant-analyst for technical levels,
then news-sentiment for recent developments,
finally risk-manager for position sizing"
```

### Example: Sector Rotation
```
"Use market-researcher to identify rotating sectors,
then small-cap-screener to find leaders in those sectors,
then quant-analyst to find best entry points"
```

## 💡 Pro Tips

### 1. Be Specific with Criteria
❌ "Find good stocks"  
✅ "Find small-caps under $5 with >200% average volume"

### 2. Combine Multiple Agents
❌ "Analyze CHPT"  
✅ "Use quant-analyst for CHPT technicals and news-sentiment for recent news"

### 3. Set Clear Parameters
❌ "Check momentum stocks"  
✅ "Find stocks up >10% today with volume >1M shares"

### 4. Use Time Frames
❌ "Find breakouts"  
✅ "Find stocks breaking 52-week highs today"

### 5. Layer Your Analysis
```
Step 1: "Screen for opportunities" (small-cap-screener)
Step 2: "Research the top 3" (market-researcher)
Step 3: "Check technicals" (quant-analyst)
Step 4: "Size positions" (risk-manager)
```

## 📈 Agent Performance Metrics

Track agent effectiveness:

| Agent | Best Use Case | Success Metric |
|-------|--------------|----------------|
| small-cap-screener | Finding movers | Win rate of picks |
| market-researcher | Fundamental analysis | Catalyst accuracy |
| quant-analyst | Entry/exit timing | Price target hits |
| risk-manager | Position sizing | Drawdown control |
| news-sentiment | Sentiment shifts | Trend prediction |
| earnings-calendar | Event trading | Reaction accuracy |
| trading-journal | Performance analysis | Improvement rate |

## 🚀 Advanced Usage

### Custom Screening Chains
```python
# Morning Momentum Scanner
"Chain these agents:
1. small-cap-screener: unusual volume + price action
2. news-sentiment: check for catalysts
3. quant-analyst: confirm technical setup
4. risk-manager: position size if all positive"
```

### Automated Workflows
```python
# Set up recurring analysis
"Every morning at 9:00 AM:
- Run small-cap-screener for pre-market movers
- Check news-sentiment for overnight developments  
- Generate order list with risk-manager sizing"
```

### Multi-Timeframe Analysis
```python
# Comprehensive position review
"For each position:
- Daily: quant-analyst for intraday levels
- Weekly: market-researcher for fundamental changes
- Monthly: trading-journal for performance review"
```

## 🔧 Customizing Agents

### Modify Agent Behavior

Edit agent preferences in `config/agent_settings.json`:

```json
{
  "small-cap-screener": {
    "market_cap_range": [50000000, 2000000000],
    "min_volume": 500000,
    "price_range": [1, 50]
  },
  "risk-manager": {
    "max_position_percent": 10,
    "max_portfolio_positions": 5
  }
}
```

### Add Custom Agents

Create new agents for specific strategies:

1. Create `agents/your_custom_agent.json`
2. Define agent capabilities
3. Use in Claude Code: "Use your_custom_agent to..."

## 📚 Examples Library

### Momentum Day Trading
```
"Use small-cap-screener for stocks up >5% on >2x volume,
then quant-analyst to find the first pullback,
then risk-manager for 2% risk position size"
```

### Earnings Play Setup
```
"Use earnings-calendar for next week's reports,
filter with market-researcher for positive guidance history,
check news-sentiment for pre-earnings sentiment,
size with risk-manager for event volatility"
```

### Sector Rotation Trade
```
"Use market-researcher to identify this week's strongest sector,
screen with small-cap-screener for sector leaders,
analyze with quant-analyst for breakout setups,
position with risk-manager using sector allocation limits"
```

## 🎓 Learning Path

### Beginner (Week 1)
- Master `small-cap-screener` for finding opportunities
- Use `risk-manager` for every position
- Review with `trading-journal` daily

### Intermediate (Week 2-4)  
- Add `quant-analyst` for timing
- Incorporate `news-sentiment` for catalysts
- Chain 2-3 agents together

### Advanced (Month 2+)
- Create complex agent chains
- Develop custom screening criteria
- Automate daily workflows
- Build agent-based strategies

## 🆘 Troubleshooting

**Agent not responding?**
- Check agent name spelling
- Verify Claude Code is updated
- Try simpler prompts first

**Wrong results?**
- Be more specific with criteria
- Check config settings
- Review agent parameters

**Too much data?**
- Add filters to narrow results
- Limit to top 5-10 opportunities
- Focus on specific sectors/criteria

---

Remember: Agents are tools to enhance your analysis, not replace your judgment. Always verify agent recommendations before trading! 🚀