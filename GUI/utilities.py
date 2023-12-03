from data import *
from config import BASE_PROJECT_DIRECTORY_PATH
import os
import json


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


def create_project(Project: ProjectData, path: str):
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
    
    return


#def load_project(Project: ProjectData, path: str):
#    with open(os.path.join(path, "meta.json"), 'r') as file:
#        data = json.load(file)
#    
#    Project.name = 
#
#    pass

def add_mouse(Project: ProjectData, name: str, gender: str, genotype: str):
    project_path = Project.path



    # Update json file
    with open(os.path.join(project_path, "meta.json"), 'r') as file:
        data = json.load(file)

    print(list(data.keys()))

    new = {"name": '{name}'.format(name=name), "gender": '{gender}'.format(gender=gender),
               "genotype": '{genotype}'.format(genotype=genotype)}

    data["registered_mice"].append(new)

    with open(os.path.join(project_path, "meta.json"), 'w') as file:
        json.dump(data, file, indent=2)

    # Update ProjectData

    mouse = MouseData()
    mouse.name = name
    mouse.gender = gender
    #mouse.genotype = genotype

    Project.mice.append(mouse)

    return

