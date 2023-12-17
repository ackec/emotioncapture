import pandas as pd
from config import *
# List of packages that are allowed to be imported
__all__ = ["ProjectData", "MouseData", "KeyPoints", "MouseImageData"]


class ProjectData:
    """ Meta data about an entire project. """

    name: str = ""
    """ Name of project. """

    path: str = ""
    """ Path to project directory. """

    mice: list["MouseData"] = []
    """ Mice that belong to project. """

    images: list["MouseImageData"] = []
    """ Images that are part of the project. """

    active_mouse_index: int = 0
    """ Index that point to which mouse in self.mice is active """

    inference_data: list["str"] = []

    #project_data: pd.DataFrame() = None
    
    project_data = None #pd.DataFrame() #pd.read_csv("Projects/new/detected_keypoints.csv")
    ## Columns for dataframe:
    # "Mouse_Name", "Video_Name", "Img_Path", "Frame_ID", "Ear_back_x", "Ear_back_y", "Ear_front_x", "Ear_front_y",
    # "Ear_bottom_x", "Ear_bottom_y", "Ear_top_x", "Ear_top_y", "Eye_back_x", "Eye_back_y",
    # "Eye_front_x", "Eye_front_y", "Eye_bottom_x", "Eye_bottom_y", "Eye_top_x", "Eye_top_y",
    # "Nose_top_x", "Nose_top_y", "Nose_bottom_x", "Nose_bottom_y", "Mouth_x", "Mouth_y", 
    # "eye_oppening", "ear_oppening", "ear_angle", "ear_pos_vec", "snout_pos", "mouth_pos", "face_incl", "stimuli", "orientation",
    # "keypoint_score", "profile_score", "id_phase_shift", "warn_flag"


class MouseData:
    """ Meta data about a specific mouse. """

    name: str = ""
    """ Name of mouse. """

    gender: str = ""
    """ Gender of mouse. """

    # videos: list["str"] = []
    # """ Filepath to videos belonging to the mouce. """

    genotype: str = ""

    weight: str = ""

    age: str = ""


class KeyPoints:
    """ Key points as (x, y) coordinates for an image. """
    ear_back = (None, None)
    ear_front = (None, None)
    ear_bottom = (None, None)
    ear_top = (None, None)

    eye_back = (None, None)
    eye_front = (None, None)
    eye_bottom = (None, None)
    eye_top = (None, None)

    nose_bottom = (None, None)
    nose_top = (None, None)

    mouth = (None, None)

    def __iter__(self):
        """ Iterate over the points, yields point name and postion. """
        yield "ear_back", self.ear_back
        yield "ear_front", self.ear_front
        yield "ear_bottom", self.ear_bottom
        yield "ear_top", self.ear_top
        yield "eye_back", self.eye_back
        yield "eye_front", self.eye_front
        yield "eye_bottom", self.eye_bottom
        yield "eye_top", self.eye_top
        yield "nose_bottom", self.nose_bottom
        yield "nose_top", self.nose_top
        yield "mouth", self.mouth


class MouseImageData:
    mouse: MouseData
    """ Mouse that image is of. """

    filename: str
    """ Name of the image. """

    path: str
    """ Path to image, relative project base. """

    profile_conf: float
    """ Model confidence that image is in profile. """

    key_point_conf: float
    """ Model confidence of key point placement. """

    key_points: KeyPoints
    """ Set of keypoints for the image. """
