from enum import Enum

from PyQt5.QtCore import Qt, QSize, QDir
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtWidgets import (QLabel, QSizePolicy, QFrame, QDialog, QWidget,
                             QVBoxLayout, QPushButton, QStackedWidget, QLineEdit,
                             QHBoxLayout, QFileDialog, QInputDialog, QComboBox)

from config import DIALOG_WIDTH, DIALOG_HEIGHT, RESOURCE_PATH, BASE_PROJECT_DIRECTORY_PATH

from main import MainWindow

import os
import json

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

        #text = QLabel()
        #text.setText(name)
        #text.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        #self.main_layout.addWidget(text)

        self.btn = QPushButton("Switch")
        self.btn.clicked.connect(lambda: self.parent().parent().switch(next))
        #self.main_layout.addWidget(btn)

        #self.setLayout(self.main_layout)


class ProjectDialog(QDialog):

    titles = ["Create new project",
              "Processing data",
              "Error processing data",]

    def __init__(self, main_window: MainWindow):
        super().__init__()
        self.main = main_window
        self.setWindowTitle("Team Mouse")
        #self.setGeometry(0, 0, DIALOG_WIDTH, DIALOG_HEIGHT)
        #self.setMinimumSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.set_default_size
        self.setModal(True)  # Prevent loss of focus

        self.main_layout = QVBoxLayout()

        self.modes = QStackedWidget()
        self.modes.addWidget(ProjectManager(self))
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

        
    def set_default_size(self):
        self.setGeometry(100, 100, DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setMinimumSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setMaximumSize(5000, 5000)

class TwoInputsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Two Inputs Dialog")

        self.label = QLabel("Please type mouse name and its gender below", self)

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
        return self.input1_line_edit.text(), self.input2_line_edit.text(),  self.input3_line_edit.text()
    

    
class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.videopath = None

        layout = QHBoxLayout()
        # Create two QLineEdit widgets
        label = QLabel("Select MP4 video")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set text alignment to center
        self.input1_line_edit = QLineEdit()
        self.input1_line_edit.setEnabled(False)
        browsebtn =  QPushButton("Browse")
        browsebtn.clicked.connect(lambda: self.get_video_path())

        # Create a layout and add the widgets to it
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.input1_line_edit)
        layout.addWidget(browsebtn)

    

    def get_video_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)

        file_dialog.setDirectory(os.getcwd())

        # Open file explorer for selecting a directory
        file_name = file_dialog.getOpenFileName(self, "Select Video", "", "*.mp4")
        if file_name:
            print(file_name)
            self.videopath = file_name[0]
            print("Selected file: ", self.videopath)
        
            self.show_input()
        else:
            OSError("Video must be a mp4")

    def show_input(self):
        if self.videopath:
            self.input1_line_edit.setText(self.videopath)


class ProjectManager(DialogPlaceHolder):
    def __init__(self, PDialog: ProjectDialog):
        super().__init__("New Project", ProjectMode.PROCESS)
        self.hidemouse = True
        self.data = None
        self.Dialog = PDialog
        self.set_geometry(self.Dialog)

        self.btn.clicked.connect(lambda: PDialog.set_default_size())
        self.btn.clicked.connect(lambda: PDialog.main.inferencer.inference())

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
        label_or.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set text alignment to center
        label_project.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set text alignment to center
        browsebtn =  QPushButton("Browse", self)
        browsebtn.clicked.connect(lambda: self.openFileExplorer())

        project_layout.addWidget(label_project)

        browser.addWidget(self.project_input)
        browser.addWidget(browsebtn)

        project_layout.addLayout(browser)
        project_layout.addWidget(label_or)

        create_new_project =  QPushButton("Create New Project", self)
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
        directory = file_dialog.getExistingDirectory(self, "Select Directory", QDir.currentPath())
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
        project_name, ok = QInputDialog.getText(self, "Enter Project Name", "Project/Directory Name:")

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
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set text alignment to center

        label2 = QLabel("Or:  create / edit one from below")
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set text alignment to center

        self.name_input = QLineEdit(self)
        self.gender_input = QLineEdit(self)
        self.genotype_input = QLineEdit(self)

        label_name = QLabel("Name")
        #label_name.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set text alignment to center

        label_gender = QLabel("Gender")
        #label_gender.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set text alignment to center

        label_genotype = QLabel("Genotype")
        #label_genotype.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Set text alignment to center

        layout = QVBoxLayout()
        layout_name = QHBoxLayout()
        layout_gender = QHBoxLayout()
        layout_genotype = QHBoxLayout()

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label1)
        self.dropdown = QComboBox(self)
        self.dropdown.setCurrentIndex(-1)
        self.dropdown.currentIndexChanged.connect(lambda: self.update_mouse_data())
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
        editbtn =  QPushButton("Edit")
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
                self.data["registered_mice"][current_index]["gender"] = self.gender_input.text()
                self.data["registered_mice"][current_index]["genotype"] = self.genotype_input.text()

                self.name_input.setText(self.data["registered_mice"][current_index]["name"])
                self.gender_input.setText(self.data["registered_mice"][current_index]["gender"])
                self.gender_input.setText(self.data["registered_mice"][current_index]["genotype"])
            else:
                print("Please fill the meta data of mouse attributes")
                return


        self.hidemouse = not(self.hidemouse)
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
            self.name_input.setText(self.data["registered_mice"][current_index]["name"])
            self.gender_input.setText(self.data["registered_mice"][current_index]["gender"])
            self.genotype_input.setText(self.data["registered_mice"][current_index]["genotype"])
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
            items_text = [self.dropdown.itemText(i) for i in range(self.comboBox.count())]

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


    
class Processing(QWidget):
    def __init__(self):
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


class ProcessingFailed(DialogPlaceHolder):
    def __init__(self):
        super().__init__("Processing failed", ProjectMode.NEW)
