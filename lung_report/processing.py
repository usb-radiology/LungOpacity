import os
import time
from functools import reduce
from pathlib import Path

import nibabel as nib
import numpy as np
from skimage.color import gray2rgb
from skimage.io import imsave

import hu_ranges
from quantification import hu_summaries


def open_images(image, mask):
    print(f"Got image: {image}, mask:{mask}")
    img_nifti = nib.load(image)
    mask_nifti = nib.load(mask)
    img = img_nifti.get_fdata()
    mask = np.squeeze(mask_nifti.get_fdata())
    return (
        np.rot90(np.flipud(img), 3),
        np.rot90(np.flipud(mask), 3),
        np.prod(img_nifti.header["pixdim"]),
        mask_nifti.affine,
    )


def create_images(image: str, mask: str, output_dir):
    start = time.time()
    image_data, lung_mask_data, pixdim_prod, affine = open_images(image, mask)
    end = time.time()
    print(f"Opening images and masks took: {end-start:.3f} sec")

    start = time.time()
    mask = create_mask_for_all_slices(image_data, lung_mask_data)
    end = time.time()
    print(f"Creating masks for all slices took: {end-start:.3f} sec")
    overlay = nib.Nifti1Image(np.rot90(np.flipud(mask), -3, (1, 0)), affine)
    filename_overlay = output_dir / "color_overlay.nii.gz"
    overlay.to_filename(filename_overlay)

    z_axis = np.sum(lung_mask_data, axis=(0, 1))
    z_indexes = np.argwhere(z_axis > 0)
    # + 5 is just a soft margin to add
    first_index = z_indexes[0][0] + 5
    last_index = z_indexes[-1][0]
    range_index = last_index - first_index
    step = range_index // 15
    result = []

    start = time.time()
    for i in range(first_index, last_index - step, step):
        i_data = create_image_for(image_data, mask, i)
        filename_overlay = output_dir / Path(
            Path(image).stem + "_" + str(i) + "_overlay.png"
        )
        imsave(filename_overlay, i_data)
        result.append(filename_overlay)
    end = time.time()
    print(f"Creating overlay images took: {end-start:.3f} sec")
    return result, hu_summaries(image_data, lung_mask_data), pixdim_prod


def colorize(clipped, hu_range, color):
    r_min, r_max = hu_range
    clipped = np.where((np.logical_and(clipped > r_min, clipped <= r_max)), 1, 0)
    z = gray2rgb(clipped) * np.array(color)
    return z.astype(np.uint8)


def create_mask_for_all_slices(image_data, lung_mask_data):
    clipped = lung_mask_data * image_data
    result = (
        colorize(clipped, hu_range, color)
        for (hu_range, color) in zip(hu_ranges.get_hu_ranges(), hu_ranges.get_colors())
    )
    return reduce(np.add, result)


def create_image_for(image_data, mask, slice: int, alpha=0.75):
    overlay = (
        gray2rgb(image_data[:, :, slice]) * (1.0 - alpha) + mask[:, :, slice] * alpha
    )
    # https://stackoverflow.com/questions/1735025/how-to-normalize-a-numpy-array-to-within-a-certain-range
    overlay = 255 * (overlay - np.min(overlay)) / np.ptp(overlay).astype(int)
    return overlay.astype(np.uint8)
