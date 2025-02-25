from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from pathlib import Path
from app.views.plywood_cards_view import PlywoodCardsDirectory
from app.views.thickness_view import ThicknessDirectory
from app.views.wood_view import WoodDirectory


class DirectoriesWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Загрузка UI
        ui_path = Path(__file__).resolve().parents[2] / 'assets' / 'styles' / 'directories_window.ui'
        loadUi(ui_path, self)

        # Подключение кнопок к действиям
        self.btnWoodDirectory.clicked.connect(self.open_wood_directory)
        self.btnThicknessDirectory.clicked.connect(self.open_thickness_directory)
        self.btnPlywoodCards.clicked.connect(self.open_plywood_cards)
        self.btnBack.clicked.connect(self.close)

    def open_wood_directory(self):
        self.wood_directory = WoodDirectory(self)
        self.wood_directory.show()

    def open_thickness_directory(self):
        self.thickness_window = ThicknessDirectory(self)
        self.thickness_window.show()

    def open_plywood_cards(self):
        self.plywood_cards_window = PlywoodCardsDirectory(self)
        self.plywood_cards_window.show()
