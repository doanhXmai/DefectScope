import cv2
import numpy as np


class Preprocessor:
    def __init__(self):
        self.clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))

    def preprocess(self, img):
        filtered = cv2.bilateralFilter(img, 9, 75, 75)
        enhanced = self.clahe.apply(filtered)

        _, roi_thresh = cv2.threshold(filtered, 30, 255, cv2.THRESH_BINARY)
        kernel_roi = np.ones((3, 3), np.uint8)
        roi_mask = cv2.erode(roi_thresh, kernel_roi, iterations=3)

        return enhanced, roi_mask