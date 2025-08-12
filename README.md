# Trading Dashboard & Portfolio Tracker

A comprehensive trading system for managing positions, tracking performance, and executing systematic trading strategies in small-cap stocks.

## Project Structure

```
tradev1/
├── agents/                  # Custom trading agents
│   ├── quant_analyst.json
│   ├── risk_manager.json
│   ├── market_researcher.json
│   ├── small_cap_screener.json
│   ├── news_sentiment.json
│   └── congress_tracker.json
├── data/                    # Market data and feeds
│   ├── portfolio.json       # Current positions
│   ├── watchlist.json       # Stocks to monitor
│   └── trades_history.csv   # Historical trades
├── analysis/                # Daily analysis outputs
│   └── YYYY-MM-DD/         # Daily folders
├── orders/                  # Daily trade orders
│   └── YYYY-MM-DD.md       # Orders for manual execution
├── reports/                 # Performance reports
│   ├── daily/
│   └── weekly/
├── config/                  # Configuration files
│   ├── risk_rules.json     # Stop-loss, position sizing
│   └── api_config.json     # API configurations
└── scripts/                 # Core trading scripts
    ├── daily_analysis.py
    ├── data_fetcher.py
    ├── performance_tracker.py
    └── order_generator.py
```

## Data Sources

1. **Market Data**: yfinance for real-time stock prices
2. **Congressional Trading**: QuiverQuant API / Capitol Trades
3. **News & Sentiment**: Financial news APIs
4. **Fundamentals**: SEC filings, earnings calendars

## Trading Strategy

- Focus: Small-cap stocks ($50M - $2B market cap)
- Risk Management: 2% max position size, 10% stop-loss
- Signals: Technical + Fundamental + Congressional activity
- Holding Period: 1-30 days typically

## Daily Workflow

1. **Morning Analysis** (Pre-market)
   - Fetch overnight news
   - Check congressional disclosures
   - Screen for new opportunities
   - Review existing positions

2. **Order Generation**
   - Generate buy/sell orders
   - Calculate position sizes
   - Set stop-loss levels

3. **End of Day**
   - Update portfolio tracking
   - Log performance metrics
   - Generate daily report

## Performance Tracking

- Daily P&L
- Win/Loss ratio
- Sharpe ratio
- Comparison to Russell 2000