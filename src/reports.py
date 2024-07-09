from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.decorators import logging
from src.logging import logging_f
from src.services import read_transactions_xls_file

logger = logging_f("reports", "reports.log")


@logging()
def spending_in_category(transactions: str, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция принимает датафрейм с транзакциями, название категории и опциональную дату, и возвращает сумму трат по
    заданной категории за последние три месяца от переданной даты или текущей даты, если дата не была передана."""
    logger.info("spending_in_category")
    category = category.title()
    spending = []
    if date is not None:
        format_date = datetime.strptime(f"{date}", "%d.%m.%Y")
    else:
        format_date = datetime.now()
    date_3month = format_date - timedelta(days=90)
    data = read_transactions_xls_file(transactions)
    for transaction in data:
        if pd.isnull(transaction.get("Дата платежа", "")) is False and transaction.get("Категория", "") == category:
            if date_3month <= datetime.strptime(f'{transaction.get("Дата платежа", "")}', "%d.%m.%Y") <= format_date:
                spending.append(
                    {
                        "Дата платежа": transaction.get("Дата платежа", ""),
                        "Категория": transaction.get("Категория", ""),
                        "Сумма платежа": transaction.get("Сумма платежа", ""),
                    }
                )

    df = pd.DataFrame(list(spending), columns=["Дата платежа", "Категория", "Сумма платежа"])
    logger.info(f"return df\n{df}\n")
    return df
