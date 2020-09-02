#!/bin/bash

echo "<------------------ Start: Lung quantifiction  ------------------------------------>"
echo "Running lung quantification"
echo "Input image $1"
echo "Input mask $2"
echo "Output dir $3"


source /opt/miniconda3/etc/profile.d/conda.sh
conda activate /software/lung_report_venv


echo "<------------ Start: Quantifiction output ---------------------------->"
z=$(python /software/lung_report/main.py -i $1 -m $2 -o $3) 
echo "$z"
echo "<------------ End: Quantifiction output ------------------------------>"


echo "<------------ Start: Adding results to Nora -------------------------->"
a=$(/opt/nora/bin/node /opt/nora/src/node/nora.js -p ThoraxCTD -a "$3/quantification")
echo "Adding results to nora"
echo "$a"
echo "<------------ End: Adding reults to Nora ----------------------------->"
echo "<------------------ End: Lung quantifiction  ------------------------------------>"
