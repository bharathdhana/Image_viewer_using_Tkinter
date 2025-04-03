import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("800x600")

        self.image_list = []
        self.current_index = 0

        self.label = tk.Label(self.root, text="No Image Selected", font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.canvas = tk.Canvas(self.root, bg="gray")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        self.prev_btn = tk.Button(self.btn_frame, text="Previous", command=self.prev_image, state=tk.DISABLED)
        self.prev_btn.grid(row=0, column=0, padx=5)
        
        self.next_btn = tk.Button(self.btn_frame, text="Next", command=self.next_image, state=tk.DISABLED)
        self.next_btn.grid(row=0, column=1, padx=5)
        
        self.open_btn = tk.Button(self.btn_frame, text="Open Folder", command=self.load_images)
        self.open_btn.grid(row=0, column=2, padx=5)
        
        self.exit_btn = tk.Button(self.btn_frame, text="Exit", command=self.root.quit)
        self.exit_btn.grid(row=0, column=3, padx=5)

    def load_images(self):
        folder_selected = filedialog.askdirectory()
        if not folder_selected:
            return
        
        supported_formats = (".jpg", ".jpeg", ".png", ".bmp")
        self.image_list = [os.path.join(folder_selected, file) for file in os.listdir(folder_selected) if file.lower().endswith(supported_formats)]
        
        if not self.image_list:
            messagebox.showerror("Error", "No supported image files found!")
            return
        
        self.current_index = 0
        self.display_image()
        self.update_buttons()

    def display_image(self):
        image_path = self.image_list[self.current_index]
        img = Image.open(image_path)
        img.thumbnail((self.root.winfo_width(), self.root.winfo_height()))
        self.img_tk = ImageTk.PhotoImage(img)
        
        self.canvas.delete("all")
        self.canvas.create_image(self.root.winfo_width()//2, self.root.winfo_height()//2, anchor=tk.CENTER, image=self.img_tk)
        self.label.config(text=f"{os.path.basename(image_path)}")
        
    def next_image(self):
        if self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            self.display_image()
        self.update_buttons()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_image()
        self.update_buttons()

    def update_buttons(self):
        self.prev_btn.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_index < len(self.image_list) - 1 else tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()
