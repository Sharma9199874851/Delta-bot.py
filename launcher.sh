#!/bin/bash
# Quick launcher for Termux projects
# Makes it easy to switch between projects

COLOR_GREEN='\033[0;32m'
COLOR_BLUE='\033[0;34m'
COLOR_YELLOW='\033[1;33m'
COLOR_RED='\033[0;31m'
NC='\033[0m' # No Color

clear
echo -e "${COLOR_BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║   Delta Bot - Termux Launcher          ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo -e "${COLOR_GREEN}Select a project:${NC}"
echo ""
echo "  1. 🤖 Trading Bot (Backtest)"
echo "  2. 😂 Joke Generator"
echo "  3. 🕐 Digital Clock"
echo "  4. 📖 View Guide"
echo "  5. ⚙️  Edit Configuration"
echo "  6. 📁 Open File Manager"
echo "  7. 🔄 Update Repository"
echo "  8. 🚪 Exit"
echo ""
echo -e "${COLOR_YELLOW}Choose option (1-8):${NC}"
read -r choice

case $choice in
    1)
        clear
        echo -e "${COLOR_GREEN}Starting Trading Bot...${NC}"
        echo "Enter data file (default: data/sample.csv):"
        read -r datafile
        datafile=${datafile:-data/sample.csv}
        python main.py --mode backtest --symbol BTC/USDT --data "$datafile"
        ;;
    2)
        clear
        echo -e "${COLOR_GREEN}Starting Joke Generator...${NC}"
        python joke_generator.py
        ;;
    3)
        clear
        echo -e "${COLOR_GREEN}Starting Digital Clock...${NC}"
        python digital_clock.py
        ;;
    4)
        clear
        nano TERMUX_GUIDE.md
        ;;
    5)
        clear
        nano config.yaml
        ;;
    6)
        cd /sdcard
        ls -la
        ;;
    7)
        echo -e "${COLOR_YELLOW}Updating repository...${NC}"
        git pull
        pip install --upgrade -r requirements.txt
        echo -e "${COLOR_GREEN}✅ Update complete!${NC}"
        ;;
    8)
        echo -e "${COLOR_GREEN}Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${COLOR_RED}Invalid option!${NC}"
        ;;
esac
