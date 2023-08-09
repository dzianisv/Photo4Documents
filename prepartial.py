#!/usr/bin/env python3
import sys
from PIL import Image, ImageDraw

INCH=25.4
PADDING=3
def get_dpi(image):
    """Get the DPI of an image."""
    dpi_x, dpi_y = image.info.get('dpi', (96, 96))  # default to 96 DPI if not set
    return dpi_x, dpi_y

def main():
    # Get the command line arguments
    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2]

    # Open the input image
    input_image = Image.open(input_image_path)
    dpi_x, dpi_y = get_dpi(input_image)

    # Convert the canvas size from mm to pixels
    padding = int(PADDING * dpi_x / INCH)  # padding 3mm
    canvas_width = int(100 / INCH * dpi_x)
    canvas_height = int(150 / INCH * dpi_y)
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")

    # Calculate how many input images can fit on the canvas
    num_images_x = canvas_width // (input_image.width + padding)
    num_images_y = canvas_height // (input_image.height + padding)

    # Center photos if they don't fill up the entire canvas
    total_width_of_images = num_images_x * (input_image.width + padding)
    total_height_of_images = num_images_y * (input_image.height + padding)
    offset_x = (canvas_width - total_width_of_images) // 2
    offset_y = (canvas_height - total_height_of_images) // 2

    draw = ImageDraw.Draw(canvas)

    # Paste as many images as possible onto the canvas
    for x in range(num_images_x):
        image_paste_x = offset_x + x * (input_image.width + padding)

        # draw vertical guide lines
        draw.line([(image_paste_x-1, 0), (image_paste_x-1, canvas.height)], fill="black")
        draw.line([(image_paste_x + input_image.width+1, 0), (image_paste_x + input_image.width+1, canvas.height)], fill="black")

        for y in range(num_images_y):
            image_paste_y = offset_y + y * (input_image.height + padding)

            canvas.paste(input_image, (image_paste_x, image_paste_y))

            # draw horizontal guide lines
            draw.line([(0, image_paste_y), (canvas_width, image_paste_y)], fill="black")
            draw.line([(0, image_paste_y + input_image.height+1), (canvas_width,  image_paste_y + input_image.height+1)], fill="black")

    # draw last guide lines

    # Save the resulting canvas
    canvas.save(output_image_path, dpi=(dpi_x, dpi_y))

if __name__ == '__main__':
    main()
