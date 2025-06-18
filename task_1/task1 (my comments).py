"""Необходимо реализовать декоратор @strict
Декоратор проверяет соответствие типов переданных в вызов функции аргументов типам аргументов, объявленным в прототипе функции.
(подсказка: аннотации типов аргументов можно получить из атрибута объекта функции func.__annotations__ или с помощью модуля inspect)
При несоответствии типов бросать исключение TypeError
Гарантируется, что параметры в декорируемых функциях будут следующих типов: bool, int, float, str
Гарантируется, что в декорируемых функциях не будет значений параметров, заданных по умолчанию
"""


def strict(func):
    def candy_wrapper(*args, **kwargs):
        annotations = func.__annotations__

        print(f"Аннотация типов [annotations = {annotations}]")

        # Для позиционных аргументов
        for argument_name, argument_value in zip(func.__code__.co_varnames, args):

            print(
                f"\tКортеж имён локальных переменных (+арг) [func.__code__.co_varnames = {func.__code__.co_varnames}]"
            )
            print(f"\tПереданные позиционные аргументы [args = {args}]")
            print(
                f"\tТекущая итерация [argument_name = {argument_name}], [argument_value = {argument_value}]"
            )

            if argument_name in annotations:
                exp_type = annotations[argument_name]

                print(
                    f'\t\tТип для текущего аргумента "{argument_name}" [exp_type = {exp_type}]'
                )
                print(
                    f"\t\tТекущий переданный позиционный аргумент [argument_value = {argument_value}] относится к типу [exp_type = {exp_type}] -> {isinstance(argument_value, exp_type)}"
                )

                if not isinstance(argument_value, exp_type):
                    raise TypeError(
                        f'Аргумент "{argument_name}" должен быть {exp_type.__name__}, '
                        f"текущий: {type(argument_value).__name__}"
                    )

        # Для именованных аргументов
        for argument_name, argument_value in kwargs.items():

            print(f"\tСловарь именованных аргументов [kwargs = {kwargs}]")
            print(
                f"\tТекущая итерация [argument_name = {argument_name}, argument_value = {argument_value}]"
            )

            if argument_name in annotations:
                exp_type = annotations[argument_name]

                print(
                    f'\t\tТип для текущего аргумента "{argument_name}"  [exp_type = {exp_type}]'
                )
                print(
                    f"\t\tТекущий переданный позиционный аргумент [argument_value = {argument_value}] относится к типу [exp_type = {exp_type}] -> {isinstance(argument_value, exp_type)}"
                )

                if not isinstance(argument_value, exp_type):
                    raise TypeError(
                        f"Аргумент '{argument_name}' должен быть {exp_type.__name__}, "
                        f"текущий: {type(argument_value).__name__}"
                    )

        # вызов исходной функции
        return func(*args, **kwargs)

    return candy_wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
