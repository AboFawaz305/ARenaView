from math import inf

import numpy as np


class ModelManager:
    def __init__(self, frames_manager) -> None:
        self.frames_manager = frames_manager

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
            - The ball position is very near from the center(-100 * ball_distance)
        """
        best_frame_score = -inf
        best_frame = np.zeros(shape=frames[0].shape)
        for frame in frames:
            current_score = 0
            # TODO: Detect the ball using yolov5
            ball_detected = False

            if ball_detected:
                current_score += 10_000

                # TODO: Calculate the ball distance from center
                ball_distance_from_center = 0

                current_score += -100 * ball_distance_from_center
            if current_score > best_frame_score:
                best_frame_score = current_score
                best_frame = frame

            return frame
