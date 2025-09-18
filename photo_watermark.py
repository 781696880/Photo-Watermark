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
from PIL import Image, ImageDraw, ImageFont
import piexif
from datetime import datetime


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


def format_datetime(datetime_str, format_str):
    """
    Format datetime string according to specified format.
    
    Args:
        datetime_str (str): Original datetime string from EXIF
        format_str (str): Target format string
        
    Returns:
        str: Formatted datetime string or original if parsing fails
    """
    if not datetime_str:
        return datetime_str
    
    try:
        # Parse the EXIF datetime string (typically in format "YYYY:MM:DD HH:MM:SS")
        dt = datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S")
        return dt.strftime(format_str)
    except ValueError:
        # If parsing fails, return the original string
        return datetime_str


def get_text_position(image_size, text_size, position):
    """
    Calculate the position to place text watermark based on image size and desired position.
    
    Args:
        image_size (tuple): Width and height of the image
        text_size (tuple): Width and height of the text
        position (str): Position keyword
        
    Returns:
        tuple: x, y coordinates for the text
    """
    img_width, img_height = image_size
    text_width, text_height = text_size
    
    # Define margins (5% of image dimensions)
    margin_x = img_width * 0.05
    margin_y = img_height * 0.05
    
    # Calculate positions based on keywords
    positions = {
        "top-left": (margin_x, margin_y),
        "top-center": (img_width/2 - text_width/2, margin_y),
        "top-right": (img_width - text_width - margin_x, margin_y),
        "middle-left": (margin_x, img_height/2 - text_height/2),
        "center": (img_width/2 - text_width/2, img_height/2 - text_height/2),
        "middle-right": (img_width - text_width - margin_x, img_height/2 - text_height/2),
        "bottom-left": (margin_x, img_height - text_height - margin_y),
        "bottom-center": (img_width/2 - text_width/2, img_height - text_height - margin_y),
        "bottom-right": (img_width - text_width - margin_x, img_height - text_height - margin_y)
    }
    
    return positions.get(position, positions["bottom-right"])  # Default to bottom-right


def add_watermark_to_image(image_path, watermark_text, font_size, font_color, position, output_path):
    """
    Add watermark text to an image and save it to output path.
    
    Args:
        image_path (str): Path to the input image
        watermark_text (str): Text to use as watermark
        font_size (int): Font size for the watermark
        font_color (str): Color of the watermark text
        position (str): Position of the watermark
        output_path (str): Path to save the watermarked image
    """
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Create a drawing context
        draw = ImageDraw.Draw(image)
        
        # Try to use a better font, fallback to default if not available
        try:
            # Try to use a TrueType font
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Get text dimensions
        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Get text position
        text_position = get_text_position(image.size, (text_width, text_height), position)
        
        # Add the watermark text to the image
        draw.text(text_position, watermark_text, font=font, fill=font_color)
        
        # Save the watermarked image
        image.save(output_path)
        print(f"Watermarked image saved to: {output_path}")
        
    except Exception as e:
        print(f"Error adding watermark to {image_path}: {e}")


def process_single_image(image_path, font_size, font_color, position, date_format, output_dir):
    """
    Process a single image file - add watermark and save to output directory.
    
    Args:
        image_path (str): Path to the input image
        font_size (int): Font size for the watermark
        font_color (str): Color of the watermark text
        position (str): Position of the watermark
        date_format (str): Date format string
        output_dir (str): Directory to save the watermarked image
    """
    # Get EXIF datetime
    datetime_str = get_exif_datetime(image_path)
    if not datetime_str:
        print(f"Skipping {image_path}: No EXIF DateTime information found")
        return
    
    # Format datetime according to user preference
    formatted_datetime = format_datetime(datetime_str, date_format)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output file path
    filename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, filename)
    
    # Add watermark to image
    add_watermark_to_image(image_path, formatted_datetime, font_size, font_color, position, output_path)


def process_directory(directory_path, font_size, font_color, position, date_format):
    """
    Process all images in a directory.
    
    Args:
        directory_path (str): Path to the directory containing images
        font_size (int): Font size for the watermark
        font_color (str): Color of the watermark text
        position (str): Position of the watermark
        date_format (str): Date format string
    """
    # Create watermark directory
    dir_name = os.path.basename(os.path.normpath(directory_path))
    output_dir = os.path.join(directory_path, f"{dir_name}_watermark")
    
    # Process each image file
    image_extensions = ('.jpg', '.jpeg', '.png', '.tiff', '.tif')
    for file in os.listdir(directory_path):
        if file.lower().endswith(image_extensions):
            file_path = os.path.join(directory_path, file)
            process_single_image(file_path, font_size, font_color, position, date_format, output_dir)


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
        dest="date_format",
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
        # Generate output directory
        file_dir = os.path.dirname(args.path)
        dir_name = os.path.basename(file_dir) if file_dir else "watermark_output"
        output_dir = os.path.join(file_dir, f"{dir_name}_watermark")
        
        # Process the single image
        process_single_image(args.path, args.size, args.color, args.position, args.date_format, output_dir)
    # If it's a directory
    elif os.path.isdir(args.path):
        # Process all images in the directory
        process_directory(args.path, args.size, args.color, args.position, args.date_format)
    else:
        print(f"Error: '{args.path}' is neither a file nor a directory")
        sys.exit(1)


if __name__ == "__main__":
    main()