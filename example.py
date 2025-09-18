#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example usage of Photo Watermark Tool
"""

import os
import sys
from PIL import Image
import piexif
from datetime import datetime

# Add the project root to the path so we can import photo_watermark
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_sample_image_with_exif():
    """Create a sample image with EXIF data for testing."""
    # Create a sample image
    img = Image.new('RGB', (800, 600), color='blue')
    
    # Create EXIF data with datetime
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: "Test Camera",
            piexif.ImageIFD.Model: "Test Model",
            piexif.ImageIFD.DateTime: "2023:05:20 15:30:45"
        },
        "Exif": {
            piexif.ExifIFD.DateTimeOriginal: "2023:05:20 15:30:45",
            piexif.ExifIFD.DateTimeDigitized: "2023:05:20 15:30:45"
        }
    }
    
    # Convert EXIF data to bytes
    exif_bytes = piexif.dump(exif_dict)
    
    # Save image with EXIF data
    img.save("sample.jpg", exif=exif_bytes)
    print("Sample image with EXIF data created: sample.jpg")

if __name__ == "__main__":
    create_sample_image_with_exif()