#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for Photo Watermark Tool
"""

import os
import sys
import unittest
from PIL import Image
import tempfile
import shutil
import piexif

# Add the project root to the path so we can import photo_watermark
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import photo_watermark


class TestPhotoWatermark(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.test_image_path = os.path.join(self.test_dir, "test.jpg")
        
        # Create a test image
        img = Image.new('RGB', (800, 600), color='red')
        img.save(self.test_image_path)
        
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)
        
    def test_format_datetime(self):
        """Test datetime formatting function."""
        # Test normal case
        datetime_str = "2023:01:15 14:30:25"
        format_str = "%Y-%m-%d"
        result = photo_watermark.format_datetime(datetime_str, format_str)
        self.assertEqual(result, "2023-01-15")
        
        # Test with time included
        format_str = "%Y-%m-%d %H:%M:%S"
        result = photo_watermark.format_datetime(datetime_str, format_str)
        self.assertEqual(result, "2023-01-15 14:30:25")
        
        # Test with invalid datetime string
        invalid_datetime = "Invalid Date"
        result = photo_watermark.format_datetime(invalid_datetime, format_str)
        self.assertEqual(result, invalid_datetime)
        
        # Test with None
        result = photo_watermark.format_datetime(None, format_str)
        self.assertIsNone(result)
        
    def test_get_text_position(self):
        """Test text position calculation."""
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
            
    def test_get_text_position_default(self):
        """Test default position when invalid position is given."""
        image_size = (800, 600)
        text_size = (100, 20)
        
        # Test with invalid position (should default to bottom-right)
        result = photo_watermark.get_text_position(image_size, text_size, "invalid-position")
        expected = photo_watermark.get_text_position(image_size, text_size, "bottom-right")
        self.assertEqual(result, expected)
        
    def test_add_watermark_to_image(self):
        """Test adding watermark to an image."""
        output_path = os.path.join(self.test_dir, "output.jpg")
        
        # Add watermark to image
        photo_watermark.add_watermark_to_image(
            image_path=self.test_image_path,
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
            
    def test_get_exif_datetime_no_exif(self):
        """Test EXIF datetime extraction when no EXIF data is present."""
        result = photo_watermark.get_exif_datetime(self.test_image_path)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()