# YouTube Live Timelapse Maker

A Python desktop app that captures screenshots from a YouTube live stream at regular intervals and compiles them into a timelapse video.

## How It Works

1. Extracts the direct stream URL from a YouTube live link using **yt-dlp**
2. Grabs a frame from the stream at your chosen interval using **OpenCV**
3. Saves each frame as a numbered `.jpg` in the `screenshots/` folder
4. When you stop, it stitches all frames into an `.mp4` timelapse video

If the stream URL expires during a long capture session, it automatically refreshes it.

## Requirements

- Python 3.10+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [OpenCV](https://pypi.org/project/opencv-python/)
- [Pillow](https://pypi.org/project/Pillow/)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the app:

```bash
python main.py
```

A GUI window will open with:

- **YouTube Live URL** — paste any YouTube live stream link
- **Interval (seconds)** — time between each screenshot (default: 180 = 3 minutes)
- **Start** — begins capturing frames
- **Stop & Build** — stops capturing and automatically builds the timelapse video

The output video is saved as `timelapse.mp4` in the project folder.

Also, you don't need to open the youtube livestream :D, just keep the app running and also keep the internet connection. have fun

## Configuration

Default settings can be changed in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `YOUTUBE_URL` | — | Default YouTube live stream URL |
| `CAPTURE_INTERVAL` | `180` | Seconds between each frame |
| `SCREENSHOTS_DIR` | `screenshots` | Folder where frames are saved |
| `TIMELAPSE_FPS` | `30` | Frame rate of the output video |
| `TIMELAPSE_OUTPUT` | `timelapse.mp4` | Output video filename |

## Project Structure

```
youtube-live-timelaps-maker/
├── main.py          # Entry point — launches the GUI
├── capture.py       # Frame capture logic
├── timelapse.py     # Timelapse video compiler
├── config.py        # Default settings
├── requirements.txt # Python dependencies
└── screenshots/     # Captured frames (created automatically)
```
