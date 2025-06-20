import pytest
from task_3.solution import appearance, tests
"""
1. Базовые условия
2. Все заходы вне урока
3. Присутствуют весь урок
4. До урока + первая половина, вторая половина + после урока 
5. Точка пересечения - один зашёл, второй вышел
6. Множественные интервалы
7. Нулевой интервал
8. Нет данных об интервалах
"""

# 1. Базовые тесты (из условия)
@pytest.mark.parametrize('intervals,expected_answer', [
    (tests[0]['intervals'], tests[0]['answer']),
    (tests[1]['intervals'], tests[1]['answer']),
    (tests[2]['intervals'], tests[2]['answer']),
])
def test_base_cases(intervals, expected_answer):
    assert appearance(intervals) == expected_answer

# 2. Все заходы вне урока (всё вне интервала урока)
def test_not_in_lesson():
    intervals = {
        'lesson': [10, 20],
        'pupil': [7, 9, 22, 24],
        'tutor': [8, 9, 21, 25]
    }
    assert appearance(intervals) == 0

# 3. Присутствуют весь урок (интервал в интервал)
def test_all_in_lesson():
    intervals = {
        'lesson': [10, 20],
        'pupil': [10, 20],
        'tutor': [10, 20]
    }
    assert appearance(intervals) == 10

# 4. До урока + первая половина, вторая половина + после урока (+ 5. Точка пересечения = 15)
def test_half_lesson():
    intervals = {
        'lesson': [10, 20],
        'pupil': [5, 15],
        'tutor': [15, 25]
    }
    assert appearance(intervals) == 2

# 6. Множественные интервалы
def test_multi_intervals():
    intervals = {
        'lesson': [10, 20],
        'pupil': [5, 7, 9, 12, 15, 17, 19, 25],
        'tutor': [6, 13, 14, 19, 20, 25]
    }
    assert appearance(intervals) == 4

# 7. Нулевой инетрвал
def test_zero_interval():
    intervals = {
        'lesson': [10, 20],
        'pupil': [11, 11], # zero
        'tutor': [10, 20]
    }
    assert appearance(intervals) == 0

# 8. Нет данных об интервалах
def test_none_interval():
    intervals = {
        'lesson': [10, 20],
        'pupil': [], # None
        'tutor': [10, 20]
    }
    assert appearance(intervals) == 0