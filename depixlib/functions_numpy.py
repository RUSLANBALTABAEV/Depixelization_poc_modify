"""
NumPy-accelerated functions for fast template matching.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Tuple
import numpy as np
import cv2

from depixlib.LoadedImage import LoadedImage
from depixlib.Rectangle import ColorRectangle, RectangleMatch

logger = logging.getLogger(__name__)


def findRectangleMatches(
    rectangleSizeOccurrences: Dict[Tuple[int, int], int],
    pixelatedSubRectangles: List[ColorRectangle],
    searchImage: LoadedImage,
    pixelatedImage: LoadedImage,
    averageType: str
) -> Dict[Tuple[int, int], List[RectangleMatch]]:
    """
    Find matching rectangles using NumPy-accelerated template matching.
    
    Args:
        rectangleSizeOccurrences: Dictionary of rectangle sizes
        pixelatedSubRectangles: List of pixelated rectangles
        searchImage: Image to search for matches
        pixelatedImage: Pixelated input image
        averageType: Type of averaging ('gammacorrected' or 'linear')
        
    Returns:
        Dictionary mapping (x, y) coordinates to list of matches
    """
    logger.info("Using NumPy-accelerated template matching")
    
    # Convert images to numpy arrays
    search_array = np.array(
        searchImage.getCopyOfLoadedPILImage(),
        dtype=np.float32
    ) / 255.0
    
    pixel_array = np.array(
        pixelatedImage.getCopyOfLoadedPILImage(),
        dtype=np.float32
    ) / 255.0
    
    # Handle alpha channel if present
    if search_array.ndim == 3 and search_array.shape[2] == 4:
        search_array = search_array[:, :, :3]
    if pixel_array.ndim == 3 and pixel_array.shape[2] == 4:
        pixel_array = pixel_array[:, :, :3]
    
    # Apply gamma correction for linear averaging
    if averageType == "linear":
        search_array = np.power(search_array, 2.2)
        pixel_array = np.power(pixel_array, 2.2)
    
    matches: Dict[Tuple[int, int], List[RectangleMatch]] = {}
    total_blocks = len(pixelatedSubRectangles)
    processed = 0
    
    # Process each unique size
    for (w, h), count in rectangleSizeOccurrences.items():
        logger.debug("Processing block size: %dx%d (%d occurrences)", w, h, count)
        
        # Find all rectangles with this size
        matching_rects = [
            r for r in pixelatedSubRectangles
            if r.width == w and r.height == h
        ]
        
        for r in matching_rects:
            processed += 1
            
            try:
                # Extract block from pixelated image
                block = pixel_array[r.y:r.y + h, r.x:r.x + w]
                
                # Ensure block has correct dimensions
                if block.shape[0] != h or block.shape[1] != w:
                    logger.warning(
                        "Block at (%d, %d) has incorrect dimensions: expected %dx%d, got %s",
                        r.x, r.y, h, w, block.shape
                    )
                    continue
                
                # Ensure 3D array even for grayscale
                if block.ndim == 2:
                    block = np.stack([block, block, block], axis=-1)
                
                # Perform template matching
                result = cv2.matchTemplate(
                    search_array,
                    block,
                    cv2.TM_SQDIFF_NORMED
                )
                
                # Find best match(es)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                
                # Extract matched region data from search image
                match_x, match_y = min_loc
                
                # Flatten matched data to list (row by row, then column)
                matched_data = []
                for dy in range(h):
                    for dx in range(w):
                        if match_x + dx < searchImage.width and match_y + dy < searchImage.height:
                            matched_data.append(searchImage.imageData[match_x + dx][match_y + dy])
                        else:
                            # Pad with black if out of bounds
                            matched_data.append((0, 0, 0))
                
                # Create match object
                match = RectangleMatch(
                    match_x,
                    match_y,
                    matched_data
                )
                
                matches[(r.x, r.y)] = [match]
                
            except Exception as e:
                logger.error(
                    "Error processing block at (%d, %d): %s",
                    r.x, r.y, str(e)
                )
                continue
            
            # Progress logging
            if processed % 50 == 0 or processed == total_blocks:
                logger.info(
                    "Progress: %d/%d blocks processed (%.1f%%)",
                    processed,
                    total_blocks,
                    (processed / total_blocks) * 100
                )
    
    logger.info("Found %d matches for %d blocks", len(matches), total_blocks)
    return matches
