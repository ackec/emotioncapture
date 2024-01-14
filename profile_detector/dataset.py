from PIL import Image
from pathlib import Path

import torch
from torch.utils.data import Dataset, WeightedRandomSampler, Subset
from torchvision.transforms import (ToTensor, Resize, Normalize, Compose,
                                    RandomHorizontalFlip, RandomRotation)


IMG_HEIGHT, IMG_WIDTH = 224, 224
FILE_TYPE = "jpg"


class ProfileDataset(Dataset):

    def __init__(self, path: str, augment=True):
        super().__init__()

        data_dir = Path(path)

        # Find all images paths
        self.targets, self.image_paths = [], []
        for path in data_dir.glob(f"annotated_images/*.{FILE_TYPE}"):
            self.image_paths.append(path)
            self.targets.append(True)

        for path in data_dir.glob(f"Bad_images/*.{FILE_TYPE}"):
            self.image_paths.append(path)
            self.targets.append(False)

        nr_images = len(self.image_paths)
        if nr_images == 0:
            raise Exception(f"No images found in \'{data_dir}\'.")

        if augment:
            self.transform = Compose([
                ToTensor(),
                Resize((IMG_HEIGHT, IMG_WIDTH), antialias=True),
                RandomHorizontalFlip(),
                RandomRotation([-10, 10]),
                Normalize((0.485, 0.456, 0.406),
                          (0.229, 0.224, 0.225)),
            ])
        else:
            self.transform = Compose([
                ToTensor(),
                Resize((IMG_HEIGHT, IMG_WIDTH), antialias=True),
                Normalize((0.485, 0.456, 0.406),
                          (0.229, 0.224, 0.225)),
            ])

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, ix):
        f = self.image_paths[ix]
        target = self.targets[ix]
        image = Image.open(f)
        return self.transform(image), torch.tensor([target]).float(), ix

def get_balanced_sampler(subset: Subset, targets: list, p_neg: float, generator):
    """ Returns sampler which samples negative with probability of `p_neg`. """
    num_positive = sum(1 for i in subset.indices if targets[i])
    num_negative = len(subset) - num_positive
    wp, wn = 1 / (p_neg * num_positive), 1 / ((1-p_neg) * num_negative)
    weights = [wp if targets[i] == 1 else wn for i in subset.indices]
    sampler = WeightedRandomSampler(torch.DoubleTensor(weights),
                                    num_samples=len(subset),
                                    replacement=True,
                                    generator=generator)
    return sampler