import os
import csv

from core.models.schemas import Candle

def __init_file(file_path: str) -> Candle | None:
    if not os.path.isfile(file_path):
        print(f'[*] CSV File initialized: {file_path}')
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['time', 'open', 'high', 'low', 'close'])
        
        return None
    
    else:
        last_candle : Candle | None = None
        
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)  
            for row in reader:
                if row:
                    last_candle = Candle(time=int(row[0]), open=float(row[1]), high=float(row[2]), low=float(row[3]), close=float(row[4]))
        
        return last_candle
            
        

def __write_to_file(file_path: str, candle: Candle) -> None:
    with open(file_path, mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([candle.time, candle.open, candle.high, candle.low, candle.close])
        print(f'     [+] Row added in [{file_path}] : [{candle.time}, {candle.open}, {candle.high}, {candle.low}, {candle.close}]')
        

def store_in_csv(file_path: str, candle: Candle) -> None:
    __init_file(file_path)
    __write_to_file(file_path, candle)


def get_latest_from_csv(file_path: str) -> Candle | None:
    return __init_file(file_path)