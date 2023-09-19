import torch
import torch.nn as nn
import torchvision.models as models

class CustomResNet50Model(nn.Module):
    def __init__(self, num_points=10):
        super(CustomResNet50Model, self).__init__()

        # Load the pre-trained ResNet-50 model
        self.resnet50 = models.resnet50(pretrained=True)

        # Modify the last fully connected layer for regression
        in_features = self.resnet50.fc.in_features
        self.resnet50.fc = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.Linear(512, num_points * 2)  # 2 coordinates (x, y) for each point
        )

    def forward(self, x):
        return self.resnet50(x)
