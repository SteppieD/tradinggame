# Simplified Trading Dashboard

## Overview
The dashboard has been simplified to focus on three essential sections:

### 1. Position Tracker
- Current holdings with entry/current prices
- Real-time P&L calculations
- Visual indicators for strong performers (🚀 >10%, ⭐ >5%)

### 2. Performance Summary
- Portfolio value and overall return
- Today's P&L
- Benchmark comparison (SPY/IWM)

### 3. Next Day Instructions
- Pre-calculated CIBC trailing stop parameters
- Trigger Delta and Limit Offset values
- Ready to input at 6:30 AM PST daily

## Quick Start
```bash
# Open simplified dashboard
open dashboard_simple.html

# Generate daily stop instructions
python generate_stop_instructions.py

# Update prices manually if needed
python update_prices_manual.py CHPT=11.62 EVGO=4.045 FCEL=4.26
```

## Stock Price Collection
Since Alpha Vantage MCP is not available, I've created a custom `stock-price-collector` agent that:
- Fetches real-time prices from multiple sources
- Handles volatile small-cap stocks
- Provides fallback options when APIs are delayed

To use: "Get current prices using stock-price-collector"

## Files
- `dashboard_simple.html` - Clean, focused dashboard
- `generate_stop_instructions.py` - Creates daily CIBC orders
- `smart_stops.py` - Intelligent stop-loss calculations
- `.claude/agents/stock-price-collector.md` - Custom price fetching agent

The dashboard auto-refreshes every 30 seconds and reads from JSON data files in the `data/` directory.