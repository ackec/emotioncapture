import os
import json

from enum import Enum
import typing
from PyQt5 import QtGui

from PyQt5.QtCore import Qt, QSize, QDir
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtWidgets import (QLabel, QSizePolicy, QDialog, QWidget,
                             QVBoxLayout, QPushButton, QStackedWidget,
                             QLineEdit, QHBoxLayout, QFileDialog, QInputDialog,
                             QComboBox)

from config import (DIALOG_WIDTH, DIALOG_HEIGHT, RESOURCE_PATH,
                    BASE_PROJECT_DIRECTORY_PATH)

from main import MainWindow

from utilities import *

import os
import json

import time

__all__ = ["ProjectDialog", "ProjectMode", "NewProject", "MouseCreator", "NewData", "open_directory_dialog"]





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

        # text = QLabel()
        # text.setText(name)
        # text.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        # self.main_layout.addWidget(text)

        self.btn = QPushButton("Switch")
        self.btn.clicked.connect(lambda: self.parent().parent().switch(next))
        # self.main_layout.addWidget(btn)

        # self.setLayout(self.main_layout)


class ProjectDialog(QDialog):

    titles = ["Create new project",
              "Processing data",
              "Error processing data",]

    def __init__(self, main: MainWindow):
        super().__init__()
        self.setWindowTitle("Team Mouse")
        # self.setGeometry(0, 0, DIALOG_WIDTH, DIALOG_HEIGHT)
        # self.setMinimumSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.set_default_size
        self.setModal(True)  # Prevent loss of focus

        self.main = main

        self.main_layout = QVBoxLayout()

        self.modes = QStackedWidget()
        self.modes.addWidget(NewData(self))
        self.modes.addWidget(Processing(self.main))
        self.modes.addWidget(ProcessingFailed())

        self.main_layout.addWidget(self.modes)
        self.setLayout(self.main_layout)

    def switch(self, mode: ProjectMode):
        self.setWindowTitle(self.titles[mode.value])
        self.modes.setCurrentIndex(mode.value)

    def show(self, mode: ProjectMode):
        self.switch(mode)
        super().show()

    # currently not implemented
    def startInference(self, mode: ProjectMode):
        self.switch(mode)
        super().show()


    def set_default_size(self):
        self.setGeometry(100, 100, DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setMinimumSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setMaximumSize(5000, 5000)



class VideoWidget(QWidget):
    def __init__(self, projectdata, btn):
        super().__init__()

        self.start = btn
        self.project = projectdata

        self.videopath = None

        layout = QHBoxLayout()
        # Create two QLineEdit widgets
        label = QLabel("Select video or images")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set text alignment to center
        self.input1_line_edit = QLineEdit()
        self.input1_line_edit.setEnabled(False)
        browsebtn = QPushButton("Browse")
        browsebtn.clicked.connect(lambda: self.get_video_path())

        # Create a layout and add the widgets to it
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.input1_line_edit)
        layout.addWidget(browsebtn)

    def get_video_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.Option.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)

        file_dialog.setDirectory(os.getcwd())

        file_filter = "Video Files (*.mp4);;Image Files (*.png *.jpg *.jpeg)"

        # Open file explorer for selecting a directory
        file_names, _ = file_dialog.getOpenFileNames(self, "Select Files", "", file_filter)
        if file_names:
            #print(file_names)
            self.videopath = file_names
            print("Selected file: ", self.videopath)
            self.show_input()
            if self.project.active_mouse_index:
                self.start.setEnabled(True)
            self.videopath = self.videopath[0]
            #print(self.videopath)

            self.project.inference_data.append(self.videopath)
        else:
            OSError("Video must be a mp4")

    def show_input(self):
        if self.videopath:
            self.input1_line_edit.setText(self.videopath[0])



