# Depix Architecture

## Overview

Depix is a depixelization tool that recovers plaintext from pixelated screenshots using template matching and geometric analysis.

## Project Structure

```
depix/
├── depix.py                    # Main entry point
├── depixlib/                   # Core library
│   ├── __init__.py
│   ├── LoadedImage.py         # Image loading and caching
│   ├── Rectangle.py           # Rectangle data structures
│   ├── functions.py           # Core algorithm functions
│   ├── functions_numpy.py     # NumPy-accelerated matching
│   └── helpers.py             # Utility functions
├── tool_show_boxes.py         # Visualization tool
├── tool_gen_pixelated.py      # Test image generator
├── tests/                     # Unit tests
│   └── test_depix.py
├── images/                    # Sample images
│   ├── testimages/
│   └── searchimages/
└── docs/                      # Documentation
```

## Core Components

### 1. LoadedImage (depixlib/LoadedImage.py)

**Purpose**: Efficient image loading and pixel data caching.

**Key Features**:
- Loads images using PIL/Pillow
- Caches pixel data in 2D array `[x][y]` format
- Provides fast pixel access without repeated `getpixel()` calls
- Handles RGB/RGBA conversion automatically

**Usage**:
```python
image = LoadedImage("path/to/image.png")
pixel = image.imageData[x][y]  # (r, g, b)
copy = image.getCopyOfLoadedPILImage()
```

### 2. Rectangle Classes (depixlib/Rectangle.py)

**Rectangle**: Base class for rectangular regions
- Properties: `x`, `y`, `width`, `height`, `area`
- Methods: `contains_point(x, y)`

**ColorRectangle**: Rectangle with associated color
- Inherits from Rectangle
- Additional property: `color` (RGB tuple)

**RectangleMatch**: Match information for template matching
- Properties: `x`, `y`, `data`
- Stores matched region location and pixel data

### 3. Core Functions (depixlib/functions.py)

#### findSameColorSubRectangles()
Detects same-color rectangular blocks in pixelated image.

**Algorithm**:
1. Scan image left-to-right, top-to-bottom
2. For each unprocessed pixel, find maximum same-color rectangle
3. Expand horizontally first, then vertically
4. Store as ColorRectangle

**Time Complexity**: O(w × h) where w, h are image dimensions

#### removeMootColorRectangles()
Filters out common colors that don't contain information:
- Black (0, 0, 0)
- White (255, 255, 255)
- Optional: custom background color

#### findRectangleSizeOccurences()
Counts occurrences of each unique rectangle size.
Returns: `Dict[(width, height), count]`

#### splitSingleMatchAndMultipleMatches()
Separates rectangles into two groups:
- **Single matches**: All matches are identical (high confidence)
- **Multiple matches**: Different matches found (ambiguous)

#### writeFirstMatchToImage()
Copies pixels from first match directly to output.
Used for single-match (high confidence) blocks.

#### writeAverageMatchToImage()
Averages all possible matches for ambiguous blocks.
Used for multiple-match blocks.

### 4. NumPy Functions (depixlib/functions_numpy.py)

#### findRectangleMatches()
Performs template matching using OpenCV.

**Algorithm**:
1. Convert images to NumPy arrays (float32, normalized 0-1)
2. Apply gamma correction if needed (linear mode)
3. For each unique block size:
   - Extract block from pixelated image
   - Use `cv2.matchTemplate()` with `TM_SQDIFF_NORMED`
   - Find minimum (best match) location
   - Store match coordinates and data

**Optimization**:
- Processes blocks by size (avoids redundant template creation)
- Uses NumPy vectorization
- Progress logging every 50 blocks

**Time Complexity**: O(n × s × w × h)
- n = number of blocks
- s = search image size
- w, h = block dimensions

### 5. Helper Functions (depixlib/helpers.py)

Utility functions for:
- Argument validation (`check_file`, `check_color`)
- Color manipulation (`rgb_to_hex`, `hex_to_rgb`)
- Color comparison (`calculate_color_distance`, `are_colors_similar`)
- Path validation

## Algorithm Flow

