# Depix

Depix is a proof-of-concept tool for recovering plaintext from pixelized screenshots.

This implementation works on pixelized images created with linear box filters. Read more about the technique in [this article](https://www.spipm.nl/2030.html).

## Features

- 🔍 Recover text from pixelated screenshots
- ⚡ NumPy-accelerated template matching
- 🎨 Support for multiple averaging methods (gamma-corrected, linear)
- 🛠️ Additional tools for visualization and testing
- 📊 Detailed progress logging and statistics

## Example

![Example](docs/img/Recovering_prototype_latest.png)

## Installation

### Requirements

- Python 3.7+
- PIL/Pillow
- NumPy
- OpenCV (cv2)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/depix.git
cd depix

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Depixelization

```bash
python3 depix.py \
    -p /path/to/pixelated/image.png \
    -s /path/to/search/image.png \
    -o /path/to/output.png
```

### Options

- `-p, --pixelimage PATH` - Path to pixelated image (required)
- `-s, --searchimage PATH` - Path to search pattern image (required)
- `-o, --outputimage PATH` - Path to output image (default: output.png)
- `-a, --averagetype TYPE` - Averaging method: `gammacorrected` or `linear` (default: gammacorrected)
- `-b, --backgroundcolor R,G,B` - Background color to ignore (e.g., `40,41,35`)

### Example: Notepad Screenshot (Windows)

```bash
python3 depix.py \
    -p images/testimages/testimage3_pixels.png \
    -s images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png
```

### Example: Sublime Text (Linear Averaging)

```bash
python3 depix.py \
    -p images/testimages/sublime_screenshot_pixels_gimp.png \
    -s images/searchimages/debruin_sublime_Linux_small.png \
    --backgroundcolor 40,41,35 \
    --averagetype linear
```

## Additional Tools

### Visualize Detected Blocks

Use this tool to verify that pixelated blocks are detected correctly:

```bash
python3 tool_show_boxes.py \
    -p /path/to/pixelated/image.png \
    -s /path/to/search/image.png
```

Options:
- `-e, --enhance N` - Enhancement factor for visualization (default: 3)
- `-o, --outputimage PATH` - Save visualization to file instead of displaying

### Generate Pixelated Test Images

```bash
python3 tool_gen_pixelated.py \
    -i /path/to/input/image.png \
    -o /path/to/output.png \
    --blocksize 5 \
    --method gamma
```

Options:
- `-b, --blocksize N` - Size of pixelation blocks (default: 5)
- `-m, --method METHOD` - Averaging method: `gamma` or `linear` (default: gamma)

## Creating Search Images

To create an effective search image:

1. **Cut out the pixelated region** exactly from your screenshot
2. **Create a De Bruijn sequence** containing all expected characters
3. **Paste into the same editor** with identical settings:
   - Same font and size
   - Same text colors
   - Same background color
4. **Take a screenshot** of the De Bruijn sequence
5. **Use as search image** with the `-s` flag

### De Bruijn Sequence

A [De Bruijn sequence](https://en.wikipedia.org/wiki/De_Bruijn_sequence) is a cyclic sequence where every possible substring of length n appears exactly once. This ensures all character combinations are available for matching.

## How It Works

### Algorithm Overview

1. **Block Detection**: Identify same-color rectangular blocks in the pixelated image
2. **Template Matching**: Search for each block in the search image using OpenCV's template matching
3. **Single Match Resolution**: Directly copy blocks with unique matches
4. **Multiple Match Averaging**: Average all possible matches for ambiguous blocks
5. **Output Generation**: Reconstruct the depixelized image

### Key Assumptions

- The pixelation used a linear box filter
- Text positioning is at pixel-level precision (not sub-pixel)
- No additional compression was applied after pixelation
- Font settings match between original and search images

## Known Limitations

- **Sub-pixel rendering**: Modern text rasterizers may use sub-pixel positioning, which can reduce accuracy
- **Font matching**: Requires knowledge of the exact font, size, and rendering settings
- **Compression artifacts**: Additional image compression can corrupt the pixelated blocks
- **Block boundary alignment**: The algorithm requires pixel-perfect block boundaries

## Performance

- **NumPy acceleration**: Fast template matching using OpenCV
- **Progress tracking**: Real-time progress updates for large images
- **Memory efficient**: Streams pixel data without loading entire arrays

## Troubleshooting

### Too many block size variants

If you see this warning:
```
WARNING - Too many variants on block size. Re-cropping the image might help.
```

**Solution**: Your pixelated region may not be cut precisely. Use `tool_show_boxes.py` to visualize detected blocks and re-crop more carefully.

### No matches found

**Possible causes**:
- Font doesn't match between pixelated and search images
- Different text rendering settings (antialiasing, hinting)
- Different background colors
- Wrong averaging method (try switching between `gamma` and `linear`)

### Poor results

**Try**:
- Ensure the search image uses the exact same font settings
- Include more character variations in your De Bruijn sequence
- Try both averaging methods
- Filter background color with `--backgroundcolor`

## Related Projects

- **[DepixHMM](https://github.com/JonasSchatz/DepixHMM)** - HMM-based approach with better precision
- **[UnRedacter](https://github.com/BishopFox/unredacter)** - Advanced tool by Bishop Fox
- **[de-pixelate](https://github.com/KoKuToru/de-pixelate_gaV-O6NPWrI)** - TensorFlow-based video depixelation

## Contributing

Contributions are welcome! Areas for improvement:

- Additional averaging filter implementations
- HMM-based enhancement
- Sub-pixel positioning support
- Better block detection algorithms
- GUI interface

## License

This work is licensed under a Creative Commons Attribution 4.0 International License.
See LICENSE file for details.

## Disclaimer

This tool is for educational and research purposes only. Always obtain proper authorization before attempting to recover redacted information.

## Acknowledgments

- Original research on depixelization techniques
- OpenCV and NumPy communities
- Contributors and testers

---

**Note**: This is a proof-of-concept. For production use, consider more sophisticated approaches like HMM-based methods.
