import requests
import json
from config import keys


class ConverterException(Exception):
    pass


class Converter:
    @staticmethod
    def calculate_rate(message):
        data = message.text.split()

        if len(data) != 3:
            raise ConverterException('Ошибка ввода данных.')
        else:
            base, quote, amount = data
            base = base.lower()
            quote = quote.lower()
        try:
            amount = float(amount)

        except ValueError:
            raise ConverterException('Ошибка ввода. Сумма должна быть числом.')
        else:
            if amount < 0:
                raise ConverterException('Ошибка ввода данных. Сумма должна быть положительной.')

        if base == quote:
            raise ConverterException(f'Указана одинаковая валюта для пересчета - {base}')
        if base not in keys.keys():
            raise ConverterException(f'Неправильно указано название валюты - {base}')
        if quote not in keys.keys():
            raise ConverterException(f'Неправильно указано название валюты - {quote}')

        path = f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}'
        r = requests.get(path).content
        result = json.loads(r)
        final_sum = amount * result[keys[quote]]
        return f'{base} в сумме {amount:.2f} = {quote} в сумме {final_sum:.2f}'
