from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from app.db_utils.orders_db import get_sales_data
from app.db_utils.puzzles_db import get_all_puzzles


class AnalyticsOrder(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        ui_path = Path(__file__).resolve().parents[2] / 'assets' / 'styles' / 'analytics_order.ui'
        loadUi(ui_path, self)

        self.load_products()

        # Настраиваем область для диаграммы
        self.chart_layout = QVBoxLayout(self.chart_widget)
        self.chart_figure = Figure()
        self.chart_canvas = FigureCanvas(self.chart_figure)
        self.chart_layout.addWidget(self.chart_canvas)

        # Подключение кнопок
        self.btn_apply_filter.clicked.connect(self.update_data)
        self.btnExit.clicked.connect(self.close)

        # Обновляем данные при запуске
        self.update_data()

    def load_products(self):
        """Загружает список продукты в комбобокс"""
        self.product_filter.clear()
        products = get_all_puzzles()
        for product in products:
            self.product_filter.addItem(product[1], product[0])

    def update_data(self):
        # Получаем данные из базы
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        product = self.product_filter.currentData()
        sales_data = get_sales_data(start_date, end_date, product)

        # Обновляем таблицу
        self.update_table(sales_data)

        # Обновляем диаграмму
        self.update_chart(sales_data)

    def update_table(self, sales_data):
        """Обновляет таблицу данными о продажах."""
        # Создать равномерное разделение таблицы на столбцы
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.sales_table.setRowCount(len(sales_data))

        for row_idx, row in enumerate(sales_data):
            self.sales_table.setItem(row_idx, 0, QTableWidgetItem(str(row["total_quantity"])))
            self.sales_table.setItem(row_idx, 1, QTableWidgetItem(f"{row['total_price']:.2f}"))
            self.sales_table.setItem(row_idx, 2, QTableWidgetItem(row["date"]))

    def update_chart(self, sales_data):
        """Обновляет диаграмму с помощью Matplotlib."""
        self.chart_figure.clear()
        ax = self.chart_figure.add_subplot(111)

        product_name = self.product_filter.currentText()

        # Подготовка данных
        products = [row["date"] for row in sales_data]
        totals = [row["total_price"] for row in sales_data]

        # Построение диаграммы
        ax.bar(products, totals, color="skyblue")
        ax.set_title("Продажи по товару " + product_name)
        ax.set_xlabel("Дата")
        ax.set_ylabel("Сумма продаж")

        # Обновление отображения
        self.chart_canvas.draw()
