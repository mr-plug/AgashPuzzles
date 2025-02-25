from app.db_utils.base import execute_query, execute_action
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / 'databases' / 'plywood.db'



def initialize_plywood_db():
    """Создаёт таблицу для фанерных листов."""
    # Удаляем старую таблицу, если она существует, и создаем её заново
    query = '''
    CREATE TABLE IF NOT EXISTS plywood_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wood_type TEXT NOT NULL,
        thickness TEXT NOT NULL,
        name TEXT NOT NULL,
        UNIQUE(wood_type, thickness)
    )
    '''
    execute_action(DB_PATH, query)


def save_plywood_name(wood_type, thickness, name):
    """Сохраняет или обновляет название фанерного листа."""
    query = '''
    INSERT INTO plywood_cards (wood_type, thickness, name)
    VALUES (?, ?, ?)
    ON CONFLICT(wood_type, thickness) DO UPDATE SET name = excluded.name
    '''
    execute_action(DB_PATH, query, (wood_type, thickness, name))


def get_all_plywood_cards():
    """
    Возвращает список всех фанерных листов.
    Каждый элемент списка — кортеж (id, name).
    """
    query = '''
    SELECT id, name FROM plywood_cards
    '''
    result = execute_query(DB_PATH, query)
    return result


def get_plywood_name(wood_type, thickness):
    """Возвращает название фанерного листа."""
    query = '''
    SELECT name FROM plywood_cards
    WHERE wood_type = ? AND thickness = ?
    '''
    result = execute_query(DB_PATH, query, (wood_type, thickness))
    return result[0][0] if result else None


def add_default_names():
    wood_types = ["Береза", "Сосна", "Клен", "Махагон", "Дуб", "Липа", "Тик", "Вишня"]
    thicknesses = ["3 мм", "4 мм", "6 мм", "9 мм"]
    for wood_type in wood_types:
        for thickness in thicknesses:
            save_plywood_name(wood_type, thickness, f"{wood_type}, {thickness}")
