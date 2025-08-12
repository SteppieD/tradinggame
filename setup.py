#!/usr/bin/env python3

"""
AI Trading Assistant - Setup Script
Configures your trading environment in minutes
"""

import json
import os
import sys
from pathlib import Path
import subprocess

# ANSI colors for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header():
    """Display welcome header"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}🤖 AI Trading Assistant Setup{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    print("This wizard will help you set up your trading environment.\n")

def check_python_version():
    """Ensure Python 3.8+ is installed"""
    print(f"{YELLOW}Checking Python version...{RESET}")
    if sys.version_info < (3, 8):
        print(f"{RED}❌ Python 3.8+ required. You have {sys.version}{RESET}")
        sys.exit(1)
    print(f"{GREEN}✅ Python {sys.version.split()[0]} detected{RESET}\n")

def install_dependencies():
    """Install required Python packages"""
    print(f"{YELLOW}Installing Python dependencies...{RESET}")
    
    requirements = [
        "requests",
        "pandas",
        "python-dotenv",
        "colorama",
        "tabulate"
    ]
    
    for package in requirements:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✅ {package} already installed")
        except ImportError:
            print(f"  📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            print(f"  ✅ {package} installed")
    
    print(f"{GREEN}✅ All dependencies installed{RESET}\n")

def create_directories():
    """Create necessary directory structure"""
    print(f"{YELLOW}Creating directory structure...{RESET}")
    
    directories = [
        "data",
        "data/executions",
        "config",
        "reports",
        "reports/daily",
        "reports/executions",
        "logs",
        "orders",
        "scripts",
        "agents"
    ]
    
    base_path = Path.cwd()
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}/")
    
    print(f"{GREEN}✅ Directory structure created{RESET}\n")

def setup_broker_config():
    """Configure broker settings"""
    print(f"{YELLOW}Setting up broker configuration...{RESET}\n")
    
    print("Please enter your broker information:")
    
    broker_name = input(f"  {BLUE}Broker name (e.g., CIBC, TD, Interactive Brokers):{RESET} ").strip()
    if not broker_name:
        broker_name = "Generic Broker"
    
    account_types = ["TFSA", "RRSP", "Cash", "Margin", "Other"]
    print(f"\n  {BLUE}Account types:{RESET}")
    for i, acc_type in enumerate(account_types, 1):
        print(f"    {i}. {acc_type}")
    
    while True:
        try:
            choice = int(input(f"  {BLUE}Select account type (1-{len(account_types)}):{RESET} "))
            if 1 <= choice <= len(account_types):
                account_type = account_types[choice - 1]
                break
        except ValueError:
            pass
        print(f"  {RED}Invalid choice. Please enter a number 1-{len(account_types)}{RESET}")
    
    while True:
        try:
            commission = float(input(f"  {BLUE}Commission per trade (e.g., 6.95):{RESET} $"))
            break
        except ValueError:
            print(f"  {RED}Please enter a valid number{RESET}")
    
    currencies = ["CAD", "USD", "EUR", "GBP"]
    print(f"\n  {BLUE}Currency:{RESET}")
    for i, currency in enumerate(currencies, 1):
        print(f"    {i}. {currency}")
    
    while True:
        try:
            choice = int(input(f"  {BLUE}Select currency (1-{len(currencies)}):{RESET} "))
            if 1 <= choice <= len(currencies):
                currency = currencies[choice - 1]
                break
        except ValueError:
            pass
        print(f"  {RED}Invalid choice. Please enter a number 1-{len(currencies)}{RESET}")
    
    while True:
        try:
            starting_balance = float(input(f"  {BLUE}Starting balance:{RESET} $"))
            break
        except ValueError:
            print(f"  {RED}Please enter a valid number{RESET}")
    
    broker_config = {
        "broker_name": broker_name,
        "account_type": account_type,
        "commission_per_trade": commission,
        "currency": currency,
        "starting_balance": starting_balance
    }
    
    config_path = Path("config/broker_settings.json")
    with open(config_path, 'w') as f:
        json.dump(broker_config, f, indent=2)
    
    print(f"\n{GREEN}✅ Broker configuration saved{RESET}\n")
    return broker_config

def setup_portfolio(broker_config):
    """Initialize portfolio file"""
    print(f"{YELLOW}Initializing portfolio...{RESET}")
    
    portfolio = {
        "cash_balance": broker_config["starting_balance"],
        "starting_balance": broker_config["starting_balance"],
        "positions": [],
        "pending_orders": [],
        "last_updated": "",
        "total_value": broker_config["starting_balance"],
        "total_pnl": 0,
        "total_pnl_percent": 0.0,
        "broker_info": {
            "name": broker_config["broker_name"],
            "account_type": broker_config["account_type"],
            "commission_per_trade": broker_config["commission_per_trade"]
        }
    }
    
    portfolio_path = Path("data/portfolio.json")
    with open(portfolio_path, 'w') as f:
        json.dump(portfolio, f, indent=2)
    
    print(f"{GREEN}✅ Portfolio initialized with ${broker_config['starting_balance']:.2f} {broker_config['currency']}{RESET}\n")

def setup_risk_rules():
    """Configure risk management rules"""
    print(f"{YELLOW}Setting up risk management rules...{RESET}\n")
    
    print("Configure your risk parameters (press Enter for defaults):")
    
    def get_float_input(prompt, default):
        value = input(f"  {BLUE}{prompt} (default: {default}):{RESET} ").strip()
        if not value:
            return default
        try:
            return float(value)
        except ValueError:
            print(f"  {YELLOW}Invalid input, using default: {default}{RESET}")
            return default
    
    def get_int_input(prompt, default):
        value = input(f"  {BLUE}{prompt} (default: {default}):{RESET} ").strip()
        if not value:
            return default
        try:
            return int(value)
        except ValueError:
            print(f"  {YELLOW}Invalid input, using default: {default}{RESET}")
            return default
    
    risk_rules = {
        "max_position_size_percent": get_float_input("Max position size %", 10),
        "max_concurrent_positions": get_int_input("Max concurrent positions", 5),
        "stop_loss_percent": get_float_input("Stop loss %", 10),
        "break_even_trigger": get_float_input("Move stop to break-even at % gain", 5),
        "trailing_stop_percent": get_float_input("Trailing stop %", 10),
        "profit_target_percent": get_float_input("Profit target %", 15),
        "max_daily_trades": get_int_input("Max trades per day", 3),
        "min_volume": get_int_input("Minimum daily volume", 100000),
        "min_price": get_float_input("Minimum stock price", 1.0),
        "max_price": get_float_input("Maximum stock price", 50.0)
    }
    
    rules_path = Path("config/risk_rules.json")
    with open(rules_path, 'w') as f:
        json.dump(risk_rules, f, indent=2)
    
    print(f"\n{GREEN}✅ Risk management rules configured{RESET}\n")

def setup_env_file():
    """Create .env file for API keys"""
    print(f"{YELLOW}Setting up API configuration...{RESET}\n")
    
    env_path = Path(".env")
    
    if env_path.exists():
        print(f"  {YELLOW}⚠️  .env file already exists{RESET}")
        overwrite = input(f"  {BLUE}Overwrite? (y/N):{RESET} ").strip().lower()
        if overwrite != 'y':
            print(f"  {GREEN}✅ Keeping existing .env file{RESET}\n")
            return
    
    print("Get your free API key at: https://www.alphavantage.co/support/#api-key")
    api_key = input(f"  {BLUE}Alpha Vantage API key (or press Enter to add later):{RESET} ").strip()
    
    env_content = f"""# API Configuration
