import torch
import cv2
from torch.utils.data import Dataset
import os
from torchvision import transforms
import torchvision.transforms.functional as F
import cv2
import numpy as np
from torch import Tensor
import pandas as pd
from PIL import Image

from openpifpaf import encoder, headmeta, metric, transforms

# class CustomAffine(transforms.RandomAffine):
#     def forward(self, img):
#         fill = self.fill
#         channels, height, width = F.get_dimensions(img)
#         if isinstance(img, Tensor):
#             if isinstance(fill, (int, float)):
#                 fill = [float(fill)] * channels
#             else:
#                 fill = [float(f) for f in fill]
#         img_size = [width, height]  # flip for keeping BC on get_params call
#         self.ret = self.get_params(self.degrees, self.translate, self.scale, self.shear, img_size)
#         # only difference to save ret as self.ret compared to original version
#         # Apply affine transformation
#         transformed_img = F.affine(img, *self.ret, interpolation=self.interpolation, fill=fill, center=self.center)
#         return transformed_img

#     def get_param2(self):
#         return self.ret

# class CustomFlip(transforms.RandomHorizontalFlip):
#     def forward(self, img):
#         if torch.rand(1) < self.p:
#             self.flip = True
#             return F.hflip(img)
#         self.flip = False
#         return img

class CustomDataset(Dataset):
    def __init__(self, data, image_dir, transform=None, preprocess=None, device = torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        self.data =  pd.read_csv('labeling/csv_files/018757.csv')

        self.image_dir = "labeling/images"
        self.transform = transform
        self.device = device
        self.preprocess = preprocess


    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        frame_info = self.data.iloc[idx]
        frame_path = os.path.join(self.image_dir, f"018757_frame{int(frame_info['Frame_ID'])}.jpg")

# IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`) and integer or boolean arrays are valid indices

        #image = cv2.imread(frame_path)
        image = Image.open(frame_path).convert('RGB')
        meta = None
        points = frame_info[2:].values
        points = np.hstack((points.reshape(-1, 2), np.ones((11, 1)))).astype(float) # add visability 1 to all
        anns = [{'keypoints': points}]


        image, anns, meta = self.preprocess()(image, anns, meta)

        # show_points = True
        # if show_points:
        #     img2 = (image*50+120).numpy().astype(np.uint8).transpose(1, 2, 0)
        #     img2 = np.ascontiguousarray(img2, dtype=np.uint8)

        #     for i, (x, y, _) in enumerate(points):
        #         cv2.circle(img2, (int(x), int(y)), 2, (255, 0, 255), -1)
        #     cv2.imshow("Video Frame", img2)
        #     cv2.waitKey(0)
        return image, anns, meta
        old_image = image
        # Define a transformation sequence
        img_transform = transforms.Compose([
            transforms.ToPILImage(),  # Convert to PIL Image
            transforms.Resize((300, 600)),  # Resize to the desired size
            transforms.ToTensor(),  # Convert to a PyTorch tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize pixel values
        ])

        data_aug = transforms.Compose([
            CustomAffine(degrees=20, translate=None, scale=None),
            CustomFlip(),
        ])
        # img, param = CustomAffine(degrees=20, translate=None, scale=None),
        # img, param["flip"] = CustomFlip(),


        points = torch.tensor(frame_info.values[2:].astype(int), dtype=torch.float32).to(self.device)
        image = img_transform(image)
        image = data_aug(image)
        self.angle, self.translate, self.scale, self.shear = data_aug.transforms[0].get_param2()
        self.flip = data_aug.transforms[1].flip
        aug2_points = points.reshape(-1,2)
        aug2_points[:,0]*=600/1920
        aug2_points[:,1]*=300/1080

        center = torch.tensor([300,150]).to("cuda") 
        angle = torch.tensor(self.angle*torch.pi/180)

        aug2_points = aug2_points-center # Translate to origin
        rot = torch.stack([torch.stack([torch.cos(angle), -torch.sin(angle)]),
                           torch.stack([torch.sin(angle), torch.cos(angle)])]).to("cuda")
        aug2_points = torch.matmul(aug2_points,rot.T) + center
        if self.flip:
            aug2_points[:,0] = 600 - aug2_points[:,0]

        ### show points
        show_points = False
        if show_points:
            img2 = (image*50+120).numpy().astype(np.uint8).transpose(1, 2, 0)
            img2 = np.ascontiguousarray(img2, dtype=np.uint8)
            for i, (x, y) in enumerate(aug2_points.reshape(-1, 2)):
                cv2.circle(img2, (int(x), int(y)), 2, (255, 0, 255), -1)
            cv2.imshow("Video Frame", img2)
            cv2.waitKey(0)

        return image.to(self.device), aug2_points.ravel().to(self.device)





