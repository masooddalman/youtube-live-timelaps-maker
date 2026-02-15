"""
Compiles all captured screenshots into a timelapse video.
"""

import os
import cv2

from config import SCREENSHOTS_DIR, TIMELAPSE_FPS, TIMELAPSE_OUTPUT


def build_timelapse(screenshots_dir: str = None, output_path: str = None, on_log=None):
    log = on_log or print

    screenshots_dir = screenshots_dir or SCREENSHOTS_DIR
    output_path = output_path or TIMELAPSE_OUTPUT

    if not os.path.exists(screenshots_dir):
        log(f"Directory not found: {screenshots_dir}")
        return

    files = sorted([
        f for f in os.listdir(screenshots_dir)
        if f.startswith("frame_") and f.endswith(".jpg")
    ])

    if not files:
        log("No frames found — nothing to build.")
        return

    log(f"Found {len(files)} frames. Building timelapse...")

    first = cv2.imread(os.path.join(screenshots_dir, files[0]))
    height, width = first.shape[:2]

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, TIMELAPSE_FPS, (width, height))

    for fname in files:
        frame = cv2.imread(os.path.join(screenshots_dir, fname))
        if frame is None:
            continue
        if frame.shape[:2] != (height, width):
            frame = cv2.resize(frame, (width, height))
        out.write(frame)

    out.release()

    duration = len(files) / TIMELAPSE_FPS
    log(f"Timelapse saved: {output_path}  ({duration:.1f}s at {TIMELAPSE_FPS} FPS)")


if __name__ == "__main__":
    build_timelapse()
