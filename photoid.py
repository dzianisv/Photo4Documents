#!/usr/bin/env python3
import sys
from majormode.photoidmagick import BiometricPassportPhoto, load_image_and_correct_orientation
from PIL import Image


def get_dpi(image):
    """Get the DPI of an image."""
    dpi_x, dpi_y = image.info.get('dpi', (96, 96))  # default to 96 DPI if not set
    return dpi_x, dpi_y


def preprocess(rgba_image):
    if rgba_image.mode != 'RGBA':
        return rgba_image
      # Create a new white RGB image
    rgb_image = Image.new("RGB", rgba_image.size, "WHITE")
    # Paste the RGBA image onto the RGB image, using the alpha channel as a mask
    rgb_image.paste(rgba_image, (0, 0), rgba_image)
    return rgb_image

def process(input_image, size_mm):
    # Load the image

    dpi = get_dpi(input_image)
    size = int(size_mm[0] * dpi[0] / 25.4), int(size_mm[1] * dpi[1] / 25.4)

    input_image = preprocess(input_image)

    """
     Build an object `BiometricPassportPhoto` from an image.


        @param image: An object `PIL.Image`.

        @param forbid_abnormally_open_eyelid: Indicate whether to allow eyelids
            way too open or too close.

        @param forbid_closed_eye: Indicate whether to check if one or two eyes
            are closed.

        @param forbid_oblique_face: Indicate whether to check if the face is
            oblique.

        @param forbid_open_mouth: Indicate whether to check if the mouth is
            closed with no smile.

        @param forbid_unevenly_open_eye: Indicate whether to check if the 2
            eyelids are evenly open (same area of the visible part of the eyes).


        @param threshold_eyelid_too_closed: A float value used to detect
            whether the eyelids of an eye is narrowed or closed (cf.
            @{link __detect_eyelid_opening_state}).

        @param threshold_eyelid_too_open: A float value used to detect whether
            the eyelids of an eye are widely open (cf.
            @{link __detect_eyelid_opening_state}).

        @param threshold_eye_area_similarity: A float value between `0.0` and
            `1.0` representing the maximum relative difference between the
            visible areas of the two eyes.  This threshold is used to detect
            whether one eye is more open or closed than the other.

        @param threshold_face_features_perpendicularity: A floating point
            number between `0.0` and `1.0` representing the maximum acceptable
            perpendicularity between the midsagittal facial and the
            midhorizontal iris lines.

        @param threshold_face_features_intersection_middle: A floating point
            number between `0.0` and `1.0` representing the default maximum
            acceptable relative between the center point of the midhorizontal
            iris line and the point of intersection between the midsagittal
            facial line with the midhorizontal iris line.

        @param threshold_rima_oris_lips_areas: A floating point number between
            `0.0` and `1.0` representing the default maximum acceptable
            relative difference between the area of the orifice of the mouth
            (rima oris) with the areas of the upper and lower lips.


        @raise BiometricPassportPhotoException: If the photo doesn't comply
            with the requirements for a biometric passport photo.

        @raise ValueError: If the argument `image` is not an object `PIL.Image`.
        """
    passport_photo = BiometricPassportPhoto(input_image,
        forbid_abnormally_open_eyelid=False,
        forbid_oblique_face=False,
        forbid_unevenly_open_eye=False,
    )

    return passport_photo.build_image(size)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]}  <input_image_path> <output_image_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    input_image = load_image_and_correct_orientation(input_path)
    output_path = sys.argv[2]

    image = process(input_image, (40, 50))
    image.save(output_path)
