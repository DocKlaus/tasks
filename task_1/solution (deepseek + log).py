import logging

# Настройка логирования (вариант deepseek)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("strict_decorator")


def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__

        logger.debug(f"Аннотации типов: {annotations}")
        # Для позиционных аргументов
        for arg_name, arg_value in zip(func.__code__.co_varnames, args):
            logger.debug(f"Позиционный аргумент: {arg_name}={arg_value}")

            if arg_name in annotations:
                expected_type = annotations[arg_name]
                logger.debug(f"Ожидаемый тип для {arg_name}: {expected_type}")

                if not isinstance(arg_value, expected_type):
                    error_msg = (
                        f'Аргумент "{arg_name}" должен быть {expected_type.__name__}, '
                        f"получен {type(arg_value).__name__}"
                    )
                    logger.error(error_msg)
                    raise TypeError(error_msg)

        # Для именованных аргументов
        for arg_name, arg_value in kwargs.items():
            logger.debug(f"Именованный аргумент: {arg_name}={arg_value}")

            if arg_name in annotations:
                expected_type = annotations[arg_name]
                logger.debug(f"Ожидаемый тип для {arg_name}: {expected_type}")

                if not isinstance(arg_value, expected_type):
                    error_msg = (
                        f'Аргумент "{arg_name}" должен быть {expected_type.__name__}, '
                        f"получен {type(arg_value).__name__}"
                    )
                    logger.error(error_msg)
                    raise TypeError(error_msg)

        logger.debug("Все проверки типов пройдены успешно")
        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


# Пример использования
if __name__ == "__main__":
    logger.info("Тест корректных аргументов")
    print(sum_two(1, 2))  # Успешный вызов

    logger.info("Тест некорректных аргументов")
    try:
        print(sum_two(1, 2.4))  # Вызовет TypeError
    except TypeError as e:
        logger.exception("Ошибка типа аргумента")
