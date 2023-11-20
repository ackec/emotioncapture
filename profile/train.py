from pathlib import Path
import pandas as pd

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn

from torch.utils.data import DataLoader, random_split
from torch.nn.modules.loss import _Loss
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader

from dataset import ProfileDataset
from model import ProfileDetector

TRAIN_DATA_PATH = './dataset/train'
SAVE_MODEL_DIR = './trained_models'

# Config
EPOCHS = 300
LR = 1e-3
WD = 1e-4


def train_epoch(model: nn.Module, dataloader: DataLoader, optimizer: Optimizer,
                objective: _Loss, use_cuda: bool):
    loss = 0
    correct = 0
    total = 0
    nr_batches = 0

    for inputs, targets in dataloader:
        if use_cuda:
            inputs, targets = inputs.cuda(), targets.cuda()

        inputs.requires_grad_(True)

        model.train()
        prediction = model(inputs)
        batch_loss = objective(prediction, targets)
        batch_loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        loss += batch_loss.item()
        nr_batches += 1
        total += targets.size(0)

        is_correct: torch.Tensor = (prediction > 0.5) == targets
        is_correct = is_correct.cpu().numpy().flatten().tolist()
        correct += sum(1 for correct in is_correct if correct)

    return (loss / nr_batches), correct/total


def eval_epoch(model: nn.Module, dataloader: DataLoader, objective: _Loss,
               use_cuda: bool):
    loss = 0
    correct = 0
    total = 0
    nr_batches = 0

    for inputs, targets in dataloader:
        if use_cuda:
            inputs, targets = inputs.cuda(), targets.cuda()

        inputs.requires_grad_(False)

        model.eval()
        prediction = model(inputs)
        batch_loss = objective(prediction, targets)

        loss += batch_loss.item()
        nr_batches += 1
        total += targets.size(0)

        is_correct: torch.Tensor = (prediction > 0.5) == targets
        is_correct = is_correct.cpu().numpy().flatten().tolist()
        correct += sum(1 for correct in is_correct if correct)

    return (loss / nr_batches), correct/total


def print_metrics(train_loss, val_loss, train_acc, val_acc):
    print("{:<12} {:<18} {:<18}".format("", "Loss", "Acc"))
    print("{:<12} {:<18.8f} {:<18.2f}".format("Train", train_loss, train_acc))
    print("{:<12} {:<18.8f} {:<18.2f}".format("Val", val_loss, val_acc))


def train(model: nn.Module, train_data: DataLoader, val_data: DataLoader,
          optimizer: Optimizer, objective: _Loss, use_cuda: bool, epochs: int,
          name: str = "profile_detector"):
    train_loss_log, train_acc_log = [], []
    val_loss_log, val_acc_log = [], []
    best_val_loss = 1000

    # Create directories for trained models
    model_path = Path(SAVE_MODEL_DIR)
    ckpt_path = model_path / "checkpoints"
    model_path.mkdir(exist_ok=True)
    ckpt_path.mkdir(exist_ok=True)

    for epoch in range(1, epochs+1):

        print('\nEpoch: %d' % epoch)
        train_loss, train_acc = train_epoch(model, train_data, optimizer,
                                            objective, use_cuda)
        train_loss_log.append(train_loss)
        train_acc_log.append(train_acc)

        val_loss, val_acc = eval_epoch(model, val_data, objective, use_cuda)
        val_loss_log.append(val_loss)
        val_acc_log.append(val_acc)

        print_metrics(train_loss, val_loss, train_acc*100, val_acc*100)

        # Save current best model
        if val_loss < best_val_loss:
            torch.save(model.state_dict(), model_path/(name + '_best'))

    # Save loss and accuracy
    torch.save(model.state_dict(), model_path/(name + '_final'))
    metrics = pd.DataFrame({"train loss": train_loss_log, "train accuracy": train_acc_log,
                           "validation loss": val_loss_log, "validation accuracy": val_acc_log})
    metrics.to_csv(model_path / (name + '_metrics.csv'), index=False)

    print('Training Finished!')
    return model, train_loss_log, train_acc_log


if __name__ == '__main__':
    # Check if CUDA support is available (GPU)
    use_cuda = torch.cuda.is_available()

    dataset = ProfileDataset(TRAIN_DATA_PATH)
    generator = torch.Generator().manual_seed(42)
    train_dataset, val_dataset = random_split(dataset, [0.9, 0.1], generator)

    train_loader = DataLoader(train_dataset, batch_size=128,
                              shuffle=True, generator=generator)
    print(f"Loaded train dataset with {len(train_dataset)} images.")

    val_loader = DataLoader(val_dataset, batch_size=64,
                            shuffle=True, generator=generator)
    print(f"Loaded validation dataset with {len(val_dataset)} images.")

    # Load and initialize the network architecture
    model = ProfileDetector(pretrained=True, freeze_backbone=True)

    if use_cuda:
        model.cuda()
        cudnn.benchmark = True

    # The objective (loss) function
    objective = nn.BCELoss()

    # The optimizer used for training the model
    optimizer = torch.optim.Adam(model.parameters(), lr=LR, weight_decay=WD)

    model, loss_log, acc_log = train(model=model,
                                     train_data=train_loader,
                                     val_data=val_loader,
                                     optimizer=optimizer,
                                     objective=objective,
                                     use_cuda=use_cuda,
                                     epochs=EPOCHS)
