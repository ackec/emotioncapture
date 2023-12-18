from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QPen
from PyQt5.QtCore import Qt, QSize, QItemSelectionModel,QModelIndex
import tkinter
from tkinter import filedialog
import os
import  re
import numpy as np
import time
from data import *
from config import ACCEPTED_TYPES

# List of packages that are allowed to be imported
__all__ = ["ImageMetadataViewer", "ImageControl",
           "ImageViewer"]


class PlaceHolder(QLabel):
    """ Placeholder widget while app is being developed """

    def __init__(self, name: str, parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setText(name)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

    
class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()  # "Image viewer"
        # self.setText("Image viewer")

        self.setMinimumSize(640, 320)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setScaledContents(True)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setMouseTracking(True) 
        
        self.COLORS = [
        Qt.GlobalColor.red,
        Qt.GlobalColor.green,
        Qt.GlobalColor.blue,
        ]
    
        self.key_columns = ["Ear_back_x", "Ear_back_y", "Ear_front_x", "Ear_front_y",
                            "Ear_bottom_x", "Ear_bottom_y", "Ear_top_x", "Ear_top_y", "Eye_back_x", "Eye_back_y",
                            "Eye_front_x", "Eye_front_y", "Eye_bottom_x", "Eye_bottom_y", "Eye_top_x", "Eye_top_y",
                            "Nose_top_x", "Nose_top_y", "Nose_bottom_x", "Nose_bottom_y", "Mouth_x", "Mouth_y"]
        
        
        
    def update_image(self,data, size=16):
        pixmap = QPixmap(self.image_path)
        
        name = os.path.basename(self.image_path)
        data_row = data[data["Img_Path"]==name]
        
        if len(data_row)>1:
            parent_name = os.path.dirname(self.image_path)
            parent_name = os.path.basename(os.path.normpath(parent_name))
            data_row = data_row[data_row["Video_Name"] == parent_name]
            
            if len(data_row)==0:    ##No data was found for the image
                return
            elif len(data_row)>1: ##Fix if multiple of same name in folder
                data_row = data_row[0,:]
        
        painter = QPainter()
        painter.begin(pixmap)
        
        if data is not None:
            key_points = data_row[self.key_columns]
            
            for i in range(key_points.size//2):
                j = 2*i
                name = self.key_columns[j]
                
                x = key_points.iloc[0,j]
                y = key_points.iloc[0,j+1]
                
                color = None
                if "ear" in name.lower():
                    color = self.COLORS[0]
                elif "eye" in name.lower():
                    color = self.COLORS[1]
                else:
                    color = self.COLORS[2]
                
                painter.setBrush(color or Qt.GlobalColor.red)
                painter.drawEllipse(x - size / 2,y - size / 2,size,size)
            
        painter.end()
        # except: ## No keypoints
        #     painter.end()
        
        self.setPixmap(pixmap)
    
        
    def display_image(self, image_path: str, data_row=None, size=16):
        #print(image_path)
        if image_path == "":
            pixmap = QPixmap()
            self.setPixmap(pixmap)
            return
        
        self.image_path = image_path
        pixmap = QPixmap(image_path)
        
        painter = QPainter()
        painter.begin(pixmap)
        
        if data_row is not None:
            key_points = data_row[self.key_columns]
            for i in range(key_points.size//2):
                j = 2*i
                name = self.key_columns[j]
                
                x = key_points.iloc[0,j]
                y = key_points.iloc[0,j+1]
                
                color = None
                if "ear" in name.lower():
                    color = self.COLORS[0]
                elif "eye" in name.lower():
                    color = self.COLORS[1]
                else:
                    color = self.COLORS[2]
                
                painter.setBrush(color or Qt.GlobalColor.red)
                painter.drawEllipse(round(x - size/2), round(y - size/2), size, size)
        
        painter.end()
        # except: ## No keypoints
        #     painter.end()
        
        self.setPixmap(pixmap)
    
        
class ImageControl(QWidget):
    def __init__(self, file_list,data_viewer):
        super().__init__()  # "Image controls"
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('background-color: lightgray; border-radius: 10px')
        # self.setFixedWidth(500)

        self.file_list = file_list
        self.data_viewer = data_viewer
        self.main_layout = QHBoxLayout()
        self.items = 0
        
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
        self.image_index.setToolTip("Current selected image")
        self.image_index.setText("{} / {}".format(0, 0))
        
        self.file_list.tree_view.clicked.connect(self.update_index)        
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
        if current_index is not None and current_index.isValid():
            row = current_index.row()
            self.items = self.file_list.siblings
            self.image_index.setText("{} / {}".format(row+1,self.items))

    def browse_forward(self):
        
        index = self.file_list.current_index
        row = index.row()
        if row == self.file_list.siblings-1:
            row = 0
        else:
            row += 1

        new_index = index.siblingAtRow(row)
        self.file_list.current_index = new_index
        self.file_list.tree_view.setCurrentIndex(new_index)
        self.file_list.select_item(new_index)
        self.update_index()
        self.data_viewer.update_attributes(new_index)
        

    def browse_backward(self):
        index = self.file_list.current_index
        row = index.row()
        if row == 0:
            row = self.file_list.siblings-1
        else:
            row -= 1

        new_index = index.siblingAtRow(row)
        self.file_list.current_index = new_index
        self.file_list.tree_view.setCurrentIndex(new_index)
        self.file_list.select_item(new_index)
        self.update_index()
        self.data_viewer.update_attributes(new_index)
        
        
    def remove_current_image(self):
        
        index = self.file_list.current_index
        if index is None:
            return
        
        parent = index.parent()
        path = index.model().filePath(index)
        
        row = index.row()
        
        if row == 0:
            new_index = index.siblingAtRow(row+1)
            new_row = 1
        else:
            new_index = index.siblingAtRow(row-1)
            new_row = row
        
        self.items -= 1
        self.image_index.setText("{} / {}".format(new_row,self.items))
        
        if index.model().fileName(index) == new_index.model().fileName(new_index):
            new_index = parent.child(1,0)
                
        if new_index.isValid():
            self.file_list.select_item(new_index)
            self.file_list.tree_view.setCurrentIndex(new_index)
            self.file_list.tree_view.selectionModel().select(new_index,QItemSelectionModel.ClearAndSelect)
            self.data_viewer.update_attributes(new_index)
            
        else:
            self.file_list.current_index = None
            self.file_list.image_viewer.display_image("")
            self.image_index.setText("{} / {}".format(0,0))
            
        try:
            self.file_list.tree_view.model().remove(index)
            name = index.model().fileName(index)
            data = self.file_list.main.project.project_data
            data_row =  self.data.loc[self.data["Img_Path"] == name]
            
            parent_name = index.model().fileName(index.parent())
            data_row = data_row[data_row["Video_Name"] == parent_name]
                
            for i in len(data_row):    
                data.drop(data_row[i,:].index)
        except:
            pass
        
        

    def edit_picture(self):
        
        index = self.file_list.current_index
        
        if index is not None and index.isValid():
            name = index.model().fileName(index)
            path = index.model().filePath(index)
            self.file_list.main.editor_dialog.show(name,path,self.file_list)
                   
            ##Update image viewer: Why this not do stuff   !!  
            #data_row =  self.file_list.data.loc[self.file_list.data["Img_Path"] == name]
            #self.file_list.image_viewer.display_image(path,data_row)
            

class ImageMetadataViewer(QLabel):
    def __init__(self, file_list):
        super().__init__()

        self.file_list = file_list
        self.file_list.tree_view.clicked.connect(self.update_attributes)

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

        self.create_label_row("Mouse", "Anonymouse", 0)
        self.create_label_row("Gender", "NaN", 1)
        self.create_label_row("GenoType", "Something", 2)
        self.create_label_row("Weight", 0, 3)
        self.create_label_row("Age", 1, 4)

        self.create_label_row("Filename", "placeholder.jpg", 5)
        self.create_label_row("Label", "Baseline", 6)
        
        self.create_label_row("ProfileConfidence", 0, 7)
        self.create_label_row("KeypointConfidence", 0, 8)

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
        if isinstance(value, (float,np.float64,int, str)):
            value_widget = self.attr_to_label_map[description+"_value"]
            value_widget.setText("{}".format(value))
        else:
            ValueError("Value must be either integer or string")

    def update_attributes(self, index: QModelIndex=None):
        if index is None:
            self.clear_attributes()
        file_name = index.model().fileName(index)
        
        #try:
        ext = os.path.splitext(file_name)[-1]
        if ext not in ACCEPTED_TYPES:   ##Check if selected item is an image (not folder))
            return
        
        data = self.file_list.main.project.project_data
        
        if data is not None:
            # try:
            data_row = data[data["Img_Path"] == file_name]
            
            parent_name = index.model().fileName(index.parent())
            data_row = data_row[data_row["Video_Name"] == parent_name]
            
            if len(data_row)==0:    ##No data was found for the image
                self.clear_attributes()
                return
            elif len(data_row)>1: ##Fix if multiple of same name in folder
                data_row = data_row.iloc[0]
            
            
            data_row = data_row.squeeze()
            current_name = data_row["Mouse_Name"]
            self.update_label_row("Mouse", current_name)
            
            mouse_data = [mouse for mouse in self.file_list.main.project.mice if mouse.name == current_name]
            if len(mouse_data) > 0:
                mouse = mouse_data[0]
                self.update_label_row("Gender", mouse.gender)
                self.update_label_row("GenoType", mouse.genotype)
                self.update_label_row("Weight", mouse.weight)
                self.update_label_row("Age", mouse.age)

            self.update_label_row("Filename", data_row["Img_Path"])
            self.update_label_row("Label", data_row["Stimuli"])
            
            self.update_label_row("ProfileConfidence", round(data_row["profile_score"], 3))
            self.update_label_row("KeypointConfidence",round(data_row["keypoint_score"], 3))
            # except:
            #     return
            
    def clear_attributes(self):
        self.update_label_row("Gender", "")
        self.update_label_row("GenoType", "")
        self.update_label_row("Weight","")
        self.update_label_row("Age", "")
        
        self.update_label_row("Filename", "")
        self.update_label_row("Label", "")
        
        self.update_label_row("ProfileConfidence", "")
        self.update_label_row("KeypointConfidence", "")
        