import numpy as np
import talib

from core.models.enums import Signal
from core.models.schemas import Candle
from core.utils import store_in_csv


class TradingStrategyTwo:
    def __init__(self, stoch_length, stoch_d_length, overbought_threshold, oversold_threshold, stop_loss, window_size, data_csv_file):
        self.stoch_length : int = stoch_length
        self.stoch_d_length : int = stoch_d_length
        self.overbought_threshold : int = overbought_threshold
        self.oversold_threshold : int = oversold_threshold
        self.stop_loss : float = stop_loss
        self.window_size : int = window_size
        self.candles: list[Candle] = []
        self.transactions :bool = False
        self.stop_loss_price :float = None
        self.data_csv_file: str = data_csv_file

    def update_candle(self, candle: Candle) -> None:
        if len(self.candles) == 0 or self.candles[-1].time < candle.time:
            self.candles.append(candle)
            store_in_csv(self.data_csv_file, candle)

            if len(self.candles) > self.window_size:
                self.candles.pop(0)

    def generate_signal(self):
        if len(self.candles) < self.window_size:
            raise Exception(f'Insufficient data - candles count [{len.self.candles}]')

        close_prices = np.array([candle.close for candle in self.candles[-self.window_size:]])

        stoch, stoch_d = talib.STOCH(close_prices, close_prices, close_prices,
                                     fastk_period=self.stoch_length, slowk_period=self.stoch_d_length,
                                     slowd_period=self.stoch_d_length)

        if self.transactions is False and stoch[-1] < self.oversold_threshold and stoch_d[-1] < self.oversold_threshold:
            signal = Signal.BUY
            self.transactions = True
            self.stop_loss_price = close_prices[-1] * (1 - self.stop_loss)
        elif self.transactions and (stoch[-1] > self.overbought_threshold or stoch_d[-1] > self.overbought_threshold):
            signal = Signal.SELL
            self.transactions = False
        elif self.transactions and close_prices[-1] < self.stop_loss_price:
            signal = Signal.SELL
            self.transactions = False
        else:
            signal = Signal.HOLD

        return signal, self.candles[-1]

    def execute_test_trade(self, signal):
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
            f"stoch_length={self.stoch_length}, "
            f"stoch_d_length={self.stoch_d_length}, "
            f"overbought_threshold={self.overbought_threshold}, "
            f"oversold_threshold={self.oversold_threshold}, "
            f"stop_loss={self.stop_loss}, "
            f"window_size={self.window_size}, "
            f"data_csv_file='{self.data_csv_file}'"
            f")"
        )