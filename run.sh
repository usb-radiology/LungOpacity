#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

INPUT_PATH=$DIR/dicom
OUTPUT_PATH=$DIR/output


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

docker run --gpus all \
    -v $DIR/:/apps/LungOpacity \
    -v $INPUT_PATH/:/data -v $OUTPUT_PATH/:/data_out \
    -ti lungopacity_frontier bash -c "bash /apps/LungOpacity/run_LungOpacity.sh -i /data -o /data_out"