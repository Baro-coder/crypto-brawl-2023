from enum import Enum

class CurrencyId(Enum):
    BTC = 'BTC'
    ETH = 'ETH'
    USD = 'USD'


class Type(Enum):
    CURRENT = 'current'


class Signal(Enum):
    BUY  = 0
    SELL = 1
    HOLD = 2
