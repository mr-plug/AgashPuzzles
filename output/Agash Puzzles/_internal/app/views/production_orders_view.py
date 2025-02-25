from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
from PyQt5 import uic
from app.db_utils.orders_db import get_all_orders
from app.views.production_order_card_view import ProductionCardView


class ProductionsListView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = Path(__file__).resolve().parents[2] / 'assets' / 'styles' / 'productions_list.ui'
        uic.loadUi(ui_path, self)

        self.backButton.clicked.connect(self.close)
        self.load_productions()
        self.productionsListWidget.itemClicked.connect(self.open_production_card)

    def load_productions(self):
        """Загружает заказы в список"""
        self.productionsListWidget.clear()
        productions = get_all_orders()  # Получаем заказы из базыЫ
        for production in productions:
            # Если статус в разработке или выполнен
            if production['status'] >= 2:
                item = QListWidgetItem()
                item.setData(0, f"Задание на производство заказа №{production['id']}")
                item.setData(1, production['id'])
                self.productionsListWidget.addItem(item)

    def open_production_card(self, item):
        """Открывает карточку задания по выбранному элементу"""
        production_id = item.data(1)
        self.production_card_view = ProductionCardView(production_id, self)
        self.production_card_view.show()
