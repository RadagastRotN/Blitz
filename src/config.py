from pathlib import Path

import yaml
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QWidget, QSpinBox, QFontComboBox, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, \
    QPushButton, QColorDialog

from .utils import ROOT_DIR


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if Config._instance is None:
            self = super().__new__(cls)
            cls._instance = self
            config = cls.read_config()
            self._changed = False
            self._wpm = config['wpm']
            self._font_face = config['font']['face']
            self._font_size = config['font']['size']
            self._bg_color = config['bg_color']
        return Config._instance

    @property
    def wpm(self):
        return self._wpm

    @wpm.setter
    def wpm(self, wpm):
        print(wpm, self._wpm)
        if wpm > 0 and self._wpm != wpm:
            self._wpm = wpm
            self._changed = True

    @property
    def font_face(self):
        return self._font_face

    @font_face.setter
    def font_face(self, font_face):
        if self._font_face != font_face:
            self._font_face = font_face
            self._changed = True

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        if font_size > 0 and self._font_size != font_size:
            self._font_size = font_size
            self._changed = True

    @property
    def bg_color(self):
        return self._bg_color

    @font_size.setter
    def bg_color(self, bg_color):
        if self._bg_color != bg_color:
            self._bg_color = bg_color
            self._changed = True

    def get_font(self):
        return QFont(self._font_face, self._font_size, QFont.Bold)

    def get_bg_color(self):
        return QColor(self._bg_color)

    @staticmethod
    def read_config(filename=None):
        if filename is None:
            filename = ROOT_DIR / 'config.yml'
        with open(filename) as config_file:
            return yaml.safe_load(config_file)

    def save_config(self, filename=None):
        if not self._changed:
            return
        if filename is None:
            filename = ROOT_DIR / 'config.yml'
        config = {'wpm': self._wpm,
                  'font': {'face': self._font_face, 'size': self._font_size},
                  'bg_color': self._bg_color,
                  }
        with open(filename, 'w') as config_file:
            return yaml.safe_dump(config, config_file)


class ConfigTab(QWidget):

    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        config = Config()
        self.config = config

        self.wpm = QSpinBox(minimum=1, maximum=10000, value=config.wpm)
        self.font_face = QFontComboBox(currentFont=config.font_face)
        self.font_size = QSpinBox(minimum=10, maximum=200, value=config.font_size)
        self.color_button = QPushButton('Choose colour')
        self.wpm.valueChanged.connect(self.set_wpm)
        self.font_size.valueChanged.connect(self.set_font_size)
        self.font_face.currentFontChanged.connect(self.set_font_face)
        self.color_button.clicked.connect(self.color_button_clicked)

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel('WPM:'))
        self.layout.addWidget(self.wpm)

        self.layout.addWidget(QLabel('Font face:'))
        self.layout.addWidget(self.font_face)
        self.layout.addWidget(QLabel('Font size:'))
        self.layout.addWidget(self.font_size)
        self.layout.addWidget(QLabel('Background colour:'))
        self.layout.addWidget(self.color_button)

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.layout)

        self.setAutoFillBackground(True)

    def set_wpm(self, value):
        self.config.wpm = value

    def set_font_face(self, value):
        self.config.font_face = value.family()

    def set_font_size(self, value):
        self.config.font_size = value

    def color_button_clicked(self):
        color = QColorDialog.getColor()
        self.config.bg_color = color.name()
        self.parent_window.set_bg_color()
