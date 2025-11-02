"""
Rectangle data structures for Depix.
"""
from __future__ import annotations
from typing import List, Tuple


class Rectangle:
    """Basic rectangle with position and dimensions."""
    
    def __init__(
        self,
        startCoordinates: Tuple[int, int],
        endCoordinates: Tuple[int, int]
    ) -> None:
        """
        Initialize a rectangle.
        
        Args:
            startCoordinates: (x, y) top-left corner
            endCoordinates: (x, y) bottom-right corner
        """
        self.startCoordinates = startCoordinates
        self.endCoordinates = endCoordinates
        self.x = startCoordinates[0]
        self.y = startCoordinates[1]
        self.width = endCoordinates[0] - self.x
        self.height = endCoordinates[1] - self.y
    
    def __repr__(self) -> str:
        return (f"Rectangle(start={self.startCoordinates}, "
                f"end={self.endCoordinates}, "
                f"w={self.width}, h={self.height})")
    
    @property
    def area(self) -> int:
        """Calculate rectangle area."""
        return self.width * self.height
    
    def contains_point(self, x: int, y: int) -> bool:
        """Check if point is inside rectangle."""
        return (self.x <= x < self.x + self.width and
                self.y <= y < self.y + self.height)


class ColorRectangle(Rectangle):
    """Rectangle with associated color."""
    
    def __init__(
        self,
        color: Tuple[int, int, int],
        startCoordinates: Tuple[int, int],
        endCoordinates: Tuple[int, int]
    ) -> None:
        """
        Initialize a colored rectangle.
        
        Args:
            color: RGB color tuple
            startCoordinates: (x, y) top-left corner
            endCoordinates: (x, y) bottom-right corner
        """
        super().__init__(startCoordinates, endCoordinates)
        self.color = color
    
    def __repr__(self) -> str:
        return (f"ColorRectangle(color={self.color}, "
                f"start={self.startCoordinates}, "
                f"end={self.endCoordinates}, "
                f"w={self.width}, h={self.height})")


class RectangleMatch:
    """Match information for a rectangle."""
    
    def __init__(self, x: int, y: int, data: List) -> None:
        """
        Initialize a rectangle match.
        
        Args:
            x: X coordinate in search image
            y: Y coordinate in search image
            data: Pixel data of the matched region
        """
        self.x = x
        self.y = y
        self.data = data
    
    def __repr__(self) -> str:
        return f"RectangleMatch(x={self.x}, y={self.y}, data_len={len(self.data)})"
