import cv2
import pandas as pd
import numpy as np
import os

class VideoAnnotation:
    def __init__(self, video_path, csv_name, num_points=8):
        self.video_path = os.path.join(os.path.dirname(__file__), "..", video_path).replace('\\', '/')  
        self.csv_name = os.path.join(os.path.dirname(__file__), csv_name).replace('\\', '/')  
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

            # Display previously clicked points
            if (self.df_points["Frame_ID"] == self.current_frame).any():
                points = self.df_points.loc[self.df_points["Frame_ID"] == self.current_frame]
                for i in range(self.num_points):
                    cv2.circle(self.frame, (points[f"Point_{i+1}_X"].item(), points[f"Point_{i+1}_Y"].item()), 5, self.hsv_to_bgr((i*20, 255, 255)), -1)

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
                        self.df_points.loc[self.df_points["Frame_ID"] == self.current_frame] = pd.DataFrame([point_dict])
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
                self.clicked_points = []
            elif key == ord('a'):
                self.current_frame -= 1
                self.clicked_points = []

            if key == ord('b'):
                if self.clicked_points:
                    self.clicked_points.pop()
        self.cap.release()

if __name__ == "__main__":
    video_path = "videos/out_kompressed.mp4"
    csv_name = "csv_files/out.csv"
    num_points = 8

    annotator = VideoAnnotation(video_path, csv_name, num_points)
    annotator.annotate_video()
