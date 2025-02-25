import sqlite3
from pathlib import Path

from app.db_utils.puzzles_db import get_puzzle_by_id

# Путь к базе данных
DB_PATH = Path(__file__).resolve().parents[2] / 'databases' / 'orders.db'


def execute_query(query, params=None, fetch=False):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, params or ())
    if fetch:
        result = cursor.fetchall()
    else:
        connection.commit()
        result = None
    connection.close()
    return result


# Функция для создания таблиц базы данных
def create_tables():
    """Создает таблицы clients, orders и order_items."""
    clients_table = '''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    '''

    orders_table = '''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status INTEGER NOT NULL,
        client_id INTEGER NOT NULL,
        registration_date DATE NOT NULL,
        completion_date DATE,
        production_registration_date DATE,
        production_completion_date DATE,
        production_status INTEGER,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    );
    '''

    order_items_table = '''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        puzzle_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (puzzle_id) REFERENCES puzzles (id)
    );
    '''

    execute_query(clients_table)
    execute_query(orders_table)
    execute_query(order_items_table)


def get_all_orders():
    """Получает список всех заказов из БД"""
    query = '''
    SELECT id, registration_date, status
    FROM orders
    ORDER BY registration_date DESC
    '''
    results = execute_query(query, fetch=True)
    return [{"id": row[0], "registration_date": row[1], "status": row[2]} for row in results]


def get_order_by_id(order_id):
    """Получает данные заказа по его ID."""
    # Получение основного заказа
    order_query = '''
    SELECT *
    FROM orders
    WHERE id = ?
    '''
    order = execute_query(order_query, (order_id,), fetch=True)
    if not order:
        return None
    order = order[0]

    # Получение позиций заказа
    items_query = '''
    SELECT puzzle_id, quantity
    FROM order_items
    WHERE order_id = ?
    '''
    items = execute_query(items_query, (order_id,), fetch=True)

    return {
        "id": order["id"],
        "status": order["status"],
        "client_id": order["client_id"],
        "registration_date": order["registration_date"],
        "completion_date": order["completion_date"],
        "production_registration_date": order["production_registration_date"],
        "production_completion_date": order["production_completion_date"],
        "items": [
            {
                "puzzle_id": item["puzzle_id"],
                "price": get_puzzle_by_id(item["puzzle_id"])["price"],
                "quantity": item["quantity"],
                "total": item["quantity"] * get_puzzle_by_id(item["puzzle_id"])["price"]
            }
            for item in items
        ]
    }


def save_order(order_data):
    """Сохраняет данные заказа в базу."""
    # Обновление основного заказа
    order_query = '''
    UPDATE orders
    SET status = ?, client_id = ?, registration_date = ?, completion_date = ?
    WHERE id = ?
    '''
    execute_query(
        order_query,
        (order_data["status"],
         order_data["client_id"],
         order_data["registration_date"],
         order_data["completion_date"],
         order_data["order_id"])
    )

    insert_item_query = '''
    UPDATE order_items
    SET quantity = ?
    WHERE order_id = ? AND puzzle_id = ?
    '''
    for item in order_data["items"]:
        execute_query(insert_item_query, (
            item["quantity"],
            order_data["order_id"],
            item["puzzle_id"]
        ))


def save_production(production_data):
    """Сохраняет данные заказа в базу."""
    # Обновление основного задания заказа
    order_query = '''
    UPDATE orders
    SET status = ?, production_registration_date = ?, production_completion_date = ?
    WHERE id = ?
    '''

    execute_query(
        order_query,
        (production_data["status"],
         production_data["production_registration_date"],
         production_data["production_completion_date"],
         production_data["order_id"])
    )

    insert_item_query = '''
    UPDATE order_items
    SET quantity = ?
    WHERE order_id = ? AND puzzle_id = ?
    '''
    for item in production_data["items"]:
        execute_query(insert_item_query, (
            item["quantity"],
            production_data["order_id"],
            item["puzzle_id"]
        ))


def get_clients():
    """Возвращает список всех клиентов."""
    query = 'SELECT id, name FROM clients'
    clients = execute_query(query, fetch=True)
    return [{"id": client["id"], "name": client["name"]} for client in clients]


