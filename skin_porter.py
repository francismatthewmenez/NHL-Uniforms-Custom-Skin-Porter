import os
import sys
import shutil
from tkinter import Tk, Label, Button, filedialog, messagebox
from PIL import Image

def resource_path(relative_path):
    """Get the absolute path to a resource, whether running from development or a bundled executable."""
    try:
        # When running from a PyInstaller bundle, sys._MEIPASS points to the temp directory
        base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.abspath(".")
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# File paths
mask_path = resource_path("mask.png")  # mask.png in the same directory as the script
jersey_folder = resource_path("jerseys")  # Folder containing jersey templates in the same directory
output_folder = resource_path("NHL Uniforms Skin Pack")  # Output folder in the same directory

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def resize_if_necessary(image):
    """Resize the image to 128x128 if it's 64x64."""
    if image.size == (64, 64):
        image = image.resize((128, 128), Image.NEAREST)
    return image

def apply_mask(image, mask):
    """Apply the mask to the image."""
    mask = mask.convert("L")  # Convert mask to grayscale
    if mask.size != image.size:
        mask = mask.resize(image.size, Image.NEAREST)  # Resize mask to match image size
    return Image.composite(image, Image.new("RGBA", image.size), mask)

def embed_image_in_jerseys(image_path):
    """Embed the selected image into jersey templates."""
    image = Image.open(image_path)
    image = resize_if_necessary(image)
    mask_image = Image.open(mask_path)  # Use the mask from the same folder
    image = apply_mask(image, mask_image)
    jersey_filenames = sorted([f for f in os.listdir(jersey_folder) if f.endswith(".png")])
    for jersey_filename in jersey_filenames:
        jersey_path = os.path.join(jersey_folder, jersey_filename)
        try:
            jersey_skin = Image.open(jersey_path)
            jersey_skin = jersey_skin.convert("RGBA")
            jersey_skin.paste(image, (0, 0), image)
            output_path = os.path.join(output_folder, jersey_filename)
            jersey_skin.save(output_path)
            print(f"Saved: {output_path}")
        except Exception as e:
            print(f"Error processing {jersey_filename}: {e}")

def zip_output_folder():
    """Zip the NHL Uniforms Skin Pack folder and save it on the user's Desktop."""
    home_directory = os.path.expanduser("~")
    desktop_folder = os.path.join(home_directory, "Desktop")
    
    zip_base_name = os.path.join(desktop_folder, "NHL Uniforms Skin Pack")
    zip_filename = zip_base_name + ".zip"
    
    print(f"Zip base name: {zip_base_name}")
    print(f"Zip filename: {zip_filename}")

    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    # Create the zip file and save it to Desktop
    shutil.make_archive(zip_base_name, 'zip', output_folder)
    
    messagebox.showinfo("Success", "Check your _internal folder located in the same folder as the skin_porter.exe file. Your skin pack should be there!")

def select_image():
    """Open a dialog to select an image file and process it."""
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if file_path:
        embed_image_in_jerseys(file_path)
        Label(window, text="Processing Completed!").pack(pady=10)
        Button(window, text="Download Skin Pack", command=zip_output_folder).pack(pady=20)

# Create the GUI window
window = Tk()
window.title("Minecraft Jersey Embedding")
window.geometry("300x250")

Label(window, text="Select the custom skin to embed:").pack(pady=10)
Button(window, text="Choose Image", command=select_image).pack(pady=20)

window.mainloop()
