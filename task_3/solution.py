"""
1. Делаем из интервалов пары (для ученика и учителя)
2. Объединяем пересекающиеся
3. Фильтруем, если выходит за пределы урока
"""


def appearance(intervals: dict[str, list[int]]) -> int:
    # В функцию передаётся только один тект [inter: {less:[...], pupil:[...], tutor:[...]}]
    # Разбиваем интервал урока на переменные
    less_start, less_end = intervals["lesson"]
    # print(f'less_start: {less_start}, less_end: {less_end}')

    # Функция принимает по-очереди учителя и ученика
    # Обрезает начало и конец интервала, если они не вписываются в урок

    def trim_by_lesson(local_intervals: list[int]):
        list_for_pairs = []
        for i in range(0, len(local_intervals), 2):
            start = local_intervals[i]
            end = local_intervals[i + 1]

            # Обрезаем по началу урока
            start = max(start, less_start)

            # Обрезаем по окончанию урока
            end = min(end, less_end)

            # Сравниваем начало с концом.
            # Конец будет раньше, чем начало после обрезки, если ученик/учитель зашёл и вышел раньше начала урока или позже окончания урока
            if start < end:
                list_for_pairs.append((start, end))
            list_for_pairs.sort()

        return list_for_pairs


    def merged(list_for_pairs):
        # Между интервалами есть пересечения. Объединяем
        list_merged_intervals = []
        for cur_interval in list_for_pairs:

            # Первый сразу добавляем
            if not list_merged_intervals:
                list_merged_intervals.append(cur_interval)

            else:
                # Последний интервал - последний в списке объединённых
                last_interval = list_merged_intervals[-1]
                # Если начало текущего не объединённого интервала меньше или равно окончания последнего объединённого интервала, значит есть пересечение
                if cur_interval[0] <= last_interval[1]:
                    new_interval = (last_interval[0], max(last_interval[1], cur_interval[1]))
                    # Заменяем последний интервал в листе на новый объединённый
                    list_merged_intervals[-1] = new_interval
                else:
                    # Если не пересекается, то просто добавляем
                    list_merged_intervals.append(cur_interval)

        return list_merged_intervals


    pupil_trim_intervals = trim_by_lesson(intervals["pupil"])
    # print(f'pupil_trim_intervals: {pupil_trim_intervals}')
    pupil_merged_intervals = merged(pupil_trim_intervals)
    # print(f'pupil_merged_intervals: {pupil_merged_intervals}')

    tutor_trim_intervals = trim_by_lesson(intervals["tutor"])
    # print(f'tutor_trim_intervals: {tutor_trim_intervals}')
    tutor_merged_intervals = merged(tutor_trim_intervals)
    # print(f'tutor_merged_intervals: {tutor_merged_intervals}')

    # Объединяем учителя и ученика
    result_time = 0
    p = t = 0

    while p < len(pupil_merged_intervals) and t < len(tutor_merged_intervals):
        pupil_start, pupil_end = pupil_merged_intervals[p]
        tutor_start, tutor_end = tutor_merged_intervals[t]

        common_start = max(pupil_start, tutor_start)
        common_end = min(pupil_end, tutor_end)

        # False будет если интервалы не пересекаются(например: ученик зашёл и вышел, а учитель все это время не заходил)
        if common_start < common_end:
            # Если пересекаются, то в общее время добавляем время интервала
            result_time += common_end - common_start

        # Тикаем счётчики
        if pupil_end < tutor_end:
            p += 1
        else:
            t += 1

    return result_time




tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       print(f'test_answer: {test_answer}')
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