class MouseSelector(QComboBox):
    def __init__(self, projectdata: ProjectData):
        super().__init__()
        self.project = projectdata

        self.update()

        self.currentIndexChanged.connect(lambda: self.update_active_mouse_index())

    def update_active_mouse_index(self):
        self.project.active_mouse_index = self.currentIndex()
        print("Selected Mouse: ", self.project.mice[self.project.active_mouse_index].name)

    def update(self):

        self.clear()

        if self.project.active_mouse_index is None:
            self.setCurrentIndex(-1)
        else:
            self.setCurrentIndex(self.project.active_mouse_index)

        if len(self.project.mice) > 0:
            for mouse in self.project.mice:
                self.addItem(mouse.name)


class ProjectInformation(QWidget):
    def __init__(self, projectdata: ProjectData):
        super().__init__()

        self.project = projectdata
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text = QLabel("Project information")
        self.name = QLabel(projectdata.name)
        self.path = QLabel(projectdata.path)

        self.main_layout.addWidget(text)
        self.main_layout.addWidget(self.name)
        self.main_layout.addWidget(self.path)
        #self.setWindowTitle("Team Mouse")

    def update(self):
        self.name.setText(self.project.name)
        self.path.setText(self.project.path)


class NewData(DialogPlaceHolder):
    def __init__(self, PDialog: ProjectDialog):
        super().__init__("New Project", ProjectMode.PROCESS)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.dialog = PDialog
        self.set_geometry(self.dialog)

        self.project_info = ProjectInformation(self.dialog.main.project)
        self.mouse_selector = MouseSelector(self.dialog.main.project)
        self.video_widget = VideoWidget(self.dialog.main.project, self.btn)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.project_info)
        self.layout.addWidget(self.mouse_selector)
        self.layout.addWidget(self.video_widget)
        self.layout.addWidget(self.btn)

        self.setLayout(self.layout)

    
    def set_geometry(self, PDialog: ProjectDialog):
        PDialog.setGeometry(100, 100, 300, 400)
        PDialog.setMinimumSize(300, 400)
        PDialog.setMaximumSize(300, 400)

    def update_params(self):
        self.project_info.update()
        self.mouse_selector.update()
        self.video_widget.update()

    def showEvent(self, event):
        # Override the showEvent method to update parameters when the dialog is shown
        #parameter_value = "New Value"  # Replace with your updated parameter value
        #self.update_parameters(parameter_value)
        #print(self.dialog.main.project.mice)
        self.update_params()
        super().showEvent(event)

class Processing(QWidget):
    def __init__(self, main: MainWindow):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Animated GIF
        icon_label = QLabel(self)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(icon_label)
        icon_animation = QMovie(RESOURCE_PATH + '/mouse.gif')
        icon_label.setMovie(icon_animation)
        icon_label.setScaledContents(True)
        icon_animation.start()
        icon_animation.setScaledSize(QSize(160, 160))

        # Text beneath GIF
        text = QLabel()
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont('Arial', 12)
        text.setStyleSheet("color: #404040")
        text.setFont(font)
        text.setText("Processing...")
        self.main_layout.addWidget(text)

        self.setLayout(self.main_layout)

        self.main = main


    # TODO
    # Fix this so that it changes screen before
    def showEvent(self, event):
        print("Start inference")
        super().showEvent(event)
        self.main.inferencer.inference(self.main.project.inference_data)
        self.main.file_list.update_file_list()
        print("inference done")
        #self.close()



class ProcessingFailed(DialogPlaceHolder):
    def __init__(self):
        super().__init__("Processing failed", ProjectMode.NEW)



