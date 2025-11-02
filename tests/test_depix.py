"""
Unit tests for Depix functionality.
"""
import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from depixlib.Rectangle import Rectangle, ColorRectangle, RectangleMatch
from depixlib.helpers import (
    check_color,
    calculate_color_distance,
    are_colors_similar,
    rgb_to_hex,
    hex_to_rgb
)


class TestRectangle(unittest.TestCase):
    """Test Rectangle class."""
    
    def test_rectangle_creation(self):
        """Test basic rectangle creation."""
        rect = Rectangle((0, 0), (10, 20))
        self.assertEqual(rect.x, 0)
        self.assertEqual(rect.y, 0)
        self.assertEqual(rect.width, 10)
        self.assertEqual(rect.height, 20)
    
    def test_rectangle_area(self):
        """Test area calculation."""
        rect = Rectangle((0, 0), (10, 20))
        self.assertEqual(rect.area, 200)
        
        rect2 = Rectangle((5, 5), (15, 25))
        self.assertEqual(rect2.area, 200)
    
    def test_contains_point(self):
        """Test point containment."""
        rect = Rectangle((10, 10), (20, 20))
        
        # Points inside
        self.assertTrue(rect.contains_point(10, 10))
        self.assertTrue(rect.contains_point(15, 15))
        self.assertTrue(rect.contains_point(19, 19))
        
        # Points outside
        self.assertFalse(rect.contains_point(9, 10))
        self.assertFalse(rect.contains_point(10, 9))
        self.assertFalse(rect.contains_point(20, 20))
        self.assertFalse(rect.contains_point(25, 25))


class TestColorRectangle(unittest.TestCase):
    """Test ColorRectangle class."""
    
    def test_color_rectangle_creation(self):
        """Test colored rectangle creation."""
        rect = ColorRectangle((255, 0, 0), (0, 0), (10, 10))
        self.assertEqual(rect.color, (255, 0, 0))
        self.assertEqual(rect.width, 10)
        self.assertEqual(rect.height, 10)
    
    def test_color_rectangle_inheritance(self):
        """Test that ColorRectangle inherits from Rectangle."""
        rect = ColorRectangle((0, 255, 0), (5, 5), (15, 15))
        self.assertEqual(rect.area, 100)
        self.assertTrue(rect.contains_point(10, 10))


class TestRectangleMatch(unittest.TestCase):
    """Test RectangleMatch class."""
    
    def test_match_creation(self):
        """Test match creation."""
        data = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        match = RectangleMatch(10, 20, data)
        self.assertEqual(match.x, 10)
        self.assertEqual(match.y, 20)
        self.assertEqual(len(match.data), 3)


class TestHelpers(unittest.TestCase):
    """Test helper functions."""
    
    def test_check_color_valid(self):
        """Test valid color parsing."""
        self.assertEqual(check_color("255,0,0"), (255, 0, 0))
        self.assertEqual(check_color("0,255,0"), (0, 255, 0))
        self.assertEqual(check_color("128, 128, 128"), (128, 128, 128))
        self.assertIsNone(check_color(None))
    
    def test_check_color_invalid(self):
        """Test invalid color parsing."""
        with self.assertRaises(Exception):
            check_color("255,0")
        
        with self.assertRaises(Exception):
            check_color("invalid")
        
        with self.assertRaises(Exception):
            check_color("256,0,0")  # Out of range
    
    def test_rgb_to_hex(self):
        """Test RGB to hex conversion."""
        self.assertEqual(rgb_to_hex((255, 0, 0)), "#ff0000")
        self.assertEqual(rgb_to_hex((0, 255, 0)), "#00ff00")
        self.assertEqual(rgb_to_hex((0, 0, 255)), "#0000ff")
        self.assertEqual(rgb_to_hex((128, 128, 128)), "#808080")
    
    def test_hex_to_rgb(self):
        """Test hex to RGB conversion."""
        self.assertEqual(hex_to_rgb("#ff0000"), (255, 0, 0))
        self.assertEqual(hex_to_rgb("00ff00"), (0, 255, 0))
        self.assertEqual(hex_to_rgb("#0000ff"), (0, 0, 255))
        self.assertEqual(hex_to_rgb("808080"), (128, 128, 128))
    
    def test_hex_to_rgb_invalid(self):
        """Test invalid hex conversion."""
        with self.assertRaises(ValueError):
            hex_to_rgb("invalid")
        
        with self.assertRaises(ValueError):
            hex_to_rgb("#ff")
    
    def test_calculate_color_distance(self):
        """Test color distance calculation."""
        # Same color
        dist = calculate_color_distance((255, 0, 0), (255, 0, 0))
        self.assertEqual(dist, 0.0)
        
        # Different colors
        dist = calculate_color_distance((255, 0, 0), (0, 0, 0))
        self.assertEqual(dist, 255.0)
        
        # Pythagoras
        dist = calculate_color_distance((0, 0, 0), (3, 4, 0))
        self.assertEqual(dist, 5.0)
    
    def test_are_colors_similar(self):
        """Test color similarity check."""
        # Identical colors
        self.assertTrue(are_colors_similar((255, 0, 0), (255, 0, 0)))
        
        # Similar colors
        self.assertTrue(are_colors_similar((255, 0, 0), (250, 0, 0), threshold=10))
        
        # Different colors
        self.assertFalse(are_colors_similar((255, 0, 0), (0, 0, 255), threshold=10))
        
        # Custom threshold
        self.assertTrue(are_colors_similar((100, 100, 100), (110, 110, 110), threshold=20))
        self.assertFalse(are_colors_similar((100, 100, 100), (150, 150, 150), threshold=20))


class TestFunctions(unittest.TestCase):
    """Test main depixelization functions."""
    
    def test_remove_moot_colors(self):
        """Test moot color filtering."""
        from depixlib.functions import removeMootColorRectangles
        
        rects = [
            ColorRectangle((0, 0, 0), (0, 0), (10, 10)),        # Black
            ColorRectangle((255, 255, 255), (10, 10), (20, 20)), # White
            ColorRectangle((128, 128, 128), (20, 20), (30, 30)), # Gray
            ColorRectangle((40, 41, 35), (30, 30), (40, 40))    # Background
        ]
        
        # Without background color
        filtered = removeMootColorRectangles(rects, None)
        self.assertEqual(len(filtered), 2)  # Only gray and background color
        
        # With background color
        filtered = removeMootColorRectangles(rects, (40, 41, 35))
        self.assertEqual(len(filtered), 1)  # Only gray
    
    def test_find_rectangle_size_occurrences(self):
        """Test rectangle size counting."""
        from depixlib.functions import findRectangleSizeOccurences
        
        rects = [
            ColorRectangle((255, 0, 0), (0, 0), (5, 5)),
            ColorRectangle((0, 255, 0), (5, 5), (10, 10)),
            ColorRectangle((0, 0, 255), (10, 10), (20, 20)),
            ColorRectangle((255, 255, 0), (20, 20), (25, 30))
        ]
        
        sizes = findRectangleSizeOccurences(rects)
        
        self.assertEqual(sizes[(5, 5)], 2)   # Two 5x5 rectangles
        self.assertEqual(sizes[(10, 10)], 1) # One 10x10 rectangle
        self.assertEqual(sizes[(5, 10)], 1)  # One 5x10 rectangle


if __name__ == '__main__':
    unittest.main()
