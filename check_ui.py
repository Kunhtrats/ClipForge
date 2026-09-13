"""Run with python check_ui.py; no network requests or downloads."""
import tkinter as tk
from unittest.mock import patch

from ClipForge import AUDIO_FORMATS, VIDEO_FORMATS, ClipForgeApp


root = tk.Tk()
try:
    app = ClipForgeApp(root)
    root.update()
    assert app.format_var.get() == VIDEO_FORMATS[0]
    app.media_type.set("audio")
    app._refresh_formats()
    assert tuple(app.format_menu["values"]) == tuple(AUDIO_FORMATS)
    assert str(app.res_menu["state"]) == "disabled"
    app.media_type.set("video")
    app._refresh_formats()
    assert str(app.res_menu["state"]) == "readonly"
    assert app.format_var.get() == VIDEO_FORMATS[0]
    with patch.object(root, "clipboard_get", return_value=" https://example.com/video "):
        app._paste_url()
    assert app.url_entry.get() == "https://example.com/video"
    with patch.object(root, "clipboard_get", side_effect=tk.TclError):
        app._paste_url()
    assert "clipboard is empty" in app.status_label["text"]
    app._update_progress(42, "Downloading: 42%")
    assert app.progress["value"] == 42
    app._log("UI check passed")
    assert "UI check passed" in app.log_box.get("1.0", "end")
    for size in ("600x840", "720x900", "1000x950"):
        root.geometry(size)
        root.update()
        assert app.log_box.winfo_height() > 20, size
        assert app.log_box.winfo_rooty() + app.log_box.winfo_height() <= root.winfo_rooty() + root.winfo_height(), size
    print("UI checks passed (modes, clipboard, progress, log, resizing).")
finally:
    root.destroy()