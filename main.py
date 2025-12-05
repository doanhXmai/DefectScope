from src.app import App
from src.core.config import Settings

if __name__ == "__main__":
    app = App()
    settings = Settings()

    image_files = [
        settings.ORIGINAL_IMAGES[1],
        # settings.ORIGINAL_IMAGES[2],
        # settings.ORIGINAL_IMAGES[3],
        # settings.ORIGINAL_IMAGES[4]
    ]

    app.run_app(image_files)

    app.show_results()
    # app.save_results()