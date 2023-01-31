from typing import Generator, Iterable, Any
import numpy as np
from numpy.typing import NDArray
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import cv2 as cv

# Use multiprocessing. This makes things significantly faster
from multiprocessing import Process, Queue

from math import floor, log, sqrt

from tikzpaint.figures import Drawable, Displayable
from tikzpaint.util import Coordinates, copy, Number
from tikzpaint.shapes.base import L0Path

pi = 3.1415926535
e = 2.7182818284
eps = 1e-5

# Returns true if stuff converges
def Converge(centroids, last):
    really_small_number = 0.01
    dists = np.sqrt(np.sum((centroids - last) ** 2))
    return dists < really_small_number

# Main algorithm for clustering
def cluster(image: NDArray[np.float64], centroids: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.int64]]:
    K = centroids.shape[0]    
    last = np.zeros_like(centroids, dtype = centroids.dtype)
    categories = np.ones_like(image, dtype = np.int64)
    
    max_iterations = floor(log(image.shape[0] * image.shape[1]))

    for i in range(max_iterations):
        # print(f"Running k means, {np.sqrt(np.sum((centroids - last) ** 2))}")
        last = np.array(centroids, dtype = centroids.dtype)
        im = image.reshape(image.shape[0], image.shape[1], 1, image.shape[2])
        cents = centroids.reshape(1, 1, -1, centroids.shape[1])
        dists = np.sqrt(np.sum((im - cents) ** 2, axis = 3))
        categories = np.argmin(dists, axis = 2)
        for i in range(K):
            centroids[i] = np.average(image[categories == i], axis = 0)
        if Converge(centroids, last):
            break

    return centroids, categories

def sum_intra_cluster_distance(centroids, image, categories):
    K = len(centroids)
    sum: float = 0.
    for i in range(K):
        im = image[categories == i]
        dists = np.sqrt(np.sum((im - centroids[i]) ** 2, axis = 1))
        sum += float(np.sum(dists))
    return sum

def get_centroid(image: NDArray, K: int, seed: int = 42069):
    np.random.seed(seed)
    return image[np.random.choice(image.shape[0], size=K, replace=False), np.random.choice(image.shape[1], size=K, replace=False)]

# Define the atom task for multiprocessing. You don't need to understand this in 2211
def task(image: NDArray[np.float64], centroids: NDArray[np.float64], history: Queue):
    K = len(centroids)
    centroids, categories = cluster(image, centroids)
    hist = (K, sum_intra_cluster_distance(centroids, image, categories))
    history.put(hist)
    
def determine_best_k(img: NDArray, min_K: int = 3, max_K: int = 10, downscale: int = 10):
    # Determines the best K for the K means clustering
    # First downscale the image for easy processing
    R, C, _ = img.shape
    image = np.array(img[::downscale, ::downscale, :])
    processes: list[Process] = []
    history = Queue(max_K - min_K)
    for K in range(min_K, max_K):
        centroids = get_centroid(image, K)
        p = Process(target = task, args = (image, centroids, history))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    hist_list = [history.get() for _ in range(history.qsize())]
    # We are looking via the elbow method for the biggest change in "change". Hence the second derivative
    H = [s[1] for s in sorted(hist_list)]
    dH = [H[k] - H[k + 1] for k in range(len(H) - 1)]
    d2H = [dH[k] - dH[k + 1] for k in range(len(dH) - 1)]
    max_idx = int(np.argmax(d2H))
    return max_idx + min_K + 1

# For debug
def display_segmented_image(image, categories, centroids, K):
    image_copy = np.array(image, dtype = image.dtype)
    for i in range(K):
        image_copy[categories == i] = centroids[i]
    plt.figure()
    plt.imshow(image_copy)
    plt.show()
    print("This uses only the following colors:")
    plt.figure()
    plt.imshow(centroids.reshape((1,) + centroids.shape))
    plt.show()

# Get value of pixel with error checking
def pixel_in(img: NDArray[np.float64], i: int, j: int) -> float:
    if i >= img.shape[0]:
        return pixel_in(img, img.shape[0] - 1, j)
    if i < 0:
        return pixel_in(img, 0, j)
    if j >= img.shape[1]:
        return pixel_in(img, i, img.shape[1] - 1)
    if j < 0:
        return pixel_in(img, i, 0)
    return float(img[i, j, :])

# Value of pixel with linear interpolation
def value_in(pixels: NDArray[np.float64], x: float, y: float):
    j = floor(x - 0.5)
    tj = x - 0.5 - j
    i = floor(y - 0.5)
    ti = y - 0.5 - i
    interpolated = pixel_in(pixels, i, j) * (1 - ti) * (1 - tj) + pixel_in(pixels, i, j+1) * (1 - ti) * (tj) + pixel_in(pixels, i+1, j+1) * (ti) * (tj) + pixel_in(pixels, i+1, j) * (ti) * (1 - tj)
    return float(interpolated)

def gradient(pixels: NDArray[np.float64], x: float, y: float):
    newx = (value_in(pixels, x + eps, y) - value_in(pixels, x, y)) / eps
    newy = (value_in(pixels, x, y + eps) - value_in(pixels, x, y)) / eps
    return (float(newx), float(newy))

# Distance of point from the contour line
def gradient_shift(pixels: NDArray[np.float64], threshold, x: float, y: float):
    gx, gy = gradient(pixels, x, y)
    g_norm = sqrt(gx * gx + gy * gy)
    d = threshold - value_in(pixels, x, y)
    return (gx * d / g_norm / g_norm, gy * d / g_norm / g_norm)

# Iterative algorithm to bring a point closer to the contour line
def fit_point_better(pixels: NDArray[np.float64], threshold: float, point: tuple[float, float]) -> tuple[float, float]:
    if abs(value_in(pixels, point[0], point[1]) - threshold) < 1/255:
        return point
    hx, hy = gradient_shift(pixels, threshold, point[0], point[1])
    new_point = (point[0] + hx, point[1] + hy)
    return fit_point_better(pixels, threshold, new_point)



class Image(Drawable):
    def __init__(self, img_path: str, color_accuracy: int = -1):
        """Implementation of an image that can be drawn in SVG and TeX. Inherently, we can only display so many colors before the code gets ridiculous, So color_accuracy defines the number of colors you want. Default is 5"""
        # Perform the clustering algorithm and store the paths on initialization
        image = mpimg.imread(img_path)
        image = self.preprocess(image)
        
        # Determine best K and perform clustering
        if color_accuracy < 0:
            downscale_factor = max(image.shape[0]//300, image.shape[1]//300)
            color_accuracy = determine_best_k(image, downscale = downscale_factor)
        centroids = get_centroid(image, color_accuracy)
        colors, labels = cluster(image, centroids)
        display_segmented_image(image, labels, colors, color_accuracy)
        
        #
        pass
    
    def preprocess(self, img: NDArray) -> NDArray[np.float64]:
        if np.issubdtype(img.dtype, np.uint8):
            img = np.array(img, dtype = np.float64) / 255
        if len(img.shape) == 2:
            img = img.reshape(img.shape + (1,)) + np.zeros((1, 1, 3), dtype=np.float64)
        if img.shape[-1] == 4:
            img = img[:3]
        return img

    def draw(self) -> Generator[Displayable, None, None]:
        return super().draw()
    
if __name__ == "__main__":
    path = "C:/Users/User/Desktop/20221102_151817.jpg"
    im = Image(path, 9)