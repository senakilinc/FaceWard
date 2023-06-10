import cv2
import os

def save_video_screenshots(video_path, screenshot_folder):
    # Create the screenshot folder if it doesn't exist
    os.makedirs(screenshot_folder, exist_ok=True)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get the frames per second (fps) of the video
    fps = video.get(cv2.CAP_PROP_FPS)

    # Set the number of frames to skip between each screenshot
    skip_frames = int(fps / 10)  # Save 10 frames per second

    # Initialize the current frame number and screenshot number
    current_frame = 0
    screenshot_num = 0

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Loop through each frame of the video
    while True:
        # Read the next frame
        ret, frame = video.read()
        if not ret:
            break

        # Increment the current frame number
        current_frame += 1

        # If it's time to save a screenshot, do so
        if current_frame % skip_frames == 0:
            # Detect faces in the frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # If a face is detected, crop the frame to include only the face and save it as a screenshot
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                face_frame = frame[y:y+h, x:x+w]
                screenshot_path = os.path.join(screenshot_folder, f"{screenshot_num}.jpg")
                cv2.imwrite(screenshot_path, face_frame)
                screenshot_num += 1

    # Release the video file
    video.release()
