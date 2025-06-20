"""
Первичный анализ логических конструкций, требующих оптимизации используемой памяти и времени

Основные этапы
1. Получить ответ по текущей странице
2. Получить суп
3. Найти все блоки с буквами ("А", "Б", ...) на странице -> цикл по блокам
4. В блоке с буквой посчитать все теги li
5. Вносить в словарь
6. Найти блок со ссылкой на следующую страницу и перейти по ней
7. Делать пункты 1-6, пока есть ссылка на следующую страницу
8. Переписать в csv
"""

# Для парсинга
import requests
from bs4 import BeautifulSoup

# Для отладки
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


# Получаем ответ с вики
def get_response(url):
    response = requests.get(url)
    logger.debug(f"response: {response.status_code}")

    return response


# Варим красивый суп
def get_soup(response):
    soup = BeautifulSoup(response.text, "html.parser")
    logger.debug(f"tittle text: {soup.title.text}")

    return soup


# На текущей странице находим нужную группу
def find_group(soup) -> list:
    pages = soup.find("div", id="mw-pages")
    logger.debug(f'pages.text: {pages.text[:25].replace('\n', '')}...')

    current_group = pages.find_all("div", attrs={"class": "mw-category-group"})
    logger.debug(f"len current_group: {len(current_group)}")

    if not current_group:
        return []
    return current_group

# Из группы тянем Букву-ключ (h3) и количество животных (li)
def add_to_dict(group: list) -> None:
    for element in group:
        logger.debug(f'element.text: {element.text[:25].replace('\n', '')}...')

        text_h3 = element.find("h3").text
        logger.debug(f"text_h3: {text_h3}")

        count_li = len(element.find_all("li"))
        logger.debug(f"count_li: {count_li}")

        if text_h3 in dict_lett_num:
            dict_lett_num[text_h3] += count_li
            logger.debug(f"dict_lett_num: {dict_lett_num}")

        else:
            dict_lett_num[text_h3] = count_li
            logger.debug(f"dict_lett_num: {dict_lett_num}")


if __name__ == "__main__":
    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    dict_lett_num = {}

    next_page = True

    while next_page:

        response = get_response(url)
        soup = get_soup(response)
        group = find_group(soup)
        if group:
            add_to_dict(group)

        a_next_page = soup.find(name='a', string='Следующая страница')
        logger.debug(f"a_next_page: {a_next_page}")

        if not a_next_page:
            next_page = False
        else:
            url = "https://ru.wikipedia.org" + a_next_page["href"]
            logger.debug(f"next_page_url: {url}")

    for key, value in dict_lett_num.items():
        print(f"{key}: {value}")