ALPHA_VANTAGE_API_KEY={api_key if api_key else 'your_api_key_here'}

# Add other API keys as needed:
# POLYGON_API_KEY=
# IEX_CLOUD_API_KEY=
# YAHOO_FINANCE_API_KEY=
"""
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    if api_key:
        print(f"{GREEN}✅ API configuration saved{RESET}\n")
    else:
        print(f"{YELLOW}⚠️  Remember to add your API key to .env file{RESET}\n")

def create_example_trades():
    """Create example trade file"""
    print(f"{YELLOW}Creating example files...{RESET}")
    
    example_trades = """# Example trades - Copy your broker's format here
BUY 100 AAPL @ 150.25
SOLD 50 TSLA @ 890.50
Bought 200 SNDL at $2.15
"""
    
    example_path = Path("EXAMPLE_TRADES.txt")
    with open(example_path, 'w') as f:
        f.write(example_trades)
    
    print(f"  ✅ Example files created{RESET}\n")

def setup_claude_instructions():
    """Create Claude Code instructions file"""
    print(f"{YELLOW}Setting up Claude Code integration...{RESET}")
    
    claude_md = """# Claude Code Instructions

## Available Agents
Use these specialized agents for trading analysis:

- `small-cap-screener` - Find momentum opportunities
- `market-researcher` - Fundamental analysis
- `quant-analyst` - Technical signals
- `risk-manager` - Position sizing
- `news-sentiment` - News monitoring
- `earnings-calendar` - Earnings tracking
- `trading-journal` - Performance analysis

