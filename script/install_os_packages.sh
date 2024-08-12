#!/bin/bash
# @Author: Ramiro Luiz Nunes
# @Date:   2024-05-12 09:54:28
# @Last Modified by:   Ramiro Luiz Nunes
# @Last Modified time: 2024-05-12 10:22:27


# Check if the script is running as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Identify the operating system
OS=$(lsb_release -is)

# Choose the appropriate action based on the operating system
case $OS in
    Ubuntu|Debian)
        # Use the correct path to the requirements file
        REQ_FILE="../versioning/os/requirements_${OS,,}.txt"
        echo "Installing packages from $REQ_FILE for $OS..."
        if [ -f "$REQ_FILE" ]; then
            cat "$REQ_FILE" | xargs sudo apt install -y --verbose-versions
        else
            echo "Requirements file $REQ_FILE not found."
            exit 1
        fi
        ;;
    Fedora)
        # Use the correct path to the requirements file
        REQ_FILE="../versioning/os/requirements_fedora.txt"
        echo "Installing packages from $REQ_FILE for Fedora..."
        if [ -f "$REQ_FILE" ]; then
            cat "$REQ_FILE" | xargs sudo dnf install -y
        else
            echo "Requirements file $REQ_FILE not found."
            exit 1
        fi
        ;;
    *)
        echo "Unsupported OS: $OS"
        exit 1
        ;;
esac
