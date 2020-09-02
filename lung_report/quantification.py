import numpy as np


def hu_summaries(image_data, lung_mask_data):
    data = image_data * lung_mask_data
    total = lung_mask_data.sum()
    bins = np.array(
        [
            ((data > -1000) & (data <= -901)).sum(),
            ((data > -901) & (data <= -801)).sum(),
            ((data > -801) & (data <= -701)).sum(),
            ((data > -701) & (data <= -601)).sum(),
            ((data > -601) & (data <= -501)).sum(),
            ((data > -501) & (data <= -401)).sum(),
            ((data > -401) & (data <= -301)).sum(),
            ((data > -301) & (data <= -201)).sum(),
            ((data > -201) & (data <= -101)).sum(),
            ((data > -101) & (data < 0)).sum(),
        ]
    )
    return bins * 100 / total, bins
