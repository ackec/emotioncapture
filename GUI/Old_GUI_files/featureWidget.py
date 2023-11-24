import sys, random, math, os
import csv
import numpy as np

import tkinter
from tkinter import filedialog

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter

class featureWidget(QWidget):
    def __init__(self):
        super(featureWidget, self).__init__()
        
        self.feature_layout = QVBoxLayout()
        self.label2 = QLabel("This is Page 2")
        self.feature_layout.addWidget(self.label2)
        self.setLayout(self.feature_layout)
        
        
        self.setMinimumSize(800, 600)
        self.show()
        
    def createGraphicView(self):        ##Not used
        self.scene = VisGraphicsScene(self)
        
        #self.brush = [QBrush(Qt.green), QBrush(Qt.yellow), QBrush(Qt.red)]
        
        self.view = VisGraphicsView(self.scene, self)
        
        self.setCentralWidget(self.view)
        self.view.setGeometry(0, 0, 800, 600)
        
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