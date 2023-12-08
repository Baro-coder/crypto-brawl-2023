from testBTC import run_test_one

balance = 1000000
def main():
    file_path1 = '../test_data/ATAI-Dev.BTC.MIN5.csv'
    print("Test for 5min from DB: ")
    run_test_one(file_path1, short_ema_length=10, long_ema_length=30, stop_loss=0.01, window_size=30, start_balance=balance)

    print("Test for 1min from platform: ")
    file_path2 = '../data/BTC.csv'
    run_test_one(file_path=file_path2, short_ema_length=5, long_ema_length=20, stop_loss=0.01, window_size=20, start_balance=balance)


if __name__ == "__main__":
    main()
