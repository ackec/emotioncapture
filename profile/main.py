import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.utils.data import DataLoader, random_split

from dataset import ProfileDataset
from model import ProfileDetector
from train import train
from test import test

TRAIN_DATA_PATH = './dataset/train'
TEST_DATA_PATH = './dataset/train'  # Change to real test

# Check if CUDA support is available (GPU)
use_cuda = torch.cuda.is_available()


dataset = ProfileDataset(TRAIN_DATA_PATH)
train_dataset, val_dataset = random_split(dataset, [0.9, 0.1])


train_loader = DataLoader(train_dataset, batch_size=64,
                          shuffle=True)
print(f"Loaded train dataset with {len(train_dataset)} images.")

val_loader = DataLoader(val_dataset, batch_size=64,
                        shuffle=True)
print(f"Loaded validation dataset with {len(val_dataset)} images.")

test_dataset = ProfileDataset(TEST_DATA_PATH, augment=False)
test_loader = DataLoader(test_dataset, batch_size=64,
                         shuffle=True)
print(f"Loaded test dataset with {len(test_dataset)} images.")

# Load and initialize the network architecture
model = ProfileDetector(pretrained=True, freeze_backbone=True)

if use_cuda:
    model.cuda()
    cudnn.benchmark = True

# The objective (loss) function
objective = nn.BCELoss()

# The optimizer used for training the model
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

model, loss_log, acc_log = train(model=model,
                                 train_data=train_loader,
                                 val_data=val_loader,
                                 optimizer=optimizer,
                                 objective=objective,
                                 use_cuda=use_cuda,
                                 start_epoch=1,
                                 epochs=50)

test_acc = test(model, test_loader, use_cuda)
