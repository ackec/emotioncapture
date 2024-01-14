from torchvision import models
import torch.nn as nn


class ProfileDetector(nn.Module):
    """ Binary classifier for images. Uses ResNet 18 as backbone.  """

    def __init__(self, pretrained=True, freeze_backbone=True):
        super().__init__()

        resnet_params = {}
        if pretrained:
            resnet_params['weights'] = 'ResNet18_Weights.DEFAULT'

        self.backbone = models.resnet18(**resnet_params)
        self.backbone.avgpool = nn.AdaptiveAvgPool2d(output_size=(1, 1))
        self.backbone.fc = nn.Identity()

        if freeze_backbone and pretrained:
            for params in self.backbone.parameters():
                params.requires_grad = False

        self.fc = nn.Sequential(nn.Flatten(),
                                nn.Linear(512, 128),
                                nn.ReLU(),
                                nn.Dropout(0.2),
                                nn.Linear(128, 1),
                                nn.Sigmoid())

    def forward(self, inputs):
        out = self.backbone(inputs)
        return self.fc(out)


class ProfileDetectorLarge(nn.Module):
    """ Binary classifier for images. Uses ResNet 50 as backbone.  """

    def __init__(self, pretrained=True, freeze_backbone=True):
        super().__init__()

        resnet_params = {}
        if pretrained:
            resnet_params['weights'] = 'ResNet50_Weights.DEFAULT'

        self.backbone = models.resnet50(**resnet_params)
        self.backbone.avgpool = nn.AdaptiveAvgPool2d(output_size=(1, 1))
        self.backbone.fc = nn.Identity()

        if freeze_backbone and pretrained:
            for params in self.backbone.parameters():
                params.requires_grad = False

        self.fc = nn.Sequential(nn.Flatten(),
                                nn.Linear(512, 128),
                                nn.ReLU(),
                                nn.Dropout(0.2),
                                nn.Linear(128, 1),
                                nn.Sigmoid())

    def forward(self, inputs):
        out = self.backbone(inputs)
        return self.fc(out)
