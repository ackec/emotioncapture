import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, os

# List of packages that are allowed to be imported
__all__ = ["TreeView"]

accepted_types = (".jpg",".tiff",".png",".exr",".psd")
ICON_SIZE = QSize(64,64)
project_name = "Test Project"

class IconProvider(QFileIconProvider):

    def __init__(self,widget) -> None:
        super().__init__()
        self.widget = widget
        
    def icon(self, type: QFileIconProvider.IconType):

        fn = type.filePath()

        if fn.endswith(accepted_types):
            a = QPixmap(ICON_SIZE)
            a.load(fn)
            
            if True:    ##Add check of scores
                ## Add warning triangle
                warning = QPixmap()
                warning.load("warning.png")
                
                painter = QPainter()
                painter.begin(a)
                painter.drawPixmap(QPoint(),warning)
                painter.end()
            
            return QIcon(a)
        else:
            return super().icon(type)
        
class TreeView(QWidget):

    def __init__(self):
    
        QWidget.__init__(self)
        
        
        self.tree_view = QTreeView()
        self.tree_view.setUniformRowHeights(False)
        #self.tree_view.setItemDelegate
        self.tree_view.setIconSize(ICON_SIZE)
        
        # Creating a QFileSystemModel
        self.model = QFileSystemModel()
        self.model.setIconProvider(IconProvider(self))
        current = os.getcwd() + "/Projects/test_project" ##BASE_PROJECT_DIRECTORY_PATH
        print(current)
        self.model.setRootPath(current)  # Set the root path to display the entire filesystem
        
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(current))

        self.tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        # Filter the files shown in the view
        filters = ['*.png', '*.jpg', '*.jpeg', '*.gif']  # Add more image formats if needed
        self.model.setNameFilters(filters)
        self.model.setNameFilterDisables(False)
        
        for i in range(1, self.tree_view.model().columnCount()):
            self.tree_view.header().hideSection(i)
            
       #self.tree_view.expand(self.model.index(os.getcwd() + "/Projects/test_project"))
        
        
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.openMenu)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("{}".format(project_name)))
        layout.addWidget(self.tree_view)
        self.setLayout(layout)
        
        self.create_label_menu()
        
    def create_label_menu(self):
        self.label_menu = QMenu()
        self.label = self.label_menu.addMenu(self.tr("Assign label"))
        
        
        self.new_label = self.label_menu.addAction(self.tr("Create new label"))
        self.new_label.triggered.connect(self.create_label)
    
    def openMenu(self, position):
    
        indexes = self.tree_view.selectedIndexes()
        
        ## Find level from root
        if len(indexes) > 0:
        
            level = 0
            index = indexes[0]
            while index.parent().isValid() and index.parent() != self.tree_view.rootIndex():
                index = index.parent()
                level += 1
                
        if level == 2:
            self.label_menu.exec_(self.tree_view.viewport().mapToGlobal(position))
   
    def create_label(self):
        label_dialog = LabelDialog()
        if label_dialog.label_name is not None:
            temp = self.label.addAction(label_dialog.label_name)
            temp.triggered.connect(lambda: self.assign_label(temp.text()))
    
    def assign_label(self,label):
        print(label)
        ##TODO assign the label
        indexes = self.tree_view.selectedIndexes()
        
        if len(indexes) > 1:
            for ind in indexes:
                item = ind.model().fileName(ind)
                print(item)
                
        elif len(indexes) == 1:
            indexes = indexes[0]
            item = indexes.model().fileName(indexes)
            print(item)
        else:
            return
    
    def select_folder(self):
        path = "C/Mouse"
        # Creating a QFileSystemModel
        self.model = QFileSystemModel()
        self.model.setIconProvider(IconProvider())
        #current = os.getcwd() + "/Projects/test_project" ##BASE_PROJECT_DIRECTORY_PATH
        #print(current)
        self.model.setRootPath(path)  # Set the root path to display the entire filesystem
        
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(path))
        
        #Filter the files shown in the view
        filters = ['*.png', '*.jpg', '*.jpeg', '*.gif']  # Add more image formats if needed
        self.model.setNameFilters(filters)
        self.model.setNameFilterDisables(False)
        
        
        for i in range(1, self.tree_view.model().columnCount()):
            self.tree_view.header().hideSection(i)

class LabelDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
    
        self.setWindowTitle("Create Label")
        self.label_name = None
        
        main_layout = QGridLayout()
        
        info_label = QLabel("Create Label:")
        
        self.create_label = QLineEdit()
        
        submit_button = QPushButton("Submit Label")
        submit_button.clicked.connect(self.submit)
        
        main_layout.addWidget(info_label,0,0)
        main_layout.addWidget(self.create_label,0,1)
        main_layout.addWidget(submit_button,1,1)
        self.setLayout(main_layout)
        
        self.exec()

    def submit(self):
        self.label_name = self.create_label.text()
        self.accept()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = TreeView()
    window.show()
    sys.exit(app.exec_())