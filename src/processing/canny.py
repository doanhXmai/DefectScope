import cv2
import numpy as np


class CannyDetector:
    def __init__(self, sigma=0.33):
        self.sigma = sigma

    def detect(self, enhanced_img, roi_mask):
        v = np.median(enhanced_img)
        lower = int(max(0, (1.0 - self.sigma) * v))
        upper = int(min(255, (1.0 + self.sigma) * v))

        edges = cv2.Canny(enhanced_img, lower, upper)
        edges_masked = cv2.bitwise_and(edges, edges, mask=roi_mask)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 3))
        edges_closed = cv2.morphologyEx(edges_masked, cv2.MORPH_CLOSE, kernel)

        return edges_masked, edges_closed