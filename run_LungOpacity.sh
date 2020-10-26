#!/bin/bash

dcmfile=$(ls -t /docker/shs/in/*.dcm | head -n 1)

dcm2niix -m y -o /docker/shs/tmp /docker/shs/in/

file=$(ls -t /docker/shs/tmp/*.nii | head -n 1)


source /venv_niftynet/bin/activate
python3.5 /apps/LungOpacity/lung_mask/lungmask.py -i $file -o /docker/shs/tmp/mask.nii.gz -model_dir /apps/niftynet_model -conf /apps/LungOpacity/lung_mask/conf_3d.ini
deactivate 

source /venv_report/bin/activate
python3.6 /apps/LungOpacity/lung_report/main.py -i $file -m  /docker/shs/tmp/mask.nii.gz -o  /docker/shs/tmp/

img2dcm -stf $dcmfile  /docker/shs/tmp/report.jpg /docker/shs/out/lungopacity_report.dcm

chmod 777 /docker/shs/out/lungopacity_report.dcm

exit