```
┌─────────────────────────────────────────────────┐
│ 1. Load pixelated and search images             │
│    - LoadedImage caches pixel data              │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 2. Detect pixelated blocks                      │
│    - findSameColorSubRectangles()               │
│    - Returns list of ColorRectangle objects     │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 3. Filter moot colors                           │
│    - removeMootColorRectangles()                │
│    - Remove black, white, background            │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 4. Count block sizes                            │
│    - findRectangleSizeOccurences()              │
│    - Group by (width, height)                   │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 5. Find matches in search image                 │
│    - findRectangleMatches() [NumPy]             │
│    - Template matching for each block           │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 6. Drop empty matches                           │
│    - dropEmptyRectangleMatches()                │
│    - Remove blocks with no matches              │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 7. Split by match confidence                    │
│    - splitSingleMatchAndMultipleMatches()       │
│    - Single: unique match (certain)             │
│    - Multiple: ambiguous matches                │
└──────────────────┬──────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
┌────────▼────────┐  ┌───────▼────────┐
│ 8a. Write single│  │ 8b. Write avg  │
│     matches     │  │     matches    │
│ (high conf.)    │  │ (ambiguous)    │
└────────┬────────┘  └───────┬────────┘
         │                   │
         └─────────┬─────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│ 9. Save output image                            │
└─────────────────────────────────────────────────┘
```

## Averaging Methods

### Gamma-Corrected (Default)
Mimics most screenshot tools (Windows Snipping Tool, Greenshot).

**Algorithm**:
```
average_rgb = sum(rgb_values) / count
```

Works in gamma-encoded color space (0-255).

### Linear
Mimics GIMP and other professional tools.

**Algorithm**:
```
linear_values = (rgb / 255) ^ 2.2
average_linear = sum(linear_values) / count
srgb = (average_linear ^ (1/2.2)) * 255
```

Works in linear light space for physically accurate averaging.

## Performance Characteristics

### Time Complexity
- Block detection: O(w × h)
- Template matching: O(n × s)
  - n = number of blocks
  - s = search image pixels
- Total: O(w × h + n × s)

### Space Complexity
- Image cache: O(w × h) for RGB data
- Matches: O(n × b) where b = average block size
- Total: O(w × h + n × b)

### Optimization Strategies
1. **Pixel data caching**: Load once, access many times
2. **NumPy vectorization**: Fast array operations
3. **OpenCV template matching**: Hardware-accelerated
4. **Size grouping**: Process similar blocks together
5. **Early filtering**: Remove moot colors before matching

## Extension Points

### Custom Averaging Methods
Implement in `functions_numpy.py`:
```python
def findRectangleMatches(..., averageType):
    if averageType == "custom":
        # Apply custom transformation
        search_array = custom_transform(search_array)
        pixel_array = custom_transform(pixel_array)
```

### Advanced Matching
Replace `cv2.matchTemplate()` with:
- Multi-scale matching
- Rotation-invariant matching
- Feature-based matching
- Machine learning approaches

### Block Detection
Improve `findSameColorSubRectangles()` with:
- Sub-pixel boundary detection
- Fuzzy color matching
- Adaptive thresholds
- ML-based segmentation

## Testing Strategy

### Unit Tests
- Rectangle classes and operations
- Helper functions (color conversion, validation)
- Algorithm components in isolation

### Integration Tests
- Full depixelization pipeline
- Different image formats
- Edge cases (small images, large blocks)

### Performance Tests
- Large image processing
- Memory usage profiling
- Speed benchmarks

## Future Improvements

1. **HMM-based approach**: More sophisticated probabilistic matching
2. **Sub-pixel handling**: Better support for anti-aliased text
3. **GPU acceleration**: Use CUDA for template matching
4. **Parallel processing**: Multi-threaded block matching
5. **GUI interface**: User-friendly desktop application
6. **Batch processing**: Process multiple images
7. **Video support**: Frame-by-frame depixelization

## References

- Original article: https://www.spipm.nl/2030.html
- OpenCV Template Matching: https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html
- De Bruijn Sequences: https://en.wikipedia.org/wiki/De_Bruijn_sequence
