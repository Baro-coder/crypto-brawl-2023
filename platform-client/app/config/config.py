from enum import Enum


ROOT_URL = 'https://platform.the-brawl.eu'
API_URL = f'{ROOT_URL}/ui/api'

class Enpoints(Enum):
    RATES = f'{API_URL}/rates'
