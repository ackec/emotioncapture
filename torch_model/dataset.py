import torch
import cv2
from torch.utils.data import Dataset
import os

class CustomDataset(Dataset):
    def __init__(self, data, image_dir, transform=None):
        self.data = data
        self.image_dir = image_dir
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        frame_info = self.data.iloc[idx]
        frame_path = os.path.join(self.image_dir, f"frame_{int(frame_info['Frame_ID'])}.jpg")  # Adjust to your file path structure
        image = cv2.imread(frame_path)  # Load the frame using OpenCV

        # Apply the specified transformation if provided
        if self.transform:
            # image = self.transform(image)
            image, points = self.transform(image, frame_info.values[1:])
        else:
            points = torch.tensor(frame_info.values[1:], dtype=torch.float32)

            # # points = torch.tensor(frame_info.values[1:], dtype=torch.float32)

        return image, points





