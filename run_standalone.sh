#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


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

mkdir -p $OUTPUT_PATH
docker run --gpus all \
    -v $INPUT_PATH/:/docker/shs/in -v $OUTPUT_PATH/:/docker/shs/out \
    -ti lungopacity_frontier

