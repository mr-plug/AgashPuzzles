import os

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from pathlib import Path
from PyQt5.QtGui import QPixmap
from app.db_utils.puzzles_db import get_puzzle_by_id, update_puzzle_price
from app.db_utils.plywood_db import get_all_plywood_cards


class PuzzleCard(QMainWindow):
    def __init__(self, puzzle_id, parent=None):
        super().__init__(parent)
        ui_path = Path(__file__).resolve().parents[2] / 'assets' / 'styles' / 'puzzle_card.ui'
        loadUi(ui_path, self)

        puzzle = get_puzzle_by_id(puzzle_id)
        self.setWindowTitle("Агаш Пазл - " + puzzle["name"])

        self.puzzle_id = puzzle_id
        self.btnSave.clicked.connect(self.save_changes)
        self.btnBack.clicked.connect(self.close)

        self.load_puzzle_data()

    def load_puzzle_data(self):
        """Загружает данные пазла и фанерных листов."""
        puzzle = get_puzzle_by_id(self.puzzle_id)
        sheets = get_all_plywood_cards()

        self.lineName.setText(puzzle["name"])
        self.spinDetailsCount.setValue(puzzle["details_count"])
        self.spinPrice.setValue(puzzle["price"])

        image_path = str(Path(__file__).resolve().parents[2] / 'assets' / 'puzzles' / puzzle["layout_image"])
        self.labelLayout.setPixmap(QPixmap(image_path))

        self.comboSheet.clear()
        for sheet_id, sheet_name in sheets:
            self.comboSheet.addItem(sheet_name, sheet_id)

        index = self.comboSheet.findData(puzzle["sheet_id"])
        if index != -1:
            self.comboSheet.setCurrentIndex(index)

    def save_changes(self):
        """Сохраняет изменения с подтверждением."""
        name = self.lineName.text()
        details_count = self.spinDetailsCount.value()
        sheet_id = self.comboSheet.currentData()
        price = self.spinPrice.value()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Название пазла не может быть пустым.")
            return

        confirmation = QMessageBox.question(
            self, "Подтверждение", "Вы уверены, что хотите сохранить изменения?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            update_puzzle_price(self.puzzle_id, name, details_count, sheet_id, price)  # Обновляем цену
            QMessageBox.information(self, "Успех", "Изменения сохранены.")
