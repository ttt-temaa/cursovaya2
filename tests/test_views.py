import json
from unittest.mock import Mock, patch

from pandas import DataFrame

from src.views import full_views


@patch("pandas.read_excel")
def test_full_views(mock_reader: Mock) -> None:
    mock_reader.return_value = DataFrame(
        [
            {
                "Дата операции": "31.01.2019 13:34:15",
                "Дата платежа": "30.01.2019",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -35.0,
                "Валюта операции": "RUB",
                "Сумма платежа": -35.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Мобильная связь",
                "MCC": "",
                "Описание": "Teletie Бизнес +7 966 000-00-00",
                "Бонусы (включая кэшбэк)": 0,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 35.0,
            },
            {
                "Дата операции": "30.01.2019 20:34:24",
                "Дата платежа": "30.01.2019",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -97.8,
                "Валюта операции": "RUB",
                "Сумма платежа": -97.8,
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Супермаркеты",
                "MCC": 5411.0,
                "Описание": "SPAR",
                "Бонусы (включая кэшбэк)": 1,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 97.8,
            },
            {
                "Дата операции": "30.01.2019 20:34:24",
                "Дата платежа": "30.01.2019",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -197.8,
                "Валюта операции": "RUB",
                "Сумма платежа": -197.8,
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Фастфуд",
                "MCC": 5411.0,
                "Описание": "Rumyanyj Khleb",
                "Бонусы (включая кэшбэк)": 1,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 197.8,
            },
            {
                "Дата операции": "30.01.2019 20:34:24",
                "Дата платежа": "30.01.2019",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -977.51,
                "Валюта операции": "RUB",
                "Сумма платежа": -977.51,
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Каршеринг",
                "MCC": 5411.0,
                "Описание": "Ситидрайв",
                "Бонусы (включая кэшбэк)": 1,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": -977.51,
            },
            {
                "Дата операции": "30.01.2019 20:34:24",
                "Дата платежа": "30.01.2019",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -1000.8,
                "Валюта операции": "RUB",
                "Сумма платежа": -1000.8,
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Топливо",
                "MCC": 5411.0,
                "Описание": "ЛУКОЙЛ",
                "Бонусы (включая кэшбэк)": 1,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 1000.8,
            },
        ]
    )
    assert (full_views("2020-12-12 05:59:59")[0:1000]) == (
        json.dumps(
            {
                "greeting": "Доброе утро!",
                "cards": [{"last_digits": "7197", "total_spent": 2308.91, "cashback": 23.09}],
                "top_transactions": [
                    {
                        "date": "30.01.2019",
                        "amount": -35.0,
                        "category": "Мобильная связь",
                        "description": "Teletie Бизнес +7 966 000-00-00",
                    },
                    {"date": "30.01.2019", "amount": -97.8, "category": "Супермаркеты", "description": "SPAR"},
                    {"date": "30.01.2019", "amount": -197.8, "category": "Фастфуд", "description": "Rumyanyj Khleb"},
                    {"date": "30.01.2019", "amount": -977.51, "category": "Каршеринг", "description": "Ситидрайв"},
                    {"date": "30.01.2019", "amount": -1000.8, "category": "Топливо", "description": "ЛУКОЙЛ"},
                ],
                "currency_rates": [{"currency": "USD", "rate": 85.6933}, {"currency": "EUR", "rate": 91.9092}],
                "stock_prices": [
                    {"stock": "TSLA", "price": 210.975},
                    {"stock": "AAPL", "price": 215.7334},
                    {"stock": "AMZN", "price": 197.2132},
                    {"stock": "MSFT", "price": 453.755},
                    {"stock": "GOOGL", "price": 182.68},
                ],
            },
            ensure_ascii=False,
            indent=4,
        )[0:1000]
    )