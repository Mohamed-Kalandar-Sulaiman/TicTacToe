#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Generate requirements.txt using pipreqs
pipreqs . --force

# Install all the required packages from requirements.txt
pip install -r requirements.txt

echo "Requirements have been generated and packages installed successfully."
