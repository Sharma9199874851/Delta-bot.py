# Termux Setup Guide - Delta Bot & Tools

Complete guide to running Delta Bot, Joke Generator, and Digital Clock on Termux (Android).

## 📱 Step 1: Install Termux

### Option A: Google Play Store
1. Open Google Play Store
2. Search for "Termux"
3. Install the official Termux app

### Option B: F-Droid (Recommended)
1. Install F-Droid app from f-droid.org
2. Search for "Termux"
3. Install from F-Droid

## 🔧 Step 2: Initial Setup

### 2.1 Update Termux
```bash
pkg update
pkg upgrade -y
```

### 2.2 Grant Storage Access
```bash
termux-setup-storage
```
This allows access to your phone's storage.

### 2.3 Install Essential Tools
```bash
pkg install -y python git curl wget nano
```

**What these do:**
- `python` - Python 3 runtime
- `git` - Clone repositories
- `curl` - Download files
- `wget` - Download from web
- `nano` - Text editor

## 📥 Step 3: Clone Your Repository

```bash
# Navigate to storage
cd /sdcard

# Create a projects directory
mkdir my_projects
cd my_projects

# Clone the repository
git clone https://github.com/Sharma9199874851/Delta-bot.py.git
cd Delta-bot.py
```

## 🤖 Step 4: Setup Trading Bot

### 4.1 Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** This may take 5-10 minutes on first install.

### 4.2 Configure the Bot
```bash
# Copy example env file
cp .env.example .env

# Edit with your API credentials
nano .env
```

Add your exchange credentials:
```
EXCHANGE_API_KEY=your_api_key_here
EXCHANGE_API_SECRET=your_api_secret_here
```

**To save in nano:**
- Press `Ctrl + X`
- Press `Y` to confirm
- Press `Enter` to save

### 4.3 Prepare Historical Data

You need a CSV file with OHLCV data. Format:
```
timestamp,open,high,low,close,volume
2025-01-01 00:00,40000,40500,39800,40200,100
2025-01-01 04:00,40200,40800,40000,40500,120
...
```

**Option A: Download Sample Data**
```bash
# Create data directory
mkdir data

# Download sample BTC data (example)
curl -o data/BTC_USDT_4h.csv https://example.com/btc_data.csv
```

**Option B: Create Dummy Data**
```bash
python examples/simple_backtest.py
```

### 4.4 Run Backtest
```bash
# Test with sample data
python main.py --mode backtest --symbol BTC/USDT --data data/BTC_USDT_4h.csv
```

**Expected Output:**
```
============================================================
BACKTEST RESULTS - BTC/USDT
============================================================
Total Trades: 25
Winning Trades: 20
Losing Trades: 5
Win Rate: 80.00%
Total P&L: $1250.50
ROI: 1250.50%
...
```

### 4.5 Run Live Trading (Optional)
```bash
# Ensure .env is configured with real API keys
python main.py --mode live --symbol BTC/USDT
```

## 😂 Step 5: Setup Joke Generator

### 5.1 Install Dependencies
```bash
pip install requests
```

### 5.2 Run Joke Generator
```bash
python joke_generator.py
```

**Output Example:**
```
Fetching a random joke for you...

Here's your joke: 
Why did the Python programmer go broke? Because he didn't have any class!
```

## 🕐 Step 6: Setup Digital Clock

### 6.1 Install Dependencies
```bash
pip install -r clock_requirements.txt
```

### 6.2 Run Digital Clock
```bash
python digital_clock.py
```

**Menu Options:**
```
WORLD TIME ZONE CLOCK - MAIN MENU

1. Live Clock (Updates every second)
2. Static Snapshot (Single view of all timezones)
3. Timezone Information
4. Exit

Select an option (1-4): 1
```

## 📋 Complete Setup Script

Run this all at once:

```bash
#!/bin/bash

# Update system
pkg update
pkg upgrade -y

# Setup storage
termux-setup-storage

# Install tools
pkg install -y python git curl wget nano

# Navigate to projects
cd /sdcard
mkdir -p my_projects
cd my_projects

# Clone repo
git clone https://github.com/Sharma9199874851/Delta-bot.py.git
cd Delta-bot.py

# Install all dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r clock_requirements.txt

echo "Setup complete! Ready to run projects."
echo "- Trading Bot: python main.py --mode backtest --symbol BTC/USDT --data data/sample.csv"
echo "- Joke Generator: python joke_generator.py"
echo "- Digital Clock: python digital_clock.py"
```

