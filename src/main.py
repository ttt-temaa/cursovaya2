from src.reports import spending_in_category
from src.services import local_function_services
from src.views import full_views

if __name__ == "__main__":
    time = input("Введите дату и время (формат YYYY-MM-DD HH:MM:SS (2007-12-12 14:15:56))\n")
    print(full_views(time))
    local_function_services()
    user_input = input(
        "Проанализируем траты по данной вами категории за последние три месяца? Да/Нет\n").lower()
    if user_input == "да":
        category = input("Введите категорию\n").lower()
        date = input("Введите дату (формат 12.15.2007)\n").lower()
        print(spending_in_category("../data/operations.xls", category, date))
