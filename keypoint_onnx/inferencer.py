from abc import ABC, abstractmethod
import csv
import os
import cv2
import numpy as np
from mmdeploy_runtime import Detector, PoseDetector

class BaseInferencer(ABC):
    def __init__(self, input: str, output: str):
        self.config = None
        self.input_path = input
        self.output_path = output
        super().__init__()

    @abstractmethod
    def inference(self, input):
        pass

    @abstractmethod
    def save_results(self):
        pass



#class ProfileInferencer(BaseInferencer):
#    pass
    
        
class KeyPointInferencer(BaseInferencer):
    def __init__(self, inputpath: str, outputpath: str):
        self.Detector = Detector(model_path='./mmdeploy_models/mmdet/ort', device_name='cpu', device_id=0)
        self.PoseDetector = PoseDetector(model_path='./mmdeploy_models/mmpose/ort', device_name='cpu', device_id=0)
        self.processed_img = None
        super().__init__(input=inputpath, output=outputpath)

    def save_results(self, keypoints):
        with open(self.output_path+'/detected_keypoints.csv', "w", newline="") as csv_file:

            csv_writer = csv.writer(csv_file)

            header = ["Img_Path", "Frame_ID", "Ear_back_x", "Ear_back_y", "Ear_front_x", "Ear_front_y",
                        "Ear_bottom_x", "Ear_bottom_y", "Ear_top_x", "Ear_top_y", "Eye_back_x", "Eye_back_y",
                        "Eye_front_x", "Eye_front_y", "Eye_bottom_x", "Eye_bottom_y", "Eye_top_x", "Eye_top_y",
                        "Nose_top_x", "Nose_top_y", "Nose_bottom_x", "Nose_bottom_y", "Mouth_x", "Mouth_y"]
            csv_writer.writerow(header)

            for i, (result, img_path) in enumerate(keypoints):
                
                frame_id = i 

                [ear_back_x, ear_back_y] = result[0]
                [ear_front_x, ear_front_y] = result[1]
                [ear_bottom_x, ear_bottom_y] = result[2]
                [ear_top_x, ear_top_y] = result[3]
                [eye_back_x, eye_back_y] = result[4]
                [eye_front_x, eye_front_y] = result[5]
                [eye_bottom_x, eye_bottom_y] = result[6]
                [eye_top_x, eye_top_y] = result[7]
                [nose_top_x, nose_top_y] = result[8]
                [nose_bottom_x, nose_bottom_y] = result[9]
                [mouth_x, mouth_y] = result[10]

                row = [img_path, frame_id, ear_back_x, ear_back_y, ear_front_x, ear_front_y, ear_bottom_x,
                        ear_bottom_y, ear_top_x, ear_top_y, eye_back_x, eye_back_y, eye_front_x, eye_front_y,
                        eye_bottom_x, eye_bottom_y, eye_top_x, eye_top_y, nose_top_x, nose_top_y, nose_bottom_x,
                        nose_bottom_y, mouth_x, mouth_y]

                csv_writer.writerow(row)
        return 

    def forward(self, img):
        """
            Forward an image through detector and posedetector network
        """

        # Find bounding box
        bboxes, _, _ = self.Detector(img)

        # Get coordinates and confidence score of bounding box
        [left, top, right, bottom], score = bboxes[0][0:4].astype(int), bboxes[0][4]
        bbox = np.array((left, top, right, bottom), dtype=int)

        # Find keypoints in image inside bounding box
        result = self.PoseDetector(img, bbox)
        _, point_num, _ = result.shape
        points = result[:, :, :2].reshape(point_num, 2)

        return np.rint(points).astype(int), score
    
    def inference(self):
        files = [f for f in os.listdir(self.input_path) if f.lower().endswith('.jpg')]
        keypoints_list = []
        score_list = []
        for file in files:
            img = cv2.imread(self.input_path + '/' + file)
            keypoints, bbox_score = self.forward(img)
            keypoints_list.append((keypoints, file))
            score_list.append((bbox_score, file))
        
        self.save_results(keypoints_list)
        print("saved results")
        return

def main():
    input = "./inputs_test"
    output = "./output_test"
    Model = KeyPointInferencer(input, output)
    Model.inference()


if __name__ == "__main__":
    main()

