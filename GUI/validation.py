from PyQt5.QtWidgets import QLabel, QSizePolicy, QFrame, QWidget
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
        self.setIconSize(QtCore.QSize(100,100))
        self.setFixedWidth(450)
        self.setSpacing(0)
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

class ImageControl(PlaceHolder):
    def __init__(self):
        super().__init__("Image controls")


class ImageMetadataViewer(PlaceHolder):
    def __init__(self):
        super().__init__("Image metadata")
