import sys, random, math, os
import csv
import numpy as np

import tkinter
from tkinter import filedialog

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter

from poseWidget import poseWidget
from featureWidget import featureWidget

app = QApplication([])

class VisGraphicsScene(QGraphicsScene): ##Not used
    def __init__(self,window):
        super(VisGraphicsScene, self).__init__()
        
        
class VisGraphicsView(QGraphicsView): ##Not used
    def __init__(self, scene, parent):
        super(VisGraphicsView, self).__init__(scene, parent)
        self.startX = 0.0
        self.startY = 0.0
        self.distance = 0.0
        self.myScene = scene
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)


    def wheelEvent(self, event):
        zoom = 1 + event.angleDelta().y()*0.001
        self.scale(zoom, zoom)
        
    def mousePressEvent(self, event):
        self.startX = event.globalPos().x()
        self.startY = event.globalPos().y()
        self.myScene.wasDragg = False
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        #print(event.globalPos())
        endX = event.globalPos().x()
        endY = event.globalPos().y()
        deltaX = endX - self.startX
        deltaY = endY - self.startY
        distance = math.sqrt(deltaX*deltaX + deltaY*deltaY)
        if(distance > 5):
            self.myScene.wasDragg = True
        super().mouseReleaseEvent(event)
         
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        
        self.pictures = None
        self.current_index = None
        self.image_extensions = [".jpg",".png"] ## add in lowercase
        
        self.pict_dict = {}
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.button_layout = QHBoxLayout()
        self.btn_pose = QPushButton("Pose \n Estimation")
        self.btn_pose.setStyleSheet("QPushButton {background-color: lightblue}")
        self.btn_pose.clicked.connect(self.showPose)
        self.button_layout.addWidget(self.btn_pose)

        self.btn_feature = QPushButton("Feature \n Extraction")
        self.btn_feature.setStyleSheet("QPushButton {background-color: lightgrey}")
        self.btn_feature.clicked.connect(self.showFeature)
        self.button_layout.addWidget(self.btn_feature)
        
        self.layout.addLayout(self.button_layout)
        
        #self.createGraphicView()
        self.setWindowTitle("Mouse")
        
        self.generalLayout = QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.generalLayout)
        self.setCentralWidget(self.central_widget)
        
        # Create a stacked widget to manage multiple pages
        self.stacked_widget = QStackedWidget()
        
        self.pose_widget = poseWidget()
        self.stacked_widget.addWidget(self.pose_widget)
        
        self.feature_widget = featureWidget()
        self.stacked_widget.addWidget(self.feature_widget)
        
        self.layout.addWidget(self.stacked_widget)
        
        self.setMinimumSize(800, 600)
        self.show()
    
    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        
        """
        if self.pose_widget is not None and self.pose_widget.image.pixmap():
            print("resize")
            self.pose_widget.image.pixmap().scaledToWidth(self.width())
        """
        
    def showPose(self):
        
        if self.stacked_widget.currentWidget() != self.pose_widget:
            self.stacked_widget.setCurrentWidget(self.pose_widget)
            
            self.btn_pose.setStyleSheet("QPushButton {background-color: lightblue}")
            self.btn_feature.setStyleSheet("QPushButton {background-color: lightgrey}")
        else:
            pass
            
    def showFeature(self):
        if self.stacked_widget.currentWidget() != self.feature_widget:
            self.stacked_widget.setCurrentWidget(self.feature_widget)

            self.btn_feature.setStyleSheet("QPushButton {background-color: lightblue}")
            self.btn_pose.setStyleSheet("QPushButton {background-color: lightgrey}")
            
        else:
            pass
        
    def createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QtWidgets.QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # Creating menus using a title
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")
     
    def createToolBars(self):
        # Using a title
        fileToolBar = self.addToolBar("File")
        # Using a QToolBar object
        #editToolBar = QtWidgets.QToolBar("Edit", self)
        #self.addToolBar(editToolBar)
        # Using a QToolBar object and a toolbar area
        helpToolBar = QtWidgets.QToolBar("Help", self)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, helpToolBar)
        
    def createGraphicView(self):    
        self.scene = VisGraphicsScene(self)
        
        #self.brush = [QBrush(Qt.green), QBrush(Qt.yellow), QBrush(Qt.red)]
        
        self.view = VisGraphicsView(self.scene, self)
        
        self.setCentralWidget(self.view)
        self.view.setGeometry(0, 0, 800, 600)
    

        
def main():
    app = QApplication(sys.argv)

    ex = MainWindow()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()
