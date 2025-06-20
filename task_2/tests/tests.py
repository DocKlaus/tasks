"""
Тесты:
1. Инициализация класса
2. Успешный вызов get_page()
3. Вызов get_page() с ошибкой
4. Вызов parse_groups()
5. Вызов parse_groups() без h3, без li
6. Вызов parse_groups() без li
7. Успешный вызов find_next_page()
8. Вызов find_next_page() с ошибкой
9. Сохранение в csv
10. Основной сценарий run()
11. Вызов run() при get_page() = None

"""

from unittest.mock import patch, Mock, mock_open
from bs4 import BeautifulSoup
import requests

from task_2.solution import WikipediaAnimalsParser


# 1. Тест для инициализации класса
def test_initialization():
    parser = WikipediaAnimalsParser()
    assert parser.letters_counts == {}
    assert parser.session.headers["User-Agent"] is not None

# 2. Тест для метода get_page
def test_get_page_success():
    parser = WikipediaAnimalsParser()

    # Заглушка содержимого response
    mock_response = Mock()
    mock_response.text = "<html>Test</html>"
    mock_response.raise_for_status = Mock()

    with patch.object(parser.session, "get", return_value=mock_response) as mock_get:
        soup = parser.get_page("http://test.com")
        assert soup is not None
        mock_get.assert_called_once_with("http://test.com", timeout=10)

# 3. Тест на ошибку запроса
def test_get_page_fail():
    parser = WikipediaAnimalsParser()
    with patch.object(parser.session, "get", side_effect=requests.RequestException("Error")) as mock_get:
        soup = parser.get_page("http://test.com")
        assert soup is None

# 4. Тест для парсинга групп
def test_parse_groups():
    parser = WikipediaAnimalsParser()
    test_html = """
    <div id="mw-pages">
        <div class="mw-category-group">
            <h3>Буква 1</h3>
            <ul>
                <li>Животное 1</li>
                <li>Животное 2</li>
            </ul>
        </div>
        <div class="mw-category-group">
            <h3>Буква 2</h3>
            <ul>
                <li>Животное 3</li>
            </ul>
        </div>
    </div>
    """
    soup = BeautifulSoup(test_html, features="html.parser")
    parser.parse_groups(soup)
    assert parser.letters_counts == {"Буква 1": 2, "Буква 2": 1}


# 5. Парсинг некорректной разметки
# нет h3, нет li
def test_parse_empty_groups():
    parser = WikipediaAnimalsParser()
    test_html = "<div></div>"
    soup = BeautifulSoup(test_html, "html.parser")
    parser.parse_groups(soup)
    # Словарь должен быть пустым
    assert parser.letters_counts == {}

# 6. Парсинг разметки без li (группа без животных)
def test_parse_group_without_items():
    parser = WikipediaAnimalsParser()
    test_html = """
    <div id="mw-pages">
        <div class="mw-category-group"><h3>A</h3></div>
    </div>
    """
    soup = BeautifulSoup(test_html, "html.parser")
    parser.parse_groups(soup)
    assert parser.letters_counts == {"A": 0}


# 7. Тест для поиска следующей страницы
def test_find_next_page_success():
    parser = WikipediaAnimalsParser()
    # Есть href
    test_html = """
    <div>
        <a href="/next_page">Следующая страница</a>
    </div>
    """
    soup = BeautifulSoup(test_html, features="html.parser")
    next_url = parser.find_next_page(soup)
    assert next_url == "https://ru.wikipedia.org/next_page"


# 8. Тест, где следующая страница не найдена
def test_find_next_page_failure():
    parser = WikipediaAnimalsParser()
    # Нет href
    test_html = """
    <div>
        <a>Следующая страница</a>
    </div>
    """
    soup = BeautifulSoup(test_html, features="html.parser")
    assert parser.find_next_page(soup) is None