**Save as `setup.sh` and run:**
```bash
bash setup.sh
```

## 🎯 Quick Command Reference

### Navigation
```bash
pwd                          # Show current directory
ls                           # List files
cd /sdcard                   # Go to phone storage
cd ..                        # Go up one directory
mkdir folder_name            # Create directory
```

### File Operations
```bash
cp file.txt copy.txt         # Copy file
mv file.txt folder/          # Move file
rm file.txt                  # Delete file
cat file.txt                 # View file contents
nano file.txt                # Edit file
```

### Python
```bash
python --version             # Check Python version
pip list                     # List installed packages
pip install package_name     # Install package
python script.py             # Run Python script
```

### Git
```bash
git clone repo_url           # Clone repository
git pull                     # Update repository
git status                   # Check changes
```

## 🔴 Troubleshooting

### Problem: "Permission denied" error
**Solution:**
```bash
chmod +x script.py
python script.py
```

### Problem: "ModuleNotFoundError" for packages
**Solution:**
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt
pip install --upgrade -r clock_requirements.txt
```

### Problem: Storage access issues
**Solution:**
```bash
# Grant storage permission again
termux-setup-storage
```

### Problem: Python version mismatch
**Solution:**
```bash
# Check Python version
python --version

# Upgrade Python
pkg install -y python --upgrade
```

### Problem: API Key not recognized
**Solution:**
```bash
# Check .env file
cat .env

# Verify format (no quotes around values):
# EXCHANGE_API_KEY=abc123
# EXCHANGE_API_SECRET=xyz789
```

### Problem: Slow performance
**Solution:**
- Close other apps
- Reduce backtest data size
- Use smaller timeframes
- Increase device RAM (restart device)

## 🌐 Network & Data Usage

**Important for Mobile:**
- Trading bot requires ~2MB per backtest
- Joke generator uses minimal data (~1KB per call)
- Digital clock uses ~1KB per update
- Real-time trading needs stable internet

**Recommendation:**
- Use WiFi for large backtests
- Mobile data fine for small tests
- Keep device plugged in for long trades

## 💾 File Locations

```
/sdcard/my_projects/Delta-bot.py/
├── main.py                    # Main entry point
├── config.yaml                # Bot configuration
├── requirements.txt           # Dependencies
├── joke_generator.py          # Joke script
├── digital_clock.py           # Clock script
├── src/
│   ├── indicators.py
│   ├── strategy.py
│   ├── exchange.py
│   ├── portfolio.py
│   ├── backtest.py
│   └── trader.py
├── data/                      # Store CSV data here
│   └── BTC_USDT_4h.csv
├── logs/                      # Trading logs
└── examples/
    └── simple_backtest.py
```

## 🔐 Security Tips

⚠️ **Important for Termux Trading:**

1. **Never share API keys** - Keep `.env` private
2. **Use read-only API keys** if possible
3. **Enable IP whitelisting** on exchange
4. **Use paper trading first** before real money
5. **Keep backups** of important configs

**Protect your .env file:**
```bash
chmod 600 .env              # Only you can read
ls -la .env                 # Verify permissions
```

## 📊 Performance Tips

**For Smooth Operation:**
```bash
# Free up RAM
kill-server                 # Restart Termux server

# Monitor resources
free -h                     # Check memory
df -h                       # Check storage

# Run in background
python main.py &            # Run without blocking
jobs                        # List background jobs
```

## 🆘 Need More Help?

**Useful Resources:**
- [Termux Wiki](https://wiki.termux.com/)
- [Termux GitHub](https://github.com/termux)
- [Python Docs](https://docs.python.org/3/)

**Common Issues:**
- Check internet connection
- Restart Termux app
- Clear cache: `termux-reset-home`
- Reinstall Termux if major issues

---

**Happy Trading & Hacking on Termux!** 🚀📱
