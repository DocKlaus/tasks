import pytest
from task_1.solution import sum_two, strict

# 1. Позиционные аргументы
# 1.1. Оба коррректные
def test_correct_args():
    assert sum_two(1, 2) == 3

# 1.2. Первый некорректный
def test_incorrect_first_arg():
    with pytest.raises(TypeError, match='Аргумент "a" должен быть int, текущий - float'):
        sum_two(2.5, 2)

# 1.3. Второй некорректный
def test_incorrect_second_arg():
    with pytest.raises(TypeError, match='Аргумент "a" должен быть int, текущий - str'):
        sum_two(2, '1')

# 1.4. Оба некорректны
def test_both_positional_args_incorrect():
    with pytest.raises(TypeError) as exc_info:
        sum_two("1.5", "2")  # Ошибка должна быть по первому аргументу (a)
    assert 'Аргумент "a" должен быть int, текущий - str' in str(exc_info.value)

# 2. Именованные аргументы
# 2.1. Оба корректны
def test_kwargs_correct():
    assert sum_two(a=1, b=2) == 3

# 2.2. Получено некорреткное значение
def test_kwargs_incorrect():
    with pytest.raises(TypeError, match='Аргумент "b" должен быть int, получен float'):
        sum_two(a=1, b=2.5)

# Без аннотаций — проверки типов нет
def test_no_annotations():
    @strict
    def dummy(a, b):
        return a + b
    assert dummy(1, 2) == 3



