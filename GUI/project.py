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



# TODO 
# Remove this class
"""
class TwoInputsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Two Inputs Dialog")

        self.label = QLabel("Please type mouse name and its gender below",
                            self)

        # Create two QLineEdit widgets
        self.input1_line_edit = QLineEdit(self)
        self.input2_line_edit = QLineEdit(self)
        self.input3_line_edit = QLineEdit(self)

        # Create a QPushButton to accept the inputs
        accept_button = QPushButton("OK", self)
        accept_button.clicked.connect(self.accept)

        # Create a layout and add the widgets to it
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input1_line_edit)
        layout.addWidget(self.input2_line_edit)
        layout.addWidget(self.input3_line_edit)
        layout.addWidget(accept_button)

    def get_inputs(self):
        # Return the entered values for input1 and input2
        return (self.input1_line_edit.text(),
                self.input2_line_edit.text(),
                self.input3_line_edit.text())
"""

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

"""
class ProjectManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hidemouse = True
        self.data = None
        self.set_geometry(self.parent())

        self.btn = QPushButton("Switch")
        self.btn.clicked.connect(
            lambda: self.parent().parent().switch(ProjectMode.PROCESS)
        )

        self.btn.clicked.connect(self.parent().set_default_size)
        self.btn.clicked.connect(self.parent().inferencer.inference)

        self.create_widgets()

        self.setLayout(self.layout)

    def create_widgets(self):
        # Create widgets

        project_widget = self.create_project_selector()
        mouse_widget = self.create_mouse_selector()
        video_browser = VideoWidget()

        # Create layout
        self.layout = QVBoxLayout()

        # Add layouts
        self.layout.addLayout(project_widget)
        self.layout.addLayout(mouse_widget)
        self.layout.addWidget(video_browser)

        self.layout.addWidget(self.btn)

    def create_project_selector(self):
        # Init layout
        project_layout = QVBoxLayout()

        browser = QHBoxLayout()
        self.project_input = QLineEdit()
        label_project = QLabel("Select project below", self)
        label_or = QLabel("Or", self)
        # Set text alignment to center
        label_or.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Set text alignment to center
        label_project.setAlignment(Qt.AlignmentFlag.AlignCenter)
        browsebtn = QPushButton("Browse", self)
        browsebtn.clicked.connect(lambda: self.openFileExplorer())

        project_layout.addWidget(label_project)

        browser.addWidget(self.project_input)
        browser.addWidget(browsebtn)

        project_layout.addLayout(browser)
        project_layout.addWidget(label_or)

        create_new_project = QPushButton("Create New Project", self)
        create_new_project.clicked.connect(lambda: self.create_project())

        # TODO
        # Have project load data correctly from csv's and append to Data Classes

        project_layout.addWidget(create_new_project)

        return project_layout

    def set_geometry(self, PDialog: ProjectDialog):
        PDialog.setGeometry(100, 100, 300, 400)
        PDialog.setMinimumSize(300, 400)
        PDialog.setMaximumSize(300, 400)

    def openFileExplorer(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        print(os.getcwd())
        file_dialog.setDirectory(os.getcwd())

        # Open file explorer for selecting a directory
        directory = file_dialog.getExistingDirectory(
            self, "Select Directory", QDir.currentPath())
        if directory:

            print(f"Selected directory: {directory}")

            with open(directory+'/meta.json', 'r') as file:
                self.data = json.load(file)
                print(self.data)

            self.dropdown.clear()

            for mouse in self.data["registered_mice"]:
                if mouse["name"] is not None and mouse["gender"] is not None:
                    self.dropdown.addItem(mouse["name"])
                    self.dropdown.setCurrentIndex(-1)
                    self.name_input.setText("")
                    self.gender_input.setText("")

    def create_project(self):
        base_path = BASE_PROJECT_DIRECTORY_PATH

        # Get the directory name from the user
        project_name, ok = QInputDialog.getText(
            self, "Enter Project Name", "Project/Directory Name:")

        if ok and project_name:
            # Construct the full path
            project_path = os.path.join(base_path, project_name)

            try:
                # Create the directory
                os.makedirs(project_path)
                print(f"Directory created: {project_path}")
            except OSError as e:
                print(f"Error creating directory: {e}")

            self.project_path = project_path

            self.init_meta_data()

    def init_meta_data(self):
        meta_path = self.project_path + "/meta.json"

        project_name = str.split(self.project_path, '/')[-1]
        project_path = self.project_path

        self.data = {
            "project_name": "{project_name}".format(project_name=project_name),
            "project_path": "{project_path}".format(project_path=project_path),
            "registered_mice": [
                {
                    "name": "",
                    "gender": "",
                    "genotype": ""
                }
            ]
        }
        with open(meta_path, 'w') as file:
            json.dump(self.data, file, indent=2)

    def create_mouse_selector(self):
        label1 = QLabel("Select Mouse from below")
        # Set text alignment to center
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label2 = QLabel("Or:  create / edit one from below")
        # Set text alignment to center
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name_input = QLineEdit(self)
        self.gender_input = QLineEdit(self)
        self.genotype_input = QLineEdit(self)

        label_name = QLabel("Name")
        # label_name.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set text alignment to center

        label_gender = QLabel("Gender")
        # label_gender.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set text alignment to center

        label_genotype = QLabel("Genotype")
        # label_genotype.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set text alignment to center

        layout = QVBoxLayout()
        layout_name = QHBoxLayout()
        layout_gender = QHBoxLayout()
        layout_genotype = QHBoxLayout()

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label1)
        self.dropdown = QComboBox(self)
        self.dropdown.setCurrentIndex(-1)
        self.dropdown.currentIndexChanged.connect(
            lambda: self.update_mouse_data())
        layout.addWidget(self.dropdown)
        layout.addWidget(label2)

        layout_name.addWidget(label_name)
        layout_name.addWidget(self.name_input)

        layout_gender.addWidget(label_gender)
        layout_gender.addWidget(self.gender_input)

        layout_genotype.addWidget(label_genotype)
        layout_genotype.addWidget(self.genotype_input)

        layout.addLayout(layout_name)
        layout.addLayout(layout_gender)
        layout.addLayout(layout_genotype)

        # Add buttons for mouse selecting
        edit_buttons = QHBoxLayout()
        editbtn = QPushButton("Edit")
        editbtn.clicked.connect(lambda: self.toggle_edit_mode())
        confirm_button = QPushButton("Add Mouse")
        confirm_button.clicked.connect(lambda: self.show_input_dialog())
        edit_buttons.addWidget(editbtn)
        edit_buttons.addWidget(confirm_button)

        layout.addLayout(edit_buttons)

        self.toggle_false()

        return layout

    def toggle_edit_mode(self):

        # If toggling off, save the text input to current active mouse profile
        if self.hidemouse:
            current_index = self.dropdown.currentIndex()
            print("What am i", self.name_input.text())
            if self.name_input.text() != "" and self.gender_input.text() != "" and self.genotype_input.text() != "":
                print(self.name_input.text())
                self.data["registered_mice"][current_index]["name"] = self.name_input.text()
                self.data["registered_mice"][current_index]["gender"] = self.gender_input.text(
                )
                self.data["registered_mice"][current_index]["genotype"] = self.genotype_input.text(
                )

                self.name_input.setText(
                    self.data["registered_mice"][current_index]["name"])
                self.gender_input.setText(
                    self.data["registered_mice"][current_index]["gender"])
                self.gender_input.setText(
                    self.data["registered_mice"][current_index]["genotype"])
            else:
                print("Please fill the meta data of mouse attributes")
                return

        self.hidemouse = not (self.hidemouse)
        self.name_input.setEnabled(self.hidemouse)
        self.gender_input.setEnabled(self.hidemouse)
        self.genotype_input.setEnabled(self.hidemouse)

    def toggle_false(self):
        self.hidemouse = False
        self.name_input.setEnabled(self.hidemouse)
        self.gender_input.setEnabled(self.hidemouse)
        self.genotype_input.setEnabled(self.hidemouse)

    def update_mouse_data(self):
        if hasattr(self, 'data'):
            current_index = self.dropdown.currentIndex()
            self.name_input.setText(
                self.data["registered_mice"][current_index]["name"])
            self.gender_input.setText(
                self.data["registered_mice"][current_index]["gender"])
            self.genotype_input.setText(
                self.data["registered_mice"][current_index]["genotype"])
        else:
            return

    def save_mouse(self):

        new = {"name": '{name}'.format(name=self.name_input.text()), "gender": '{gender}'.format(gender=self.gender_input.text()),
               "genotype": '{genotype}'.format(name=self.genotype_input.text())}
        self.data["registered_mice"].append(new)
        self.dropdown.addItem(self.name_input.text())
        self.dropdown.setCurrentIndex(-1)
        self.update_mouse_data()

    def validate_dropdown(self):
        if hasattr(self, 'data'):
            items_text = [self.dropdown.itemText(
                i) for i in range(self.comboBox.count())]

    def show_input_dialog(self):
        # Create an instance of the custom dialog
        dialog = TwoInputsDialog(self)

        # Show the dialog and get the results
        result = dialog.exec_()

        # Check if the user clicked OK
        if result == QDialog.Accepted:
            self.new_mouse, self.new_gender, self.new_genotype = dialog.get_inputs()
            new = {"name": '{name}'.format(name=self.new_mouse), "gender": '{gender}'.format(gender=self.new_gender),
                   "genotype": '{genotype}'.format(genotype=self.new_genotype)}
            self.data["registered_mice"].append(new)
            self.dropdown.addItem(self.new_mouse)
            self.dropdown.setCurrentIndex(-1)
            self.update_mouse_data()
"""

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
        time.sleep(2)
        self.main.inferencer.inference(self.main.project.inference_data)
        print("inference done")
        self.close()



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
