from src.reports import spending_in_category
from src.services import local_function_services
from src.views import full_views

if __name__ == "__main__":
    time = input("Здравстуйте!\nВведите время (формат 2007-12-15 22:09:56)\n")
    print(full_views(time))
    local_function_services()
    user_input = input(
        "Хотите проанализировать ваши траты по заданной категории за последние три месяца "
        "(от переданной даты)? Да/Нет\n"
    ).lower()
    if user_input == "да":
        category = input("Введите категорию\n").lower()
        date = input("Введите дату (формат 10.08.2020)\n").lower()
        print(spending_in_category("../data/operations.xls", category, date))
