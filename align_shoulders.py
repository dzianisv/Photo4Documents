#!/usr/bin/env python3
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image

def align_shoulders(image_pil):
    # Convert PIL image to OpenCV format
    image_rgb = np.array(image_pil)
    image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)

    # Process the image to detect pose
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        print("No shoulders detected.")
        return image_pil  # Return the original image if no shoulders are detected

    # Get landmarks
    landmarks = results.pose_landmarks.landmark

    # Shoulder coordinates
    left_shoulder = np.array([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y])
    right_shoulder = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y])

    # Calculate the angle to align shoulders horizontally
    angle = np.degrees(np.arctan2(left_shoulder[1] - right_shoulder[1],
                                  left_shoulder[0] - right_shoulder[0]))

    # Rotate the image to align shoulders horizontally
    rotated_image = image_pil.rotate(-angle, resample=Image.BICUBIC, expand=True)

    return rotated_image

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python align_shoulders.py <input_image> <output_image>")
    else:
        input_image_path = sys.argv[1]
        output_image_path = sys.argv[2]
        input_image = Image.open(input_image_path)
        rotated_image = align_shoulders(input_image)
        rotated_image.save(output_image_path) 