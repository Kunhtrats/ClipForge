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
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    if os.path.exists(os.path.join(base_dir, "ffmpeg.exe")):
        os.environ["PATH"] = base_dir + os.pathsep + os.environ.get("PATH", "")

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
        self.root.geometry("720x900")
        self.root.minsize(600, 840)
        self.root.configure(bg="#f1f5f9")

        self.output_dir = os.path.join(os.path.expanduser("~"), "Downloads")

        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        self.root.option_add("*Font", "{Segoe UI} 10")
        self.root.option_add("*TCombobox*Listbox.font", "{Segoe UI} 10")
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", foreground="#0f172a")
        style.configure("Muted.TLabel", foreground="#475569")
        style.configure("Heading.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("TButton", padding=(16, 10), background="#eef2ff",
                        foreground="#3730a3", borderwidth=0)
        style.map("TButton", background=[("active", "#e0e7ff")])
        style.configure("Primary.TButton", background="#4f46e5", foreground="white",
                        font=("Segoe UI", 11, "bold"), padding=(16, 14))
        style.map("Primary.TButton", background=[("disabled", "#e2e8f0"),
                  ("pressed", "#3730a3"), ("active", "#4338ca")],
                  foreground=[("disabled", "#475569")])
        style.configure("Mode.TRadiobutton", padding=(18, 12), background="#f1f5f9",
                        foreground="#334155", indicatoron=False)
        style.map("Mode.TRadiobutton", background=[("selected", "#e0e7ff"),
                  ("active", "#eef2ff")], foreground=[("selected", "#3730a3")])
        style.configure("TEntry", padding=10, fieldbackground="white",
                        bordercolor="#cbd5e1", lightcolor="#cbd5e1", darkcolor="#cbd5e1")
        style.map("TEntry", bordercolor=[("focus", "#4f46e5")])
        style.configure("TCombobox", padding=8, arrowsize=16)
        style.map("TCombobox", fieldbackground=[("readonly", "#f8fafc")],
                  foreground=[("disabled", "#64748b"), ("readonly", "#0f172a")])
        style.configure("Horizontal.TProgressbar", background="#4f46e5",
                        troughcolor="#e2e8f0", borderwidth=0, thickness=8)

        header = tk.Frame(self.root, bg="#f1f5f9")
        header.pack(fill="x", padx=28, pady=(24, 18))
        tk.Label(header, text="ClipForge", font=("Segoe UI", 26, "bold"),
                 bg="#f1f5f9", fg="#0f172a").pack(anchor="w")
        tk.Label(header, text="Your favorite content, saved your way.",
                 bg="#f1f5f9", fg="#475569").pack(anchor="w", pady=(4, 0))

        card = ttk.Frame(self.root, padding=24)
        card.pack(fill="x", padx=28)
        ttk.Label(card, text="1  Paste a link", style="Heading.TLabel").pack(anchor="w")
        ttk.Label(card, text="Add the URL of the video you want to save.",
                  style="Muted.TLabel").pack(anchor="w", pady=(4, 10))
        url_row = ttk.Frame(card)
        url_row.pack(fill="x")
        self.url_entry = ttk.Entry(url_row)
        self.url_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(url_row, text="Paste", command=self._paste_url).pack(side="right", padx=(8, 0))

        ttk.Label(card, text="2  Make it yours", style="Heading.TLabel").pack(anchor="w", pady=(24, 10))
        type_frame = ttk.Frame(card)
        type_frame.pack(fill="x")
        self.media_type = tk.StringVar(value="video")
        for value, label in (("video", "Video"), ("audio", "Audio only")):
            ttk.Radiobutton(type_frame, text=label, variable=self.media_type, value=value,
                            style="Mode.TRadiobutton", command=self._refresh_formats).pack(
                                side="left", fill="x", expand=True, padx=(0, 4))

        opts_frame = ttk.Frame(card)
        opts_frame.pack(fill="x", pady=(16, 0))
        opts_frame.columnconfigure((0, 1), weight=1, uniform="options")
        ttk.Label(opts_frame, text="File format").grid(row=0, column=0, sticky="w", pady=(0, 6))
        ttk.Label(opts_frame, text="Video quality").grid(row=0, column=1, sticky="w", pady=(0, 6))
        self.format_var = tk.StringVar(value=VIDEO_FORMATS[0])
        self.format_menu = ttk.Combobox(opts_frame, textvariable=self.format_var,
                                       values=VIDEO_FORMATS, state="readonly", width=12)
        self.format_menu.grid(row=1, column=0, sticky="ew", padx=(0, 12))
        self.res_var = tk.StringVar(value=RESOLUTIONS[0])
        self.res_menu = ttk.Combobox(opts_frame, textvariable=self.res_var,
                                    values=RESOLUTIONS, state="readonly", width=12)
        self.res_menu.grid(row=1, column=1, sticky="ew")
        self.quality_hint = ttk.Label(card, text="Best uses the highest available quality.", style="Muted.TLabel")
        self.quality_hint.pack(anchor="w", pady=(8, 0))

        ttk.Label(card, text="3  Choose a destination", style="Heading.TLabel").pack(anchor="w", pady=(24, 10))
        out_frame = ttk.Frame(card)
        out_frame.pack(fill="x")
        self.out_label = ttk.Label(out_frame, text=self.output_dir, style="Muted.TLabel", anchor="w")
        self.out_label.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.out_label.bind("<Configure>", lambda event: self.out_label.configure(wraplength=max(100, event.width)))
        ttk.Button(out_frame, text="Browse...", command=self._choose_folder).pack(side="right")
        self.download_btn = ttk.Button(card, text="Download", command=self._start_download, style="Primary.TButton")
        self.download_btn.pack(fill="x", pady=(20, 0))

        activity = ttk.Frame(self.root, padding=(24, 18))
        activity.pack(fill="both", expand=True, padx=28, pady=(16, 24))
        ttk.Label(activity, text="Download activity", style="Heading.TLabel").pack(anchor="w")
        self.status_label = ttk.Label(activity, text="Ready when you are. Paste a link to get started.", style="Muted.TLabel")
        self.status_label.pack(fill="x", pady=(8, 12))
        self.status_label.bind("<Configure>", lambda event: self.status_label.configure(wraplength=max(100, event.width)))
        self.progress = ttk.Progressbar(activity, mode="determinate", maximum=100)
        self.progress.pack(fill="x", pady=(0, 12))
        log_frame = ttk.Frame(activity)
        log_frame.pack(fill="both", expand=True)
        self.log_box = tk.Text(log_frame, height=3, width=1, state="disabled", bg="#f8fafc",
                               fg="#475569", relief="flat", padx=10, pady=8, wrap="word",
                               font=("Segoe UI", 9), highlightthickness=1, highlightbackground="#e2e8f0")
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_box.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_box.configure(yscrollcommand=scrollbar.set)
        self.log_box.pack(fill="both", expand=True)
        self.url_entry.focus_set()

    def _paste_url(self):
        try:
            url = self.root.clipboard_get().strip()
        except tk.TclError:
            self.status_label.config(text="Your clipboard is empty. Copy a video link first.")
            return
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, url)
        self.url_entry.focus_set()

    def _refresh_formats(self):
        if self.media_type.get() == "audio":
            self.format_menu["values"] = AUDIO_FORMATS
            self.res_menu.configure(state="disabled")
            self.quality_hint.config(text="Audio only saves the sound, without the video.")
        else:
            self.format_menu["values"] = VIDEO_FORMATS
            self.res_menu.configure(state="readonly")
            self.quality_hint.config(text="Best uses the highest available quality.")
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