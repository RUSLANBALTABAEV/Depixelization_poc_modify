# Depix Usage Examples

## Basic Examples

### 1. Simple Depixelization

Recover text from a pixelated Notepad screenshot:

```bash
python3 depix.py \
    -p images/testimages/testimage3_pixels.png \
    -s images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png \
    -o output.png
```

**Expected output:**
```
2024-10-28 10:30:00 - INFO - Loading pixelated image from images/testimages/testimage3_pixels.png
2024-10-28 10:30:00 - INFO - Loading search image from images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png
2024-10-28 10:30:01 - INFO - Finding color rectangles from pixelated space
2024-10-28 10:30:01 - INFO - Found 245 same color rectangles
2024-10-28 10:30:01 - INFO - 189 rectangles left after moot filter
2024-10-28 10:30:01 - INFO - Found 3 different rectangle sizes
2024-10-28 10:30:01 - INFO - Finding matches in search image
2024-10-28 10:30:02 - INFO - Found 189 matches for 189 blocks
2024-10-28 10:30:02 - INFO - [156 straight matches | 33 multiple matches]
2024-10-28 10:30:02 - INFO - Successfully saved output image to: output.png
```

### 2. Linear Averaging (GIMP-style)

For screenshots pixelated with GIMP or other tools using linear averaging:

```bash
python3 depix.py \
    -p images/testimages/sublime_screenshot_pixels_gimp.png \
    -s images/searchimages/debruin_sublime_Linux_small.png \
    --averagetype linear \
    -o output_linear.png
```

### 3. With Background Color Filter

Filter out editor background to improve results:

```bash
python3 depix.py \
    -p pixelated_sublime.png \
    -s search_sublime.png \
    --backgroundcolor 40,41,35 \
    --averagetype linear \
    -o output.png
```

**Common background colors:**
- Sublime Text Dark: `40,41,35`
- VS Code Dark: `30,30,30`
- Notepad White: `255,255,255`
- Terminal Black: `0,0,0`

## Advanced Examples

### 4. Processing Multiple Images

Create a batch script (`batch_depix.sh`):

```bash
#!/bin/bash

# Array of pixelated images
images=(
    "image1.png"
    "image2.png"
    "image3.png"
)

# Search image (same for all)
search="search_pattern.png"

# Process each image
for img in "${images[@]}"; do
    output="output_${img}"
    echo "Processing $img..."
    python3 depix.py -p "$img" -s "$search" -o "$output"
done

echo "Batch processing complete!"
```

Run with:
```bash
chmod +x batch_depix.sh
./batch_depix.sh
```

### 5. Creating Custom Search Images

#### Step 1: Generate De Bruijn Sequence

Python script to generate character sequence:

```python
def generate_debruijn(chars, n):
    """Generate De Bruijn sequence for given characters."""
    from itertools import product
    
    alphabet = chars
    k = len(alphabet)
    a = [0] * k * n
    sequence = []

    def db(t, p):
        if t > n:
            if n % p == 0:
                sequence.extend(a[1:p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)

    db(1, 1)
    return ''.join(alphabet[i] for i in sequence)

# Generate for alphanumeric
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
sequence = generate_debruijn(chars, 2)
print(sequence)
```

#### Step 2: Create Search Image

1. Open your text editor (Notepad, Sublime, etc.)
2. Set exact same font, size, and colors as original
3. Paste the De Bruijn sequence
4. Take screenshot
5. Save as search image

### 6. Visualizing Detection Quality

Before running depixelization, check if blocks are detected correctly:

```bash
python3 tool_show_boxes.py \
    -p pixelated.png \
    -s search.png \
    --enhance 5 \
    -o visualization.png
```

**Good detection:**
- Clean rectangular boxes
- All text blocks outlined
- Consistent box sizes

**Poor detection:**
- Fragmented boxes
- Many different sizes
- Overlapping boxes

**Solution for poor detection:** Re-crop the image more precisely.

### 7. Generating Test Images

Create pixelated test images with different block sizes:

```bash
# Small blocks (5x5)
python3 tool_gen_pixelated.py \
    -i original.png \
    -o pixelated_5x5.png \
    --blocksize 5

# Medium blocks (10x10)
python3 tool_gen_pixelated.py \
    -i original.png \
    -o pixelated_10x10.png \
    --blocksize 10

# Large blocks (20x20)
python3 tool_gen_pixelated.py \
    -i original.png \
    -o pixelated_20x20.png \
    --blocksize 20
```

