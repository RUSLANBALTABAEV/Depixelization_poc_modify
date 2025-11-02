# Depix Quick Start Guide

Get started with Depix in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/depix.git
cd depix

# Install dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .
```

## Basic Usage

### 1. Simple Depixelization

```bash
python3 depix.py \
    -p path/to/pixelated.png \
    -s path/to/search.png \
    -o output.png
```

### 2. Try the Example

```bash
python3 depix.py \
    -p images/testimages/testimage3_pixels.png \
    -s images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png \
    -o example_output.png
```

## Common Options

### Different Averaging Method
```bash
# For GIMP-pixelated images
python3 depix.py -p image.png -s search.png --averagetype linear
```

### Filter Background Color
```bash
# Ignore editor background (e.g., Sublime Text)
python3 depix.py -p image.png -s search.png --backgroundcolor 40,41,35
```

### Combine Options
```bash
python3 depix.py \
    -p sublime_pixelated.png \
    -s sublime_search.png \
    --averagetype linear \
    --backgroundcolor 40,41,35 \
    -o recovered.png
```

## Visualization Tool

Before depixelizing, check if blocks are detected correctly:

```bash
python3 tool_show_boxes.py -p pixelated.png -s search.png
```

**Good detection:** Clean, rectangular boxes  
**Bad detection:** Fragmented or overlapping → re-crop image

## Create Test Images

```bash
# Generate pixelated image for testing
python3 tool_gen_pixelated.py \
    -i original.png \
    -o pixelated.png \
    --blocksize 5
```

## Workflow Example

### Step 1: Prepare Your Images

1. **Pixelated image**: Cut out ONLY the pixelated region
2. **Search image**: Screenshot of De Bruijn sequence with same font/settings

### Step 2: Verify Detection

```bash
python3 tool_show_boxes.py -p pixelated.png -s search.png
```

If blocks look wrong, re-crop the pixelated image more precisely.

### Step 3: Run Depixelization

```bash
# Try default settings first
python3 depix.py -p pixelated.png -s search.png -o output1.png

# If results are poor, try linear
python3 depix.py -p pixelated.png -s search.png --averagetype linear -o output2.png

# Compare and pick best
```

### Step 4: Check Results

Open the output images and compare quality. The best method depends on how the original was pixelated.

## Common Issues

### ❌ "Too many block size variants"
**Solution:** Re-crop the pixelated region more precisely. Use `tool_show_boxes.py` to visualize.

### ❌ "No matches found"
**Solutions:**
- Try opposite averaging method (`linear` ↔ `gammacorrected`)
- Verify font settings match exactly
- Ensure search image has all necessary characters

### ❌ Poor quality results
**Solutions:**
- Try both averaging methods
- Add `--backgroundcolor` filter
- Verify the original wasn't compressed after pixelation
- Check if text uses sub-pixel rendering

## Next Steps

- **Read full documentation**: `README.md`
- **See more examples**: `EXAMPLES.md`
- **Understand the algorithm**: `ARCHITECTURE.md`
- **Check changelog**: `CHANGELOG.md`

## Getting Help

1. Check `EXAMPLES.md` for similar use cases
2. Run `python3 depix.py --help` for all options
3. Use `tool_show_boxes.py` to debug detection issues
4. Read troubleshooting in `README.md`

## Tips

✅ **DO:**
- Cut pixelated regions precisely
- Match font settings exactly
- Use De Bruijn sequences for search images
- Try both averaging methods
- Visualize detection first

❌ **DON'T:**
- Include non-pixelated borders
- Use compressed images as input
- Expect perfect results with sub-pixel text
- Use different font settings
- Skip the visualization step

## Quick Reference

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--pixelimage` | `-p` | Pixelated image path | *required* |
| `--searchimage` | `-s` | Search image path | *required* |
| `--outputimage` | `-o` | Output image path | `output.png` |
| `--averagetype` | `-a` | Averaging method | `gammacorrected` |
| `--backgroundcolor` | `-b` | Background color | `None` |

### Averaging Methods

- **`gammacorrected`** (default): For Windows Snipping Tool, Greenshot, most screenshot tools
- **`linear`**: For GIMP, professional image editors

### Common Background Colors

| Editor | RGB Values |
|--------|------------|
| Sublime Text Dark | `40,41,35` |
| VS Code Dark | `30,30,30` |
| Notepad | `255,255,255` |
| Terminal | `0,0,0` |

## Example Session

```bash
$ cd depix

# Check what we have
$ ls images/testimages/
testimage3_pixels.png

# Visualize detection
$ python3 tool_show_boxes.py \
    -p images/testimages/testimage3_pixels.png \
    -s images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png

# Looks good! Run depixelization
$ python3 depix.py \
    -p images/testimages/testimage3_pixels.png \
    -s images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png \
    -o recovered.png

2024-10-28 10:30:00 - INFO - Loading pixelated image...
2024-10-28 10:30:00 - INFO - Loading search image...
2024-10-28 10:30:01 - INFO - Found 189 same color rectangles
2024-10-28 10:30:02 - INFO - [156 straight matches | 33 multiple matches]
2024-10-28 10:30:02 - INFO - Successfully saved output image to: recovered.png

# Success!
$ open recovered.png
```

## Performance Tips

For large images:
- **Monitor progress**: Watch console output
- **Use visualization first**: Catch issues early
- **Process regions separately**: If very large
- **Check memory usage**: May need more RAM

## That's It!

You're now ready to use Depix. For more advanced usage, check out the other documentation files.

Happy depixelizing! 🔍✨
