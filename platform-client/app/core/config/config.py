import os


class Settings:        
    def __init__(self, 
                 data_dir: str,
                 root_url: str,
                 api_url_sufix: str,
                 refresh_delay: int) -> None:
        
        print('[*] Setting up the configuration...')
        # Urls
        self._root_url : str = root_url
        self._api_url  : str = f'{root_url}/{api_url_sufix}'
        self.endpoints : dict = {
            "rates" : f'{self._api_url}/rates',
            "user"  : f'{self._api_url}/user',
            "trade" : f'{self._api_url}/transactions'
        }
        print('    [-] Root URL: ' + self._root_url)
        print('    [-] API  URL: ' + self._api_url)
        print('    [-] Endpoints: ')
        for key, endpoint in self.endpoints.items():
            print(f'       - {key}  : {endpoint}')
        
        # Directories
        self.data_dir : str = data_dir
        if not os.path.isdir(data_dir):
            print(f'    [!] Data directory [{data_dir}] does not exists! Creating...')
            os.mkdir(data_dir)
        print('    [-] Data directory: ' + self.data_dir)
        
        self.data_btc_csv_file : str = f'{data_dir}/BTC.csv'
        print('       - BTC data : ' + self.data_btc_csv_file)
        self.data_eth_csv_file : str = f'{data_dir}/ETH.csv'
        print('       - ETH data : ' + self.data_eth_csv_file)
        
        # Refresh rate [s]
        self.refresh_delay : int = refresh_delay
        print(f'    [-] Refresh delay: {refresh_delay}[s]')
        
        
settings = Settings(
    data_dir='data',
    root_url='https://platform.the-brawl.eu',
    api_url_sufix='ui/api',
    refresh_delay=10,
)
