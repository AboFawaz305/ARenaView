#!/bin/python
import os
import sys
from math import ceil, inf

import cv2

from ModelManager import *

# Define the paths
VIDEO_PATH = sys.argv[2] #"./vvv.mp4"  # Input video
OUTPUT_PATH = sys.argv[3] # "./vvv_out.mp4"  # Output video

# Create a VideoCapture object
cap = cv2.VideoCapture(VIDEO_PATH)

# Check if the video file was successfully opened
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video properties for the output file
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Initialize the model
mm = ModelManager(None)

# Create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for MP4
out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

print(f"Processing video with {total_frames} frames...")

# Frame counter for progress tracking
frame_count = 0


def annotate_frame(frame, score):
    # Add text with score
    text = str(score)
    org = (10, 150)  # Coordinates for the text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 255, 255)  # White in BGR
    thickness = 2
    cv2.putText(frame, text, org, font, font_scale, color, thickness, cv2.LINE_AA)


def init_array(size):
    array = []
    for i in range(size):
        array.append((-inf, 0, None))
    return array


def write_video(frames):
    for _, _, f in frames:
        # Write frame to output video
        out.write(f)


size = ceil(fps) * int(sys.argv[1])
frames_scores = init_array(size)
i = 0

# Process and write frames to output video
while True:
    ret, frame = cap.read()
    if not ret:
        print("Reached the end of the video or failed to read the frame.")
        break

    # Process frame
    frame, cscore = mm.estimate_best_view(frame)
    cscore = float(cscore)

    if cscore >= frames_scores[0][0]:
        annotate_frame(frame, cscore)
        frames_scores[0] = (cscore, i, frame)
        frames_scores.sort(key=lambda fs: fs[0])
    i += 1
    # Show progress
    frame_count += 1
    if frame_count % 10 == 0:
        progress = (frame_count / total_frames) * 100
        print(f"Progress: {progress:.1f}% ({frame_count}/{total_frames})")

frames_scores.sort(key=lambda fs: fs[1])
write_video(frames_scores)

# Release resources
cap.release()
out.release()
print(f"Video processing complete! Output saved to {OUTPUT_PATH}")

# Optional: Show file info
if os.path.exists(OUTPUT_PATH):
    file_size_mb = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"Output file size: {file_size_mb:.2f} MB")
    print(f"Video duration: {total_frames/fps:.2f} seconds")
