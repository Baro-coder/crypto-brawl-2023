from time import sleep

from .config import settings
from .strategies import TradingStrategyOne
from .models.enums import CurrencyId, Signal
from .models.wallets import Wallet, CryptoWallet

from .utils import get_auth_cookies, read_candles_from_csv
from .reqs import get_wallet_id, get_wallet_ballance, get_candle, buy, sell


class Controller:
    def __init__(self, load_strategies_data_from_files : bool = False) -> None:
        # Config
        self._settings = settings
        
        # Wallets
        self._wallet_usd : Wallet
        self._wallet_btc : CryptoWallet
        self._wallet_eth : CryptoWallet
        
        # Auth Cookies
        self._cookies : dict = get_auth_cookies()
        
        # Strategies
        self._load_strategies_data_from_files = load_strategies_data_from_files
        # -- BTC
        self._btc_strategy : TradingStrategyOne = TradingStrategyOne(
            short_ema_length=10, 
            long_ema_length=30, 
            stop_loss=0.01, 
            window_size=50,
            data_csv_file=self._settings.data_btc_csv_file
            )
        print(self._btc_strategy)
        
        # -- ETH
        self._eth_strategy : TradingStrategyOne = TradingStrategyOne(
            short_ema_length=10, 
            long_ema_length=30, 
            stop_loss=0.01, 
            window_size=50,
            data_csv_file=self._settings.data_eth_csv_file
            )
        print(self._eth_strategy)
        
        
    
    # Public methods
    # -- initialize
    def initialize(self) -> None:
        print('[*] Controller initializing...')
        self.__init_wallets()
        
        if self._load_strategies_data_from_files:
            self.__init_candles_from_files()
            if len(self._btc_strategy.candles) <= self._btc_strategy.window_size and len(self._eth_strategy.candles) <= self._eth_strategy.window_size:
                self.__init_candles()
        else:
            self.__init_candles()
        
    # -- work
    def work(self) -> None:
        print('[*] Controller works...')
        
        
        # Loop
        while True:
            # -- Update candles
            try:
                self.__strategy_update()
            except Exception as why:
                # TODO: Auth cookies retrieve function
                print(f'[!] Error: {why}')
                continue
                
            # -- Generate signals
            signal_btc, signal_eth = self.__generate_signals()
            
            
            # -- Interpret signal
            self.__interpret_signals(signal_btc=signal_btc, signal_eth=signal_eth)
            
            # -- Wallets update
            self.__wallets_update()
            
            # -- Delay
            sleep(self._settings.refresh_delay)


    # Private methods
    # -- initialize
    def __init_wallets(self) -> None:
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
    
    
    def __init_candles(self) -> None:
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
    
    
    def __init_candles_from_files(self) -> None:
        print('    [*] Candles loading from files...')
        
        # -- BTC
        print(f'        [-] Reading file: {self._btc_strategy.data_csv_file} ...')
        candles = read_candles_from_csv(
            file_path=self._btc_strategy.data_csv_file
        )
        self._btc_strategy.candles = candles
        print('             - Loaded candles: ' + str(len(candles)))
        
        # -- ETH
        print(f'        [-] Reading file: {self._eth_strategy.data_csv_file} ...')
        candles = read_candles_from_csv(
            file_path=self._eth_strategy.data_csv_file
        )
        self._eth_strategy.candles = candles
        print('             - Loaded candles: ' + str(len(candles)))
        

    # -- work
    def __strategy_update(self) -> None:
        try:
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
    
    
    def __generate_signals(self):
        print('    [*] Strategies signals generate...')
        
        try:
            signal_btc : Signal = self._btc_strategy.generate_signal()
            signal_eth : Signal = self._eth_strategy.generate_signal()
    
        except Exception:
            signal_btc : Signal = Signal.HOLD
            signal_eth : Signal = Signal.HOLD
    
        finally:
            print('        [-] Signal BTC : ' + signal_btc.name)
            print('        [-] Signal ETH : ' + signal_eth.name)
            return ((signal_btc, signal_eth))


    def __interpret_signals(self, signal_btc : Signal, signal_eth : Signal) -> None:
        # -- -- BTC
        try:
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
                                amount=self._wallet_usd.value * 0.95,
                                cookies=self._cookies
                            )

                        case Signal.SELL:
                            sell(
                                url=self._settings.endpoints['trade'],
                                wallet_src=self._wallet_eth,
                                wallet_dst=self._wallet_usd,
                                amount=self._wallet_eth.value * 0.95,
                                cookies=self._cookies
                            )

                        case Signal.HOLD:
                            pass
                        
        except Exception as why:
            print(f'[!] Error: {why}')


    def __wallets_update(self) -> None:
        print('    [*] Wallets update...')
        
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
            close_price=self._btc_strategy.candles[-1].close
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
            close_price=self._eth_strategy.candles[-1].close
        )
