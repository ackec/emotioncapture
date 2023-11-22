from enum import Enum

from PyQt5.QtWidgets import (QLabel, QSizePolicy, QFrame, QDialog, QWidget,
                             QVBoxLayout, QPushButton)

from config import DIALOG_WIDTH, DIALOG_HEIGHT

__all__ = ["ProjectDialog", "ProjectMode"]


class ProjectMode(Enum):
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
        btn.clicked.connect(lambda: self.parent().switch(next))
        self.main_layout.addWidget(btn)

        self.setLayout(self.main_layout)


class ProjectDialog(QDialog):

    # TODO: Use a QStackedWidget instead

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
        self.displayed_widget = QWidget()
        self.main_layout.addWidget(self.displayed_widget)
        self.setLayout(self.main_layout)

    def switch(self, mode: ProjectMode, **kwargs):
        if mode == ProjectMode.NEW:
            new_widget = NewProject(**kwargs)
        elif mode == ProjectMode.PROCESS:
            new_widget = Processing(**kwargs)
        elif mode == ProjectMode.ERROR:
            new_widget = ProcessingFailed(**kwargs)
        else:
            raise ValueError("Incorrect mode supplied.")

        self.setWindowTitle(self.titles[mode.value])
        self.main_layout.replaceWidget(self.displayed_widget, new_widget)
        self.displayed_widget.setParent(None)
        self.displayed_widget = new_widget

    def show(self, mode: ProjectMode):
        self.switch(mode)
        super().show()


class NewProject(DialogPlaceHolder):
    def __init__(self):
        super().__init__("New Project", ProjectMode.PROCESS)


class Processing(DialogPlaceHolder):
    def __init__(self):
        super().__init__("Processing", ProjectMode.ERROR)


class ProcessingFailed(DialogPlaceHolder):
    def __init__(self):
        super().__init__("Processing failed", ProjectMode.NEW)
