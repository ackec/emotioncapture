import cv2

# self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
# ret, self.frame = self.cap.read()

# cap = cv2.VideoCapture(video_path)

for i, (x, y) in enumerate(points):
    cv2.circle(image, x, y, 5, (255, 0, 255), -1)

cv2.imshow("Video Frame", image)

