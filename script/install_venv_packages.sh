#!/bin/bash
# @Author: Ramiro Luiz Nunes
# @Date:   2024-05-12 10:23:52
# @Last Modified by:   Ramiro Luiz Nunes
# @Last Modified time: 2024-05-12 10:47:21


# Check if the virtual environment already exists
if [ ! -d "../venv" ]; then
    # Create virtual environment if it does not exist
    python3 -m venv ../venv
else
    echo "Using existing virtual environment."
fi

# Activate virtual environment
source ../venv/bin/activate

# Install Python packages
pip install -r ../versioning/requirements.txt

# Deactivate virtual environment
deactivate
