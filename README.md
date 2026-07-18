# ClipForge

A tiny, single-file desktop app for downloading audio or video from the web using [yt-dlp](https://github.com/yt-dlp/yt-dlp), with a simple Tkinter GUI.

Paste a URL, choose **Video** or **Audio only**, pick a format and (for video) a resolution, choose a save folder, and hit **Download**.

## Features
- Video formats: `mp4`, `mkv`, `webm`
- Audio formats: `mp3`, `m4a`, `wav`, `flac`, `opus`, `aac`, `vorbis`
- Resolutions: `144` up to `2160`, plus `best` / `worst`
- Choose your download folder
- Live progress bar and log
- Everything in one file: `clipforge.py`

## Requirements
- Python 3.8+
- [ffmpeg](https://ffmpeg.org/download.html) installed and available on your system `PATH` (required for audio extraction and merging video/audio)

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/clipforge.git
cd clipforge
pip install yt-dlp
```

## Usage

```bash
python clipforge.py
```

1. Paste the video URL.
2. Choose **Video** or **Audio only**.
3. Pick a format (and resolution, if video).
4. Choose where to save the file.
5. Click **Download** and watch the progress bar.

## Notes
- Tkinter ships with most Python installations. On Linux, if it's missing, install it via your package manager (e.g. `sudo apt install python3-tk`).
- Downloading content you don't have the rights to may violate the terms of service of the source site or local copyright law. Use responsibly.

## License
MIT