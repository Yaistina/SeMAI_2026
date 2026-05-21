import cv2
import numpy as np
from PIL import Image


class SlideSelector:
    def __init__(self, difference_limit=25, crop_area=None, frame_step=10, min_interval=20):
        self.difference_limit = difference_limit
        self.crop_area = crop_area
        self.frame_step = frame_step
        self.min_interval = min_interval

    def find_slides(self, video_path, progress_callback=None):
        video = cv2.VideoCapture(video_path)

        if not video.isOpened():
            return []

        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        success, previous_frame = video.read()

        if not success:
            video.release()
            return []

        slides = [self._to_image(self._crop(previous_frame))]
        last_saved_frame = 0
        frame_index = 0

        while True:
            success, current_frame = video.read()

            if not success:
                break

            frame_index += 1

            if frame_index % self.frame_step != 0:
                continue

            previous_slide = self._crop(previous_frame)
            current_slide = self._crop(current_frame)

            if self._is_new_slide(previous_slide, current_slide):
                if frame_index - last_saved_frame >= self.min_interval:
                    slides.append(self._to_image(current_slide))
                    last_saved_frame = frame_index

            previous_frame = current_frame

            if progress_callback and total_frames > 0:
                progress = int((frame_index / total_frames) * 100)
                progress_callback(progress, len(slides))

        video.release()
        return slides

    def _crop(self, frame):
        if self.crop_area is None:
            return frame

        x, y, width, height = self.crop_area
        return frame[y:y + height, x:x + width]

    def _is_new_slide(self, previous_frame, current_frame):
        previous_small = cv2.resize(previous_frame, (320, 180))
        current_small = cv2.resize(current_frame, (320, 180))

        difference = cv2.absdiff(previous_small, current_small)
        gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

        return np.mean(gray) > self.difference_limit

    def _to_image(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_frame)


class PdfCreator:
    def save(self, images, output_path):
        if not images:
            return False

        images[0].save(output_path, save_all=True, append_images=images[1:])
        return True


class VideoPdfConverter:
    def __init__(self, selector=None, pdf_creator=None):
        self.selector = selector or SlideSelector()
        self.pdf_creator = pdf_creator or PdfCreator()

    def convert(self, video_path, output_path, progress_callback=None):
        slides = self.selector.find_slides(video_path, progress_callback=progress_callback)
        saved = self.pdf_creator.save(slides, output_path)

        return {
            "saved": saved,
            "slides_count": len(slides),
            "output_path": output_path,
        }
