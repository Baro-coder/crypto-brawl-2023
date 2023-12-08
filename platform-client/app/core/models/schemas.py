from typing import NamedTuple
from .enums import CurrencyId

class Candle(NamedTuple):
    time    : int
    open    : float 
    high    : float 
    low     : float 
    close   : float 

    def __repr__(self) -> str:
        return f'Candle(time[{self.time}], open[{self.open}], high[{self.high}], low[{self.low}], close[{self.close}])'
