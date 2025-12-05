import cv2

from src.processing.canny import CannyDetector
from src.processing.preprocessor import Preprocessor
from src.processing.scan_errors import ScanErrors
from src.utils.file_helper import FileHelper

from src.utils.log import ConsoleLogger as cl

class App:
    def __init__(self):
        self.pre = Preprocessor()
        self.canny = CannyDetector()
        self.scanner = ScanErrors()
        self.results = []
        self.results_img = {}

    def process(self, image_path):
        img = FileHelper.read_image(image_path)
        if img is None:
            cl.info(f"Không tìm thấy file: {image_path}")
            return

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 1. Preprocess
        enhanced, roi_mask = self.pre.preprocess(img_gray)

        # 2. Canny detector
        edges_masked, edges_closed = self.canny.detect(enhanced, roi_mask)

        # 3. Classification
        img_out, c_crack, c_poro = self.scanner.scan_and_draw(img_gray, edges_closed)

        imgs = {
            "Original": img,
            "Gray": img_gray,
            "Edges": edges_masked,
            f"Results_{c_poro}(Porosity_Red)-{c_crack}_(Crack_Yellow)": img_out
        }

        return imgs, img_out

    def _results(self, paths):
        for path in paths:
            imgs, result = self.process(path)
            self.results.append(imgs)
            self.results_img[path] = result

    def run_app(self, paths):
        self._results(paths)

    def show_results(self):
        for result in self.results:
            FileHelper.show_images(result, cols=1)

    def save_results(self):
        for key in self.results_img:
            new_path = key.replace("original", "processed")
            if FileHelper.save_image(self.results_img[key], new_path):
                cl.info("Đã lưu ảnh thành công!")
            else:
                cl.warn("Lưu ảnh thất bại!")