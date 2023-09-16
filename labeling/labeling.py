import cv2
import pandas as pd
import numpy as np
import os
import ffmpeg

class VideoAnnotation:
    def __init__(self, video_path, num_points=8):
        self.video_id = video_path.split("-")[0]
        self.video_path = os.path.join(os.path.dirname(__file__), "../videos", video_path).replace('\\', '/')  
        self.csv_name = os.path.join(os.path.dirname(__file__), f"csv_files/{self.video_id}.csv").replace('\\', '/')  
        self.num_points = num_points
        self.clicked_points = []
        self.current_frame = 0

        self.cap = cv2.VideoCapture(self.video_path)

        if not self.cap.isOpened():
            print("Error: Could not open video file.")
            exit()

        try:
            self.df_points = pd.read_csv(self.csv_name)
            self.current_frame = self.df_points["Frame_ID"].max()
            if np.isnan(self.current_frame):
                self.current_frame = 0
        except:
            self.df_points = pd.DataFrame(columns=["Frame_ID"] + [f"Point_{i+1}_{axis}" for i in range(self.num_points) for axis in ["X", "Y"]])

        cv2.namedWindow("Video Frame")
        cv2.setMouseCallback("Video Frame", self.mouse_callback)

    def hsv_to_bgr(self, hsv_color):
        return tuple(int(x) for x in cv2.cvtColor(np.uint8([[hsv_color]]), cv2.COLOR_HSV2BGR)[0][0])

    def show_cur_points(self):
        for i, (x, y) in enumerate(self.clicked_points):
            cv2.circle(self.frame, (x, y), 5, self.hsv_to_bgr((i*20, 255, 255)), -1)  
        cv2.imshow("Video Frame", self.frame)

    def get_frame(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        ret, self.frame = self.cap.read()
        if not ret:
            return None
        return self.frame

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.clicked_points.append((x, y))
            self.show_cur_points()

    def annotate_video(self):
        while True:
            self.frame = self.get_frame()
            if self.frame is None:
                break

            self.show_cur_points()
            key = cv2.waitKey(0) & 0xFF
            if key == ord('q'):
                break
            if key == ord('s'):
                # Save the clicked points to the CSV file
                if len(self.clicked_points) == self.num_points:
                    point_dict = {"Frame_ID": self.current_frame}
                    for i, (x, y) in enumerate(self.clicked_points):
                        point_dict[f"Point_{i+1}_X"] = x
                        point_dict[f"Point_{i+1}_Y"] = y

                    if (self.df_points["Frame_ID"] == self.current_frame).any():
                        existing_index = self.df_points.index[self.df_points["Frame_ID"] == self.current_frame].tolist()[0]
                        self.df_points.loc[existing_index] = point_dict
                    else:
                        self.df_points = pd.concat([self.df_points, pd.DataFrame([point_dict])], ignore_index=True)

                    self.df_points = self.df_points.sort_values(by=["Frame_ID"])
                    print(f"{self.num_points} points saved to DataFrame.")
                    self.df_points.to_csv(self.csv_name, index=False)
                    self.clicked_points = []
                    self.current_frame += 1

                else:
                    print(f"Please click on {self.num_points} points.")

            elif key == ord('d'): 
                self.current_frame += 1
                if (self.df_points["Frame_ID"] == self.current_frame).any():
                    self.clicked_points =list(map(tuple, np.reshape(self.df_points.loc[self.df_points["Frame_ID"] == self.current_frame].values[0,1:].astype(int), (-1, 2))))
                else:
                    self.clicked_points = []

            elif key == ord('a'):
                self.current_frame -= 1
                if (self.df_points["Frame_ID"] == self.current_frame).any():
                    self.clicked_points = list(map(tuple, np.reshape(self.df_points.loc[self.df_points["Frame_ID"] == self.current_frame].values[0,1:].astype(int), (-1, 2))))
                else:
                    self.clicked_points = []

            if key == ord('b'):
                if self.clicked_points:
                    self.clicked_points.pop()
                    self.show_cur_points()
        self.cap.release()

if __name__ == "__main__":
    video_path = "018757-2023-06-08 08-53-33.mp4"
    csv_name = "csv_files/out.csv"
    num_points = 8

    # input_file = 'mouse.mkv'
    # output_file = 'python_out.mp4'

    # input_stream = ffmpeg.input(input_file)
    # output_stream = ffmpeg.output(input_stream, output_file, vf='mpdecimate')

    # ffmpeg.run(output_stream)
    annotator = VideoAnnotation(video_path, num_points)
    annotator.annotate_video()
