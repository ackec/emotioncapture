import sys
import os


#sys.path.append('../profile_detector')
from pathlib import Path
from matplotlib import pyplot as plt

import torch
import torch.nn as nn

from torchvision.io import VideoReader
from torchvision.utils import save_image
from torchvision.transforms import Resize, Normalize, Compose

import time
from pathlib import Path
import shutil

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from profile_detector.model import ProfileDetector

from Feature_extracion.feature_from_labelpos import points_to_features

#from main import MainWindow


from abc import ABC, abstractmethod
import csv
import os
import cv2
import numpy as np
from mmdeploy_runtime import Detector, PoseDetector

from inferencer import KeyPointInferencer

from data import *

PROFILE_MODEL_PATH = "./models/profile/profile_detector_freeze_final"
BBOX_MODEL_PATH = "./models/pose/mmdeploy_models/mmdet/ort"
KEYPOINT_MODEL_PATH = "./models/pose/mmdeploy_models/mmpose/ort"

IMG_HEIGHT, IMG_WIDTH = 224, 224
FILE_TYPE = "jpg"

THRESHOLD = 0.7
""" Threshold above which a frame is considered a profile.  """

stop_early = True

def frames_to_time(frame_id, frame_rate):
    time_in_seconds = frame_id / frame_rate
    minutes = int(time_in_seconds // 60)
    seconds = int(time_in_seconds % 60)
    return minutes, seconds

def is_in_range(val, lower, upper):
    return lower <= val <= upper

def check_feature_ranges(features):

    # Limits as per olivia's email
    lower = [0.51, 0.41, 160, 131, 72, 28, 62]
    upper = [0.79, 0.65, 200, 158, 90, 39, 75]

    for idx, val in enumerate(features):
        if is_in_range(val, lower[idx], upper[idx]):
            return False
    
    return True


def is_video_path(file_path):
    video_extensions = ['.mp4']  # Add more video extensions if needed
    #print(file_path)
    #return any(file_path.lower().endswith(ext) for ext in video_extensions)
    return any(file_path.lower().endswith(ext) for ext in video_extensions)

def is_image_path(file_path):
    image_extensions = ['.png', '.jpg', '.jpeg']  # Add more image extensions if needed
    return any(file_path.lower().endswith(ext) for ext in image_extensions)

def process_input_paths(paths):
    video_paths = []
    image_paths = []
    #if is_video_path(paths):
    #    return [paths], []
    #if is_image_path(paths):
    #    return [], [paths]

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

        # self.save_directory = os.path.join(self.project.path, self.project.mice[self.project.active_mouse_index].name)


        self.profile_detector = ProfileDetector(pretrained=True, freeze_backbone=True)
        self.profile_detector.load_state_dict(torch.load(PROFILE_MODEL_PATH, map_location=torch.device('cpu')))

        print("Created inferencer")

    def video_detect_profiles(self, video_path, save_plot=True):
        self.video_path = Path(video_path)
        output_path = Path(self.input_path)
        output_path.mkdir(parents=True, exist_ok=True)

        reader = VideoReader(str(self.video_path.absolute()), "video")
        video_len = reader.get_metadata()["video"]["duration"][0]
        frame_rate = reader.get_metadata()["video"]["fps"][0]
        #print(video_len)
        transform = Compose([
            Resize((IMG_HEIGHT, IMG_WIDTH), antialias=True),
            Normalize((0.485, 0.456, 0.406),
                    (0.229, 0.224, 0.225)),
        ])

        self.profile_detector.eval()
        predictions: list[float] = []
        time_stamps: list[float] = []

        # Best frame found of last second
        #prev_saved = {"path": "", "time": -10.0, "score": 0}

        for images, f_times in image_batcher(reader, 1):
            #if f_times[-1] > 10:
            #    return
            #if len(predictions) % (10*frame_rate) == 0:
            #   yield f"Processed: {f_times[-1]}s / {video_len} s"
            #if len(predictions) % (10*frame_rate) == 0:
            yield f"Processed: {f_times[-1]}s / {video_len} s"
                #print(f"Processed: {f_times[-1]}s / {video_len} s")

            frames = transform(images)
            preds = self.profile_detector(frames).squeeze(1).tolist()
            predictions.extend(preds)
            time_stamps.extend(f_times)
        fids_to_save: list[float] = []

        yield f"Finalizing Profile Detection Step"
        #print("Fetched all predictions")
            # Save best frame of last second
        prev_saved = {"time": -10.0, "score": 0}
        for i, pred in enumerate(predictions):
            f_time = time_stamps[i]

            if pred < THRESHOLD:
                    continue
                #path = output_path / (f'img_{f_index}.{FILE_TYPE}')
            #print(i, pred)
            if f_time < prev_saved["time"] + 1 :
                    # Less than one second since last save
                if prev_saved["score"] > pred:
                        # Last saved was better, skip to next
                    continue

                    # Remove last saved, replace with new best
                    #Path(prev_saved["path"]).unlink()

                #save_image(images[i], path)
                fids_to_save[-1] = i
                prev_saved = {"time": f_time, "score": pred}
                continue

            fids_to_save.append(i)
            prev_saved = {"time": f_time, "score": pred}
        
        fids = iter(fids_to_save)
        next_frame = next(fids)
        video_name = os.path.splitext(os.path.basename(self.video_path))[0]
        
        self.img_paths = []
        self.img_preds = []

        reader = VideoReader(str(self.video_path.absolute()), "video")
        for fid, frame in enumerate(reader):

            if fid < next_frame:
                continue
            
            mins, secs = frames_to_time(next_frame, frame_rate)

            image = frame["data"].float().div(255)
            path = output_path / (f'img_{fid}_time_{mins}_{secs}.{FILE_TYPE}')
            temp = 1
            while os.path.exists(path):
                path = output_path / (f'img_{fid}_time_{mins}_{secs}_{temp}.{FILE_TYPE}')
                temp += 1

            #print("Saving: ", path)
            save_image(image, path)
            yield f"Saving image , {os.path.basename(path)}"
            self.img_paths.append(path)
            self.img_preds.append(predictions[fid])



            try:
                next_frame = next(fids)
            except StopIteration:
                break




    def image_detect_profiles(self):
        # TODO
        pass

    def find_keypoints(self):
        self.project.keypoints = self.keypoint_detector.inference()
        return
    
    def inference(self, path):

        # #print("Start inference")
        yield f"{len(path)}"
        video, images = process_input_paths(path)
        #assert(len(video) < 2)
        self.keypoint_detector = None
        self.save_directory = os.path.join(self.project.path, self.project.mice[self.project.active_mouse_index].name)
        #self.input_path =  os.path.join(self.save_directory, os.path.splitext(os.path.basename(path))[0])
        self.output = os.path.join(self.project.path, "detected_keypoints.csv")



            
        #time.sleep(3)

        if len(video) > 0:
            for i, vid in enumerate(video):
                yield f"Video {i+1}/{len(video)}"
                #yield f"Starting inference on {vid}"
                #time.sleep(2)

                self.input_path =  os.path.join(self.save_directory, os.path.splitext(os.path.basename(vid))[0])

                for status in self.video_detect_profiles(vid):
                        yield status
                # # TODO Image inference
                # #if len(images > 1):
                # #     self.image_detect_profiles(self)


                if self.keypoint_detector is None:
                    self.keypoint_detector = KeyPointInferencer(self.input_path, self.output)
                else:
                    self.keypoint_detector.input_path = self.input_path
                    self.keypoint_detector.video_name = os.path.splitext(os.path.basename(vid))[0]

                yield "Starting Keypoint Detection..."

                #time.sleep(3)


                keypoints_list = []
                keypoint_scores = []
                #keypoints = np.zeros((len(self.img_paths), 11))
                files = self.img_paths
                profile_scores = []
                mouse_features = []
                warn_flags = []
                orientations = []
                for i, file in enumerate(self.img_paths):

                    yield f"Processed: {i}/{len(files)} images"
                    img = cv2.imread(file.absolute().as_posix())
                    kp, _, _, min_keypoints_score = self.keypoint_detector.forward(img)

                    profile_confidence = self.img_preds[i]

                    mouse_feature = points_to_features(kp[np.newaxis, :, :])

                    #
                    mouse_feature = [float(element[0]) for element in mouse_feature]

                    warn_flag = check_feature_ranges(mouse_feature)

                    if profile_confidence < 0.75:
                        warn_flag = 1

                    if min_keypoints_score < 0.8:
                        warn_flag = 1

                    # TODO Fix this
                    if kp[0, 0] > kp[8, 0]:
                        orientations.append("left")
                    else:
                        orientations.append("right")

                    


                    keypoints_list.append(kp)
                    keypoint_scores.append(min_keypoints_score)
                    profile_scores.append(profile_confidence)
                    mouse_features.append(mouse_feature)
                    warn_flags.append(warn_flag)

                yield "Saving Results..."

                #time.sleep(2)
                self.keypoint_detector.save_results(keypoints_list, files, mouse_features,
                                                    orientations, keypoint_scores, profile_scores,
                                                    warn_flags)

        if len(images) > 0:

            self.input_path =  os.path.join(self.save_directory, os.path.basename(os.path.dirname(images[0])))


            #yield self.save_directory+os.path.dirname(images[0])

            #time.sleep(10)
            self.img_paths = []
            for img in images:
                path = Path(img)
                self.img_paths.append(path)
            #self.img_paths = images
            
            if self.keypoint_detector is None:
                self.keypoint_detector = KeyPointInferencer(self.input_path, self.output)
            else:
                self.keypoint_detector.input_path = self.input_path
                self.keypoint_detector.video_name= os.path.basename(os.path.dirname(images[0]))



            keypoints_list = []
            keypoint_scores = []
            files = self.img_paths
            profile_scores = []
            mouse_features = []
            warn_flags = []
            orientations = []
            for i, file in enumerate(self.img_paths):

                yield f"Processed: {i}/{len(files)} images"
                img = cv2.imread(file.absolute().as_posix())
                kp, _, _, min_keypoints_score = self.keypoint_detector.forward(img)

                # Assume that profile is always in profile during inference on individual images
                profile_confidence = 1.0

                mouse_feature = points_to_features(kp[np.newaxis, :, :])

                    #
                mouse_feature = [float(element[0]) for element in mouse_feature]

                warn_flag = check_feature_ranges(mouse_feature)

                if profile_confidence < 0.75:
                    warn_flag = True

                if min_keypoints_score < 0.8:
                    warn_flag = True

                    # TODO Fix this
                if kp[0, 0] > kp[8, 0]:
                    orientations.append("left")
                else:
                    orientations.append("right")

                    


                keypoints_list.append(kp)
                keypoint_scores.append(min_keypoints_score)
                profile_scores.append(profile_confidence)
                mouse_features.append(mouse_feature)
                warn_flags.append(warn_flag)


                os.makedirs(self.input_path, exist_ok=True)




                output_file_name = os.path.basename(file.absolute().as_posix())

                name, ext = os.path.splitext(output_file_name)

                destination = os.path.join(self.input_path, output_file_name)

                tmp = 1
                while os.path.exists(destination):
                    new_name = f'{name}_{tmp}{ext}'
                    destination = os.path.join(self.input_path, new_name)
                    tmp += 1


                cv2.imwrite(destination, img)



            yield "Saving Results..."

            #time.sleep(2)
            self.keypoint_detector.save_results(keypoints_list, files, mouse_features,
                                                orientations, keypoint_scores, profile_scores,
                                                warn_flags)




if __name__ == "__name__":
    inferencer = Inferencer()
