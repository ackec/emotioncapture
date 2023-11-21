from pathlib import Path
from matplotlib import pyplot as plt

import torch
import torch.nn as nn

from torchvision.io import VideoReader
from torchvision.utils import save_image
from torchvision.transforms import Resize, Normalize, Compose

from model import ProfileDetector

VIDEO_PATH = './videos/F3H-2021-10-01 11-23-58.mp4'
MODEL_PATH = './trained_models/profile_detector_freeze_best'
OUTPUT_PATH = './output/profiles'

IMG_HEIGHT, IMG_WIDTH = 224, 224
FILE_TYPE = "jpg"

THRESHOLD = 0.7
""" Threshold above which a frame is considered a profile.  """


def image_batcher(reader: VideoReader, batch_size=8):
    """ Combine sequential frames from videos into a batch. """
    images = None
    time_stamps: list[float] = []
    i = 0
    for frame in reader:
        if i >= batch_size:
            yield images, time_stamps
            i = 0
            images = None
            time_stamps = []

        img: torch.Tensor = frame["data"].float().div(255).unsqueeze(0)
        time_s: float = frame['pts']

        images = torch.concat((images, img), 0) if images is not None else img
        time_stamps.append(time_s)
        i += 1

        # For testing only, stop after 100s
        # if time_s > 100:
        #     break

    yield images, time_stamps


def save_score_plot(predictions: list[float], time_stamps: list[float]):
    """ Plot the prediction score for every frame. """
    scaled_preds = [p*100 for p in predictions]
    plt.rcParams["figure.figsize"] = (20, 5)
    plt.plot(time_stamps, scaled_preds, label="Confidence")
    plt.hlines(y=100*THRESHOLD, xmin=time_stamps[0],
               xmax=time_stamps[-1]+1, label="Threshold",
               linestyles='--', colors='red')
    plt.title("Prediction score for video")
    plt.xlabel("Seconds")
    plt.ylabel("Confidence (%)")
    plt.ylim((0, 100))
    plt.xlim((time_stamps[0], time_stamps[-1]))
    plt.legend()
    plt.savefig(output_path / 'scores.jpg')
    plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]


def inference(model: nn.Module,
              video_path: Path,
              output_path: Path,
              save_plot=True):
    reader = VideoReader(str(video_path.absolute()), "video")
    video_len = reader.get_metadata()["video"]["duration"][0]
    frame_rate = reader.get_metadata()["video"]["fps"][0]

    transform = Compose([
        Resize((IMG_HEIGHT, IMG_WIDTH), antialias=True),
        Normalize((0.485, 0.456, 0.406),
                  (0.229, 0.224, 0.225)),
    ])

    model.eval()
    predictions: list[float] = []
    time_stamps: list[float] = []

    # Best frame found of last second
    prev_saved = {"path": "", "time": -10.0, "score": 0}

    for images, f_times in image_batcher(reader, 16):
        if len(predictions) % (10*frame_rate) == 0:
            print(f"Processed: {f_times[-1]}s / {video_len} s")

        frames = transform(images)
        preds = model(frames).squeeze(1).tolist()

        # TODO: Come up with a better solution to finding spread out images.

        # Save best frame of last second
        for i, pred in enumerate(preds):
            if pred < THRESHOLD:
                continue
            f_index = len(predictions) + i
            path = output_path / (f'img_{f_index}.{FILE_TYPE}')

            if prev_saved["time"] + 1 > f_times[i]:
                # Less than one second since last save
                if prev_saved["score"] > pred:
                    # Last saved was better, skip to next
                    continue

                # Remove last saved, replace with new best
                Path(prev_saved["path"]).unlink()

            save_image(images[i], path)
            prev_saved = {"path": path, "time": f_times[i], "score": pred}

        predictions.extend(preds)
        time_stamps.extend(f_times)

    if save_plot:
        save_score_plot(predictions, time_stamps)


if __name__ == '__main__':
    model_path = Path(MODEL_PATH)
    model = ProfileDetector(pretrained=True, freeze_backbone=True)
    model.load_state_dict(torch.load(model_path))

    video_path = Path(VIDEO_PATH)
    output_path = Path(OUTPUT_PATH)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Processing video: \'{video_path.absolute()}\'")
    inference(model, video_path, output_path, save_plot=True)
    print("Done!")
    print(f"Images saved in {output_path.absolute()}")
