# YouTube Live Timelapse Maker

**[فارسی](README.fa.md)** | English

![Banner](assets/banner.png)

A Python desktop app that captures screenshots from multiple YouTube live streams simultaneously at regular intervals and compiles them into timelapse videos. Perfect for monitoring multiple streams or creating time-lapse content from live broadcasts.

## Features

- **Multi-stream support** — capture from unlimited YouTube live streams concurrently
- **Custom naming** — name each stream for organized output
- **Independent controls** — start, stop, and build each stream separately
- **Live activity log** — monitor all streams in real-time
- **Auto URL refresh** — handles stream URL expiration automatically
- **Organized output** — separate folders for screenshots and videos

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

### 1. Install Python

Download and install Python 3.10 or newer from the official website:

https://www.python.org/downloads/

> **Windows users:** Make sure to check **"Add Python to PATH"** during installation.

To verify the installation, open a terminal and run:

```bash
python --version
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the app:

```bash
python main.py
```

### Multi-Stream Interface

The app opens with a split-panel interface:

**Left Panel (Streams):**
- Click **"➕ Add Stream"** to add more streams
- Each stream has:
  - **URL** — paste the YouTube live stream link
  - **Name** — custom name for the stream (used for folders/files)
  - **Interval** — seconds between screenshots (default: 180)
  - **Status** — real-time status indicator
  - **Start/Stop** — independent capture controls
  - **Build** — compile captured frames into a timelapse
  - **Remove** — delete the stream from the list

**Right Panel (Activity Log):**
- Live activity feed showing all stream operations
- Each log entry is tagged with the stream name

### Output Structure

For a stream named `my_stream`:
- Screenshots: `screenshots/my_stream/`
- Video: `output/timelapse_my_stream.mp4`

> **Note:** You don't need to open the YouTube livestream in a browser. Just keep the app running with an active internet connection.

## Configuration

Default settings can be changed in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `YOUTUBE_URL` | — | Default YouTube live stream URL |
| `CAPTURE_INTERVAL` | `180` | Seconds between each frame |
| `SCREENSHOTS_DIR` | `screenshots` | Folder where frames are saved |
| `TIMELAPSE_FPS` | `30` | Frame rate of the output video |
| `TIMELAPSE_OUTPUT` | `timelapse.mp4` | Output video filename |

## Screenshots

### Main Interface
![Main UI](assets/appUI.png)
*Multi-stream manager with activity log*

## Project Structure

```
youtube-live-timelaps-maker/
├── main.py          # Entry point — launches the GUI
├── capture.py       # Frame capture logic
├── timelapse.py     # Timelapse video compiler
├── config.py        # Default settings
├── requirements.txt # Python dependencies
├── screenshots/     # Captured frames (auto-created)
│   ├── stream_1/    # Frames for stream 1
│   └── stream_2/    # Frames for stream 2
└── output/          # Compiled timelapse videos (auto-created)
    ├── timelapse_stream_1.mp4
    └── timelapse_stream_2.mp4
```
