from PyQt5.QtWidgets import QLabel, QSizePolicy, QFrame, QWidget


# List of packages that are allowed to be imported
__all__ = ["ImageMetadataViewer", "ImageControl",
           "ImageViewer", "ImageFileList"]


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


class ImageViewer(PlaceHolder):
    def __init__(self):
        super().__init__("Image viewer")


class ImageControl(PlaceHolder):
    def __init__(self):
        super().__init__("Image controls")


class ImageMetadataViewer(PlaceHolder):
    def __init__(self):
        super().__init__("Image metadata")
