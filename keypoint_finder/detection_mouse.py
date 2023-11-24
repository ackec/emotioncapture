# Copyright (c) OpenMMLab. All rights reserved.
from mmcv.transforms import LoadImageFromFile
from mmengine.dataset.sampler import DefaultSampler

from mmdet.datasets import AspectRatioBatchSampler, CocoDataset
from mmdet.datasets.transforms import (LoadAnnotations, PackDetInputs,
                                       RandomFlip, Resize)
from mmdet.evaluation import CocoMetric

# dataset settings
dataset_type = CocoDataset
data_root = 'dataset'
classes = ('mouse')
default_scope = 'mmdet'  # The default registry scope to find modules. Refer to https://mmengine.readthedocs.io/en/latest/advanced_tutorials/registry.html
from mmengine.config import read_base

with read_base():
    from ..mmdetection.mmdet.configs.rtmdet.rtmdet_l_8xb32_300e_coco import *

from mmcv.transforms.loading import LoadImageFromFile
from mmcv.transforms.processing import RandomResize
from mmengine.hooks.ema_hook import EMAHook

from mmdet.datasets.transforms.formatting import PackDetInputs
from mmdet.datasets.transforms.loading import LoadAnnotations
from mmdet.datasets.transforms.transforms import (CachedMixUp, CachedMosaic,
                                                  Pad, RandomCrop, RandomFlip,
                                                  Resize, YOLOXHSVRandomAug)
from mmdet.engine.hooks.pipeline_switch_hook import PipelineSwitchHook
from mmdet.models.layers.ema import ExpMomentumEMA

checkpoint = 'https://download.openmmlab.com/mmdetection/v3.0/rtmdet/cspnext_rsb_pretrain/cspnext-s_imagenet_600e.pth'  # noqa
model.update(
    dict(
        backbone=dict(
            deepen_factor=0.33,
            widen_factor=0.5,
            init_cfg=dict(
                type='Pretrained', prefix='backbone.', checkpoint=checkpoint),
                frozen_stages=4 # max 4
                ),
        neck=dict(
            in_channels=[128, 256, 512], out_channels=128, num_csp_blocks=1),
        bbox_head=dict(in_channels=128, feat_channels=128, exp_on_reg=False, num_classes=1)
        
        ))

train_pipeline = [
    dict(type=LoadImageFromFile, backend_args=backend_args),
    dict(type=LoadAnnotations, with_bbox=True),
    dict(type=CachedMosaic, img_scale=(640, 640), pad_val=114.0),
    dict(
        type=RandomResize,
        scale=(1280, 1280),
        ratio_range=(0.5, 2.0),
        resize_type=Resize,
        keep_ratio=True),
    dict(type=RandomCrop, crop_size=(640, 640)),
    dict(type=YOLOXHSVRandomAug),
    dict(type=RandomFlip, prob=0.5),
    dict(type=Pad, size=(640, 640), pad_val=dict(img=(114, 114, 114))),
    dict(
        type=CachedMixUp,
        img_scale=(640, 640),
        ratio_range=(1.0, 1.0),
        max_cached_images=20,
        pad_val=(114, 114, 114)),
    dict(type=PackDetInputs)
]

train_pipeline_stage2 = [
    dict(type=LoadImageFromFile, backend_args=backend_args),
    dict(type=LoadAnnotations, with_bbox=True),
    dict(
        type=RandomResize,
        scale=(640, 640),
        ratio_range=(0.5, 2.0),
        resize_type=Resize,
        keep_ratio=True),
    dict(type=RandomCrop, crop_size=(640, 640)),
    dict(type=YOLOXHSVRandomAug),
    dict(type=RandomFlip, prob=0.5),
    dict(type=Pad, size=(640, 640), pad_val=dict(img=(114, 114, 114))),
    dict(type=PackDetInputs)
]

train_dataloader.update(dict(dataset=dict(pipeline=train_pipeline)))

custom_hooks = [
    dict(
        type=EMAHook,
        ema_type=ExpMomentumEMA,
        momentum=0.0002,
        update_buffers=True,
        priority=49),
    dict(
        type=PipelineSwitchHook,
        switch_epoch=280,
        switch_pipeline=train_pipeline_stage2)
]



train_dataloader = dict(
    batch_size=16,
    num_workers=2,
    persistent_workers=True,
    sampler=dict(type=DefaultSampler, shuffle=True),
    batch_sampler=dict(type=AspectRatioBatchSampler),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='train_annotations.json',
        data_prefix=dict(img='annotated_images'),
        metainfo=dict(classes=classes),
        filter_cfg=dict(filter_empty_gt=True, min_size=32),
        pipeline=train_pipeline,
        backend_args=backend_args))

val_dataloader = dict(
    batch_size=1,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type=DefaultSampler, shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='val_annotations.json',
        data_prefix=dict(img='annotated_images'),
        metainfo=dict(classes=classes),

        test_mode=True,
        pipeline=test_pipeline,
        backend_args=backend_args))
test_dataloader = val_dataloader

val_evaluator = dict(
    type=CocoMetric,
    ann_file='dataset/val_annotations.json',
    metric='bbox',
    format_only=False,
    backend_args=backend_args)
test_evaluator = val_evaluator




vis_backends = [dict(type='TensorboardVisBackend')]
visualizer=dict(type='Visualizer', vis_backends=[dict(type='TensorboardVisBackend')])
# visualizer = dict(
#     type='SelfSupVisualizer', vis_backends=vis_backends, name='visualizer')
# inference on test dataset and
# format the output results for submission.
# test_dataloader = dict(
#     batch_size=1,
#     num_workers=2,
#     persistent_workers=True,
#     drop_last=False,
#     sampler=dict(type=DefaultSampler, shuffle=False),
#     dataset=dict(
#         type=dataset_type,
#         data_root=data_root,
#         ann_file=data_root + 'annotations/image_info_test-dev2017.json',
#         data_prefix=dict(img='test2017/'),
#         test_mode=True,
#         pipeline=test_pipeline))
# test_evaluator = dict(
#     type=CocoMetric,
#     metric='bbox',
#     format_only=True,
#     ann_file=data_root + 'annotations/image_info_test-dev2017.json',
#     outfile_prefix='./work_dirs/coco_detection/test')
