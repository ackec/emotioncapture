import sys, random, math, os
import csv
import numpy as np

import re
import tkinter
from tkinter import filedialog

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

class poseWidget(QWidget):
    def __init__(self):
        super(poseWidget, self).__init__()
        
        self.pictures = None
        self.current_index = None
        self.image_extensions = [".jpg",".png"] ## add in lowercase
        
        self.pict_dict = {}
        
        #self.createGraphicView()
        
        self.pose_layout = QGridLayout()
        self.imageDisplay()
        self.createButtons()
        self.createListView()
        
        self.setLayout(self.pose_layout)
        
        #centralWidget.setStyleSheet("background-color: midnightblue;")
        
        
        self.setMinimumSize(800, 600)
        self.show()
        
    
    
    def drawEllipse(self,x,y,radii=5):
        painter = QtGui.QPainter(self.image.pixmap())
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor('yellow'))
        pen.setWidth(radii)
        painter.setPen(pen)
        painter.drawEllipse(x-radii/2, y-radii/2, radii, radii)
        painter.end()
    
    def createListView(self):
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.currentItemChanged.connect(self.selectListItem)
        self.list_widget.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        self.list_widget.setFixedWidth(200)
        #self.list_widget.setSortingEnabled(True)
        self.pose_layout.addWidget(self.list_widget, 0,1)
    
    def selectListItem(self,item):
        name = item.text()
        self.displayImage(self.folder_path+"/"+name)
        self.current_index = self.pictures.index(name)
        
        
    def addToList(self,item):
        
        icon = QtGui.QIcon(self.folder_path+"/"+item)
        
        #item_layout.addWidget(icon)
        #item_layout.addWidget(item)
        new_item = QtWidgets.QListWidgetItem(icon,item)
        
        #s = ''.join(re.findall(r'\d+', item))
        #new_item.setData(int(s),item)
        
        self.list_widget.addItem(new_item)
        
    def createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QtWidgets.QVBoxLayout()
        buttonsLayout.setSpacing(20)
        imageButton = QPushButton("Select Image")
        imageButton.setFixedSize(200,50)
        imageButton.clicked.connect(self.selectImage)
        buttonsLayout.addWidget(imageButton)
        folderButton = QPushButton("Select Folder")
        folderButton.setFixedSize(200,50)
        folderButton.clicked.connect(self.selectFolder)
        buttonsLayout.addWidget(folderButton)
        
        csvButton = QPushButton("Select CSV")
        csvButton.setFixedSize(200,50)
        csvButton.clicked.connect(self.loadPoints)
        buttonsLayout.addWidget(csvButton)
        
        pointButton = QPushButton("Show Points")
        pointButton.setFixedSize(200,50)
        pointButton.clicked.connect(self.showPoints)
        buttonsLayout.addWidget(pointButton)
        
        self.pose_layout.addLayout(buttonsLayout,0,0)
        #buttonsLayout.addStretch()
        buttonsLayout.setAlignment(Qt.AlignVCenter)
    
        
    def selectFolder(self):
        ## Browse and select folder to display images from
        tkinter.Tk().withdraw()
        folder_path = filedialog.askdirectory()
        
        if folder_path == None or folder_path == "":
            return
        
        files = os.listdir(folder_path)
        ##Remove non picture files
        
        self.folder_path = folder_path
        self.pictures = [image_name for image_name in files if os.path.splitext(image_name)[1].lower() in self.image_extensions]  
        
        self.current_index = 0
        self.displayImage(self.folder_path+"/"+self.pictures[self.current_index])
        
        for name in self.pictures:
            self.addToList(name)
    
        #self.list_widget.sortItems()
        
    def loadPoints(self):
        tkinter.Tk().withdraw()
        csv_path = filedialog.askopenfilename()
        
        if csv_path == None or csv_path == "":
            return
        file_type = os.path.splitext(csv_path)[1]        
        if file_type.lower() != ".csv":
            return
        
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
                        
            header = next(reader)
            #print(header)
            
            for row in reader:
                self.pict_dict[row[0]] = row[2:]
        
    def showPoints(self):
        if self.pict_dict == None or len(self.pict_dict) == 0:
            return
        if self.pictures == None or len(self.pictures) == 0 or self.current_index == None:
            return
        
        current_image_name = self.pictures[self.current_index]
        current_points = self.pict_dict[current_image_name]
        
        if len(current_points) != 22:
            print("Invalid amount of points")
            return
        
        for i in range(int(len(current_points)/2)):
            image_size = self.image.size()
            x = int(current_points[2*i]) * image_size.width()/1980
            y = int(current_points[2*i+1]) * image_size.height()/1080
            
            #print(image_size.width()/1980,image_size.height()/1080)
            
            #point = QPoint(round(x),round(y))
            #point = self.image.mapToGlobal(point)
            #self.drawEllipse(point.x(),point.y())
            
            self.drawEllipse(x,y)
            
        self.image.update()
        
    def imageDisplay(self):
        ## Label (pixmap) for displaying images
        
        self.image_layout = QVBoxLayout()
        
        self.image = QtWidgets.QLabel()
        self.image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addWidget(self.image)
        
        button_layout = QHBoxLayout()
        backButton = QToolButton()
        backButton.setArrowType(QtCore.Qt.LeftArrow)
        backButton.setFixedSize(100,30)
        backButton.clicked.connect(self.browseBackward)
        button_layout.addWidget(backButton)
        
        forwardButton = QToolButton()
        forwardButton.setArrowType(QtCore.Qt.RightArrow)
        forwardButton.setFixedSize(100,30)
        forwardButton.clicked.connect(self.browseForward)
        button_layout.addWidget(forwardButton)
        
        self.image_layout.addLayout(button_layout)        
        self.pose_layout.addLayout(self.image_layout,0,2)        
        
    def displayImage(self,file_path):
        pixmap = QtGui.QPixmap(file_path)
        pixmap = pixmap.scaledToWidth(self.width())
        self.image.setPixmap(pixmap)
        
    def selectImage(self):
        ## Browse and select image to display
        tkinter.Tk().withdraw()
        file_path = filedialog.askopenfilename()
        print("Selected file:{}".format(file_path))
        
        ## Check if a file is selected
        if file_path == None or file_path == "":
            return
        ## Check if picture (Add more extensions?)
        file_type = os.path.splitext(file_path)[1]        
        if file_type.lower() not in self.image_extensions:
            return
        
        self.displayImage(file_path)
        
    def browseForward(self):
        if self.pictures == None or len(self.pictures) == 0 or self.current_index == None:
            return
            
        if self.current_index == len(self.pictures)-1:
            self.current_index = 0
        else:
            self.current_index += 1
        
        if self.list_widget.count() != 0:
            item = self.list_widget.item(self.current_index)
            self.list_widget.setCurrentItem(item)   ##Also calls selectListItem
        else:
            self.displayImage(self.folder_path+"/"+self.pictures[self.current_index])
     
    def browseBackward(self): 
        if self.pictures == None or len(self.pictures) == 0 or self.current_index == None:
            return
        
        if self.current_index == 0:
            self.current_index = len(self.pictures)-1
        else:
            self.current_index -= 1
        
        if self.list_widget.count() != 0:
            item = self.list_widget.item(self.current_index)
            self.list_widget.setCurrentItem(item)   ##Also calls selectListItem
        else:
            self.displayImage(self.folder_path+"/"+self.pictures[self.current_index])