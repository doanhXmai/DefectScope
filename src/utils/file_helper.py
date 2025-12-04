import cv2
import os
import matplotlib.pyplot as plt
from typing import List, Optional
import numpy as np
from src.utils.log import ConsoleLogger as cl

class FileHelper:
    @staticmethod
    def read_image(path: str) -> Optional[np.ndarray]:
        if not os.path.exists(path):
            cl.error(f"File not found: {path}")
            return None
        try:
            img = cv2.imread(path)
            if img is None:
                cl.error(f"Failed to read image format: {path}")
                return None
            cl.info(f"Read image successfully: {path} | Shape: {img.shape}")
            return img
        except Exception as e:
            cl.error(f"Error reading image {path}: {e}")
            return None

    @staticmethod
    def save_image(img: np.ndarray, path: str) -> bool:
        try:
            folder = os.path.dirname(path)
            if folder and not os.path.exists(folder):
                os.makedirs(folder)
                cl.info(f"Created directory: {folder}")

            success = cv2.imwrite(path, img)
            if success:
                cl.info(f"Saved image to: {path}")
                return True
            else:
                cl.error(f"Failed to save image to: {path}")
                return False
        except Exception as e:
            cl.error(f"Error saving image {path}: {e}")
            return False

    @staticmethod
    def show_image(img: np.ndarray, title: str = "Image"):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        plt.figure(figsize=(8, 6))
        plt.imshow(img_rgb)
        plt.title(title)
        plt.axis("off")
        plt.show()
        cl.info(f"Displaying image: {title}")

    @staticmethod
    def show_images(images: List[np.ndarray], titles: Optional[List[str]] = None, cols: int = 3):
        if not images:
            cl.warn("No images to display.")
            return

        n_images = len(images)
        rows = (n_images // cols) + (1 if n_images % cols > 0 else 0)

        plt.figure(figsize=(5 * cols, 5 * rows))

        for i, img in enumerate(images):
            if img is None:
                continue

            plt.subplot(rows, cols, i + 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.imshow(img_rgb)

            if titles and i < len(titles):
                plt.title(titles[i])
            else:
                plt.title(f"Image {i+1}")

            plt.axis("off")

        plt.tight_layout()
        plt.show()
        cl.info(f"Displayed {n_images} images in grid")