from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
from PyQt5.uic import loadUi
from pathlib import Path
from app.db_utils.puzzles_db import get_all_puzzles
from app.views.puzzle_card import PuzzleCard


class PuzzlesList(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = Path(__file__).resolve().parents[2] / 'assets' / 'styles' / 'puzzles_list.ui'
        loadUi(ui_path, self)

        self.btnBack.clicked.connect(self.close)
        self.listPuzzles.itemDoubleClicked.connect(self.open_puzzle_card)

        self.load_puzzles()

    def load_puzzles(self):
        """Загружает список пазлов в QListWidget."""
        self.listPuzzles.clear()
        puzzles = get_all_puzzles()
        for puzzle_id, puzzle_name in puzzles:
            item = QListWidgetItem(puzzle_name)
            item.setData(1, puzzle_id)
            self.listPuzzles.addItem(item)

    def open_puzzle_card(self, item):
        """Открывает карточку пазла."""
        puzzle_id = item.data(1)
        self.puzzle_card = PuzzleCard(puzzle_id, parent=self)
        self.puzzle_card.show()
