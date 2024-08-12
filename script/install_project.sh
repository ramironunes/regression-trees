#!/bin/bash
# @Author: Ramiro Luiz Nunes
# @Date:   2024-05-12 10:15:55
# @Last Modified by:   Ramiro Luiz Nunes
# @Last Modified time: 2024-05-12 10:54:49


# Define some ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'       # Blue color
MAGENTA='\033[0;35m'    # Magenta color for purple
CYAN='\033[0;36m'       # Cyan can be used for a lighter blue
ORANGE='\033[0;33m'     # Orange, similar to dark yellow
NC='\033[0m' # No Color

# Print a colorful header
echo -e "${GREEN}========================================================${NC}"
echo -e "${CYAN}          Installing Regression Trees Project          ${NC}"
echo -e "${GREEN}========================================================${NC}"

# Check if already in the script directory, if not, navigate to it
if [[ $(basename "$PWD") != "script" ]]; then
    cd script
fi

# Grant execute permissions to the scripts
echo "Granting execute permissions to scripts..."
chmod +x install_os_packages.sh
chmod +x install_venv_packages.sh

# Install OS-specific packages
echo "Installing OS-specific packages..."
./install_os_packages.sh

# Setup virtual environment and install Python requirements
echo "Setting up virtual environment and installing Python requirements..."
./install_venv_packages.sh

# Navigate back to the project root only if needed
if [[ $(basename "$PWD") == "script" ]]; then
    cd ..
fi
