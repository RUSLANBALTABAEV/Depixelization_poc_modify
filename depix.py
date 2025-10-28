from __future__ import annotations

import argparse
import logging
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recover passwords from pixelized screenshots."
    )
    parser.add_argument("-p", "--pixelimage", required=True, type=check_file, metavar="PATH")
    parser.add_argument("-s", "--searchimage", required=True, type=check_file, metavar="PATH")
    parser.add_argument("-a", "--averagetype", default="gammacorrected", choices=["gammacorrected", "linear"])
    parser.add_argument("-b", "--backgroundcolor", default=None, type=check_color, metavar="RGB")
    parser.add_argument("-o", "--outputimage", default="output.png", metavar="PATH")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logging.info("Loading pixelated image from %s", args.pixelimage)
    pixelatedImage = LoadedImage(args.pixelimage)
    unpixelatedOutputImage = pixelatedImage.getCopyOfLoadedPILImage()

    logging.info("Loading search image from %s", args.searchimage)
    searchImage = LoadedImage(args.searchimage)

    logging.info("Finding color rectangles from pixelated space")
    pixelatedRectange = Rectangle((0, 0), (pixelatedImage.width - 1, pixelatedImage.height - 1))
    pixelatedSubRectanges = findSameColorSubRectangles(pixelatedImage, pixelatedRectange)
    logging.info("Found %s same color rectangles", len(pixelatedSubRectanges))

    pixelatedSubRectanges = removeMootColorRectangles(pixelatedSubRectanges, args.backgroundcolor)
    logging.info("%s rectangles left after moot filter", len(pixelatedSubRectanges))

    rectangeSizeOccurences = findRectangleSizeOccurences(pixelatedSubRectanges)
    logging.info("Found %s different rectangle sizes", len(rectangeSizeOccurences))

    logging.info("Finding matches in search image")
    rectangleMatches = findRectangleMatches(rectangeSizeOccurences, pixelatedSubRectanges, searchImage, pixelatedImage, args.averagetype)

    logging.info("Removing blocks with no matches")
    pixelatedSubRectanges = dropEmptyRectangleMatches(rectangleMatches, pixelatedSubRectanges)

    logging.info("Splitting single matches and multiple matches")
    singleResults, pixelatedSubRectanges = splitSingleMatchAndMultipleMatches(pixelatedSubRectanges, rectangleMatches)
    logging.info("[%s straight matches | %s multiple matches]", len(singleResults), len(pixelatedSubRectanges))

    logging.info("Writing single match results to output")
    writeFirstMatchToImage(singleResults, rectangleMatches, searchImage, unpixelatedOutputImage)

    logging.info("Writing average results for multiple matches to output")
    writeAverageMatchToImage(pixelatedSubRectanges, rectangleMatches, searchImage, unpixelatedOutputImage)

    logging.info("Saving output image to: %s", args.outputimage)
    unpixelatedOutputImage.save(args.outputimage)


if __name__ == "__main__":
    main()
