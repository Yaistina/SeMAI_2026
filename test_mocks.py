import unittest

from mocks import MockApplication, MockRecognizer, MockTable


class TestMocks(unittest.TestCase):
    def test_mock_application_updates_progress(self):
        app = MockApplication()

        app.update_progress(50, 2)

        self.assertEqual(app.progress, 50)
        self.assertEqual(app.detected_slides, 2)
        self.assertEqual(app.status, "Processing video... 50%")

    def test_mock_recognizer_returns_slides(self):
        recognizer = MockRecognizer(slides=["slide_a", "slide_b"])

        result = recognizer.find_slides("video.mp4")

        self.assertTrue(recognizer.was_called)
        self.assertEqual(result, ["slide_a", "slide_b"])

    def test_mock_table_adds_rows(self):
        table = MockTable()

        table.add_row({"slide": "slide_1"})
        table.add_row({"slide": "slide_2"})

        self.assertEqual(table.row_count(), 2)

    def test_mock_table_clear(self):
        table = MockTable()

        table.add_row({"slide": "slide_1"})
        table.clear()

        self.assertEqual(table.row_count(), 0)


if __name__ == "__main__":
    unittest.main()
