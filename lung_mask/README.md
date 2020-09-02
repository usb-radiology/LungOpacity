# Lung Segmentation Covid-19

## Pre-requistes
To run this pipeline, Git, Python und CUDA 9.0 incl. the 4 patches needs to be installed on the system.

## Setup environment
```shell
mkdir LungMask_USBnet && cd LungMask_USBnet

git clone --single-branch \
   --branch krn_branch https://gitlab.uhbs.ch/yangsh/niftynet.git

 git --git-dir ./niftynet/.git --work-tree ./niftynet \
    reset --hard 808027e671

# install Python virtual environment for GPU compute
python3 -m venv lungmask_usbnet_venv --clear

#  activate Pyhton virtual environment
source $(pwd)/lungmask_usbnet_venv/bin/activate

python -m pip install --upgrade pip

# install Python virtual environment for GPU compute
python -m pip install -r niftynet/requirements-gpu.txt

# install Python virtual environment for CPU compute
python -m pip install -r niftynet/requirements-cpu.txt

# recommended but optional packages
python -m pip install SimpleITK scikit-image pyaml opencv-python antspyx

# install NiftyNet
python -m pip install -e ./niftynet
python -c "import tensorflow as tf; tf.Session(); print(tf.__version__)"
```

At this stage, the TensorFlow version should be displayed as 1.12.0. Now, we install LungMask-USBnet. Note, that the commands for Windows 10 and Linux differ.

## clone LungMask-USBnet project
```shell

## Linux
GIT_LFS_SKIP_SMUDGE=1 \
   git clone git@gitlab.uhbs.ch:yangsh/lungmask_usbnet.git

## Windows 10
$Env:GIT_LFS_SKIP_SMUDGE=1;
git clone git@gitlab.uhbs.ch:yangsh/lungmask_usbnet.git
```
Then, we download the models and optionally test data.

```shell
# download models and test data
git -C ./lungmask_usbnet lfs pull --include niftynet_model
git -C ./lungmask_usbnet lfs pull --include test_data
```
### run the code 
```shell
# run the test data
python ./lungmask_usbnet/lungmask.py

# run own data
python ./lungmask_usbnet/lungmask.py -i nifti_inputpath -o nifti_outputpath
```
