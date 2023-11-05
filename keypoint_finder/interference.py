from mmpose.apis import MMPoseInferencer
# from mmcv.image import imread
from mmpose.apis import inference_topdown, init_model
from mmpose.registry import VISUALIZERS
# from mmpose.structures import merge_data_samples
from mmpose.apis import visualize



model_cfg = 'keypoint_finder/mouse.py'
ckpt = 'work_dirs/mouse/best_coco_AP_epoch_420.pth'
device = 'cuda'

# init model
model = init_model(model_cfg, ckpt, device=device)


img_path = 'dataset/annotated_images/G2F2-baseline_frame11609.jpg'

# inference on a single image
batch_results = inference_topdown(model, img_path)



pred_instances = batch_results[0].pred_instances

keypoints = pred_instances.keypoints
keypoint_scores = pred_instances.keypoint_scores

metainfo = 'keypoint_finder/custom.py'

print(pred_instances.keypoints)

visualize(
    img_path,
    keypoints,
    keypoint_scores,
    metainfo=metainfo,
    show=True)


# inferencer = MMPoseInferencer(
#     pose2d='/media/svahn/Y/MOUSE/emotioncapture/keypoint_finder/mouse.py',
#     pose2d_weights='/media/svahn/Y/MOUSE/emotioncapture/work_dirs/mouse/epoch_420.pth'
# )




# instantiate the inferencer using the model alias

# The MMPoseInferencer API employs a lazy inference approach,
# creating a prediction generator when given input
# result_generator = inferencer(img_path, show=True)
# result = next(result_generator)