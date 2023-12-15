from data import *
from config import BASE_PROJECT_DIRECTORY_PATH
import os
import json
import pandas as pd
from tree_view import FileList

def init_project(name: str, path: str):

    #data = {
    #    "project_name": "{project_name}".format(project_name=name),
    #    "project_path": "{project_path}".format(project_path=path),
    #    "registered_mice": [
    #        {
    #            "name": "",
    #            "gender": "",
    #            "genotype": ""
    #        }
    #    ]
    #}
    data = {
        "project_name": "{project_name}".format(project_name=name),
        "project_path": "{project_path}".format(project_path=path),
        "registered_mice": []
    }
    meta_file = os.path.join(path, "meta.json")

    with open(meta_file, 'w') as file:
        json.dump(data, file, indent=2)


def create_project(Project: ProjectData, path: str, file_list = FileList):
    try:
        # Create the directory
        os.makedirs(path)
        print(f"Directory created: {path}")
    except OSError as e:
        print(f"Error creating directory: {e}")
    print("path = ", path)
    Project.name = str.split(path, '/')[-1]
    Project.path = path
    print(Project.name)
    print(Project.path)

    init_project(Project.name, Project.path)
    
    file_list.show_file_list()
    return


def load_project(Project: ProjectData, path: str, filelist: FileList):
    if os.path.exists(os.path.join(path, "meta.json")):
        with open(os.path.join(path, "meta.json"), 'r') as file:
            data = json.load(file)
        
        Project.name = data["project_name"]
        Project.path = data["project_path"]
        # Reset
        Project.mice = []
        for mouse in data["registered_mice"]:
            m_data = MouseData()
            m_data.name = mouse["name"]
            m_data.gender = mouse["gender"]
            m_data.genotype = mouse["genotype"]
            m_data.weight = mouse["weight"]
            m_data.age = mouse["age"]
            # TODO
            # Add genotype?
            Project.mice.append(m_data)

        print("Loaded project with parameters:")
        print("Project name: ", Project.name)
        print("Project path: ", Project.path)
        #for mouse in Project.mice:
        #    print("Mouse name: ", mouse.name, "     Mouse gender: ", mouse.gender)

        if os.path.exists(os.path.join(path, "detected_keypoints.csv")):
            Project.project_data = pd.read_csv(os.path.join(path, "detected_keypoints.csv"))
        else:
            Project.project_data = None
        
        filelist.show_file_list()
    else:
        print("Project does not exist")
    return

def add_mouse(Project: ProjectData, name: str, gender: str, genotype: str, weight: str, age: str):
    project_path = Project.path



    # Update json file
    with open(os.path.join(project_path, "meta.json"), 'r') as file:
        data = json.load(file)

    print(list(data.keys()))

    new = {"name": '{name}'.format(name=name), "gender": '{gender}'.format(gender=gender),
               "genotype": '{genotype}'.format(genotype=genotype),
               "weight": '{weight}'.format(weight=weight),
               "age": '{age}'.format(age=age)}

    data["registered_mice"].append(new)

    with open(os.path.join(project_path, "meta.json"), 'w') as file:
        json.dump(data, file, indent=2)

    # Update ProjectData

    mouse = MouseData()
    mouse.name = name
    mouse.gender = gender
    mouse.genotype = genotype
    mouse.weight = weight
    mouse.age = age

    Project.mice.append(mouse)

    return

