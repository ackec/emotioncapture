from pathlib import Path
import torch

from profile_detector.inference import inference, ProfileDetector
from keypoint_finder.inference_keypoint import find_keypoints
from Feature_extracion.feature_from_labelpos import points_to_features
from Feature_extracion.create_clusters2 import cluster_keypoints, do_umap_projection


VIDEO_PATH = 'videos/018757-2023-06-08 08-53-33.mp4'
MODEL_PATH = './trained_models/profile_detector_freeze_best'
OUTPUT_PATH = './output/profiles'
XY_CSV_FILE = "output/detected_keypoints.csv"
FEATURE_CSV_FILE = "output/mouse_features.csv"

if __name__ == '__main__':
    model_path = Path(MODEL_PATH)
    profile_model = ProfileDetector(pretrained=True, freeze_backbone=True)
    profile_model.load_state_dict(torch.load(model_path))
    profile_model.to("cuda")

    # inference(profile_model, VIDEO_PATH, OUTPUT_PATH, save_plot=True)
    find_keypoints(img_path=OUTPUT_PATH, csv_out_file=XY_CSV_FILE)
    points_to_features(XY_CSV_FILE, FEATURE_CSV_FILE)
    # do_umap_projection(FEATURE_CSV_FILE)
    cluster_keypoints(FEATURE_CSV_FILE)