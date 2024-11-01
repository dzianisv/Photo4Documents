#!/usr/bin/env python3

# model required https://www.kaggle.com/datasets/sergiovirahonda/shape-predictor-68-face-landmarksdat
# curl -L https://raw.githubusercontent.com/italojs/facial-landmarks-recognition/refs/heads/master/shape_predictor_68_face_landmarks.dat  >  shape_predictor_68_face_landmarks.dat

from PIL import Image
import dlib
import numpy as np
import sys

def align_face(input_path, output_path):
    # Load the image and ensure it's RGB
    image = Image.open(input_path).convert('RGB')
    image_np = np.array(image)

    # Initialize dlib's face detector and shape predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    # Detect faces in the image
    dets = detector(image_np, 1)

    if len(dets) == 0:
        print("No faces detected.")
        return

    # Assume the first detected face is the one to align
    face = dets[0]

    # Get the landmarks
    shape = predictor(image_np, face)
    landmarks = [(shape.part(i).x, shape.part(i).y) for i in range(68)]

    # Use the tip of the nose and the base of the nose
    nose_tip = np.array(landmarks[30])
    nose_base = np.array(landmarks[33])

    # Calculate the angle to rotate the image
    angle = np.degrees(np.arctan2(nose_base[0] - nose_tip[0], nose_base[1] - nose_tip[1]))

    # Rotate the image to align the nose vertically
    rotated_image = image.rotate(angle, resample=Image.BICUBIC, expand=True)

    # Save the aligned image
    rotated_image.save(output_path)
    print(f"Aligned image saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python align_face.py <input_image> <output_image>")
    else:
        input_image_path = sys.argv[1]
        output_image_path = sys.argv[2]
        align_face(input_image_path, output_image_path)