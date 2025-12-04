import cv2
import numpy as np
from src.utils.log import ConsoleLogger as cl


class Preprocessor:
    """
    Class chịu trách nhiệm tiền xử lý ảnh mối hàn:
    - Chuyển xám (Grayscale)
    - Khử nhiễu (Denoise)
    - Cắt vùng quan tâm (ROI Clipping)
    """

    @staticmethod
    def to_grayscale(img: np.ndarray) -> np.ndarray:
        """Chuyển ảnh sang thang độ xám."""
        try:
            if len(img.shape) == 2:
                cl.warn("Image is already grayscale.")
                return img

            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return gray_img
        except Exception as e:
            cl.error(f"Error converting to grayscale: {e}")
            return img

    @staticmethod
    def remove_noise(img: np.ndarray, method: str = "gaussian", ksize: int = 5) -> np.ndarray:
        """
        Khử nhiễu ảnh.
        - method="gaussian": Làm mờ nhẹ, giảm nhiễu hạt (nhanh).
        - method="bilateral": Giữ lại cạnh (edges) tốt hơn nhưng chậm hơn (tốt cho vết nứt).
        """
        try:
            if method == "gaussian":
                # ksize phải là số lẻ (3, 5, 7...)
                return cv2.GaussianBlur(img, (ksize, ksize), 0)

            elif method == "bilateral":
                # Giữ cạnh sắc nét, khử nhiễu bề mặt kim loại
                return cv2.bilateralFilter(img, 9, 75, 75)

            else:
                cl.warn(f"Unknown denoise method '{method}'. Using original.")
                return img
        except Exception as e:
            cl.error(f"Error removing noise: {e}")
            return img

    @staticmethod
    def crop_roi(img: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
        """
        Cắt vùng quan tâm (ROI) dựa trên tọa độ hình chữ nhật.
        """
        try:
            h_img, w_img = img.shape[:2]

            # Kiểm tra tọa độ hợp lệ
            if x < 0 or y < 0 or x + w > w_img or y + h > h_img:
                cl.warn(f"ROI coordinates out of bounds: {x},{y},{w},{h}. Returning original.")
                return img

            roi = img[y:y + h, x:x + w]
            cl.debug(f"Cropped ROI: {w}x{h}")
            return roi
        except Exception as e:
            cl.error(f"Error cropping ROI: {e}")
            return img

    @staticmethod
    def auto_crop_center(img: np.ndarray, scale: float = 0.8) -> np.ndarray:
        """
        Tự động cắt vùng trung tâm ảnh (giữ lại scale% kích thước).
        Hữu ích nếu mối hàn luôn nằm ở giữa.
        """
        h, w = img.shape[:2]
        new_w, new_h = int(w * scale), int(h * scale)
        start_x = (w - new_w) // 2
        start_y = (h - new_h) // 2

        return Preprocessor.crop_roi(img, start_x, start_y, new_w, new_h)