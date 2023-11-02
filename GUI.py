import sys, random, math, os

import tkinter
from tkinter import filedialog

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QMainWindow, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

app = QApplication([])

class VisGraphicsScene(QGraphicsScene):
    def __init__(self,window):
        super(VisGraphicsScene, self).__init__()
        
        
class VisGraphicsView(QGraphicsView):
    def __init__(self, scene, parent):
        super(VisGraphicsView, self).__init__(scene, parent)
        self.startX = 0.0
        self.startY = 0.0
        self.distance = 0.0
        self.myScene = scene
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
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
        
        #self.createGraphicView()
        self.setWindowTitle("My App")
        
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self.imageDisplay()
        self.createButtons()
        
        self.setMinimumSize(800, 600)
        self.show()
        
    def imageDisplay(self):
        self.image = QtWidgets.QLabel()
        self.image.setText("Hi")
        pixmap = QtGui.QPixmap('lul.jpg')
        self.image.setPixmap(pixmap)
        self.image.resize(pixmap.width(), pixmap.height())
        
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.generalLayout.addWidget(self.image)
        
    def createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QtWidgets.QGridLayout()
        
        #buttons = ["Select Image", "1","2"]
        imageButton = QPushButton("Select Image")
        imageButton.clicked.connect(self.selectImage)
        buttonsLayout.addWidget(imageButton)
        
        folderButton = QPushButton("Select Folder")
        folderButton.clicked.connect(self.selectFolder)
        buttonsLayout.addWidget(folderButton)
        """
        for i,name in enumerate(buttons):
            button = QPushButton(name)
            #self.buttonMap[key].setFixedSize(50, 50)
            buttonsLayout.addWidget(button, 0, i)
        """
        self.generalLayout.addLayout(buttonsLayout)
    
    def selectImage(self):
        tkinter.Tk().withdraw()
        file_path = filedialog.askopenfilename()
        print("Selected file:{}".format(file_path))
        
        ## Check if a file is selected
        if file_path == None or file_path == "":
            return
        ## Check if picture (Add more extensions?)
        file_type = os.path.splitext(file_path)[1]        
        if file_type.lower() != ".jpg" and file_type.lower() != ".png":
            return
        
        pixmap = QtGui.QPixmap(file_path)
        pixmap = pixmap.scaledToWidth(self.width())
        self.image.setPixmap(pixmap)
        #self.image.resize(pixmap.width(), pixmap.height())
    
    def selectFolder(self):
        tkinter.Tk().withdraw()
        folder_path = filedialog.askdirectory()
        files = os.listdir(folder_path)
        print(files)
    
        pixmap = QtGui.QPixmap(folder_path)
        pixmap = pixmap.scaledToWidth(self.width())
        self.width()
        self.image.setPixmap(pixmap)
        #self.image.resize(pixmap.width(), pixmap.height())
        
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
