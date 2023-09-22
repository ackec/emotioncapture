import cv2
import pandas as pd
import numpy as np
import os

class VideoAnnotation:
    def __init__(self, video_path, num_points=8):
        self.video_id = video_path.split("-")[0]
        self.video_path = os.path.join(os.path.dirname(__file__), "../videos", video_path).replace('\\', '/')
        self.csv_name = os.path.join(os.path.dirname(__file__), f"csv_files/{self.video_id}.csv").replace('\\', '/')
        self.img_path = os.path.join(os.path.dirname(__file__), f"images").replace('\\', '/')
        if not os.path.exists(self.img_path):
            os.makedirs(self.img_path)
        self.num_points = num_points
        self.clicked_points = []
        self.current_frame = 0
        self.line_start = None
        self.line_end = None
        self.zoom_start = (0,0)  # Start position for zooming
        self.cap = cv2.VideoCapture(self.video_path)
        self.img_dim = (int(self.cap.get(4)), int(self.cap.get(3)))
        self.zoom_end = self.img_dim

        if not self.cap.isOpened():
            print("Error: Could not open video file.")
            exit()

        try:
            self.df_points = pd.read_csv(self.csv_name)
            self.current_frame = self.df_points["Frame_ID"].max()
            if np.isnan(self.current_frame):
                self.current_frame = 0
        except:
            self.df_points = pd.DataFrame(columns=["Img_Path", "Frame_ID"] + [f"Point_{i+1}_{axis}" for i in range(self.num_points) for axis in ["X", "Y"]])

        cv2.namedWindow("Video Frame")
        cv2.setMouseCallback("Video Frame", self.mouse_callback)

    def hsv_to_bgr(self, hsv_color):
        return tuple(int(x) for x in cv2.cvtColor(np.uint8([[hsv_color]]), cv2.COLOR_HSV2BGR)[0][0])

    def show_cur_points(self):
        frame_copy = self.frame.copy()  # Create a copy of the frame to draw waypoints and zoom
        zoomed_frame = cv2.resize(frame_copy[self.zoom_start[0]:self.zoom_end[0], self.zoom_start[1]:self.zoom_end[1]], (self.img_dim[1], self.img_dim[0]))
        scale_x = (self.zoom_end[1] - self.zoom_start[1])/self.img_dim[1]
        scale_y = (self.zoom_end[0] - self.zoom_start[0])/self.img_dim[0]

        for i, (x, y) in enumerate(self.clicked_points):
            cv2.circle(zoomed_frame, (int((x-self.zoom_start[1])/scale_x), int((y-self.zoom_start[0])/scale_y)), 5, self.hsv_to_bgr((i*20, 255, 255)), -1)

        if self.line_start and self.line_end:
            adjusted_start =  (int((self.line_start[0]-self.zoom_start[1])/scale_x), int((self.line_start[1]-self.zoom_start[0])/scale_y))
            adjusted_end =  (int((self.line_end[0]-self.zoom_start[1])/scale_x), int((self.line_end[1]-self.zoom_start[0])/scale_y))
            cv2.line(zoomed_frame, adjusted_start, adjusted_end, (0, 255, 0), 2)

        cv2.imshow("Video Frame", zoomed_frame)


    def get_frame(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        ret, self.frame = self.cap.read()
        if not ret:
            return None
        return self.frame

    def get_zoomed_coords(self, x, y):
        scale_x = (self.zoom_end[1] - self.zoom_start[1])/self.img_dim[1]
        scale_y = (self.zoom_end[0] - self.zoom_start[0])/self.img_dim[0]
        return int(self.zoom_start[1] + x*scale_x), int(self.zoom_start[0] + y*scale_y)

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.line_start = self.get_zoomed_coords(x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            self.line_end = self.get_zoomed_coords(x, y)
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
                self.zoom_start = (0,0)
                self.zoom_end = self.img_dim
            self.show_cur_points()


        elif event == cv2.EVENT_MBUTTONDOWN:
            self.move_start = self.get_zoomed_coords(x, y)  # Store the start position for zooming

        elif event == cv2.EVENT_MBUTTONUP:
            self.move_end = self.get_zoomed_coords(x, y)
            diff_x = self.move_end[0] - self.move_start[0]
            diff_y = self.move_end[1] - self.move_start[1]
            # print(diff_x, diff_y)
            self.zoom_start = (self.zoom_start[0]-diff_y, self.zoom_start[1]-diff_x)
            self.zoom_end = (self.zoom_end[0]-diff_y, self.zoom_end[1]-diff_x)
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
                    point_dict = {"Img_Path": f"{self.video_id}_frame{self.current_frame}.jpg",
                                  "Frame_ID": self.current_frame}
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
                    img_path = f"{self.img_path}/{self.video_id}_frame{self.current_frame}.jpg"
                    if not os.path.isfile(img_path):
                        cv2.imwrite(img_path, self.frame)
                    self.current_frame += 1

                else:
                    print(f"Please click on {self.num_points} points, you have clicked {len(self.clicked_points)}.")

            elif key == ord('d'): 
                self.current_frame += 1
                if (self.df_points["Frame_ID"] == self.current_frame).any():
                    self.clicked_points = list(map(tuple, np.reshape(self.df_points.loc[self.df_points["Frame_ID"] == self.current_frame].values[0,2:].astype(int), (-1, 2))))
                else:
                    self.clicked_points = []

            elif key == ord('a'):
                self.current_frame -= 1
                if (self.df_points["Frame_ID"] == self.current_frame).any():
                    self.clicked_points = list(map(tuple, np.reshape(self.df_points.loc[self.df_points["Frame_ID"] == self.current_frame].values[0,2:].astype(int), (-1, 2))))
                else:
                    self.clicked_points = []

            if key == ord('b'):
                if self.clicked_points:
                    self.clicked_points.pop()
                    self.show_cur_points()
        self.cap.release()

if __name__ == "__main__":
    video_path = "018757-2023-06-08 08-53-33.mp4"
    num_points = 11

    annotator = VideoAnnotation(video_path, num_points)
    annotator.annotate_video()
