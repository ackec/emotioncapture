from enum import Enum
import sys
from PyQt5.QtWidgets import (QLabel, QSizePolicy, QFrame, QDialog, QWidget,
                             QVBoxLayout, QPushButton, QStackedWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

from config import DIALOG_WIDTH, DIALOG_HEIGHT, PROCESSING_GIF_PATH

# List of packages that are allowed to be imported
__all__ = ["ImageFileList",
           "VisualisationWidget"]

class VisualisationWidget(QWidget):
    """ Placeholder widget while app is being developed """

    def __init__(self, name: str):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.main_layout = QVBoxLayout()

        text = QLabel()
        text.setText(name)
        text.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.main_layout.addWidget(text)

        btn = QPushButton("Switch")
        btn.clicked.connect(lambda: self.parent().parent().switch(next))
        self.main_layout.addWidget(btn)

        self.setLayout(self.main_layout)

class PlaceHolder(QLabel):
    """ Placeholder widget while app is being developed """

    def __init__(self, name: str, parent: QWidget | None = None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setText(name)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)


class ImageFileList(PlaceHolder):
    def __init__(self):
        super().__init__("File list")


class RadarPlot(PlaceHolder):
    def __init__(self):
        super().__init__("Radar Plot")

        # Set up the main window
        self.setWindowTitle("Radar Plot")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Load data (replace 'clipboard' with your file path)
        self.radardata = pd.read_clipboard(sep='\t', header=True)

        # Initialize the radar plot
        self.init_radar_plot()

    def init_radar_plot(self):
        # Create axis for the figure
        ax = self.figure.add_subplot(111, polar=True)

        # Plot the radar
        self.radar_plot(ax)

        # Draw the canvas
        self.canvas.draw()

    def radar_plot(self, ax):
        parameter = self.radardata['parameter']
        stimulation = self.radardata['stimulation']
        baseline = self.radardata['baseline']
        upper = self.radardata['upper']
        lower = self.radardata['lower']

        # Plot polygons
        polygons = [
            Polygon(list(zip(parameter, upper)), facecolor='darkgrey', alpha=0.5),
            Polygon(list(zip(parameter, lower)), facecolor='white', alpha=0.7),
            Polygon(list(zip(parameter, baseline)), edgecolor='black', linewidth=1, facecolor='none'),
        ]

        pc = PatchCollection(polygons, match_original=True)
        ax.add_collection(pc)

        # Set axis labels and limits
        ax.set_xlabel("Facial profile response to stimulation X")
        ax.set_ylabel("Proportional change from baseline")
        ax.set_ylim(-0.25, 0.2)


class UMAPViewer(PlaceHolder):
    def __init__(self):
        super().__init__("UMAP Viewer")


class MouseFeatures(PlaceHolder):
    def __init__(self):
        super().__init__("Mouse Features")
