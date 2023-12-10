from typing import Tuple

import numpy as np
import talib

from core.models.enums import Signal
from core.models.schemas import Candle
from core.utils.store import store_in_csv


class TradingStrategyOne:
    def __init__(self, short_ema_length, long_ema_length, stop_loss, window_size, data_csv_file):
        self.short_ema_length: int = short_ema_length
        self.long_ema_length: int = long_ema_length
        self.stop_loss: float = stop_loss
        self.window_size: int = window_size
        self.candles: list[Candle] = []
        self.transactions: bool = False
        self.stop_loss_price: float = None
        self.data_csv_file: str = data_csv_file
        self.open_price: int = None

    def set_transaction_flag(self, flag: bool):
        self.transactions = flag

    def update_candle(self, candle: Candle) -> None:
        if len(self.candles) == 0 or self.candles[-1].time < candle.time:
            self.candles.append(candle)
            store_in_csv(self.data_csv_file, candle)

            if len(self.candles) > self.window_size:
                self.candles.pop(0)

    def generate_signal(self) -> tuple[Signal, Candle]:
        if len(self.candles) < self.window_size:
            raise Exception(f'Insufficient data - candles count [{len.self.candles}]')

        close_prices = np.array([candle.close for candle in self.candles[-self.window_size:]])
        ema_short = talib.EMA(close_prices, timeperiod=self.short_ema_length)
        ema_long = talib.EMA(close_prices, timeperiod=self.long_ema_length)

        if self.transactions is False and ema_short[-1] > ema_long[-1]:
            signal = Signal.BUY
            self.stop_loss_price = close_prices[-1] * (1 - self.stop_loss)
            self.open_price = close_prices[-1]

        elif self.transactions and ema_short[-1] < ema_long[-1]:
            signal = Signal.SELL

        elif self.transactions and close_prices[-1] < self.stop_loss_price:
            signal = Signal.SELL

        elif self.transactions and close_prices[-1] > self.open_price:
            self.stop_loss_price = close_prices[-1] * (1 - self.stop_loss)
            signal = Signal.HOLD

        else:
            signal = Signal.HOLD

        return signal, self.candles[-1]

    def execute_test_trade(self, signal: Signal):

        if signal == Signal.BUY:
            print("Executing BUY order")
            return signal, self.candles[-1]

        elif signal == Signal.SELL:
            print("Executing SELL order")
            return signal, self.candles[-1]
        else:
            return None, None

    def __str__(self):
        return (
            f"TradingStrategyTwo("
            f"short_ema_length={self.short_ema_length}, "
            f"long_ema_length={self.long_ema_length}, "
            f"stop_loss={self.stop_loss}, "
            f"window_size={self.window_size}, "
            f"data_csv_file='{self.data_csv_file}'"
            f")"
        )
