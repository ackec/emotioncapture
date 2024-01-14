# Installation instructions

## Installation

```bash
# Clone the repository
git clone git@gitlab.liu.se:team-mouse/emotioncapture.git
cd emotioncapture

# Create conda environment
conda env create -f environment.yml

# Activate it
conda activate emotioncapture
```

Install more packages by adding them to environment.yml and run
```bash
conda env update -f environment.yml
```

## Running GUI
Run GUI with
```bash
python GUI/main.py
```

## Training

### Setup project for training
Run setup script to create folders and download dependencies.
```bash
python setup.py
```

The general file structure should look like this:
```
emotionscapture
├── Dataset
│   ├── annotated_images
│   ├── Bad_images
│   └── CSV_files
├── feature_extraction
├── GUI
├── keypoint_finder
├── keypoint_onnx
│   └── output_test
├── labeling
│   └── csv_files
├── mmdetection
├── mmpose
├── models
│   ├── pose
│   │   └── mmdeploy_models
│   │       ├── mmdet
│   │       │   └── ort
│   │       └── mmpose
│   │           └── ort
│   └── profile
└── profile_detector
```