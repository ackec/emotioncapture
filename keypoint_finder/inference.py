from mmpose.apis import MMPoseInferencer

pose_cfg = 'work_dirs/mouse/mouse.py'
pose_checkpoint_path = 'work_dirs/mouse/epoch_420.pth'
det_cfg = "work_dirs/detection_mouse/detection_mouse.py"
det_model ="keypoint_finder/detection_mouse.py"
det_weights="work_dirs/detection_mouse/epoch_300.pth"

img_path = 'dataset/annotated_images/'
inferencer = MMPoseInferencer(pose_cfg, pose_checkpoint_path, device="cuda", det_model=det_model, det_weights=det_weights, det_cat_ids=[0]) #meybee change to 1 after retrain

metainfo = 'keypoint_finder/mouse_skeleton.py'
result_generator = inferencer(img_path, metainfo=metainfo, out_dir='output', draw_bbox=True, draw_heatmap=True)
results = next(result_generator)
# results = [result for result in result_generator]
print(results)
# print(result["predictions"][0][0]["keypoints"])
# print(result["predictions"][0][0]["bbox"])




