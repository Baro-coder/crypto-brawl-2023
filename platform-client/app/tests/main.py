from testBTC import run_test_one, run_test_two

balance = 1000000

def test_one():
    files_path = ['../test_data/ATAI-Dev.BTC.MIN1_new_week.csv',
                  '../test_data/ATAI-Dev.BTC.MIN5_new_week.csv',
                  '../test_data/ATAI-Dev.ETH.MIN1_new_week.csv',
                  '../test_data/ATAI-Dev.ETH.MIN5_new_week.csv',
                  '../data/BTC.csv']

    for file_path in files_path:
        best_short_ema_length = 0
        best_long_ema_length = 0
        best_stop_loss = 0
        best_total_balance = 0
        best_total_profit = 0
        current_files_path = ""
        for short_ema_length in range(7, 20):
            for long_ema_length in range(20, 50):
                for stop_loss in range(1, 20):
                    total_balance = run_test_one(file_path, short_ema_length=short_ema_length,
                                                 long_ema_length=long_ema_length,
                                                 stop_loss=stop_loss / 1000, window_size=50, start_balance=balance)

                    if total_balance > best_total_balance:
                        best_total_balance = total_balance
                        best_short_ema_length = short_ema_length
                        best_long_ema_length = long_ema_length
                        best_stop_loss = stop_loss / 1000
                        best_total_profit = best_total_balance - balance
                        current_files_path = file_path

        print(f'Najlepsze parametry strategii:')
        print(f'Short EMA Length: {best_short_ema_length}')
        print(f'Long EMA Length: {best_long_ema_length}')
        print(f'Stop Loss: {best_stop_loss}')
        print(f'Total Balance: {best_total_balance}')
        print(f'Total Profit: {best_total_profit}')
        print(f'File Path: {current_files_path}')
def test_two():
    files_path = ['../test_data/ATAI-Dev.BTC.MIN1_new_week.csv',
                  '../test_data/ATAI-Dev.BTC.MIN5_new_week.csv',
                  '../test_data/ATAI-Dev.ETH.MIN1_new_week.csv',
                  '../test_data/ATAI-Dev.ETH.MIN5_new_week.csv',
                  '../data/BTC.csv']

    for file_path in files_path:
        best_stoch_d_length = 0
        best_stoch_length = 0
        best_stop_loss = 0
        best_total_balance = 0
        best_total_profit = 0
        current_files_path = ""
        for stoch_length in range(7, 30):
            for stoch_d_length in range(1, 20):
                for stop_loss in range(1, 20):
                    for overbought_threshold in range(70, 90, 5):
                        for oversold_threshold in range(10, 30, 5):
                            total_balance = run_test_two(file_path, stoch_length=stoch_length, stoch_d_length=stoch_d_length, overbought_threshold=overbought_threshold, oversold_threshold=overbought_threshold,
                                                         stop_loss=stop_loss / 1000, window_size=50, start_balance=balance)

                            if total_balance > best_total_balance:
                                best_total_balance = total_balance
                                best_stoch_length = stoch_length
                                best_stoch_d_length = stoch_d_length
                                best_stop_loss = stop_loss / 1000
                                best_total_profit = best_total_balance - balance
                                current_files_path = file_path

        print(f'Najlepsze parametry strategii:')
        print(f'Stoch: {best_stoch_length}')
        print(f'd_stoch: {best_stoch_d_length}')
        print(f'Stop Loss: {best_stop_loss}')
        print(f'Total Balance: {best_total_balance}')
        print(f'Total Profit: {best_total_profit}')
        print(f'File Path: {current_files_path}')

def main():
    test_one()
    test_two()


if __name__ == "__main__":
    main()
