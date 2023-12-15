import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, os
from config import BASE_PROJECT_DIRECTORY_PATH,ACCEPTED_TYPES,ICON_SIZE

# List of packages that are allowed to be imported
__all__ = ["FileList"]

project_name = "Test Project"

class IconProvider(QFileIconProvider):

    def __init__(self,file_list) -> None:
        super().__init__()
        self.file_list = file_list
        
    def icon(self, type: QFileIconProvider.IconType):

        fn = type.filePath()

        if fn.endswith(ACCEPTED_TYPES):
            a = QPixmap(QSize(ICON_SIZE,ICON_SIZE))
            a.load(fn)
        
            ## Add warning triangle
            warning = QPixmap()
            warning.load("GUI/res/warning.png")
            
            try: ## Get dataframe
                name = os.path.basename(fn)
                data = self.file_list.main.project.project_data
                warn_flag = data[data["Img_Path"] == name]["warn_flag"]
                warn_flag = warn_flag.iloc[-1]
            except: ## No data found
                warn_flag = False
        
            if warn_flag:
                painter = QPainter()
                painter.begin(a)
                painter.drawPixmap(QPoint(),warning)
                painter.end()
        
            return QIcon(a)
        else:
            return super().icon(type)
        
class FileList(QWidget):

    def __init__(self, main=None,image_viewer=None):
    
        QWidget.__init__(self)
        
        self.current_index = None
        self.siblings = 0
        
        self.image_viewer = image_viewer
        #self.data = None
        if main is not None:
            self.main = main
                
        
        self.tree_view = QTreeView()
        self.tree_view.setUniformRowHeights(False)
        #self.tree_view.setItemDelegate
        self.tree_view.setIconSize(QSize(ICON_SIZE,ICON_SIZE))
        
        # Creating a QFileSystemModel
        self.model = QFileSystemModel()
        
        project_path = os.getcwd() + "/" + BASE_PROJECT_DIRECTORY_PATH # + "/" + project.name
        
        self.model.setRootPath(project_path)  # Set the root path to display the entire filesystem
        
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(project_path))
        
        self.tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        # Filter the files shown in the view
        filters = ['*.png', '*.jpg', '*.jpeg', '*.gif']  # Add more image formats if needed
        self.model.setNameFilters(filters)
        self.model.setNameFilterDisables(False)
        
        for i in range(1, self.tree_view.model().columnCount()):
            self.tree_view.header().hideSection(i)
                   
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.openMenu)
        
        self.tree_view.clicked.connect(self.select_item)
        
        layout = QVBoxLayout()
        self.title_label = QLabel("")
        layout.addWidget(self.title_label)
        layout.addWidget(self.tree_view)
        self.setLayout(layout)
        
        self.create_label_menu()
        self.tree_view.hide()
        
    def show_file_list(self):
        project_name = self.main.project.name
        project_path = self.main.project.path
        print("hej")
        provider = IconProvider(self)
        self.model.setIconProvider(provider)
        self.title_label.setText(project_name)
        self.model.setRootPath(project_path)  # Set the root path to display the entire filesystem
        self.tree_view.setRootIndex(self.model.index(project_path))
        
        self.tree_view.show()
        pass

    def select_item(self, index: QModelIndex):
        try:
            self.data = self.main.project.project_data
        except: ##no data found
            self.data = None        
            
        self.current_index = index
        path = index.model().filePath(index)
        name = index.model().fileName(index)
        
        ext = os.path.splitext(name)[-1]
        if ext in ACCEPTED_TYPES:   ##Check if selected item is an image (not folder))
            try:
                data_row = self.data[self.data["Img_Path"] == name]
            except:
                data_row = None
                        
            self.siblings = self.tree_view.model().rowCount(index.parent())
            self.image_viewer.display_image(path,data_row)
        
        
    def create_label_menu(self):
        self.label_menu = QMenu()
        self.label = self.label_menu.addMenu(self.tr("Assign label"))
        
        base = self.label.addAction("baseline")
        base.triggered.connect(lambda: self.assign_label(base.text()))
        
        stim = self.label.addAction("experiment")
        stim.triggered.connect(lambda: self.assign_label(stim.text()))
        
        rec = self.label.addAction("recovery")
        rec.triggered.connect(lambda: self.assign_label(rec.text()))
        
        # self.new_label = self.label_menu.addAction(self.tr("Create new label"))
        # self.new_label.triggered.connect(self.create_label)
    
    def openMenu(self, position):
    
        indexes = self.tree_view.selectedIndexes()
        
        ## Find level from root
        if len(indexes) > 0:
        
            level = 0
            index = indexes[0]
            while index.parent().isValid() and index.parent() != self.tree_view.rootIndex():
                index = index.parent()
                level += 1
        
        if level >= 1:
            self.label_menu.exec_(self.tree_view.viewport().mapToGlobal(position))
   
    def create_label(self):
        label_dialog = LabelDialog()
        if label_dialog.label_name is not None:
            temp = self.label.addAction(label_dialog.label_name)
            temp.triggered.connect(lambda: self.assign_label(temp.text()))
    
    def assign_label(self,label):
        #print(self.main.project.name)
        try:
            self.data = self.main.project.project_data
        except: ##no data found
            self.data = None     
            return
        
        indexes = self.tree_view.selectedIndexes()
        
        if len(indexes) > 1:
            for ind in indexes:
                name = ind.model().fileName(ind)
                
                ext = os.path.splitext(name)[-1]
                if ext in ACCEPTED_TYPES:   ##Check if image
                    #data_row = self.data[self.data["Img_Name"] == name]
                    #stimuli
                    self.data.loc[self.data["Img_Path"] == name,"Stimuli"] = label
                    
                else:   ##Its a folder
                    for i in range(self.tree_view.model().rowCount(ind)):
                        child_index = ind.child(i,0)    ##Every picture in folder
                        child_name = child_index.model().fileName(child_index)
                        self.data.loc[self.data["Img_Path"] == child_name,"Stimuli"] = label
                
        elif len(indexes) == 1:
            ind = indexes[0]
            name = ind.model().fileName(ind)
                
            ext = os.path.splitext(name)[-1]
            if ext in ACCEPTED_TYPES:   ##Check if image
                self.data.loc[self.data["Img_Path"] == name,"Stimuli"] = label
                
            else:   ##Its a folder
                for i in range(self.tree_view.model().rowCount(ind)):
                    child_index = ind.child(i,0)    ##Every picture in folder
                    child_name = child_index.model().fileName(child_index)
                    self.data.loc[self.data["Img_Path"] == child_name,"Stimuli"] = label
        else:
            return
        
        
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