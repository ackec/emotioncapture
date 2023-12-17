from pathlib import Path
import umap
import numpy as np
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
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

#import hdbscan
import sklearn.cluster as cluster
import matplotlib.colors
import matplotlib.pyplot as plt
from validation import ImageViewer
from data import ProjectData
# from config import DIALOG_WIDTH, DIALOG_HEIGHT, PROCESSING_GIF_PATH

# List of packages that are allowed to be imported
__all__ = ["MouseFeatures", "VisualisationWidget", "RadarPlot"]

class MouseData():
    def __init__(self):
        self.columns = ['eye_opening', 'ear_opening', 'ear_angle', 'ear_pos_vec', 'snout_pos', 'mouth_pos', 'face_incl']


    def calculate_mousedata(self, project):
        self.df = project.project_data
        self.radardata = self.df[self.columns]


        video_names = self.df['Video_Name'].unique()
        self.df_mean = pd.DataFrame(columns=self.df.columns)

        for video_name in video_names:
            video_df = self.df[self.df["Video_Name"] == video_name]
            stimulis = video_df['Stimuli'].unique()
            for stimuli in stimulis:
                index = len(self.df_mean)
                self.df_mean.loc[index] = video_df[video_df["Stimuli"]==stimuli].iloc[0]
                self.df_mean.loc[index, self.columns] = video_df[video_df["Stimuli"]==stimuli][self.columns].mean()


        mice_names = self.df['Mouse_Name'].unique()
        self.mice_mean_baseline = pd.DataFrame(columns=self.df.columns)

        for mice_name in mice_names:
            mouse_df = self.df[self.df["Mouse_Name"] == mice_name]
            stimulis = mouse_df['Stimuli'].unique()
            index = len(self.mice_mean_baseline)
            self.mice_mean_baseline.loc[index] =  mouse_df[mouse_df["Stimuli"]==stimuli].iloc[0]
            self.mice_mean_baseline.loc[index, self.columns] = mouse_df[mouse_df["Stimuli"] == "baseline"][self.columns].mean()


        self.baseline = self.mice_mean_baseline        

        self.baseline_derivation = pd.DataFrame()
        for mouse_name in mice_names:
            baseline_derivation = self.df_mean[self.df_mean["Mouse_Name"] == mouse_name][self.columns]\
                                 .div(self.mice_mean_baseline[self.mice_mean_baseline["Mouse_Name"] == mouse_name][self.columns].iloc[0])
            baseline_derivation[["Video_Name","Img_Path", "Frame_ID", "Stimuli", "Mouse_Name"]] = self.df_mean[["Video_Name","Img_Path", "Frame_ID", "Stimuli", "Mouse_Name"]]
            self.baseline_derivation = pd.concat([self.baseline_derivation, baseline_derivation])


        self.umap = umap.UMAP().fit_transform(self.df_mean[self.columns].values)
        self.baseline_derivation["umap_x"]=self.umap[:,0]
        self.baseline_derivation["umap_y"]=self.umap[:,1]




class VisualisationWidget(QWidget):

    def __init__(self, file_list):
        # self.project = project
        super().__init__()
        self.file_list = file_list

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        
        # self.file_list.currentItemChanged.connect(self.clicked_image)
        self.file_list.tree_view.clicked.connect(self.clicked_tree)

        self.main_layout = QHBoxLayout(self)
        col2_layout = QVBoxLayout()
        col2_row2_layout = QHBoxLayout()

        self.mouse_features = MouseFeatures()
        self.mousedata = MouseData()
        self.line_plot = LinePlot(self.mousedata)
        self.radar_plot = RadarPlot(self.mousedata, self.line_plot, self.mouse_features)
        self.scatter_plot = ScatterPlot(self.mousedata, self.radar_plot, self.mouse_features, self.line_plot)
        self.image_viewer = ImageViewer()

        col2_row2_layout.addWidget(self.radar_plot)
        col2_row2_layout.addWidget(self.mouse_features)

        col2_layout.addWidget(self.scatter_plot)
        col2_layout.addWidget(self.line_plot)

        col2_layout.addLayout(col2_row2_layout)

        self.main_layout.addLayout(col2_layout)
        # self.main_layout.addLayout(col2_row2_layout)

        self.setLayout(self.main_layout)
        self.has_init = False

    def init_visualisation(self, project, plot_nr):
        self.mousedata.calculate_mousedata(project)
        self.line_plot.init_line_plot()
        self.radar_plot.init_radar_plot()
        self.scatter_plot.init_scatter_plot(plot_nr)
        self.project = project
        self.has_init = True
    
    def change_cluster(self, plot_nr):
        self.scatter_plot.init_scatter_plot(plot_nr)


    def clicked_tree(self,index):
        file_name = index.model().fileName(index)
        """ 
        ## Use this to check if the selected item was an image
        ext = os.path.splitext(file_name)[-1]
        if ext not in ACCEPTED_TYPES:   ##Check if selected item is an image (not folder))
            return
        """
        
        #self.df["Img_Name"]
        print(f"CLICK: {file_name}")
        if self.has_init:
            clicked_data = self.mousedata.df[self.mousedata.df["Img_Path"] == file_name]
            self.radar_plot.update_radar_plot_file(clicked_data)
            self.scatter_plot.set_marker_to_image(clicked_data)
            self.line_plot.set_lineplot_to_image(clicked_data)


    def clicked_image(self):
        item = self.file_list.currentItem()
        file_name = item.text()

        #self.df["Img_Name"]
        print(f"CLICK1: {file_name}")
        if self.has_init:
            clicked_data = self.mousedata.df[self.mousedata.df["Img_Path"] == file_name]
            self.radar_plot.update_radar_plot_file(clicked_data)

