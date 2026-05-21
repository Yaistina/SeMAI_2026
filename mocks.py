"""
Mocks for Video to Presentation project.

Task:
Implement mocks for classes Application, Recognizer, Table.
"""


class MockApplication:
    """
    Mock version of the main application class.

    It imitates the GUI application without opening a real interface.
    """

    def __init__(self):
        self.video_path = "test_video.mp4"
        self.output_path = "test_presentation.pdf"
        self.difference_limit = 25
        self.frame_step = 10
        self.status = "Ready"
        self.progress = 0
        self.detected_slides = 0

    def select_video(self, path):
        self.video_path = path
        self.status = "Video selected"

    def set_output_path(self, path):
        self.output_path = path

    def update_progress(self, progress, slides_count):
        self.progress = progress
        self.detected_slides = slides_count
        self.status = f"Processing video... {progress}%"

    def show_success(self):
        self.status = "PDF presentation created"

    def show_error(self, message):
        self.status = f"Error: {message}"


class MockRecognizer:
    """
    Mock version of the recognizer class.

    In the real project this role is performed by SlideSelector.
    This mock returns prepared slides instead of analyzing a real video.
    """

    def __init__(self, slides=None):
        self.slides = slides or ["slide_1", "slide_2", "slide_3"]
        self.was_called = False

    def find_slides(self, video_path, progress_callback=None):
        self.was_called = True

        if progress_callback:
            progress_callback(30, 1)
            progress_callback(70, 2)
            progress_callback(100, len(self.slides))

        return self.slides

    def recognize(self, video_path):
        self.was_called = True
        return self.slides


class MockTable:
    """
    Mock version of a table component.

    It imitates a table where detected slides or conversion results
    can be displayed.
    """

    def __init__(self):
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def remove_row(self, index):
        if 0 <= index < len(self.rows):
            self.rows.pop(index)

    def clear(self):
        self.rows = []

    def get_rows(self):
        return self.rows

    def row_count(self):
        return len(self.rows)


def demo():
    app = MockApplication()
    recognizer = MockRecognizer()
    table = MockTable()

    app.select_video("lecture_video.mp4")

    slides = recognizer.find_slides(
        app.video_path,
        progress_callback=app.update_progress
    )

    for index, slide in enumerate(slides, start=1):
        table.add_row({
            "number": index,
            "slide": slide,
            "status": "detected"
        })

    app.show_success()

    print("Application status:", app.status)
    print("Recognizer called:", recognizer.was_called)
    print("Table rows:", table.get_rows())


if __name__ == "__main__":
    demo()