# 9. Тест для сохранения в csv
def test_save_to_csv():
    parser = WikipediaAnimalsParser()
    parser.letters_counts = {"Буква 1": 2, "Буква 2": 1}

    # Объект, имитирующий работу open.
    # mock_open() возвращает файлоподобный объект с методами write(), read(), close() и др...
    m_o = mock_open()

    # Замена встроенной функции open() на объект-заглушку
    # для замены csv.writer не требуется создание спец объекта. Создаётся стандартный мок-объект
    # Альтернативный вариант записи:  patch("csv.writer", return_value=mock_writer) - но это избыточно
    with patch("builtins.open", m_o), patch("csv.writer") as m_writer:
        parser.save_to_csv()

        # одиночный вызов и с нужными аргументами
        # то есть запись в csv производилась 1 раз (csv.writer вызывался 1 раз)
        m_o.assert_called_once_with("beasts.csv", "w", newline="", encoding="utf-8")

        # метод writerow у csv.writer вызывался 2 раза, т.к. 2 строки
        assert m_writer.return_value.writerow.call_count == 2


# 10. Тест основного сценария run()
# Замена на моки, чтобы не делать реальные http-запросы
@patch.object(WikipediaAnimalsParser, "get_page")
@patch.object(WikipediaAnimalsParser, "find_next_page")

# Декораторы применяются в порядке, обратном их объявлению (снизу вверх)

def test_run(mock_find_next_page, mock_get_page):
    """
    1. Корректно обрабаывает неколько страниц
    2. Правильно парсит группы
    3. Останавливается, когда нет следующей страницы
    4. Сохр в csv
    """
    parser = WikipediaAnimalsParser()
    # Две фейковые странички (супчики)

    # <h3>...</h3> - 1 шт.
    # <li>...</li> - 1 шт.
    # <a href>...</a> - 1 шт.

    mock_soup_1 = BeautifulSoup("""
    <div id="mw-pages">
        <div class="mw-category-group">
            <h3>Буква 1</h3>
            <ul><li>Животное 1</li></ul>
        </div>
        <a href="/page_2">Следующая страница</a>
    </div>
    """, "html.parser")

    # <h3>...</h3> - 1 шт.
    # <li>...</li> - 2 шт.
    # <a href>...</a> - нет

    mock_soup_2 = BeautifulSoup("""
    <div id="mw-pages">
        <div class="mw-category-group">
            <h3>Буква 2</h3>
            <ul><li>Животное 2</li><li>Животное 3</li></ul>
        </div>
    </div>
    """, "html.parser")

    # Поведение моков
    # get_page() -> mock_soup_1 -> find_next_page() -> "http://page2" -> get_page() -> mock_soup_2 -> find_next_page() -> None

    # Последовательность возвращаемых значений для мметода get_page()
    mock_get_page.side_effect = [mock_soup_1, mock_soup_2]

    # Последовательных возвращаемых значений для метода find_next_page()
    mock_find_next_page.side_effect = ["http://page2", None]

    # замена save_to_csv() на object (мок)
    with patch.object(parser, "save_to_csv") as mock_save:
        parser.run()

        # В словаре должны появиться эти данные
        assert parser.letters_counts == {"Буква 1": 1, "Буква 2": 2}
        # Метод save_to_csv() должен быть вызван только один раз после обработки всех страниц
        mock_save.assert_called_once()


# 11. Тест поведения метода run() при ошибке (когда get_page() = None)
def test_run_with_errors():
    parser = WikipediaAnimalsParser()
    # Меняем get_page() на заглушку, которая возвращает return_value=None
    # И дополнительно мокаем сохранение csv, чтобы файл не создавался

    with patch.object(parser, "get_page", return_value=None), patch.object(
        parser, "save_to_csv"
    ) as mock_save:

        parser.run()

        assert parser.letters_counts == {}  # Словарь остался пустым -> сохранения нет
        mock_save.assert_not_called()
