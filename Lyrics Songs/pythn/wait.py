import cv2
import numpy as np
import os
import time

ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image, width=60):
    height, orig_width = image.shape[:2]
    aspect_ratio = orig_width / height
    new_height = int(width / aspect_ratio / 2)

    resized_image = cv2.resize(image, (width, new_height))

    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    ascii_str = ""
    for row in gray_image:
        for pixel in row:
            ascii_str += ASCII_CHARS[min(pixel // 25, len(ASCII_CHARS) - 1)]
        ascii_str += "\n"

    return ascii_str

def print_ascii_frame(ascii_art):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ascii_art)

def video_to_ascii(video_path, width=60, fps=200):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("❌ Error: Could not open video file.")
        return

    frame_time = 1.0 / fps

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        ascii_art = image_to_ascii(frame, width)
        print_ascii_frame(ascii_art)

        time.sleep(frame_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    print("\n🎬 Video playback finished!")

video_to_ascii("your_video.mp4", width=60, fps=200)
 
