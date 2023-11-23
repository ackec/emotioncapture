from PyQt5.QtWidgets import QLabel, QFrame, QDialog, QWidget, QVBoxLayout

from config import WINDOW_HEIGHT, WINDOW_WIDTH

# List of packages that are allowed to be imported
__all__ = ["ImageEditorDialog"]


class DialogPlaceHolder(QWidget):
    """ Placeholder widget while app is being developed """

    def __init__(self, name: str):
        super().__init__()

        self.main_layout = QVBoxLayout()

        text = QLabel()
        text.setText(name)
        text.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.main_layout.addWidget(text)

        self.setLayout(self.main_layout)


class ImageEditorDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edit image")
        self.setGeometry(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setModal(True)

        self.main_layout = QVBoxLayout()

        self.image = ImageEditor()
        self.main_layout.addWidget(self.image)

        self.setLayout(self.main_layout)


class ImageEditor(DialogPlaceHolder):
    def __init__(self):
        super().__init__("Image Editor")


class OverlayControls(DialogPlaceHolder):
    def __init__(self):
        super().__init__("Overlay control")


class OverlayPlot(DialogPlaceHolder):
    def __init__(self):
        super().__init__("Overlay plot")
