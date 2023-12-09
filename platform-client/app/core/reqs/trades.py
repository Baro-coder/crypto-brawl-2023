import requests
from typing import NamedTuple

from core.models.wallets import Wallet, CryptoWallet


class TransactionPayload(NamedTuple):
    sourceWalletId          : str
    destWalletId            : str
    amountFromSourceWallet  : float
    exchangeRate            : str


def __perform_transaction(url: str, wallet_src: Wallet, wallet_dst: Wallet, amount: float, cookies: dict) -> None:
    # Payload build
    payload = TransactionPayload(
        sourceWalletId          = wallet_src.id,
        destWalletId            = wallet_dst.id,
        amountFromSourceWallet  = amount,
        exchangeRate            = "0"
    )
    
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
    try:
        # Perform buy transaction
        __perform_transaction(url, wallet_src, wallet_dst, amount, cookies)
    except Exception:
        raise


def sell(url: str, wallet_src: CryptoWallet, wallet_dst: Wallet, amount: float, cookies: dict) -> None:
    try:
        # Perform sell transaction
        __perform_transaction(url, wallet_src, wallet_dst, amount, cookies)
    except Exception:
        raise
