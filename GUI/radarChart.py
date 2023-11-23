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
        self.drawRadar()
        
        
        self.setScene(self.radar_scene)

    def drawRadar(self):
        #self.scene.clear()

        center = self.sceneRect().center()
        center = QPointF(center)
        radius = min(self.sceneRect().width(), self.sceneRect().height()) / 3
        
        num_points = len(self.data)
        angle = 2 * math.pi / num_points
        nr_edges = 3
        points_list = []
        # Draw the axes and labels
        for i in range(num_points):
            point = center + QPointF(radius * math.sin(i * angle),radius * math.cos(i * angle))
            
            line = QLineF(center, point)
            self.radar_scene.addLine(line)
            points_list.append(point)
        
        for i in range(len(points_list)):
            point = points_list[i]
            prev_point = points_list[i-1]
            
            line = QLineF(prev_point, point)
            self.radar_scene.addLine(line)
            
            for j in range(1,nr_edges):
                line = QLineF(center+(point-center)*j/nr_edges,center+(prev_point-center)*j/nr_edges)
                self.radar_scene.addLine(line)
              
        for i, label in enumerate(self.labels):
            point1 = center + radius * QPointF(math.sin(i * angle),math.cos(i * angle))
            point2 = center + radius * QPointF(math.sin((i + 1) * angle),math.cos((i + 1) * angle))
            line = QLineF(point1,point2)
            
            self.radar_scene.addLine(line)

            text = QGraphicsTextItem(label)
            text.setPos(center.x() + 1.3*radius * math.sin((i + 1) * angle) - 10,center.y() + 1.3*radius * math.cos((i + 1) * angle) - 10)
            self.radar_scene.addItem(text)
        
        # Draw the data polygon
        data_polygon = QPolygonF()
        for i, value in enumerate(self.data):
            x = (value/self.base_line[i])*radius * math.sin(i * angle)
            y = (value/self.base_line[i])*radius * math.cos(i * angle)
            data_polygon.append(center + QPointF(x, y))

        poly = self.radar_scene.addPolygon(QtGui.QPolygonF(data_polygon))
        poly.setBrush(QtGui.QBrush(QtGui.QColor(50, 150, 200, 100)))

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