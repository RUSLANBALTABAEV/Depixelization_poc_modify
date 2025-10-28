from __future__ import annotations

import logging
from typing import List, Tuple
import numpy as np
from PIL import Image
from depixlib.LoadedImage import LoadedImage
from depixlib.Rectangle import ColorRectange, Rectangle, RectangleMatch


def findSameColorSubRectangles(pixelatedImage: LoadedImage, rectangle: Rectangle) -> List[ColorRectange]:
    rects = []
    x = rectangle.x
    maxx = rectangle.x + rectangle.width + 1
    maxy = rectangle.y + rectangle.height + 1

    while x < maxx:
        y = rectangle.y
        while y < maxy:
            startColor = pixelatedImage.imageData[x][y]
            width = 1
            while x + width < maxx and pixelatedImage.imageData[x + width][y] == startColor:
                width += 1
            height = 1
            while y + height < maxy and all(pixelatedImage.imageData[x + dx][y + height] == startColor for dx in range(width)):
                height += 1
            rects.append(ColorRectange(startColor, (x, y), (x + width, y + height)))
            y += height
        x += width
    return rects


def removeMootColorRectangles(rects: List[ColorRectange], editorBackgroundColor: Tuple[int,int,int]|None) -> List[ColorRectange]:
    mootColors = [(0,0,0),(255,255,255)]
    if editorBackgroundColor:
        mootColors.append(editorBackgroundColor)
    return [r for r in rects if r.color not in mootColors]


def findRectangleSizeOccurences(rects: List[ColorRectange]) -> dict[Tuple[int,int], int]:
    sizes = {}
    for r in rects:
        size = (r.width, r.height)
        sizes[size] = sizes.get(size, 0) + 1
    return sizes


def dropEmptyRectangleMatches(rectangleMatches: dict[Tuple[int,int], List[RectangleMatch]], pixelatedSubRectanges: List[ColorRectange]) -> List[ColorRectange]:
    return [r for r in pixelatedSubRectanges if (r.x,r.y) in rectangleMatches and len(rectangleMatches[(r.x,r.y)])>0]


def splitSingleMatchAndMultipleMatches(pixelatedSubRectanges: List[ColorRectange], rectangleMatches: dict[Tuple[int,int], List[RectangleMatch]]) -> Tuple[List[ColorRectange], List[ColorRectange]]:
    singleResults = []
    multiResults = []

    for r in pixelatedSubRectanges:
        matches = rectangleMatches[(r.x,r.y)]
        firstData = np.array(matches[0].data)
        single = True
        for m in matches[1:]:
            if not np.array_equal(firstData, np.array(m.data)):
                single = False
                break
        if single:
            singleResults.append(r)
        else:
            multiResults.append(r)
    logging.debug("Split single/multi: %s / %s", len(singleResults), len(multiResults))
    return singleResults, multiResults


def writeFirstMatchToImage(singleMatchRectangles: List[ColorRectange], rectangleMatches: dict[Tuple[int,int], List[RectangleMatch]], searchImage: LoadedImage, unpixelatedOutputImage: Image.Image):
    for r in singleMatchRectangles:
        match = rectangleMatches[(r.x,r.y)][0]
        for dx in range(r.width):
            for dy in range(r.height):
                color = searchImage.imageData[match.x + dx][match.y + dy]
                unpixelatedOutputImage.putpixel((r.x + dx, r.y + dy), color)


def writeAverageMatchToImage(pixelatedSubRectanges: List[ColorRectange], rectangleMatches: dict[Tuple[int,int], List[RectangleMatch]], searchImage: LoadedImage, unpixelatedOutputImage: Image.Image):
    for r in pixelatedSubRectanges:
        matches = rectangleMatches[(r.x,r.y)]
        img = Image.new("RGB", (r.width, r.height))
        for match in matches:
            idx = 0
            for dx in range(r.width):
                for dy in range(r.height):
                    px = match.data[idx]
                    idx += 1
                    curr = img.getpixel((dx,dy)) if img.getpixel((dx,dy)) else (0,0,0)
                    avg = tuple((px[i]+curr[i])//2 for i in range(3))
                    img.putpixel((dx,dy), avg)
        for dx in range(r.width):
            for dy in range(r.height):
                unpixelatedOutputImage.putpixel((r.x+dx, r.y+dy), img.getpixel((dx,dy)))
