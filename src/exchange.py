"""Exchange integration for live trading."""

import ccxt
import logging
from typing import Dict, List, Optional


class ExchangeConnector:
    """Connect to crypto exchanges (Binance, Coinbase, etc.)"""

    def __init__(self, exchange_name: str, api_key: str, api_secret: str):
        """Initialize exchange connection."""
        self.logger = logging.getLogger(__name__)
        self.exchange_name = exchange_name.lower()

        try:
            ExchangeClass = getattr(ccxt, self.exchange_name)
            self.exchange = ExchangeClass({
                'apiKey': api_key,
                'secret': api_secret,
                'enableRateLimit': True
            })
        except AttributeError:
            self.logger.error(f"Exchange {exchange_name} not supported")
            raise

    def get_balance(self) -> Dict:
        """Get account balance."""
        try:
            balance = self.exchange.fetch_balance()
            return balance
        except Exception as e:
            self.logger.error(f"Error fetching balance: {e}")
            return {}

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int = 100) -> List:
        """Get OHLCV (candlestick) data."""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            self.logger.error(f"Error fetching OHLCV for {symbol}: {e}")
            return []

    def create_market_order(self, symbol: str, order_type: str, amount: float) -> Dict:
        """Create market order (BUY or SELL)."""
        try:
            if order_type.upper() == 'BUY':
                order = self.exchange.create_market_buy_order(symbol, amount)
            elif order_type.upper() == 'SELL':
                order = self.exchange.create_market_sell_order(symbol, amount)
            else:
                raise ValueError(f"Invalid order type: {order_type}")
            self.logger.info(f"Order created: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error creating order: {e}")
            return {}

    def create_limit_order(self, symbol: str, order_type: str, amount: float, price: float) -> Dict:
        """Create limit order."""
        try:
            if order_type.upper() == 'BUY':
                order = self.exchange.create_limit_buy_order(symbol, amount, price)
            elif order_type.upper() == 'SELL':
                order = self.exchange.create_limit_sell_order(symbol, amount, price)
            else:
                raise ValueError(f"Invalid order type: {order_type}")
            self.logger.info(f"Limit order created: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error creating limit order: {e}")
            return {}

    def cancel_order(self, order_id: str, symbol: str) -> Dict:
        """Cancel existing order."""
        try:
            result = self.exchange.cancel_order(order_id, symbol)
            self.logger.info(f"Order cancelled: {order_id}")
            return result
        except Exception as e:
            self.logger.error(f"Error cancelling order: {e}")
            return {}

    def get_open_orders(self, symbol: Optional[str] = None) -> List:
        """Get open orders."""
        try:
            orders = self.exchange.fetch_open_orders(symbol)
            return orders
        except Exception as e:
            self.logger.error(f"Error fetching open orders: {e}")
            return []

    def get_order_status(self, order_id: str, symbol: str) -> Dict:
        """Get order status."""
        try:
            order = self.exchange.fetch_order(order_id, symbol)
            return order
        except Exception as e:
            self.logger.error(f"Error fetching order: {e}")
            return {}
