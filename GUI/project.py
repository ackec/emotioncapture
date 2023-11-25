from enum import Enum

from pathlib import Path

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import (QLabel, QSizePolicy, QFrame, QDialog, QWidget,
                             QVBoxLayout, QPushButton, QStackedWidget)

from config import DIALOG_WIDTH, DIALOG_HEIGHT, PROCESSING_GIF_PATH

__all__ = ["ProjectDialog", "ProjectMode"]


class ProjectMode(Enum):
    """ Possible states of the project management. """
    NEW = 0
    """ New project screen. """
    PROCESS = 1
    """ Processing data screen. """
    ERROR = 2
    """ An error has occured screen. """


class DialogPlaceHolder(QWidget):
    """ Placeholder widget while app is being developed """

    def __init__(self, name: str, next: "ProjectDialog.Mode"):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout()

        text = QLabel()
        text.setText(name)
        text.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.main_layout.addWidget(text)

        btn = QPushButton("Switch")
        btn.clicked.connect(lambda: self.parent().parent().switch(next))
        self.main_layout.addWidget(btn)

        self.setLayout(self.main_layout)


class ProjectDialog(QDialog):

    titles = ["Create new project",
              "Processing data",
              "Error processing data",]

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Team Mouse")
        self.setGeometry(0, 0, DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setMinimumSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setModal(True)  # Prevent loss of focus

        self.main_layout = QVBoxLayout()

        self.modes = QStackedWidget()
        self.modes.addWidget(NewProject())
        self.modes.addWidget(Processing())
        self.modes.addWidget(ProcessingFailed())

        self.main_layout.addWidget(self.modes)
        self.setLayout(self.main_layout)

    def switch(self, mode: ProjectMode):
        self.setWindowTitle(self.titles[mode.value])
        self.modes.setCurrentIndex(mode.value)

    def show(self, mode: ProjectMode):
        self.switch(mode)
        super().show()


class NewProject(DialogPlaceHolder):
    def __init__(self):
        super().__init__("New Project", ProjectMode.PROCESS)


class Processing(QWidget):
    def __init__(self):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Animated GIF
        icon_label = QLabel(self)
        self.main_layout.addWidget(icon_label)
        self.icon_animation = QMovie(PROCESSING_GIF_PATH)
        icon_label.setMovie(self.icon_animation)
        self.icon_animation.start()

        # Text beneth GIF
        text = QLabel()
        text.setText("Processing...")
        self.main_layout.addWidget(text)

        # Temporary switch button (remove later)
        btn = QPushButton("Switch")
        btn.clicked.connect(lambda: self.parent().parent().switch(next))
        self.main_layout.addWidget(btn)

        self.setLayout(self.main_layout)

    def startStopAnimation(self):
        if self.icon_animation.state() == QMovie.MovieState.Running:
            self.icon_animation.stop()
        else:
            self.icon_animation.start()


class ProcessingFailed(DialogPlaceHolder):
    def __init__(self):
        super().__init__("Processing failed", ProjectMode.NEW)
