import os
from enum import Enum


DATA_DIR = 'data'

if not os.path.isdir(DATA_DIR):
    print('[*] Created data directory: ' + DATA_DIR)
    os.mkdir(DATA_DIR)


ROOT_URL = 'https://platform.the-brawl.eu'
API_URL = f'{ROOT_URL}/ui/api'

class Enpoints(Enum):
    RATES = f'{API_URL}/rates'


RETRIEVER_DELAY : int = 10  # [s]
