from pathlib import Path
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import (QLabel, QSizePolicy, QFrame, QDialog, QWidget,
                             QVBoxLayout, QPushButton, QStackedWidget, QSizePolicy,
                             QHBoxLayout)

# from config import DIALOG_WIDTH, DIALOG_HEIGHT, PROCESSING_GIF_PATH
from PyQt5.QtWidgets import QLabel, QSizePolicy, QFrame, QWidget

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

import hdbscan
import sklearn.cluster as cluster
import matplotlib.colors

# from config import DIALOG_WIDTH, DIALOG_HEIGHT, PROCESSING_GIF_PATH

# List of packages that are allowed to be imported
__all__ = ["ImageFileList", "MouseFeatures",
           "VisualisationWidget", "RadarPlot"]

class VisualisationWidget(QWidget):
    """ Placeholder widget while app is being developed """

    def __init__(self, name: str):
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.main_layout = QHBoxLayout(self)
        col1_layout = QHBoxLayout()
        col2_layout = QVBoxLayout(self)
        col2_row2_layout = QHBoxLayout(self)

        col2_row2_layout.addWidget(RadarPlot())
        col2_row2_layout.addWidget(MouseFeatures())
        col1_layout.addWidget(ImageFileList())
        col2_layout.addWidget(ScatterPlot("test"))
        col2_layout.addLayout(col2_row2_layout)

        self.main_layout.addLayout(col1_layout)
        self.main_layout.addLayout(col2_layout)
        self.main_layout.addLayout(col2_row2_layout)

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
    def __init__(self, csv_features_filepath="../Feature_extracion/output/mouse_features.csv", stimuli_start=100, stimuli_end=200):
        super().__init__()

        self.setWindowTitle("Radar Plot")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.columns = ['eye_oppening', 'ear_oppening', 'ear_angle', 'ear_pos_vec', 'snout_pos', 'mouth_pos', 'face_incl']
        df = pd.read_csv(csv_features_filepath)
        self.radardata = df[self.columns]

        self.stimuli_start = stimuli_start
        self.stimuli_end = stimuli_end

        self.baseline = self.radardata.iloc[:stimuli_start]
        self.stimulation = self.radardata.iloc[stimuli_start: stimuli_end]/self.baseline.mean()
        self.recovery = self.radardata.iloc[stimuli_end:]
        # self.baseline = pd.concat((start,end)).mean(axis=0)
        self.upper = self.stimulation.mean() + self.stimulation.sem()
        self.lower = self.stimulation.mean() - self.stimulation.sem()
        self.sample = self.stimulation.mean()
        print(self.sample)
        self.init_radar_plot()

    def init_radar_plot(self):
        ax = self.figure.add_subplot(111, polar=True)
        self.radar_plot(ax)
        self.canvas.draw()

    def update_radar_plot(self, clicked_index):
        self.sample = self.radardata.iloc[clicked_index] / self.baseline.mean()
        print(self.sample)
        ax = self.figure.add_subplot(111, polar=True)
        ax.clear()
        self.radar_plot(ax)
        ax.set_ylim(self.sample.min()-0.02, self.sample.max()+0.02)
        self.canvas.draw()

    def radar_plot(self, ax):
        rad_linspace = np.linspace(0, 2 * np.pi, len(self.columns), endpoint=False)

        polygons = [
            Polygon(list(zip(rad_linspace, self.upper)), facecolor='darkgrey', alpha=0.5),
            Polygon(list(zip(rad_linspace, self.lower)), facecolor='white', alpha=0.7),
            Polygon(list(zip(rad_linspace, [1]*7)), edgecolor='black', linewidth=1, facecolor='none'),
            Polygon(list(zip(rad_linspace, self.sample)), edgecolor='blue', linewidth=1, facecolor='none'),
        ]

        pc = PatchCollection(polygons, match_original=True)
        ax.add_collection(pc)

        ax.set_ylim(0.85, 1.15)
        ax.set_xticks(rad_linspace)
        ax.set_xticklabels(self.columns)
        ax.set_yticklabels([])



