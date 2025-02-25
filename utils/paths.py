from pathlib import Path

# Базовый путь проекта
BASE_DIR = Path(__file__).resolve().parent.parent

def get_assets_path(*path_segments):
    """Возвращает путь к папке assets."""
    return BASE_DIR / "assets" / Path(*path_segments)

def get_styles_path(*path_segments):
    """Возвращает путь к папке styles."""
    return get_assets_path("styles", *path_segments)

def get_puzzles_path(*path_segments):
    """Возвращает путь к папке puzzles."""
    return get_assets_path("puzzles", *path_segments)
