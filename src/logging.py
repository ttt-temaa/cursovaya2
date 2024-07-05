import logging


def logging_f(name: str, log_f: str) -> logging.Logger:
    """логер, записывающий результат работы функции в файл"""
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(log_f, "w")
    # Создаем handler для стандартного вывода
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # Создаем форматтера для вывода в консоль
    file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    # Добавляем handler в логгер
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger
