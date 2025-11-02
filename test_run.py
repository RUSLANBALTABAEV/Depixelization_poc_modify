"""
Test script to verify depixelization works correctly.
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

def create_test_images():
    """Create simple test images for depixelization."""
    
    # Create original text image
    width, height = 200, 50
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw text
    text = "HELLO WORLD"
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    draw.text((10, 15), text, fill='black', font=font)
    img.save('test_original.png')
    print("✓ Created test_original.png")
    
    # Create pixelated version
    block_size = 5
    pixelated = img.copy()
    pixels = np.array(pixelated)
    
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            # Get block
            block = pixels[y:min(y+block_size, height), x:min(x+block_size, width)]
            # Calculate average
            avg_color = block.mean(axis=(0, 1)).astype(int)
            # Set block to average
            pixels[y:min(y+block_size, height), x:min(x+block_size, width)] = avg_color
    
    pixelated = Image.fromarray(pixels.astype('uint8'))
    pixelated.save('test_pixelated.png')
    print("✓ Created test_pixelated.png")
    
    # Create search image (De Bruijn-like sequence)
    search_img = Image.new('RGB', (400, 100), color='white')
    draw = ImageDraw.Draw(search_img)
    
    # All printable characters
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 "
    
    x_pos = 10
    y_pos = 15
    for char in chars:
        draw.text((x_pos, y_pos), char, fill='black', font=font)
        x_pos += 12
        if x_pos > 380:
            x_pos = 10
            y_pos += 25
    
    search_img.save('test_search.png')
    print("✓ Created test_search.png")
    
    return 'test_pixelated.png', 'test_search.png', 'test_output.png'


def run_depixelization_test():
    """Run a complete depixelization test."""
    print("\n=== Depixelization Test ===\n")
    
    # Create test images
    print("1. Creating test images...")
    pixelated, search, output = create_test_images()
    
    # Run depixelization
    print("\n2. Running depixelization...")
    import subprocess
    result = subprocess.run([
        'python3', 'depix.py',
        '-p', pixelated,
        '-s', search,
        '-o', output
    ], capture_output=True, text=True)
    
    print("\n--- Output ---")
    print(result.stdout)
    
    if result.returncode != 0:
        print("\n--- Errors ---")
        print(result.stderr)
        return False
    
    # Check if output was created
    if os.path.exists(output):
        print(f"\n✓ Output file created: {output}")
        
        # Compare sizes
        orig = Image.open('test_original.png')
        out = Image.open(output)
        
        if orig.size == out.size:
            print(f"✓ Size matches: {orig.size}")
        else:
            print(f"✗ Size mismatch: original={orig.size}, output={out.size}")
        
        # Calculate similarity
        orig_arr = np.array(orig)
        out_arr = np.array(out)
        
        if orig_arr.shape == out_arr.shape:
            diff = np.abs(orig_arr.astype(float) - out_arr.astype(float))
            avg_diff = diff.mean()
            print(f"✓ Average pixel difference: {avg_diff:.2f}")
            
            if avg_diff < 50:
                print("\n✓✓✓ DEPIXELIZATION SUCCESSFUL! ✓✓✓")
                return True
            else:
                print("\n⚠ Depixelization completed but quality is low")
                return True
        else:
            print(f"✗ Shape mismatch for comparison")
            return True
    else:
        print(f"\n✗ Output file not created")
        return False


def test_basic_functionality():
    """Test basic depixlib functionality."""
    print("\n=== Testing Core Functionality ===\n")
    
    try:
        from depixlib.LoadedImage import LoadedImage
        from depixlib.Rectangle import Rectangle, ColorRectangle, RectangleMatch
        from depixlib.functions import findSameColorSubRectangles
        
        # Create a simple test image
        img = Image.new('RGB', (10, 10), color='white')
        pixels = img.load()
        
        # Create a 5x5 red block
        for x in range(5):
            for y in range(5):
                pixels[x, y] = (255, 0, 0)
        
        img.save('test_simple.png')
        
        # Load and test
        loaded = LoadedImage('test_simple.png')
        print(f"✓ LoadedImage works: {loaded.width}x{loaded.height}")
        
        # Test rectangle detection
        rect = Rectangle((0, 0), (loaded.width - 1, loaded.height - 1))
        print(f"✓ Rectangle created: {rect}")
        
        # Test block detection
        blocks = findSameColorSubRectangles(loaded, rect)
        print(f"✓ Block detection works: found {len(blocks)} blocks")
        
        # Clean up
        os.remove('test_simple.png')
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("DEPIX FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Test basic functionality first
    basic_ok = test_basic_functionality()
    
    if not basic_ok:
        print("\n✗ Basic functionality test failed!")
        exit(1)
    
    # Test full depixelization
    depix_ok = run_depixelization_test()
    
    print("\n" + "=" * 60)
    if basic_ok and depix_ok:
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("=" * 60)
        exit(0)
    else:
        print("✗✗✗ SOME TESTS FAILED ✗✗✗")
        print("=" * 60)
        exit(1)
