"""Portfolio and position management."""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Position:
    """Represents an active trading position."""
    symbol: str
    entry_price: float
    quantity: float
    position_type: str  # 'LONG' or 'SHORT'
    entry_time: datetime
    stop_loss: float
    take_profit: float
    status: str = 'OPEN'  # OPEN, CLOSED, SL_HIT, TP_HIT
    exit_price: Optional[float] = None
    exit_time: Optional[datetime] = None
    profit_loss: float = 0.0
    profit_loss_percent: float = 0.0
    metadata: Dict = field(default_factory=dict)

    def update_pnl(self, current_price: float):
        """Update profit/loss based on current price."""
        if self.position_type == 'LONG':
            self.profit_loss = (current_price - self.entry_price) * self.quantity
            self.profit_loss_percent = ((current_price - self.entry_price) / self.entry_price) * 100
        else:  # SHORT
            self.profit_loss = (self.entry_price - current_price) * self.quantity
            self.profit_loss_percent = ((self.entry_price - current_price) / self.entry_price) * 100

    def close(self, exit_price: float, exit_time: datetime):
        """Close the position."""
        self.exit_price = exit_price
        self.exit_time = exit_time
        self.status = 'CLOSED'
        self.update_pnl(exit_price)


class Portfolio:
    """Manage trading portfolio and positions."""

    def __init__(self, initial_balance: float):
        """Initialize portfolio."""
        self.logger = logging.getLogger(__name__)
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions: List[Position] = []
        self.closed_positions: List[Position] = []
        self.trade_history: List[Dict] = []

    def open_position(self, symbol: str, entry_price: float, quantity: float,
                      position_type: str, stop_loss: float, take_profit: float) -> Position:
        """Open a new trading position."""
        position = Position(
            symbol=symbol,
            entry_price=entry_price,
            quantity=quantity,
            position_type=position_type,
            entry_time=datetime.now(),
            stop_loss=stop_loss,
            take_profit=take_profit
        )
        self.positions.append(position)
        self.balance -= entry_price * quantity  # Deduct from balance
        self.logger.info(f"Position opened: {position}")
        return position

    def close_position(self, position: Position, exit_price: float):
        """Close a trading position."""
        position.close(exit_price, datetime.now())
        self.positions.remove(position)
        self.closed_positions.append(position)
        self.balance += exit_price * position.quantity  # Add back to balance
        self.balance += position.profit_loss  # Add PnL

        self.logger.info(f"Position closed: {position.symbol} | PnL: ${position.profit_loss:.2f} ({position.profit_loss_percent:.2f}%)")
        self.trade_history.append({
            'symbol': position.symbol,
            'entry_price': position.entry_price,
            'exit_price': position.exit_price,
            'quantity': position.quantity,
            'profit_loss': position.profit_loss,
            'profit_loss_percent': position.profit_loss_percent,
            'entry_time': position.entry_time,
            'exit_time': position.exit_time
        })

    def check_stops(self, symbol: str, current_price: float) -> Optional[Position]:
        """Check if any positions hit stop loss or take profit."""
        for position in self.positions:
            if position.symbol != symbol:
                continue

            position.update_pnl(current_price)

            if position.position_type == 'LONG':
                if current_price <= position.stop_loss:
                    position.status = 'SL_HIT'
                    return position
                elif current_price >= position.take_profit:
                    position.status = 'TP_HIT'
                    return position
            else:  # SHORT
                if current_price >= position.stop_loss:
                    position.status = 'SL_HIT'
                    return position
                elif current_price <= position.take_profit:
                    position.status = 'TP_HIT'
                    return position

        return None

    def get_active_positions(self, symbol: Optional[str] = None) -> List[Position]:
        """Get active positions."""
        if symbol:
            return [p for p in self.positions if p.symbol == symbol]
        return self.positions

    def get_portfolio_stats(self) -> Dict:
        """Get portfolio statistics."""
        total_trades = len(self.closed_positions)
        if total_trades == 0:
            return {
                'total_balance': self.balance,
                'available_balance': self.balance,
                'open_positions': len(self.positions),
                'closed_trades': 0,
                'win_rate': 0.0,
                'total_profit_loss': 0.0,
                'roi': 0.0
            }

        winning_trades = len([p for p in self.closed_positions if p.profit_loss > 0])
        total_pnl = sum([p.profit_loss for p in self.closed_positions])
        roi = (total_pnl / self.initial_balance) * 100

        return {
            'total_balance': self.balance,
            'available_balance': self.balance,
            'open_positions': len(self.positions),
            'closed_trades': total_trades,
            'win_rate': (winning_trades / total_trades) * 100,
            'total_profit_loss': total_pnl,
            'roi': roi
        }
