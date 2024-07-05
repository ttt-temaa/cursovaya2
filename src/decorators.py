from typing import Any, Callable


def logging(filename: str = "decorators") -> Callable:
    """декоратор, логирущий вызов функции"""

    def decorators(function: Callable[[Any], Any]) -> Callable[[Any], Callable]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with open(filename, "a", encoding="utf-8") as f:
                try:
                    werty = function(*args, **kwargs)
                    data = werty.to_dict(orient="list")
                    f.write(f"{str(data)}\n")
                except Exception as e:
                    f.write(f"{function.__name__} error: {e}\n")
                else:
                    f.write(f"{function.__name__} ok\n")
                    return werty

        return wrapper

    return decorators
