from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtCore import QDate, Qt
from PyQt5 import uic
from app.db_utils.orders_db import get_order_by_id, save_production
from app.db_utils.puzzles_db import get_puzzles_for_order, get_puzzle_by_id



class ProductionCardView(QMainWindow):
    def __init__(self, production_id, parent=None):
        super().__init__(parent)
        ui_path = Path(__file__).resolve().parents[2] / 'assets' / 'styles' / 'production_card.ui'
        uic.loadUi(ui_path, self)

        self.production_id = production_id
        self.setWindowTitle(f"Агаш Пазл - Задание на производство заказа №{production_id}")

        # Список для хранения айди пазлов
        self.puzzles_id_list = []

        # Подключение кнопок
        self.saveButton.clicked.connect(self.save_production)
        self.backButton.clicked.connect(self.close)

        # Загрузка данных
        self.load_statuses()
        self.puzzles = get_puzzles_for_order()
        self.load_production()

    def load_statuses(self):
        """Загружает список статусов в комбобокс"""
        self.statusComboBox.clear()
        statuses = ["Принято в производство", "Выполнен"]
        for i in range(len(statuses)):
            self.statusComboBox.addItem(statuses[i], i)

    def load_production(self):
        """Загружает данные заказа"""
        production = get_order_by_id(self.production_id)

        status = 0 if production['status'] == 2 else 1
        self.statusComboBox.setCurrentIndex(
            self.statusComboBox.findData(status)
        )
        self.registrationDateEdit.setDate(QDate.fromString(production['production_registration_date'], 'yyyy-MM-dd'))
        self.completionDateEdit.setDate(QDate.fromString(production['production_completion_date'], 'yyyy-MM-dd'))
        self.fill_production_items(production['items'])

    def fill_production_items(self, items):
        """Заполняет таблицу строками заказа"""
        # Создать равномерное разделение таблицы на столбцы
        self.productionItemsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.productionItemsTable.setRowCount(len(items))
        for row, item in enumerate(items):
            puzzle = get_puzzle_by_id(item["puzzle_id"])
            self.puzzles_id_list.append(item["puzzle_id"])

            puzzle_id_item = QTableWidgetItem(puzzle["name"])
            quantity_item = QTableWidgetItem(str(item["quantity"]))

            self.productionItemsTable.setItem(row, 0, puzzle_id_item)
            self.productionItemsTable.setItem(row, 1, quantity_item)

            self.productionItemsTable.item(row, 0).setFlags(self.productionItemsTable.item(row, 0).flags() & Qt.ItemIsSelectable)

    def save_production(self):
        """Сохраняет изменения заказа"""
        if self.completionDateEdit.date() < self.registrationDateEdit.date():
            QMessageBox.warning(
                self,
                "Ошибка",
                "Дата выполнения задания на производство заказа не может быть раньше даты создания задания на производство заказа."
            )
            return

        confirmation = QMessageBox.question(
            self, "Подтверждение", "Вы уверены, что хотите сохранить изменения?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            status = 2 if self.statusComboBox.currentData() == 0 else 3
            production_data = {
                'order_id': self.production_id,
                'status': status,
                'production_registration_date': self.registrationDateEdit.date().toString('yyyy-MM-dd'),
                'production_completion_date': self.completionDateEdit.date().toString('yyyy-MM-dd'),
                'items': []
            }

            # Сбор данных из таблицы
            for row in range(self.productionItemsTable.rowCount()):
                quantity_item = self.productionItemsTable.item(row, 1)
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

                production_data['items'].append({'puzzle_id': self.puzzles_id_list[row], 'quantity': quantity})

            save_production(production_data)
            self.load_production()
            QMessageBox.information(self, "Успех", "Изменения сохранены.")
