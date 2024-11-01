#!/usr/bin/env python3

import cv2
import numpy as np
import mediapipe as mp
from PIL import Image

def align_shoulders(input_path, output_path):
    # Load the image
    image = cv2.imread(input_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)

    # Process the image to detect pose
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        print("No shoulders detected.")
        return

    # Get landmarks
    landmarks = results.pose_landmarks.landmark

    # Shoulder coordinates
    left_shoulder = np.array([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y])
    right_shoulder = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y])

    # Calculate the angle to align shoulders horizontally
    angle = np.degrees(np.arctan2(right_shoulder[1] - left_shoulder[1],
                                  right_shoulder[0] - left_shoulder[0]))

    # Rotate the image to align shoulders horizontally
    image_pil = Image.fromarray(image_rgb)
    rotated_image = image_pil.rotate(-angle, resample=Image.BICUBIC, expand=True)

    # Save the aligned image
    rotated_image.save(output_path)
    print(f"Aligned image saved to {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python align_shoulders.py <input_image> <output_image>")
    else:
        input_image_path = sys.argv[1]
        output_image_path = sys.argv[2]
        align_shoulders(input_image_path, output_image_path)