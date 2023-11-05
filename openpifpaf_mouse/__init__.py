
import openpifpaf

from . import mouse_kp
from .mouse_kp import MouseKp

def register():
    openpifpaf.DATAMODULES['mouse'] = mouse_kp.MouseKp
    openpifpaf.CHECKPOINT_URLS['shufflenetv2k30-animalpose'] = \
        "http://github.com/vita-epfl/openpifpaf-torchhub/releases/" \
        "download/v0.12.9/shufflenetv2k30-210511-120906-animal.pkl.epoch400"