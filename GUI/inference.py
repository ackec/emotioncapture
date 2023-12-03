import sys


#sys.path.append('../profile_detector')
from pathlib import Path
from matplotlib import pyplot as plt

import torch
import torch.nn as nn

from torchvision.io import VideoReader
from torchvision.utils import save_image
from torchvision.transforms import Resize, Normalize, Compose

from profile_detector.model import ProfileDetector

from main import MainWindow


from abc import ABC, abstractmethod
import csv
import os
import cv2
import numpy as np
from mmdeploy_runtime import Detector, PoseDetector

from inferencer import KeyPointInferencer

PROFILE_MODEL_PATH = "./models/profile/profile_detector_freeze_best"
BBOX_MODEL_PATH = "./models/keypoint/profile_detector_freeze_best"
KEYPOINT_MODEL_PATH = "./models/profile/profile_detector_freeze_best"

IMG_HEIGHT, IMG_WIDTH = 224, 224
FILE_TYPE = "jpg"

THRESHOLD = 0.7
""" Threshold above which a frame is considered a profile.  """




def is_video_path(file_path):
    video_extensions = ['.mp4']  # Add more video extensions if needed
    return any(file_path.lower().endswith(ext) for ext in video_extensions)

def is_image_path(file_path):
    image_extensions = ['.png', '.jpg', '.jpeg']  # Add more image extensions if needed
    return any(file_path.lower().endswith(ext) for ext in image_extensions)

def process_input_paths(paths):
    video_paths = []
    image_paths = []

    for path in paths:
        if is_video_path(path):
            video_paths.append(path)
        elif is_image_path(path):
            image_paths.append(path)

    return video_paths, image_paths


def image_batcher(reader: VideoReader, batch_size=8):
    """ Combine sequential frames from videos into a batch. """
    images = None
    time_stamps: list[float] = []
    i = 0
    for frame in reader:
        if i >= batch_size:
            yield images, time_stamps
            i = 0
            images = None
            time_stamps = []

        img: torch.Tensor = frame["data"].float().div(255).unsqueeze(0)
        time_s: float = frame['pts']

        images = torch.concat((images, img), 0) if images is not None else img
        time_stamps.append(time_s)
        i += 1

        # For testing only, stop after 100s
        # if time_s > 100:
        #     break

    yield images, time_stamps


class Inferencer():
    def __init__(self, main: MainWindow):
        
        self.main = main

        self.input_path = None

        self.profile_detector = ProfileDetector(pretrained=True, freeze_backbone=True)
        self.profile_detector.load_state_dict(torch.load(PROFILE_MODEL_PATH))

        self.save_directory = os.path.join(main.Project.path, main.Project.mice[main.Project.active_mouse])

        self.input = os.path.join(self.save_directory, "images")
        self.output = os.path.join(self.save_directory, "detected_keypoints.csv")

        self.keypoint_detector = KeyPointInferencer(self.input, self.output)

    def save_score_plot(self, predictions: list[float], time_stamps: list[float]):
        """ Plot the prediction score for every frame. """
        scaled_preds = [p*100 for p in predictions]
        plt.rcParams["figure.figsize"] = (20, 5)
        plt.plot(time_stamps, scaled_preds, label="Confidence")
        plt.hlines(y=100*THRESHOLD, xmin=time_stamps[0],
                xmax=time_stamps[-1]+1, label="Threshold",
                linestyles='--', colors='red')
        plt.title("Prediction score for video")
        plt.xlabel("Seconds")
        plt.ylabel("Confidence (%)")
        plt.ylim((0, 100))
        plt.xlim((time_stamps[0], time_stamps[-1]))
        plt.legend()
        plt.savefig(os.path.join(self.input, "score/score.jpg"))
        plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]

    def video_detect_profiles(self, video_path, save_plot=True):
        video_path = Path(video_path)
        output_path = Path(self.input)
        output_path.mkdir(parents=True, exist_ok=True)

        reader = VideoReader(str(video_path.absolute()), "video")
        video_len = reader.get_metadata()["video"]["duration"][0]
        frame_rate = reader.get_metadata()["video"]["fps"][0]

        transform = Compose([
            Resize((IMG_HEIGHT, IMG_WIDTH), antialias=True),
            Normalize((0.485, 0.456, 0.406),
                    (0.229, 0.224, 0.225)),
        ])

        self.profile_detector.eval()
        predictions: list[float] = []
        time_stamps: list[float] = []

        # Best frame found of last second
        prev_saved = {"path": "", "time": -10.0, "score": 0}

        for images, f_times in image_batcher(reader, 24):
            if len(predictions) % (10*frame_rate) == 0:
                print(f"Processed: {f_times[-1]}s / {video_len} s")

            frames = transform(images)
            preds = self.profile_detector(frames).squeeze(1).tolist()

            # TODO: Come up with a better solution to finding spread out images.

            # Save best frame of last second
            for i, pred in enumerate(preds):
                if pred < THRESHOLD:
                    continue
                f_index = len(predictions) + i
                path = output_path / (f'img_{f_index}.{FILE_TYPE}')

                if f_times[i] < prev_saved["time"] + 0.5 :
                    # Less than one second since last save
                    if prev_saved["score"] > pred:
                        # Last saved was better, skip to next
                        continue

                    # Remove last saved, replace with new best
                    Path(prev_saved["path"]).unlink()

                save_image(images[i], path)
                prev_saved = {"path": path, "time": f_times[i], "score": pred}

            predictions.extend(preds)
            time_stamps.extend(f_times)

        if save_plot:
            self.save_score_plot(predictions, time_stamps)
            pass

    def image_detect_profiles(self):
        # TODO
        pass

    def find_keypoints(self):
        self.keypoint_detector.inference()
        return
    
    def inference(self, path):
        print("Start inference")
        video, images = process_input_paths(self, path)
        assert(len(video) < 2)
        
        self.video_detect_profiles(video[0])

        # TODO
        if len(images > 1):
            self.image_detect_profiles(self)

        self.find_keypoints()
