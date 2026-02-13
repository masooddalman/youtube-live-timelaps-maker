"""
Captures a frame from a YouTube live stream at regular intervals.
Uses yt-dlp to get the direct stream URL, then OpenCV to grab frames.
"""

import os
import subprocess
import sys
import time
from datetime import datetime

import cv2

from config import SCREENSHOTS_DIR


def get_stream_url(youtube_url: str) -> str:
    """Use yt-dlp to extract the direct stream URL."""
    result = subprocess.run(
        ["yt-dlp", "-f", "best", "-g", youtube_url],
        capture_output=True, text=True,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp failed:\n{result.stderr}")
    return result.stdout.strip()


def capture_frame(stream_url: str, save_path: str) -> bool:
    """Grab a single frame from the stream and save it."""
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        return False
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return False
    cv2.imwrite(save_path, frame)
    return True


def run(youtube_url: str = None, interval: int = None, on_log=None, stop_flag=None):
    """
    Main capture loop.
      youtube_url : stream URL  (falls back to config)
      interval    : seconds between captures (falls back to config)
      on_log      : callback(str) for log messages
      stop_flag   : callable that returns True when we should stop
    """
    from config import YOUTUBE_URL, CAPTURE_INTERVAL

    youtube_url = youtube_url or YOUTUBE_URL
    interval = interval or CAPTURE_INTERVAL
    log = on_log or print
    should_stop = stop_flag or (lambda: False)

    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    log("Fetching stream URL...")
    stream_url = get_stream_url(youtube_url)
    log("Stream URL obtained.")

    frame_count = 0
    log(f"Capturing every {interval}s. Press Stop to finish.\n")

    while not should_stop():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"frame_{frame_count:05d}_{timestamp}.jpg"
        save_path = os.path.join(SCREENSHOTS_DIR, filename)

        ok = capture_frame(stream_url, save_path)
        if ok:
            frame_count += 1
            log(f"Saved: {filename}  (total: {frame_count})")
        else:
            log("Frame grab failed. Refreshing stream URL...")
            try:
                stream_url = get_stream_url(youtube_url)
            except RuntimeError as e:
                log(str(e))

        # Sleep in small increments so we can react to stop_flag quickly
        for _ in range(interval):
            if should_stop():
                break
            time.sleep(1)

    log(f"\nStopped. Captured {frame_count} frames total.")
    return frame_count


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
