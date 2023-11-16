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
        
        self.createMenuBar()
        
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
        
    
    

        
def main():
    app = QApplication(sys.argv)

    ex = MainWindow()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()
