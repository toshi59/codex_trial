import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox


def convert_mp3_to_mp4(mp3_path: str, mp4_path: str) -> tuple[bool, str]:
    """Convert an MP3 file to MP4 using ffmpeg."""
    try:
        subprocess.run([
            "ffmpeg",
            "-y",  # overwrite output file if it exists
            "-i",
            mp3_path,
            mp4_path,
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True, "Conversion successful."
    except FileNotFoundError:
        return False, "ffmpeg is not installed or not found in PATH."
    except subprocess.CalledProcessError as exc:
        return False, f"Conversion failed: {exc.stderr.decode().strip()}"


def select_mp3():
    path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
    if path:
        mp3_var.set(path)
        # Suggest an output file name based on input
        mp4_var.set(os.path.splitext(path)[0] + ".mp4")


def select_mp4():
    path = filedialog.asksaveasfilename(defaultextension=".mp4",
                                        filetypes=[("MP4 files", "*.mp4")])
    if path:
        mp4_var.set(path)


def convert():
    mp3_path = mp3_var.get()
    mp4_path = mp4_var.get()
    if not mp3_path:
        messagebox.showerror("Error", "Please choose an MP3 file.")
        return
    if not mp4_path:
        messagebox.showerror("Error", "Please specify an output MP4 file.")
        return

    ok, msg = convert_mp3_to_mp4(mp3_path, mp4_path)
    if ok:
        messagebox.showinfo("Success", msg)
    else:
        messagebox.showerror("Error", msg)


# Build UI
root = tk.Tk()
root.title("MP3 to MP4 Converter")

mp3_var = tk.StringVar()
mp4_var = tk.StringVar()

# MP3 selection row
tk.Label(root, text="MP3 file:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
mp3_entry = tk.Entry(root, textvariable=mp3_var, width=40)
mp3_entry.grid(row=0, column=1, padx=5)
tk.Button(root, text="Browse", command=select_mp3).grid(row=0, column=2, padx=5)

# MP4 output row
tk.Label(root, text="Output MP4:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
mp4_entry = tk.Entry(root, textvariable=mp4_var, width=40)
mp4_entry.grid(row=1, column=1, padx=5)
tk.Button(root, text="Browse", command=select_mp4).grid(row=1, column=2, padx=5)

# Convert button
convert_btn = tk.Button(root, text="Convert", command=convert)
convert_btn.grid(row=2, column=1, pady=10)

root.mainloop()
