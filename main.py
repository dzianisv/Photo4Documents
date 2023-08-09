#!/usr/bin/env python3
import sys
import background
import photoid
import prepartial
import logging
import exifread

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stderr))

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    size = (40, 50)

    logger.info("Loading image %s...", input_path)
    image = photoid.load_image_and_correct_orientation(input_path)

    logger.info("Removing background...")
    image = background.process(image)

    logger.info("Cropping image to %s...", size)
    image = photoid.process(image, size)

    logger.info("Placing photos on the list...")
    image = prepartial.process(image)

    logger.info("Saving image to %s...", output_path)
    image.save(output_path)