import sys
import math
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPolygonF, QFont
from PyQt5.QtCore import Qt, QPoint


class RadarChart(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Radar Chart')
        self.setGeometry(100, 100, 400, 400)

        self.base_line = np.array([10,10,10,10,10,10,10],dtype=np.float32)
        self.data = [9, 8, 11, 12, 10, 9, 10]  # Sample data points for the radar chart
        self.labels = ['Eye Opening', 'Ear Position', 'Ear Opening', 'Ear Angle', 
                       'Snout Position','Mouth Position','Face Inclination']  # Labels for each axis

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define the center and radius of the radar chart
        center = self.rect().center()
        radius = min(self.width(), self.height()) / 3

        # Draw the axes
        num_points = len(self.base_line)
        angle = 2 * math.pi / num_points
        points_list = []
        for i in range(num_points):
            x = center.x() + radius * math.sin(i * angle)
            y = center.y() + radius * math.cos(i * angle)
            
            painter.drawLine(center.x(), center.y(), x, y)
            points_list.append(QPoint(x,y))
        
        for i in range(len(points_list)):
            point = points_list[i]
            prev_point = points_list[i-1]
            
            painter.drawLine(prev_point, point)
            
            
        # Draw the axis labels
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)
        offset = 50
        for i, label in enumerate(self.labels):
            x = center.x() + (radius + offset) * math.sin(i * angle)
            y = center.y() + (radius + offset) * math.cos(i * angle)
            text_rect = painter.fontMetrics().boundingRect(label)
            painter.drawText(QPoint(x - text_rect.width() / 2, y + text_rect.height() / 2), label)


        # Draw the data polygon
        painter.setBrush(QColor(50, 150, 200, 100))  # Set color and transparency for the data area
        painter.setPen(Qt.NoPen)

        data_polygon = QPolygonF()
        for i, value in enumerate(self.data):
            x = (value/self.base_line[i])*radius * math.sin(i * angle)
            y = (value/self.base_line[i])*radius * math.cos(i * angle)
            
            data_polygon.append(center + QPoint(x, y))

        painter.drawPolygon(data_polygon)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RadarChart()
    window.show()
    sys.exit(app.exec_())