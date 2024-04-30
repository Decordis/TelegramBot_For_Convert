import json

import requests

from info import valut

from dotenv import load_dotenv
import os
load_dotenv()

headers = {"apikey": os.getenv('API_KEY')}
class APIException(Exception):
    pass

class Conversation:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote==base:
            raise APIException(f'нет смысла проверять одинаковые валюты 😬')
        try:
            quote_ticker = valut[quote]
        except KeyError:
            raise APIException(f'Я не понял {quote}, давайте ещё раз 😅')
        try:
            base_ticker = valut[base]
        except KeyError:
            raise APIException(f'Я не понял {base}, может ещё разочек? 😅')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'А такой {amount} вообще существует?🧐')

        url = f'https://api.apilayer.com/exchangerates_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}'

        r = requests.get(url, headers=headers)
        res = json.loads(r.content)['result']

        result = round(res, 2)

        return result



