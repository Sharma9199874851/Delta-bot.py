#!/usr/bin/env python3
"""Delta Bot - Main entry point."""

import os
from dotenv import load_dotenv
from src.trader import DeltaTradingBot
import pandas as pd
import argparse


def main():
    """Main function."""
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Delta Bot - Crypto Swing Trading')
    parser.add_argument('--mode', choices=['backtest', 'live'], default='backtest',
                        help='Trading mode: backtest or live')
    parser.add_argument('--symbol', default='BTC/USDT', help='Trading pair')
    parser.add_argument('--config', default='config.yaml', help='Config file path')
    parser.add_argument('--data', help='Path to historical data CSV for backtesting')
    
    args = parser.parse_args()
    
    # Initialize bot
    bot = DeltaTradingBot(config_path=args.config)
    
    if args.mode == 'backtest':
        # Load historical data
        if not args.data:
            print("Error: --data argument required for backtest mode")
            return
        
        try:
            df = pd.read_csv(args.data)
            print(f"Loaded {len(df)} candles from {args.data}")
            
            # Run backtest
            results = bot.backtest(args.symbol, '4h', df)
            
            # Print results
            stats = results['statistics']
            print("\n" + "="*60)
            print(f"BACKTEST RESULTS - {args.symbol}")
            print("="*60)
            print(f"Total Trades: {stats['total_trades']}")
            print(f"Winning Trades: {stats['winning_trades']}")
            print(f"Losing Trades: {stats['losing_trades']}")
            print(f"Win Rate: {stats['win_rate']:.2f}%")
            print(f"Total P&L: ${stats['total_profit_loss']:.2f}")
            print(f"ROI: {stats['roi']:.2f}%")
            print(f"Best Trade: ${stats['best_trade']:.2f}")
            print(f"Worst Trade: ${stats['worst_trade']:.2f}")
            print(f"Avg Trade: ${stats['avg_profit_per_trade']:.2f}")
            print(f"Max Drawdown: {stats['max_drawdown']:.2f}%")
            print(f"Sharpe Ratio: {stats['sharpe_ratio']:.4f}")
            print("="*60)
            
        except FileNotFoundError:
            print(f"Error: Data file '{args.data}' not found")
    
    elif args.mode == 'live':
        # Initialize portfolio
        bot.initialize_portfolio()
        
        # Get API credentials from environment
        api_key = os.getenv('EXCHANGE_API_KEY')
        api_secret = os.getenv('EXCHANGE_API_SECRET')
        
        if not api_key or not api_secret:
            print("Error: EXCHANGE_API_KEY and EXCHANGE_API_SECRET required in .env")
            return
        
        # Connect to exchange
        bot.connect_exchange(api_key, api_secret)
        
        # Start live trading
        symbols = [args.symbol]
        bot.execute_live_trading(symbols)


if __name__ == '__main__':
    main()
