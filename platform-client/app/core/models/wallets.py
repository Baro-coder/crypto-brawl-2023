from .enums import CurrencyId

class Wallet:
    def __init__(self, id: str, currency_id: CurrencyId, value: float = 0.0) -> None:
        self.id : str = id
        self.currency_id : CurrencyId = currency_id
        self.value : float = value
        print(f'    [+] Created wallet {currency_id.value}')

    def update_value(self, new_value: float) -> None:
        if new_value:
            print(f'        [-] Wallet {self.currency_id.value} : updated value : {new_value}')
            self.value = new_value
    

class CryptoWallet(Wallet):
    def __init__(self, id: str, currency_id: CurrencyId, balance: float = 0.0, value: float = 0.0) -> None:
        super().__init__(id, currency_id, value)
        self.balance : float = balance
        
    def update_balance(self, new_balance: float) -> None:
        print(f'        [-] Wallet {self.currency_id.value} : updated balance : {new_balance}')
        self.balance = new_balance
        
    def update_value(self, new_value: float | None = None, close_price: float | None = None) -> None:
        if new_value:
            return super().update_value(new_value)
        elif close_price:
            return super().update_value(self.balance * close_price)
