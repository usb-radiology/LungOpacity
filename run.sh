#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
MODEL_DIR=$DIR/thoraxctd/lung_mask/niftynet_model

INPUT_PATH=$DIR/data/thoraxct.nii
OUTPUT_PATH=$DIR/data/mask.nii.gz


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

data_dir=$(dirname $INPUT_PATH)
data_name=$(basename $INPUT_PATH)

out_dir=$(dirname $OUTPUT_PATH)
out_name=$(basename $OUTPUT_PATH)

docker run --gpus all \
    -v $DIR/:/apps/LungOpacity \
    -v $data_dir/:/data -v $out_dir/:/data_out \
    -ti lung_opacity bash -c "source /venv_niftynet/bin/activate; python3.5 /apps/LungOpacity/lung_mask/lungmask.py -i /data/$data_name -o /data_out/$out_name -model_dir /apps/LungOpacity/lung_mask/niftynet_model -conf /apps/LungOpacity/lung_mask/conf_3d.ini"

docker run --gpus all \
    -v $DIR/:/apps/LungOpacity \
    -v $data_dir/:/data -v $out_dir/:/data_out \
    -ti lung_opacity bash -c ". /venv_report/bin/activate;python3.6 /apps/LungOpacity/lung_report/main.py -i /data/$data_name -m /data_out/$out_name -o /data_out/"