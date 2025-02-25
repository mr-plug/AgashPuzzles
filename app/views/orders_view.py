from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
from PyQt5 import uic
from app.views.order_card_view import OrderCardView
from app.db_utils.orders_db import get_all_orders


class OrdersListView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = Path(__file__).resolve().parents[2] / 'assets' / 'styles' / 'orders_list.ui'
        uic.loadUi(ui_path, self)

        self.backButton.clicked.connect(self.close)
        self.load_orders()
        self.ordersListWidget.itemClicked.connect(self.open_order_card)

    def load_orders(self):
        """Загружает заказы в список"""
        self.ordersListWidget.clear()
        orders = get_all_orders()  # Получаем заказы из базыЫ
        for order in orders:
            item = QListWidgetItem()
            item.setData(0, f"Заказ №{order['id']}")
            item.setData(1, order['id'])
            self.ordersListWidget.addItem(item)

    def open_order_card(self, item):
        """Открывает карточку заказа по выбранному элементу"""
        order_id = item.data(1)
        self.order_card_view = OrderCardView(order_id, self)
        self.order_card_view.show()
