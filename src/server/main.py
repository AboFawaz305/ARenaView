import random
import time

from flask import Flask, jsonify, request

from FramesManager import FramesManager
from ModelManager import ModelManager

app = Flask(__name__)

# Initialize FramesManager with 22 input sources
# The frames manager job is to gather frames from the body cams and organize
# them so that they can be processed by the model manager
frames_manager = FramesManager()

# Initialize ModelManager with the framesManager
# The model manager job is to process frames and then choose the best view from them and
# add some enhancements on them
model_manager = ModelManager(frames_manager)

tokens = set()


@app.route("/register-device")
def register_device():
    """
    This API endpoint will register bodycams on players and send an ID and a token to each
    bodycam.
    """
    # TODO: a verification step to register devices securely
    device_id = frames_manager.add_new_source()

    # TODO: use a more secure algorithm to generate tokens
    token = random.randint(10000, 100_000)
    tokens.add(token)

    return jsonify({"device-id": device_id, "token": token}), 200


@app.route("/frame", methods=["POST"])
def received_frame():
    """
    This API endpoint receive frames from the bodycams on the players
    The received data should contain the body cam ID and the frame data
    """

    # Make sure that the request is valid
    if request.method != "POST":
        return "Method Not Allowed", 405
    if not request.is_json:
        return "Bad Request", 400

    json = request.get_json()
    frame = json["frame"]
    device_id = json["device_id"]
    token = json["token"]

    # Make sure the data is valid
    if frame is None or device_id is None or token is None:
        return "Bad Request", 400

    if token not in tokens or device_id not in frames_manager.devices_ids:
        return "Unauthorized", 401

    frames_manager.add_frame(device_id, frame)
    return "Success", 200


@app.route("/frame")
def viewer_connect():
    """
    This API endpoint send the latest choosen frame with the enhancements from
    the model
    """
    # return the good frame with modifications if any from the model
    frame = model_manager.get_frame()

    return jsonify({"frame": frame}), 200


if __name__ == "__main__":
    # Run flask in multi threaded mode
    app.run(threaded=True)
