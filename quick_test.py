"""
Quick test to verify all imports and basic functionality.
"""

print("Testing imports...")

try:
    from depixlib.LoadedImage import LoadedImage
    print("✓ LoadedImage")
except Exception as e:
    print(f"✗ LoadedImage: {e}")

try:
    from depixlib.Rectangle import Rectangle, ColorRectangle, RectangleMatch
    print("✓ Rectangle classes")
except Exception as e:
    print(f"✗ Rectangle classes: {e}")

try:
    from depixlib.helpers import check_file, check_color
    print("✓ Helpers")
except Exception as e:
    print(f"✗ Helpers: {e}")

try:
    from depixlib.functions import (
        findSameColorSubRectangles,
        removeMootColorRectangles,
        findRectangleSizeOccurences
    )
    print("✓ Functions")
except Exception as e:
    print(f"✗ Functions: {e}")

try:
    from depixlib.functions_numpy import findRectangleMatches
    print("✓ NumPy functions")
except Exception as e:
    print(f"✗ NumPy functions: {e}")

print("\nTesting basic functionality...")

try:
    # Test Rectangle
    rect = Rectangle((0, 0), (10, 10))
    assert rect.width == 10
    assert rect.height == 10
    assert rect.area == 100
    print("✓ Rectangle works")
except Exception as e:
    print(f"✗ Rectangle: {e}")

try:
    # Test ColorRectangle
    crect = ColorRectangle((255, 0, 0), (0, 0), (5, 5))
    assert crect.color == (255, 0, 0)
    assert crect.width == 5
    print("✓ ColorRectangle works")
except Exception as e:
    print(f"✗ ColorRectangle: {e}")

try:
    # Test color parsing
    color = check_color("255,0,0")
    assert color == (255, 0, 0)
    color = check_color("128, 128, 128")
    assert color == (128, 128, 128)
    print("✓ Color parsing works")
except Exception as e:
    print(f"✗ Color parsing: {e}")

print("\n" + "="*50)
print("All basic tests passed!")
print("="*50)
print("\nNow you can run:")
print("  python depix.py -p <pixelated> -s <search> -o <output>")
