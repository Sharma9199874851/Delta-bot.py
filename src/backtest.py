"""Backtesting engine for strategy validation."""

import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Tuple
from src.strategy import SwingTradingStrategy
from src.portfolio import Portfolio
from datetime import datetime, timedelta


class Backtester:
    """Backtest trading strategy on historical data."""

    def __init__(self, config: Dict, strategy: SwingTradingStrategy):
        """Initialize backtester."""
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.strategy = strategy

    def run(self, price_data: pd.DataFrame, volume_data: pd.DataFrame) -> Dict:
        """
        Run backtest on historical data.
        
        Args:
            price_data: DataFrame with OHLCV price data
            volume_data: DataFrame with volume data
        
        Returns:
            Backtest results and statistics
        """
        portfolio = Portfolio(self.config['trading']['initial_capital'])
        signals = []
        trades = []
        equity_curve = [portfolio.balance]
        
        # Get price series
        prices = price_data['close'].values
        volumes = volume_data.values if isinstance(volume_data, pd.Series) else volume_data

        # Iterate through each candle
        for i in range(len(prices)):
            # Only generate signal after sufficient data points
            if i < 50:
                continue

            current_price = prices[i]
            historical_prices = prices[:i+1]
            historical_volumes = volumes[:i+1] if len(volumes) > 0 else np.ones(i+1)

            # Generate signal
            signal, confidence = self.strategy.generate_signal(historical_prices, historical_volumes)
            signals.append({
                'index': i,
                'signal': signal,
                'confidence': confidence,
                'price': current_price
            })

            # Execute trades based on signal
            if signal == 'BUY' and len(portfolio.positions) < self.config['risk']['max_concurrent_positions']:
                position_size = self.strategy.calculate_position_size(portfolio.balance, signal)
                if position_size > 0:
                    entry_price = self.strategy.get_entry_price(current_price, signal)
                    stop_loss = self.strategy.get_stop_loss_price(entry_price, signal)
                    take_profit = self.strategy.get_take_profit_price(entry_price, signal)

                    quantity = position_size / entry_price
                    position = portfolio.open_position(
                        symbol=price_data.name if hasattr(price_data, 'name') else 'TRADE',
                        entry_price=entry_price,
                        quantity=quantity,
                        position_type='LONG',
                        stop_loss=stop_loss,
                        take_profit=take_profit
                    )

            elif signal == 'SELL' and len(portfolio.positions) > 0:
                # Close oldest position
                position = portfolio.positions[0]
                portfolio.close_position(position, current_price)
                trades.append({
                    'entry_price': position.entry_price,
                    'exit_price': position.exit_price,
                    'profit_loss': position.profit_loss,
                    'profit_loss_percent': position.profit_loss_percent
                })

            # Check stop losses and take profits
            for position in portfolio.positions[:]:
                triggered = portfolio.check_stops(position.symbol, current_price)
                if triggered:
                    portfolio.close_position(triggered, current_price)
                    trades.append({
                        'entry_price': triggered.entry_price,
                        'exit_price': triggered.exit_price,
                        'profit_loss': triggered.profit_loss,
                        'profit_loss_percent': triggered.profit_loss_percent
                    })

            # Update equity curve
            unrealized_pnl = sum([p.profit_loss for p in portfolio.positions])
            equity_curve.append(portfolio.balance + unrealized_pnl)

        # Calculate statistics
        stats = self._calculate_stats(portfolio, trades, equity_curve)
        
        return {
            'portfolio': portfolio,
            'trades': trades,
            'signals': signals,
            'equity_curve': equity_curve,
            'statistics': stats
        }

    def _calculate_stats(self, portfolio: Portfolio, trades: List[Dict], equity_curve: List[float]) -> Dict:
        """Calculate backtest statistics."""
        if len(trades) == 0:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_profit_loss': 0.0,
                'avg_profit_per_trade': 0.0,
                'best_trade': 0.0,
                'worst_trade': 0.0,
                'roi': 0.0,
                'max_drawdown': 0.0,
                'sharpe_ratio': 0.0
            }

        winning_trades = len([t for t in trades if t['profit_loss'] > 0])
        losing_trades = len([t for t in trades if t['profit_loss'] < 0])
        total_pnl = sum([t['profit_loss'] for t in trades])
        
        # Calculate max drawdown
        max_drawdown = self._calculate_max_drawdown(equity_curve)
        
        # Calculate Sharpe ratio (simplified)
        returns = np.diff(equity_curve) / np.array(equity_curve[:-1])
        sharpe_ratio = np.mean(returns) / (np.std(returns) + 1e-6) if len(returns) > 0 else 0

        return {
            'total_trades': len(trades),
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': (winning_trades / len(trades)) * 100 if len(trades) > 0 else 0,
            'total_profit_loss': total_pnl,
            'avg_profit_per_trade': total_pnl / len(trades) if len(trades) > 0 else 0,
            'best_trade': max([t['profit_loss'] for t in trades]) if trades else 0,
            'worst_trade': min([t['profit_loss'] for t in trades]) if trades else 0,
            'roi': (total_pnl / self.config['trading']['initial_capital']) * 100,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio
        }

    @staticmethod
    def _calculate_max_drawdown(equity_curve: List[float]) -> float:
        """Calculate maximum drawdown."""
        if len(equity_curve) < 2:
            return 0.0
        
        peak = equity_curve[0]
        max_dd = 0.0
        
        for value in equity_curve:
            if value > peak:
                peak = value
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd
        
        return max_dd * 100
