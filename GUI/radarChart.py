import sys
import math
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget,QGraphicsScene,QGraphicsTextItem,QGraphicsView,QMainWindow,QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPolygonF, QFont
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5 import QtGui
import csv


class RadarChart(QGraphicsView):
    def __init__(self,data,base_line):
        super().__init__()

        self.base_line = base_line
        self.data = data
        self.labels = ['Eye\nOpening', 'Ear\nPosition', 'Ear\nOpening', 'Ear\nAngle', 
                       'Snout\nPosition','Mouth\nPosition','Face\nInclination']  # Labels for each axis

        self.radar_scene = QGraphicsScene()
        self.setSceneRect(0, 0, 400, 300)
        
        ##Change alpha of pen. (Prob/def a better way to do this)
        self.base_pen = QtGui.QPen()
        color = self.base_pen.color()
        color.setAlpha(150)
        self.base_pen.setColor(color)
        
        self.drawRadar()
        
        
        self.setScene(self.radar_scene)

    def drawRadar(self):
        #self.scene.clear()

        center = self.sceneRect().center()
        center = QPointF(center)
        radius = min(self.sceneRect().width(), self.sceneRect().height()) / 3
        
        num_points = len(self.data)
        angle = 2 * math.pi / num_points
        baseline_edge_id = 3
        points_list = []
        
        pen = QtGui.QPen()
        color = pen.color()
        color.setAlpha(50)
        pen.setColor(color)
        
        # Draw the axes going from center
        for i in range(num_points):
            direction = QPointF(math.sin(i * angle),math.cos(i * angle))
            point = center + radius * direction
            
            line = QLineF(center, point)
            self.radar_scene.addLine(line,self.base_pen)
            line = QLineF(point, center + 2*radius * direction)
            self.radar_scene.addLine(line,pen)
            points_list.append(point)
        
        # Draw the "circular" axes (2*baseline_edge_id) is the amount of drawn "circles"
        for j in range(1,2*baseline_edge_id+1):
            
            if j == baseline_edge_id:
                    pen = QtGui.QPen(QtGui.QColor(255, 0, 0, 255))
            elif j > baseline_edge_id:
                pen = QtGui.QPen()
                color = pen.color()
                color.setAlpha(500/j**2)
                #print(j,500/j**2)
                pen.setColor(color)
            else:
                pen = self.base_pen
                    
            for i in range(len(points_list)):
                point = points_list[i]
                prev_point = points_list[i-1]
                
                line = QLineF(center+(point-center)*j/baseline_edge_id,center+(prev_point-center)*j/baseline_edge_id)
                self.radar_scene.addLine(line,pen)
              
        for i, label in enumerate(self.labels):
            text = QGraphicsTextItem(label)
            text.setPos(center.x() + 1.5*radius * math.sin(i * angle) - 10,center.y() + 1.5*radius * math.cos(i * angle) - 10)
            self.radar_scene.addItem(text)
        
        # Draw the data polygon
        data_polygon = QPolygonF()
        for i, value in enumerate(self.data):
            x = (value/self.base_line[i])*radius * math.sin(i * angle)
            y = (value/self.base_line[i])*radius * math.cos(i * angle)
            data_polygon.append(center + QPointF(x, y))

        poly = self.radar_scene.addPolygon(QtGui.QPolygonF(data_polygon))
        poly.setBrush(QtGui.QBrush(QtGui.QColor(50, 100, 255, 100)))

        #self.fitInView(self.sceneRect())#, Qt.AspectRatioMode.)
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    base_line = np.array([0.531152017,0.739292161,180,150.57125,81.806875,30.016875,65.80125],dtype=np.float32)
    data = np.array([0.612903226, 0.833333333, 180, 150.15, 88.54, 36.26, 72.61],dtype=np.float32)  # Sample data points for the radar chart
    
    scene = RadarChart(data,base_line)
    
    main = QMainWindow()
    central_widget = QWidget()
    main.setCentralWidget(central_widget)
    
    main.layout = QVBoxLayout(central_widget)
    
    view = RadarChart(data,base_line)
    main.layout.addWidget(view)
    main.show()
    
    sys.exit(app.exec_())