import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import os

class CropApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Cropper 2")

        self.images = []
        self.crop_box = None

        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(fill=tk.X)

        tk.Button(self.btn_frame, text="Select Images", command=self.load_images).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="Apply Crop", command=self.apply_crop).pack(side=tk.LEFT)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.start_x = self.start_y = 0
        self.rect = None
        self.tk_img = None
        self.preview_path = None

    def load_images(self):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        self.images = filedialog.askopenfilenames(filetypes=filetypes)
        if not self.images:
            return

        # Load and scale down first image for preview
        self.preview_path = self.images[0]
        img = Image.open(self.preview_path)
        self.orig_width, self.orig_height = img.size

        # Compute scale factor to fit screen
        screen_w = self.root.winfo_screenwidth() - 200
        screen_h = self.root.winfo_screenheight() - 200
        scale = min(screen_w / img.width, screen_h / img.height, 1.0)
        self.scale = scale

        disp_size = (int(img.width * scale), int(img.height * scale))
        disp_img = img.resize(disp_size)

        self.tk_img = ImageTk.PhotoImage(disp_img)
        self.canvas.config(width=disp_img.width, height=disp_img.height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        self.crop_box = (int(x1), int(y1), int(x2), int(y2))

    def apply_crop(self):
        if not self.crop_box:
            messagebox.showwarning("No crop", "Please draw a crop box first!")
            return

        # Convert from display coords to original image coords
        x1, y1, x2, y2 = self.crop_box
        scale = 1 / self.scale
        x1, y1, x2, y2 = [int(v * scale) for v in (x1, y1, x2, y2)]

        width, height = x2 - x1, y2 - y1

        out_dir = filedialog.askdirectory(title="Select Output Folder")
        if not out_dir:
            return

        for img_path in self.images:
            filename = os.path.basename(img_path)
            out_path = os.path.join(out_dir, filename)
            subprocess.run([
                "magick", "convert", img_path,
                "-crop", f"{width}x{height}+{x1}+{y1}",
                out_path
            ])

        messagebox.showinfo("Done", "Cropped images saved!")


def main():
    root = tk.Tk()
    app = CropApp(root)
    root.mainloop()
