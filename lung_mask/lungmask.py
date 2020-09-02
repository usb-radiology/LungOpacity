import argparse
import os
import numpy as np
import shutil
import subprocess
import ants
import nibabel as nib
from scipy.ndimage.measurements import label
from scipy.ndimage.morphology import generate_binary_structure
import skimage.measure
from skimage import morphology


scriptDirectory = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(
    description='single case inference with NiftyNet')
parser.add_argument('-i', action='store', dest='filepath',
                    default='/data/thoraxct.nii')
parser.add_argument('-o', action='store', dest='output',
                    default='/data/pred.nii.gz')
parser.add_argument('-model_dir', action='store',
                    dest='model_dir', default='./niftynet_model')
parser.add_argument('-conf', action='store',
                    dest='conf', default='./conf_3d.ini')

res = parser.parse_args()


def keep_largest_two_components(mask):
    mask = morphology.remove_small_holes(mask, 1000, connectivity=1)
    mask = skimage.measure.label(mask)
    regions = skimage.measure.regionprops(mask)
    voxsum = np.asarray([x.area for x in regions])
    ind = np.argsort(voxsum)
    voxsum = voxsum[ind]
    if voxsum[-2] < voxsum[-1]*0.25:
        mask = mask == ind[-1]+1
    else:
        mask = (mask == ind[-1]+1) | (mask == ind[-2]+1)
    return mask


cwd = os.path.dirname(os.path.realpath(__file__))
os.chdir(cwd)

conf_path = os.path.join(cwd, res.conf)

s_dir = os.path.dirname(os.path.realpath(res.filepath))
tmp_dir = os.path.join(s_dir, 'tmp')

output = os.path.realpath(res.output)

os.makedirs(tmp_dir, exist_ok=True)
raw = ants.image_read(res.filepath)

print("downsampling thorax CT")
raw_down = ants.resample_image(raw, (2, 2, 2), interp_type=1)
ants.image_write(raw_down, os.path.join(tmp_dir, 'ct_down.nii.gz'), ri=True)

model_dir = os.path.realpath(res.model_dir)
print("prediction with niftynet")

icommand = " net_run inference -c " + conf_path + \
    " -a niftynet.application.segmentation_application.SegmentationApplication \
    --model_dir=" + model_dir + \
    " --image=inference_data" \
    " --save_seg_dir=" + tmp_dir

print(icommand)
os.chdir(s_dir)
subprocess.call(['cd ' + s_dir], shell=True, executable='/bin/bash')
subprocess.call(icommand, shell=True, executable='/bin/bash')

print("postproccessing")
hdr = nib.load(os.path.join(tmp_dir, 'ct_down_pred.nii.gz'))
data = np.squeeze(hdr.get_fdata())
structure = generate_binary_structure(3, 1)
unique_labels = np.unique(data)
mask = keep_largest_two_components(data == unique_labels[1])
newhdr = nib.Nifti1Image(mask, hdr.affine, hdr.header)
newhdr.set_data_dtype(hdr.get_data_dtype())
nib.save(newhdr, os.path.join(tmp_dir, 'ct_down_pred_post.nii.gz'))

print("upsampling thorax CT")
pred_down = ants.image_read(os.path.join(tmp_dir, 'ct_down_pred_post.nii.gz'))
pred = ants.resample_image_to_target(
    pred_down, raw, interp_type=1, verbose=True)

print(output)
ants.image_write(pred, output, ri=True)

img_mask = pred.numpy()
img_raw = raw.numpy()
img_lung = img_raw*img_mask
lesion_mask = (img_lung > -600) & (img_lung < 0)
file1 = open(os.path.join(s_dir, "output.txt"), "w")
file1.writelines("{:.2f}".format(np.sum(lesion_mask) /
                                 np.sum(img_mask)*100).format() + "%")
file1.close()


shutil.rmtree(tmp_dir)
