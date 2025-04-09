"""
Continuously send the data you recorded to the server. This file should work on
the device.
"""

import time

import cv2 as cv
import requests

SERVER_URL = "https://url-to-server.com"
REGISTER_ENDPOINT = f"{SERVER_URL}/registsr-device"
FRAME_ENDPOINT = f"{SERVER_URL}/frame"

# Register on the server
registeration = requests.get(REGISTER_ENDPOINT)

# TODO: Handle possible Errors after registering the device

device_id = registeration.json()["device_id"]
token = registeration.json()["token"]


video = cv.VideoCapture(0)
if not video.isOpened():
    # TODO: Implement a recovery mechanism to deal with non opening devices
    print("Cant open video")
    quit()

i = 1
while True:
    # Take a frame
    ret, frame = video.read()
    if not ret:
        # Handle non received frames.
        if i > 10:
            print("Cant receive frame Exiting.")
            quit()
        print("Cant receive frame waiting for {(2**i)*10}ms")
        time.sleep((2**i) * 10 / 1000)
        i += 1
        continue
    i = 1
    # Send the frame
    json = {"device_id": device_id, "token": token, "frame": frame}
    response = requests.post(FRAME_ENDPOINT, json=json)

    # TODO: Handle response errors.

    # Repeat
