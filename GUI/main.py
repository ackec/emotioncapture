import sys, os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QStyle, QApplication,
                             QHBoxLayout, QVBoxLayout)

from validation import *
from project import *
from editor import *
from visualisation import RadarPlot

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
        
        ##  Temp menu to test functions (To be removed)
        tempMenu = menu_bar.addMenu("&Temp")
        
        load_folder = tempMenu.addAction("Select Folder")
        load_folder.triggered.connect(self.file_list.select_folder)
        ##
        
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
        self.edit.triggered.connect(lambda: self.editor_dialog.show(None))

    def create_widgets(self):
        main_layout = QHBoxLayout()

        # Components
        self.image_viewer = ImageViewer()
        self.file_list = ImageFileList(self.image_viewer)
        self.image_metadata_viewer = ImageMetadataViewer()
        self.image_control = ImageControl(self.file_list)
        self.radar_plot = RadarPlot()

        # Dialogs
        self.project_dialog = ProjectDialog()
        self.editor_dialog = ImageEditorDialog()

        # Left side
        main_layout.addWidget(self.file_list, 40)

        # Right side
        right_side_layout = QVBoxLayout()
        right_side_layout.addWidget(self.image_viewer, 65)
        right_side_layout.addWidget(self.image_control)

        # TODO MOVE to right component
        right_side_layout.addWidget(self.radar_plot, 35)
        right_side_layout.addWidget(self.image_metadata_viewer, 35)
        main_layout.addLayout(right_side_layout, 60)

        self.central_widget.setLayout(main_layout)

            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
