from torchvision import models
import torch.nn as nn


class ProfileDetector(nn.Module):
    """ Binary classifier for images. Uses ResNet 18 as backbone.  """

    def __init__(self, pretrained=True, freeze_backbone=True):
        super().__init__()
        
        resnet_params = {}
        if pretrained:
            resnet_params['weights'] = 'ResNet18_Weights.DEFAULT'

        self.model = models.resnet18(**resnet_params)

        if freeze_backbone and pretrained:
            for params in self.model.parameters():
                params.requires_grad = False

        self.model.avgpool = nn.AdaptiveAvgPool2d(output_size=(1, 1))
        self.model.fc = nn.Sequential(nn.Flatten(),
                                      nn.Linear(512, 128),
                                      nn.ReLU(),
                                      nn.Dropout(0.2),
                                      nn.Linear(128, 1),
                                      nn.Sigmoid())
        
    def forward(self, inputs):
        return self.model(inputs)
