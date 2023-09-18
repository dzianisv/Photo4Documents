#!/usr/bin/env python3
import sys
import math
import argparse
from PIL import Image, ImageDraw, ImageFont
import re

INCH=25.4
PADDING=3
TARGET_DPI=300

def parse_size_string(size_str):
    match = re.match(r'(\d+)x(\d+)(mm|inch)?$', size_str)
    if match:
        width, height, units = match.groups()
        width, height = int(width), int(height)

        # Convert to millimeters if units are inches
        if units == "inch":
            width = int(width * 25.4)
            height = int(height * 25.4)
        elif not units or units == "mm":
            pass
        else:
            raise ValueError(f"Unsupported units in size string: {units}")

        return width, height
    else:
        raise ValueError(f"Invalid size string format: {size_str}")

def estimate_dpi(img: Image, size_mm=(35, 45)):
    # Get pixel dimensions
    width_px, height_px = img.size

    # Convert physical dimensions from mm to inches
    width_inch = size_mm[0] / INCH
    height_inch = size_mm[1] / INCH

    # Calculate DPI
    dpi_x = width_px / width_inch
    dpi_y = height_px / height_inch
    return math.ceil(dpi_x), math.ceil(dpi_y)

def get_dpi(image):
    """Get the DPI of an image."""
    return image.info.get('dpi', None)

def set_dpi(image, size_mm=(35, 45)):
    """Set the DPI of an image."""
    dpi = estimate_dpi(image, size_mm)
    image.info['dpi'] = dpi
    return dpi

def print_label(text: str, canvas):
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    text_width, text_height = draw.textsize(text, font=font)
    x = (canvas.width - text_width) / 2
    y = canvas.height - text_height - 10  # 10 pixels padding from the bottom
    draw.text((x, y), text, fill="black", font=font)

def process(input_image, label=None, canvas_size_mm=(100, 150)):
    # Open the input image
    dpi_x, dpi_y = get_dpi(input_image)

    # Convert the canvas size from mm to pixels
    padding = int(PADDING * dpi_x / INCH)  # padding 3mm
    canvas_width = int(canvas_size_mm[0] / INCH * dpi_x)
    canvas_height = int(canvas_size_mm[1] / INCH * dpi_y)
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    print(f"Source photos size {input_image.width * INCH / dpi_x}x{input_image.height * INCH / dpi_y}mm")
    # Calculate how many input images can fit on the canvas
    num_images_x = canvas_width // (input_image.width + padding)
    num_images_y = canvas_height // (input_image.height + padding)
    print(f"Photos: {num_images_x}x{num_images_y}")

    # Center photos if they don't fill up the entire canvas
    total_width_of_images = num_images_x * (input_image.width + padding)
    total_height_of_images = num_images_y * (input_image.height + padding)
    offset_x = (canvas_width - total_width_of_images) // 2
    offset_y = (canvas_height - total_height_of_images) // 2

    draw = ImageDraw.Draw(canvas)
    guide_line_lenght = int(0.1 * min(canvas.height, canvas.width))

    # Paste as many images as possible onto the canvas
    for x in range(num_images_x):
        image_paste_x = offset_x + x * (input_image.width + padding)

        # draw vertical guide lines
        draw.line([(image_paste_x-1, 0), (image_paste_x-1, guide_line_lenght)], fill="black")
        draw.line([(image_paste_x + input_image.width+1, 0), (image_paste_x + input_image.width+1, guide_line_lenght)], fill="black")

        draw.line([(image_paste_x-1, canvas.height-guide_line_lenght), (image_paste_x-1, canvas.height)], fill="black")
        draw.line([(image_paste_x + input_image.width+1, canvas.height-guide_line_lenght), (image_paste_x + input_image.width+1, canvas.height)], fill="black")

        for y in range(num_images_y):
            image_paste_y = offset_y + y * (input_image.height + padding)

            canvas.paste(input_image, (image_paste_x, image_paste_y))

            # draw horizontal guide lines
            draw.line([(0, image_paste_y), (guide_line_lenght, image_paste_y)], fill="black")
            draw.line([(0, image_paste_y + input_image.height+1), (guide_line_lenght,  image_paste_y + input_image.height+1)], fill="black")

            draw.line([(canvas_width-guide_line_lenght, image_paste_y), (canvas_width, image_paste_y)], fill="black")
            draw.line([(canvas_width-guide_line_lenght, image_paste_y + input_image.height+1), (canvas_width,  image_paste_y + input_image.height+1)], fill="black")

    if label:
        print_label(label, canvas)

    # Save the resulting canvas
    # canvas.save(output_image_path, dpi=(dpi_x, dpi_y))
    return canvas

if __name__ == '__main__':
    # Get the command line arguments
    import argparse

def main():
    parser = argparse.ArgumentParser(description="Process an image")

    # Positional arguments for input and output image paths
    parser.add_argument("input_image", help="Path to the input image")
    parser.add_argument("output_image", help="Path to save the processed image")

    # Optional argument for label
    parser.add_argument("--label", type=str, default="", help="Label text to be added to the image")

    # Optional argument for input image size with a default value of 35x45
    parser.add_argument("--input-image-size", type=str, default="35x45mm",
                        help="Size of the input image in format WxH (e.g., 35x45mm)")

    # Optional argument for output canvas size with a default value of 100x150mm
    parser.add_argument("--output-canvas-size", type=str, default="100x150mm",
                        help="Size of the output canvas in format WxH<unit> (e.g., 100x150mm or 4x6inch)")

    args = parser.parse_args()

    input_image = Image.open(args.input_image)

    if args.input_image_size:
        if not get_dpi(input_image):
            set_dpi(input_image, parse_size_string(args.input_image_size))

    image = process(input_image, args.label, canvas_size_mm=parse_size_string(args.output_canvas_size))
    image.save(args.output_image, dpi=get_dpi(input_image))

if __name__ == "__main__":
    main()