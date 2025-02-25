from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from pathlib import Path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загрузка UI
        ui_path = Path(__file__).resolve().parents[2] / 'assets' / 'styles' / 'main_window.ui'
        loadUi(ui_path, self)

        # Подключение кнопок к действиям
        self.btnDirectories.clicked.connect(self.open_directories_window)
        self.btnPuzzles.clicked.connect(self.open_puzzles_list_window)
        self.btnOrders.clicked.connect(self.open_orders_list_window)
        self.btnProductions.clicked.connect(self.open_productions_list_window)
        self.btnAnalyticsOrders.clicked.connect(self.open_analytics_orders_window)
        self.btnAnalyticsProductions.clicked.connect(self.open_analytics_production_window)
        self.btnExit.clicked.connect(self.confirm_exit)

    def open_directories_window(self):
        from app.views.directories_window import DirectoriesWindow
        self.directories_window = DirectoriesWindow(self)
        self.directories_window.show()

    def open_puzzles_list_window(self):
        from app.views.puzzles_list import PuzzlesList
        self.puzzles_list_window = PuzzlesList(self)
        self.puzzles_list_window.show()

    def open_orders_list_window(self):
        from app.views.orders_view import OrdersListView
        self.order_list_view = OrdersListView(self)
        self.order_list_view.show()

    def open_productions_list_window(self):
        from app.views.production_orders_view import ProductionsListView
        self.production_list_view = ProductionsListView(self)
        self.production_list_view.show()

    def open_analytics_orders_window(self):
        from app.views.analytics_order_view import AnalyticsOrder
        self.analytic_view = AnalyticsOrder(self)
        self.analytic_view.show()

    def open_analytics_production_window(self):
        from app.views.analytics_production_view import AnalyticsProduction
        self.analytic_view = AnalyticsProduction(self)
        self.analytic_view.show()

    def confirm_exit(self):
        confirmation = QMessageBox.question(
            self,
            "Подтверждение выхода",
            "Вы уверены, что хотите выйти из приложения?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmation == QMessageBox.Yes:
            self.close()
