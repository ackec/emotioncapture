import sys


#sys.path.append('../profile_detector')
from pathlib import Path
from matplotlib import pyplot as plt

import torch
import torch.nn as nn

from torchvision.io import VideoReader
from torchvision.utils import save_image
from torchvision.transforms import Resize, Normalize, Compose


from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from profile_detector.model import ProfileDetector

#from main import MainWindow


from abc import ABC, abstractmethod
import csv
import os
import cv2
import numpy as np
from mmdeploy_runtime import Detector, PoseDetector

from inferencer import KeyPointInferencer

from data import *

PROFILE_MODEL_PATH = "./models/profile/profile_detector_freeze_best"
BBOX_MODEL_PATH = "./models/pose/mmdeploy_models/mmdet/ort"
KEYPOINT_MODEL_PATH = "./models/pose/mmdeploy_models/mmpose/ort"

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
    #print("hej")

    yield images, time_stamps


class Inferencer():
    def __init__(self, project: ProjectData):
        
        self.project = project

        self.input_path = None

        #print("Created inferencer")
        #print("input path: ", self.input)
        #print("output path: ", self.output)

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
            #if len(predictions) % (10*frame_rate) == 0:
                #print(f"Processed: {f_times[-1]}s / {video_len} s")

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

            # TODO
            # Save scores for the best images for each second.
            # Idk how to do this right now

           


    def image_detect_profiles(self):
        # TODO
        pass

    def find_keypoints(self):
        self.keypoint_detector.inference()
        return
    
    def inference(self, path):
        self.save_directory = os.path.join(self.project.path, self.project.mice[self.project.active_mouse_index].name)

        self.input = os.path.join(self.save_directory, "images")
        self.output = os.path.join(self.save_directory, "detected_keypoints.csv")

        self.profile_detector = ProfileDetector(pretrained=True, freeze_backbone=True)
        self.profile_detector.load_state_dict(torch.load(PROFILE_MODEL_PATH, map_location=torch.device('cpu')))
        self.keypoint_detector = KeyPointInferencer(self.input, self.output)

        #print("Start inference")
        video, images = process_input_paths(path)
        assert(len(video) < 2)
        
        self.video_detect_profiles(video[0])

        # TODO
        #if len(images > 1):
        #     self.image_detect_profiles(self)
        files = [f for f in os.listdir(self.input) if f.lower().endswith('.jpg')]
        keypoints_list = []
        bbox_score_list = []
        keypoint_score_list = []
        for file in files:
            image_data = MouseImageData()
            kp = KeyPoints()
            path = self.input + '/' + file
            img = cv2.imread(path)
            keypoints, bbox_score, bbox = self.keypoint_detector.forward(img)
            keypoints_list.append((keypoints, file))
            bbox_score_list.append(bbox_score)

            image_data.mouse = self.project.mice[self.project.active_mouse_index]
            image_data.path = path
            image_data.profile_conf = 0.5   # Temp
            image_data.key_point_conf = 0.5     # Temp

            [ear_back_x, ear_back_y] = keypoints[0]
            [ear_front_x, ear_front_y] = keypoints[1]
            [ear_bottom_x, ear_bottom_y] = keypoints[2]
            [ear_top_x, ear_top_y] = keypoints[3]
            [eye_back_x, eye_back_y] = keypoints[4]
            [eye_front_x, eye_front_y] = keypoints[5]
            [eye_bottom_x, eye_bottom_y] = keypoints[6]
            [eye_top_x, eye_top_y] = keypoints[7]
            [nose_top_x, nose_top_y] = keypoints[8]
            [nose_bottom_x, nose_bottom_y] = keypoints[9]
            [mouth_x, mouth_y] = keypoints[10]

            kp.ear_back = (ear_back_x, ear_back_y)
            kp.ear_front = (ear_front_x, ear_front_y)
            kp.ear_bottom = (ear_bottom_x, ear_bottom_y)
            kp.ear_top = (ear_top_x, ear_top_y)
            kp.eye_back = (eye_back_x, eye_back_y)
            kp.eye_front = (eye_front_x, eye_front_y)
            kp.eye_bottom = (eye_bottom_x, eye_bottom_y)
            kp.eye_top = (eye_top_x, eye_top_y)
            kp.nose_top = (nose_top_x, nose_top_y)
            kp.nose_bottom = (nose_bottom_x, nose_bottom_y)
            kp.mouth = (mouth_x, mouth_y)

            image_data.key_points = kp

            self.project.images.append(image_data)
        
        self.keypoint_detector.save_results(keypoints_list)
        
        #for image in self.project.images:
        #    print(image.path)
            


        #print(files)
        #self.find_keypoints()
