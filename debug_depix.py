"""
Debug script to check what's happening during depixelization.
"""
from depixlib.LoadedImage import LoadedImage
from depixlib.Rectangle import Rectangle
from depixlib.functions import (
    findSameColorSubRectangles,
    removeMootColorRectangles,
    findRectangleSizeOccurences
)
from depixlib.functions_numpy import findRectangleMatches
from PIL import Image
import numpy as np

def debug_depix(pixelated_path, search_path):
    """Debug the depixelization process."""
    
    print("=" * 60)
    print("DEPIX DEBUG")
    print("=" * 60)
    
    # Load images
    print("\n1. Loading images...")
    pixelated = LoadedImage(pixelated_path)
    search = LoadedImage(search_path)
    print(f"   Pixelated: {pixelated.width}x{pixelated.height}")
    print(f"   Search: {search.width}x{search.height}")
    
    # Check first few pixels
    print("\n2. Sample pixels from pixelated image:")
    for x in range(min(5, pixelated.width)):
        for y in range(min(3, pixelated.height)):
            print(f"   [{x},{y}] = {pixelated.imageData[x][y]}")
    
    # Find rectangles
    print("\n3. Finding color rectangles...")
    rect = Rectangle((0, 0), (pixelated.width - 1, pixelated.height - 1))
    blocks = findSameColorSubRectangles(pixelated, rect)
    print(f"   Found {len(blocks)} blocks")
    
    if blocks:
        print("\n4. Sample blocks:")
        for i, block in enumerate(blocks[:5]):
            print(f"   Block {i}: pos=({block.x},{block.y}) "
                  f"size={block.width}x{block.height} color={block.color}")
    
    # Remove moot colors
    print("\n5. Filtering moot colors...")
    blocks = removeMootColorRectangles(blocks, None)
    print(f"   {len(blocks)} blocks after filtering")
    
    # Count sizes
    print("\n6. Block sizes:")
    sizes = findRectangleSizeOccurences(blocks)
    for size, count in sorted(sizes.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   {size[0]}x{size[1]}: {count} blocks")
    
    # Try template matching on first block
    if blocks:
        print("\n7. Testing template matching on first block...")
        test_block = blocks[0]
        print(f"   Block: pos=({test_block.x},{test_block.y}) "
              f"size={test_block.width}x{test_block.height}")
        
        # Convert to numpy
        search_array = np.array(search.getCopyOfLoadedPILImage(), dtype=np.float32) / 255.0
        pixel_array = np.array(pixelated.getCopyOfLoadedPILImage(), dtype=np.float32) / 255.0
        
        if search_array.ndim == 3 and search_array.shape[2] == 4:
            search_array = search_array[:, :, :3]
        if pixel_array.ndim == 3 and pixel_array.shape[2] == 4:
            pixel_array = pixel_array[:, :, :3]
        
        print(f"   Search array shape: {search_array.shape}")
        print(f"   Pixel array shape: {pixel_array.shape}")
        
        # Extract block
        block_img = pixel_array[
            test_block.y:test_block.y + test_block.height,
            test_block.x:test_block.x + test_block.width
        ]
        print(f"   Block shape: {block_img.shape}")
        print(f"   Block color range: [{block_img.min():.3f}, {block_img.max():.3f}]")
        
        # Try matching
        import cv2
        if block_img.shape[0] > 0 and block_img.shape[1] > 0:
            try:
                result = cv2.matchTemplate(search_array, block_img, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                print(f"   Match found at: {min_loc}")
                print(f"   Match score: {min_val:.6f}")
            except Exception as e:
                print(f"   ERROR in matching: {e}")
    
    print("\n" + "=" * 60)
    print("Debug complete!")
    print("=" * 60)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python debug_depix.py <pixelated.png> <search.png>")
        sys.exit(1)
    
    debug_depix(sys.argv[1], sys.argv[2])
