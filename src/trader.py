"""Main trading engine."""

import logging
import yaml
from typing import Dict, Optional
from src.exchange import ExchangeConnector
from src.strategy import SwingTradingStrategy
from src.portfolio import Portfolio
from src.backtest import Backtester
import pandas as pd
import numpy as np


class DeltaTradingBot:
    """Main trading bot engine."""

    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize the trading bot."""
        self.logger = self._setup_logging()
        self.config = self._load_config(config_path)
        self.strategy = SwingTradingStrategy(self.config)
        self.portfolio = None
        self.exchange = None

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger('DeltaBot')
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler
        fh = logging.FileHandler('logs/trading.log')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        return logger

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            self.logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            self.logger.error(f"Configuration file {config_path} not found")
            raise

    def connect_exchange(self, api_key: str, api_secret: str):
        """Connect to exchange with credentials."""
        try:
            exchange_name = self.config['trading']['exchange']
            self.exchange = ExchangeConnector(exchange_name, api_key, api_secret)
            self.logger.info(f"Connected to {exchange_name}")
        except Exception as e:
            self.logger.error(f"Failed to connect to exchange: {e}")
            raise

    def initialize_portfolio(self, initial_balance: Optional[float] = None):
        """Initialize portfolio with initial balance."""
        balance = initial_balance or self.config['trading']['initial_capital']
        self.portfolio = Portfolio(balance)
        self.logger.info(f"Portfolio initialized with ${balance}")

    def backtest(self, symbol: str, timeframe: str, historical_data: pd.DataFrame) -> Dict:
        """
        Run backtest on provided historical data.
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Candle timeframe (e.g., '4h')
            historical_data: DataFrame with OHLCV data
        
        Returns:
            Backtest results
        """
        self.logger.info(f"Starting backtest for {symbol} on {timeframe}")
        
        backtester = Backtester(self.config, self.strategy)
        
        prices = historical_data['close']
        volumes = historical_data['volume'] if 'volume' in historical_data else np.ones(len(historical_data))
        
        results = backtester.run(prices, volumes)
        
        # Log results
        stats = results['statistics']
        self.logger.info(f"Backtest completed: {stats['total_trades']} trades")
        self.logger.info(f"Win Rate: {stats['win_rate']:.2f}%")
        self.logger.info(f"ROI: {stats['roi']:.2f}%")
        
        return results

    def execute_live_trading(self, symbols: list):
        """
        Execute live trading on specified symbols.
        
        Args:
            symbols: List of trading pairs
        """
        if not self.exchange:
            self.logger.error("Exchange not connected")
            return
        
        if not self.portfolio:
            self.initialize_portfolio()
        
        self.logger.info(f"Starting live trading on {symbols}")
        
        try:
            while True:
                for symbol in symbols:
                    # Fetch OHLCV data
                    timeframe = self.config['trading']['timeframe']
                    ohlcv = self.exchange.get_ohlcv(symbol, timeframe, limit=100)
                    
                    if not ohlcv:
                        continue
                    
                    # Extract prices
                    prices = np.array([candle[4] for candle in ohlcv])  # Close prices
                    volumes = np.array([candle[5] for candle in ohlcv])
                    
                    # Generate signal
                    signal, confidence = self.strategy.generate_signal(prices, volumes)
                    self.logger.info(f"{symbol} Signal: {signal} (Confidence: {confidence:.2f})")
                    
                    # Execute trades
                    current_price = prices[-1]
                    
                    if signal == 'BUY' and len(self.portfolio.positions) < self.config['risk']['max_concurrent_positions']:
                        self._execute_buy(symbol, current_price, signal)
                    
                    elif signal == 'SELL' and len(self.portfolio.positions) > 0:
                        self._execute_sell(symbol, current_price)
                    
                    # Check stop losses and take profits
                    self._check_position_management(symbol, current_price)
        
        except KeyboardInterrupt:
            self.logger.info("Live trading stopped by user")
            self._print_portfolio_summary()

    def _execute_buy(self, symbol: str, current_price: float, signal: str):
        """Execute a buy order."""
        position_size_usd = self.strategy.calculate_position_size(self.portfolio.balance, signal)
        entry_price = self.strategy.get_entry_price(current_price, signal)
        quantity = position_size_usd / entry_price
        
        stop_loss = self.strategy.get_stop_loss_price(entry_price, signal)
        take_profit = self.strategy.get_take_profit_price(entry_price, signal)
        
        self.logger.info(f"BUY {symbol}: {quantity:.6f} @ ${entry_price:.2f} | SL: ${stop_loss:.2f} | TP: ${take_profit:.2f}")
        
        if self.config['trading']['live_trading']:
            order = self.exchange.create_market_order(symbol, 'BUY', quantity)
            if order:
                self.portfolio.open_position(symbol, entry_price, quantity, 'LONG', stop_loss, take_profit)

    def _execute_sell(self, symbol: str, current_price: float):
        """Execute a sell order."""
        positions = self.portfolio.get_active_positions(symbol)
        
        if positions:
            position = positions[0]
            quantity = position.quantity
            self.logger.info(f"SELL {symbol}: {quantity:.6f} @ ${current_price:.2f}")
            
            if self.config['trading']['live_trading']:
                order = self.exchange.create_market_order(symbol, 'SELL', quantity)
                if order:
                    self.portfolio.close_position(position, current_price)

    def _check_position_management(self, symbol: str, current_price: float):
        """Check and manage stop losses and take profits."""
        positions = self.portfolio.get_active_positions(symbol)
        
        for position in positions[:]:
            triggered = self.portfolio.check_stops(symbol, current_price)
            if triggered:
                reason = f"({triggered.status})"
                self.logger.info(f"Position closed {reason}: {symbol} @ ${current_price:.2f} | PnL: ${triggered.profit_loss:.2f}")
                
                if self.config['trading']['live_trading']:
                    self.portfolio.close_position(triggered, current_price)

    def _print_portfolio_summary(self):
        """Print portfolio summary."""
        if not self.portfolio:
            return
        
        stats = self.portfolio.get_portfolio_stats()
        self.logger.info("="*50)
        self.logger.info("PORTFOLIO SUMMARY")
        self.logger.info("="*50)
        self.logger.info(f"Total Balance: ${stats['total_balance']:.2f}")
        self.logger.info(f"Open Positions: {stats['open_positions']}")
        self.logger.info(f"Closed Trades: {stats['closed_trades']}")
        self.logger.info(f"Win Rate: {stats['win_rate']:.2f}%")
        self.logger.info(f"Total P&L: ${stats['total_profit_loss']:.2f}")
        self.logger.info(f"ROI: {stats['roi']:.2f}%")
        self.logger.info("="*50)
