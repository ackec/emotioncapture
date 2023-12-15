import sys
import os
from enum import Enum
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/lib/x86_64-linux-gnu/qt5/plugins'
from PyQt5.QtWidgets import (QMainWindow, QWidget, QStyle, QApplication,
                             QHBoxLayout, QVBoxLayout, QStackedWidget)
from PyQt5 import QtCore

from validation import *
from project import *
from editor import *
from visualisation import VisualisationWidget1, VisualisationWidget2
from data import *
from tree_view import *

from config import WINDOW_HEIGHT, WINDOW_WIDTH

from inference import *

class GuiMode(Enum):
    """ Possible states of the project management. """
    MAIN = 0
    """ New project screen. """
    VISUAL = 1
    """ Processing data screen. """

# TODO
# Create inferencer class elsewhere


class tempInferencer():
    def inference(self):
        print("Start inference")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # TODO
        # Fix this because it gives a circular import

        self.project = ProjectData()

        ## TODO remove this ##
        #mouce = MouseData()
        #mouce.name = "mouse1"
        #self.project.mice.append(mouce)
        #self.project.active_mouse_index = 0
        #videopath = "converted_videos/M3N-2021-09-23 10-00-56.mp4"
        ###########################
        
        ## And move this #########
        self.inferencer = Inferencer(self.project)
        # self.inferencer.inference(videopath)
        ###########################

        #self.project = example_project()

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

        # Temp menu to test functions (To be removed)
        tempMenu = menu_bar.addMenu("&Temp")

        load_folder = tempMenu.addAction("Select Folder")
        load_folder.triggered.connect(self.file_list.select_folder)

         
        pixmapi = QStyle.StandardPixmap.SP_FileDialogNewFolder
        icon = self.style().standardIcon(pixmapi)

        # Create new project button
        newnew = file_menu.addAction("New Project")
        newnew.setIcon(icon)
        newnew.triggered.connect(
            lambda: self.new_project_dialog.show()
        )

                # Create new project button
        newnew = file_menu.addAction("Open Project")
        newnew.setIcon(icon)
        newnew.triggered.connect(
            lambda: open_directory_dialog(self.project)
        )

        # Create Add Mouse to project button
        newnew = file_menu.addAction("Add Mouse to Project")
        newnew.setIcon(icon)
        newnew.triggered.connect(
            lambda: self.new_mouse_dialog.show()
        )

        # Create new project button
        new = file_menu.addAction("New Data")
        #pixmapi = QStyle.StandardPixmap.SP_FileDialogNewFolder
        #icon = self.style().standardIcon(pixmapi)
        new.setIcon(icon)
        new.triggered.connect(
            lambda: self.project_dialog.show(ProjectMode.NEW)
        )

        

        # Open edit view (temporary button)
        self.edit = edit_menu.addAction("Edit")
        pixmapi = QStyle.StandardPixmap.SP_LineEditClearButton
        icon = self.style().standardIcon(pixmapi)
        self.edit.setIcon(icon)
        self.edit.triggered.connect(
            lambda: self.editor_dialog.show(self.project.images[0]))

        # Switch window to visualisation HDBSCAN
        self.visualisation = visualisation_menu.addAction("Visualisation HDBSCAN")
        pixmapi = QStyle.StandardPixmap.SP_LineEditClearButton
        icon = self.style().standardIcon(pixmapi)
        self.visualisation.setIcon(icon)
        self.visualisation.triggered.connect(self.switchwindowHDBSCAN)

        # Switch window to visualisation Kmeans
        self.visualisation = visualisation_menu.addAction("Visualisation kmeans")
        pixmapi = QStyle.StandardPixmap.SP_LineEditClearButton
        icon = self.style().standardIcon(pixmapi)
        self.visualisation.setIcon(icon)
        self.visualisation.triggered.connect(self.switchwindowKmeans)

        # Switch window to main
        self.visualisation = visualisation_menu.addAction("Main")
        pixmapi = QStyle.StandardPixmap.SP_LineEditClearButton
        icon = self.style().standardIcon(pixmapi)
        self.visualisation.setIcon(icon)
        self.visualisation.triggered.connect(self.switchwindowMain)


    def create_widgets(self):
        main_layout = QHBoxLayout()

        # Components
        self.image_viewer = ImageViewer()
        self.file_list = FileList(self,self.image_viewer)
        self.image_metadata_viewer = ImageMetadataViewer(self.file_list)

        #self.image_metadata_viewer.update_attributes(self.project)

        self.image_control = ImageControl(self.file_list)

        # Dialogs
        self.project_dialog = ProjectDialog(self)
        self.new_project_dialog = NewProject(self)
        self.new_mouse_dialog = MouseCreator(self)
        self.editor_dialog = ImageEditorDialog()
        self.visualisation_widget = QWidget()
        
        #self.visualisation_widget1 = VisualisationWidget1(self.project,self.file_list)
        #self.visualisation_widget2 = VisualisationWidget2(self.project, self.file_list)

        # Left side
        main_layout.addWidget(self.file_list, 40)

        # Right side
        right_side_widget = QWidget()
        right_side_layout = QVBoxLayout()
        right_side_widget.setLayout(right_side_layout)
        right_side_layout.addWidget(self.image_viewer, 65)
        right_side_layout.addWidget(self.image_control, 0,
                                    QtCore.Qt.AlignmentFlag.AlignCenter)
        right_side_layout.addWidget(self.image_metadata_viewer, 35)

        # Stack
        self.modes = QStackedWidget()
        self.modes.addWidget(right_side_widget)  # index 0
        self.modes.addWidget(self.visualisation_widget1)  # index 1
        self.modes.addWidget(self.visualisation_widget2)  # index 2

        main_layout.addWidget(self.modes, 60)
        self.central_widget.setLayout(main_layout)

    def switchwindowHDBSCAN(self):
        if self.modes.currentIndex() == 0:
            print("switch 1")
            self.modes.setCurrentIndex(1)
        elif self.modes.currentIndex() == 2:
            print("switch 2")
            self.modes.setCurrentIndex(1)

    def switchwindowKmeans(self):
        if self.modes.currentIndex() == 0:
            print("switch 1")
            self.modes.setCurrentIndex(2)
        elif self.modes.currentIndex() == 1:
            print("switch 2")
            self.modes.setCurrentIndex(2)
    
    def switchwindowMain(self):
        if self.modes.currentIndex() == 1:
            print("switch 1")
            self.modes.setCurrentIndex(0)
        elif self.modes.currentIndex() == 2:
            print("switch 2")
            self.modes.setCurrentIndex(0)
        
        #if self.modes.currentIndex() == 0:
        #    print("switch 1")
        #    self.modes.setCurrentIndex(1)
        #elif self.modes.currentIndex() == 1:
        #    print("switch 2")
        #    self.modes.setCurrentIndex(0)
            #self.mouse.init_visualisation(self.project)
            #self.lineinit_line_plot()


def example_project():
    project = ProjectData()
    project.name = "Project Example 1"
    project.path = "project_path"

    mouse = MouseData(project)
    mouse.gender = "male"
    mouse.name = "Anonymouse"
    project.mice = [mouse]

    image = MouseImageData()
    image.mouse = mouse
    image.filename = "F3H.jpg"
    image.path = "F3H.jpg"
    image.key_point_conf = 0.89
    image.profile_conf = 0.97
    project.images = [image]

    # key_points = KeyPoints()
    # key_points.ear_back = (815, 334)
    # key_points.ear_front = (722, 461)
    # key_points.ear_bottom = (791, 427)
    # key_points.ear_top = (727, 372)
    # key_points.eye_back = (590, 458)
    # key_points.eye_front = (544, 459)
    # key_points.eye_bottom = (566, 478)
    # key_points.eye_top = (571, 436)
    # key_points.nose_top = (417, 473)
    # key_points.nose_bottom = (423, 506)
    # key_points.mouth = (486, 568)
    # image.key_points = key_points

    
    
    return project


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #example = example_project()
    ex = MainWindow()
    #ex.project = example
    #ex.file_list.update_file_list()
    ex.show()
    sys.exit(app.exec())
