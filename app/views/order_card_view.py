from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtCore import QDate, Qt
from PyQt5 import uic
from app.db_utils.orders_db import get_order_by_id, save_order, get_clients
from app.db_utils.puzzles_db import get_puzzles_for_order, get_puzzle_by_id


class OrderCardView(QMainWindow):
    def __init__(self, order_id, parent=None):
        super().__init__(parent)
        ui_path = Path(__file__).resolve().parents[2] / 'assets' / 'styles' / 'order_card.ui'
        uic.loadUi(ui_path, self)

        self.order_id = order_id
        self.setWindowTitle(f"Агаш Пазл - Заказ №{order_id}")

        # Список для хранения айди пазлов
        self.puzzles_id_list = []

        # Подключение кнопок
        self.saveButton.clicked.connect(self.save_order)
        self.backButton.clicked.connect(self.close)

        # Загрузка данных
        self.load_clients()
        self.load_statuses()
        self.puzzles = get_puzzles_for_order()
        self.load_order()

    def load_clients(self):
        """Загружает список клиентов в комбобокс"""
        self.clientComboBox.clear()
        clients = get_clients()
        for client in clients:
            self.clientComboBox.addItem(client['name'], client['id'])

    def load_statuses(self):
        """Загружает список статусов в комбобокс"""
        self.statusComboBox.clear()
        statuses = ["Черновик", "Согласовано с клиентом", "На производстве", "Готов к отгрузке", "Отгружен клиенту"]
        for i in range(len(statuses)):
            self.statusComboBox.addItem(statuses[i], i)

    def load_order(self):
        """Загружает данные заказа"""
        order = get_order_by_id(self.order_id)
        self.statusComboBox.setCurrentIndex(
            self.statusComboBox.findData(order['status'])
        )
        self.clientComboBox.setCurrentIndex(
            self.clientComboBox.findData(order['client_id'])
        )
        self.registrationDateEdit.setDate(QDate.fromString(order['registration_date'], 'yyyy-MM-dd'))
        self.completionDateEdit.setDate(QDate.fromString(order['completion_date'], 'yyyy-MM-dd'))
        self.fill_order_items(order['items'])

    def fill_order_items(self, items):
        """Заполняет таблицу строками заказа"""
        # Создать равномерное разделение таблицы на столбцы
        self.orderItemsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.orderItemsTable.setRowCount(len(items))
        for row, item in enumerate(items):
            puzzle = get_puzzle_by_id(item["puzzle_id"])
            self.puzzles_id_list.append(item["puzzle_id"])

            puzzle_id_item = QTableWidgetItem(puzzle["name"])
            price_item = QTableWidgetItem(str(item["price"]))
            quantity_item = QTableWidgetItem(str(item["quantity"]))
            total_item = QTableWidgetItem(str(item["total"]))

            self.orderItemsTable.setItem(row, 0, puzzle_id_item)
            self.orderItemsTable.setItem(row, 1, price_item)
            self.orderItemsTable.setItem(row, 2, quantity_item)
            self.orderItemsTable.setItem(row, 3, total_item)

            self.orderItemsTable.item(row, 0).setFlags(self.orderItemsTable.item(row, 0).flags() & Qt.ItemIsSelectable)
            self.orderItemsTable.item(row, 1).setFlags(self.orderItemsTable.item(row, 1).flags() & Qt.ItemIsSelectable)
            self.orderItemsTable.item(row, 3).setFlags(self.orderItemsTable.item(row, 3).flags() & Qt.ItemIsSelectable)

    def save_order(self):
        """Сохраняет изменения заказа"""
        if self.completionDateEdit.date() < self.registrationDateEdit.date():
            QMessageBox.warning(
                self,
                "Ошибка",
                "Дата выполнения заказа не может быть раньше даты создания заказа."
            )
            return

        confirmation = QMessageBox.question(
            self, "Подтверждение", "Вы уверены, что хотите сохранить изменения?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            order_data = {
                'order_id': self.order_id,
                'status': self.statusComboBox.currentData(),
                'client_id': self.clientComboBox.currentData(),
                'registration_date': self.registrationDateEdit.date().toString('yyyy-MM-dd'),
                'completion_date': self.completionDateEdit.date().toString('yyyy-MM-dd'),
                'items': []
            }

            # Сбор данных из таблицы
            for row in range(self.orderItemsTable.rowCount()):
                quantity_item = self.orderItemsTable.item(row, 2)
                quantity = int(quantity_item.text())

                if quantity < 0:
                    QMessageBox.warning(
                        self,
                        "Ошибка",
                        "Количество продукта не может отрицательным."
                    )
                    return
                if quantity >= 100000000:
                    QMessageBox.warning(
                        self,
                        "Ошибка",
                        "Количество продукта не может быть слишком большим."
                    )
                    return

                order_data['items'].append({'puzzle_id': self.puzzles_id_list[row], 'quantity': quantity})

            save_order(order_data)
            self.load_order()
            QMessageBox.information(self, "Успех", "Изменения сохранены.")
