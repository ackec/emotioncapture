import sys, os
from enum import Enum

from PyQt5.QtWidgets import (QMainWindow, QWidget, QStyle, QApplication,
                             QHBoxLayout, QVBoxLayout, QStackedWidget)
from PyQt5 import QtCore

from validation import *
from project import *
from editor import *
from visualisation import *
from data import *

from config import WINDOW_HEIGHT, WINDOW_WIDTH

class GuiMode(Enum):
    """ Possible states of the project management. """
    MAIN = 0
    """ New project screen. """
    VISUAL = 1
    """ Processing data screen. """


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
        visualisation_menu = menu_bar.addMenu("&Visualisation")
        
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

        # Switch window to visualisation
        self.visualisation = visualisation_menu.addAction("Visualisation")
        pixmapi = QStyle.StandardPixmap.SP_LineEditClearButton
        icon = self.style().standardIcon(pixmapi)
        self.visualisation.setIcon(icon)
        #self.visualisation.triggered.connect(self.switchwindow)


    def create_widgets(self):
        main_layout = QHBoxLayout()

        # Components
        self.image_viewer = ImageViewer()
        self.file_list = ImageFileList(self.image_viewer)
        self.image_metadata_viewer = ImageMetadataViewer(self.file_list)
        
        #self.image_metadata_viewer.update_attributes(ExampleData2)

        self.image_control = ImageControl(self.file_list)
        #self.radar_plot = RadarPlot()

        # Dialogs
        self.project_dialog = ProjectDialog()
        self.editor_dialog = ImageEditorDialog()
        self.visualisation_widget = VisualisationWidget("test")

        # Left side
        main_layout.addWidget(self.file_list, 40)

        # Right side
        right_side_widget = QWidget()
        right_side_layout = QVBoxLayout()
        right_side_widget.setLayout(right_side_layout)
        right_side_layout.addWidget(self.image_viewer, 65)
        right_side_layout.addWidget(self.image_control,0,QtCore.Qt.AlignmentFlag.AlignCenter )

        # TODO MOVE to right component
        #right_side_layout.addWidget(self.radar_plot, 35)
        right_side_layout.addWidget(self.image_metadata_viewer, 35)


        self.modes = QStackedWidget()
        self.modes.addWidget(right_side_widget) # index 0
        self.modes.addWidget(self.visualisation_widget) # index 1


        main_layout.addWidget(self.modes, 60)
        self.central_widget.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
