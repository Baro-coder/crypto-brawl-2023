from time import sleep

from .config import settings
from .models.enums import CurrencyId, Signal
from .models.wallets import Wallet, CryptoWallet
from .models.schemas import Candle

from .utils import get_auth_cookies
from .reqs import get_wallet_id, get_wallet_ballance, get_candle, buy, sell


class Controller:
    def __init__(self) -> None:
        # Config
        self._settings = settings
        
        # Wallets
        self._wallet_usd : Wallet
        self._wallet_btc : CryptoWallet
        self._wallet_eth : CryptoWallet
        
        # Auth Cookies
        self._cookies : dict = get_auth_cookies()
        
    
    def initialize(self) -> None:
        print('[*] Controller initializing...')
        
        # Wallets init
        print('    [*] Wallets init...')
        # -- USD
        self._wallet_usd = Wallet(
            id=get_wallet_id(self._settings.endpoints['user'], CurrencyId.USD, cookies=self._cookies),
            currency_id=CurrencyId.USD,
            value=get_wallet_ballance(self._settings.endpoints['user'], CurrencyId.USD, cookies=self._cookies)
        )
        
        # -- BTC
        self._wallet_btc = CryptoWallet(
            id=get_wallet_id(self._settings.endpoints['user'], CurrencyId.BTC, cookies=self._cookies),
            currency_id=CurrencyId.BTC,
            balance=get_wallet_ballance(self._settings.endpoints['user'], CurrencyId.BTC, cookies=self._cookies)
        )
        
        # -- ETH
        self._wallet_eth = CryptoWallet(
            id=get_wallet_id(self._settings.endpoints['user'], CurrencyId.ETH, cookies=self._cookies),
            currency_id=CurrencyId.ETH,
            balance=get_wallet_ballance(self._settings.endpoints['user'], CurrencyId.ETH, cookies=self._cookies)
        )
        
        # Candles init
        # TODO
        
    
    def work(self) -> None:
        print('[*] Controller works...')
        
        # Loop
        while True:
            # -- Strategy update
            # TODO: Strategy update func

            # -- Strategy generate signals
            # TODO: Strategy generate func
            signal : Signal = Signal.HOLD

            # -- perform transaction
            match(signal):
                case Signal.BUY:
                    pass
                
                case Signal.SELL:
                    pass
                
                case Signal.HOLD:
                    pass
                
                case _:
                    pass
            
            sleep(self._settings.refresh_delay)
