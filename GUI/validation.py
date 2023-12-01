from PyQt5.QtWidgets import (QLabel, QSizePolicy, QFrame, 
                            QWidget,QHBoxLayout, QStyle,QGridLayout)
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

    def __init__(self, name: str, parent=None):
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
        
        self.setMinimumSize(640, 320)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setScaledContents(True)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        
    def display_image(self,image_data:MouseImageData):
        
        pixmap = QtGui.QPixmap(image_data.path)
        #pixmap = pixmap.scaledToWidth(self.width())
        self.setPixmap(pixmap)


    """ 
    def hasHeightForWidth(self):
        return self.pixmap() is not None

    def heightForWidth(self, w):
        if self.pixmap():
            return int(w * (self.pixmap().height() / self.pixmap().width()))
      
    def resizeEvent(self, resize_event):
        size = resize_event.size()
        w = size.width()
        h = self.heightForWidth(w)
        p = self.pixmap()
        if p != None:
            scaledPix = p.scaled(w,h) #, QtCore.Qt.KeepAspectRatio)   #, transformMode = QtCore.Qt.SmoothTransformation)
            self.setPixmap(scaledPix)
    """
class ImageControl(QWidget):
    def __init__(self,file_list):
        super().__init__() #"Image controls"
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: lightgray; border-radius: 10px' )
        #self.setFixedWidth(500)
        
        self.file_list = file_list
        self.main_layout = QHBoxLayout()

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(8, 0, 8, 0)
        button_layout.setSpacing(4)
        #button_layout.addStretch()
        
        back_button = QtWidgets.QToolButton()
        back_button.setArrowType(QtCore.Qt.LeftArrow)
        back_button.setFixedSize(30,30)
        back_button.clicked.connect(self.browse_backward)
        #back_button.setStyleSheet("border : 10px, border-color: beige;")
        button_layout.addWidget(back_button, 0,
                                   QtCore.Qt.AlignmentFlag.AlignLeading |
                                   QtCore.Qt.AlignmentFlag.AlignVCenter)
        
        self.image_index = QLabel()
        current_index = self.file_list.current_index
        items = len(self.file_list.pictures)
        self.image_index.setText("{} / {}".format(current_index,items))
        self.file_list.currentItemChanged.connect(self.update_index)
        button_layout.addWidget(self.image_index)

        forward_button = QtWidgets.QToolButton()
        forward_button.setArrowType(QtCore.Qt.RightArrow)
        forward_button.setFixedSize(30,30)
        forward_button.clicked.connect(self.browse_forward)
        #forward_button.setStyleSheet("background-color: rgba(0,0,0,0);")
        button_layout.addWidget(forward_button, 0,
                                   QtCore.Qt.AlignmentFlag.AlignLeading |
                                   QtCore.Qt.AlignmentFlag.AlignVCenter)
        
        trash_button = QtWidgets.QPushButton()
        trash_button.setFixedSize(30,30)
        pixmapi = QStyle.StandardPixmap.SP_TrashIcon
        icon = self.style().standardIcon(pixmapi)
        trash_button.setIcon(icon)
       # trash_button.setStyleSheet("background-color: rgba(0,0,0,0);"    
        trash_button.clicked.connect(self.remove_current_image)
        button_layout.addWidget(trash_button, 0,
                                   QtCore.Qt.AlignmentFlag.AlignTrailing |
                                   QtCore.Qt.AlignmentFlag.AlignVCenter)
        
        edit_button = QtWidgets.QPushButton()
        edit_button.setFixedSize(30,30)
        pixmapi = QStyle.StandardPixmap.SP_DialogResetButton
        icon = self.style().standardIcon(pixmapi)
        edit_button.setIcon(icon)
        #edit_button.setStyleSheet("background-color: rgba(0,0,0,0);")
        button_layout.addWidget(edit_button, 0,
                                   QtCore.Qt.AlignmentFlag.AlignTrailing |
                                   QtCore.Qt.AlignmentFlag.AlignVCenter)
        
        #button_layout.addStretch()
        self.main_layout.addStretch(10)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch(10)
        self.setLayout(self.main_layout)
        
    def update_index(self):
        current_index = self.file_list.current_index
        items = self.file_list.count()
        self.image_index.setText("{} / {}".format(current_index+1,items))

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
        
    def remove_current_image(self):
        name = self.file_list.currentItem().text()
        image_data = [image_data for image_data in self.file_list.pictures if image_data.filename == name][0]
        self.file_list.pictures.remove(image_data)  ##Remove from pictures list
        self.file_list.takeItem(self.file_list.current_index)   #remove from widget

        #self.file_list.image_viewer.setPixmap(QtGui.QPixmap()) ##Not required. new selected image in list -> update image viewer
        #self.file_list.current_index -= 1

        self.update_index()


class ImageMetadataViewer(QLabel):
    def __init__(self,file_list):
        super().__init__() #"Image metadata"
        
        self.file_list = file_list
        self.file_list.currentItemChanged.connect(self.update_attributes)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        
        #self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        self.setStyleSheet('background-color: white; border-radius: 10px;' )

        self.info_layout = QGridLayout()
        self.info_layout.setContentsMargins(20,0,10,0)
        self.info_layout.setVerticalSpacing(0)
        self.current_data = ExampleData()
        self.create_labels(self.current_data)
        self.setAlignment(QtCore.Qt.AlignCenter)
        
        self.setLayout(self.info_layout)

    def create_labels(self,data):
        self.attr_to_label_map = {}

        mouse = data.mouse
        self.create_label_row("Mouse", mouse.name,0)
        self.create_label_row("Gender", mouse.gender,1)
        
        self.create_label_row("Filename", data.filename,2)
        self.create_label_row("Path", data.path,3)
        
        self.create_label_row("Profile Confidence", data.profile_conf,4)
        self.create_label_row("Key Point Confidence", data.key_point_conf,5)

    def create_label_row(self,description:str,value:int|str,row:int):
        attr_widget = QLabel()
        attr_widget.setText("{}:".format(description))
        self.info_layout.addWidget(attr_widget,row,0)
        self.attr_to_label_map[description] = attr_widget

        value_widget = QLabel()
        value_widget.setText("{}".format(value))
        self.info_layout.addWidget(value_widget,row,1)
        self.attr_to_label_map[description+"_value"] = value_widget

    def update_label_row(self,description:str,value:int|str):

        value_widget = self.attr_to_label_map[description+"_value"]
        value_widget.setText("{}".format(value))

    def update_attributes(self):
        #name = self.file_list.currentItem()
        ##data = [image_data for image_data in self.file_list.pictures if image_data.filename == name][0]
        if type(self.current_data) == ExampleData:
            self.current_data = ExampleData2()
        elif type(self.current_data) == ExampleData2:
            self.current_data = ExampleData()

        mouse = self.current_data.mouse
        self.update_label_row("Mouse", mouse.name)
        self.update_label_row("Gender", mouse.gender)
        
        self.update_label_row("Filename", self.current_data.filename)
        self.update_label_row("Path", self.current_data.path)
        
        self.update_label_row("Profile Confidence", self.current_data.profile_conf)
        self.update_label_row("Key Point Confidence", self.current_data.key_point_conf)
