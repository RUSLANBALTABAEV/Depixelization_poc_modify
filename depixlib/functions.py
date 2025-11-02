"""
Core functions for Depix depixelization algorithm.
"""
from __future__ import annotations

import logging
from typing import List, Tuple, Dict
import numpy as np
from PIL import Image
from depixlib.LoadedImage import LoadedImage
from depixlib.Rectangle import ColorRectangle, Rectangle, RectangleMatch

logger = logging.getLogger(__name__)


def findSameColorSubRectangles(
    pixelatedImage: LoadedImage,
    rectangle: Rectangle
) -> List[ColorRectangle]:
    """
    Find all same-color sub-rectangles within the given rectangle.
    
    Args:
        pixelatedImage: The loaded pixelated image
        rectangle: The rectangle to search within
        
    Returns:
        List of ColorRectangle objects
    """
    rects = []
    x = rectangle.x
    max_x = rectangle.x + rectangle.width + 1
    max_y = rectangle.y + rectangle.height + 1

    while x < max_x:
        y = rectangle.y
        while y < max_y:
            start_color = pixelatedImage.imageData[x][y]
            
            # Find width of same-color block
            width = 1
            while (x + width < max_x and 
                   pixelatedImage.imageData[x + width][y] == start_color):
                width += 1
            
            # Find height of same-color block
            height = 1
            while y + height < max_y:
                if all(pixelatedImage.imageData[x + dx][y + height] == start_color 
                       for dx in range(width)):
                    height += 1
                else:
                    break
            
            rects.append(ColorRectangle(
                start_color,
                (x, y),
                (x + width, y + height)
            ))
            y += height
        x += width
    
    return rects


def removeMootColorRectangles(
    rects: List[ColorRectangle],
    editorBackgroundColor: Tuple[int, int, int] | None
) -> List[ColorRectangle]:
    """
    Remove rectangles with moot colors (black, white, background).
    
    Args:
        rects: List of color rectangles
        editorBackgroundColor: Optional background color to filter
        
    Returns:
        Filtered list of color rectangles
    """
    moot_colors = [(0, 0, 0), (255, 255, 255)]
    if editorBackgroundColor:
        moot_colors.append(editorBackgroundColor)
    
    filtered = [r for r in rects if r.color not in moot_colors]
    logger.debug("Removed %d moot color rectangles", len(rects) - len(filtered))
    return filtered


def findRectangleSizeOccurences(
    rects: List[ColorRectangle]
) -> Dict[Tuple[int, int], int]:
    """
    Count occurrences of each rectangle size.
    
    Args:
        rects: List of color rectangles
        
    Returns:
        Dictionary mapping (width, height) to occurrence count
    """
    sizes: Dict[Tuple[int, int], int] = {}
    for r in rects:
        size = (r.width, r.height)
        sizes[size] = sizes.get(size, 0) + 1
    return sizes


def dropEmptyRectangleMatches(
    rectangleMatches: Dict[Tuple[int, int], List[RectangleMatch]],
    pixelatedSubRectangles: List[ColorRectangle]
) -> List[ColorRectangle]:
    """
    Remove rectangles that have no matches.
    
    Args:
        rectangleMatches: Dictionary of matches
        pixelatedSubRectangles: List of rectangles
        
    Returns:
        Filtered list of rectangles with matches
    """
    filtered = [
        r for r in pixelatedSubRectangles
        if (r.x, r.y) in rectangleMatches 
        and len(rectangleMatches[(r.x, r.y)]) > 0
    ]
    logger.debug(
        "Dropped %d rectangles with no matches",
        len(pixelatedSubRectangles) - len(filtered)
    )
    return filtered


def splitSingleMatchAndMultipleMatches(
    pixelatedSubRectangles: List[ColorRectangle],
    rectangleMatches: Dict[Tuple[int, int], List[RectangleMatch]]
) -> Tuple[List[ColorRectangle], List[ColorRectangle]]:
    """
    Split rectangles into single-match and multiple-match groups.
    
    Args:
        pixelatedSubRectangles: List of rectangles
        rectangleMatches: Dictionary of matches
        
    Returns:
        Tuple of (single_results, multi_results)
    """
    single_results = []
    multi_results = []

    for r in pixelatedSubRectangles:
        matches = rectangleMatches[(r.x, r.y)]
        
        if len(matches) == 1:
            single_results.append(r)
            continue
        
        # Check if all matches are identical
        first_data = np.array(matches[0].data)
        is_single = True
        
        for m in matches[1:]:
            if not np.array_equal(first_data, np.array(m.data)):
                is_single = False
                break
        
        if is_single:
            single_results.append(r)
        else:
            multi_results.append(r)
    
    logger.debug(
        "Split: %d single matches, %d multiple matches",
        len(single_results),
        len(multi_results)
    )
    return single_results, multi_results


def writeFirstMatchToImage(
    singleMatchRectangles: List[ColorRectangle],
    rectangleMatches: Dict[Tuple[int, int], List[RectangleMatch]],
    searchImage: LoadedImage,
    unpixelatedOutputImage: Image.Image
) -> None:
    """
    Write first match for each single-match rectangle to output image.
    
    Args:
        singleMatchRectangles: List of rectangles with single matches
        rectangleMatches: Dictionary of matches
        searchImage: The search image
        unpixelatedOutputImage: Output image to write to
    """
    for r in singleMatchRectangles:
        matches = rectangleMatches.get((r.x, r.y), [])
        
        if not matches:
            continue
            
        match = matches[0]
        
        # Use match data (already extracted and flattened)
        idx = 0
        for dy in range(r.height):
            for dx in range(r.width):
                if idx < len(match.data):
                    color = match.data[idx]
                    unpixelatedOutputImage.putpixel((r.x + dx, r.y + dy), color)
                idx += 1


def writeAverageMatchToImage(
    pixelatedSubRectangles: List[ColorRectangle],
    rectangleMatches: Dict[Tuple[int, int], List[RectangleMatch]],
    searchImage: LoadedImage,
    unpixelatedOutputImage: Image.Image
) -> None:
    """
    Write averaged matches for multiple-match rectangles to output image.
    
    Args:
        pixelatedSubRectangles: List of rectangles with multiple matches
        rectangleMatches: Dictionary of matches
        searchImage: The search image
        unpixelatedOutputImage: Output image to write to
    """
    for r in pixelatedSubRectangles:
        matches = rectangleMatches.get((r.x, r.y), [])
        
        if not matches:
            continue
        
        # Initialize accumulator
        accumulator = np.zeros((r.height, r.width, 3), dtype=np.float32)
        
        # Average all matches
        for match in matches:
            idx = 0
            for dy in range(r.height):
                for dx in range(r.width):
                    if idx < len(match.data):
                        pixel = match.data[idx]
                        accumulator[dy, dx] += np.array(pixel, dtype=np.float32)
                    idx += 1
        
        # Divide by number of matches
        accumulator = accumulator / len(matches)
        
        # Write to output image
        for dy in range(r.height):
            for dx in range(r.width):
                color = tuple(int(c) for c in accumulator[dy, dx])
                unpixelatedOutputImage.putpixel((r.x + dx, r.y + dy), color)
