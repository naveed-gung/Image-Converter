import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import threading

app = TkinterDnD.Tk()
app.geometry("600x750")
app.title("Image Converter & Resizer")
app.config(bg="#1e1e2e")

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

def toggle_theme():
    if ctk.get_appearance_mode() == "dark":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

theme_btn = ctk.CTkButton(app, text="🌙/☀️", command=toggle_theme, corner_radius=10)
theme_btn.pack(pady=5)

image_paths = []  
img_preview_label = None
progress_bar = None

def select_images():
    global image_paths
    image_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
    if image_paths:
        show_preview(image_paths[0])  
        file_label.configure(text=f"{len(image_paths)} images selected")

def show_preview(img_path):
    global img_preview_label
    img = Image.open(img_path)
    img.thumbnail((250, 250))  
    img_tk = ImageTk.PhotoImage(img)

    if img_preview_label:
        img_preview_label.destroy()  

    img_preview_label = ctk.CTkLabel(app, image=img_tk, text="")
    img_preview_label.image = img_tk
    img_preview_label.pack(pady=10)

def convert_and_resize():
    threading.Thread(target=process_images, daemon=True).start()

def process_images():
    global progress_bar
    
    if not image_paths:
        file_label.configure(text="⚠️ No images selected!", text_color="red")
        return

    output_format = format_var.get()
    new_width = int(width_entry.get())
    new_height = int(height_entry.get())
    output_name = name_entry.get().strip()
    
    total_images = len(image_paths)
    progress_bar.set(0)

    try:
        for idx, img_path in enumerate(image_paths):
            img = Image.open(img_path)
            img_resized = img.resize((new_width, new_height))
            
            base_dir = os.path.dirname(img_path)
            filename = f"{output_name}_{idx + 1}.{output_format.lower()}" if total_images > 1 else f"{output_name}.{output_format.lower()}"
            new_image_path = os.path.join(base_dir, filename)

            img_resized.save(new_image_path, output_format.upper())
            
            progress_bar.set((idx + 1) / total_images)  

        status_label.configure(text=f"✅ {total_images} images saved!", text_color="green")
    except Exception as e:
        status_label.configure(text=f"⚠️ Error: {e}", text_color="red")

def drop_file(event):
    global image_paths
    dropped_files = event.data.strip("{}").split()
    image_paths = [file for file in dropped_files if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))]
    
    if image_paths:
        show_preview(image_paths[0])
        file_label.configure(text=f"{len(image_paths)} images selected")

def close_app():
    app.destroy()

def toggle_fullscreen():
    app.attributes("-fullscreen", not app.attributes("-fullscreen"))

def minimize():
    app.iconify()

control_frame = ctk.CTkFrame(app, fg_color="transparent")
control_frame.pack(fill="x", padx=10, pady=5)

close_btn = ctk.CTkButton(control_frame, text="✖", width=30, command=close_app, fg_color="red", corner_radius=10)
close_btn.pack(side="right", padx=5)
fullscreen_btn = ctk.CTkButton(control_frame, text="⬜", width=30, command=toggle_fullscreen, corner_radius=10)
fullscreen_btn.pack(side="right", padx=5)
minimize_btn = ctk.CTkButton(control_frame, text="➖", width=30, command=minimize, corner_radius=10)
minimize_btn.pack(side="right", padx=5)

file_label = ctk.CTkLabel(app, text="Drag & Drop Images or Select", font=("Arial", 14))
file_label.pack(pady=10)
select_btn = ctk.CTkButton(app, text="Browse Images", command=select_images, corner_radius=15)
select_btn.pack(pady=10)

width_label = ctk.CTkLabel(app, text="Width:", font=("Arial", 12))
width_label.pack()
width_entry = ctk.CTkEntry(app, placeholder_text="Enter width")
width_entry.pack(pady=5)
height_label = ctk.CTkLabel(app, text="Height:", font=("Arial", 12))
height_label.pack()
height_entry = ctk.CTkEntry(app, placeholder_text="Enter height")
height_entry.pack(pady=5)

format_label = ctk.CTkLabel(app, text="Select Format:", font=("Arial", 12))
format_label.pack(pady=5)
format_var = ctk.StringVar(value="png")
format_menu = ctk.CTkOptionMenu(app, variable=format_var, values=["jpg", "png", "bmp"])
format_menu.pack(pady=5)

name_label = ctk.CTkLabel(app, text="Output File Name:", font=("Arial", 12))
name_label.pack()
name_entry = ctk.CTkEntry(app, placeholder_text="Enter file name")
name_entry.pack(pady=5)

convert_btn = ctk.CTkButton(app, text="Convert & Resize", command=convert_and_resize, corner_radius=15)
convert_btn.pack(pady=20)

progress_bar = ctk.CTkProgressBar(app)
progress_bar.pack(pady=10)
progress_bar.set(0)

status_label = ctk.CTkLabel(app, text="", font=("Arial", 12))
status_label.pack(pady=10)

app.drop_target_register(DND_FILES)
app.dnd_bind("<<Drop>>", drop_file)

app.mainloop()
