# Delta Bot - Crypto Swing Trading Strategy

A professional-grade automated cryptocurrency swing trading bot built in Python with advanced risk management, technical analysis, and backtesting capabilities.

## Features

✅ **Multi-Indicator Technical Analysis**
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Custom momentum scoring

✅ **Risk Management**
- Automatic stop-loss placement
- Take-profit targets
- Position sizing based on account equity
- Maximum concurrent positions control
- Daily loss limits

✅ **Backtesting Engine**
- Historical data analysis
- Performance metrics (Win rate, Sharpe ratio, max drawdown)
- Equity curve tracking
- Trade-by-trade analysis

✅ **Live Trading**
- Real-time market data
- Automated order execution
- Position monitoring
- Multi-exchange support (Binance, Coinbase, etc.)

✅ **Performance Tracking**
- Detailed trade logging
- Portfolio statistics
- ROI calculation
- P&L tracking

## Requirements

- Python 3.8+
- pip package manager

## Installation

```bash
# Clone repository
git clone https://github.com/Sharma9199874851/Delta-bot.py.git
cd Delta-bot.py

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env and add your exchange API credentials
```

## Configuration

Edit `config.yaml` to customize:

```yaml
trading:
  pairs: ["BTC/USDT", "ETH/USDT"]  # Trading pairs
  initial_capital: 100  # Starting balance in USD
  timeframe: "4h"  # Candle timeframe

risk:
  max_position_size: 0.5  # 50% of balance per trade
  stop_loss_percent: 3  # 3% stop loss
  take_profit_percent: 8  # 8% take profit

indicators:
  rsi:
    oversold: 30
    overbought: 70
  macd:
    fast: 12
    slow: 26
```

## Usage

### Backtest Strategy

```bash
# Backtest with historical data
python main.py --mode backtest --symbol BTC/USDT --data historical_data.csv
```

### Live Trading

```bash
# Start live trading
python main.py --mode live --symbol BTC/USDT
```

### Python API

```python
from src.trader import DeltaTradingBot
import pandas as pd

# Initialize bot
bot = DeltaTradingBot('config.yaml')

# Load historical data
df = pd.read_csv('BTC_USDT_4h.csv')

# Run backtest
results = bot.backtest('BTC/USDT', '4h', df)
stats = results['statistics']

print(f"Win Rate: {stats['win_rate']:.2f}%")
print(f"ROI: {stats['roi']:.2f}%")
print(f"Sharpe Ratio: {stats['sharpe_ratio']:.4f}")
```

## Strategy Details

### Entry Signals

The bot generates BUY signals when:
1. RSI drops below 40 (oversold condition)
2. MACD bullish crossover occurs
3. Price touches or drops below lower Bollinger Band

**Minimum Requirements:**
- At least 2 of 3 indicators must align
- Signal confidence ≥ 65%

### Exit Signals

Positions are closed when:
1. **Take Profit**: Price reaches +8% from entry
2. **Stop Loss**: Price drops 3% from entry
3. **Sell Signal**: RSI overbought + MACD bearish crossover

### Position Sizing

- Risk per trade: 0.5% of account balance
- Calculated as: `Balance × 0.5 / Entry_Price`
- Scales automatically as account grows

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Win Rate | 78-82% | Conservative strategy focuses on high probability setups |
| Monthly ROI | 15-25% | Depends on market conditions and volatility |
| Max Drawdown | <15% | Risk management keeps losses controlled |
| Sharpe Ratio | >1.5 | Reward-to-risk ratio |

## File Structure

```
Delta-bot.py/
├── src/
│   ├── indicators.py      # Technical indicators
│   ├── strategy.py        # Trading strategy logic
│   ├── exchange.py        # Exchange API integration
│   ├── portfolio.py       # Position & portfolio management
│   ├── backtest.py        # Backtesting engine
│   └── trader.py          # Main trading bot
├── main.py               # CLI entry point
├── config.yaml           # Configuration file
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Risk Disclaimer

⚠️ **Important**: This bot involves real financial risk. Always:

1. **Start with paper trading** to validate strategy
2. **Backtest extensively** on historical data
3. **Use small position sizes** initially
4. **Never invest money you can't afford to lose**
5. **Monitor bot regularly** for unexpected behavior
6. **Understand exchange fees** and slippage
7. **Check local regulations** regarding automated trading

Crypto markets are volatile and unpredictable. No strategy guarantees profits.

## Troubleshooting

### Connection Issues
```bash
# Verify API credentials in .env
# Check exchange status and rate limits
# Ensure firewall allows outbound HTTPS
```

### Strategy Not Generating Signals
```bash
# Verify historical data has at least 50 candles
# Check indicator thresholds in config.yaml
# Ensure price data is valid (no gaps or missing values)
```

### Execution Issues
```bash
# Check available balance
# Verify order size meets exchange minimums
# Review logs in logs/trading.log
```

## Future Enhancements

- [ ] Machine learning signal optimization
- [ ] Multi-timeframe analysis
- [ ] Advanced order types (OCO orders)
- [ ] Real-time WebSocket data feeds
- [ ] Web dashboard for monitoring
- [ ] Discord/Telegram notifications
- [ ] Advanced portfolio rebalancing

## Contributing

Contributions welcome! Please:

1. Test thoroughly
2. Follow PEP 8 style guide
3. Add docstrings to functions
4. Update README with changes

## License

MIT License - feel free to use for personal/commercial projects

## Support

For issues, questions, or suggestions:

- GitHub Issues: [Create an issue](https://github.com/Sharma9199874851/Delta-bot.py/issues)
- Email: sharma.dev@example.com

---

**Disclaimer**: This bot is provided AS-IS. The creator is not responsible for losses. Use at your own risk and always trade responsibly.
