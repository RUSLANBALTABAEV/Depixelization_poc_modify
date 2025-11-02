"""
Depix - PoC for recovering plaintext from pixelized screenshots.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

from depixlib.helpers import check_file, check_color
from depixlib.functions_numpy import findRectangleMatches
from depixlib.functions import (
    dropEmptyRectangleMatches,
    findRectangleSizeOccurences,
    findSameColorSubRectangles,
    removeMootColorRectangles,
    splitSingleMatchAndMultipleMatches,
    writeAverageMatchToImage,
    writeFirstMatchToImage
)
from depixlib.LoadedImage import LoadedImage
from depixlib.Rectangle import Rectangle

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Recover passwords from pixelized screenshots.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python3 depix.py -p pixelated.png -s search.png -o output.png
  python3 depix.py -p image.png -s search.png --averagetype linear
  python3 depix.py -p image.png -s search.png --backgroundcolor 40,41,35
        """
    )
    parser.add_argument(
        "-p", "--pixelimage",
        required=True,
        type=check_file,
        metavar="PATH",
        help="Path to pixelated image"
    )
    parser.add_argument(
        "-s", "--searchimage",
        required=True,
        type=check_file,
        metavar="PATH",
        help="Path to search image (De Bruijn sequence)"
    )
    parser.add_argument(
        "-a", "--averagetype",
        default="gammacorrected",
        choices=["gammacorrected", "linear"],
        help="Type of RGB averaging (default: gammacorrected)"
    )
    parser.add_argument(
        "-b", "--backgroundcolor",
        default=None,
        type=check_color,
        metavar="R,G,B",
        help="Background color to ignore (format: r,g,b)"
    )
    parser.add_argument(
        "-o", "--outputimage",
        default="output.png",
        metavar="PATH",
        help="Path to output image (default: output.png)"
    )
    return parser.parse_args()


def main() -> None:
    """Main depixelization function."""
    args = parse_args()

    try:
        # Load images
        logger.info("Loading pixelated image from %s", args.pixelimage)
        pixelatedImage = LoadedImage(args.pixelimage)
        unpixelatedOutputImage = pixelatedImage.getCopyOfLoadedPILImage()

        logger.info("Loading search image from %s", args.searchimage)
        searchImage = LoadedImage(args.searchimage)

        # Find rectangles
        logger.info("Finding color rectangles from pixelated space")
        pixelatedRectangle = Rectangle(
            (0, 0),
            (pixelatedImage.width - 1, pixelatedImage.height - 1)
        )
        pixelatedSubRectangles = findSameColorSubRectangles(
            pixelatedImage, pixelatedRectangle
        )
        logger.info("Found %d same color rectangles", len(pixelatedSubRectangles))

        # Filter rectangles
        pixelatedSubRectangles = removeMootColorRectangles(
            pixelatedSubRectangles, args.backgroundcolor
        )
        logger.info(
            "%d rectangles left after moot filter",
            len(pixelatedSubRectangles)
        )

        # Find rectangle sizes
        rectangleSizeOccurrences = findRectangleSizeOccurences(
            pixelatedSubRectangles
        )
        logger.info(
            "Found %d different rectangle sizes",
            len(rectangleSizeOccurrences)
        )

        # Find matches
        logger.info("Finding matches in search image")
        rectangleMatches = findRectangleMatches(
            rectangleSizeOccurrences,
            pixelatedSubRectangles,
            searchImage,
            pixelatedImage,
            args.averagetype
        )

        # Drop empty matches
        logger.info("Removing blocks with no matches")
        pixelatedSubRectangles = dropEmptyRectangleMatches(
            rectangleMatches,
            pixelatedSubRectangles
        )

        # Split matches
        logger.info("Splitting single matches and multiple matches")
        singleResults, pixelatedSubRectangles = splitSingleMatchAndMultipleMatches(
            pixelatedSubRectangles,
            rectangleMatches
        )
        logger.info(
            "[%d straight matches | %d multiple matches]",
            len(singleResults),
            len(pixelatedSubRectangles)
        )

        # Write results
        logger.info("Writing single match results to output")
        writeFirstMatchToImage(
            singleResults,
            rectangleMatches,
            searchImage,
            unpixelatedOutputImage
        )

        logger.info("Writing average results for multiple matches to output")
        writeAverageMatchToImage(
            pixelatedSubRectangles,
            rectangleMatches,
            searchImage,
            unpixelatedOutputImage
        )

        # Save output
        output_path = Path(args.outputimage)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        unpixelatedOutputImage.save(str(output_path))
        logger.info("Successfully saved output image to: %s", args.outputimage)

    except Exception as e:
        logger.error("Error during depixelization: %s", str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
