import sys
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import QApplication, QWidget, QTabWidget, QMainWindow, QFileDialog
from PySide6.QtGui import QPalette, QClipboard
from PySide6.QtCore import Qt, QTimer

from utils import alert, TEMP_DIR
from .config import Config, ConfigTab
from .rsvp_tab import RSVPTab

config = Config()

OPEN_TAB_CAPTION = "OPEN FILE"
CLIPBOARD_TAB_CAPTION = "FROM CLIPBOARD"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._wpm = 1

        # Set window properties
        self.setWindowTitle('Blitz')

        tabs = QTabWidget()
        self.tabs = tabs
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)

        self.set_bg_color()

        self.open_button = QWidget()
        self.open_button.setAutoFillBackground(True)
        self.clipboard_button = QWidget()
        self.clipboard_button.setAutoFillBackground(True)

        tabs.addTab(ConfigTab(self), "CONFIG")
        tabs.addTab(self.open_button, OPEN_TAB_CAPTION)
        tabs.addTab(self.clipboard_button, CLIPBOARD_TAB_CAPTION)

        tabs.currentChanged.connect(self.on_current_changed)

        # Set up a timer to change the text
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_text)

        self._wpm = config.wpm

        self.setCentralWidget(tabs)
        self.showMaximized()

    def on_current_changed(self, index):
        if self.timer.isActive():
            self.timer.stop()

        if self.tabs.tabText(index) == OPEN_TAB_CAPTION:
            self.open_file_dialog()
        elif self.tabs.tabText(index) == CLIPBOARD_TAB_CAPTION:
            self.paste_clipboard()
        elif type(self.tabs.currentWidget()) == RSVPTab:
            self.tabs.currentWidget().activate()
            self._update_timer()

    def paste_clipboard(self):
        text = QClipboard().text()
        if text:
            filename = TEMP_DIR / str(datetime.now().timestamp())
            with open(filename, 'w') as tmp_file:
                tmp_file.write(text)
            self.tabs.addTab(RSVPTab(filename, self), "from clipboard")
            self.tabs.setCurrentIndex(self.tabs.count() - 1)
        else:
            self.tabs.setCurrentIndex(0)
            alert("Clipboard does not contain text", "Notice")

    @property
    def wpm(self):
        return self._wpm

    @wpm.setter
    def wpm(self, wpm):
        if wpm <= 0:
            return
        self._wpm = wpm
        if type(self.tabs.currentWidget()) == RSVPTab:
            self._update_timer()

    def _update_timer(self):
        cpm = self._wpm / self.tabs.currentWidget().source.average_len
        self.interval = 60000 / cpm
        self.tabs.currentWidget().update_stats()
        if self.timer.isActive():
            self.timer.stop()
            self.timer.start(self.interval)

    def toggle(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.toggle_text()
            self.timer.start(self.interval)

    def keyPressEvent(self, event):
        control_held = Qt.KeyboardModifier.ControlModifier in event.modifiers()
        if event.key() == Qt.Key_Space:
            self.toggle()
        elif event.key() == Qt.Key_Up:
            self.wpm += 10 if not control_held else 50
        elif event.key() == Qt.Key_Down:
            self.wpm -= 10 if not control_held else 50

    def toggle_text(self):
        self.tabs.currentWidget().toggle_text()

    def open_file_dialog(self):
        tabs_count = self.tabs.count()
        file_names, _ = QFileDialog.getOpenFileNames(self, 'Open File(s)')
        opened = 0
        for filename in file_names:
            try:
                self.tabs.addTab(RSVPTab(filename, self), self._fname_to_tab_caption(filename))
                opened += 1
            except (FileNotFoundError, UnicodeDecodeError) as ex:
                alert(f"Couldn't open file {filename}:\n{ex}", "Error")
        if opened:
            self.tabs.setCurrentIndex(tabs_count)
        else:
            self.tabs.setCurrentIndex(0 if tabs_count == 2 else tabs_count - 1)

    @staticmethod
    def _fname_to_tab_caption(filename):
        filename = Path(filename).name
        if len(filename) > 25:
            return f"{filename[:11]}...{filename[-11:]}"
        else:
            return filename

    def set_bg_color(self):
        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, Config().get_bg_color())
        self.setPalette(palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.open_file_dialog()
    exit_code = app.exec()
    Config().save_config()
    sys.exit(exit_code)
