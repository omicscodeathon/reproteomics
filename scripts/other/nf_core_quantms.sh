#!/bin/bash

# Bash script to run nf-core/quantms pipeline without a scheduler

set -euo pipefail  # This ensures that the script exits on errors and unset variables

# Set the paths
nextflow_path="/path/to/nextflow/"
workflow_path="/path/to/nf-core/quantms/workflow/"
output_dir="/path/to/output_directory/"
params_file="path/to/json/file/"

# Navigate to the workflow directory
cd "$workflow_path"

# Run the pipeline
"$nextflow_path" run main.nf \
    --outdir "$output_dir" \
    -profile singularity
    -params-file "$params_file"

# Add a sleep command to give some time before script exits
sleep 10

echo "Pipeline completed successfully"
