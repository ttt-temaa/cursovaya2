import json
import os.path
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.confing_logging import f_logg
from src.decorators import logging
from src.services import read_transactions_xls_file

logger = f_logg(__name__)


@logging()
def spending_in_category(transactions: list[dict], category: str, date: Optional[str] = None) -> str:
    """Функция принимает датафрейм с транзакциями, название категории и опциональную дату, и возвращает сумму трат по
    заданной категории за последние три месяца от переданной даты или текущей даты, если дата не была передана."""
    logger.info("spending_in_category")
    category = category.title()
    spending = {"Дата платежа": 0, "Категория": 0, "Сумма платежа": 0}
    if date is not None:
        format_date = datetime.strptime(f"{date}", "%d.%m.%Y")
    else:
        format_date = datetime.now()
    date_3month = format_date - timedelta(days=90)
    for transaction in transactions:
        if pd.isnull(transaction.get("Дата платежа", "")) is False and transaction.get("Категория", "") == category:
            if date_3month <= datetime.strptime(f'{transaction.get("Дата платежа", "")}', "%d.%m.%Y") <= format_date:
                spending["Дата платежа"] = transaction.get("Дата платежа")
                spending["Категория"] = transaction.get("Категория")
                spending["Сумма платежа"] = transaction.get("Сумма платежа")

    json_answer = json.dumps(spending, ensure_ascii=False)
    logger.info(f"return json\n{json_answer}\n")
    print(json_answer)
    return json_answer


operations = read_transactions_xls_file(os.path.join("..", "data", "operations.xls"))
print(spending_in_category(operations, "Каршеринг", "12.12.2021"))
