import sys
import pandas as pd
import os
from enum import Enum
from inference import * #Important, must be before qt imports
# os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/lib/x86_64-linux-gnu/qt5/plugins'
from PyQt5.QtWidgets import (QMainWindow, QWidget, QStyle, QApplication,
                             QHBoxLayout, QVBoxLayout, QStackedWidget)
from PyQt5 import QtCore

from validation import *
from project import *
from editor import *
from visualisation import VisualisationWidget
from data import *
from tree_view import *

from config import WINDOW_HEIGHT, WINDOW_WIDTH


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
        #self.project.project_data  = pd.read_csv("detected_keypoints.csv")
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
        file_menu.setToolTipsVisible(True)
        visualisation_menu = menu_bar.addMenu("&Visualisation")
        visualisation_menu.setToolTipsVisible(True)
         
        
        # Create new project button
        newnew = file_menu.addAction("New Project")
        pixmapi = QStyle.StandardPixmap.SP_FileDialogNewFolder
        icon = self.style().standardIcon(pixmapi)
        newnew.setIcon(icon)
        newnew.triggered.connect(
            lambda: self.new_project_dialog.show()
        )
        newnew.setToolTip("Create a new blank project.")
        
        # Create open project button
        open = file_menu.addAction("Open Project")
        pixmapi = QStyle.StandardPixmap.SP_DirOpenIcon
        icon = self.style().standardIcon(pixmapi)
        open.setIcon(icon)
        open.triggered.connect(
            lambda: open_directory_dialog(self.project, self.file_list)
        )
        open.setToolTip("Open an existing project.")
        
        # Create save project button
        save = file_menu.addAction("Save Project")
        pixmapi = QStyle.StandardPixmap.SP_DialogSaveButton
        icon = self.style().standardIcon(pixmapi)
        save.setIcon(icon)
        save.triggered.connect(
            lambda: self.save_project()
        )
        save.setToolTip("Save project changes.")
        
        # Create Add Mouse to project button
        add = file_menu.addAction("Add Mouse to Project")
        pixmapi = QStyle.StandardPixmap.SP_FileIcon
        icon = self.style().standardIcon(pixmapi)
        add.setIcon(icon)
        add.triggered.connect(
            lambda: self.new_mouse_dialog.show()
        )
        add.setToolTip("Create and add a mouse to current project.")

        # Create new data button
        newdata = file_menu.addAction("New Data")
        pixmapi = QStyle.StandardPixmap.SP_FileIcon
        icon = self.style().standardIcon(pixmapi)
        newdata.setIcon(icon)
        newdata.triggered.connect(
            lambda: self.project_dialog.show(ProjectMode.NEW)
        )
        newdata.setToolTip("Add pictures or videos to a mouse.")

        
        # Switch window to visualisation HDBSCAN
        hdbscan = visualisation_menu.addAction("Visualisation HDBSCAN")
        pixmapi = QStyle.StandardPixmap.SP_FileDialogInfoView
        icon = self.style().standardIcon(pixmapi)
        hdbscan.setIcon(icon)
        hdbscan.triggered.connect(self.switchwindowHDBSCAN)
        hdbscan.setToolTip("Visualise results using HDBSCAN clustering.")

        # Switch window to visualisation Kmeans
        kmeans = visualisation_menu.addAction("Visualisation kmeans")
        pixmapi = QStyle.StandardPixmap.SP_FileDialogInfoView
        icon = self.style().standardIcon(pixmapi)
        kmeans.setIcon(icon)
        kmeans.triggered.connect(self.switchwindowKmeans)
        kmeans.setToolTip("Visualise results using kmeans clustering.")

        # Switch window to main
        main_return = visualisation_menu.addAction("Main")
        pixmapi = QStyle.StandardPixmap.SP_ArrowBack
        icon = self.style().standardIcon(pixmapi)
        main_return.setIcon(icon)
        main_return.triggered.connect(self.switchwindowMain)
        main_return.setToolTip("Return to standard interface.")
        
        # Update visualisation data
        reload = visualisation_menu.addAction("Reload visualisation data")
        pixmapi = QStyle.StandardPixmap.SP_BrowserReload
        icon = self.style().standardIcon(pixmapi)
        reload.setIcon(icon)
        reload.triggered.connect(self.reload_visualisation_data)
        reload.setToolTip("Recompute feature value incase user has changed keypoint locations.")

    def save_project(self):
    
        data = self.project.project_data
        
        if data is not None:
            csv_path = os.path.join(self.project.path, "detected_keypoints.csv")
            data.to_csv(csv_path,index=False)
        
    
    def create_widgets(self):
        main_layout = QHBoxLayout()

        # Components
        self.image_viewer = ImageViewer()
        self.file_list = FileList(self,self.image_viewer)
        self.image_metadata_viewer = ImageMetadataViewer(self.file_list)

        #self.image_metadata_viewer.update_attributes(self.project)

        self.image_control = ImageControl(self.file_list, self.image_metadata_viewer)

        # Dialogs
        self.project_dialog = ProjectDialog(self)
        self.new_project_dialog = NewProject(self, self.file_list)
        self.new_mouse_dialog = MouseCreator(self)
        self.editor_dialog = ImageEditorDialog()
        self.visualisation_widget = VisualisationWidget(self.file_list)
        # self.visualisation_widget = VisualisationWidget2(self.file_list)

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
        self.modes.addWidget(self.visualisation_widget)  # index 1
        # self.modes.addWidget(self.visualisation_widget)  # index 2

        main_layout.addWidget(self.modes, 60)
        self.central_widget.setLayout(main_layout)


    def switchwindowHDBSCAN(self):
        if self.project.project_data is None or self.project.project_data.empty:
            print("Error, no data in dataframe")
            return
        if self.visualisation_widget.has_init:
            self.visualisation_widget.change_cluster(0)
        else:
            self.visualisation_widget.init_visualisation(self.project, 0)

        self.modes.setCurrentIndex(1)
        print("switch to HDBSCAN")

    def switchwindowKmeans(self):
        if self.project.project_data is None or self.project.project_data.empty:
            print("Error, no data in dataframe")
            return

        if self.visualisation_widget.has_init:
            self.visualisation_widget.change_cluster(1)
        else:
            self.visualisation_widget.init_visualisation(self.project, 1)
        self.modes.setCurrentIndex(1)
        print("switch to K-means")

    def switchwindowMain(self):
        self.modes.setCurrentIndex(0)
        print("switch to validation")

    def reload_visualisation_data(self):
        if self.project.project_data is None or self.project.project_data.empty:
            print("Error, no data in dataframe")
            return
        
        self.visualisation_widget
        self.visualisation_widget.init_visualisation(self.project, 0)
        self.modes.setCurrentIndex(1)
        print("Reloaded dataframe")



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
