import numpy as np
import talib

from core.models.schemas import Candle


class TradingStrategyTwo:
    def __init__(self, stoch_length, stoch_d_length, overbought_threshold, oversold_threshold, stop_loss, window_size):
        self.stoch_length = stoch_length
        self.stoch_d_length = stoch_d_length
        self.overbought_threshold = overbought_threshold
        self.oversold_threshold = oversold_threshold
        self.stop_loss = stop_loss
        self.window_size = window_size
        self.candles: list[Candle] = []
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

        stoch, stoch_d = talib.STOCH(close_prices, close_prices, close_prices,
                                     fastk_period=self.stoch_length, slowk_period=self.stoch_d_length,
                                     slowd_period=self.stoch_d_length)

        if self.transactions is False and stoch[-1] < self.oversold_threshold and stoch_d[-1] < self.oversold_threshold:
            signal = "BUY"
            self.transactions = True
            self.stop_loss_price = close_prices[-1] * (1 - self.stop_loss)
            # print(f"Buy price: {close_prices[-1]} with SL price: {self.stop_loss_price}")
        elif self.transactions and (stoch[-1] > self.overbought_threshold or stoch_d[-1] > self.overbought_threshold):
            signal = "SELL"
            self.transactions = False
            # print(f"Sell price: {close_prices[-1]}")
        elif self.transactions and close_prices[-1] < self.stop_loss_price:
            signal = "SELL"
            self.transactions = False
            # print(f"Sell by SL price: {close_prices[-1]}")
        else:
            signal = "HOLD"

        return signal

    def execute_test_trade(self, signal):
        if signal == "BUY":
            #print("Executing BUY order")
            return signal, self.candles[-1]
        elif signal == "SELL":
            #print("Executing SELL order")
            return signal, self.candles[-1]
        else:
            return None, None
