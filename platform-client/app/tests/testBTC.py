from core.models.schemas import Candle
from strategies.strategy_one import TradingStrategyOne
from strategies.strategy_two import TradingStrategyTwo
from core.utils.store import read_candles_from_csv

balance = None
purchase_price = None
bought_count, sold_count = 0, 0

current_file_path = ""
candles_data: list[Candle] = []


def run_test_one(file_path, short_ema_length, long_ema_length, stop_loss, window_size, start_balance):
    global balance, bought_count, sold_count, candles_data
    balance = start_balance
    bought_count, sold_count = 0, 0

    if file_path != current_file_path or candles_data == []:
        candles_data = read_candles_from_csv(file_path)

    strategy = TradingStrategyOne(short_ema_length=short_ema_length, long_ema_length=long_ema_length,
                                  stop_loss=stop_loss, window_size=window_size)

    for candle in candles_data:
        # print(candle.time)
        strategy.update_candle(candle)
        signal = strategy.generate_signal()
        received_signal, current_price = strategy.execute_test_trade(signal)
        update_balance(received_signal, current_price)

    # print("Total balance:" + str(balance))
    return balance, bought_count, sold_count


def run_test_two(file_path, stoch_length, stoch_d_length, overbought_threshold, oversold_threshold, stop_loss,
                 window_size, start_balance):
    global balance, bought_count, sold_count
    balance = start_balance
    bought_count, sold_count = 0, 0
    candles_data: list[Candle] = read_candles_from_csv(file_path)

    strategy = TradingStrategyTwo(stoch_length=stoch_length, stoch_d_length=stoch_d_length,
                                  overbought_threshold=overbought_threshold, oversold_threshold=oversold_threshold,
                                  stop_loss=stop_loss, window_size=window_size)

    for candle in candles_data:
        # print(candle.time)
        strategy.update_candle(candle)
        signal = strategy.generate_signal()
        received_signal, current_price = strategy.execute_test_trade(signal)
        update_balance(received_signal, current_price)

    # print("Total balance:" + str(balance))
    return balance, bought_count, sold_count


def update_balance(received_signal: str | None, current_price: Candle | None):
    global balance, bought_count, sold_count
    global purchase_price

    if received_signal is None or current_price is None:
        return

    if received_signal == "BUY":
        purchase_price = current_price.close
        # print(balance)
        bought_count += 1
    elif received_signal == "SELL":
        balance = balance * (current_price.close / purchase_price)
        sold_count += 1
        # print("Balance after sell: " + str(balance))
    else:
        pass
