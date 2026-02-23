import cv2
import os

source = "./data/background/2.mp4"
output_video_path = "./data/cache/video.mp4"
timestamp_file = "./data/timestamps.txt"

input_video = cv2.VideoCapture(source)
if not input_video.isOpened():
    raise RuntimeError("Failed to open the video file.")

image_timestamps = []
last_integer_timestamp = 0.0

with open(timestamp_file, "r") as file:
    for line in file:
        parts = line.strip().split("|")
        if len(parts) != 3:
            continue
        image_path, audio_path, timestamp_str = parts
        try:
            timestamp = float(timestamp_str)
            image_timestamps.append((image_path, timestamp))
            if int(timestamp) > last_integer_timestamp:
                last_integer_timestamp = int(timestamp)
        except ValueError:
            continue

fps = input_video.get(cv2.CAP_PROP_FPS)
ret, frame = input_video.read()
if not ret or frame is None:
    raise RuntimeError("Failed to read a frame from the video.")

frame_size = (frame.shape[1], frame.shape[0])

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)
if not output_video.isOpened():
    raise RuntimeError("Failed to open the output video file.")

image = None
scale = 1.0
dst_rc = None

while True:
    current_timestamp = input_video.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

    for img_path, ts in image_timestamps:
        if abs(ts - current_timestamp) < 0.01:
            image = cv2.imread(img_path)
            if image is not None:
                scale = min(frame.shape[1] / image.shape[1], frame.shape[0] / image.shape[0])
                image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
                cx = (frame.shape[1] - image.shape[1]) // 2
                cy = (frame.shape[0] - image.shape[0]) // 2
                dst_rc = (cx, cy, image.shape[1], image.shape[0])

    if image is not None and dst_rc:
        frame_copy = frame.copy()
        x, y, w, h = dst_rc
        frame_copy[y:y+h, x:x+w] = image
        output_video.write(frame_copy)
    else:
        output_video.write(frame)

    if current_timestamp >= last_integer_timestamp:
        break

    ret, frame = input_video.read()
    if not ret or frame is None:
        break

output_video.release()
input_video.release()
