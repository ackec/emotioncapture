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
from torch.utils.data.sampler import SubsetRandomSampler

from torch.utils.data import DataLoader, random_split
from test_model import test

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



# Preprocess the image (resize, normalize, etc.)

# Perform inference to get (x, y) coordinates
# with torch.no_grad():
#     model.eval()
#     output = model(preprocessed_image)

# Post-process the output if necessary

# Visualize the result (draw points on the image)

if __name__ == "__main__":


    # extract_frames("torch_model/videos/018757-2023-06-08 08-53-33.mp4")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data = pd.read_csv('labeling/csv_files/018757.csv')
    image_dir = "annotated_images"


    train_split=0.7
    dataset = CustomDataset(data, image_dir, device=device)
    train_dataset, test_dataset = random_split(dataset,[int(dataset.data.shape[0]*train_split), int(dataset.data.shape[0]*(1-train_split)+1)])
    # Hyperparameters
    batch_size = 18
    lr = 0.001
    num_epochs = 1000

    train_data = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_data = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

    model = train_model(train_data, test_data, lr, num_epochs)

    test(model, test_dataset)

    # Initialize the model
