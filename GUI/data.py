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

    active_mouse_index: int = None
    """ Index that point to which mouse in self.mice is active """


class MouseData:
    """ Meta data about a specific mouse. """

    name: str = ""
    """ Name of mouse. """

    gender: str = ""
    """ Gender of mouse. """


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
