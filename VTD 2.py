import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pathlib import Path

from converter import SlideSelector, PdfCreator, VideoPdfConverter


class VideoToPresentationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to Presentation")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#111827")
        self.root.resizable(False, False)

        self.video_path = tk.StringVar()
        self.output_path = tk.StringVar(value="Presentationauto.pdf")
        self.difference_limit = tk.IntVar(value=25)
        self.frame_step = tk.IntVar(value=10)
        self.status_text = tk.StringVar(value="Ready")
        self.slides_text = tk.StringVar(value="Detected slides: 0")
        self.progress_value = tk.IntVar(value=0)

        self.setup_style()
        self.build_ui()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Main.TFrame", background="#111827")
        style.configure("Card.TFrame", background="#1f2937")

        style.configure(
            "Title.TLabel",
            background="#111827",
            foreground="#f9fafb",
            font=("Segoe UI", 26, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background="#111827",
            foreground="#9ca3af",
            font=("Segoe UI", 11)
        )

        style.configure(
            "CardTitle.TLabel",
            background="#1f2937",
            foreground="#f9fafb",
            font=("Segoe UI", 14, "bold")
        )

        style.configure(
            "Text.TLabel",
            background="#1f2937",
            foreground="#d1d5db",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Status.TLabel",
            background="#1f2937",
            foreground="#93c5fd",
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "Modern.TButton",
            background="#2563eb",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=11,
            borderwidth=0
        )

        style.map("Modern.TButton", background=[("active", "#1d4ed8")])

        style.configure(
            "Secondary.TButton",
            background="#374151",
            foreground="#ffffff",
            font=("Segoe UI", 10),
            padding=8,
            borderwidth=0
        )

        style.map("Secondary.TButton", background=[("active", "#4b5563")])

        style.configure(
            "Horizontal.TProgressbar",
            background="#2563eb",
            troughcolor="#374151",
            bordercolor="#374151",
            lightcolor="#2563eb",
            darkcolor="#2563eb"
        )

    def build_ui(self):
        main = ttk.Frame(self.root, style="Main.TFrame", padding=30)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Video to Presentation", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            main,
            text="Automatic video frame extraction and PDF presentation generation.",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(4, 24))

        content = ttk.Frame(main, style="Main.TFrame")
        content.pack(fill="both", expand=True)

        left_card = ttk.Frame(content, style="Card.TFrame", padding=24)
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 12))

        right_card = ttk.Frame(content, style="Card.TFrame", padding=24)
        right_card.pack(side="right", fill="both", expand=True, padx=(12, 0))

        ttk.Label(left_card, text="Conversion settings", style="CardTitle.TLabel").pack(anchor="w")

        ttk.Label(left_card, text="Video file", style="Text.TLabel").pack(anchor="w", pady=(18, 6))
        video_row = ttk.Frame(left_card, style="Card.TFrame")
        video_row.pack(fill="x")

        ttk.Entry(video_row, textvariable=self.video_path).pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(video_row, text="Browse", style="Secondary.TButton", command=self.browse_video).pack(side="right")

        ttk.Label(left_card, text="Output PDF", style="Text.TLabel").pack(anchor="w", pady=(18, 6))
        ttk.Entry(left_card, textvariable=self.output_path).pack(fill="x")

        ttk.Label(left_card, text="Sensitivity: frame difference limit", style="Text.TLabel").pack(anchor="w", pady=(18, 6))
        ttk.Scale(left_card, from_=5, to=80, variable=self.difference_limit, orient="horizontal").pack(fill="x")

        ttk.Label(left_card, text="Speed: analyze every N frames", style="Text.TLabel").pack(anchor="w", pady=(18, 6))
        ttk.Scale(left_card, from_=1, to=30, variable=self.frame_step, orient="horizontal").pack(fill="x")

        ttk.Button(
            left_card,
            text="Generate presentation",
            style="Modern.TButton",
            command=self.start_conversion_thread
        ).pack(fill="x", pady=(24, 14))

        ttk.Progressbar(
            left_card,
            variable=self.progress_value,
            maximum=100,
            style="Horizontal.TProgressbar"
        ).pack(fill="x", pady=(0, 12))

        ttk.Label(left_card, textvariable=self.status_text, style="Status.TLabel").pack(anchor="w")
        ttk.Label(left_card, textvariable=self.slides_text, style="Text.TLabel").pack(anchor="w", pady=(5, 0))

        ttk.Label(right_card, text="Workflow", style="CardTitle.TLabel").pack(anchor="w")

        steps = [
            ("1", "Select a video file"),
            ("2", "Set output PDF name"),
            ("3", "Adjust detection sensitivity"),
            ("4", "Run automatic frame analysis"),
            ("5", "Export detected slides to PDF")
        ]

        for number, text in steps:
            row = ttk.Frame(right_card, style="Card.TFrame")
            row.pack(fill="x", pady=9)

            badge = tk.Label(row, text=number, bg="#2563eb", fg="white", font=("Segoe UI", 10, "bold"), width=3)
            badge.pack(side="left", padx=(0, 12))

            ttk.Label(row, text=text, style="Text.TLabel", wraplength=260).pack(side="left")

        separator = tk.Frame(right_card, bg="#374151", height=1)
        separator.pack(fill="x", pady=18)

        ttk.Label(right_card, text="How detection works", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))

        explanation = (
            "The program compares consecutive video frames. "
            "If the visual difference is higher than the selected limit, "
            "the frame is considered a new slide and added to the final PDF."
        )

        ttk.Label(right_card, text=explanation, style="Text.TLabel", wraplength=310, justify="left").pack(anchor="w")

    def browse_video(self):
        path = filedialog.askopenfilename(
            title="Select video file",
            filetypes=[("Video files", "*.mp4 *.mov *.avi *.mkv"), ("All files", "*.*")]
        )

        if path:
            self.video_path.set(path)
            self.status_text.set("Video selected")

    def start_conversion_thread(self):
        thread = threading.Thread(target=self.convert_video, daemon=True)
        thread.start()

    def update_progress(self, progress, slides_count):
        self.progress_value.set(progress)
        self.slides_text.set(f"Detected slides: {slides_count}")
        self.status_text.set(f"Processing video... {progress}%")
        self.root.update_idletasks()

    def convert_video(self):
        video_path = self.video_path.get().strip()
        output_path = self.output_path.get().strip()

        if not video_path:
            messagebox.showerror("Error", "Please select a video file.")
            return

        if not Path(video_path).exists():
            messagebox.showerror("Error", "Video file does not exist.")
            return

        if not output_path:
            output_path = "video_to_presentation.pdf"

        if not output_path.lower().endswith(".pdf"):
            output_path += ".pdf"

        self.progress_value.set(0)
        self.slides_text.set("Detected slides: 0")
        self.status_text.set("Starting conversion...")

        selector = SlideSelector(
            difference_limit=self.difference_limit.get(),
            frame_step=self.frame_step.get(),
            min_interval=20
        )

        converter = VideoPdfConverter(selector=selector, pdf_creator=PdfCreator())

        result = converter.convert(
            video_path=video_path,
            output_path=output_path,
            progress_callback=self.update_progress
        )

        if result["saved"]:
            self.progress_value.set(100)
            self.status_text.set("PDF presentation created")
            self.slides_text.set(f"Detected slides: {result['slides_count']}")

            messagebox.showinfo(
                "Completed",
                f"Presentation created successfully:\n{result['output_path']}\nSlides: {result['slides_count']}"
            )
        else:
            self.status_text.set("No slides detected")
            messagebox.showwarning("Result", "No slides were detected. Try lowering the difference limit.")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToPresentationApp(root)
    root.mainloop()
