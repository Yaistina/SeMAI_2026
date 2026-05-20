import cv2
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pathlib import Path


class VideoToPresentation:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to Presentation")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#111827")

        self.video_path = tk.StringVar()
        self.output_path = tk.StringVar(value="Presentation.pdf")
        self.status_text = tk.StringVar(value="Ready")
        self.saved_text = tk.StringVar(value="Saved slides: 0")

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
            font=("Segoe UI", 24, "bold")
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
            font=("Segoe UI", 13, "bold")
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
            padding=10,
            borderwidth=0
        )

        style.map(
            "Modern.TButton",
            background=[("active", "#1d4ed8")]
        )

        style.configure(
            "Secondary.TButton",
            background="#374151",
            foreground="#ffffff",
            font=("Segoe UI", 10),
            padding=8,
            borderwidth=0
        )

        style.map(
            "Secondary.TButton",
            background=[("active", "#4b5563")]
        )

    def build_ui(self):
        main = ttk.Frame(self.root, style="Main.TFrame", padding=28)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Video to Presentation", style="Title.TLabel").pack(anchor="w")

        ttk.Label(
            main,
            text="Convert useful video frames into a clean PDF presentation.",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(4, 24))

        content = ttk.Frame(main, style="Main.TFrame")
        content.pack(fill="both", expand=True)

        left_card = ttk.Frame(content, style="Card.TFrame", padding=22)
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 12))

        right_card = ttk.Frame(content, style="Card.TFrame", padding=22)
        right_card.pack(side="right", fill="both", expand=True, padx=(12, 0))

        ttk.Label(left_card, text="Project settings", style="CardTitle.TLabel").pack(anchor="w")

        ttk.Label(left_card, text="Video file", style="Text.TLabel").pack(anchor="w", pady=(18, 6))

        row = ttk.Frame(left_card, style="Card.TFrame")
        row.pack(fill="x")

        ttk.Entry(row, textvariable=self.video_path).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8)
        )

        ttk.Button(
            row,
            text="Browse",
            style="Secondary.TButton",
            command=self.browse_video
        ).pack(side="right")

        ttk.Label(left_card, text="Output PDF", style="Text.TLabel").pack(anchor="w", pady=(18, 6))

        ttk.Entry(left_card, textvariable=self.output_path).pack(fill="x")

        ttk.Button(
            left_card,
            text="Start extraction",
            style="Modern.TButton",
            command=self.start_extraction
        ).pack(fill="x", pady=(26, 12))

        ttk.Label(left_card, textvariable=self.status_text, style="Status.TLabel").pack(anchor="w")
        ttk.Label(left_card, textvariable=self.saved_text, style="Text.TLabel").pack(anchor="w", pady=(5, 0))

        ttk.Label(right_card, text="Workflow", style="CardTitle.TLabel").pack(anchor="w")

        workflow = [
            ("1", "Select video file"),
            ("2", "Choose slide area"),
            ("3", "Preview extracted region"),
            ("4", "Save important frames"),
            ("5", "Generate PDF presentation")
        ]

        for number, text in workflow:
            item = ttk.Frame(right_card, style="Card.TFrame")
            item.pack(fill="x", pady=8)

            badge = tk.Label(
                item,
                text=number,
                bg="#2563eb",
                fg="white",
                font=("Segoe UI", 10, "bold"),
                width=3
            )
            badge.pack(side="left", padx=(0, 12))

            ttk.Label(item, text=text, style="Text.TLabel").pack(side="left")

        separator = tk.Frame(right_card, bg="#374151", height=1)
        separator.pack(fill="x", pady=18)

        ttk.Label(right_card, text="Controls", style="CardTitle.TLabel").pack(anchor="w")

        ttk.Label(right_card, text="Mouse click — select 4 points", style="Text.TLabel").pack(anchor="w", pady=4)
        ttk.Label(right_card, text="S — save current frame", style="Text.TLabel").pack(anchor="w", pady=4)
        ttk.Label(right_card, text="Q — finish and export PDF", style="Text.TLabel").pack(anchor="w", pady=4)

    def browse_video(self):
        path = filedialog.askopenfilename(
            title="Select video file",
            filetypes=[
                ("Video files", "*.mp4 *.mov *.avi *.mkv"),
                ("All files", "*.*")
            ]
        )

        if path:
            self.video_path.set(path)
            self.status_text.set("Video selected")

    def start_extraction(self):
        path = self.video_path.get().strip()
        output = self.output_path.get().strip()

        if not path:
            messagebox.showerror("Error", "Please select a video file.")
            return

        if not Path(path).exists():
            messagebox.showerror("Error", "Video file does not exist.")
            return

        if not output.lower().endswith(".pdf"):
            output += ".pdf"

        self.status_text.set("Opening video...")
        self.root.update()

        video = cv2.VideoCapture(path)

        if not video.isOpened():
            messagebox.showerror("Error", "Cannot open video.")
            return

        ret, first_frame = video.read()

        if not ret:
            messagebox.showerror("Error", "Cannot read first frame.")
            video.release()
            return

        points = []
        images = []

        def click(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
                points.append([x, y])

                cv2.circle(first_frame, (x, y), 7, (0, 0, 255), -1)

                cv2.putText(
                    first_frame,
                    str(len(points)),
                    (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

                cv2.imshow("Select slide area", first_frame)

        cv2.imshow("Select slide area", first_frame)
        cv2.setMouseCallback("Select slide area", click)

        self.status_text.set("Select 4 points around the slide area")
        self.root.update()

        while len(points) < 4:
            cv2.imshow("Select slide area", first_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                video.release()
                cv2.destroyAllWindows()
                return

        x1 = min(p[0] for p in points)
        y1 = min(p[1] for p in points)
        x2 = max(p[0] for p in points)
        y2 = max(p[1] for p in points)

        self.status_text.set("Preview running")
        self.root.update()

        while True:
            ret, frame = video.read()

            if not ret:
                break

            slide = frame[y1:y2, x1:x2]

            cv2.imshow("Preview | S = save | Q = finish", slide)

            key = cv2.waitKey(30) & 0xFF

            if key == ord("s"):
                rgb = cv2.cvtColor(slide, cv2.COLOR_BGR2RGB)
                images.append(Image.fromarray(rgb))

                self.saved_text.set(f"Saved slides: {len(images)}")
                self.status_text.set("Slide saved")
                self.root.update()

            elif key == ord("q"):
                break

        video.release()
        cv2.destroyAllWindows()

        if len(images) == 0:
            messagebox.showwarning(
                "No slides",
                "No slides were saved.\nPress S during preview."
            )
            self.status_text.set("No slides saved")
            return

        images[0].save(
            output,
            save_all=True,
            append_images=images[1:]
        )

        self.status_text.set("PDF presentation created")

        messagebox.showinfo(
            "Completed",
            f"Presentation created successfully:\n{output}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToPresentation(root)
    root.mainloop()
