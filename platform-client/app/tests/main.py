from testBTC import run_test_one, run_test_two

balance = 1000000


def test_one():
    global sold_count, bought_count
    files_path = ['../test_data/ATAI-Dev.BTC.MIN1_new_week.csv',
                  '../test_data/ATAI-Dev.ETH.MIN1_new_week.csv',
                  ]
    # '../test_data/ATAI-Dev.BTC.MIN5_new_week.csv',
    # '../test_data/ATAI-Dev.ETH.MIN5_new_week.csv',
    # '../data/BTC.csv'

    for file_path in files_path:
        best_short_ema_length = 0
        best_long_ema_length = 0
        best_stop_loss = 0
        best_total_balance = 0
        best_total_profit = 0
        current_files_path = ""
        for short_ema_length in range(7, 20):
            for long_ema_length in range(20, 30):
                for stop_loss in range(1, 20):
                    total_balance, \
                        bought_count, \
                        sold_count = run_test_one(file_path, short_ema_length=short_ema_length,
                                                  long_ema_length=long_ema_length,
                                                  stop_loss=stop_loss / 1000, window_size=50,
                                                  start_balance=balance)

                    if total_balance > best_total_balance:
                        best_total_balance = total_balance
                        best_short_ema_length = short_ema_length
                        best_long_ema_length = long_ema_length
                        best_stop_loss = stop_loss / 1000
                        best_total_profit = best_total_balance - balance
                        current_files_path = file_path
                        print(f'Nowa lepsza strategia:')
                        print(f'Short EMA Length: {best_short_ema_length}')
                        print(f'Long EMA Length: {best_long_ema_length}')
                        print(f'Stop Loss: {best_stop_loss}')
                        print(f'Total Balance: {best_total_balance}')
                        print(f'Total Profit: {best_total_profit}')
                        print(f'f Execution transactions: {bought_count} : {sold_count}')
                        print(f'File Path: {current_files_path}')
            print(f'EMA Short: {short_ema_length}')

        with open('wyniki.txt', 'a') as file:
            file.write(f'Najlepsze parametry strategii Stoch:\n')
            file.write(f'Ema long: {best_long_ema_length}\n')
            file.write(f'Ema short: {best_short_ema_length}\n')
            file.write(f'Stop Loss: {best_stop_loss}\n')
            file.write(f'Total Balance: {best_total_balance}\n')
            file.write(f'Total Profit: {best_total_profit}\n')
            file.write(f'Percent Profit: {best_total_profit / balance * 100}%\n')
            file.write(f'f Execution transactions: {bought_count} : {sold_count}')
            file.write(f'File Path: {current_files_path}\n')

        print(f'Najlepsze parametry strategii:')
        print(f'Short EMA Length: {best_short_ema_length}')
        print(f'Long EMA Length: {best_long_ema_length}')
        print(f'Stop Loss: {best_stop_loss}')
        print(f'Total Balance: {best_total_balance}')
        print(f'Total Profit: {best_total_profit}')
        print(f'File Path: {current_files_path}')


def test_two():
    files_path = ['../data/BTC.csv']

    for file_path in files_path:
        best_stoch_d_length = 0
        best_stoch_length = 0
        best_stop_loss = 0
        best_total_balance = 0
        best_total_profit = 0
        best_overbought_threshold = 0
        best_oversold_threshold = 0
        current_files_path = ""
        for stoch_length in range(7, 20):
            for stoch_d_length in range(7, 20):
                for stop_loss in range(1, 10):
                    for overbought_threshold in range(70, 90, 5):
                        for oversold_threshold in range(10, 30, 5):
                            total_balance, \
                                bought_count, \
                                sold_count = run_test_two(file_path, stoch_length=stoch_length,
                                                          stoch_d_length=stoch_d_length,
                                                          overbought_threshold=overbought_threshold,
                                                          oversold_threshold=overbought_threshold,
                                                          stop_loss=stop_loss / 1000,
                                                          window_size=50,
                                                          start_balance=balance)

                            if total_balance > best_total_balance:
                                best_total_balance = total_balance
                                best_stoch_length = stoch_length
                                best_stoch_d_length = stoch_d_length
                                best_stop_loss = stop_loss / 1000
                                best_total_profit = best_total_balance - balance
                                current_files_path = file_path
                                best_oversold_threshold = oversold_threshold
                                best_overbought_threshold = overbought_threshold
                                print(f'Najlepsze parametry strategii Stoch:')
                                print(f'Stoch: {best_stoch_length}')
                                print(f'd_stoch: {best_stoch_d_length}')
                                print(f'Stop Loss: {best_stop_loss}')
                                print(f'Overbought Threshold: {best_overbought_threshold}')
                                print(f'Oversold Threshold: {best_oversold_threshold}')
                                print(f'Total Balance: {best_total_balance}')
                                print(f'Total Profit: {best_total_profit}')
                                print(f'Percent Profit: {best_total_profit / balance * 100}%')
                                print(f'f Execution transactions: {bought_count} : {sold_count}')
                                print(f'File Path: {current_files_path}')
            print(f'Stoch:  {stoch_length}')

        with open('wyniki.txt', 'a') as file:
            file.write(f'Najlepsze parametry strategii Stoch:\n')
            file.write(f'Stoch: {best_stoch_length}\n')
            file.write(f'd_stoch: {best_stoch_d_length}\n')
            file.write(f'Stop Loss: {best_stop_loss}\n')
            file.write(f'Overbought Threshold: {best_overbought_threshold}\n')
            file.write(f'Oversold Threshold: {best_oversold_threshold}\n')
            file.write(f'Total Balance: {best_total_balance}\n')
            file.write(f'Total Profit: {best_total_profit}\n')
            file.write(f'Percent Profit: {best_total_profit / balance * 100}%\n')
            file.write(f'File Path: {current_files_path}\n')


def test_one_statistic():
    files_path = ['../data/BTC.csv']

    for file_path in files_path:
        total_balance, bought_count, sold_count = run_test_one(file_path, short_ema_length=17,
                                                               long_ema_length=25,
                                                               stop_loss=0.001, window_size=50, start_balance=balance)

        print(f'Total Balance: {total_balance}')
        print(f'Percent Profit: {(total_balance - balance) / balance * 100}%')
        print(f'Executed trades: {bought_count} bought, {sold_count} sold')


def test_two_statistic():
    files_path = ['../test_data/ATAI-Dev.BTC.MIN1_new_week.csv',
                  '../test_data/ATAI-Dev.ETH.MIN1_new_week.csv', ]

    for file_path in files_path:
        total_balance, bought_count, sold_count = run_test_two(file_path, stoch_length=12,
                                                               stoch_d_length=7,
                                                               overbought_threshold=80,
                                                               oversold_threshold=10,
                                                               stop_loss=0.005,
                                                               window_size=50,
                                                               start_balance=balance)

        print(f'Total Balance: {total_balance}')
        print(f'Percent Profit: {(total_balance - balance) / balance * 100}%')
        print(f'Executed trades: {bought_count} bought, {sold_count} sold')


def main():
    # test_one()
    # test_two()
    # test_two_statistic()
    test_one_statistic()


if __name__ == "__main__":
    main()
