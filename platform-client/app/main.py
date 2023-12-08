from models.enums import CurrencyId, Type
from utils import get_auth_cookies
from reqs import retrieve_data


def main() -> None:
    # Prepare
    cookies = get_auth_cookies()
    
    # Retrieve
    retrieve_data(
        currency_id=CurrencyId.BTC, 
        cookies=cookies
        )


if __name__ == '__main__':
    main()