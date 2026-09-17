# 🎬 ClipForge

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/Kunhtrats/clipforge/releases)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/Kunhtrats/clipforge)

> 🚀 Modern, beautiful desktop app for downloading audio and video using [yt-dlp](https://github.com/yt-dlp/yt-dlp)

Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern, customizable Tkinter UI.

---

## ✨ Features

- 🎥 **Video formats**: mp4, mkv, webm
- 🎵 **Audio formats**: mp3, m4a, wav, flac, opus, aac, vorbis
- 📐 **Resolutions**: 144p to 4K (2160p), plus `best`/`worst`
- 📂 **Custom save location**
- 📊 **Live progress** with speed and ETA
- 🪵 **Activity log**
- 🎨 **Modern UI** with CustomTkinter
- 💻 **Cross-platform**: Windows, macOS, Linux

---

## 📦 Installation

### Option 1: Download executable (Windows)

Grab the latest `ClipForge.exe` from [**Releases**](../../releases) - portable, no install needed.

### Option 2: Run from source

**Requirements:**
- Python 3.8+
- [ffmpeg](https://ffmpeg.org/download.html) on your system PATH

```bash
git clone https://github.com/Kunhtrats/clipforge.git
cd clipforge
pip install -r requirements.txt
python -m clipforge.app
```

---

## 🎯 Usage

1. 📋 **Paste** a video URL (YouTube, Twitter, etc.)
2. 🔘 Choose **Video** or **Audio Only**
3. ⚙️ Pick format and resolution
4. 📁 Select save location
5. ⬇️ Click **Download** and watch the magic happen

---

## 🏗️ Build from source

### Package as executable (PyInstaller)

```bash
pip install pyinstaller customtkinter yt-dlp

# Windows
pyinstaller --onefile --windowed --add-data "ffmpeg.exe;." --name ClipForge clipforge/app.py

# macOS/Linux
pyinstaller --onefile --windowed --add-data "ffmpeg:." --name ClipForge clipforge/app.py
```

Output: `dist/ClipForge.exe` (or `ClipForge` on Unix)

---

## 📂 Project Structure

```
clipforge/
├── clipforge/
│   ├── __init__.py
│   └── app.py          # Main application
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🔧 Tech Stack

- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Modern Tkinter UI
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Video/audio download engine
- **[ffmpeg](https://ffmpeg.org)** - Media processing

---

## ⚖️ Legal

- ✅ MIT License - free to use, modify, distribute
- ⚠️ ClipForge is a GUI wrapper for yt-dlp
- 🚫 Does not circumvent DRM or host content
- ⚠️ Downloading copyrighted material without permission may violate terms of service or laws in your jurisdiction
- 📜 Use responsibly and respect content creators' rights

---

## 📄 License

[MIT License](LICENSE) © 2026 Miguel Alarcón

---

## 🙏 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerhouse behind downloads
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Beautiful modern UI
- [ffmpeg](https://ffmpeg.org) - Media processing (LGPL)

---

**Made with ❤️ and Python**