class ScatterPlot(QMainWindow):
    def __init__(self, radar_plot):
        super().__init__()

        self.setWindowTitle("Scatter Plot")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)


        self.features = pd.read_csv('../Feature_extracion/output/mouse_features.csv')
        self.umap = self.features[["umap_x", "umap_y"]].values

        self.last_clicked_index = None
        self.stim_start = 100
        self.stim_end = 200
        self.init_scatter_plot()
        self.radar_plot = radar_plot

    def init_scatter_plot(self):
        hdbscan_labels = hdbscan.HDBSCAN(min_samples=10, min_cluster_size=12).fit_predict(self.umap)
        kmeans_labels = cluster.KMeans(n_clusters=3).fit_predict(self.umap)

        cmap = ['red', 'blue', 'green', 'pink', 'purple', 'orange', 'brown', 'teal', 'darkgreen', 'chocolate', 'cyan']
        # clustered = (hdbscan_labels >= 0)
        ax = self.figure.add_subplot(111)
        self.colous = [cmap[label] for label in hdbscan_labels]
        self.scatter1 = ax.scatter(self.umap[:self.stim_start, 0], self.umap[:self.stim_start, 1], c=self.colous[:self.stim_start], marker="^", label='Baseline', s=10, picker=10)
        self.scatter2 = ax.scatter(self.umap[self.stim_start:self.stim_end, 0], self.umap[self.stim_start:self.stim_end, 1], c=self.colous[self.stim_start:self.stim_end], marker="x", label='Stumulation', s=10, picker=10)
        #self.scatter3 = ax.scatter(self.umap[self.stim_end:, 0], self.umap[self.stim_end:, 1], c=self.colous[self.stim_end:], marker="o", label='Recovery', s=10, picker=10)

        # ax.set_xlabel("X-axis")
        # ax.set_ylabel("Y-axis")
        # ax.set_title("Scatter Plot")

        handles, labels = ax.get_legend_handles_labels()
        leg = ax.legend(handles=handles, labels=labels)
        [lgd.set_color('black') for lgd in leg.legendHandles]

        self.canvas.mpl_connect('pick_event', self.on_pick)
        self.canvas.draw()

    def on_pick(self, event):
        if event.mouseevent.name == 'button_press_event':
            ind = event.ind
            if len(ind) > 0:
                distances = np.sqrt((self.umap[:,0] - event.mouseevent.xdata)**2 + (self.umap[:,1] - event.mouseevent.ydata)**2)
                closest_index = np.argmin(distances)

                if self.last_clicked_index is not None:
                    if self.last_clicked_index < self.stim_start:
                        self.scatter1._facecolors[self.last_clicked_index] = matplotlib.colors.to_rgba(self.colous[self.last_clicked_index]) 
                    elif self.last_clicked_index < self.stim_end:
                        self.scatter2._facecolors[self.last_clicked_index - self.stim_start] = matplotlib.colors.to_rgba(self.colous[self.last_clicked_index])
                    else:
                        self.scatter3._facecolors[self.last_clicked_index - self.stim_end] = matplotlib.colors.to_rgba(self.colous[self.last_clicked_index])

                if closest_index < self.stim_start:
                    self.scatter1._facecolors[closest_index] = (0, 1, 0, 1)
                elif closest_index < self.stim_end:
                    self.scatter2._facecolors[closest_index-self.stim_start] = (0, 1, 0, 1)
                else:
                    self.scatter3._facecolors[closest_index-self.stim_end] = (0, 1, 0, 1)
            
                if closest_index == self.last_clicked_index:
                    return

                self.last_clicked_index = closest_index
                x_clicked = self.umap[self.last_clicked_index][0]
                y_clicked = self.umap[self.last_clicked_index][1]
                self.radar_plot.update_radar_plot(self.last_clicked_index)
                print(f"Clicked Point: ({x_clicked:.2f}, {y_clicked:.2f}), from frame {self.features['Frame_ID'][self.last_clicked_index]}, and with path: {self.features['Img_Path'][self.last_clicked_index]}")
            self.canvas.draw()

class UMAPViewer(PlaceHolder):
    def __init__(self):
        super().__init__("UMAP Viewer")


class MouseFeatures(QLabel):
    def __init__(self):
        super().__init__("Mouse Features")
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        
        self.info_layout = QHBoxLayout()
        self.setAlignment(Qt.AlignCenter)
        self.info_dict = {"Mouse:":"Anonymouse",
                          "Gender:":"Male",
                          "Genotype:":"Opto",
                          "Image:":"Img_example.jpg",
                          "Profile Score:":0.89,
                          "Key Point Score":0.97}
        temp_text = ""
        for key,value in self.info_dict.items():
            temp_text += "{} \t \t \t {} \n".format(key,value)
            
        self.setText(temp_text)
        self.setLayout(self.info_layout)