Test different averaging methods:

```bash
# Gamma-corrected (default)
python3 tool_gen_pixelated.py \
    -i original.png \
    -o pixelated_gamma.png \
    --method gamma

# Linear (GIMP-style)
python3 tool_gen_pixelated.py \
    -i original.png \
    -o pixelated_linear.png \
    --method linear
```

## Real-World Scenarios

### Scenario 1: Password Recovery

**Problem:** Someone pixelated a password in a screenshot.

**Solution:**
1. Cut out the pixelated region exactly
2. Identify the text editor and font used
3. Create De Bruijn sequence with expected characters (letters, numbers, symbols)
4. Generate search image with same settings
5. Run depixelization

```bash
python3 depix.py \
    -p password_pixelated.png \
    -s search_password_chars.png \
    -o recovered_password.png
```

### Scenario 2: Code Snippet

**Problem:** Code snippet was pixelated in a presentation.

**Solution:**
1. Identify the code editor (VS Code, Sublime, etc.)
2. Match the theme and font settings
3. Create search image with code-relevant characters
4. Run with appropriate background color

```bash
python3 depix.py \
    -p code_pixelated.png \
    -s search_code.png \
    --backgroundcolor 30,30,30 \
    --averagetype linear \
    -o recovered_code.png
```

### Scenario 3: Terminal Output

**Problem:** Command output was pixelated in a tutorial.

**Solution:**
1. Identify terminal font (usually monospace)
2. Match background color
3. Create search image with shell commands and output

```bash
python3 depix.py \
    -p terminal_pixelated.png \
    -s search_terminal.png \
    --backgroundcolor 0,0,0 \
    -o recovered_terminal.png
```

## Troubleshooting Examples

### Issue 1: No Matches Found

```
2024-10-28 10:30:02 - INFO - Found 0 matches for 189 blocks
```

**Diagnosis:**
```bash
# Check what blocks were detected
python3 tool_show_boxes.py -p pixelated.png -s search.png
```

**Solutions:**
- Try opposite averaging method (`--averagetype linear` or `--averagetype gammacorrected`)
- Verify font settings match exactly
- Check if search image has all necessary characters
- Ensure no compression was applied after pixelation

### Issue 2: Too Many Block Size Variants

```
WARNING - Too many variants on block size (234 > 50). Re-cropping the image might help.
```

**Solution:**
```bash
# Visualize to see the problem
python3 tool_show_boxes.py -p pixelated.png -s search.png

# Carefully re-crop the pixelated region
# Only include the actual pixelated blocks
# Avoid including any non-pixelated borders
```

### Issue 3: Poor Quality Results

**Try different settings:**

```bash
# Test 1: Linear averaging
python3 depix.py -p image.png -s search.png --averagetype linear -o output1.png

# Test 2: With background filter
python3 depix.py -p image.png -s search.png --backgroundcolor 40,41,35 -o output2.png

# Test 3: Both
python3 depix.py -p image.png -s search.png --averagetype linear --backgroundcolor 40,41,35 -o output3.png

# Compare results
```

## Performance Examples

### Large Image Processing

For large images, monitor progress:

```bash
python3 depix.py \
    -p large_image.png \
    -s search.png \
    -o output.png 2>&1 | tee depix.log
```

Expected output shows progress:
```
2024-10-28 10:30:05 - INFO - Progress: 50/500 blocks processed (10.0%)
2024-10-28 10:30:10 - INFO - Progress: 100/500 blocks processed (20.0%)
2024-10-28 10:30:15 - INFO - Progress: 150/500 blocks processed (30.0%)
...
```

### Memory Optimization

For very large images, process in sections:

```python
# split_image.py
from PIL import Image

def split_image(path, rows, cols):
    img = Image.open(path)
    w, h = img.size
    tile_w = w // cols
    tile_h = h // rows
    
    for i in range(rows):
        for j in range(cols):
            box = (j*tile_w, i*tile_h, (j+1)*tile_w, (i+1)*tile_h)
            tile = img.crop(box)
            tile.save(f"tile_{i}_{j}.png")

split_image("huge_image.png", 2, 2)
```