# Функция для добавления тестовых данных в таблицы
def add_sample_data():
    """Добавляет тестовые данные в таблицы."""
    # Добавляем клиентов
    clients = [
        ('Клиент А',), ('Клиент B',), ('Клиент C',), ('Клиент D',),
        ('Клиент E',), ('Клиент F',), ('Клиент G',), ('Клиент H',),
        ('Клиент I',), ('Клиент J',)
    ]

    execute_query('INSERT INTO clients (name) VALUES (?);', params=clients[0])

    for client in clients[1:]:
        execute_query('INSERT INTO clients (name) VALUES (?);', params=client)

    # Добавляем заказы
    orders = [
        (0, 1, '2024-01-01', '2024-01-10', None, None, None),
        (1, 2, '2024-01-05', '2024-01-15', None, None, None),
        (2, 3, '2024-01-10', '2024-01-20', '2024-01-18', '2024-01-25', 0),
        (3, 4, '2024-01-12', '2024-01-22', '2024-01-20', '2024-01-23', 1),
        (4, 5, '2024-01-15', '2024-01-25', '2024-01-22', '2024-01-29', 1),
        (4, 6, '2024-01-16', '2024-02-01', '2024-01-25', '2024-02-01', 1),
        (4, 7, '2024-01-17', '2024-02-02', '2024-01-24', '2024-02-02', 1),
        (4, 8, '2024-01-20', '2024-02-05', '2024-01-23', '2024-02-02', 1),
        (4, 9, '2024-01-22', '2024-02-07', '2024-01-28', '2024-02-03', 1),
        (4, 1, '2024-01-23', '2024-02-10', '2024-01-29', '2024-02-04', 1),
    ]

    order_query = '''
    INSERT INTO orders (
        status, client_id, registration_date, completion_date, production_registration_date, production_completion_date, production_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?);
    '''

    for order in orders:
        execute_query(order_query, order)

    # Добавляем позиции заказов
    order_items = [
        (1, 1, 18),
        (1, 2, 15),
        (1, 5, 3),
        (1, 4, 2),

        (2, 2, 10),
        (2, 3, 7),
        (2, 5, 4),
        (2, 1, 2),
        (2, 6, 50),

        (3, 5, 12),
        (3, 1, 10),
        (3, 4, 11),

        (4, 2, 42),
        (4, 3, 43),
        (4, 1, 43),
        (4, 5, 43),

        (5, 1, 13),
        (5, 2, 32),
        (5, 4, 43),
        (5, 3, 54),
        (5, 5, 65),
        (5, 6, 23),

        (6, 1, 13),
        (6, 2, 12),
        (6, 5, 43),

        (7, 1, 51),
        (7, 2, 52),
        (7, 4, 53),
        (7, 5, 52),
        (7, 3, 54),
        (7, 6, 55),

        (8, 1, 13),
        (8, 3, 35),
        (8, 2, 47),
        (8, 5, 28),
        (8, 6, 12),

        (9, 3, 14),
        (9, 4, 35),
        (9, 2, 47),
        (9, 1, 58),
        (9, 6, 62),
        (9, 5, 11),

        (10, 6, 11),
        (10, 4, 32),
        (10, 3, 13),
        (10, 1, 98),
        (10, 2, 10)
    ]

    order_items_query = '''
    INSERT INTO order_items (
        order_id, puzzle_id, quantity
    ) VALUES (?, ?, ?);
    '''

    for item in order_items:
        execute_query(order_items_query, item)


def get_sales_data(start_date, end_date, product_id):
    """Возвращает данные о продажах за период с фильтром по товару."""
    query = '''
    SELECT id
    FROM orders
    WHERE completion_date BETWEEN ? AND ?
    '''
    params = [start_date, end_date]

    orders_filter_date = execute_query(query, params, fetch=True)
    items = {}
    for order in orders_filter_date:
        order_info = get_order_by_id(order['id'])
        if order_info['status'] == 4:
            for item in order_info['items']:
                if item['puzzle_id'] == product_id:
                    items[order_info['completion_date']] = items.get(item['puzzle_id'], 0) + item['quantity']

    result = []
    for completion_date in items.keys():
        puzzle = get_puzzle_by_id(product_id)
        result.append({'total_quantity': items[completion_date],
                       'total_price': puzzle['price'] * items[completion_date],
                       'date': completion_date})

    return result


def get_productions_data():
    """Возвращает данные о продажах за период с фильтром по товару."""
    query = '''
    SELECT id, production_completion_date
    FROM orders
    WHERE status = 2
    '''

    productions = execute_query(query, params=None, fetch=True)
    result = []
    for production in productions:
        result.append({"product_name": "Задание на производство заказа №" + str(production["id"]),
                       "date": production["production_completion_date"]})

    return result
