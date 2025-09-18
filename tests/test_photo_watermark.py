#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive tests for Photo Watermark Tool
"""

import os
import sys
import unittest
from PIL import Image
import tempfile
import shutil
import piexif

# Add the project root to the path so we can import photo_watermark
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import photo_watermark


class TestPhotoWatermarkComprehensive(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before running tests in the class."""
        # Create a temporary directory for testing
        cls.test_dir = tempfile.mkdtemp()
        
        # Create a test image without EXIF
        cls.test_image_no_exif = os.path.join(cls.test_dir, "test_no_exif.jpg")
        img = Image.new('RGB', (800, 600), color='red')
        img.save(cls.test_image_no_exif)
        
        # Create a test image with EXIF
        cls.test_image_with_exif = os.path.join(cls.test_dir, "test_with_exif.jpg")
        img = Image.new('RGB', (800, 600), color='blue')
        
        # Create EXIF data with datetime
        exif_dict = {
            "0th": {
                piexif.ImageIFD.DateTime: "2023:05:20 15:30:45"
            },
            "Exif": {
                piexif.ExifIFD.DateTimeOriginal: "2023:05:20 15:30:45",
            }
        }
        
        # Convert EXIF data to bytes and save
        exif_bytes = piexif.dump(exif_dict)
        img.save(cls.test_image_with_exif, exif=exif_bytes)
        
    @classmethod
    def tearDownClass(cls):
        """Tear down class fixtures after running all tests in the class."""
        # Remove the temporary directory after all tests
        shutil.rmtree(cls.test_dir)
        
    def test_get_exif_datetime_with_exif(self):
        """Test EXIF datetime extraction when EXIF data is present."""
        result = photo_watermark.get_exif_datetime(self.test_image_with_exif)
        self.assertEqual(result, "2023:05:20 15:30:45")
        
    def test_get_exif_datetime_no_exif(self):
        """Test EXIF datetime extraction when no EXIF data is present."""
        result = photo_watermark.get_exif_datetime(self.test_image_no_exif)
        self.assertIsNone(result)
        
    def test_format_datetime(self):
        """Test datetime formatting function."""
        # Test normal case
        datetime_str = "2023:01:15 14:30:25"
        format_str = "%Y-%m-%d"
        result = photo_watermark.format_datetime(datetime_str, format_str)
        self.assertEqual(result, "2023-01-15")
        
    def test_get_text_position_all_positions(self):
        """Test text position calculation for all positions."""
        image_size = (800, 600)
        text_size = (100, 20)
        
        # Test all positions
        positions = [
            "top-left", "top-center", "top-right",
            "middle-left", "center", "middle-right",
            "bottom-left", "bottom-center", "bottom-right"
        ]
        
        for position in positions:
            result = photo_watermark.get_text_position(image_size, text_size, position)
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            self.assertGreaterEqual(result[0], 0)
            self.assertGreaterEqual(result[1], 0)
            
    def test_add_watermark_to_image(self):
        """Test adding watermark to an image."""
        output_path = os.path.join(self.test_dir, "output_watermark.jpg")
        
        # Add watermark to image
        photo_watermark.add_watermark_to_image(
            image_path=self.test_image_no_exif,
            watermark_text="Test Watermark",
            font_size=24,
            font_color="white",
            position="bottom-right",
            output_path=output_path
        )
        
        # Check that output image was created
        self.assertTrue(os.path.exists(output_path))
        
        # Check that output image can be opened
        try:
            output_img = Image.open(output_path)
            self.assertIsNotNone(output_img)
            output_img.close()
        except Exception as e:
            self.fail(f"Output image could not be opened: {e}")

    def test_process_single_image_with_exif(self):
        """Test processing a single image that has EXIF data."""
        # Create output directory
        output_dir = os.path.join(self.test_dir, "single_output_watermark")
        
        # Process the image
        photo_watermark.process_single_image(
            image_path=self.test_image_with_exif,
            font_size=24,
            font_color="white",
            position="bottom-right",
            date_format="%Y-%m-%d",
            output_dir=output_dir
        )
        
        # Check that output directory was created
        self.assertTrue(os.path.exists(output_dir))
        
        # Check that output image was created
        output_image_path = os.path.join(output_dir, "test_with_exif.jpg")
        self.assertTrue(os.path.exists(output_image_path))
        
        # Check that output image can be opened
        try:
            output_img = Image.open(output_image_path)
            self.assertIsNotNone(output_img)
            output_img.close()
        except Exception as e:
            self.fail(f"Output image could not be opened: {e}")


if __name__ == "__main__":
    unittest.main()