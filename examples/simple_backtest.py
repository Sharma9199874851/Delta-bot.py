#!/usr/bin/env python3
"""Simple backtest example."""

import pandas as pd
from src.trader import DeltaTradingBot
import numpy as np


def generate_sample_data(num_candles=500):
    """
    Generate sample OHLCV data for testing.
    In real usage, load actual historical data from exchange.
    """
    dates = pd.date_range(start='2025-01-01', periods=num_candles, freq='4h')
    
    # Generate realistic price movement
    prices = [40000]  # Start at $40k for BTC
    for _ in range(num_candles - 1):
        change = np.random.normal(0, 0.005)  # 0.5% std dev
        prices.append(prices[-1] * (1 + change))
    
    df = pd.DataFrame({
        'timestamp': dates,
        'open': prices,
        'high': np.array(prices) * 1.01,
        'low': np.array(prices) * 0.99,
        'close': prices,
        'volume': np.random.uniform(100, 500, num_candles)
    })
    
    return df


if __name__ == '__main__':
    # Initialize bot
    bot = DeltaTradingBot('config.yaml')
    
    # Generate sample data
    print("Generating sample market data...")
    df = generate_sample_data(500)
    
    # Run backtest
    print("Running backtest...")
    results = bot.backtest('BTC/USDT', '4h', df)
    
    # Display results
    stats = results['statistics']
    print("\n" + "="*60)
    print("BACKTEST RESULTS")
    print("="*60)
    print(f"Total Trades: {stats['total_trades']}")
    print(f"Winning Trades: {stats['winning_trades']}")
    print(f"Losing Trades: {stats['losing_trades']}")
    print(f"Win Rate: {stats['win_rate']:.2f}%")
    print(f"Total P&L: ${stats['total_profit_loss']:.2f}")
    print(f"ROI: {stats['roi']:.2f}%")
    print(f"Sharpe Ratio: {stats['sharpe_ratio']:.4f}")
    print(f"Max Drawdown: {stats['max_drawdown']:.2f}%")
    print("="*60)
