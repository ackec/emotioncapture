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
        
        self.generalLayout.addWidget(self.createListView(),0,0,2,1)
        self.generalLayout.addLayout(self.imageDisplay(),0,1,1,1)  
        self.generalLayout.addLayout(self.imageInfo(),1,1,1,1)  
        
        self.createMenuBar()
        
        #self.setMinimumSize(1000, 600)
        self.setFixedSize(1000, 600)
        self.show()
            
    def drawEllipse(self,x,y,radii=1):
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
        
        return self.list_widget
    
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
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("&File")
        edit_menu = menu_bar.addMenu("&Edit")
        help_menu = menu_bar.addMenu("&Help")
        tempMenu = menu_bar.addMenu("&Temp")
        
        self.new = file_menu.addAction("New Project")
        pixmapi = QStyle.StandardPixmap.SP_FileDialogNewFolder
        icon = self.style().standardIcon(pixmapi)
        self.new.setIcon(icon)
        self.new.triggered.connect(self.newProject)
        
        self.save = file_menu.addAction("Save Project")
        pixmapi = QStyle.StandardPixmap.SP_DialogSaveButton
        icon = self.style().standardIcon(pixmapi)
        self.save.setIcon(icon)
        
        self.blank = file_menu.addAction("")
        
        
        #self.load.triggered.connect(self.loadAction)
        
        load_image = tempMenu.addAction("Select Image")
        load_image.triggered.connect(self.selectImage)
        
        load_folder = tempMenu.addAction("Select Folder")
        load_folder.triggered.connect(self.selectFolder)
        
        load_csv = tempMenu.addAction("Select CSV")
        load_csv.triggered.connect(self.loadPoints)
        
        show_points = tempMenu.addAction("Show Points")
        show_points.triggered.connect(self.showPoints)
    
    def newProject(self):
        self.dlg = QDialog(self)
        
        dlg_layout = QFormLayout()
        self.dlg.setWindowTitle("New Project")
        
        project_name = QLineEdit()
        project_name.setAlignment(Qt.AlignRight)

        mouse_name = QLineEdit()
        mouse_name.setAlignment(Qt.AlignRight)
        
        file_browse = QHBoxLayout()
        file_name = QLineEdit()
        file_name.setObjectName("file_name")
        file_name.setReadOnly(True)
        
        file_browse_btn = QPushButton()
        file_browse_btn.setText("Browse")
        file_browse_btn.clicked.connect(self.selectFolder)
        file_browse.addWidget(file_name)
        file_browse.addWidget(file_browse_btn)

        create_buttons = QHBoxLayout()
        
        cancel_button = QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.clicked.connect(self.dlg.close)
        create_buttons.addWidget(cancel_button)
        
        create_button = QPushButton()
        create_button.setText("Create")
        create_button.clicked.connect(self.createProject)
        create_buttons.addWidget(create_button)

        dlg_layout.addRow("Project Name",project_name)
        dlg_layout.addRow("Mouse Name",mouse_name)
        dlg_layout.addRow("File Path(s)",file_browse)
        dlg_layout.addRow("",create_buttons)
        
        self.dlg.setLayout(dlg_layout)
        self.dlg.exec()
    
    def createProject(self):
        ## Add save information from project creation
        self.dlg.close()
        return
        
    def imageDisplay(self):
        ## Label (pixmap) for displaying images
        
        self.image_layout = QVBoxLayout()
        self.image_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        #self.image_layout.setSpacing(0)
        
        self.image = QtWidgets.QLabel()
        self.image.setStyleSheet("border: 1px solid black;") 
        self.image.setFixedSize(500,300) #QtCore.QSize(500,300))
        self.image_layout.addWidget(self.image)
        
        
        #button_frame = QFrame()
        #button_frame.setFrameStyle(QFrame.StyledPanel)
        #button_frame.setContentsMargins(1,1,1,1)
        
        button_layout = QHBoxLayout()
        #button_frame.setLayout(button_layout)
        
        
        button_layout.addStretch()
        #button_layout.setSpacing(0)
        
        back_button = QToolButton()
        back_button.setArrowType(QtCore.Qt.LeftArrow)
        back_button.setFixedSize(30,30)
        back_button.clicked.connect(self.browseBackward)
        button_layout.addWidget(back_button)
        
        forward_button = QToolButton()
        forward_button.setArrowType(QtCore.Qt.RightArrow)
        forward_button.setFixedSize(30,30)
        forward_button.clicked.connect(self.browseForward)
        button_layout.addWidget(forward_button)
        
        trash_button = QPushButton()
        trash_button.setFixedSize(30,30)
        pixmapi = QStyle.StandardPixmap.SP_TrashIcon
        icon = self.style().standardIcon(pixmapi)
        trash_button.setIcon(icon)
        button_layout.addWidget(trash_button)
        
        edit_button = QPushButton()
        edit_button.setFixedSize(30,30)
        pixmapi = QStyle.StandardPixmap.SP_DialogResetButton
        icon = self.style().standardIcon(pixmapi)
        edit_button.setIcon(icon)
        button_layout.addWidget(edit_button)
        
        button_layout.addStretch()
        #self.image_layout.addWidget(button_frame)
        self.image_layout.addLayout(button_layout) 
        
        return self.image_layout          
    
    def displayImage(self,file_path):
        pixmap = QtGui.QPixmap(file_path)
        pixmap = pixmap.scaledToWidth(self.image.width())
        self.image.setPixmap(pixmap)
    
    
    def imageInfo(self):
        self.info = QLabel()
        self.info.setFixedSize(500,200)
        self.info.setStyleSheet("border: 1px solid black;") 
        self.info_layout = QHBoxLayout()
        self.info.setAlignment(QtCore.Qt.AlignCenter)
        self.info_dict = {"Mouse:":"Anonymouse",
                          "Gender:":"Male",
                          "Genotype:":"Opto",
                            "Image:":"Img_example.jpg",
                            "Profile Score:":0.89,
                            "Key Point Score":0.97}
        
        temp_text = ""
        for key,value in self.info_dict.items():
            temp_text += "{} \t \t \t {} \n".format(key,value)
            
        self.info.setText(temp_text)
        self.info_layout.addWidget(self.info)
        return self.info_layout
    
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

        #Remove earlier loaded pictures (Should remove this and fix add in future)
        if self.pictures != None and len(self.pictures) != 0:
            self.pictures = []
            self.pict_dict = {}
            self.list_widget.clear()
            
        
        files = os.listdir(folder_path)
        ##Remove non picture files
        
        self.folder_path = folder_path
        self.pictures = [image_name for image_name in files if os.path.splitext(image_name)[1].lower() in self.image_extensions]  
       
        
        self.current_index = 0
        self.displayImage(self.folder_path+"/"+self.pictures[self.current_index])
        
        for name in self.pictures:
            self.addToList(name)
            
        if self.dlg.isVisible():
            text = self.dlg.findChild(QLineEdit,name="file_name")
            text.setText(folder_path)
    
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
