import json
import os
from datetime import datetime
from heapq import nlargest
from typing import Sequence

import pandas as pd
import requests
from dotenv import load_dotenv

from src.logging import logging_f
from src.services import read_transactions_xls_file

logger = logging_f("views", "views.log")

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_KEY_2 = os.getenv("API_KEY_2")


def full_views(time: str) -> str:
    """функция, принимающая на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS, возвращающая JSON-ответ"""
    logger.info("full_views")
    card_numbers = []
    local_cards = []
    amounts = []
    main_transactions = []
    stock_prices = []
    currency_rates = []
    currency = ["USD", "EUR"]
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    output = {
        "greeting": "",
        "cards": [],
        "top_transactions": [],
        "currency_rates": [Sequence[str]],
        "stock_prices": [],
    }

    time_format = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    morning = datetime.strptime("05:00:00", "%H:%M:%S")
    day = datetime.strptime("12:00:00", "%H:%M:%S")
    evening = datetime.strptime("18:00:00", "%H:%M:%S")
    night = datetime.strptime("23:00:00", "%H:%M:%S")
    if morning.time() <= time_format.time() < day.time():
        greet = "Доброе утро!"
    elif morning.time() <= time_format.time() < evening.time():
        greet = "Добрый день!"
    elif evening.time() <= time_format.time() < night.time():
        greet = "Добрый вечер!"
    else:
        greet = "Доброй ночи!"

    output["greeting"] = greet
    for item in currency:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{item}"
        response = requests.get(url, headers={"apikey": API_KEY})
        response_data = response.json()
        path = response_data["conversion_rates"]["RUB"]
        currency_rates.append(dict(currency=item, rate=path))
    output["currency_rates"] = currency_rates

    data = read_transactions_xls_file("../data/operations.xls")
    for transaction in data:
        if not pd.isnull(transaction.get("Номер карты")):
            card_numbers.append(dict(last_digits=transaction.get("Номер карты", "").replace("*", "")))
    for card in card_numbers:
        if card not in local_cards:
            local_cards.append(card)
    for transaction in data:
        if not pd.isnull(transaction.get("Номер карты")):
            for local in local_cards:
                if local.get("last_digits", "") in transaction.get("Номер карты", ""):
                    if pd.isnull(transaction.get("Сумма операции", "")) is False:
                        try:
                            local["total_spent"] += abs(transaction.get("Сумма операции", ""))
                            local["cashback"] += abs(transaction.get("Сумма операции", "") / 100)
                        except KeyError:
                            local["total_spent"] = abs(transaction.get("Сумма операции", ""))
                            local["cashback"] = abs(transaction.get("Сумма операции", "") / 100)
    for local in local_cards:
        local["total_spent"] = round(float(local.get("total_spent", "")), 2)
        local["cashback"] = round(float(local.get("cashback", "")), 2)
    output["cards"] = local_cards

    for transactions in data:
        amounts.append(transactions.get("Сумма операции"))
    amounts = nlargest(5, amounts)
    for transactions in data:
        for amount in amounts:
            if transactions.get("Сумма операции") == amount:
                main_transactions.append(
                    dict(
                        date=transactions.get("Дата платежа"),
                        amount=amount,
                        category=transactions.get("Категория"),
                        description=transactions.get("Описание"),
                    )
                )
                amounts.remove(amount)
    output["top_transactions"] = main_transactions

    datas = read_transactions_xls_file("../data/operations2_t_bank.xls")
    for transactions in datas:
        if not pd.isnull(transactions.get("Номер карты")):
            card_numbers.append(dict(last_digits=transactions.get("Номер карты", "").replace("*", "")))
    for card in card_numbers:
        if card not in local_cards:
            local_cards.append(card)
    for transactions in datas:
        if not pd.isnull(transactions.get("Номер карты")):
            for local in local_cards:
                if local.get("last_digits", "") in transactions.get("Номер карты", ""):
                    if pd.isnull(transactions.get("Сумма операции", "")) is False:
                        try:
                            local["total_spent"] += abs(transactions.get("Сумма операции", ""))
                            local["cashback"] += abs(transactions.get("Сумма операции", "") / 100)
                        except KeyError:
                            local["total_spent"] = abs(transactions.get("Сумма операции", ""))
                            local["cashback"] = abs(transactions.get("Сумма операции", "") / 100)
    for local in local_cards:
        local["total_spent"] = round(float(local.get("total_spent", "")), 2)
        local["cashback"] = round(float(local.get("cashback", "")), 2)
    output["cards"] = local_cards

    for transactions in datas:
        amounts.append(transactions.get("Сумма операции"))
    amounts = nlargest(5, amounts)
    for transactions in datas:
        for amount in amounts:
            if transactions.get("Сумма операции") == amount:
                main_transactions.append(
                    dict(
                        date=transactions.get("Дата платежа"),
                        amount=amount,
                        category=transactions.get("Категория"),
                        description=transactions.get("Описание"),
                    )
                )
                amounts.remove(amount)
    output["top_transactions"] = main_transactions

    url_2 = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY_2}"
    response_2 = requests.get(url_2, headers={"apikey": API_KEY_2})
    response_data_2 = response_2.json()
    for share in response_data_2:
        for stock in stocks:
            if share.get("symbol", "") == stock:
                stock_prices.append(dict(stock=stock, price=share.get("price", "")))
    output["stock_prices"] = stock_prices

    json_data = json.dumps(output, ensure_ascii=False, indent=4)
    logger.info(f"full_views\n{json_data}\n")

    with open("user_settings.json", "w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=4)

    return json_data
