# Profile detector
Here are some instructions for training a profile detector.

## Setup
Create the training data. Place examples of valid profiles in `Dataset/annotated_images` and examples of invalid images in `Dataset/Bad_images`. Images should be of the JPG format.

## Run training
To train the model, run
```bash
python profile_detector/train.py
```

## Evaluate
To evaluate the performance of a model, look at the evaluation jupyter notebook `evaluate.ipynb`.

## Inference
To run the model on a single video, without using the GUI, open `inference.py` and specifiy the `VIDEO_PATH`, `MODEL_PATH`, and `OUTPUT_PATH`. Then run it like

```bash
python profile_detector/inference.py
```
