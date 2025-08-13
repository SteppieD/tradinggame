# 🚨 CRITICAL: Price Data Policy

## MANDATORY RULE: Only Use Alpha Vantage API

### ✅ ALWAYS USE:
```bash
python update_prices.py
```
or
```bash
python always_use_alpha_vantage.py
```

### ❌ NEVER USE:
- Web searches for stock prices
- Manual price estimates
- "Last known" prices older than 15 minutes
- Any source other than Alpha Vantage API

## Why This Matters

**What happened with FCEL:**
1. We used web search data showing FCEL at $6.08
2. Actual Alpha Vantage price was $4.09
3. Stop-loss was set ABOVE market price
4. Position sold immediately at market open
5. Lost potential gains due to bad data

## Dashboard Features

### 📊 Update Prices Button
- Green button in dashboard header
- Click to refresh prices via Alpha Vantage
- Turns orange and pulses when data is stale (>15 min)
- Shows ✅ when successfully updated

### Automatic Checks
- Dashboard checks data freshness on load
- Warns if prices are >15 minutes old
- Auto-refreshes display every 30 seconds
- Validates freshness every 5 minutes

## Implementation

### Price Checker Agent
Created `alpha-vantage-price-checker` agent that:
- Enforces Alpha Vantage as sole price source
- Blocks any web search attempts for prices
- Validates data freshness
- Auto-invokes when prices are needed

### Scripts Available
1. **update_prices.py** - Primary price updater
2. **always_use_alpha_vantage.py** - Enforces policy and checks freshness
3. **morning_routine.py** - MUST run this at 6:30 AM (includes price update)

## Morning Routine (CRITICAL)

```bash
# 6:30 AM PST - EVERY DAY
python always_use_alpha_vantage.py  # Get fresh prices
python morning_routine.py           # Generate stop orders
```

## Error Prevention

### Before Setting Any Stop Orders:
1. Run `python update_prices.py`
2. Verify prices in CIBC app match
3. Calculate stops based on REAL prices
4. Never use prices from memory or web searches

### Data Freshness Rules:
- **Fresh**: < 15 minutes old ✅
- **Stale**: > 15 minutes old ⚠️
- **Invalid**: From web search ❌

## Consequences of Not Following

Using wrong price data can cause:
- Stops triggering immediately (like FCEL)
- Selling at wrong prices
- Missing profit opportunities
- Invalid portfolio calculations
- Bad trading decisions

## Remember

**One Command to Rule Them All:**
```bash
python update_prices.py
```

This is the ONLY way to get stock prices. Period.

---

*Last Updated: August 13, 2025*
*Policy Status: ENFORCED*