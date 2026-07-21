# ClipForge

A tiny desktop app for downloading audio or video from the web using [yt-dlp](https://github.com/yt-dlp/yt-dlp), with a simple Tkinter GUI.

Paste a URL, choose **Video** or **Audio only**, pick a format and (for video) a resolution, choose a save folder, and hit **Download**.

## Features
- Video formats: `mp4`, `mkv`, `webm`
- Audio formats: `mp3`, `m4a`, `wav`, `flac`, `opus`, `aac`, `vorbis`
- Resolutions: `144` up to `2160`, plus `best` / `worst`
- Choose your download folder
- Live progress bar and log
- Single Python source file: `ClipForge.py`
- **Windows release is a single, portable `.exe`** — ffmpeg is bundled inside it, nothing else to install

## Download (Windows)

Grab the latest `ClipForge.exe` from the [Releases](../../releases) page. No Python, no ffmpeg, no install — just run it.

## Running from source

### Requirements
- Python 3.8+
- [ffmpeg](https://ffmpeg.org/download.html) installed and available on your system `PATH` (required for audio extraction and merging video/audio). Only needed when running the `.py` directly — the packaged `.exe` already has it embedded.

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/clipforge.git
cd clipforge
pip install yt-dlp
python ClipForge.py
```

## Usage

1. Paste the video URL.
2. Choose **Video** or **Audio only**.
3. Pick a format (and resolution, if video).
4. Choose where to save the file.
5. Click **Download** and watch the progress bar.

## Building the single-file .exe yourself

The repo includes a ready-to-use `ClipForge.spec` for [PyInstaller](https://pyinstaller.org/).

1. Download `ffmpeg.exe` and `ffprobe.exe` (a static Windows build, e.g. from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)) and place them in the repo root, next to `ClipForge.py`.
2. Install build tools:
   ```bash
   pip install pyinstaller yt-dlp
   ```
3. Build:
   ```bash
   pyinstaller ClipForge.spec
   ```
4. The finished binary is at `dist/ClipForge.exe` — a single portable file with ffmpeg embedded inside it.

## Notes
- Tkinter ships with most Python installations. On Linux, if it's missing, install it via your package manager (e.g. `sudo apt install python3-tk`).
- ffmpeg is distributed here under the LGPL (using an LGPL/"shared" build, not a GPL "full" build), so it can be redistributed alongside this project's code. See the [ffmpeg license page](https://ffmpeg.org/legal.html) for details.
- This project is just a GUI wrapper around yt-dlp — it doesn't circumvent DRM or host any content. Downloading material you don't have the rights to may still violate the terms of service of the source site or local copyright law. Use responsibly.

## License
MIT