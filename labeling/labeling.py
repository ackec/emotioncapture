import cv2
import pandas as pd
import numpy as np
import os

# ffmpeg -i videos/mouse.mkv -c:v copy -c:a aac -strict experimental output.mp
# ffmpeg -i output.mp4 -vf mpdecimate -vsync vfr out_kompressed.mp4

video_path = "vidoes/out_kompressed.mp4"

csv_name = "out"

NUM_POINTS = 8

clicked_points = []
current_frame = 0


def hsv_to_bgr(hsv_color):
    return tuple(int(x) for x in cv2.cvtColor(np.uint8([[hsv_color]]), cv2.COLOR_HSV2BGR)[0][0])

def show_cur_points():
    for i, (x, y) in enumerate(clicked_points):
        print(x, y)
        cv2.circle(frame, (x, y), 5, hsv_to_bgr((i*20, 255, 255)), -1)  
    cv2.imshow("Video Frame", frame)


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        show_cur_points()



cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

try:
    df_points = pd.read_csv(f"csv_files/{csv_name}.csv")
    current_frame = df_points["Frame_ID"].max()
    if current_frame != current_frame:  # is_nan
        current_frame = 0
except:    
    df_points = pd.DataFrame(columns = ["Frame_ID"] + [f"Point_{i+1}_{axis}" for i in range(NUM_POINTS) for axis in ["X", "Y"]])


cv2.namedWindow("Video Frame")
cv2.setMouseCallback("Video Frame", mouse_callback)
while True:
    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
    ret, frame = cap.read()
    if not ret:
        break

    # Display previously clicked points
    if (df_points["Frame_ID"]==current_frame).any():
        points = df_points.loc[df_points["Frame_ID"]==current_frame]
        for i in range(NUM_POINTS):
            cv2.circle(frame, (points[f"Point_{i+1}_X"].item(), points[f"Point_{i+1}_Y"].item()), 5, hsv_to_bgr((i*20, 255, 255)), -1)
    
    show_cur_points()

    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        break
    if key == ord('s'):
        # Save the clicked points to the CSV file
        if len(clicked_points) == NUM_POINTS:
            point_dict = {"Frame_ID": current_frame}
            for i, (x, y) in enumerate(clicked_points):
                point_dict[f"Point_{i+1}_X"] = x
                point_dict[f"Point_{i+1}_Y"] = y

            if (df_points["Frame_ID"] == current_frame).any():
                df_points.loc[df_points["Frame_ID"] == current_frame] =pd.DataFrame([point_dict])
            else:
                df_points = pd.concat([df_points, pd.DataFrame([point_dict])], ignore_index=True)

            df_points = df_points.sort_values(by=["Frame_ID"])
            print(f"{NUM_POINTS} points saved to DataFrame.")
            df_points.to_csv(f"csv_files/{csv_name}.csv", index=False)
            clicked_points = []
            current_frame += 1

        else:
            print(f"Please click on {NUM_POINTS} points.")

    elif key == ord('d'): 
        current_frame += 1
        clicked_points = []

        print(current_frame)
    elif key == ord('a'):
        current_frame -= 1
        clicked_points = []

        print(current_frame)

    if key == ord('b'):
        if clicked_points:
            clicked_points.pop()
cap.release()
