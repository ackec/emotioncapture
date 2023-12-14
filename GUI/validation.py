from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QPen
from PyQt5.QtCore import Qt, QSize
import tkinter
from tkinter import filedialog
import os
import  re
import numpy as np

from data import *

# List of packages that are allowed to be imported
__all__ = ["ImageMetadataViewer", "ImageControl",
           "ImageViewer", "ImageFileList"]


class PlaceHolder(QLabel):
    """ Placeholder widget while app is being developed """

    def __init__(self, name: str, parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setText(name)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

class ImageFileList(QListWidget):
    def __init__(self, main,image_viewer):
        super().__init__()  # "Image File list"
        self.main_window = main
        self.image_viewer = image_viewer
        self.current_index = 0
        self.pictures = []

       # self.setSortingEnabled(True)
 
        # Allowed file extensions for loading images
        # Find better way to check if image or not (?)
        self.image_extensions = [".jpg", ".png"]

        self.currentItemChanged.connect(self.select_list_item)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setIconSize(QSize(150, 100))
        self.setFixedWidth(550)
        self.setSpacing(5)
        self.setUniformItemSizes(True)

    def select_folder(self):
        ##Browse and select folder to display images from.
        tkinter.Tk().withdraw()
        folder_path = filedialog.askdirectory()

        if folder_path == None or folder_path == "":
            return

        files = os.listdir(folder_path)

        mouse = MouseData()
        mouse.gender = "None"
        mouse.name = "Anonymouse"
        for image_name in files:
            # Remove non picture files
            if os.path.splitext(image_name)[1].lower() in self.image_extensions:
                image_data = MouseImageData()
                image_data.mouse = mouse
                image_data.filename = image_name
                image_data.path = folder_path + "/" + image_name

                self.pictures.append(image_data)

        self.current_index = 0
        self.image_viewer.display_image(self.pictures[self.current_index])
        
        frame_ids = [int(re.findall(r'\d+', item.filename)[-1]) for item in self.pictures]
        sorting = np.argsort(frame_ids)
        self.pictures = [self.pictures[index] for index in sorting]
        
        for image_data in self.pictures:
            self.add_to_list(image_data)

    def add_to_list(self, image_data: MouseImageData):
        name = image_data.filename
        icon = QIcon(image_data.path)
        new_item = QListWidgetItem(icon, name) 
        
        self.addItem(new_item)
        
    def update_file_list(self):
        self.pictures = self.main_window.project.images
        
        frame_ids = [int(re.findall(r'\d+', item.filename)[-1]) for item in self.pictures]
        sorting = np.argsort(frame_ids)
        self.pictures = [self.pictures[index] for index in sorting]
        
        self.clear()
        for image_data in self.pictures:
            self.add_to_list(image_data)
        

    def select_list_item(self, item: QListWidgetItem):
        if self.count() == 0 or item is None:
            return
        
        name = item.text()
        # Find image with correct name
        image_data = [
            image_data for image_data in self.pictures if image_data.filename == name][0]

        self.image_viewer.display_image(image_data)
        self.current_index = self.pictures.index(image_data)
    
class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()  # "Image viewer"
        # self.setText("Image viewer")

        self.setMinimumSize(640, 320)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setScaledContents(True)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        
        self.COLORS = [
        Qt.GlobalColor.red,
        Qt.GlobalColor.green,
        Qt.GlobalColor.blue,
        ]
        

    def display_image(self, image_data: MouseImageData, size=16):

        pixmap = QPixmap(image_data.path)
        
        painter = QPainter()
        painter.begin(pixmap)
        try:
            for name, pt in image_data.key_points:
                color = None
                if "ear" in name:
                    color = self.COLORS[0]
                elif "eye" in name:
                    color = self.COLORS[1]
                else:
                    color = self.COLORS[2]
                
                painter.setBrush(color or Qt.GlobalColor.red)
                painter.drawEllipse(pt[0] - size / 2,pt[1] - size / 2,size,size)
                
        except: ## No keypoints
            pass
        
        painter.end()
        
        self.setPixmap(pixmap)

class ImageControl(QWidget):
    def __init__(self, file_list):
        super().__init__()  # "Image controls"
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('background-color: lightgray; border-radius: 10px')
        # self.setFixedWidth(500)

        self.file_list = file_list
        self.main_layout = QHBoxLayout()

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(8, 0, 8, 0)
        button_layout.setSpacing(4)
        # button_layout.addStretch()

        back_button = QToolButton()
        back_button.setToolTip("Browse backward in list")
        back_button.setArrowType(Qt.LeftArrow)
        back_button.setFixedSize(30, 30)
        back_button.clicked.connect(self.browse_backward)
        # back_button.setStyleSheet("border : 10px, border-color: beige;")
        button_layout.addWidget(back_button, 0,
                                Qt.AlignmentFlag.AlignLeading |
                                Qt.AlignmentFlag.AlignVCenter)

        self.image_index = QLabel()
        current_index = self.file_list.current_index
        items = len(self.file_list.pictures)
        self.image_index.setText("{} / {}".format(current_index, items))
        #self.file_list.currentItemChanged.connect(self.update_index)
        button_layout.addWidget(self.image_index)

        forward_button = QToolButton()
        forward_button.setToolTip("Browse forward in list")
        forward_button.setArrowType(Qt.RightArrow)
        forward_button.setFixedSize(30, 30)
        forward_button.clicked.connect(self.browse_forward)
        # forward_button.setStyleSheet("background-color: rgba(0,0,0,0);")
        button_layout.addWidget(forward_button, 0,
                                Qt.AlignmentFlag.AlignLeading |
                                Qt.AlignmentFlag.AlignVCenter)

        trash_button = QPushButton()
        trash_button.setToolTip("Discard current selected frame")
        trash_button.setFixedSize(30, 30)
        pixmapi = QStyle.StandardPixmap.SP_TrashIcon
        icon = self.style().standardIcon(pixmapi)
        trash_button.setIcon(icon)
       # trash_button.setStyleSheet("background-color: rgba(0,0,0,0);"    
        trash_button.clicked.connect(self.remove_current_image)
        button_layout.addWidget(trash_button, 0,
                                Qt.AlignmentFlag.AlignTrailing |
                                Qt.AlignmentFlag.AlignVCenter)

        edit_button = QPushButton()
        edit_button.setToolTip("Edit current selected frame")
        edit_button.setFixedSize(30, 30)
        pixmapi = QStyle.StandardPixmap.SP_DialogResetButton
        icon = self.style().standardIcon(pixmapi)  
        edit_button.clicked.connect(self.edit_picture)
        edit_button.setIcon(icon)
        # edit_button.setStyleSheet("background-color: rgba(0,0,0,0);")
        button_layout.addWidget(edit_button, 0,
                                Qt.AlignmentFlag.AlignTrailing |
                                Qt.AlignmentFlag.AlignVCenter)

        # button_layout.addStretch()
        self.main_layout.addStretch(10)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch(10)
        self.setLayout(self.main_layout)

    def update_index(self):
        current_index = self.file_list.current_index
        items = self.file_list.count()
        self.image_index.setText("{} / {}".format(current_index+1,items))

    def browse_forward(self):
        pictures = self.file_list.pictures
        index = self.file_list.current_index
        if (pictures == None or len(pictures) == 0 or index == None):
            return

        if index == len(pictures)-1:
            self.file_list.current_index = 0
        else:
            self.file_list.current_index += 1

        if self.file_list.count() != 0:
            item = self.file_list.item(self.file_list.current_index)
            self.file_list.setCurrentItem(item)  # Also calls selectListItem

    def browse_backward(self):
        pictures = self.file_list.pictures
        index = self.file_list.current_index
        if pictures == None or len(pictures) == 0 or index == None:
            return

        if index == 0:
            self.file_list.current_index = len(pictures)-1
        else:
            self.file_list.current_index -= 1

        if self.file_list.count() != 0:
            item = self.file_list.item(self.file_list.current_index)
            self.file_list.setCurrentItem(item)   ##Also calls selectListItem
        
    def remove_current_image(self):
        name = self.file_list.currentItem().text()
        image_data = [image_data for image_data in self.file_list.pictures if image_data.filename == name][0]
        #os.remove(image_data.path)
        self.file_list.pictures.remove(image_data)  ##Remove from pictures list
        self.file_list.takeItem(self.file_list.current_index)   #remove from widget

        self.update_index()

    def edit_picture(self):
        name = self.file_list.currentItem().text()
        image_data = [image_data for image_data in self.file_list.pictures if image_data.filename == name][0]
        self.file_list.main_window.editor_dialog.show(image_data)


class ImageMetadataViewer(QLabel):
    def __init__(self, file_list):
        super().__init__()

        self.file_list = file_list
        #self.file_list.currentItemChanged.connect(self.update_attributes)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.setStyleSheet('background-color: white; border-radius: 10px;')

        self.info_layout = QGridLayout()
        self.info_layout.setContentsMargins(20, 0, 10, 0)
        self.info_layout.setVerticalSpacing(0)
        self.current_data = None
        self.create_labels()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.info_layout)

    def create_labels(self):
        self.attr_to_label_map = {}

        self.create_label_row("Mouse", "", 0)
        self.create_label_row("Gender", "", 1)

        self.create_label_row("Filename", "", 2)
        self.create_label_row("Path", "", 3)

        self.create_label_row("Profile Confidence", "", 4)
        self.create_label_row("Key Point Confidence", "", 5)

    def create_label_row(self, description: str, value, row: int):
        if isinstance(value, (int, str)):
            attr_widget = QLabel()
            attr_widget.setText("{}:".format(description))
            self.info_layout.addWidget(attr_widget, row, 0)
            self.attr_to_label_map[description] = attr_widget

            value_widget = QLabel()
            value_widget.setText("{}".format(value))
            self.info_layout.addWidget(value_widget, row, 1)
            self.attr_to_label_map[description+"_value"] = value_widget
        else:
            ValueError("Value must be either integer or string")

    def update_label_row(self, description: str, value):
        if isinstance(value, (int, str)):
            value_widget = self.attr_to_label_map[description+"_value"]
            value_widget.setText("{}".format(value))
        else:
            ValueError("Value must be either integer or string")

    def update_attributes(self, item: QListWidgetItem):
        if item is None:
            return
        #return
        #self.current_data = project.images[0]
        
        name = self.file_list.currentItem().text()
        data = [image_data for image_data in self.file_list.pictures if image_data.filename == name][0]
        mouse = data.mouse
        self.update_label_row("Mouse", mouse.name)
        self.update_label_row("Gender", mouse.gender)

        try:
            self.update_label_row("Filename", data.filename)
        except:
            self.update_label_row("Filename", ""),
        
        try:
            self.update_label_row("Path", data.path)
        except:
            self.update_label_row("Path", data.path)

        try:
            self.update_label_row("Profile Confidence",
                              data.profile_conf)
        except:
            self.update_label_row("Profile Confidence",
                              "")
            
        try:
            self.update_label_row("Key Point Confidence",
                              data.key_point_conf)
        except:
            self.update_label_row("Key Point Confidence",
                              "")