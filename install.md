    # Clone the repository
    git clone git@gitlab.liu.se:team-mouse/emotioncapture.git
    cd emotioncapture

    # Create conda environment
    conda env create -f environment.yml

    # Activate it
    conda activate emotioncapture


Install more packages by adding them to environment.yml and run

    conda env update -f environment.yml

Download and unzip models from link and place in emotioncapture/
    https://liuonline.sharepoint.com/:f:/s/CVLgroup1/Eozl9JI3-vxNr6yYGjZ_oEcBRU-AEiOBNbIYoU0uxXzn0Q?e=gOXKmH

Structure should be emotioncapture/models/pose/.. and emotioncapture/models/profile/..

run GUI with 

    python GUI/main.py


To train you also need to get (in root):

    git clone git@github.com:open-mmlab/mmpose.git
    git clone git@github.com:open-mmlab/mmdetection.git

The general file structure should look like this:

    emotionscapture
    ├── Dataset
    │   ├── annotated_images
    │   ├── Bad_images
    │   └── CSV_files
    ├── Feature_extracion
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
