import requests
from typing import NamedTuple

from core.models.wallets import Wallet, CryptoWallet


class TransactionBuyPayload(NamedTuple):
    sourceWalletId          : str
    destWalletId            : str
    amountFromSourceWallet  : float
    exchangeRate            : str


class TransactionSellPayload(NamedTuple):
    sourceWalletId              : str
    destWalletId                : str
    amountToDestinationWallet   : float
    exchangeRate                : str


def __perform_transaction(url: str, wallet_src, wallet_dst, amount: float, cookies: dict, payload: dict) -> None:
    # Perform request
    print('            [$] REQUEST (POST): ' + url, end=' | ')
    response = requests.post(
        url=url,
        data=payload,
        cookies=cookies,
        verify=False
    )
    
    # Check response code
    if response.status_code == 200:
        print('OK')
    
    else:
        # HTTP Exception
        print('ERROR - ' + str(response.status_code))
        print(f'ERROR ({str(response.status_code)})')
        raise Exception("Error response code: " + str(response.status_code))



def buy(url: str, wallet_src: Wallet, wallet_dst: CryptoWallet, amount: float, cookies: dict) -> None:
    print(f'    [*] Operation [BUY]: Currency [{wallet_dst.currency_id.value}], Amount [{amount}]')
    
    # Payload build
    payload = TransactionBuyPayload(
        sourceWalletId          = wallet_src.id,
        destWalletId            = wallet_dst.id,
        amountFromSourceWallet  = amount,
        exchangeRate            = "0"
    )._asdict()
    
    try:
        # Perform buy transaction
        __perform_transaction(url, wallet_src, wallet_dst, amount, cookies, payload)
    except Exception:
        raise


def sell(url: str, wallet_src: CryptoWallet, wallet_dst: Wallet, amount: float, cookies: dict) -> None:
    print(f'    [*] Operation [SELL]: Currency [{wallet_dst.currency_id.value}], Amount [{amount}]')
    
    # Payload build
    payload = TransactionSellPayload(
        sourceWalletId              = wallet_src.id,
        destWalletId                = wallet_dst.id,
        amountToDestinationWallet   = amount,
        exchangeRate                = "0"
    )._asdict()
    
    try:
        # Perform sell transaction
        __perform_transaction(url, wallet_src, wallet_dst, amount, cookies, payload)
    except Exception:
        raise
