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