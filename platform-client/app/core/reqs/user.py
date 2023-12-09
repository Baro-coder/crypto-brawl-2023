import requests

from core.models.enums import CurrencyId


# -- Get wallet data
def __get_wallet_data(url: str, id: str, cookies: dict) -> dict:
    # Perform request
    print('            [$] REQUEST (GET): ' + url, end=' | ')
    response = requests.get(
        url=url,
        cookies=cookies,
        verify=False
    )
    
    # Check response code
    if response.status_code == 200:
        print('OK')
        
        # Retrieve wallets list
        data : dict = response.json()["user"]["accounts"][0]["wallets"]
        
        # Try to find the appropriate wallet
        for wallet in data:
            if wallet["currencyId"] == id:
                return wallet
        
        else:
            # If there is no wallet with specified id
            raise Exception(f"No wallet [{id}] in wallets list")
        
    else:
        # HTTP Exception
        print('ERROR - ' + str(response.status_code))
        print(f'ERROR ({str(response.status_code)})')
        raise Exception("Error response code: " + str(response.status_code))


# -- -- Get wallet's balance
def get_wallet_ballance(url: str, wallet_id : CurrencyId, cookies : dict) -> float:
    try:
        # Get wallet data
        wallet_data : dict = __get_wallet_data(url, wallet_id.value.lower(), cookies)
    except Exception:
        raise
    else:
        # Return wallet balance
        return float(wallet_data["balance"])
    
    
# -- -- Get wallet object
def get_wallet_id(url: str, wallet_id : CurrencyId, cookies : dict) -> None:
    try:
        # Get wallet data
        wallet_data : dict = __get_wallet_data(url, wallet_id.value.lower(), cookies)
    except Exception:
        raise
    else:
        # Return wallet id
        return wallet_data["id"]