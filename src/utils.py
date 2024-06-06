from datetime import timedelta
from pathlib import Path

from PySide6.QtWidgets import QMessageBox

ROOT_DIR = Path(__file__).parent.parent


def to_readable_time(minutes):
    delta = timedelta(minutes=minutes)
    return str(delta).split('.')[0]


def alert(text, caption=''):
    dlg = QMessageBox()
    dlg.setWindowTitle(caption)
    dlg.setText(text)
    return dlg.exec()
