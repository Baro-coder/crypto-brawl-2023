from time import sleep

from config import DATA_DIR
from models.enums import CurrencyId
from models.schemas import Candle
from utils import get_auth_cookies, store_in_csv, get_latest_from_csv
from reqs import retrieve_candle


def _get_candle(cookies: dict, currency_id: CurrencyId, prev_candle : Candle | None) -> Candle | None:
    csv_file = f'{DATA_DIR}/{currency_id.value.upper()}.csv'
    
    try:
        candle : Candle = retrieve_candle(cookies=cookies, currency_id=currency_id)
        
        if prev_candle is None or prev_candle.time != candle.time:
            store_in_csv(csv_file, candle=candle)
        
        prev_candle = candle
        
    except Exception:
        candle = None
    
    finally:
        return candle


def main() -> None:
    # Prepare
    cookies = get_auth_cookies()
    
    candle_btc : Candle | None = get_latest_from_csv(f'{DATA_DIR}/{CurrencyId.BTC.value.upper()}.csv')
    candle_eth : Candle | None = get_latest_from_csv(f'{DATA_DIR}/{CurrencyId.ETH.value.upper()}.csv')
    
    # Retrieve
    try:
        while True:
            candle_btc = _get_candle(cookies=cookies, currency_id=CurrencyId.BTC, prev_candle=candle_btc)
            candle_eth = _get_candle(cookies=cookies, currency_id=CurrencyId.RTH, prev_candle=candle_eth)
            
            sleep(1)
            
    except KeyboardInterrupt:
        print('\n[*] Stop')


if __name__ == '__main__':
    main()
