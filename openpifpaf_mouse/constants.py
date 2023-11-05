
import os

import numpy as np

_CATEGORIES = ['mouse']  # only for preprocessing

MOUSE_KEYPOINTS=[
    "Ear_back",
    "Ear_front",
    "Ear_botten",
    "Ear_top",
    "Eye_back",
    "Eye_front",
    "Eye_botten",
    "Eye_top",
    "Nose_top",
    "Nose_botten",
    "Mounth"
    ]


HFLIP = {


    "Ear_back": "Ear_back",
    "Ear_front": "Ear_front",
    "Ear_botten": "Ear_botten",
    "Ear_top": "Ear_top",
    "Eye_back": "Eye_back",
    "Eye_front": "Eye_front",
    "Eye_botten": "Eye_botten",
    "Eye_top": "Eye_top",
    "Nose_top": "Nose_top",
    "Nose_botten": "Nose_botten",
    "Mounth": "Mounth"

}


ALTERNATIVE_NAMES = [
    "Ear_back",
    "Ear_front",
    "Ear_botten",
    "Ear_top",
    "Eye_back",
    "Eye_front",
    "Eye_botten",
    "Eye_top",
    "Nose_top",
    "Nose_botten",
    "Mounth"
]


MOUSE_SKELETON = [
    (1, 3), (1, 4), (3, 2), (4, 2), #Ear
    (5, 7), (5, 8), (8, 6), (7, 6), #Eye 
    (6, 9),  #Eye -> nose
    (6, 10), #Nose -> Nose
    (10, 11), #Nose -> mounth
]

MOUSE_SIGMAS = [
    0.026,  # nose
    0.025,  # eyes
    0.025,  # eyes
    0.035,  # ears
    0.035,  # ears
    0.079,  # throat
    0.079,  # tail
    0.079,  # withers
    0.072,  # elbows
    0.072,  # elbows
    0.072,  # elbows
]

split, error = divmod(len(MOUSE_KEYPOINTS), 4)
MOUSE_SCORE_WEIGHTS = [5.0] * split + [3.0] * split + [1.0] * split + [0.5] * split + [0.1] * error

MOUSE_CATEGORIES = ['animal']

MOUSE_POSE = np.array([
    [0.0, 4.3, 2.0],  # 'nose',            # 1
    [-0.4, 4.7, 2.0],  # 'left_eye',        # 2
    [0.4, 4.7, 2.0],  # 'right_eye',       # 3
    [-0.7, 5.0, 2.0],  # 'left_ear',        # 4
    [0.7, 5.0, 2.0],  # 'right_ear',       # 5
    [0.2, 3.0, 2.0],  # 'throat',            # 6
    [6.7, 3.8, 2.0],  # 'tail',             # 7
    [0.8, 4.0, 2.0],  # 'withers',         # 8
    [1.0, 2.0, 2.0],  # 'L_F_elbow',      # 9
    [0.6, 2.2, 2.0],  # 'R_F_elbow',     # 10
    [5.8, 2.1, 2.0],  # 'L_B_elbow',      # 11
])


assert len(MOUSE_POSE) == len(MOUSE_KEYPOINTS) == len(ALTERNATIVE_NAMES) == len(MOUSE_SIGMAS) \
       == len(MOUSE_SCORE_WEIGHTS), "dimensions!"


def draw_ann(ann, *, keypoint_painter, filename=None, margin=0.5, aspect=None, **kwargs):
    from openpifpaf import show  # pylint: disable=import-outside-toplevel

    bbox = ann.bbox()
    xlim = bbox[0] - margin, bbox[0] + bbox[2] + margin
    ylim = bbox[1] - margin, bbox[1] + bbox[3] + margin
    if aspect == 'equal':
        fig_w = 5.0
    else:
        fig_w = 5.0 / (ylim[1] - ylim[0]) * (xlim[1] - xlim[0])

    with show.canvas(filename, figsize=(fig_w, 5), nomargin=True, **kwargs) as ax:
        ax.set_axis_off()
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)

        if aspect is not None:
            ax.set_aspect(aspect)

        keypoint_painter.annotation(ax, ann)


def draw_skeletons(pose):
    from openpifpaf.annotation import Annotation  # pylint: disable=import-outside-toplevel
    from openpifpaf import show  # pylint: disable=import-outside-toplevel

    scale = np.sqrt(
        (np.max(pose[:, 0]) - np.min(pose[:, 0]))
        * (np.max(pose[:, 1]) - np.min(pose[:, 1]))
    )

    show.KeypointPainter.show_joint_scales = True
    show.KeypointPainter.font_size = 0
    keypoint_painter = show.KeypointPainter()

    ann = Annotation(
        keypoints=MOUSE_KEYPOINTS, skeleton=MOUSE_SKELETON, score_weights=MOUSE_SCORE_WEIGHTS)
    ann.set(pose, np.array(MOUSE_SIGMAS) * scale)
    os.makedirs('all-images', exist_ok=True)
    draw_ann(ann, filename='all-images/skeleton_animal.png', keypoint_painter=keypoint_painter)


def print_associations():
    for j1, j2 in MOUSE_SKELETON:
        print(MOUSE_SKELETON[j1 - 1], '-', MOUSE_KEYPOINTS[j2 - 1])


if __name__ == '__main__':
    print_associations()
    draw_skeletons(MOUSE_POSE)