Then process each tile separately.

## Integration Examples

### Python API Usage

```python
from depixlib.LoadedImage import LoadedImage
from depixlib.Rectangle import Rectangle
from depixlib.functions import *
from depixlib.functions_numpy import findRectangleMatches

# Load images
pixelated = LoadedImage("pixelated.png")
search = LoadedImage("search.png")

# Process
rect = Rectangle((0, 0), (pixelated.width-1, pixelated.height-1))
blocks = findSameColorSubRectangles(pixelated, rect)
blocks = removeMootColorRectangles(blocks, None)

sizes = findRectangleSizeOccurences(blocks)
matches = findRectangleMatches(sizes, blocks, search, pixelated, "gammacorrected")

# Get results
single, multi = splitSingleMatchAndMultipleMatches(blocks, matches)

# Write to output
output = pixelated.getCopyOfLoadedPILImage()
writeFirstMatchToImage(single, matches, search, output)
writeAverageMatchToImage(multi, matches, search, output)
output.save("output.png")

print(f"Success! {len(single)} certain matches, {len(multi)} ambiguous")
```

### Web Service Integration

```python
# web_depix.py
from flask import Flask, request, send_file
import tempfile
import os
from depix import main as depix_main

app = Flask(__name__)

@app.route('/depixelize', methods=['POST'])
def depixelize():
    # Get uploaded files
    pixelated = request.files['pixelated']
    search = request.files['search']
    
    # Save temporarily
    with tempfile.TemporaryDirectory() as tmpdir:
        pix_path = os.path.join(tmpdir, 'pixelated.png')
        search_path = os.path.join(tmpdir, 'search.png')
        output_path = os.path.join(tmpdir, 'output.png')
        
        pixelated.save(pix_path)
        search.save(search_path)
        
        # Run depixelization
        # (Would need to refactor depix.py to accept programmatic args)
        # For now, use subprocess
        import subprocess
        subprocess.run([
            'python3', 'depix.py',
            '-p', pix_path,
            '-s', search_path,
            '-o', output_path
        ])
        
        # Return result
        return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
```

### Command Line Wrapper

```python
# depix_wrapper.py
import subprocess
import sys
from pathlib import Path

def depix(pixelated, search, output=None, **kwargs):
    """
    Wrapper for depix command line tool.
    
    Args:
        pixelated: Path to pixelated image
        search: Path to search image
        output: Path to output image (default: output.png)
        **kwargs: Additional options (averagetype, backgroundcolor)
    
    Returns:
        Path to output file
    """
    cmd = ['python3', 'depix.py', '-p', str(pixelated), '-s', str(search)]
    
    if output:
        cmd.extend(['-o', str(output)])
    
    if 'averagetype' in kwargs:
        cmd.extend(['-a', kwargs['averagetype']])
    
    if 'backgroundcolor' in kwargs:
        bg = kwargs['backgroundcolor']
        cmd.extend(['-b', f"{bg[0]},{bg[1]},{bg[2]}"])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Depix failed: {result.stderr}")
    
    return output or 'output.png'

# Usage
if __name__ == '__main__':
    result = depix(
        'test.png',
        'search.png',
        output='result.png',
        averagetype='linear',
        backgroundcolor=(40, 41, 35)
    )
    print(f"Saved to {result}")
```

## Comparison Examples

### Compare Different Methods

```bash
#!/bin/bash
# compare_methods.sh

IMAGE="pixelated.png"
SEARCH="search.png"

echo "Testing gamma-corrected averaging..."
python3 depix.py -p "$IMAGE" -s "$SEARCH" \
    --averagetype gammacorrected -o output_gamma.png

echo "Testing linear averaging..."
python3 depix.py -p "$IMAGE" -s "$SEARCH" \
    --averagetype linear -o output_linear.png

echo "Testing with background filter..."
python3 depix.py -p "$IMAGE" -s "$SEARCH" \
    --backgroundcolor 40,41,35 -o output_bg.png

echo "Testing linear + background..."
python3 depix.py -p "$IMAGE" -s "$SEARCH" \
    --averagetype linear --backgroundcolor 40,41,35 -o output_both.png

echo "Done! Check output_*.png files"
```

### Quality Metrics

