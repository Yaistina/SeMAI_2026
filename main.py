from converter import SlideSelector, VideoPdfConverter
from settings import CROP_AREA, DIFFERENCE_LIMIT, OUTPUT_PDF, VIDEO_PATH


if __name__ == "__main__":
    selector = SlideSelector(
        difference_limit=DIFFERENCE_LIMIT,
        crop_area=CROP_AREA,
    )
    converter = VideoPdfConverter(selector=selector)
    result = converter.convert(VIDEO_PATH, OUTPUT_PDF)

    print("PDF created:", result["saved"])
    print("Slides:", result["slides_count"])
