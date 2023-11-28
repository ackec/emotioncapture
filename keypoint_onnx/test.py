import cv2
import numpy as np
from mmdeploy_runtime import Detector, PoseDetector

img = cv2.imread('./inputs_test/mouse.jpg')



def main():
    # Create Detector and Pose Detector
    detector = Detector(model_path='./mmdeploy_models/mmdet/ort', device_name='cpu', device_id=0)
    pose_detector = PoseDetector(model_path='./mmdeploy_models/mmpose/ort', device_name='cpu', device_id=0)

    bboxes, _, _ = detector(img)

    [left, top, right, bottom], score = bboxes[0][0:4].astype(int), bboxes[0][4]
    bbox = np.array((left, top, right, bottom), dtype=int)
    cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 0), 2)
    result = pose_detector(img, bbox)
    _, point_num, _ = result.shape
    points = result[:, :, :2].reshape(point_num, 2)
        
    for [x, y] in points.astype(int):
        cv2.circle(img, (x, y), 1, (0, 255, 0), 5)

        cv2.imwrite('output_pose.png', img)


if __name__ == '__main__':
    main()