#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo Watermark Tool
====================

A command-line tool to add watermark with EXIF shooting time to photos.
"""

import argparse
import os
import sys
from PIL import Image
import piexif


def get_exif_datetime(image_path):
    """
    Extract shooting time from image EXIF data.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Date time string in format 'YYYY-MM-DD HH:MM:SS' or None if not found
    """
    try:
        exif_dict = piexif.load(image_path)
        
        # Try to get shooting time from EXIF
        if "Exif" in exif_dict:
            if piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
                return exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode("utf-8")
            elif piexif.ExifIFD.DateTimeDigitized in exif_dict["Exif"]:
                return exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized].decode("utf-8")
        
        if "0th" in exif_dict:
            if piexif.ImageIFD.DateTime in exif_dict["0th"]:
                return exif_dict["0th"][piexif.ImageIFD.DateTime].decode("utf-8")
                
        return None
    except Exception as e:
        print(f"Error reading EXIF data from {image_path}: {e}")
        return None


def parse_args():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Add watermark with EXIF shooting time to photos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  photo-watermark /path/to/image.jpg
  photo-watermark -s 36 -c red /path/to/photos/
  photo-watermark -p top-left -f "YYYY-MM-DD HH:mm:ss" /path/to/image.jpg
        """
    )
    
    parser.add_argument(
        "path",
        help="Image file or directory path"
    )
    
    parser.add_argument(
        "-s", "--size",
        type=int,
        default=24,
        help="Font size (default: 24)"
    )
    
    parser.add_argument(
        "-c", "--color",
        default="white",
        help="Font color (default: white)"
    )
    
    parser.add_argument(
        "-p", "--position",
        choices=[
            "top-left", "top-center", "top-right",
            "middle-left", "center", "middle-right",
            "bottom-left", "bottom-center", "bottom-right"
        ],
        default="bottom-right",
        help="Watermark position (default: bottom-right)"
    )
    
    parser.add_argument(
        "-f", "--format",
        default="%Y-%m-%d",
        help="Date format (default: %%Y-%%m-%%d)"
    )
    
    return parser.parse_args()


def main():
    """
    Main function to run the photo watermark tool.
    """
    args = parse_args()
    
    # Check if path exists
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist")
        sys.exit(1)
    
    # If it's a file
    if os.path.isfile(args.path):
        datetime_str = get_exif_datetime(args.path)
        if datetime_str:
            print(f"EXIF DateTime: {datetime_str}")
        else:
            print("No EXIF DateTime information found")
    # If it's a directory
    elif os.path.isdir(args.path):
        print(f"Processing directory: {args.path}")
        # For now, just list image files
        image_extensions = ('.jpg', '.jpeg', '.png', '.tiff', '.tif')
        for file in os.listdir(args.path):
            if file.lower().endswith(image_extensions):
                file_path = os.path.join(args.path, file)
                datetime_str = get_exif_datetime(file_path)
                if datetime_str:
                    print(f"{file}: {datetime_str}")
                else:
                    print(f"{file}: No EXIF DateTime information")
    else:
        print(f"Error: '{args.path}' is neither a file nor a directory")
        sys.exit(1)


if __name__ == "__main__":
    main()