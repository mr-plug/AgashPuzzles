from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from app.db_utils.plywood_db import initialize_plywood_db, get_plywood_name, save_plywood_name


class PlywoodCardsDirectory(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = Path(__file__).resolve().parents[2] / 'assets' / 'styles' / 'plywood_cards.ui'
        loadUi(ui_path, self)

        initialize_plywood_db()  # Инициализация базы данных

        self.wood_types = ["Береза", "Сосна", "Клен", "Махагон", "Дуб", "Липа", "Тик", "Вишня"]
        self.thicknesses = ["3 мм", "4 мм", "6 мм", "9 мм"]

        self.comboWood.addItems(self.wood_types)
        self.comboThickness.addItems(self.thicknesses)

        self.comboWood.currentTextChanged.connect(self.update_name_from_db)
        self.comboThickness.currentTextChanged.connect(self.update_name_from_db)
        self.btnSave.clicked.connect(self.save_name)
        self.btnBack.clicked.connect(self.close)

        self.update_name_from_db()

    def update_name_from_db(self):
        """Обновляет поле с названием из базы данных."""
        wood = self.comboWood.currentText()
        thickness = self.comboThickness.currentText()

        self.lineName.setText(get_plywood_name(wood, thickness))

    def save_name(self):
        """Сохраняет название фанерного листа в базу данных."""
        wood = self.comboWood.currentText()
        thickness = self.comboThickness.currentText()
        name = self.lineName.text()

        save_plywood_name(wood, thickness, name)
        QMessageBox.information(self, "Название сохранено", f'Название "{name}" сохранено!')
