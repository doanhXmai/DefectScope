from src.core.config import Settings
from src.utils.file_helper import FileHelper
from src.utils.preprocessor import Preprocessor

if __name__ == "__main__":
    settings = Settings()
    img_1 = FileHelper.read_image(settings.ORIGINAL_IMAGES[1])
    img_2 = FileHelper.read_image(settings.ORIGINAL_IMAGES[2])
    img_3 = FileHelper.read_image(settings.ORIGINAL_IMAGES[3])
    img_4 = FileHelper.read_image(settings.ORIGINAL_IMAGES[4])


    # FileHelper.show_image(img_1, title="Anh 1")
    # FileHelper.show_images([img_1, img_2, img_3, img_4], ["Anh 1", "Anh 2", "Anh 3", "Anh 4"], cols = 2)

    roi_img = Preprocessor.auto_crop_center(img_2)

    gray_img = Preprocessor.to_grayscale(roi_img)

    denoised_img = Preprocessor.remove_noise(gray_img, method="bilateral")

    FileHelper.show_images([img_2, roi_img, gray_img, denoised_img],
                           ["Original Image", "Roi Image", "Gray Image", "Denoised Image"],
                           cols=2)