from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from .config import Config
from chunkers.chunkers import BasicChunker
from .sources import open_source
from .utils import to_readable_time


class RSVPTab(QWidget):

    def __init__(self, source, parent_window):
        super().__init__()
        self.parent_window = parent_window

        self.source = BasicChunker(open_source(source))
        self.chunk = 0

        self.chunk_label = QLabel('', self)
        self.chunk_label.setAlignment(Qt.AlignCenter)

        self.stats_label = QLabel('WPM:   Text length: \nEstimated time:   Interval: ', self)
        self.stats_label.setAlignment(Qt.AlignTop)
        # Set background color
        self.setAutoFillBackground(True)

        # Use a layout to center the label in the window
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.chunk_label, 1)
        self.layout.addWidget(self.stats_label)
        self.setLayout(self.layout)

        # Create a label and set its properties
        self.chunk_label.setFont(Config().get_font())

        self.update_stats()

    def activate(self):
        self.chunk_label.setFont(Config().get_font())

    def toggle_text(self):
        try:
            self.chunk_label.setText(self.source.get_chunk(self.chunk))
            self.chunk += 1
        except IndexError:
            self.parent_window.toggle()
            self.chunk = 0

    def _get_stats(self):
        return self.parent_window.wpm, self.source.words_count, \
               to_readable_time(self.source.words_count / self.parent_window.wpm)

    def update_stats(self):
        self.stats_label.setText("WPM: {:d}  Text length: {:d}\nEstimated time: {}".format(*self._get_stats()))
