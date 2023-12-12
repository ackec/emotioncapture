from abc import ABC, abstractmethod
import csv
import os
import cv2
import numpy as np
from mmdeploy_runtime import Detector, PoseDetector
from pathlib import Path
from data import *
import re

import pandas as pd
import numpy as np
from calc_mouse_features import points_to_features

BBOX_MODEL_PATH = "models/pose/mmdeploy_models/mmdet/ort"
KEYPOINT_MODEL_PATH = "models/pose/mmdeploy_models/mmpose/ort"

# class BaseInferencer(ABC):
#     def __init__(self, input: str, output: str):
#         self.config = None
#         self.input_path = input
#         self.output_path = output
#         super().__init__()

#     @abstractmethod
#     def inference(self, input):
#         pass

#     @abstractmethod
#     def save_results(self):
#         pass


visualize = False

#class ProfileInferencer(BaseInferencer):
#    pass
    
        
class KeyPointInferencer():
    def __init__(self, inputpath: str, outputpath: str):
        self.Detector = Detector(model_path=BBOX_MODEL_PATH, device_name='cpu', device_id=0)
        self.PoseDetector = PoseDetector(model_path=KEYPOINT_MODEL_PATH, device_name='cpu', device_id=0)
        self.processed_img = None
        self.video_name = os.path.basename(inputpath)
        self.mouse_name = os.path.basename(os.path.dirname(inputpath))
        
        self.config = None
        self.input_path = inputpath
        self.output_path = outputpath


    def save_results(self, keypoints, files, mouse_features, orientations, keypoint_scores, profile_scores, warn_flags):
        if not os.path.exists(self.output_path):
            with open(self.output_path, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                header = ["Mouse_Name", "Video_Name", "Img_Path", "Frame_ID", "Ear_back_x", "Ear_back_y", "Ear_front_x", "Ear_front_y",
                            "Ear_bottom_x", "Ear_bottom_y", "Ear_top_x", "Ear_top_y", "Eye_back_x", "Eye_back_y",
                            "Eye_front_x", "Eye_front_y", "Eye_bottom_x", "Eye_bottom_y", "Eye_top_x", "Eye_top_y",
                            "Nose_top_x", "Nose_top_y", "Nose_bottom_x", "Nose_bottom_y", "Mouth_x", "Mouth_y", 
                            "eye_oppening", "ear_oppening", "ear_angle", "ear_pos_vec", "snout_pos", "mouth_pos", "face_incl", "stimuli", "orientation",
                            "keypoint_score", "profile_score", "id_phase_shift", "warn_flag"]
                csv_writer.writerow(header)

        with open(self.output_path, "a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            for i, (result, img_path, mouse_feature, orientation, keypoint_score, profile_score, warn_flag) in enumerate(zip(keypoints, files, mouse_features, orientations, keypoint_scores, profile_scores, warn_flags)):
                img_path = img_path.as_posix()
                frame_id = re.search(r'\d+', img_path).group()
                row = [self.mouse_name, self.video_name, img_path, frame_id, *result.ravel(),
                        *mouse_feature, "baseline", orientation, keypoint_score, profile_score, 0, warn_flag]
                csv_writer.writerow(row)
        return 

    def forward(self, img):
        """
            Forward an image through detector and posedetector network
        """

        # Find bounding box
        bboxes, _, _ = self.Detector(img)

        # Get coordinates and confidence score of bounding box
        [left, top, right, bottom], bbox_score = bboxes[0][0:4].astype(int), bboxes[0][4]
        bbox = np.array((left, top, right, bottom), dtype=int)

        # Find keypoints in image inside bounding box
        # if bbox_score < 0.8:
        #     return -1
        result = self.PoseDetector(img, bbox)
        _, point_num, _ = result.shape
        points = result[:, :, :2].reshape(point_num, 2)
        print("keypoint_scores")
        print(result[:, :, -1])

        scores = result[:,:,-1].T
        #min_keypoint_score = np.min
        #print(result)

        return points, bbox_score, bbox, np.min(scores)
    
    def inference(self):
        print("Starting keypoint inference")
        files = [f for f in os.listdir(self.input_path) if f.lower().endswith('.jpg')]
        keypoints_list = []
        score_list = []
        for file in files:
            #print(file)
            img = cv2.imread(self.input_path + '/' + file)
            keypoints, bbox_score, bbox = self.forward(img)
            keypoints_list.append(keypoints)
            score_list.append(bbox_score)

            if visualize:
                path = self.input_path+'/vis'
                if not os.path.exists(path):
                    os.mkdir(path)
                name = f'vis_{file}'
                print(name)
                cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 10, 10), 2)
                for [x, y] in keypoints.astype(int):
                    cv2.circle(img, (x, y), 1, (10, 255, 10), 7)
                    cv2.imwrite(os.path.join(path, name), img)


        mouse_features = points_to_features(np.array(keypoints_list))

        self.save_results(keypoints_list, files, np.array(mouse_features).T)
        df = pd.read_csv(self.output_path)
        print("saved results")
        return df
    



def main():
    input = "output/profiles"
    output = "output_test.csv"
    Model = KeyPointInferencer(input, output)
    Model.inference()


if __name__ == "__main__":
    main()

