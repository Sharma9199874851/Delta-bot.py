#!/bin/bash
# Automated Termux Setup Script
# Run this to setup all projects at once

set -e  # Exit on error

echo "================================"
echo "  Delta Bot - Termux Setup"
echo "================================"
echo ""

echo "[1/7] Updating Termux packages..."
pkg update
pkg upgrade -y

echo "[2/7] Setting up storage access..."
termux-setup-storage

echo "[3/7] Installing essential tools..."
pkg install -y python git curl wget nano

echo "[4/7] Navigating to projects directory..."
cd /sdcard
mkdir -p my_projects
cd my_projects

echo "[5/7] Cloning repository..."
if [ -d "Delta-bot.py" ]; then
    echo "Repository already exists. Updating..."
    cd Delta-bot.py
    git pull
    cd ..
else
    git clone https://github.com/Sharma9199874851/Delta-bot.py.git
fi

cd Delta-bot.py

echo "[6/7] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -r clock_requirements.txt

echo "[7/7] Creating data directories..."
mkdir -p data logs

echo ""
echo "================================"
echo "  ✅ Setup Complete!"
echo "================================"
echo ""
echo "📂 Project Location: /sdcard/my_projects/Delta-bot.py/"
echo ""
echo "🚀 Quick Start Commands:"
echo ""
echo "  1. Trading Bot (Backtest):"
echo "     python main.py --mode backtest --symbol BTC/USDT --data data/sample.csv"
echo ""
echo "  2. Joke Generator:"
echo "     python joke_generator.py"
echo ""
echo "  3. Digital Clock:"
echo "     python digital_clock.py"
echo ""
echo "📖 Full Guide: TERMUX_GUIDE.md"
echo ""
echo "⚙️  Next Steps:"
echo "  1. Configure .env with your API keys"
echo "  2. Add historical data to data/ folder"
echo "  3. Test with backtest first"
echo ""
echo "Happy Trading! 🎯📈"
