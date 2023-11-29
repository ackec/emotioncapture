from PyQt5.QtWidgets import (QLabel, QSizePolicy, QFrame, 
                            QWidget,QHBoxLayout, QStyle)
from PyQt5 import QtWidgets
from PyQt5 import QtCore,QtGui
import tkinter
from tkinter import filedialog
import os

from data import *

# List of packages that are allowed to be imported
__all__ = ["ImageMetadataViewer", "ImageControl",
           "ImageViewer", "ImageFileList"]


class PlaceHolder(QLabel):
    """ Placeholder widget while app is being developed """

    def __init__(self, name: str, parent: QWidget | None = None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setText(name)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)


class ImageFileList(QtWidgets.QListWidget):
    def __init__(self,image_viewer):
        super().__init__()  #"Image File list"
        
        self.image_viewer = image_viewer
        self.current_index = 0
        self.pictures = []
        self.image_extensions = [".jpg",".png"] ## Allowed file extensions for loading images
                                                ## Find better way to check if image or not (?)
                                                
        self.currentItemChanged.connect(self.select_list_item)
        self.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        self.setIconSize(QtCore.QSize(150,100))
        self.setFixedWidth(550)
        self.setSpacing(5)
        self.setUniformItemSizes(True)
        
    
    def select_folder(self):
        ## Browse and select folder to display images from
        tkinter.Tk().withdraw()
        folder_path = filedialog.askdirectory()
        
        if folder_path == None or folder_path == "":
            return
        
        files = os.listdir(folder_path)
        
        mouse = MouseData()
        mouse.gender = "None"
        mouse.name = "Anonymouse"
        for image_name in files:
            ##Remove non picture files
            if os.path.splitext(image_name)[1].lower() in self.image_extensions:
                image_data = MouseImageData()
                image_data.mouse = mouse
                image_data.filename = image_name
                image_data.path = folder_path + "/" + image_name
                
                self.pictures.append(image_data)
        
        self.current_index = 0
        self.image_viewer.display_image(self.pictures[self.current_index])
            
        for image_data in self.pictures:
            self.add_to_list(image_data)
            
    def add_to_list(self,image_data:MouseImageData):
        name = image_data.filename
        icon = QtGui.QIcon(image_data.path)
        new_item = QtWidgets.QListWidgetItem(icon,name)
        
        self.addItem(new_item)
    
    def select_list_item(self,item:QtWidgets.QListWidgetItem):
        name = item.text()
        ## Find image with correct name
        image_data = [image_data for image_data in self.pictures if image_data.filename == name][0]
        
        self.image_viewer.display_image(image_data)
        self.current_index = self.pictures.index(image_data)
        
        
class ImageViewer(QLabel):
    def __init__(self):
        super().__init__() #"Image viewer"
        #self.setText("Image viewer")
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        
    def display_image(self,image_data:MouseImageData):
        
        pixmap = QtGui.QPixmap(image_data.path)
        pixmap = pixmap.scaledToWidth(self.width())
        self.setPixmap(pixmap)

class ImageControl(QWidget):
    def __init__(self,file_list):
        super().__init__() #"Image controls"
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        
        #self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.file_list = file_list
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        back_button = QtWidgets.QToolButton()
        back_button.setArrowType(QtCore.Qt.LeftArrow)
        back_button.setFixedSize(30,30)
        back_button.clicked.connect(self.browse_backward)
        button_layout.addWidget(back_button)
        
        forward_button = QtWidgets.QToolButton()
        forward_button.setArrowType(QtCore.Qt.RightArrow)
        forward_button.setFixedSize(30,30)
        forward_button.clicked.connect(self.browse_forward)
        button_layout.addWidget(forward_button)
        
        trash_button = QtWidgets.QPushButton()
        trash_button.setFixedSize(30,30)
        pixmapi = QStyle.StandardPixmap.SP_TrashIcon
        icon = self.style().standardIcon(pixmapi)
        trash_button.setIcon(icon)
        button_layout.addWidget(trash_button)
        
        edit_button = QtWidgets.QPushButton()
        edit_button.setFixedSize(30,30)
        pixmapi = QStyle.StandardPixmap.SP_DialogResetButton
        icon = self.style().standardIcon(pixmapi)
        edit_button.setIcon(icon)
        button_layout.addWidget(edit_button)
        
        button_layout.addStretch()
        self.setLayout(button_layout)
        

    def browse_forward(self):
        if self.file_list.pictures == None or len(self.file_list.pictures) == 0 or self.file_list.current_index == None:
            return
            
        if self.file_list.current_index == len(self.file_list.pictures)-1:
            self.file_list.current_index = 0
        else:
            self.file_list.current_index += 1
        
        if self.file_list.count() != 0:
            item = self.file_list.item(self.file_list.current_index)
            self.file_list.setCurrentItem(item)   ##Also calls selectListItem
     
    def browse_backward(self): 
        if self.file_list.pictures == None or len(self.file_list.pictures) == 0 or self.file_list.current_index == None:
            return
        
        if self.file_list.current_index == 0:
            self.file_list.current_index = len(self.pictures)-1
        else:
            self.file_list.current_index -= 1
            
        if self.file_list.count() != 0:
            item = self.file_list.item(self.file_list.current_index)
            self.file_list.setCurrentItem(item)   ##Also calls selectListItem
        
            
class ImageMetadataViewer(QLabel):
    def __init__(self):
        super().__init__() #"Image metadata"
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        
        self.info_layout = QHBoxLayout()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.info_dict = {"Mouse:":"Anonymouse",
                          "Gender:":"Male",
                          "Genotype:":"Opto",
                            "Image:":"Img_example.jpg",
                            "Profile Score:":0.89,
                            "Key Point Score":0.97}
        
        temp_text = ""
        for key,value in self.info_dict.items():
            temp_text += "{} \t \t \t {} \n".format(key,value)
            
        self.setText(temp_text)
        
        self.setLayout(self.info_layout)
