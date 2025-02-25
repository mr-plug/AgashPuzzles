import sqlite3
from pathlib import Path

# Путь к базе данных
DB_PATH = Path(__file__).resolve().parents[2] / 'databases' / 'puzzles.db'


# Функция для выполнения SQL-запросов
def execute_query(query, params=None, fetch=False):
    """Функция для выполнения запросов, возвращает результат по запросу, если необходимо."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute(query, params or ())
    if fetch:
        result = cursor.fetchall()
    else:
        connection.commit()
        result = None
    connection.close()
    return result


# Функция для создания таблицы puzzles
def create_puzzles_table():
    """Создаёт таблицу puzzles в базе данных."""
    query = '''
    CREATE TABLE IF NOT EXISTS puzzles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sheet_id INTEGER NOT NULL,
        details_count INTEGER NOT NULL,
        price REAL NOT NULL,
        layout_image TEXT NOT NULL,
        FOREIGN KEY (sheet_id) REFERENCES plywood (id)
    );
    '''
    execute_query(query)


# Функция для добавления тестовых данных в таблицу puzzles
def add_sample_puzzles():
    """Добавление примеров пазлов в базу данных для тестирования."""
    puzzles = [
        ('Пазл лес-озеро', 1, 126, 1000, 'puzzle_1.png'),
        ('Красивые горы и озеро', 2, 126, 1200, 'puzzle_2.png'),
        ('Пазл река между гор', 1, 126, 1500, 'puzzle_3.png'),
        ('Пазл красивый вид с гор', 3, 126, 1800, 'puzzle_4.png'),
        ('Пазл мужчина на горе красивый вид', 2, 126, 1300, 'puzzle_5.png'),
        ('Мужчина встречает красивый закат', 3, 126, 1400, 'puzzle_6.png')
    ]

    query = '''
    INSERT INTO puzzles (name, sheet_id, details_count, price, layout_image)
    VALUES (?, ?, ?, ?, ?)
    '''

    for puzzle in puzzles:
        execute_query(query, puzzle)


# Функция для обновления цены пазла по его ID
def update_puzzle_price(puzzle_id, new_name, new_details_count, new_sheet_id, new_price):
    """Обновление цены пазла по его ID."""
    query = '''
    UPDATE puzzles
    SET name = ?, details_count = ?, sheet_id = ?, price = ?
    WHERE id = ?
    '''
    execute_query(query, (new_name, new_details_count, new_sheet_id, new_price, puzzle_id))


# Функция для получения всех пазлов
def get_all_puzzles():
    """Получение всех пазлов из базы данных."""
    query = 'SELECT id, name FROM puzzles'
    return execute_query(query, fetch=True)


def get_puzzles_for_order():
    """Возвращает список всех пазлов."""
    query = 'SELECT id, name, price FROM puzzles'
    puzzles = execute_query(query, fetch=True)
    return [{"id": puzzle[0], "name": puzzle[1], "price": puzzle[2]} for puzzle in puzzles]


# Функция для получения пазла по ID
def get_puzzle_by_id(puzzle_id):
    """Получение данных пазла по его ID."""
    query = 'SELECT * FROM puzzles WHERE id = ?'
    result = execute_query(query, (puzzle_id,), fetch=True)
    if result:
        return {
            "id": result[0][0],
            "name": result[0][1],
            "sheet_id": result[0][2],
            "details_count": result[0][3],
            "price": result[0][4],
            "layout_image": result[0][5]
        }
    return None
