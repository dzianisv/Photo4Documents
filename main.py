#!/usr/bin/env python3
import sys
import background
import photoid
import prepartial
import logging
import argparse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stderr))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--align-shoulders', action='store_true', help='align shoulders')
    parser.add_argument('--size', type=str, default='40x50', help='40x50mm EU passport, 55x55mm (600x600px) US passport')
    parser.add_argument('input_path', help='input path')
    parser.add_argument('output_path', help='output path')
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path

    h,w = args.size.split('x')
    size = (int(h), int(w)) 

    logger.info("Loading image \"%s\"...", input_path)
    image = photoid.load_image_and_correct_orientation(input_path)
    dpi = image.info.get('dpi')

    if args.align_shoulders:
        from align_shoulders import align_shoulders
        logger.info("Aligning shoulders...")
        image = align_shoulders(image)
    
    logger.info("Removing background...")
    image = background.process(image)
    image.save("_background-removed.png", dpi=dpi)

    logger.info("Cropping image to \"%s\"...", size)
    image = photoid.process(image, size)
    image.save("_cropped.png", dpi=dpi)

    logger.info("Placing photos on the list...")
    image = prepartial.process(image, dpi=dpi)

    logger.info("Saving image to \"%s\"...", output_path)
    image.save(output_path)