```python
# quality_metrics.py
from PIL import Image
import numpy as np

def calculate_similarity(img1_path, img2_path):
    """Calculate similarity between two images."""
    img1 = np.array(Image.open(img1_path))
    img2 = np.array(Image.open(img2_path))
    
    # Ensure same size
    if img1.shape != img2.shape:
        return 0.0
    
    # Calculate MSE
    mse = np.mean((img1 - img2) ** 2)
    
    # Calculate PSNR
    if mse == 0:
        return 100.0
    
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    
    return psnr

# Compare outputs
original = "original.png"
outputs = [
    "output_gamma.png",
    "output_linear.png",
    "output_bg.png",
    "output_both.png"
]

print("Quality Comparison (PSNR - higher is better):")
for output in outputs:
    score = calculate_similarity(original, output)
    print(f"{output:25s}: {score:.2f} dB")
```

## Automation Examples

### Automated Testing

```python
# test_depix_quality.py
import subprocess
import os
from pathlib import Path

def test_depixelization(test_cases):
    """Run depixelization tests and report results."""
    results = []
    
    for name, pixelated, search, expected in test_cases:
        print(f"\nTesting: {name}")
        output = f"test_output_{name}.png"
        
        # Run depix
        cmd = ['python3', 'depix.py', '-p', pixelated, '-s', search, '-o', output]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Check if output matches expected (optional)
            if expected and os.path.exists(expected):
                # Could use image comparison here
                pass
            
            results.append({
                'name': name,
                'status': 'PASS',
                'output': output
            })
            print(f"✓ {name} passed")
        else:
            results.append({
                'name': name,
                'status': 'FAIL',
                'error': result.stderr
            })
            print(f"✗ {name} failed: {result.stderr}")
    
    return results

# Test cases
test_cases = [
    ('notepad_test', 'test1_pix.png', 'search1.png', 'expected1.png'),
    ('sublime_test', 'test2_pix.png', 'search2.png', 'expected2.png'),
    ('vscode_test', 'test3_pix.png', 'search3.png', 'expected3.png'),
]

results = test_depixelization(test_cases)

# Print summary
passed = sum(1 for r in results if r['status'] == 'PASS')
failed = sum(1 for r in results if r['status'] == 'FAIL')
print(f"\n{'='*50}")
print(f"Results: {passed} passed, {failed} failed")
```

### Continuous Integration

```yaml
# .github/workflows/test.yml
name: Depix Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run unit tests
      run: |
        python -m pytest tests/
    
    - name: Run integration tests
      run: |
        python3 depix.py \
          -p images/testimages/testimage3_pixels.png \
          -s images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png \
          -o test_output.png
        
        # Check if output was created
        test -f test_output.png
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v2
      with:
        name: test-outputs
        path: test_output.png
```

## Advanced Techniques

### Multi-Pass Processing

```bash
#!/bin/bash
# multi_pass.sh - Try multiple methods and pick best result

IMAGE="pixelated.png"
SEARCH="search.png"

# Pass 1: Gamma-corrected
python3 depix.py -p "$IMAGE" -s "$SEARCH" -o pass1.png

# Pass 2: Linear
python3 depix.py -p "$IMAGE" -s "$SEARCH" --averagetype linear -o pass2.png

# Pass 3: Combine best parts
python3 <<EOF
from PIL import Image
import numpy as np

# Load both outputs
img1 = np.array(Image.open('pass1.png'))
img2 = np.array(Image.open('pass2.png'))
original = np.array(Image.open('$IMAGE'))

# For each pixel, choose output closest to original
result = np.zeros_like(img1)
for i in range(img1.shape[0]):
    for j in range(img1.shape[1]):
        dist1 = np.linalg.norm(img1[i,j] - original[i,j])
        dist2 = np.linalg.norm(img2[i,j] - original[i,j])
        result[i,j] = img1[i,j] if dist1 < dist2 else img2[i,j]

# Save combined result
Image.fromarray(result).save('combined.png')
print("Saved combined result to combined.png")
EOF
```

### Region-Specific Processing

