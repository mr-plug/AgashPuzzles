from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from pathlib import Path


class ThicknessDirectory(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Загрузка интерфейса
        ui_path = Path(__file__).resolve().parents[2] / 'assets' / 'styles' / 'thickness_directory.ui'
        loadUi(ui_path, self)

        # Инициализация выпадающего списка и событий
        self.thickness_data = {
            "3 мм": "3 мм - это стандартная толщина для легких пазлов, которые предназначены для детей или начинающих. Они достаточно прочные, но при этом легкие.",
            "4 мм": "4 мм - эта толщина обеспечивает хорошую прочность и стабильность, что делает её популярной для большинства пазлов.",
            "6 мм": "6 мм - такой размер используется для более крупных и сложных пазлов, где требуется дополнительная прочность и устойчивость.",
            "9 мм": "9 мм - пазлы такой толщины могут использоваться для специальных или крупных пазлов, а также для пазлов с объемными элементами.",
        }
        self.comboThickness.addItems(self.thickness_data.keys())
        self.comboThickness.currentTextChanged.connect(self.update_text_info)

        # Подключение кнопки "Назад"
        self.btnBack.clicked.connect(self.close)

        # Устанавливаем начальное значение текста
        self.update_text_info()

    def update_text_info(self):
        """Обновляет текстовое поле в зависимости от выбранного элемента."""
        selected_thickness  = self.comboThickness.currentText()
        self.textThicknessInfo.setPlainText(self.thickness_data.get(selected_thickness, ""))
