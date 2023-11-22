import sys

from PyQt5.QtWidgets import (QMainWindow, QWidget, QStyle, QApplication,
                             QHBoxLayout, QVBoxLayout)

from validation import *
from project import *
from editor import *

from config import WINDOW_HEIGHT, WINDOW_WIDTH


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mouse")
        self.setGeometry(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.create_widgets()
        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        edit_menu = menu_bar.addMenu("&Edit")

        # Create new project button
        new = file_menu.addAction("New Project")
        pixmapi = QStyle.StandardPixmap.SP_FileDialogNewFolder
        icon = self.style().standardIcon(pixmapi)
        new.setIcon(icon)
        new.triggered.connect(
            lambda: self.project_dialog.show(ProjectMode.NEW)
        )

        # Open edit view (temporary button)
        self.edit = edit_menu.addAction("Edit")
        pixmapi = QStyle.StandardPixmap.SP_LineEditClearButton
        icon = self.style().standardIcon(pixmapi)
        self.edit.setIcon(icon)
        self.edit.triggered.connect(self.editor_dialog.show)

    def create_widgets(self):
        main_layout = QHBoxLayout()

        # Components
        file_list = ImageFileList()
        image_viewer = ImageViewer()
        image_metadata_viewer = ImageMetadataViewer()

        # Dialogs
        self.project_dialog = ProjectDialog()
        self.editor_dialog = ImageEditorDialog()

        # Left side
        main_layout.addWidget(file_list, 40)

        # Right side
        right_side_layout = QVBoxLayout()
        right_side_layout.addWidget(image_viewer, 65)
        right_side_layout.addWidget(image_metadata_viewer, 35)
        main_layout.addLayout(right_side_layout, 60)

        self.central_widget.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
