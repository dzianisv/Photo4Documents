#!/usr/bin/env python3
import sys
import background
import photoid
import prepartial
import logging
import exifread
from align_shoulders import align_shoulders

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stderr))

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    size = (40,50)

    logger.info("Loading image \"%s\"...", input_path)
    image = photoid.load_image_and_correct_orientation(input_path)
    dpi = image.info.get('dpi')

    logger.info("Aligning image")
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