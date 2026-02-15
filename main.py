"""
YouTube Live Timelapse Maker — Multi-Stream GUI
"""

import os
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext

from capture import run as capture_run
from timelapse import build_timelapse


class StreamRow:
    """Represents one stream in the UI"""

    def __init__(self, parent, stream_id: int, on_remove):
        self.stream_id = stream_id
        self.on_remove = on_remove
        self._stop = False
        self._thread = None

        # Container frame
        self.frame = tk.Frame(parent, relief=tk.RIDGE, borderwidth=2, padx=5, pady=5)

        # Stream ID label
        tk.Label(self.frame, text=f"Stream {stream_id}", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky="w", padx=5
        )

        # URL
        tk.Label(self.frame, text="URL:").grid(row=1, column=0, sticky="w", padx=5)
        self.url_entry = tk.Entry(self.frame, width=50)
        self.url_entry.insert(0, "https://www.youtube.com/live/")
        self.url_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=2)

        # Interval
        tk.Label(self.frame, text="Interval (s):").grid(row=2, column=0, sticky="w", padx=5)
        self.interval_entry = tk.Entry(self.frame, width=10)
        self.interval_entry.insert(0, "180")
        self.interval_entry.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        # Status
        tk.Label(self.frame, text="Status:").grid(row=2, column=2, sticky="e", padx=5)
        self.status_label = tk.Label(self.frame, text="Idle", fg="gray", font=("Arial", 9))
        self.status_label.grid(row=2, column=3, sticky="w", padx=5)

        # Buttons
        btn_frame = tk.Frame(self.frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=5)

        self.start_btn = tk.Button(btn_frame, text="Start", width=10, bg="#4CAF50", fg="white",
                                   command=self.start)
        self.start_btn.pack(side="left", padx=3)

        self.stop_btn = tk.Button(btn_frame, text="Stop", width=10, bg="#f44336", fg="white",
                                 command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=3)

        self.build_btn = tk.Button(btn_frame, text="Build", width=10, bg="#2196F3", fg="white",
                                  command=self.build)
        self.build_btn.pack(side="left", padx=3)

        self.remove_btn = tk.Button(btn_frame, text="Remove", width=10, bg="#9E9E9E", fg="white",
                                   command=self.remove)
        self.remove_btn.pack(side="left", padx=3)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def destroy(self):
        if self._thread and self._thread.is_alive():
            self._stop = True
        self.frame.destroy()

    def set_status(self, text: str, color: str = "black"):
        self.status_label.config(text=text, fg=color)

    def get_screenshots_dir(self):
        return f"screenshots/stream_{self.stream_id}"

    def get_output_path(self):
        return f"timelapse_stream_{self.stream_id}.mp4"

    # Actions

    def start(self):
        url = self.url_entry.get().strip()
        if not url:
            self.set_status("Error: No URL", "red")
            return

        try:
            interval = int(self.interval_entry.get().strip())
            if interval < 1:
                raise ValueError
        except ValueError:
            self.set_status("Error: Invalid interval", "red")
            return

        self._stop = False
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.url_entry.config(state="disabled")
        self.interval_entry.config(state="disabled")
        self.remove_btn.config(state="disabled")

        self.set_status("Starting...", "orange")

        self._thread = threading.Thread(
            target=self._worker,
            args=(url, interval),
            daemon=True
        )
        self._thread.start()

    def stop(self):
        self._stop = True
        self.stop_btn.config(state="disabled")
        self.set_status("Stopping...", "orange")

    def build(self):
        self.set_status("Building...", "blue")
        threading.Thread(target=self._build_worker, daemon=True).start()

    def remove(self):
        self.on_remove(self)

    def _worker(self, url: str, interval: int):
        try:
            screenshots_dir = self.get_screenshots_dir()

            def log(msg):
                # We could add a per-stream log if needed
                pass

            capture_run(
                youtube_url=url,
                interval=interval,
                screenshots_dir=screenshots_dir,
                on_log=log,
                stop_flag=lambda: self._stop,
            )

            self.set_status("Stopped", "gray")
        except Exception as e:
            self.set_status(f"Error: {str(e)[:30]}", "red")
        finally:
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.url_entry.config(state="normal")
            self.interval_entry.config(state="normal")
            self.remove_btn.config(state="normal")

    def _build_worker(self):
        try:
            screenshots_dir = self.get_screenshots_dir()
            output_path = self.get_output_path()

            def log(msg):
                pass

            build_timelapse(
                screenshots_dir=screenshots_dir,
                output_path=output_path,
                on_log=log
            )

            self.set_status("Build complete", "green")
        except Exception as e:
            self.set_status(f"Build error: {str(e)[:20]}", "red")


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("YouTube Live Timelapse Maker — Multi-Stream")
        self.root.geometry("650x600")

        self.streams = []
        self.next_id = 1

        # Header
        header = tk.Frame(root, bg="#1976D2", padx=10, pady=10)
        header.pack(fill="x")

        tk.Label(header, text="YouTube Live Timelapse Maker", bg="#1976D2", fg="white",
                font=("Arial", 14, "bold")).pack()
        tk.Label(header, text="Multi-Stream Manager", bg="#1976D2", fg="white",
                font=("Arial", 10)).pack()

        # Add Stream button
        btn_frame = tk.Frame(root, padx=10, pady=10)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="➕ Add Stream", width=15, bg="#4CAF50", fg="white",
                 font=("Arial", 10, "bold"), command=self.add_stream).pack(side="left")

        # Scrollable stream container
        canvas = tk.Canvas(root, highlightthickness=0)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

        self.stream_container = tk.Frame(canvas)

        self.stream_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.stream_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Add one default stream
        self.add_stream()

    def add_stream(self):
        stream = StreamRow(self.stream_container, self.next_id, self.remove_stream)
        stream.pack(fill="x", pady=5)
        self.streams.append(stream)
        self.next_id += 1

    def remove_stream(self, stream: StreamRow):
        if len(self.streams) == 1:
            # Don't allow removing the last stream
            return

        stream.destroy()
        self.streams.remove(stream)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
