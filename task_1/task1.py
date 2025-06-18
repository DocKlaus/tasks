def strict(func):
    def candy_wrapper(*args, **kwargs):
        annotations = func.__annotations__

        for argument_name, argument_value in zip(func.__code__.co_varnames, args):
            if argument_name in annotations:
                exp_type = annotations[argument_name]
                if not isinstance(argument_value, exp_type):
                    raise TypeError(
                        f'Аргумент "{argument_name}" должен быть {exp_type.__name__}, '
                        f"текущий: {type(argument_value).__name__}"
                    )

        for argument_name, argument_value in kwargs.items():
            if argument_name in annotations:
                exp_type = annotations[argument_name]
                if not isinstance(argument_value, exp_type):
                    raise TypeError(
                        f"Аргумент '{argument_name}' должен быть {exp_type.__name__}, "
                        f"текущий: {type(argument_value).__name__}"
                    )

        return func(*args, **kwargs)

    return candy_wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
