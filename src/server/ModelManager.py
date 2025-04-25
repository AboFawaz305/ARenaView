from math import inf

import numpy as np
from ultralytics import YOLO


class ModelManager:
    def __init__(self, frames_manager=None) -> None:
        self.frames_manager = frames_manager
        # Modern approach using ultralytics package
        self.model = YOLO("best.pt")

    def estimate_best_view(self, frames):
        # Handle single frame case
        if isinstance(frames, np.ndarray) and len(frames.shape) == 3:
            frames = [frames]

        best_frame_score = -inf
        best_frame = np.zeros(shape=frames[0].shape)

        for frame in frames:
            current_score = 0
            ball_detected, bpx, bpy = self.detect_ball(frame)
            goal_detected, gpx, gpy = self.detect_goal(frame)

            if ball_detected:
                current_score += 1000
                ball_distance_from_center = abs(bpx) + abs(bpy)
                current_score -= (ball_distance_from_center / 100) ** 2

            if goal_detected:
                current_score += 1000
                goal_distance_from_center = abs(gpx) + abs(gpy)
                current_score -= (goal_distance_from_center / 100) ** 2

            if current_score > best_frame_score:
                best_frame_score = current_score
                best_frame = frame

            # if ball_detected and goal_detected:
            #     current_score += 1000

        return best_frame, str(best_frame_score)

    def detect_ball(self, frame):
        results = self.model(frame)
        for result in results:
            for box in result.boxes:
                if result.names[int(box.cls)] == "ball":
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                    return True, cx, cy
        return False, inf, inf

    def detect_goal(self, frame):
        results = self.model(frame)
        for result in results:
            for box in result.boxes:
                if result.names[int(box.cls)] == "goal":
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                    return True, cx, cy
        return False, inf, inf
