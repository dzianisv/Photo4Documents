#!/usr/bin/env python3
import cv2
from PIL import Image
import sys

def get_dpi(image_path):
    with Image.open(image_path) as img:
        dpi = img.info.get('dpi', (96, 96))
    return dpi

def detect_and_crop_head(image_path, output_path):
    # Get the DPI of the image
    dpi_x, dpi_y = get_dpi(image_path)

    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Load the Haar Cascade Classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the image to grayscale for better face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    i = 0
    for (x, y, w, h) in faces:
        # Enlarge the bounding box by 30% to capture the head
        offset = int(h * 0.5)
        x_offset = 0
        y = max(y - offset, 0)
        h += 2 * offset


        # Crop the head with the desired ratio 35x45
        aspect_ratio = 35/45
        if w > h * aspect_ratio:
            target_h = int(w / aspect_ratio)
            h = target_h
        else:
            target_w = int(h * aspect_ratio)
            x_offset = int(max(0, int((target_w - w) / 2)))
            print("x offset:", x_offset)
            x -= x_offset

        head = image[y:y+h, x:x + w]

        # Resize to 35x45mm based on extracted DPI
        new_width = int(35 * dpi_x / 25.4)
        new_height = int(45 * dpi_y / 25.4)
        resized_head = cv2.resize(head, (new_width, new_height))

        # Save the result
        cv2.imwrite(f"{i}-{output_path}", resized_head)
        i += 1

# Usage
detect_and_crop_head(sys.argv[1], sys.argv[2])
