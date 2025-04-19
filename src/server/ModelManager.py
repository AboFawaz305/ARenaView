from math import inf

import numpy as np
import torch


class ModelManager:
    """
    This class reponsibility is to process the frames retreived from
    frames_manager and return the best frame with enhancements if any
    """

    def __init__(self, frames_manager) -> None:
        self.frames_manager = frames_manager
        # Initialize the model
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5s")

    def get_frame(self):
        frames = self.frames_manager.get_frames()

        return self.estimate_frame(frames)

    def estimate_frame(self, frames):
        frame = self.estimate_best_view(frames)

        # TODO: ADD a code to add effects to the best view frame
        return frame

    def estimate_best_view(self, frames):
        """
        This algorithm determines the best frame based on score that is
        calculated based on the following criteria:
            - The frame has the ball in it(10000)
            - The ball position is very near from the center(-10 * ball_distance)
        """
        best_frame_score = -inf
        best_frame = np.zeros(shape=frames[0].shape)
        for frame in frames:
            current_score = 0
            # TODO: Detect the ball using yolov5
            ball_detected, px, py = self.detect_ball(frame)

            if ball_detected:
                # This score is very high to make sure we want choose a frame
                # that dont have a ball in it.
                current_score += 100_000

                # Calculate the ball distance from the ceneter using manhattan
                # distance
                ball_distance_from_center = abs(px) + abs(py)

                current_score += -10 * ball_distance_from_center
            if current_score > best_frame_score:
                best_frame_score = current_score
                best_frame = frame

        return best_frame

    def detect_ball(self, frame):
        results = self.model(frame)

        for obj in results.pandas.xyxy:
            if obj.name == "ball":
                xn = obj.xmin
                xx = obj.xmax
                yn = obj.ymin
                yx = obj.ymax
                # calculate x and y of the center of the detected ball
                cx, cy = ((xn + xx) / 2, (yn + yx) / 2)
                return True, cx, cy
        return False, inf, inf