class PlaceHolder(QLabel):
    """ Placeholder widget while app is being developed """

    def __init__(self, name: str, parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setText(name)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

class RadarPlot(QMainWindow):
    def __init__(self, mousedata, lineplot, mouse_features):
        super().__init__()
        self.mousedata = mousedata
        self.mouse_features = mouse_features
        self.setWindowTitle("Radar Plot")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.lineplot = lineplot

    def init_radar_plot(self):
        self.data = self.mousedata.baseline_derivation[self.mousedata.columns]
        # self.baseline = pd.concat((start,end)).mean(axis=0)
        self.upper = self.data.mean() + self.data.sem()
        self.lower = self.data.mean() - self.data.sem()
        self.sample = self.data.mean()
        print(self.sample)
        self.ax = self.figure.add_subplot(111, polar=True)
        self.radar_plot()
        self.canvas.draw()

    def update_radar_plot(self, clicked_index):
        self.sample = self.mousedata.baseline_derivation.loc[clicked_index][self.mousedata.columns]
        print(self.sample)
        self.ax.clear()
        self.radar_plot()
        # self.ax.set_ylim(self.sample.min()-0.2, self.sample.max()+0.2)
        self.ax.set_ylim(0, 2)

        self.canvas.draw()
        #self.ax.figure.savefig(f"radarplot_{clicked_index}.pdf")

    def update_radar_plot_file(self, clicked_data):
        if len(clicked_data) > 0:
            file_name = clicked_data.squeeze()["Img_Path"]
            clicked_data = self.mousedata.df.loc[clicked_data.index[0]]
            #print(clicked_data)
            mouse_name = clicked_data["Mouse_Name"]

            normalized_data = clicked_data[self.mousedata.columns] / self.mousedata.mice_mean_baseline[self.mousedata.mice_mean_baseline["Mouse_Name"] == mouse_name][self.mousedata.columns]
            self.sample = normalized_data.loc[0]
            # self.sample = self.mousedata.df[self.mousedata.df["Mouse_Name"] == clicked_data["Mouse_Name"]]
            #print(self.sample)
            self.ax.clear()
            self.radar_plot()
            # self.ax.set_ylim(self.sample.min()-0.2, self.sample.max()+0.2)
            self.ax.set_ylim(0, 2)
            #print(normalized_data)
            info_text = f"Eye Opening: {clicked_data['eye_opening']:.2f},  {self.sample['eye_opening']:.2%} \n"\
                f"Ear Opening: {clicked_data['ear_opening']:.2f},  {self.sample['ear_opening']:.2%}\n"\
                f"Ear Angle: {clicked_data['ear_angle']:.2f},  {self.sample['ear_angle']:.2%}\n"\
                f"Ear Position: {clicked_data['ear_pos_vec']:.2f},  {self.sample['ear_pos_vec']:.2%}\n"\
                f"Snout Position: {clicked_data['snout_pos']:.2f},  {self.sample['snout_pos']:.2%}\n"\
                f"Mouth Position: {clicked_data['mouth_pos']:.2f},  {self.sample['mouth_pos']:.2%}\n"\
                f"Face inclination: {clicked_data['face_incl']:.2f},  {self.sample['face_incl']:.2%}\n"\
                f"Video Name: {clicked_data['Video_Name']} \n"\
                f"File Name: {file_name} \n"\
                f"Stimuli: {clicked_data['Stimuli']}\n"\

            self.mouse_features.setText(info_text)

            self.canvas.draw()



    def radar_plot(self):
        rad_linspace = np.linspace(0, 2 * np.pi, len(self.mousedata.columns), endpoint=False)
        polygons = [
            Polygon(list(zip(rad_linspace, self.upper)), facecolor='darkgrey', alpha=0.5),
            Polygon(list(zip(rad_linspace, self.lower)), facecolor='white',  alpha=0.7),
            Polygon(list(zip(rad_linspace, [1]*7)), edgecolor='black',  linewidth=1, facecolor='none'),
            Polygon(list(zip(rad_linspace, self.sample)), edgecolor='blue', label="Clicked sample", linewidth=1, facecolor='none'),
        ]

        pc = PatchCollection(polygons, match_original=True)
        self.ax.add_collection(pc)
        self.ax.set_ylim(0.85, 1.15)
        self.ax.set_xticks(rad_linspace)
        self.ax.set_xticklabels(self.mousedata.columns)
        self.ax.set_yticklabels([])

        #legend_labels = ['Experiment +- SEM', 'Clicked sample', 'Normalized baseline']
        #legend_handles = [self.ax.plot([], [], color='darkgrey', alpha=0.5)[0],
                        #   ax.plot([], [], color='white', alpha=0.7)[0],
                        #  self.ax.plot([], [], color='blue', linewidth=1)[0],
                        #  self.ax.plot([], [], color='black', linewidth=1)[0]]

        #leg = self.ax.legend(legend_handles, legend_labels, loc='lower left', bbox_to_anchor=(1, 0.7))
        #leg.set_draggable(True)


        self.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        if event.inaxes == self.figure.axes[0]:
            theta = ((event.xdata+np.pi/7) % (2 * np.pi))-np.pi/7
            closest_index = np.argmin(np.abs(np.linspace(0, 2 * np.pi, len(self.mousedata.columns), endpoint=None) - theta))
            self.lineplot.on_radar_pick(closest_index)

class ScatterPlot(QMainWindow):
    def __init__(self, mousedata, radar_plot, mouse_features, line_plot):
        super().__init__()
        self.mousedata = mousedata
        self.radar_plot = radar_plot
        self.mouse_features = mouse_features
        self.line_plot = line_plot

        self.setWindowTitle("Scatter Plot")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)


    def features_in_range(self):
        self.features["eye_oppening"].between(0.51,0.79)
        self.features["ear_oppening"].between(1/0.65, 1/0.41)

        pass

        # Eye opening: 0.51-0.79 (ratio width/length)
        # Ear opening: 0.41-0.65 (ratio width/length)
        # Ear position: 131-158 (degrees)
        # Ear angle: probably better estimated by a present/absent indicator, otherwise most often at 180 degrees.
        # Snout position: 72-90 (degrees)
        # Mouth position: 28-39 (degrees)
        # Face inclination: 62-75 (degrees)

    def init_scatter_plot(self, plot_nr):
        self.features = self.mousedata.df

        # if "umap_x" not in self.features:
        #     standard_embedding = umap.UMAP(random_state=10).fit_transform(self.features[self.mousedata.columns])
        #     self.features["umap_x"]=standard_embedding[:,0]
        #     self.features["umap_y"]=standard_embedding[:,1]
        #     self.features.to_csv("output_test.csv")
        # self.umap = self.features[["umap_x", "umap_y"]].values

        self.last_clicked_index = None
        # self.stim_start = self.mousedata.stimuli_start
        # self.stim_end = self.mousedata.stimuli_end
        
        cmap = ['blue', 'green', 'purple', 'orange', 'brown', 'teal', 'darkgreen', 'chocolate', 'cyan', 'red', 'pink']
        # clustered = (hdbscan_labels >= 0)
        #plot = 1
        ax = self.figure.add_subplot(111)
        if plot_nr == 0:
            hdbscan_labels = cluster.HDBSCAN(min_samples=1, min_cluster_size=2).fit_predict(self.mousedata.df_mean[self.mousedata.columns].values)
            self.colous = np.array([cmap[label] for label in hdbscan_labels])
        elif plot_nr == 1:
            kmeans_labels = cluster.KMeans(n_clusters=2).fit_predict(self.mousedata.umap)
            self.colous = np.array([cmap[label] for label in kmeans_labels])


        is_baseline = self.mousedata.df_mean["Stimuli"] == "baseline"
        is_experiment = self.mousedata.df_mean["Stimuli"] == "experiment"
        is_recovery = self.mousedata.df_mean["Stimuli"] == "recovery"


        self.scatter1 = ax.scatter(*self.mousedata.umap[is_baseline].T, c=[*self.colous[is_baseline]], marker="^", label='Baseline', s=10, picker=10)
        self.scatter2 = ax.scatter(*self.mousedata.umap[is_experiment].T, c=[*self.colous[is_experiment]], marker="x", label='Experiment', s=10, picker=10)
        self.scatter3 = ax.scatter(*self.mousedata.umap[is_recovery].T, c=[*self.colous[is_recovery]], marker="o", label='Recovery', s=10, picker=10)

        # ax.set_xlabel("X-axis")
        # ax.set_ylabel("Y-axis")
        # ax.set_title("Scatter Plot")

        handles, labels = ax.get_legend_handles_labels()
        leg = ax.legend(handles=handles, labels=labels)
        leg.set_draggable(True)
        [lgd.set_color('black') for lgd in leg.legendHandles]

        self.canvas.mpl_connect('pick_event', self.on_pick)
        self.canvas.draw()

    def set_marker_to_image(self, clicked_data):
        print(clicked_data)
        hej=clicked_data.squeeze()
        index = self.mousedata.df_mean[(self.mousedata.df_mean['Video_Name'] == hej["Video_Name"]) & (self.mousedata.df_mean['Stimuli'] == hej["Stimuli"])].index
        if len(index) > 0:
            index = index[0]
            # self.mousedata.df_mean[self.mousedata.df_mean['Stimuli'] == clicked_data["Stimuli"]].index.get_loc(index)
            # index = clicked_data["Video_Name"]
            self.set_marker(index)
            self.last_clicked_index = index
            self.canvas.draw()


    def set_marker(self, index):
        # if self.last_clicked_index is None:
        #     return
        if self.last_clicked_index is not None:
            last_stimuli = self.mousedata.df_mean.loc[self.last_clicked_index]["Stimuli"]
            old_index_in_category = self.mousedata.df_mean[self.mousedata.df_mean['Stimuli'] == last_stimuli].index.get_loc(self.last_clicked_index)

            if last_stimuli == "baseline":
            # if self.last_clicked_index < self.stim_start:
                self.scatter1._facecolors[old_index_in_category] = matplotlib.colors.to_rgba(self.colous[self.last_clicked_index]) 
            elif last_stimuli == "experiment":
                self.scatter2._facecolors[old_index_in_category] = matplotlib.colors.to_rgba(self.colous[self.last_clicked_index])
            else:
                self.scatter3._facecolors[old_index_in_category] = matplotlib.colors.to_rgba(self.colous[self.last_clicked_index])

            
        # category = self.mousedata.df_mean.iloc[closest_index-1]['Stimuli']
        clicked_stimuli = self.mousedata.df_mean.iloc[index]["Stimuli"]
        old_index_in_category = self.mousedata.df_mean[self.mousedata.df_mean['Stimuli'] == clicked_stimuli].index.get_loc(index)

        if clicked_stimuli == "baseline":
            self.scatter1._facecolors[old_index_in_category] = (0, 1, 0, 1)
        elif clicked_stimuli == "experiment":
            self.scatter2._facecolors[old_index_in_category] = (0, 1, 0, 1)
        else:
            self.scatter3._facecolors[old_index_in_category] = (0, 1, 0, 1)
        

    def on_pick(self, event):
        if event.mouseevent.name == 'button_press_event':
            ind = event.ind
            if len(ind) > 0:
                distances = np.sqrt((self.mousedata.umap[:,0] - event.mouseevent.xdata)**2 + (self.mousedata.umap[:,1] - event.mouseevent.ydata)**2)
                closest_index = np.argmin(distances)

                self.set_marker(closest_index)

                if closest_index == self.last_clicked_index:
                    return

                self.last_clicked_index = closest_index
                x_clicked = self.mousedata.umap[self.last_clicked_index][0]
                y_clicked = self.mousedata.umap[self.last_clicked_index][1]
                self.radar_plot.update_radar_plot(self.last_clicked_index)
                print(f"Clicked Point: ({x_clicked:.2f}, {y_clicked:.2f}), from frame {self.features['Frame_ID'][self.last_clicked_index]}, and with path: {self.features['Img_Path'][self.last_clicked_index]}")
                
                percental_change = self.mousedata.baseline_derivation.iloc[self.last_clicked_index]
                features = self.mousedata.df_mean.loc[self.last_clicked_index]
                # features = self.features.iloc[self.last_clicked_index]
                # percental_change = features / self.mousedata.baseline.mean()
                info_text = f"Eye Opening: {features['eye_opening']:.2f},  {percental_change['eye_opening']:.2%} \n"\
                        f"Ear Opening: {features['ear_opening']:.2f},  {percental_change['ear_opening']:.2%}\n"\
                        f"Ear Angle: {features['ear_angle']:.2f},  {percental_change['ear_angle']:.2%}\n"\
                        f"Ear Position: {features['ear_pos_vec']:.2f},  {percental_change['ear_pos_vec']:.2%}\n"\
                        f"Snout Position: {features['snout_pos']:.2f},  {percental_change['snout_pos']:.2%}\n"\
                        f"Mouth Position: {features['mouth_pos']:.2f},  {percental_change['mouth_pos']:.2%}\n"\
                        f"Face inclination: {features['face_incl']:.2f},  {percental_change['face_incl']:.2%}\n"\
                        f"Colour: {self.colous[self.last_clicked_index]}\n"\
                        f"Video Name: {features['Video_Name']} \n"\
                        f"Stimulation: {features['Stimuli']} \n"\
                        f"Image index: {features['Frame_ID']:.2f} \n"\

                self.line_plot.mark_point(self.last_clicked_index)
                self.mouse_features.setText(info_text)
            self.canvas.draw()

