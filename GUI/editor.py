from typing import Callable

from PyQt5.QtGui import (QPixmap, QTransform, QWheelEvent, QIcon, QPainter,
                         QPainterPath, QPen, QBrush, QColor)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import (QPushButton, QDialog, QWidget, QHBoxLayout,
                             QStackedLayout, QGraphicsView, QGraphicsScene,
                             QGraphicsEllipseItem)

from config import WINDOW_HEIGHT, WINDOW_WIDTH, ZOOM_RANGE, RESOURCE_PATH
from data import MouseImageData, KeyPoints

# List of packages that are allowed to be imported
__all__ = ["ImageEditorDialog"]


class ImageEditorDialog(QDialog):
    """ Dialog that allows users to edit the points of an image. """

    # TODO: Test so it reset properly on close

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edit image")
        self.setMinimumSize(640, 320)
        self.setContentsMargins(0, 0, 0, 0)
        self.setGeometry(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setModal(True)

        self.image_data = None
        self.zoom = 1.0

        self.main_layout = QStackedLayout()
        self.main_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)

        self.point_editor = ImagePointEditor()
        self.main_layout.addWidget(self.point_editor)

        self.controls = OverlayControls(
            zoom_in=lambda: self._zoom(0.4),
            zoom_out=lambda: self._zoom(-0.4),
            cancel=self.hide,
            confirm=lambda: self.save_points(),
        )
        self.main_layout.addWidget(self.controls)

        self.setLayout(self.main_layout)

    def save_points(self):
        """ Save new points to mouse image data instance. """
        self.image_data.key_points = self.point_editor.save_points()
        self.hide()

    def _zoom(self, amount: float):
        self.zoom += amount

        # Clip to allowed zoom range
        self.zoom = max(self.zoom, ZOOM_RANGE[0])
        self.zoom = min(self.zoom, ZOOM_RANGE[1])

        self.point_editor.set_zoom(self.zoom)

    def wheelEvent(self, event: QWheelEvent):
        """ Zoom in/out when user scrolls mouse wheel. """
        scroll = event.angleDelta().y() / 100  # Normal scroll = +-120
        scroll += 0.8 * (1 if scroll < 0 else -1)  # +-0.4
        self._zoom(scroll)

    def resizeEvent(self, event):
        """ Move controls to bottom on window resize. """
        self.move_controls()

    def move_controls(self):
        """ Place controls 32 px from bottom. """
        x_pos = (self.width() - self.controls.width()) // 2
        y_pos = self.height() - self.controls.height() - 32
        self.controls.move(x_pos, y_pos)

    def show(self, image: MouseImageData):
        """ Display edit window with `image`. Image data is edited in-place. """
        if image is None:
            return

        self.image_data = image
        self.point_editor.set_image(image)
        super().show()


class MovablePoint(QGraphicsEllipseItem):
    COLORS = [
        Qt.GlobalColor.red,
        Qt.GlobalColor.green,
        Qt.GlobalColor.blue,
    ]

    def __init__(self, x, y, size=8, color=None):
        super(MovablePoint, self).__init__(0, 0, size, size)
        self.dot_size = size
        self.setPos(x - size / 2, y - size / 2)
        self.setBrush(color or Qt.GlobalColor.red)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable)
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def get_position(self):
        return (int(self.x() + self.dot_size / 2),
                int(self.y() + self.dot_size / 2))


