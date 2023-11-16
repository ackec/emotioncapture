import sys, random, math, os
import csv
import numpy as np

import tkinter
from tkinter import filedialog

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        
        self.pictures = None
        self.current_index = None
        self.image_extensions = [".jpg",".png"] ## add in lowercase
        
        self.pict_dict = {}
        
        self.setWindowTitle("Mouse")
        
        self.generalLayout = QtWidgets.QGridLayout()
        centralWidget = QWidget(self)
        #centralWidget.setStyleSheet("background-color: midnightblue;")
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self.imageDisplay()
        self.createButtons()
        self.createMenuBar()
        self.createListView()
        
        self.setMinimumSize(1000, 600)
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
        self.list_widget.setIconSize(QtCore.QSize(100,100))
        self.list_widget.setFixedWidth(450)
        self.list_widget.setSpacing(0)
        self.list_widget.setUniformItemSizes(True)
        self.generalLayout.addWidget(self.list_widget, 0,0)
    
    def selectListItem(self,item):
        name = item.text()
        self.displayImage(self.folder_path+"/"+name)
        self.current_index = self.pictures.index(name)
        
        
    def addToList(self,item):
        
        icon = QtGui.QIcon(self.folder_path+"/"+item)
        #item_layout.addWidget(icon)
        #item_layout.addWidget(item)
        new_item = QtWidgets.QListWidgetItem(icon,item)
        
        self.list_widget.addItem(new_item)
        
    
    def createMenuBar(self):
        menuBar = self.menuBar()
        
        fileMenu = menuBar.addMenu("&File")
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")
        
        self.new = fileMenu.addAction("New Project")
        self.save = fileMenu.addAction("Save Project")
        self.blank = fileMenu.addAction("")
        
        
        #self.load.triggered.connect(self.loadAction)
        
        #fileMenu.addAction(self.openAction)
        #fileMenu.addAction(self.saveAction)
        #fileMenu.addAction(self.exitAction)
    
    def loadAction(self):
        self.selectFolder()
    
    def createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QtWidgets.QGridLayout()
        
        imageButton = QPushButton("Select Image")
        imageButton.setFixedSize(100,30)
        imageButton.clicked.connect(self.selectImage)
        buttonsLayout.addWidget(imageButton,1,0)
        
        folderButton = QPushButton("Select Folder")
        folderButton.setFixedSize(100,30)
        folderButton.clicked.connect(self.selectFolder)
        buttonsLayout.addWidget(folderButton,1,1)
        
        csvButton = QPushButton("Select CSV")
        csvButton.setFixedSize(100,30)
        csvButton.clicked.connect(self.loadPoints)
        buttonsLayout.addWidget(csvButton,2,0)
        
        pointButton = QPushButton("Show Points")
        pointButton.setFixedSize(100,30)
        pointButton.clicked.connect(self.showPoints)
        buttonsLayout.addWidget(pointButton,2,1)
        
        self.generalLayout.addLayout(buttonsLayout,1,0,1,2)
    
    
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
        self.generalLayout.addLayout(self.image_layout,0,2)     
    
    
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
            print(header)
            
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
        
        
def main():
    app = QApplication(sys.argv)

    ex = MainWindow()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()
