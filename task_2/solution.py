"""
Мнение нейросети по улучшению имеющегося кода
Улучшения:
1. ООП - инкапсуляция логики в класс
2. Корректная обработка сетевых ошибок
3. Типизация - добавлены аннотации типов
4. Логирование - более информативное и менее нагруженное
5. URL joining - безопасное соединение url
6. Добавлен заголовок запроса User-Agent
7. Статистика
8. Timeout - Защита от зависания
9. requests.Session() - ускоряет выполнение нескольких запросов к одному серверу.
    После первого запроса соединение не закрывается, а сохраняется для повторного использования.


Вывод:
1. Нужно больше практики с классами
2. Почитать про requests.Session() и session.headers.update() - надо ли это тут вообще. Или просто хороший тон
3. Респонс и суп можно не разделять
4. Нужно больше потыкаться с логированием
5. response.raise_for_status() интересная штука. Почитать подробнее о вариациях применения
6. Безопасное вытягивание из словаря через get() практиковать чаще
7. urljoin(self.BASE_URL, next_link['href']) библиотека для правильной url-лепёшки (чтоб не лепить из строчек)
8. Потыкаться с атрибутами объектов BeautifulSoup
9. варианты next_link['href'] и next_link.find('href'). Разница, варианты применения
10. Не нагружать if __name__ == "__main__":

11. Можно добавить асинхрон
"""


import logging

import requests
from bs4 import BeautifulSoup

from typing import Dict, List, Optional
from urllib.parse import urljoin
import csv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


# Создание класса
class WikipediaAnimalsParser:
    # https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту
    # Задаём базовую часть url, которая не меняется
    BASE_URL = "https://ru.wikipedia.org"

    # Стартовая вторая часть url, которая будет меняться
    START_URL = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"

    # Инициализация (словарь для хранения, сессия текущего запроса и зачем-то headers
    def __init__(self):
        self.letters_counts: Dict[str, int] = {}
        self.session = requests.Session() # узнать лучше
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    # Получение странички (две мои функции можно объединить в одну)
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status() # проверяет, был ли HTTP-запрос успешным [ничего | HTTPError: 404 Client Error]

            return BeautifulSoup(response.text, features="html.parser")

        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    # Парсим группы
    def parse_groups(self, soup: BeautifulSoup) -> None:
        pages_div = soup.find(name="div", id="mw-pages")
        if not pages_div:
            logger.warning("No mw-pages div found")
            return

        groups = pages_div.find_all(name="div", class_="mw-category-group")
        logger.info(f"Found {len(groups)} groups on page")

        for group in groups:
            letter = group.find("h3")
            if not letter:
                continue

            letter_text = letter.text.strip()
            items_count = len(group.find_all("li"))
            self.letters_counts[letter_text] = self.letters_counts.get(letter_text, 0) + items_count # интересно. надо поюзать

            logger.debug(f'Letter: {letter_text}, Count: {items_count}')

    # Чекаем следующую страничку
    def find_next_page(self, soup: BeautifulSoup) -> Optional[str]:
        next_link = soup.find('a', string='Следующая страница')
        if next_link and 'href' in next_link.attrs: # прикольно
            return urljoin(self.BASE_URL, next_link['href']) # вместо слепливания двух строчек
        return None

    # Записываем в csv
    def save_to_csv(self, filename: str = "beasts.csv"):
        with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            for letter, count in self.letters_counts.items():
                writer.writerow([letter, count])
        logger.info(f"Result saved to {filename}")

    # Запуск
    def run(self) -> None:
        current_url = self.START_URL
        page_count = 0

        while current_url:
            page_count += 1
            logger.info(f"Page count: #{page_count}: {current_url}")

            # Получаем суп
            soup = self.get_page(current_url)
            if not soup:
                break

            # Парсим страничку (внутри идёт запись в словарь)
            self.parse_groups(soup)
            # В супе ищем новую страничку и переписываем в текущую
            current_url = self.find_next_page(soup)

        if self.letters_counts:
            self.save_to_csv()

        # Доп лог-плюшки от НС
        logger.info(f"Total pages processed: {page_count}")
        logger.info(f"Total letters found: {len(self.letters_counts)}")
        logger.info(f"Total animals: {sum(self.letters_counts.values())}")


if __name__ == "__main__":
    parser = WikipediaAnimalsParser()
    parser.run()

    # Этот блок короткий и понятный без лишней чепухи.
    # Не надо его нагружать.