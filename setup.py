import os
from pathlib import Path

WORK_DIR = Path(__file__).parent

# Create dataset folders
DATASET_PATH = WORK_DIR / 'Dataset'
Path(DATASET_PATH / 'annotated_images').mkdir(parents=True, exist_ok=True)
Path(DATASET_PATH / 'Bad_images').mkdir(parents=True, exist_ok=True)
Path(DATASET_PATH / 'CSV_files').mkdir(parents=True, exist_ok=True)

# Clone mmpose repos
os.chdir(WORK_DIR)
mm_repo_base = "git clone git@github.com:open-mmlab/"
os.system(mm_repo_base + 'mmpose.git')
os.system(mm_repo_base + 'mmdetection.git')