class NewProject(QDialog):
    def __init__(self, main: MainWindow):
        super().__init__()

        # 
        self.mainwindow = main

        #print(self.mainwindow.Project)

        # Set window parameters
        self.setWindowTitle("Create New Project")
        
        self.set_size()

        # Create widgets
        text = QLabel("Enter name of project")
        text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input = QLineEdit(self)
        accept_button = QPushButton("Create Project", self)
        accept_button.clicked.connect(self.accept)

        # Create layout
        layout = QVBoxLayout(self)
        
        # Add widgets to layout
        layout.addWidget(text)
        layout.addWidget(self.input)
        layout.addWidget(accept_button)

        # Set layout
        self.setLayout(layout)


    def set_size(self):
        """
            Set window geometry
        """
        self.setGeometry(100, 100, 200, 300)
        self.setMinimumSize(200, 300)
        self.setMaximumSize(200, 300)


    def get_inputs(self):
        """
            Get user input text from QLineEdit
        """
        return self.input.text()
    

    
    def show(self):
        """
            Open window and wait for input of project name from user
            Create project with given projectname
        """
        #print(str.join())
        result = self.exec_()
        if result == QDialog.Accepted:
            project_name = self.get_inputs()
            print("project name: ", project_name)
            if project_name != "":
                project_path = os.path.join(BASE_PROJECT_DIRECTORY_PATH, project_name)
                print("projectpath=", project_path)
                if os.path.exists(project_path):
                    print("Project with that name already exists")
                else:
                    create_project(self.mainwindow.project, project_path)
                    print("Created new project at: ", project_path)

    
class MouseCreator(QDialog):
    def __init__(self, main: MainWindow):
        super().__init__()

        self.mainwindow = main

        # Set window parameters
        self.setWindowTitle("Add new mouse")
        self.set_size()

        text = QLabel("Add new mouse to project by filling the inputs below")

        text_name = QLabel("Mouse name: ")
        self.input_name = QLineEdit()
        #text_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #text_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text_gender = QLabel("Mouse gender: ")
        self.input_gender = QLineEdit()
        #text_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #text_gender.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text_genotype = QLabel("Mouse genotype")
        self.input_genotype = QLineEdit()
        #text_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #text_genotype.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        accept_button = QPushButton("Add Mouse", self)
        accept_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout_name = QHBoxLayout()
        layout_gender = QHBoxLayout()
        layout_genotype = QHBoxLayout()

        layout_name.addWidget(text_name)
        layout_name.addWidget(self.input_name)

        layout_gender.addWidget(text_gender)
        layout_gender.addWidget(self.input_gender)

        layout_genotype.addWidget(text_genotype)
        layout_genotype.addWidget(self.input_genotype)

        layout.addWidget(text)
        layout.addLayout(layout_name)
        layout.addLayout(layout_gender)
        layout.addLayout(layout_genotype)
        layout.addWidget(accept_button)

        self.setLayout(layout)


    def set_size(self):
        """
            Set window geometry
        """
        self.setGeometry(100, 100, 200, 300)
        self.setMinimumSize(200, 300)
        self.setMaximumSize(200, 300)

    def get_inputs(self):
        """
            Get user input texts from QLineEdit
        """
        return self.input_name.text(), self.input_gender.text(), self.input_genotype.text()
    
    def check_if_project(self):
        if self.mainwindow.project.name != "":
            return True
        else:
            return False
    
    def check_validity_of_name(self, name: str):
        registered_mice = self.mainwindow.project.mice
        if len(registered_mice) <= 1:
            return True

        for mouse in registered_mice:
            if mouse.name == name:
                return False
    


    def show(self):
        """
            Open window and wait for input of project name from user
            Create project with given projectname
        """
        #print(str.join())
        if self.mainwindow.project.name != "":
            result = self.exec_()
            if result == QDialog.Accepted:
                name, gender, genotype = self.get_inputs()
                #print("project name: ", project_name)
                if name != "" and gender != "" and genotype != "":
                    if self.check_validity_of_name(name):
                        add_mouse(self.mainwindow.project, name, gender, genotype)
                    else:
                        print("Mouse with that name already exists, please enter a non existing name")



def open_directory_dialog(project: ProjectData):
    # Open the directory dialog
    dir_dialog = QFileDialog()
    
    # Set the file mode to show only directories
    dir_dialog.setDirectory(os.getcwd())
    dir_dialog.setFileMode(QFileDialog.DirectoryOnly)

    # Show the dialog and get the selected directory
    selected_directory = dir_dialog.getExistingDirectory(None, 'Select Directory', '', QFileDialog.ShowDirsOnly)

    # Check if a directory was selected
    if selected_directory:
        print(f'Selected Directory: {selected_directory}')
        load_project(project, selected_directory)
