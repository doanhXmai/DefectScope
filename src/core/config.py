import os
from functools import lru_cache


class Settings:
    ORIGINAL = r"data/original/"
    PROCESSED = r"data/processed/"
    CUSTOM = r"data/custom/"

    @property
    def ORIGINAL_IMAGES(self):
        valid_extensions = (".jpg", ".png", ".jpeg")
        files = [
            f for f in os.listdir(self.ORIGINAL)
            if f.startswith("anh_") and f.endswith(valid_extensions)
        ]

        files_sorted = sorted(
            files, key=lambda x: int(x.split('_')[1].split('.')[0])
        )

        full_paths = [os.path.join(self.ORIGINAL, f) for f in files_sorted]

        return [None] + full_paths

    @property
    def PROCESSED_IMAGES(self):
        files = [
            f for f in os.listdir(self.PROCESSED)
            if f.startswith("anh_") and f.endswith(".jpg")
        ]

        files_sorted = sorted(
            files, key=lambda x: int(x.split('_')[1].split('.')[0])
        )

        full_paths = [os.path.join(self.PROCESSED, f) for f in files_sorted]

        return [None] + full_paths


@lru_cache
def get_setting() -> Settings:
    return Settings()