## Daily Commands

### Morning Analysis
"Screen for today's opportunities with momentum and generate orders"

### Position Review  
"Analyze my positions and suggest stop-loss adjustments"

### Performance Check
"Compare my performance to the benchmarks"

### End of Day
"Update my trading journal with today's lessons"

## Important Rules
- Always use Alpha Vantage MCP for real-time quotes
- Track benchmark prices when recording trades
- Enforce risk management rules from config/risk_rules.json
- Update dashboard after each trade
"""
    
    claude_path = Path("CLAUDE.md")
    with open(claude_path, 'w') as f:
        f.write(claude_md)
    
    print(f"  ✅ Claude Code instructions created{RESET}\n")

def print_next_steps():
    """Display next steps for the user"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}✅ Setup Complete!{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    print(f"{BOLD}📋 Next Steps:{RESET}\n")
    
    steps = [
        ("Add API Key", "Edit .env file with your Alpha Vantage API key"),
        ("Open Dashboard", "Open dashboard.html in your browser"),
        ("Launch Claude Code", "Run 'claude-code' in this directory"),
        ("Start Trading", "Ask Claude to 'screen for today's opportunities'"),
        ("Record Trades", "Paste trades into PASTE_TRADES_HERE.py")
    ]
    
    for i, (title, desc) in enumerate(steps, 1):
        print(f"  {BOLD}{i}. {title}{RESET}")
        print(f"     {desc}\n")
    
    print(f"{BOLD}📚 Resources:{RESET}")
    print(f"  • Documentation: {BLUE}SETUP.md{RESET}")
    print(f"  • Video Tutorials: {BLUE}youtube.com/@aibusiness-lab{RESET}")
    print(f"  • GitHub Issues: {BLUE}github.com/SteppieD/tradinggame/issues{RESET}\n")
    
    print(f"{YELLOW}⚠️  Disclaimer:{RESET}")
    print("  Trading involves risk. Start small, use stops, and never")
    print("  trade money you can't afford to lose.\n")
    
    print(f"{GREEN}Happy Trading! 🚀{RESET}\n")

def main():
    """Main setup flow"""
    try:
        print_header()
        check_python_version()
        install_dependencies()
        create_directories()
        broker_config = setup_broker_config()
        setup_portfolio(broker_config)
        setup_risk_rules()
        setup_env_file()
        create_example_trades()
        setup_claude_instructions()
        print_next_steps()
        
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Setup cancelled by user{RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}❌ Setup failed: {e}{RESET}\n")
        print("Please report this issue at:")
        print("https://github.com/SteppieD/tradinggame/issues\n")
        sys.exit(1)

if __name__ == "__main__":
    main()