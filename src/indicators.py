"""Technical indicators for trading signals."""

import numpy as np
import pandas as pd
from typing import Tuple, Dict


class TechnicalIndicators:
    """Calculate technical indicators for trading analysis."""

    @staticmethod
    def rsi(prices: np.ndarray, period: int = 14) -> np.ndarray:
        """Calculate Relative Strength Index."""
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down if down != 0 else 0
        rsi_values = np.zeros_like(prices)
        rsi_values[:period] = 100. - 100. / (1. + rs)

        for i in range(period, len(prices)):
            delta = deltas[i-1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up * (period - 1) + upval) / period
            down = (down * (period - 1) + downval) / period

            rs = up / down if down != 0 else 0
            rsi_values[i] = 100. - 100. / (1. + rs)

        return rsi_values

    @staticmethod
    def macd(prices: np.ndarray, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Calculate MACD (Moving Average Convergence Divergence)."""
        ema_fast = pd.Series(prices).ewm(span=fast).mean().values
        ema_slow = pd.Series(prices).ewm(span=slow).mean().values
        macd_line = ema_fast - ema_slow
        signal_line = pd.Series(macd_line).ewm(span=signal).mean().values
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    @staticmethod
    def bollinger_bands(prices: np.ndarray, period: int = 20, std_dev: float = 2) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Calculate Bollinger Bands."""
        sma = pd.Series(prices).rolling(window=period).mean().values
        std = pd.Series(prices).rolling(window=period).std().values
        upper_band = sma + (std_dev * std)
        lower_band = sma - (std_dev * std)
        return upper_band, sma, lower_band

    @staticmethod
    def calculate_all(prices: np.ndarray, config: Dict) -> Dict:
        """Calculate all indicators."""
        rsi_config = config['indicators']['rsi']
        macd_config = config['indicators']['macd']
        bb_config = config['indicators']['bollinger_bands']

        rsi_values = TechnicalIndicators.rsi(prices, rsi_config['period'])
        macd_line, signal_line, histogram = TechnicalIndicators.macd(
            prices,
            macd_config['fast'],
            macd_config['slow'],
            macd_config['signal']
        )
        upper_bb, middle_bb, lower_bb = TechnicalIndicators.bollinger_bands(
            prices,
            bb_config['period'],
            bb_config['std_dev']
        )

        return {
            'rsi': rsi_values,
            'macd': macd_line,
            'macd_signal': signal_line,
            'macd_histogram': histogram,
            'bb_upper': upper_bb,
            'bb_middle': middle_bb,
            'bb_lower': lower_bb
        }
