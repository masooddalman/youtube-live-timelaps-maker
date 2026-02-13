"""
YouTube Live Timelapse Maker — GUI
"""

import threading
import tkinter as tk
from tkinter import scrolledtext

from capture import run as capture_run
from timelapse import build_timelapse


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("YouTube Live Timelapse Maker")
        self.root.resizable(False, False)

        self._stop = False
        self._thread = None

        # ── URL ──
        tk.Label(root, text="YouTube Live URL:").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        self.url_entry = tk.Entry(root, width=55)
        self.url_entry.insert(0, "https://www.youtube.com/live/GUOwh_AwOcI")
        self.url_entry.grid(row=0, column=1, padx=10, pady=(10, 0))

        # ── Interval ──
        tk.Label(root, text="Interval (seconds):").grid(row=1, column=0, sticky="w", padx=10, pady=(5, 0))
        self.interval_entry = tk.Entry(root, width=55)
        self.interval_entry.insert(0, "180")
        self.interval_entry.grid(row=1, column=1, padx=10, pady=(5, 0))

        # ── Buttons ──
        btn_frame = tk.Frame(root)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.start_btn = tk.Button(btn_frame, text="Start", width=14, bg="#4CAF50", fg="white",
                                   command=self.start)
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = tk.Button(btn_frame, text="Stop & Build", width=14, bg="#f44336", fg="white",
                                  command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        # ── Log ──
        self.log_box = scrolledtext.ScrolledText(root, width=65, height=16, state="disabled",
                                                  font=("Consolas", 9))
        self.log_box.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10))

    # ── helpers ──

    def log(self, msg: str):
        """Thread-safe log to the text box."""
        self.root.after(0, self._append_log, msg)

    def _append_log(self, msg: str):
        self.log_box.config(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    # ── actions ──

    def start(self):
        url = self.url_entry.get().strip()
        if not url:
            self.log("Please enter a YouTube URL.")
            return

        try:
            interval = int(self.interval_entry.get().strip())
            if interval < 1:
                raise ValueError
        except ValueError:
            self.log("Interval must be a positive integer (seconds).")
            return

        self._stop = False
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.url_entry.config(state="disabled")
        self.interval_entry.config(state="disabled")

        self._thread = threading.Thread(target=self._worker, args=(url, interval), daemon=True)
        self._thread.start()

    def stop(self):
        self._stop = True
        self.stop_btn.config(state="disabled")
        self.log("\nStopping capture...")

    def _worker(self, url: str, interval: int):
        try:
            capture_run(
                youtube_url=url,
                interval=interval,
                on_log=self.log,
                stop_flag=lambda: self._stop,
            )
            self.log("\nBuilding timelapse...")
            build_timelapse(on_log=self.log)
            self.log("\nDone!")
        except Exception as e:
            self.log(f"\nError: {e}")
        finally:
            self.root.after(0, self._reset_ui)

    def _reset_ui(self):
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.url_entry.config(state="normal")
        self.interval_entry.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
