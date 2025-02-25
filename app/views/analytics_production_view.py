from pathlib import Path

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi
from app.db_utils.orders_db import get_productions_data


class AnalyticsProduction(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        ui_path = Path(__file__).resolve().parents[2] / 'assets' / 'styles' / 'analytics_production.ui'
        loadUi(ui_path, self)

        # Подключение кнопок
        self.btnExit.clicked.connect(self.close)

        # Обновляем данные при запуске
        self.update_table()

    def update_table(self):
        """Обновляет таблицу данными о заданиях."""
        # Создать равномерное разделение таблицы на столбцы
        productions_data = get_productions_data()

        self.productionItemsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.productionItemsTable.setRowCount(len(productions_data))

        for row_idx, row in enumerate(productions_data):
            self.productionItemsTable.setItem(row_idx, 0, QTableWidgetItem(row["product_name"]))
            self.productionItemsTable.setItem(row_idx, 1, QTableWidgetItem(row["date"]))

            # Подсвечиваем красным, если дата выполнения завтра
            completion_date = QDate.fromString(row["date"], "yyyy-MM-dd")
            if completion_date == QDate.currentDate().addDays(1):
                self.productionItemsTable.item(row_idx, 1).setBackground(QColor("#E57373"))