class ImagePointEditor(QGraphicsView):
    def __init__(self):
        super().__init__()

        scene = QGraphicsScene(self)
        self.setScene(scene)

        self.setDragMode(self.DragMode.ScrollHandDrag)
        no_scroll_policy = Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        self.setVerticalScrollBarPolicy(no_scroll_policy)
        self.setHorizontalScrollBarPolicy(no_scroll_policy)

        self.points: dict[str, MovablePoint] = {}
        self.image = QPixmap()

    def wheelEvent(self, event):
        pass  # Do nothing on scroll

    def set_zoom(self, scale: float):
        """ Set absolute scale of image. """
        trans = QTransform()
        trans.scale(scale, scale)
        self.setTransform(trans)

    def set_image(self, image: MouseImageData):
        """ Load image and points and add to scene.  """
        self.points = {}
        self.scene().clear()

        self.image = QPixmap(image.path)
        self.scene().addPixmap(self.image)

        for name, pt in image.key_points:
            color = None
            if "ear" in name:
                color = MovablePoint.COLORS[0]
            elif "eye" in name:
                color = MovablePoint.COLORS[1]
            else:
                color = MovablePoint.COLORS[2]

            point = MovablePoint(*pt, color=color)
            self.points[name] = point
            self.scene().addItem(point)

    def save_points(self):
        """ Extract coordinates from scene and save in new Keypoints instance. """
        key_points = KeyPoints()
        for name, point in self.points.items():
            setattr(key_points, name, point.get_position())

        return key_points


class OverlayControls(QWidget):

    def __init__(self, zoom_in: Callable, zoom_out: Callable,
                 cancel: Callable, confirm: Callable):
        super().__init__()

        self.setFixedSize(196, 48)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(8, 0, 8, 0)
        self.main_layout.setSpacing(4)

        zoom_in_btn = QPushButton()
        zoom_in_btn.setIcon(QIcon(f"{RESOURCE_PATH}/zoom_in.svg"))
        zoom_in_btn.setStyleSheet("background-color: rgba(0,0,0,0);")
        zoom_in_btn.clicked.connect(zoom_in)
        self.main_layout.addWidget(zoom_in_btn, 0,
                                   Qt.AlignmentFlag.AlignLeading |
                                   Qt.AlignmentFlag.AlignVCenter)

        zoom_out_btn = QPushButton()
        zoom_out_btn.setIcon(QIcon(f"{RESOURCE_PATH}/zoom_out.svg"))
        zoom_out_btn.clicked.connect(zoom_out)
        zoom_out_btn.setStyleSheet("background-color: rgba(0,0,0,0);")
        self.main_layout.addWidget(zoom_out_btn, 0,
                                   Qt.AlignmentFlag.AlignLeading |
                                   Qt.AlignmentFlag.AlignVCenter)

        cancel_btn = QPushButton()
        cancel_btn.setIcon(QIcon(f"{RESOURCE_PATH}/cancel.svg"))
        cancel_btn.clicked.connect(cancel)
        cancel_btn.setStyleSheet("background-color: rgba(0,0,0,0);")
        self.main_layout.addWidget(cancel_btn, 1,
                                   Qt.AlignmentFlag.AlignTrailing |
                                   Qt.AlignmentFlag.AlignVCenter)

        confirm_btn = QPushButton()
        confirm_btn.setIcon(QIcon(f"{RESOURCE_PATH}/confirm.svg"))
        confirm_btn.clicked.connect(confirm)
        confirm_btn.setStyleSheet("background-color: rgba(0,0,0,0);")
        self.main_layout.addWidget(confirm_btn, 0,
                                   Qt.AlignmentFlag.AlignTrailing |
                                   Qt.AlignmentFlag.AlignVCenter)

        self.setLayout(self.main_layout)

    def paintEvent(self, event):
        # Draw semi-transparent rectangle behind buttons
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        pen = QPen(QColor("#767171"), 1)
        painter.setPen(pen)
        brush = QBrush(QColor(64, 64, 64, 200))
        painter.setBrush(brush)

        rect = QRectF(self.rect())
        # Slighly shrink dimensions to account for bordersize.
        rect.adjust(1/2, 1/2, -1/2, -1/2)

        path.addRoundedRect(rect, 4, 4)
        painter.setClipPath(path)

        painter.fillPath(path, painter.brush())
        painter.strokePath(path, painter.pen())