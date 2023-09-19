import torch
import torch.nn as nn
import torchvision.models as models
import cv2
import pandas as pd
import os
from dataset import CustomDataset  # Replace with your dataset class
from torchvision import transforms
from torch.utils.data import DataLoader
from train import train_model


def extract_frames(video_path):
    video_id = video_path.split("-")[0]

    frame_count = 0
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if(data["Frame_ID"] == frame_count).any():

            frame = frame.astype(float)
            image_filename = os.path.join(image_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(image_filename, frame)

        frame_count += 1
    cap.release()

# Define a transformation sequence
data_transform = transforms.Compose([
    transforms.ToPILImage(),  # Convert to PIL Image
    transforms.Resize((224, 224)),  # Resize to the desired size
    transforms.ToTensor(),  # Convert to a PyTorch tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize pixel values
])


# Preprocess the image (resize, normalize, etc.)

# Perform inference to get (x, y) coordinates
# with torch.no_grad():
#     model.eval()
#     output = model(preprocessed_image)

# Post-process the output if necessary

# Visualize the result (draw points on the image)

if __name__ == "__main__":


    # extract_frames("torch_model/videos/018757-2023-06-08 08-53-33.mp4")

    data = pd.read_csv('torch_model/csv_files/018757.csv')
    image_dir = "torch_model/train_images"
    dataset = CustomDataset(data, image_dir, transform=data_transform)

    # Hyperparameters
    batch_size = 32
    lr = 0.001
    num_epochs = 10

    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    train_model(dataloader, lr, num_epochs)

    # Initialize the model