class LinePlot(QMainWindow):
    def __init__(self, mousedata):
        super().__init__()
        self.mousedata = mousedata
        self.setWindowTitle("Line Plot")
        self.setGeometry(100, 100, 800, 600)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.dot = None
        self.lines = {}
        self.is_video_plot = False


    def set_lineplot_to_image(self, clicked_data):
        video_name = clicked_data.squeeze()["Video_Name"]
        video_df = self.mousedata.df[self.mousedata.df["Video_Name"] == video_name]
        mouse_name = video_df["Mouse_Name"].iloc[0]
        self.data = video_df[self.mousedata.columns]\
                                 .div(self.mousedata.mice_mean_baseline[self.mousedata.mice_mean_baseline["Mouse_Name"] == mouse_name][self.mousedata.columns].iloc[0])
        self.ax.clear()
        for col in self.data.columns:
            line, = self.ax.plot(self.data.index, self.data[col], label=col)
            self.lines[col] = line
        self.is_video_plot = True
        leg = self.ax.legend()
        self.ax.set_ylim(0.5, 1.5)
        leg.set_draggable(True)

        if self.dot:
            self.dot.pop(0).remove()
        index = (video_df.reset_index()["Img_Path"] == clicked_data.squeeze()["Img_Path"]).idxmax()
        line = self.figure.axes[0].lines[0]
        x = line.get_xdata()[index]
        y=1
        self.dot = self.ax.plot(x, y, 'ro', markersize=8)

        self.canvas.draw()



    def init_line_plot(self):
        self.data = self.mousedata.baseline_derivation[self.mousedata.columns]
        for col in self.data.columns:
            line, = self.ax.plot(self.data.index, self.data[col], label=col)
            self.lines[col] = line
        leg = self.ax.legend()
        self.ax.set_ylim(0.5, 1.5)
        leg.set_draggable(True)
        self.canvas.draw()

    def mark_point(self, index):
        if self.is_video_plot:
            self.ax.clear()
            self.init_line_plot()
            self.is_video_plot = False

        if self.dot:
            self.dot.pop(0).remove()

        line = self.figure.axes[0].lines[0]
        x = line.get_xdata()[index]
        # y = line.get_ydata()[index]
        y=1
        self.dot = self.ax.plot(x, y, 'ro', markersize=8)
        self.canvas.draw()

    def on_radar_pick(self, index):
        label = self.mousedata.columns[index]
        line = self.lines.get(label)
        if line:
            line.set_visible(not line.get_visible())
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
        self.setMaximumWidth(800)
        self.setMinimumWidth(400)
        for key,value in self.info_dict.items():
            temp_text += "{} \t \t \t {} \n".format(key,value)
            
        self.setText(temp_text)
        self.setLayout(self.info_layout)
