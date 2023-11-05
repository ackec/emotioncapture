import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.models.detection import keypointrcnn_resnet50_fpn
from torchvision.models.detection.rpn import AnchorGenerator

# Define your custom dataset class for loading images and point coordinates

# Load your modified ResNet-50 model
from model import CustomResNet50Model  # Replace with your model class

def train_epoch(model, dataloader, optimizer, criterion):
    model.train()  # Set the model to training mode

    running_loss = 0.0

    for batch_data in dataloader:
        images, target_points = batch_data

        # Zero the parameter gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(images)

        # Calculate the loss
        loss = criterion(outputs, target_points)

        # Backpropagation and optimization
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    return running_loss / len(dataloader)
    # Calculate and print average loss for this epoch
    average_loss = running_loss / len(dataloader)




def train_model(trainloader, testloader, lr, num_epochs):
    model = CustomResNet50Model(num_points=11)
    anchor_generator = AnchorGenerator(sizes=(32, 64, 128, 256, 512), aspect_ratios=(0.25, 0.5, 0.75, 1.0, 2.0, 3.0, 4.0))

    model = keypointrcnn_resnet50_fpn(pretrained=False,
                                        pretrained_backbone=True,
                                        num_keypoints=11,
                                        num_classes = 2, # Background is the first class, object is the second class
                                        rpn_anchor_generator=anchor_generator)
    model.to("cuda")

    


    # Loss function for regression (e.g., Smooth L1 Loss)
    criterion = nn.SmoothL1Loss()

    # Optimizer (e.g., Adam)
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # Training loop
    for epoch in range(num_epochs):
        loss = train_epoch(model, trainloader, optimizer, criterion)
        print(f"Epoch [{epoch+1}/{num_epochs}] Loss: {loss:.4f}")

        running_loss = 0.0
        for batch_data in testloader:
            images, target_points = batch_data
            outputs = model(images)

            images, target_points = batch_data
            loss = criterion(outputs, target_points)
            running_loss += loss.item()
        print(f"val_loss :{running_loss}")


        #test_acc = test(model, testloader)


    # Save the trained model
    torch.save(model.state_dict(), 'point_detection_model.pth')
    return model