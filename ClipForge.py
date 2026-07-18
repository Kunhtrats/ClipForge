#!/usr/bin/env python3
"""
ClipForge - a tiny GUI for yt-dlp
Paste a URL, pick audio or video, pick a format and resolution, and download.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

# If this script is running as a bundled .exe (PyInstaller), and there's an
# ffmpeg.exe sitting next to it, put that folder on PATH so yt-dlp finds it.
if getattr(sys, "frozen", False):
    app_dir = os.path.dirname(sys.executable)
    if os.path.exists(os.path.join(app_dir, "ffmpeg.exe")):
        os.environ["PATH"] = app_dir + os.pathsep + os.environ.get("PATH", "")

AUDIO_FORMATS = ["mp3", "m4a", "wav", "flac", "opus", "aac", "vorbis"]
VIDEO_FORMATS = ["mp4", "mkv", "webm"]
RESOLUTIONS = ["best", "2160", "1440", "1080", "720", "480", "360", "240", "144", "worst"]

# If ffmpeg isn't on your PATH, set its exact folder here, e.g.:
# FFMPEG_LOCATION = r"C:\Users\you\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-full_build\bin"
# Leave as None if `ffmpeg` already works from a terminal.
FFMPEG_LOCATION = None


class ClipForgeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ClipForge")
        self.root.geometry("520x420")
        self.root.resizable(False, False)

        self.output_dir = os.path.join(os.path.expanduser("~"), "Downloads")

        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        pad = {"padx": 12, "pady": 6}

        # URL
        tk.Label(self.root, text="Video URL", anchor="w").pack(fill="x", **pad)
        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack(fill="x", padx=12)

        # Type: audio or video
        type_frame = tk.LabelFrame(self.root, text="Type")
        type_frame.pack(fill="x", **pad)

        self.media_type = tk.StringVar(value="video")
        tk.Radiobutton(type_frame, text="Video", variable=self.media_type,
                        value="video", command=self._refresh_formats).pack(side="left", padx=10, pady=4)
        tk.Radiobutton(type_frame, text="Audio only", variable=self.media_type,
                        value="audio", command=self._refresh_formats).pack(side="left", padx=10, pady=4)

        # Format + resolution
        opts_frame = tk.Frame(self.root)
        opts_frame.pack(fill="x", **pad)

        tk.Label(opts_frame, text="Format").grid(row=0, column=0, sticky="w")
        self.format_var = tk.StringVar()
        self.format_menu = ttk.Combobox(opts_frame, textvariable=self.format_var,
                                         values=VIDEO_FORMATS, state="readonly", width=15)
        self.format_menu.grid(row=1, column=0, padx=(0, 10))
        self.format_menu.current(0)

        tk.Label(opts_frame, text="Resolution (video only)").grid(row=0, column=1, sticky="w")
        self.res_var = tk.StringVar()
        self.res_menu = ttk.Combobox(opts_frame, textvariable=self.res_var,
                                      values=RESOLUTIONS, state="readonly", width=15)
        self.res_menu.grid(row=1, column=1)
        self.res_menu.current(0)

        # Output folder
        out_frame = tk.LabelFrame(self.root, text="Save to")
        out_frame.pack(fill="x", **pad)

        self.out_label = tk.Label(out_frame, text=self.output_dir, anchor="w", fg="gray20")
        self.out_label.pack(side="left", fill="x", expand=True, padx=8, pady=6)
        tk.Button(out_frame, text="Choose...", command=self._choose_folder).pack(side="right", padx=8)

        # Download button
        self.download_btn = tk.Button(self.root, text="Download", command=self._start_download,
                                       bg="#2b6cb0", fg="white", font=("Arial", 11, "bold"))
        self.download_btn.pack(fill="x", padx=12, pady=10, ipady=6)

        # Progress bar + log
        self.progress = ttk.Progressbar(self.root, mode="determinate", maximum=100)
        self.progress.pack(fill="x", padx=12, pady=(0, 6))

        self.status_label = tk.Label(self.root, text="Ready.", anchor="w", fg="gray20")
        self.status_label.pack(fill="x", padx=12)

        self.log_box = tk.Text(self.root, height=6, state="disabled", bg="#f5f5f5")
        self.log_box.pack(fill="both", expand=True, padx=12, pady=8)

    def _refresh_formats(self):
        if self.media_type.get() == "audio":
            self.format_menu["values"] = AUDIO_FORMATS
            self.res_menu.configure(state="disabled")
        else:
            self.format_menu["values"] = VIDEO_FORMATS
            self.res_menu.configure(state="readonly")
        self.format_menu.current(0)

    def _choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_dir)
        if folder:
            self.output_dir = folder
            self.out_label.config(text=folder)

    def _log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    # ---------- Download logic ----------
    def _start_download(self):
        if yt_dlp is None:
            messagebox.showerror("Missing dependency", "yt-dlp is not installed.\nRun: pip install yt-dlp")
            return

        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Please paste a video URL first.")
            return

        self.download_btn.config(state="disabled", text="Downloading...")
        self.progress["value"] = 0
        self.status_label.config(text="Starting...")

        thread = threading.Thread(target=self._download, args=(url,), daemon=True)
        thread.start()

    def _download(self, url):
        media_type = self.media_type.get()
        fmt = self.format_var.get()
        resolution = self.res_var.get()

        ydl_opts = {
            "outtmpl": os.path.join(self.output_dir, "%(title)s.%(ext)s"),
            "progress_hooks": [self._progress_hook],
            "noplaylist": True,
        }

        if FFMPEG_LOCATION:
            ydl_opts["ffmpeg_location"] = FFMPEG_LOCATION

        if media_type == "audio":
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": fmt,
                "preferredquality": "192",
            }]
        else:
            if resolution in ("best", "worst"):
                height_filter = ""
            else:
                height_filter = f"[height<={resolution}]"

            selector = "bestvideo" if resolution != "worst" else "worstvideo"
            audio_selector = "bestaudio" if resolution != "worst" else "worstaudio"
            ydl_opts["format"] = f"{selector}{height_filter}+{audio_selector}/best{height_filter}"
            ydl_opts["merge_output_format"] = fmt

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.root.after(0, self._on_success)
        except Exception as exc:
            self.root.after(0, self._on_error, str(exc))

    def _progress_hook(self, d):
        if d["status"] == "downloading":
            percent_str = d.get("_percent_str", "0%").strip()
            try:
                percent = float(percent_str.replace("%", ""))
            except ValueError:
                percent = 0
            speed = d.get("_speed_str", "").strip()
            eta = d.get("_eta_str", "").strip()
            self.root.after(0, self._update_progress, percent, f"Downloading... {percent_str} ({speed}, ETA {eta})")
        elif d["status"] == "finished":
            self.root.after(0, self._log, "Download finished, processing...")

    def _update_progress(self, percent, text):
        self.progress["value"] = percent
        self.status_label.config(text=text)

    def _on_success(self):
        self.progress["value"] = 100
        self.status_label.config(text="Done!")
        self._log("Saved to " + self.output_dir)
        self.download_btn.config(state="normal", text="Download")
        messagebox.showinfo("Success", "Download complete!")

    def _on_error(self, message):
        self.status_label.config(text="Error.")
        self._log("Error: " + message)
        self.download_btn.config(state="normal", text="Download")
        messagebox.showerror("Download failed", message)


def main():
    root = tk.Tk()
    ClipForgeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()