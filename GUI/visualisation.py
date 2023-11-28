from pathlib import Path

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import (QLabel, QSizePolicy, QFrame, QDialog, QWidget,
                             QVBoxLayout, QPushButton, QStackedWidget)

from config import DIALOG_WIDTH, DIALOG_HEIGHT, PROCESSING_GIF_PATH