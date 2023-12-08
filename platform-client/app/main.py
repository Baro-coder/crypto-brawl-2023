# from time import sleep

# import config
# from models.enums import CurrencyId
# from models.schemas import Candle
# from models.wallets import Wallet

# from utils import get_auth_cookies, store_in_csv, get_latest_from_csv
# from reqs import get_candle, get_wallet_ballance


# def _get_candle(cookies: dict, currency_id: CurrencyId, prev_candle : Candle | None) -> Candle | None:
#     csv_file = f'{config.DATA_DIR}/{currency_id.value.upper()}.csv'
    
#     try:
#         candle : Candle = get_candle(cookies=cookies, currency_id=currency_id)
        
#         if prev_candle is None or prev_candle.time != candle.time:
#             store_in_csv(csv_file, candle=candle)
        
#         prev_candle = candle
        
#     except Exception:
#         candle = None
    
#     finally:
#         return candle


# def main() -> None:
#     # Prepare
#     cookies = get_auth_cookies()
    
#     candle_btc : Candle | None = get_latest_from_csv(f'{config.DATA_DIR}/{CurrencyId.BTC.value.upper()}.csv')
#     candle_eth : Candle | None = get_latest_from_csv(f'{config.DATA_DIR}/{CurrencyId.ETH.value.upper()}.csv')
    
#     wallet_btc : Wallet = Wallet(CurrencyId.BTC, 
#                                  balance=get_wallet_ballance(
#                                      wallet_id=CurrencyId.BTC, cookies=cookies
#                                      )
#                                  )
#     wallet_eth : Wallet = Wallet(CurrencyId.ETH, 
#                                  balance=get_wallet_ballance(
#                                      wallet_id=CurrencyId.ETH, cookies=cookies
#                                      )
#                                  )
#     wallet_usd : Wallet = Wallet(CurrencyId.USD, 
#                                  balance=get_wallet_ballance(
#                                      wallet_id=CurrencyId.USD, cookies=cookies
#                                      )
#                                  )
    
#     # Retrieve
#     print(f'[*] Retriever delay : {config.RETRIEVER_DELAY} [s]')
#     try:
#         while True:
#             # Get candles
#             candle_btc = _get_candle(cookies=cookies, currency_id=CurrencyId.BTC, prev_candle=candle_btc)
#             candle_eth = _get_candle(cookies=cookies, currency_id=CurrencyId.ETH, prev_candle=candle_eth)
            
#             # Update wallets' values
#             if candle_btc:
#                 wallet_btc.update_value(candle_btc.close)
#             if candle_eth:
#                 wallet_eth.update_value(candle_eth.close)
            
#             # Delay
#             sleep(config.RETRIEVER_DELAY)
            
#     except KeyboardInterrupt:
#         print('\n[*] Stop')


# def test():
#     # Prepare
#     cookies = get_auth_cookies()
    
#     dollars : int = 100000
#     rate    : int = 1
    
#     import requests
#     url = 'https://platform.the-brawl.eu/ui/api/transactions'
    
#     payload = {
#         "sourceWalletId": "4311f28d-61f6-4981-ab56-67720d690bbd",
#         "destWalletId": "2faea153-91d8-4761-9f4c-af7f17b4a4d1",
#         "amountFromSourceWallet": dollars,
#         "exchangeRate": str(float(1 / rate))
#     }

#     print(f'  [-] REQ[POST] -> {url} | ', end='')    
#     response = requests.post(url=url, cookies=cookies, data=payload, verify=False)
    
#     if response.status_code == 200:
#         print('OK')
#         print(response.content)
#     else:
#         print(f'ERROR({response.status_code})')
#         print(response.content)

import sys
from core import Controller


def main() -> None:
    controller : Controller = Controller()
    try:
        controller.initialize()
        # controller.work()
    
    except KeyboardInterrupt:
        print('[*] Stop.')

if __name__ == '__main__':
    main()
