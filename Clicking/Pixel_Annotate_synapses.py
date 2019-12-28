#! /usr/bin/env python3
"""
File: Pixel_Annotate_synapses.py
Authors Jared Galloway
        Nick Wagner
Date: 12/23/2019

Date: 12/26/2019
The purpose of this script is to allow for pixel level annotations
of Empirical (non-simulated) microscopy images. The empirical image
used as the imput is converted to a numpy array and sub-patched 
using the empirical_prep function in DataPrep helpers.py.
"""

import argparse
import cv2
import numpy as np
import os

import sys
sys.path.insert(0,"../")
from DataPrep.helpers import *

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-o", "--out", required=True, help="Path to the annotation csv")
ap.add_argument("-s", "--size", default=32, help="size of image sub-patches")
ap.add_argument("-r", "--range", default=(0,1), help="range of the sub-patched images to annotate. ex: (0,2) will load the first two of the sub-patched images for annotation", type=tuple)
args = vars(ap.parse_args())

images_to_annotate = args["range"]

# Utilizes empirical prep 
empirical_sub_patched = empirical_prep([args["image"]], size=args["size"])

# this loops the number of times between the first number given in the range
# and the second to allow for annotation of SIZExSIZE patches and being able to
# choose which ones to annotate at the time
for i in range(int(images_to_annotate[1]), int(images_to_annotate[3])):
    # a unique set of clicked points
    clicked_points = set()

    # load the numpy image, clone it, and setup the mouse callback function
    # img = np.load(args["image"], allow_pickle = True)
    img = empirical_sub_patched[i]

    # initialize an empty pixelmap for output
    pixelmap = np.zeros(img.shape[:-1]).astype(np.int)
    
    def annotate(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN and (x,y) not in clicked_points:
            clicked_points.add((x,y))
            cv2.circle(image, (x,y), 0, (255,0,255), -1)
            pixelmap[x,y] = 1

    #output_fp = open(args["out"],"a")

    cv2.imwrite('color_img.jpg', img)
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 600,600)
    cv2.imshow("image", img);
    image = cv2.imread("color_img.jpg")
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", annotate, [empirical_sub_patched[i],pixelmap])
    
    # keep looping until the <esc> key is pressed
    # display the image and wait for a keypress
    while True:
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    
    # dumps the current SIZExSIZE image to a file with the prefix given 
    # with the -o flag and ending with the number of image annotated
    # followed by .out
    np.transpose(pixelmap).dump(args["out"] + str(i) + ".out")



