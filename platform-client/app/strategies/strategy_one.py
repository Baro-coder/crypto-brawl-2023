import numpy as np
import talib

from core.models.schemas import Candle


class TradingStrategyOne:
    def __init__(self, short_ema_length, long_ema_length, stop_loss, window_size):
        self.short_ema_length = short_ema_length
        self.long_ema_length = long_ema_length
        self.stop_loss = stop_loss
        self.window_size = window_size
        self.candles : list[Candle] = []
        self.transactions = False
        self.stop_loss_price = None

    def update_candle(self, candle: Candle):
        self.candles.append(candle)

        if len(self.candles) > self.window_size:
            self.candles.pop(0)

    def generate_signal(self):
        if len(self.candles) < self.window_size:
            return "INSUFFICIENT_DATA"

        close_prices = np.array([candle.close for candle in self.candles[-self.window_size:]])
        ema_short = talib.EMA(close_prices, timeperiod=self.short_ema_length)
        ema_long = talib.EMA(close_prices, timeperiod=self.long_ema_length)

        if self.transactions is False and ema_short[-1] > ema_long[-1]:
            signal = "BUY"
            self.transactions = True
            self.stop_loss_price = close_prices[-1] * (1 - self.stop_loss)
        elif self.transactions and ema_short[-1] < ema_long[-1]:
            signal = "SELL"
            self.transactions = False
        elif self.transactions and close_prices[-1] < self.stop_loss_price:
            signal = "SELL"
            self.transactions = False
        else:
            signal = "HOLD"

        return signal

    def execute_test_trade(self, signal):

        if signal == "BUY":
            print("Executing BUY order")
            return signal, self.candles[-1]

        elif signal == "SELL":
            print("Executing SELL order")
            return signal, self.candles[-1]
        else:
            return None, None
