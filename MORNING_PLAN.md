# 📋 Daily Trading Plan - Morning Routine

## ⏰ CRITICAL TIMING
**6:30 AM PST EVERY MORNING** - Market opens, stops must be set immediately!

## 🚨 IMPORTANT REMINDERS
1. **Stop orders expire DAILY at 4:00 PM ET**
2. **They are NOT active overnight**
3. **You MUST set them each morning or positions are unprotected**
4. **CIBC does not have Good-Till-Cancelled (GTC) for trailing stops**

## 📱 Morning Routine (6:30 AM PST)

### Step 1: Run Morning Analysis
```bash
python morning_routine.py
```
This will show:
- Current pre-market prices
- Exact stop-loss parameters
- Risk assessment
- Market conditions

### Step 2: Open CIBC Investor's Edge App
1. Log in to your TFSA account
2. Go to "Trading" → "Stocks"
3. For EACH position (CHPT, EVGO, FCEL):

### Step 3: Set Trailing Stop Orders
For each stock:
1. Select "Sell"
2. Order Type: **"Trailing Stop Limit"**
3. Duration: **"Day"** (NOT Good Till Cancelled)
4. Enter:
   - Quantity: Your full position
   - Trigger Delta: From morning_routine.py output
   - Limit Offset: From morning_routine.py output
5. Review and Submit

### Step 4: Verify Orders
- Check "Orders" tab
- Confirm all 3 stops are **"Working"**
- Screenshot for records

## 📊 During Market Hours

### First 30 Minutes (6:30-7:00 AM PST)
- Monitor for unusual volatility
- Check if any gaps up/down from yesterday
- Watch for any stops getting close to trigger

### Mid-Day Check (12:00 PM PST)
```bash
python update_current_prices.py
```
- Review position performance
- Check if stops need adjustment (they trail UP automatically)

### End of Day (3:45 PM PST)
- Check final prices
- Note which stops (if any) triggered
- Prepare for tomorrow's plan

## 🛡️ Stop Loss Strategy

### Current Approach:
- **Losing positions**: Tight stops to protect capital
- **Small gains (0-5%)**: Hold near breakeven
- **Medium gains (5-10%)**: Use Fibonacci retracements
- **Large gains (>10%)**: Tight trailing stops to lock profits

### If Stop Triggers:
1. **DO NOT re-enter immediately**
2. Wait for next setup
3. Review why it triggered
4. Update strategy if needed

## 💡 Tips for Success

1. **Be Disciplined**: Set stops EVERY morning without fail
2. **Don't Override**: Trust the system, don't cancel stops emotionally
3. **Track Everything**: Log what works and what doesn't
4. **Stay Calm**: Stops triggering is part of the plan
5. **Keep Cash Ready**: For next opportunities

## 🚀 Quick Commands

```bash
# Morning routine (6:30 AM)
python morning_routine.py

# Update prices anytime
python update_current_prices.py

# Generate stop instructions
python generate_stop_instructions.py

# End of day summary
python eod_update.py

# Check fee impact
python calculate_fees_impact.py
```

## 📱 Dashboard Access
Open `dashboard_simple.html` in your browser
- Auto-refreshes every 30 seconds
- Shows real-time P&L
- Displays tomorrow's stop orders
- Tracks vs SPY/IWM benchmarks

---

**Remember**: The market doesn't care about your feelings. Stick to the plan!