from PIL import Image, ImageDraw
import numpy as np
import cv2

def main():
    light = brightness_correction()
    handled = binarization(light)
    remove_noise(handled)
