#!/usr/bin/env python3

import os
import sys
from math import ceil

import cv2

from ModelManager import ModelManager


def annotate_frame(frame, score):
    """Draw the score on the frame."""
    text = f"{score:.2f}"
    org = (10, 30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 255, 255)  # white
    thickness = 2
    cv2.putText(frame, text, org, font, font_scale, color, thickness, cv2.LINE_AA)


def main():
    if len(sys.argv) != 4:
        print(
            f"Usage: {sys.argv[0]} <clip_duration_seconds> <input_video> <output_video>"
        )
        sys.exit(1)

    # Parse arguments
    clip_duration_sec = float(sys.argv[1])
    input_path = sys.argv[2]
    output_path = sys.argv[3]

    # Open the input video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {input_path}")
        sys.exit(1)

    # Read properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # How many frames per clip
    window_size = int(ceil(fps * clip_duration_sec))
    if total_frames < window_size:
        print("Error: Video is shorter than the requested clip duration.")
        cap.release()
        sys.exit(1)

    # Initialize model manager
    mm = ModelManager(None)

    # Process every frame, estimate its score, and store scores in a list
    print(f"Scoring all {total_frames} frames...")
    scores = []
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, score = mm.estimate_best_view(frame)
        scores.append(float(score))
        frame_count += 1
        if frame_count % 100 == 0:
            pct = frame_count / total_frames * 100
            print(f"  Scored {frame_count}/{total_frames} frames ({pct:.1f}%)")
    cap.release()

    # Use the actual number of scored frames
    n_scores = len(scores)
    if n_scores < window_size:
        print(
            "Error: Video is shorter than the requested clip duration (after scoring)."
        )
        sys.exit(1)

    # Sliding-window to find the best consecutive clip
    print(f"Finding best {clip_duration_sec:.1f}s clip ({window_size} frames)...")
    current_sum = sum(scores[0:window_size])
    best_sum = current_sum
    best_start = 0

    for i in range(window_size, n_scores):
        current_sum += scores[i] - scores[i - window_size]
        if current_sum > best_sum:
            best_sum = current_sum
            best_start = i - window_size + 1

    best_end = best_start + window_size
    # Guard against overshoot
    best_end = min(best_end, n_scores)

    start_time = best_start / fps
    end_time = best_end / fps
    print(
        f"Best clip frames [{best_start}:{best_end}] "
        f"≈ [{start_time:.2f}s–{end_time:.2f}s], score sum = {best_sum:.2f}"
    )

    # Re-open video, seek to best start frame, and write out the clip
    cap2 = cv2.VideoCapture(input_path)
    cap2.set(cv2.CAP_PROP_POS_FRAMES, best_start)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print("Writing best clip to output...")
    for idx in range(best_start, best_end):
        ret, frame = cap2.read()
        if not ret:
            break
        # Optionally annotate each frame with its score:
        annotate_frame(frame, scores[idx])
        out.write(frame)

    cap2.release()
    out.release()

    # Report output file info
    if os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"Output saved: {output_path} ({size_mb:.2f} MB)")
        print(f"Clip duration: {(best_end - best_start) / fps:.2f} seconds")


if __name__ == "__main__":
    main()
