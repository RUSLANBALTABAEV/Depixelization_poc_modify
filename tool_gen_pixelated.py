"""
Tool to generate pixelated images for testing.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

from depixlib.helpers import check_file
from depixlib.LoadedImage import LoadedImage

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate pixelized image from a given image.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
    python3 tool_gen_pixelated.py -i input.png -o pixelated.png
    python3 tool_gen_pixelated.py -i input.png -o output.png --blocksize 10
    python3 tool_gen_pixelated.py -i input.png --method linear
        """
    )
    parser.add_argument(
        "-i", "--image",
        help="Path to image to pixelize",
        required=True,
        type=check_file,
        metavar="PATH"
    )
    parser.add_argument(
        "-o", "--outputimage",
        help="Path to output image (default: output_pixelated.png)",
        default="output_pixelated.png",
        metavar="PATH"
    )
    parser.add_argument(
        "-b", "--blocksize",
        help="Size of pixelation blocks (default: 5)",
        default=5,
        type=int,
        metavar="N"
    )
    parser.add_argument(
        "-m", "--method",
        help="Averaging method (default: gamma)",
        default="gamma",
        choices=["gamma", "linear"],
        metavar="METHOD"
    )
    return parser.parse_args()


def pixelate_gamma_corrected(
    image: LoadedImage,
    block_size: int
) -> list[list[tuple[int, int, int]]]:
    """
    Pixelate using gamma-corrected averaging (mimics most screenshot tools).
    
    Args:
        image: Input image
        block_size: Size of pixelation blocks
        
    Returns:
        2D array of RGB tuples
    """
    output_data = [[None for _ in range(image.height)] for _ in range(image.width)]
    
    for x in range(0, image.width, block_size):
        for y in range(0, image.height, block_size):
            # Calculate block boundaries
            max_x = min(x + block_size, image.width)
            max_y = min(y + block_size, image.height)
            
            # Accumulate RGB values
            r_sum = g_sum = b_sum = 0
            pixel_count = 0
            
            for xx in range(x, max_x):
                for yy in range(y, max_y):
                    pixel = image.imageData[xx][yy]
                    r_sum += pixel[0]
                    g_sum += pixel[1]
                    b_sum += pixel[2]
                    pixel_count += 1
            
            # Calculate average
            avg_r = int(r_sum / pixel_count)
            avg_g = int(g_sum / pixel_count)
            avg_b = int(b_sum / pixel_count)
            avg_color = (avg_r, avg_g, avg_b)
            
            # Apply average to all pixels in block
            for xx in range(x, max_x):
                for yy in range(y, max_y):
                    output_data[xx][yy] = avg_color
    
    return output_data


def pixelate_linear(
    image: LoadedImage,
    block_size: int
) -> list[list[tuple[int, int, int]]]:
    """
    Pixelate using linear RGB averaging (mimics GIMP).
    
    Args:
        image: Input image
        block_size: Size of pixelation blocks
        
    Returns:
        2D array of RGB tuples
    """
    output_data = [[None for _ in range(image.height)] for _ in range(image.width)]
    
    for x in range(0, image.width, block_size):
        for y in range(0, image.height, block_size):
            # Calculate block boundaries
            max_x = min(x + block_size, image.width)
            max_y = min(y + block_size, image.height)
            
            # Accumulate linear RGB values
            r_sum = g_sum = b_sum = 0
            pixel_count = 0
            
            for xx in range(x, max_x):
                for yy in range(y, max_y):
                    pixel = image.imageData[xx][yy]
                    # Convert to linear space (gamma = 2.2)
                    r_linear = (pixel[0] / 255.0) ** 2.2
                    g_linear = (pixel[1] / 255.0) ** 2.2
                    b_linear = (pixel[2] / 255.0) ** 2.2
                    
                    r_sum += r_linear
                    g_sum += g_linear
                    b_sum += b_linear
                    pixel_count += 1
            
            # Calculate average in linear space
            avg_r_linear = r_sum / pixel_count
            avg_g_linear = g_sum / pixel_count
            avg_b_linear = b_sum / pixel_count
            
            # Convert back to sRGB
            avg_r = int((avg_r_linear ** (1/2.2)) * 255)
            avg_g = int((avg_g_linear ** (1/2.2)) * 255)
            avg_b = int((avg_b_linear ** (1/2.2)) * 255)
            avg_color = (avg_r, avg_g, avg_b)
            
            # Apply average to all pixels in block
            for xx in range(x, max_x):
                for yy in range(y, max_y):
                    output_data[xx][yy] = avg_color
    
    return output_data


def main() -> None:
    """Main pixelation function."""
    args = parse_args()

    try:
        # Validate block size
        if args.blocksize < 1:
            raise ValueError("Block size must be at least 1")
        if args.blocksize > 100:
            logger.warning(
                "Block size %d is very large. Consider using smaller value.",
                args.blocksize
            )

        # Load image
        logger.info("Loading image from %s", args.image)
        image = LoadedImage(args.image)
        logger.info("Image size: %dx%d", image.width, image.height)

        # Create output image
        output_image = image.getCopyOfLoadedPILImage()

        # Pixelate based on method
        logger.info(
            "Pixelating with block size %d using %s method",
            args.blocksize,
            args.method
        )
        
        if args.method == "linear":
            output_data = pixelate_linear(image, args.blocksize)
        else:
            output_data = pixelate_gamma_corrected(image, args.blocksize)

        # Apply pixelated data to output image
        for x in range(image.width):
            for y in range(image.height):
                if output_data[x][y] is not None:
                    output_image.putpixel((x, y), output_data[x][y])

        # Save output
        output_path = Path(args.outputimage)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_image.save(str(output_path))
        logger.info("Successfully saved pixelated image to: %s", args.outputimage)

        # Calculate statistics
        total_pixels = image.width * image.height
        blocks_x = (image.width + args.blocksize - 1) // args.blocksize
        blocks_y = (image.height + args.blocksize - 1) // args.blocksize
        total_blocks = blocks_x * blocks_y
        compression_ratio = total_pixels / total_blocks

        logger.info("\n=== Statistics ===")
        logger.info("Original pixels: %d", total_pixels)
        logger.info("Pixelated blocks: %d (%dx%d)", total_blocks, blocks_x, blocks_y)
        logger.info("Compression ratio: %.2fx", compression_ratio)

    except Exception as e:
        logger.error("Error during pixelation: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
