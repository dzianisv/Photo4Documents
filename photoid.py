#!/usr/bin/env python3
import sys
from photoidmagick import PhotoImage, Country

def process(input_path, output_path):
    # Load the image
    image = PhotoImage(input_path)

    # Crop the image passport
    photo = image.crop(Country.BELARUS)

    # Save the cropped image
    photo.save(output_path)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]}  <input_image_path> <output_image_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    process(input_path, output_path)
