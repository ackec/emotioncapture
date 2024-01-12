    git clone git@gitlab.liu.se:team-mouse/emotioncapture.git
    cd emotioncapture

    conda create --name mmpose_final2 python=3.11
    conda activate mmpose_final2
    python -m pip install mmdeploy-runtime
    conda install pandas matplotlib
    conda install qt
    conda install pytorch torchvision torchaudio -c pytorch
    conda install umap-learn
    conda install -c conda-forge opencv
    conda install av


Download models from link and extract in emotioncapture
    https://liuonline.sharepoint.com/:f:/s/CVLgroup1/Eozl9JI3-vxNr6yYGjZ_oEcBRU-AEiOBNbIYoU0uxXzn0Q?e=gOXKmH

Structure should be emotioncapture/models/pose/.. and emotioncapture/models/profile/..