import json

import pandas as pd

from src.logging import logging_f

logger = logging_f("services", "services.log")


def read_transactions_xls_file(xls_file: str) -> list[dict]:
    """считывание операций с XLS файла и возвращение DataFrame"""
    reader = pd.read_excel(xls_file)
    data = reader.to_dict(orient="records")
    return data


def simple_search(user_request: str) -> str:
    """возвращение JSON со всеми транзакциями, содержащие запросы пользователя"""
    logger.info("user_request")
    datat = read_transactions_xls_file("../data/operations.xls")
    data = []
    for transaction in datat:
        if (user_request.lower() in (transaction.get("Описание", "")).lower()) or user_request.lower() in (
                str(transaction.get("Категория", ""))
        ).lower():
            data.append(transaction)
        for key, value in transaction.items():
            if pd.isnull(value):
                transaction[key] = None
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    logger.info(f"{json_data}\n")
    return json_data


def simple_search_local(user_request: str) -> str:
    """возвращение JSON со всеми транзакциями, содержащие запросы пользователя"""
    logger.info("start simple_search")
    python_data = read_transactions_xls_file("../data/operations2_t_bank.xls")
    data = []
    for transaction in python_data:
        if (user_request.lower() in (transaction.get("Описание", "")).lower()) or user_request.lower() in (
                str(transaction.get("Категория", ""))
        ).lower():
            data.append(transaction)
        for key, value in transaction.items():
            if pd.isnull(value):
                transaction[key] = None
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    logger.info(f"{json_data}\n")
    return json_data


def main_function_services_local() -> None:
    """Итоги модуля"""
    user_input = input("Отфильтровать транзакции по слову? Да/Нет\n").lower()
    if user_input == "да":
        user_request = input().lower()
        print(simple_search(user_request))
        print(simple_search_local(user_request))
