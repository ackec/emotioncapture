import torch
import torch.nn as nn
import torch.optim as optim

# Define your custom dataset class for loading images and point coordinates

# Load your modified ResNet-50 model
from model import CustomResNet50Model  # Replace with your model class

def train_model(dataloader, lr, num_epochs):
    model = CustomResNet50Model(num_points=11)
    


    # Loss function for regression (e.g., Smooth L1 Loss)
    criterion = nn.SmoothL1Loss()

    # Optimizer (e.g., Adam)
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # Training loop
    for epoch in range(num_epochs):
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

        # Calculate and print average loss for this epoch
        average_loss = running_loss / len(dataloader)
        print(f"Epoch [{epoch+1}/{num_epochs}] Loss: {average_loss:.4f}")

    # Save the trained model
    torch.save(model.state_dict(), 'point_detection_model.pth')
