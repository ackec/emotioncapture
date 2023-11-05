import argparse
import cv2
import pandas as pd
import numpy as np
import os
from pathlib import Path

BODY_PARTS = [
    "Ear_back_x", "Ear_back_y", "Ear_front_x", "Ear_front_y",
    "Ear_bottom_x", "Ear_bottom_y", "Ear_top_x", "Ear_top_y",
    "Eye_back_x", "Eye_back_y", "Eye_front_x", "Eye_front_y",
    "Eye_bottom_x", "Eye_bottom_y", "Eye_top_x", "Eye_top_y",
    "Nose_top_x", "Nose_top_y", "Nose_bottom_x", "Nose_bottom_y",
    "Mouth_x", "Mouth_y"
]


class VideoAnnotation:

    def __init__(self, video_path: Path, output_dir: Path, num_points=8):
        self.video_id = video_path.stem  # Filename without suffix
        self.image_output_path = output_dir / 'images'
        self.bad_image_output_path = output_dir / 'bad_images'
        csv_output_path = output_dir / 'csv_files'
        self.csv_file_path = csv_output_path / f'{self.video_id}.csv'

        self.num_points = num_points
        self.clicked_points = []
        self.current_frame = 0
        self.line_start = None
        self.line_end = None
        self.zoom_start = (0, 0)  # Start position for zooming
        self.cap = cv2.VideoCapture(str(video_path.resolve()))
        self.img_dim = (int(self.cap.get(4)), int(self.cap.get(3)))
        self.zoom_end = self.img_dim

        if not self.cap.isOpened():
            print("Error: Could not open video file.")
            exit()

        try:
            self.df_points = pd.read_csv(self.csv_file_path)
            self.current_frame = self.df_points["Frame_ID"].max()
            if np.isnan(self.current_frame):
                self.current_frame = 0
        except:
            self.df_points = pd.DataFrame(columns=["Img_Path", "Frame_ID"] + BODY_PARTS)

        cv2.namedWindow("Video Frame")
        cv2.setMouseCallback("Video Frame", self.mouse_callback)

        # Show first frame
        self.update_cur_frame()
        cv2.imshow("Video Frame", self.frame)

    def hsv_to_bgr(self, hsv_color):
        return tuple(int(x) for x in cv2.cvtColor(np.uint8([[hsv_color]]), cv2.COLOR_HSV2BGR)[0][0])
    
    def update_cur_frame(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        ret, self.frame = self.cap.read()
        if not ret:
            self.frame = None

    def show_cur_points(self):
        # Create a copy of the frame to draw waypoints and zoom
        frame_copy = self.frame
        zoomed_frame = cv2.resize(frame_copy[self.zoom_start[0]:self.zoom_end[0], self.zoom_start[1]:self.zoom_end[1]], (self.img_dim[1], self.img_dim[0]))
        scale_x = (self.zoom_end[1] - self.zoom_start[1])/self.img_dim[1]
        scale_y = (self.zoom_end[0] - self.zoom_start[0])/self.img_dim[0]

        for i, (x, y) in enumerate(self.clicked_points):
            cv2.circle(zoomed_frame, (int((x-self.zoom_start[1])/scale_x), int((y-self.zoom_start[0])/scale_y)), 5, self.hsv_to_bgr((i*20, 255, 255)), -1)

        if self.line_start and self.line_end:
            adjusted_start = (int((self.line_start[0]-self.zoom_start[1])/scale_x), int((self.line_start[1]-self.zoom_start[0])/scale_y))
            adjusted_end = (int((self.line_end[0]-self.zoom_start[1])/scale_x), int((self.line_end[1]-self.zoom_start[0])/scale_y))
            cv2.line(zoomed_frame, adjusted_start, adjusted_end, (0, 255, 0), 2)
        if len(BODY_PARTS) > len(self.clicked_points)*2:
            print(f"Frame [{self.current_frame}], Click on bodypart: {BODY_PARTS[len(self.clicked_points)*2][:-2]}")
        else: 
            print(f"Frame [{self.current_frame}], No more points to click, you have : {len(self.clicked_points) - len(BODY_PARTS)//2} to many")

        cv2.imshow("Video Frame", zoomed_frame)


    def get_zoomed_coords(self, x, y):
        scale_x = (self.zoom_end[1] - self.zoom_start[1])/self.img_dim[1]
        scale_y = (self.zoom_end[0] - self.zoom_start[0])/self.img_dim[0]
        return int(self.zoom_start[1] + x*scale_x), int(self.zoom_start[0] + y*scale_y)

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.line_start = self.get_zoomed_coords(x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            self.line_end = self.get_zoomed_coords(x, y)
            for idx, point in enumerate(self.clicked_points):
                if (self.line_start[0] - point[0])**2 + (self.line_start[1] - point[1])**2 < 25:
                    # move existing point
                    self.clicked_points[idx] = self.line_end
                    self.show_cur_points()
                    return

            self.clicked_points.append(self.line_start)
            if (self.line_start[0] - self.line_end[0])**2 + (self.line_start[1] - self.line_end[1])**2 > 25:
                self.clicked_points.append(self.line_end)
            self.show_cur_points()

        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right-click to initiate zoom
            self.zoom_start = (x, y)  # Store the start position for zooming

        elif event == cv2.EVENT_RBUTTONUP:
            # Right-click release to finish zoom
            self.zoom_end = (x, y)
            start_x, start_y = self.zoom_start
            end_x, end_y = self.zoom_end
            self.zoom_start = (min(start_y, end_y), min(start_x, end_x))
            self.zoom_end = (max(start_y, end_y), max(start_x, end_x))

            zoom_distance = np.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
            if zoom_distance < 25:
                self.zoom_start = (0, 0)
                self.zoom_end = self.img_dim
            self.show_cur_points()

        elif event == cv2.EVENT_MBUTTONDOWN:
            # Store the start position for zooming
            self.move_start = self.get_zoomed_coords(x, y)

        elif event == cv2.EVENT_MBUTTONUP:
            self.move_end = self.get_zoomed_coords(x, y)
            diff_x = self.move_end[0] - self.move_start[0]
            diff_y = self.move_end[1] - self.move_start[1]
            self.zoom_start = (self.zoom_start[0]-diff_y, self.zoom_start[1]-diff_x)
            self.zoom_end = (self.zoom_end[0]-diff_y, self.zoom_end[1]-diff_x)
            self.show_cur_points()
    
    def get_clicked_points(self):
        return list(map(tuple, np.reshape(self.df_points.loc[self.df_points["Frame_ID"] == self.current_frame].values[0, 2:].astype(int), (-1, 2))))



    def show_new_frame(self):
        self.update_cur_frame()
        if (self.df_points["Frame_ID"] == self.current_frame).any():
            self.clicked_points = self.get_clicked_points()
            self.show_cur_points()
        else:
            self.clicked_points = []
            cv2.imshow("Video Frame", self.frame)


    def annotate_video(self):
        while True:
            if self.frame is None:
                break

            key = cv2.waitKey(0) & 0xFF
            if key == ord('q') or cv2.getWindowProperty('Video Frame', cv2.WND_PROP_VISIBLE) < 1:
                break



            elif key == ord('d'):
                # Next frame
                self.current_frame += 1
                self.show_new_frame()

            elif key == ord('f'):
                # Skip ahead 10 frames
                self.current_frame += 10
                self.show_new_frame()

            elif key == ord('p'):
                # Skip ahead 100 frames
                self.current_frame += 100
                self.show_new_frame()

            elif key == ord('o'):
                # Go back 100 frames
                self.current_frame -= 100
                self.show_new_frame()

            elif key == ord('a'):
                # Previous frame
                self.current_frame -= 1
                self.show_new_frame()


        self.cap.release()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--videos', help='Path to video')
    parser.add_argument('-o', '--output', help='Path to output directory')

    args = parser.parse_args()

    arg_input_path: str | None = args.videos
    arg_output_path: str | None = args.output

    if arg_input_path is None:
        print("Error: No video path supplied, use -v or --v and supply a path,")
        return

    if arg_output_path is None:
        arg_output_path = './output'

    input_path = Path(arg_input_path)
    output_path = Path(arg_output_path)

    if not input_path.exists():
        print(f"Error: No such video path found ({input_path.resolve()})")
        return

    if not output_path.exists():
        os.mkdir(output_path)

    print(f'Processing video: {input_path.resolve()}')

    annotator = VideoAnnotation(video_path=input_path,
                                output_dir=output_path,
                                num_points=len(BODY_PARTS)//2)
    annotator.annotate_video()

    print(f'Saved results in: {output_path.resolve()}')


if __name__ == "__main__":
    main()