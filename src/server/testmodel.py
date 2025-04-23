import cv2

from ModelManager import *

# Define the path to the video file
VIDEO_PATH = "./v.mp4"  # Replace with your actual video file path

# Create a VideoCapture object
cap = cv2.VideoCapture(VIDEO_PATH)

# Check if the video file was successfully opened
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

mm = ModelManager(None)

# Read and display frames in a loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Reached the end of the video or failed to read the frame.")
        break

    frame, score = mm.estimate_best_view(frame)
    # Define the text and its properties
    text = score
    org = (10, 30)  # Coordinates for the bottom-left corner of the text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 255, 255)  # White color in BGR
    thickness = 2

    # Add text to the image
    cv2.putText(frame, text, org, font, font_scale, color, thickness, cv2.LINE_AA)

    # Display the current frame
    cv2.imshow("Video Frame", frame)

    # Wait for 25 ms and check if the 'q' key is pressed to exit
    if cv2.waitKey(25) & 0xFF == ord("q"):
        print("Playback interrupted by user.")
        break

# Release the VideoCapture object and close display windows
cap.release()
cv2.destroyAllWindows()
