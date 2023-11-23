class ProjectData:
    name: str
    """ Name of project. """

    path: str
    """ Path to project directory. """

    mouse: list["MouseData"]
    """ Mice that belong to project. """

    images: list["MouseImageData"]
    """ Images that are part of the project. """


class MouseData:
    name: str
    """ Name of mouse. """

    gender: str
    """ Gender of mouse. """


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
