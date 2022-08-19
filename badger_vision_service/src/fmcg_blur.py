"""
    FMCG Blur filter

    Will blur out any blacklisted polygons in a given image.
    Grabs the image from s3 and returns it to s3.
"""
import logging
import cv2
import numpy as np


class FMCGBlur:
    def __init__(self, properties):
        self.mask_color = properties["mask_color"]
        self.mask_polygons = properties["mask_polygons"]

    def blur(self, image):
        logging.info("blur started")
        mask_value = 255

        stencil = np.zeros(image.shape[:-1]).astype(np.uint8)
        cv2.fillPoly(stencil, self.create_polygon_list(), mask_value)

        mask = stencil != mask_value
# TODO: Convert web color to RGB
#        image[mask] = self.mask_color
        image[mask] = [128, 128, 128]

        logging.info("blur finished")

        return image

    def create_polygon_list(self):
        polygon_list = []
        for polygon in self.mask_polygons:
            polygon_list.append(self.convert_polygon(polygon))

        return np.asarray(polygon_list, dtype=np.int32)

    def convert_polygon(self, polygon):
        return np.array([[polygon[index], polygon[index + 1]] for index in range(0, len(polygon), 2)])