```python
# process_regions.py
from PIL import Image
import subprocess

def process_regions(image_path, search_path, regions):
    """
    Process specific regions with different settings.
    
    Args:
        image_path: Path to pixelated image
        search_path: Path to search image
        regions: List of (x, y, w, h, settings) tuples
    """
    img = Image.open(image_path)
    result = img.copy()
    
    for i, (x, y, w, h, settings) in enumerate(regions):
        # Crop region
        region = img.crop((x, y, x+w, y+h))
        region_path = f'region_{i}.png'
        region.save(region_path)
        
        # Process with specific settings
        output_path = f'region_{i}_output.png'
        cmd = [
            'python3', 'depix.py',
            '-p', region_path,
            '-s', search_path,
            '-o', output_path
        ]
        
        if 'averagetype' in settings:
            cmd.extend(['-a', settings['averagetype']])
        if 'backgroundcolor' in settings:
            bg = settings['backgroundcolor']
            cmd.extend(['-b', f"{bg[0]},{bg[1]},{bg[2]}"])
        
        subprocess.run(cmd)
        
        # Paste back
        processed = Image.open(output_path)
        result.paste(processed, (x, y))
    
    result.save('final_result.png')
    print("Saved final result to final_result.png")

# Example usage
regions = [
    # (x, y, width, height, settings)
    (0, 0, 100, 50, {'averagetype': 'linear'}),
    (100, 0, 100, 50, {'averagetype': 'gammacorrected'}),
    (0, 50, 200, 50, {'backgroundcolor': (40, 41, 35)})
]

process_regions('pixelated.png', 'search.png', regions)
```

## Tips and Tricks

### 1. Quick Quality Check

```bash
# Generate test, then depixelize and compare
python3 tool_gen_pixelated.py -i original.png -o test_pix.png
python3 depix.py -p test_pix.png -s search.png -o recovered.png

# Visual comparison
open original.png recovered.png  # macOS
# or
eog original.png recovered.png   # Linux
```

### 2. Finding Optimal Settings

```python
# find_best_settings.py
import subprocess
import itertools
from PIL import Image
import numpy as np

def try_settings(pixelated, search, original, avg_types, bg_colors):
    """Try all combinations of settings."""
    best_score = 0
    best_settings = None
    
    for avg in avg_types:
        for bg in bg_colors:
            output = f'test_{avg}_{bg}.png'
            cmd = ['python3', 'depix.py', '-p', pixelated, '-s', search, '-o', output, '-a', avg]
            
            if bg:
                cmd.extend(['-b', f'{bg[0]},{bg[1]},{bg[2]}'])
            
            subprocess.run(cmd, capture_output=True)
            
            # Calculate quality
            score = calculate_quality(output, original)
            print(f"Settings: avg={avg}, bg={bg}, score={score:.2f}")
            
            if score > best_score:
                best_score = score
                best_settings = (avg, bg)
    
    return best_settings, best_score

def calculate_quality(output, original):
    """Calculate quality metric."""
    # Implementation from earlier example
    pass

# Try combinations
best, score = try_settings(
    'pixelated.png',
    'search.png',
    'original.png',
    ['gammacorrected', 'linear'],
    [None, (40, 41, 35), (30, 30, 30)]
)

print(f"\nBest settings: {best} (score: {score:.2f})")
```

### 3. Debugging Failed Depixelization

```bash
# debug_depix.sh
#!/bin/bash

IMAGE="$1"
SEARCH="$2"

echo "=== Depix Debugging ==="

# 1. Check image properties
echo -e "\n1. Image Properties:"
python3 <<EOF
from PIL import Image
img = Image.open('$IMAGE')
print(f"  Size: {img.size}")
print(f"  Mode: {img.mode}")
print(f"  Format: {img.format}")
EOF

# 2. Visualize blocks
echo -e "\n2. Visualizing detected blocks..."
python3 tool_show_boxes.py -p "$IMAGE" -s "$SEARCH" -o debug_boxes.png
echo "  Saved to debug_boxes.png - check if blocks look correct"

# 3. Try both averaging methods
echo -e "\n3. Testing averaging methods..."
python3 depix.py -p "$IMAGE" -s "$SEARCH" -a gammacorrected -o debug_gamma.png 2>&1 | grep "matches"
python3 depix.py -p "$IMAGE" -s "$SEARCH" -a linear -o debug_linear.png 2>&1 | grep "matches"

echo -e "\n=== Debug Complete ===" 
echo "Check debug_*.png files for results"
```

These examples should cover most use cases for the Depix tool!
