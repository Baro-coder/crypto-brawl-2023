import logging
import time
from logging.handlers import RotatingFileHandler
from os import environ

import numpy as np
import requests
import json
import talib

from core.config.pasy import EMAIL, PASSWORD

API_KEY = 'AIzaSyBOEvN4OzAePlFp1fSRKWJlioA9r2WPZHw'
AUTH_URL = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword'
TRANSACTION_URL = 'https://platform.the-brawl.eu/api/transaction'
ACCOUNT_ID = 'adfe7035-f7f0-4511-ac3a-77da63b21d4b'
USD_WALLET_ID = '4311f28d-61f6-4981-ab56-67720d690bbd'
BTC_WALLET_ID = '2faea153-91d8-4761-9f4c-af7f17b4a4d1'
VALUATION_URL_BTC = f'https://platform.the-brawl.eu/api/account/{ACCOUNT_ID}/wallet/{BTC_WALLET_ID}/valuation'
VALUATION_URL_USD = f'https://platform.the-brawl.eu/api/account/{ACCOUNT_ID}/wallet/{USD_WALLET_ID}/valuation'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        RotatingFileHandler('test_log.txt', maxBytes=1000000, backupCount=3),
        logging.StreamHandler()
    ]
)

data = {
    "email": EMAIL,
    "password": PASSWORD,
    "returnSecureToken": True,
}
id_token = None

def login():
    global id_token
    res = requests.post(AUTH_URL, json=data, params={'key': API_KEY}).json()
    id_token = res['idToken']
    print(id_token)


def get_auth_cookies():
    return {
        'Authorization': f'Bearer {id_token}',
    }


def buy(amountFromSourceWallet: float, price):
    try:
        res = requests.post(TRANSACTION_URL, headers={
            'Authorization': f'Bearer {id_token}'
        }, json={
            "sourceWalletId": USD_WALLET_ID,
            "destWalletId": BTC_WALLET_ID,
            "amountFromSourceWallet": amountFromSourceWallet,
            "exchangeRate": "0",
        }, verify=False)

        if res.ok:
            logging.info(
                f"Buy: {res.json()['data'][0]['attributes']['exchangeRate']}, From: {amountFromSourceWallet}, Price: {price}")
            return True
        else:
            print(res.json())
            return False
    except Exception as e:
        logging.error(e)
        raise Exception from e


def sell(amountFromSourceWallet: float):
    try:
        res = requests.post(TRANSACTION_URL, headers=get_auth_cookies(), json={
            "sourceWalletId": BTC_WALLET_ID,
            "destWalletId": USD_WALLET_ID,
            "amountFromSourceWallet": amountFromSourceWallet,
            "exchangeRate": "0",
        }, verify=False)
        # print(res.json())
        if res.ok:
            logging.info(
                f"Sell: {res.json()['data'][0]['attributes']['exchangeRate']}, Amount: {amountFromSourceWallet}")
            return False
        else:
            print(res.json())
            return True
    except Exception as e:
        logging.error(e)
        raise Exception from e


def valuation_btc():
    try:
        res = requests.get(VALUATION_URL_BTC, headers={
            'Authorization': f'Bearer {id_token}'
        }, params={
            'limit': 1,
        }, verify=False)

        return float(res.json()[0]['balance'])

    except Exception as e:
        logging.error(e)
        raise Exception from e


def valuation_usd():
    try:
        res = requests.get(VALUATION_URL_USD, headers={
            'Authorization': f'Bearer {id_token}'
        }, params={
            'limit': 1,
        }, verify=False)
        return float(res.json()[0]['balance'])
    except Exception as e:
        logging.error(e)
        raise Exception from e


def get_last_price():
    try:
        res = requests.post(TRANSACTION_URL, headers={
            'Authorization': f'Bearer {id_token}'
        }, json={
            "sourceWalletId": BTC_WALLET_ID,
            "destWalletId": USD_WALLET_ID,
            "amountFromSourceWallet": 0,
            "exchangeRate": "0",
        }, verify=False)

        data = json.loads(res.text)
        # print(data)

        exchange_rate = data['data'][0]['attributes']['exchangeRate']
        btc_wallet = data['data'][0]['attributes']['sourceWalletBalance']
        usd_wallet = data['data'][0]['attributes']['destWalletBalance']

        return float(exchange_rate), float(btc_wallet), float(usd_wallet)
    except Exception as e:
        logging.error(e)
        raise Exception from e


def trading_bot():
    bought = False
    candles = []

    while True:
        try:
            curr_price, btc_amount, usd_amount = get_last_price()

            candles.append(curr_price)

            if len(candles) > 50:
                candles.pop(0)

            ema = talib.EMA(np.array(candles), timeperiod=10)

            print(f'Last price: {curr_price}')
            if not bought and curr_price < ema[-1]:
                bought = buy(usd_amount * 0.98, curr_price)
                print("Bought BTC " + str(bought))

            elif bought and curr_price > ema[-1]:
                bought = sell(btc_amount * 0.98)
                print("Sold BTC " + str(bought))

            last_price = curr_price
            time.sleep(1)
        except Exception as e:
            logging.error(e)
            login()


if __name__ == '__main__':
    # sell(0)
    login()

    trading_bot()
