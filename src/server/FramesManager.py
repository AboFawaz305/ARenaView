from math import inf


class FramesManager:
    def __init__(self) -> None:
        self.devices_ids = []
        self.devices_frames = dict()

    def add_frame(self, device_id, frame):
        self.devices_frames[device_id] = frame

    def add_new_source(self):
        did = -inf
        for x in self.devices_ids:
            did = x if x > did else did
        # Return a non existent id
        self.devices_ids.append(did + 1)
        return did + 1

    def get_frames(self):
        return self.devices_frames
