"""
Check if image is actually pixelated.
"""
from PIL import Image
import numpy as np

def check_pixelation(image_path):
    """Check if image appears to be pixelated."""
    img = Image.open(image_path)
    arr = np.array(img)
    
    print(f"Image: {image_path}")
    print(f"Size: {img.size}")
    print(f"Mode: {img.mode}")
    print(f"Array shape: {arr.shape}")
    
    # Check for same-color blocks
    print("\nChecking for pixelation patterns...")
    
    # Look at top-left 20x20 area
    if arr.shape[0] >= 20 and arr.shape[1] >= 20:
        sample = arr[0:20, 0:20]
        print(f"\nTop-left 20x20 sample:")
        print(f"Unique colors: {len(np.unique(sample.reshape(-1, sample.shape[2]), axis=0))}")
        
        # Check if adjacent pixels are often the same
        same_horizontal = 0
        same_vertical = 0
        total = 0
        
        for y in range(19):
            for x in range(19):
                if np.array_equal(sample[y, x], sample[y, x+1]):
                    same_horizontal += 1
                if np.array_equal(sample[y, x], sample[y+1, x]):
                    same_vertical += 1
                total += 1
        
        print(f"Adjacent same pixels (horizontal): {same_horizontal}/{total} ({same_horizontal/total*100:.1f}%)")
        print(f"Adjacent same pixels (vertical): {same_vertical}/{total} ({same_vertical/total*100:.1f}%)")
        
        if same_horizontal > total * 0.7 and same_vertical > total * 0.7:
            print("✓ Image appears to be PIXELATED")
        else:
            print("✗ Image does NOT appear to be pixelated")
    
    # Show first 10x10 pixels
    print("\nFirst 10x10 pixels (showing if all same color):")
    if arr.shape[0] >= 10 and arr.shape[1] >= 10:
        for y in range(min(10, arr.shape[0])):
            row = []
            for x in range(min(10, arr.shape[1])):
                if len(arr.shape) == 3:
                    pixel = tuple(arr[y, x, :3])
                else:
                    pixel = arr[y, x]
                row.append(pixel)
            # Check if all same in row
            if len(set(row)) == 1:
                print(f"Row {y}: ALL SAME - {row[0]}")
            else:
                print(f"Row {y}: {len(set(row))} different colors")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python check_image.py <image.png>")
        sys.exit(1)
    
    check_pixelation(sys.argv[1])
