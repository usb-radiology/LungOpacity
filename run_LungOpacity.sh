#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
MODEL_DIR=$DIR/thoraxctd/lung_mask/niftynet_model

while [[ $# -gt 0 ]]
do
  key="$1"

  case $key in

    -i)
    INPUT_PATH="$2"
    shift # past argument
    shift # past value
    ;;
    -o)
    OUTPUT_PATH="$2"
    shift # past argument
    shift # past value
    ;;
     *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done


if [ ! -d $OUTPUT_PATH ]
then
    mkdir $OUTPUT_PATH
fi

if [ ! -d $OUTPUT_PATH/nii ]
then
    mkdir $OUTPUT_PATH/nii
fi

dcmfile=$(ls -t $INPUT_PATH/*.dcm | head -n 1)

dcm2niix -m y -o $OUTPUT_PATH/nii $INPUT_PATH

for file in $OUTPUT_PATH/nii/*.nii; do
    source /venv_niftynet/bin/activate

    python3.5 /apps/LungOpacity/lung_mask/lungmask.py -i $file -o $OUTPUT_PATH/nii/mask.nii.gz -model_dir /apps/niftynet_model -conf /apps/LungOpacity/lung_mask/conf_3d.ini

    deactivate 

    source /venv_report/bin/activate;python3.6 /apps/LungOpacity/lung_report/main.py -i $file -m $OUTPUT_PATH/nii/mask.nii.gz -o $OUTPUT_PATH/nii
    
    img2dcm -stf $dcmfile $OUTPUT_PATH/nii/report.jpg $OUTPUT_PATH/lungopacity_report.dcm


    break 1



done 
