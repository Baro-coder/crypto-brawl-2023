import numpy as np
import talib

from core.models.enums import Signal
from core.models.schemas import Candle
from core.utils.store import store_in_csv


class TradingStrategyOne:
    def __init__(self, short_ema_length, long_ema_length, stop_loss, window_size, data_csv_file):
        self.short_ema_length   : int           = short_ema_length
        self.long_ema_length    : int           = long_ema_length
        self.stop_loss          : float         = stop_loss
        self.window_size        : int           = window_size
        self.candles            : list[Candle]  = []
        self.transactions       : bool          = False
        self.stop_loss_price    : float         = None
        self.data_csv_file      : str           = data_csv_file


    def update_candle(self, candle: Candle) -> None:
        if len(self.candles) == 0 or self.candles[-1].time < candle.time:
            self.candles.append(candle)
            store_in_csv(self.data_csv_file, candle)

            if len(self.candles) > self.window_size:
                self.candles.pop(0)


    def generate_signal(self) -> Signal:
        if len(self.candles) < self.window_size:
            raise Exception(f'Insufficient data - candles count [{len.self.candles}]')

        close_prices = np.array([candle.close for candle in self.candles[-self.window_size:]])
        ema_short = talib.EMA(close_prices, timeperiod=self.short_ema_length)
        ema_long = talib.EMA(close_prices, timeperiod=self.long_ema_length)

        if self.transactions is False and ema_short[-1] > ema_long[-1]:
            signal = Signal.BUY
            self.transactions = True
            self.stop_loss_price = close_prices[-1] * (1 - self.stop_loss)
            
        elif self.transactions and ema_short[-1] < ema_long[-1]:
            signal = Signal.SELL
            self.transactions = False
            
        elif self.transactions and close_prices[-1] < self.stop_loss_price:
            signal = Signal.SELL
            self.transactions = False
            
        else:
            signal = Signal.HOLD

        return signal


    def execute_test_trade(self, signal: Signal):

        if signal == Signal.BUY:
            print("Executing BUY order")
            return signal, self.candles[-1]

        elif signal == Signal.SELL:
            print("Executing SELL order")
            return signal, self.candles[-1]
        else:
            return None, None
