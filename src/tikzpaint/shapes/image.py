from typing import Generator, Iterable, Any
import numpy as np
from numpy.typing import NDArray
import matplotlib.image as mpimg

from tikzpaint.figures import Drawable, Displayable
from tikzpaint.util import Coordinates, copy, Number

from tikzpaint.shapes.base import L0Path

class Image(Drawable):
    def __init__(self, img_path: str, color_accuracy: int = 5):
        """Implementation of an image that can be drawn in SVG and TeX. Inherently, we can only display so many colors before the code gets ridiculous, So color_accuracy defines the number of colors you want. Default is 5"""
        # Perform the clustering algorithm and store the paths on initialization
        image = mpimg.imread(img_path)
        image = self._preprocess(image)
        colors, labels = self.cluster(image, color_accuracy)
        
        pass
    
    def _preprocess(self, img: NDArray) -> NDArray[np.float64]:
        if np.issubdtype(img.dtype, np.uint8):
            img = np.array(img, dtype = np.float64) / 255
        if len(img.shape) == 2:
            img = img.reshape(img.shape + (1,)) + np.zeros((1, 1, 3), dtype=np.float64)
        if img.shape[-1] == 4:
            img = img[:3]
        return img

    def converge(self, centroids, last):
        really_small_number = 1e-8
        dists = np.sqrt(np.sum((centroids - last) ** 2))
        return dists < really_small_number
        

    def cluster(self, image: NDArray[np.float64], colors: int) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        # Performs the image analysis and segments the image into colors
        centroids = np.random.random(size = (colors, 3))
        lastcent = np.zeros((colors, 3), dtype =np.float64)
        while True:
            lastcent = np.array(centroids, dtype = centroids.dtype)
            im = image.reshape(image.shape[0], image.shape[1], 1, image.shape[2])
            cents = centroids.reshape(1, 1, -1, centroids.shape[1])
            dists = np.sqrt(np.sum((im - cents) ** 2, axis = 3))
            categories = np.argmin(dists, axis = 2)
            for i in range(colors):
                centroids[i] = np.average(image[categories == i], axis = 0)
            if self.converge(centroids, lastcent):
                break
        return centroids, categories
