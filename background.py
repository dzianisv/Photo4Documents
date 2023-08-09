#!/usr/bin/env python3
import sys
import torch
from carvekit.api.high import HiInterface
import tempfile
import os
import PIL

def remove_background(image_path):
    # Check doc strings for more information`
    interface = HiInterface(object_type="hairs-like",  # Can be "object" or "hairs-like".
                            batch_size_seg=5,
                            batch_size_matting=1,
                            device='cuda' if torch.cuda.is_available() else 'cpu',
                            seg_mask_size=640,  # Use 640 for Tracer B7 and 320 for U2Net
                            matting_mask_size=2048,
                            trimap_prob_threshold=231,
                            trimap_dilation=30,
                            trimap_erosion_iters=5,
                            fp16=False)

    images_without_background = interface([image_path])
    return images_without_background[0]

def process(image):
    with tempfile.TemporaryDirectory() as temp_dir:
        pre_path = os.path.join(temp_dir, "pre-background-removal.png")
        post_path = os.path.join(temp_dir, "post-background-removal.png")

        image.save(pre_path)
        result_image = remove_background(pre_path)
        result_image.save(post_path)
        print(temp_dir)
        return PIL.Image.open(post_path)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]}  <input_image_path> <output_image_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    image = remove_background(input_path)
    image.save(output_path)
