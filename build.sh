#!/bin/bash

# Photo-Watermark Build Script
# This script installs dependencies and provides options to run the program

# Exit on any error
set -e

# Function to display usage information
usage() {
    echo "Photo-Watermark Build Script"
    echo "==========================="
    echo
    echo "Usage:"
    echo "  ./build.sh install     - Install dependencies"
    echo "  ./build.sh run         - Run the program with no arguments"
    echo "  ./build.sh run [args]  - Run the program with specific arguments"
    echo "  ./build.sh test        - Run tests"
    echo "  ./build.sh clean       - Clean output directories"
    echo
    echo "Examples:"
    echo "  ./build.sh install"
    echo "  ./build.sh run test_input/test_image_with_exif.jpg"
    echo "  ./build.sh run test_input"
    echo
}

# Function to install dependencies
install_deps() {
    echo "Installing dependencies..."
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
    elif command -v pip &> /dev/null; then
        pip install -r requirements.txt
    else
        echo "Error: Neither pip3 nor pip found. Please install Python pip first."
        exit 1
    fi
    echo "Dependencies installed successfully!"
}

# Function to run the program
run_program() {
    if [ $# -eq 0 ]; then
        echo "Running program with no arguments..."
        python3 photo_watermark.py
    else
        echo "Running program with arguments: $*"
        python3 photo_watermark.py "$@"
    fi
}

# Function to run tests
run_tests() {
    echo "Running tests..."
    python3 tests/test_photo_watermark.py
}

# Function to clean output directories
clean_output() {
    echo "Cleaning output directories..."
    # Find and remove all directories ending with _watermark
    find . -type d -name "*_watermark" -not -path "./.git/*" | while read dir; do
        if [ -d "$dir" ]; then
            echo "Removing directory: $dir"
            rm -rf "$dir"
        fi
    done
    echo "Clean completed!"
}

# Main script logic
case "$1" in
    install)
        install_deps
        ;;
    run)
        shift
        run_program "$@"
        ;;
    test)
        run_tests
        ;;
    clean)
        clean_output
        ;;
    *)
        usage
        ;;
esac