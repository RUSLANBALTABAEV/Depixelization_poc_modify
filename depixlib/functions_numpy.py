import logging
import numpy as np
import cv2
from depixlib.Rectangle import RectangleMatch

def findRectangleMatches(rectangeSizeOccurences, pixelatedSubRectanges, searchImage, pixelatedImage, averageType):
    logging.info("Using NumPy-accelerated findRectangleMatches")
    search_array = np.array(searchImage.getCopyOfLoadedPILImage(), dtype=np.float32)/255.0
    pixel_array = np.array(pixelatedImage.getCopyOfLoadedPILImage(), dtype=np.float32)/255.0
    if search_array.shape[-1]==4:
        search_array=search_array[:,:,:3]
    if pixel_array.shape[-1]==4:
        pixel_array=pixel_array[:,:,:3]
    matches={}
    for (w,h),_ in rectangeSizeOccurences.items():
        logging.debug("Block size: %s x %s", w, h)
        for r in pixelatedSubRectanges:
            if r.width!=w or r.height!=h:
                continue
            block = pixel_array[r.y:r.y+h, r.x:r.x+w, :]
            res = cv2.matchTemplate(search_array, block, cv2.TM_SQDIFF_NORMED)
            _,_,min_loc,_ = cv2.minMaxLoc(res)
            match = RectangleMatch(min_loc[0], min_loc[1], block.copy())
            matches[(r.x,r.y)] = [match]
    logging.info("Found %s matches", len(matches))
    return matches
