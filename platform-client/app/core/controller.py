from time import sleep

from .config import settings
from .models.enums import CurrencyId, Signal
from .models.wallets import Wallet, CryptoWallet
from .models.schemas import Candle
from .strategies import TradingStrategyOne


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
        
        # Strategies
        # -- BTC
        self._btc_strategy : TradingStrategyOne = TradingStrategyOne(
            short_ema_length=10, 
            long_ema_length=30, 
            stop_loss=0.01, 
            window_size=self._settings.btc_window_size,
            data_csv_file=self._settings.data_btc_csv_file
            )
        
        # -- ETH
        self._eth_strategy : TradingStrategyOne = TradingStrategyOne(
            short_ema_length=10, 
            long_ema_length=30, 
            stop_loss=0.01, 
            window_size=self._settings.eth_window_size,
            data_csv_file=self._settings.data_eth_csv_file
            )
        
    
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
        print('    [*] Candles init...')
        while len(self._btc_strategy.candles) <= self._btc_strategy.window_size and len(self._eth_strategy.candles) <= self._eth_strategy.window_size:
            # -- -- BTC
            self._btc_strategy.update_candle(
                get_candle(
                    url=self._settings.endpoints['rates'],
                    currency_id=self._wallet_btc.currency_id,
                    cookies=self._cookies
                )
            )
            
            # -- -- ETH
            self._eth_strategy.update_candle(
                get_candle(
                    url=self._settings.endpoints["rates"],
                    currency_id=self._wallet_eth.currency_id,
                    cookies=self._cookies
                )
            )
            
            # Delay
            sleep(self._settings.refresh_delay)
        
    
    def work(self) -> None:
        print('[*] Controller works...')
        
        # Loop
        while True:
            try:
                # -- Strategy update
                print('    [*] Strategies update...')
                
                # -- -- BTC
                self._btc_strategy.update_candle(
                    get_candle(
                        url=self._settings.endpoints['rates'],
                        currency_id=self._wallet_btc.currency_id,
                        cookies=self._cookies
                    )
                )
                
                # -- -- ETH
                self._eth_strategy.update_candle(
                    get_candle(
                        url=self._settings.endpoints["rates"],
                        currency_id=self._wallet_eth.currency_id,
                        cookies=self._cookies
                    )
                )
            
            except Exception:
                pass
            
            else:
                # -- Strategy generate signals
                print('    [*] Strategies signals generate...')
                
                signal_btc : Signal = self._btc_strategy.generate_signal()
                signal_eth : Signal = self._eth_strategy.generate_signal()

                # -- Interpret signal
                # -- -- BTC
                match(signal_btc):
                    case Signal.BUY:
                        buy(
                            url=self._settings.endpoints['trade'],
                            wallet_src=self._wallet_usd,
                            wallet_dst=self._wallet_btc,
                            amount=self._wallet_usd.value * 0.95,
                            cookies=self._cookies
                        )
                    
                    case Signal.SELL:
                        sell(
                            url=self._settings.endpoints['trade'],
                            wallet_src=self._wallet_btc,
                            wallet_dst=self._wallet_usd,
                            amount=self._wallet_btc.value * 0.95,
                            cookies=self._cookies
                        )
                    
                    case Signal.HOLD:
                        # -- -- ETH
                        match(signal_eth):
                            case Signal.BUY:
                                buy(
                                    url=self._settings.endpoints['trade'],
                                    wallet_src=self._wallet_usd,
                                    wallet_dst=self._wallet_eth,
                                    amount=self._wallet_usd.value * 0.95
                                )
                            
                            case Signal.SELL:
                                sell(
                                    url=self._settings.endpoints['trade'],
                                    wallet_src=self._wallet_btc,
                                    wallet_dst=self._wallet_usd,
                                    amount=self._wallet_btc.value * 0.95,
                                    cookies=self._cookies
                                )
                            
                            case Signal.HOLD:
                                pass
                
                # -- Update wallets balances and values
                # -- -- USD
                self._wallet_usd.update_value(get_wallet_ballance(
                    url=self._settings.endpoints['user'],
                    wallet_id=self._wallet_usd.currency_id,
                    cookies=self._cookies
                ))
                
                # -- -- BTC
                self._wallet_btc.update_balance(
                    get_wallet_ballance(
                        url=self._settings.endpoints['user'],
                        wallet_id=self._wallet_btc.currency_id,
                        cookies=self._cookies
                    )
                )
                self._wallet_btc.update_value(
                    close_price=self._btc_strategy.candles[-1]
                )
                
                # -- -- ETH
                self._wallet_eth.update_balance(
                    get_wallet_ballance(
                        url=self._settings.endpoints['user'],
                        wallet_id=self._wallet_eth.currency_id,
                        cookies=self._cookies
                    )
                )
                self._wallet_eth.update_value(
                    close_price=self._eth_strategy.candles[-1]
                )
                
                            
            finally:
                sleep(self._settings.refresh_delay)
