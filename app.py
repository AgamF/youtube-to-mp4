# imports the GUI library
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import threading

# initializes the app
window = Tk()
window.title("YouTube to mp4 converter")

# Sets the window boundaries
frame = ttk.Frame(window, padding=100)
frame.grid()

# sets the window dimensions
window_width = 650
window_height = 350

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Sets the windows contents
ttk.Label(frame, text="Enter a YouTube video link:").grid(column=0, row=0)
url_entry = ttk.Entry(frame, width=50)
url_entry.grid(column=0, row=1, pady=10)

# Folder selection
folder_path = StringVar()

def choose_folder():
    path = filedialog.askdirectory()
    if path:
        folder_path.set(path)

ttk.Button(frame, text="Choose Folder", command=choose_folder).grid(column=0, row=2)
ttk.Label(frame, textvariable=folder_path).grid(column=1, row=2)

# Status label
status_label = ttk.Label(frame, text="")
status_label.grid(column=0, row=4, columnspan=2)

progress = ttk.Progressbar(frame, orient='horizontal', length=400, mode='determinate')
progress.grid(column=0, row=5, columnspan=2, pady=10)

# Validation
def is_youtube_url(url):
    return "youtube.com" in url or "youtu.be" in url

def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)

        if total:
            percent = downloaded / total * 100
            progress['value'] = percent
            status_label.config(text=f"Downloading... {percent:.1f}%")
            window.update_idletasks()

    elif d['status'] == 'finished':
        progress['value'] = 100
        status_label.config(text="Processing file...")
        window.update_idletasks()

# Download function
def download_video():
    progress["value"] = 0
    url = url_entry.get()

    if not is_youtube_url(url):
        messagebox.showerror("Error", "Please enter a valid YouTube URL")
        return

    if not folder_path.get():
        messagebox.showerror("Error", "Please select a download folder")
        return

    try:
        status_label.config(text="Downloading...")

        ydl_opts = {
            'format': 'mp4',
            'outtmpl': os.path.join(folder_path.get(), '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        status_label.config(text="Download complete!")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="Download failed")

# Buttons
ttk.Button(frame, text="Convert", command=lambda: threading.Thread(target=download_video).start()).grid(column=0, row=3, pady=10)
ttk.Button(frame, text="Quit", command=window.destroy).grid(column=0, row=4)

window.mainloop()