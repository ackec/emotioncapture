from pathlib import Path
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import (QLabel, QSizePolicy, QFrame, QDialog, QWidget,
                             QVBoxLayout, QPushButton, QStackedWidget)

from config import DIALOG_WIDTH, DIALOG_HEIGHT
from PyQt5.QtWidgets import QLabel, QSizePolicy, QFrame, QWidget

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

from config import DIALOG_WIDTH, DIALOG_HEIGHT

# List of packages that are allowed to be imported
__all__ = ["ImageFileList",
           "VisualisationWidget", "RadarPlot"]

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


class RadarPlot(QMainWindow):
    def __init__(self):
        super().__init__()
        stimuli_start = 100
        stimuli_end = 200

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

        # Load data (replace 'your_file.csv' with your file path)
        self.radardata = pd.read_csv('output/mouse_features.csv')

        # Calculate upper and lower bounds
        start = self.radardata.iloc[:stimuli_start]
        end = self.radardata.iloc[stimuli_end:]
        self.baseline = pd.concat((start,end)).mean(axis=0)
        self.stimulation = self.radardata.iloc[stimuli_start: stimuli_end]/self.baseline

        self.upper = self.stimulation.mean(axis=0) + self.stimulation.sem(axis=0)
        self.lower = self.stimulation.mean(axis=0) - self.stimulation.sem(axis=0)
        self.init_radar_plot()

    def init_radar_plot(self):
        ax = self.figure.add_subplot(111, polar=True)
        self.radar_plot(ax)
        self.canvas.draw()

    def radar_plot(self, ax):
        parameters = list(self.radardata.columns)
        rad_linspace = np.linspace(0, 2 * np.pi, len(parameters), endpoint=False)
        # Plot polygons
        polygons = [
            Polygon(list(zip(rad_linspace, self.upper)), facecolor='darkgrey', alpha=0.5),

            Polygon(list(zip(rad_linspace, self.lower)), facecolor='white', alpha=0.7),
            Polygon(list(zip(rad_linspace, self.stimulation.mean(axis=0))), edgecolor='blue', linewidth=1, facecolor='none'),
            Polygon(list(zip(rad_linspace, [1]*7)), edgecolor='black', linewidth=1, facecolor='none'),
        ]

        pc = PatchCollection(polygons, match_original=True)
        ax.add_collection(pc)

        # Set axis labels and limits
        # ax.set_xlabel("Facial profile response to stimulation X")
        # ax.set_ylabel("Proportional change from baseline")
        ax.set_ylim(0, 1.1)

        ax.set_xticks(rad_linspace)
        ax.set_xticklabels(parameters)
        ax.set_yticklabels([])


class UMAPViewer(PlaceHolder):
    def __init__(self):
        super().__init__("UMAP Viewer")


class MouseFeatures(PlaceHolder):
    def __init__(self):
        super().__init__("Mouse Features")
