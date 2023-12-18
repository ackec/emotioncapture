import numpy as np
from pathlib import Path

import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from dataset import ProfileDataset
from model import ProfileDetector

TEST_DATA_PATH = './dataset/train'
MODEL_DIR = './trained_models'


@torch.no_grad()
def accuracy(inputs, targets, model: nn.Module, threshold=0.5) -> list[bool]:
    """ Compute model accuracy. """
    model.eval()
    prediction = model(inputs)
    is_correct: torch.Tensor = (prediction > threshold) == targets
    is_correct = is_correct.cpu().numpy().flatten().tolist()
    return prediction, is_correct


def evaluate(cm: np.array):
    precision = cm[1, 1] / (cm[1, 1] + cm[0, 1])
    recall = cm[1, 1] / (cm[1, 1] + cm[1, 0])
    F1 = 2*precision*recall / (precision + recall)
    accuracy = np.trace(cm) / np.sum(cm)
    return precision, recall, F1, accuracy


def confusion(preds: list[float], tars: list[int], thresh=0.5):
    TP = sum(1 for p, t in zip(preds, tars) if p >= thresh and t == 1)
    FP = sum(1 for p, t in zip(preds, tars) if p >= thresh and t == 0)
    FN = sum(1 for p, t in zip(preds, tars) if p < thresh and t == 1)
    TN = sum(1 for p, t in zip(preds, tars) if p < thresh and t == 0)
    return np.array([[TN, FP], [FN, TP]])


def test(model: nn.Module, dataloader: DataLoader, use_cuda: bool):
    cm = np.zeros((2, 2))
    for inputs, targets, _ in dataloader:

        # Move data to GPU if CUDA is available
        if use_cuda:
            inputs, targets = inputs.cuda(), targets.cuda()

        inputs.requires_grad_(False)

        model.eval()
        prediction = model(inputs)
        cm += confusion(prediction, targets, thresh=0.35)

    prec, recall, F1, acc = evaluate(cm)
    print("Confusion matrix")
    print(cm)
    print("Evalutaion")
    print(f"Precision: {prec} | Recall: {recall} | F1: {F1} | Accuracy: {acc}")
    return (100 * cm.trace()) / cm.sum()


if __name__ == '__main__':
    model_path = Path(MODEL_DIR) / 'profile_detector_best'
    model = ProfileDetector(pretrained=True, freeze_backbone=True)
    model.load_state_dict(torch.load(model_path))

    test_dataset = ProfileDataset(TEST_DATA_PATH, augment=False)
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)
    print(f"Loaded test dataset with {len(test_dataset)} images.")

    test_acc = test(model, test_loader, use_cuda=False)
    print(f"Test accuracy: {test_acc}")
