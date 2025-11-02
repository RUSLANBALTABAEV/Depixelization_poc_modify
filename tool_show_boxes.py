from __future__ import annotations

import argparse
import logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

from PIL import Image, ImageDraw

from depixlib.helpers import check_file, check_color
from depixlib.functions import (
    findRectangleSizeOccurences,
    findSameColorSubRectangles,
    removeMootColorRectangles
)
from depixlib.LoadedImage import LoadedImage
from depixlib.Rectangle import Rectangle

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    
    usage = """
    note:
        The pixelated rectangle must be cut out to only include the pixelated rectangles.
        The pattern search image is generally a screenshot of a De Bruijn sequence of expected characters,
        made on a machine with the same editor and text size as the original screenshot that was pixelated.
    """

    parser = argparse.ArgumentParser(
        description="Visualize detected pixelated blocks.",
        epilog=usage
    )
    parser.add_argument(
        "-p",
        "--pixelimage",
        help="path to image with pixelated rectangle",
        required=True,
        type=check_file,
        metavar="PATH"
    )
    parser.add_argument(
        "-s",
        "--searchimage",
        help="path to image with patterns to search",
        required=True,
        type=check_file,
        metavar="PATH",
    )
    parser.add_argument(
        "-b",
        "--backgroundcolor",
        help="original editor background color in format r,g,b (color to ignore)",
        default=None,
        type=check_color,
        metavar="RGB"
    )
    parser.add_argument(
        "-e",
        "--enhance",
        help="enhancement factor (default: 3)",
        default=3,
        type=int,
        metavar="N"
    )
    parser.add_argument(
        "-o",
        "--outputimage",
        help="path to save output image (optional)",
        default=None,
        metavar="PATH",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    pixelatedImagePath = args.pixelimage
    searchImagePath = args.searchimage
    editorBackgroundColor = args.backgroundcolor

    logger.info("Loading pixelated image from %s", pixelatedImagePath)
    pixelatedImage = LoadedImage(pixelatedImagePath)

    logger.info("Loading search image from %s", searchImagePath)
    searchImage = LoadedImage(searchImagePath)

    logger.info("Finding color rectangles from pixelated space")
    pixelatedRectangle = Rectangle(
        (0, 0), (pixelatedImage.width - 1, pixelatedImage.height - 1)
    )

    pixelatedSubRectangles = findSameColorSubRectangles(
        pixelatedImage, pixelatedRectangle
    )
    logger.info("Found %d same color rectangles", len(pixelatedSubRectangles))

    pixelatedSubRectangles = removeMootColorRectangles(
        pixelatedSubRectangles, editorBackgroundColor
    )
    logger.info("%d rectangles left after moot filter", len(pixelatedSubRectangles))

    rectangleSizeOccurrences = findRectangleSizeOccurences(pixelatedSubRectangles)
    logger.info("Found %d different rectangle sizes", len(rectangleSizeOccurrences))
    
    if len(rectangleSizeOccurrences) > max(
        10, pixelatedRectangle.width * pixelatedRectangle.height * 0.01
    ):
        logger.warning(
            "Too many variants on block size. Re-cropping the image might help."
        )

    # Enhance image
    enhance = args.enhance
    logger.info("Creating visualization with %dx enhancement", enhance)
    
    image = Image.open(pixelatedImagePath)
    enhancedImage = image.resize((image.width*enhance, image.height*enhance))
    draw = ImageDraw.Draw(enhancedImage)

    # Draw boxes
    for box in pixelatedSubRectangles:
        draw.rectangle([
            (box.x*enhance, box.y*enhance),
            ((box.x+box.width)*enhance - enhance, (box.y+box.height)*enhance - enhance)
        ], outline="red", width=1)

    # Save or show
    if args.outputimage:
        enhancedImage.save(args.outputimage)
        logger.info("Saved visualization to %s", args.outputimage)
    else:
        enhancedImage.show()


if __name__ == "__main__":
    main()
