"""Trading strategy implementation."""

import numpy as np
from typing import Dict, Tuple
from src.indicators import TechnicalIndicators


class SwingTradingStrategy:
    """Crypto swing trading strategy based on technical analysis."""

    def __init__(self, config: Dict):
        """Initialize strategy with configuration."""
        self.config = config
        self.strategy_config = config['strategy']
        self.indicator_config = config['indicators']

    def generate_signal(self, prices: np.ndarray, volumes: np.ndarray) -> Tuple[str, float]:
        """
        Generate trading signal: 'BUY', 'SELL', or 'HOLD'.
        Returns: (signal, confidence)
        """
        if len(prices) < max(50, self.indicator_config['macd']['slow'] + 5):
            return 'HOLD', 0.0

        indicators = TechnicalIndicators.calculate_all(prices, self.config)
        current_price = prices[-1]
        current_rsi = indicators['rsi'][-1]
        current_macd = indicators['macd'][-1]
        current_macd_signal = indicators['macd_signal'][-1]
        current_macd_hist = indicators['macd_histogram'][-1]
        current_bb_upper = indicators['bb_upper'][-1]
        current_bb_lower = indicators['bb_lower'][-1]

        # BUY Signal Logic
        buy_signals = 0
        buy_confidence = 0.0

        # Signal 1: RSI oversold + reversal
        if current_rsi < self.indicator_config['rsi']['oversold'] + 10:
            buy_signals += 1
            buy_confidence += 0.3

        # Signal 2: MACD bullish crossover
        if current_macd > current_macd_signal and current_macd_hist > 0:
            if indicators['macd_histogram'][-2] <= 0:  # Just crossed
                buy_signals += 1
                buy_confidence += 0.35
            else:
                buy_confidence += 0.15

        # Signal 3: Price at lower Bollinger Band (mean reversion)
        if current_price <= current_bb_lower * 1.02:  # Within 2% of lower band
            buy_signals += 1
            buy_confidence += 0.35

        # SELL Signal Logic
        sell_signals = 0
        sell_confidence = 0.0

        # Signal 1: RSI overbought
        if current_rsi > self.indicator_config['rsi']['overbought'] - 10:
            sell_signals += 1
            sell_confidence += 0.3

        # Signal 2: MACD bearish crossover
        if current_macd < current_macd_signal and current_macd_hist < 0:
            if indicators['macd_histogram'][-2] >= 0:  # Just crossed
                sell_signals += 1
                sell_confidence += 0.35
            else:
                sell_confidence += 0.15

        # Signal 3: Price at upper Bollinger Band
        if current_price >= current_bb_upper * 0.98:  # Within 2% of upper band
            sell_signals += 1
            sell_confidence += 0.35

        # Determine final signal
        threshold = self.strategy_config['entry_confirmation']
        min_confidence = self.strategy_config['momentum_threshold']

        if buy_signals >= threshold and buy_confidence >= min_confidence:
            return 'BUY', min(buy_confidence, 1.0)
        elif sell_signals >= threshold and sell_confidence >= min_confidence:
            return 'SELL', min(sell_confidence, 1.0)
        else:
            return 'HOLD', max(buy_confidence, sell_confidence)

    def get_entry_price(self, price: float, signal: str) -> float:
        """Get optimal entry price based on signal."""
        if signal == 'BUY':
            return price * 0.99  # Buy slightly below current price
        elif signal == 'SELL':
            return price * 1.01  # Sell slightly above current price
        return price

    def calculate_position_size(self, available_balance: float, signal: str) -> float:
        """Calculate position size based on risk management."""
        max_size = self.config['risk']['max_position_size']
        position_size = available_balance * max_size
        return position_size

    def get_stop_loss_price(self, entry_price: float, signal: str) -> float:
        """Calculate stop loss price."""
        stop_loss_pct = self.config['risk']['stop_loss_percent'] / 100
        if signal == 'BUY':
            return entry_price * (1 - stop_loss_pct)
        else:
            return entry_price * (1 + stop_loss_pct)

    def get_take_profit_price(self, entry_price: float, signal: str) -> float:
        """Calculate take profit price."""
        take_profit_pct = self.config['risk']['take_profit_percent'] / 100
        if signal == 'BUY':
            return entry_price * (1 + take_profit_pct)
        else:
            return entry_price * (1 - take_profit_pct)
