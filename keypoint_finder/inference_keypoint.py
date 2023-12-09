from mmpose.apis import MMPoseInferencer
import csv
import os
import re

def find_keypoints(img_path="output3/profiles", csv_out_file="output3/detected_keypoints.csv"):
    pose_cfg = 'trained_models/mouse.py'
    pose_checkpoint_path = 'trained_models/epoch_420.pth'
    # det_cfg = "work_dirs/detection_mouse/detection_mouse.py"
    # det_model ="work_dirs/detection_mouse/config_2.py"
    det_model= "keypoint_finder/detection_mouse.py"
    det_weights="trained_models/epoch_300.pth"
    inferencer = MMPoseInferencer(pose_cfg, pose_checkpoint_path, device="cuda", det_model=det_model, det_weights=det_weights, det_cat_ids=[0])

    metainfo = 'keypoint_finder/mouse_skeleton.py'
    result_generator = inferencer(img_path, metainfo=metainfo, out_dir=img_path + "/..",
                                    draw_bbox=True,
                                # draw_heatmap=True,
                                #   vis_out_dir=False,
                                # return_vis=False,
                                # vis_out_dir=False,
                                # pred_out_dir=False,
                                return_datasamples=False,
                                )
    results = [result for result in result_generator]


    file_names = sorted(os.scandir(path=img_path), key=lambda e: int(e.name.split('_')[1].split('.')[0]))

    with open(csv_out_file, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)

        header = ["Img_Path", "Frame_ID", "Ear_back_x", "Ear_back_y", "Ear_front_x", "Ear_front_y",
                    "Ear_bottom_x", "Ear_bottom_y", "Ear_top_x", "Ear_top_y", "Eye_back_x", "Eye_back_y",
                    "Eye_front_x", "Eye_front_y", "Eye_bottom_x", "Eye_bottom_y", "Eye_top_x", "Eye_top_y",
                    "Nose_top_x", "Nose_top_y", "Nose_bottom_x", "Nose_bottom_y", "Mouth_x", "Mouth_y"]
        csv_writer.writerow(header)

        for i, result in enumerate(results):
            keypoints = result["predictions"][0][0]["keypoints"]
            img_path = file_names[i].name
            frame_id = re.search(r'\d+', img_path).group()

            ear_back_x, ear_back_y = keypoints[0]
            ear_front_x, ear_front_y = keypoints[1]
            ear_bottom_x, ear_bottom_y = keypoints[2]
            ear_top_x, ear_top_y = keypoints[3]
            eye_back_x, eye_back_y = keypoints[4]
            eye_front_x, eye_front_y = keypoints[5]
            eye_bottom_x, eye_bottom_y = keypoints[6]
            eye_top_x, eye_top_y = keypoints[7]
            nose_top_x, nose_top_y = keypoints[8]
            nose_bottom_x, nose_bottom_y = keypoints[9]
            mouth_x, mouth_y = keypoints[10]

            row = [img_path, frame_id, ear_back_x, ear_back_y, ear_front_x, ear_front_y, ear_bottom_x,
                    ear_bottom_y, ear_top_x, ear_top_y, eye_back_x, eye_back_y, eye_front_x, eye_front_y,
                    eye_bottom_x, eye_bottom_y, eye_top_x, eye_top_y, nose_top_x, nose_top_y, nose_bottom_x,
                    nose_bottom_y, mouth_x, mouth_y]

            csv_writer.writerow(row)

    # print(results)


if __name__ == "__main__":
    find_keypoints()
