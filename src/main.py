import os
import sys
from PySide6.QtWidgets import QApplication, QWidget, QTabWidget, QMainWindow, QPushButton, \
    QFileDialog
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt, QTimer

from rsvp_tab import RSVPTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle('Blitz')

        self.wpm = 300
        self.interval = 200

        tabs = QTabWidget()
        self.tabs = tabs
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)

        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#ffffbb'))
        self.setPalette(palette)

        self.open_button = QWidget()
        self.rsvp_tab = RSVPTab('../LICENSE', self)
        self.rsvp_tab2 = RSVPTab('/home/radagast/BEST_PRODUCTIVITY_HACKS', self)

        tabs.addTab(self.rsvp_tab, "LICENSE")
        tabs.addTab(self.rsvp_tab2, "BPH")
        tabs.addTab(self.open_button, "OPEN FILE")

        tabs.currentChanged.connect(self.on_current_changed)

        # Set up a timer to change the text
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_text)

        self.select_button = QPushButton('Select File')
        self.select_button.clicked.connect(self.open_file_dialog)

        self.setCentralWidget(tabs)
        self.showMaximized()

    def on_current_changed(self, index):
        if self.tabs.tabText(index) == "OPEN":
            self.open_file_dialog()

    def set_wpm(self, wpm):
        if wpm <= 0:
            return
        self.wpm = wpm
        cpm = wpm / self.tabs.currentWidget().source.get_average_len()
        self.interval = 60000 / cpm
        self.tabs.currentWidget().update_stats()
        if self.timer.isActive():
            self.timer.stop()
            self.timer.start(self.interval)

    def toggle(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(self.interval)

    def keyPressEvent(self, event):
        control_held = Qt.KeyboardModifier.ControlModifier in event.modifiers()
        if event.key() == Qt.Key_Space:
            self.toggle()
        elif event.key() == Qt.Key_Up:
            self.set_wpm(self.wpm + (10 if not control_held else 50))
        elif event.key() == Qt.Key_Down:
            self.set_wpm(self.wpm - (10 if not control_held else 50))

    def toggle_text(self):
        self.tabs.currentWidget().toggle_text()

    def open_file_dialog(self):
        current_index = self.tabs.tabBar().currentIndex()
        file_names, _ = QFileDialog.getOpenFileNames(self, 'Open File')
        for file_name in file_names:
            self.tabs.addTab(RSVPTab(file_name, self), os.path.split(file_name)[-1])
        self.tabs.removeTab(current_index)
        self.tabs.addTab(self.open_button, "OPEN FILE")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
