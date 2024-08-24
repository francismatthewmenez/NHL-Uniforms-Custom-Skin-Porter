import os
import shutil
from PIL import Image

# Hardcoded paths for mask, jersey folder, and output folder (all within the same directory as this script)
mask_path = "mask.png"
jersey_folder = "jerseys"  # Folder containing jersey templates
output_folder = "NHL Uniforms Skin Pack"  # Folder to save the output files

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def create_transparent_mask(mask_path):
    """Create a mask where white areas become transparent and other areas are ignored."""
    mask = Image.open(mask_path).convert("RGBA")
    mask_data = mask.getdata()

    new_mask_data = []
    for item in mask_data:
        # If the pixel is white (R, G, B > 200), make it fully transparent
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            new_mask_data.append((0, 0, 0, 0))  # Transparent
        else:
            new_mask_data.append((0, 0, 0, 255))  # Opaque black

    mask.putdata(new_mask_data)
    return mask

def apply_mask_to_image(image, mask):
    """Apply the transparent mask to an image, ignoring non-white areas in the mask."""
    image_data = image.getdata()
    mask_data = mask.getdata()

    new_image_data = []
    for img_pixel, mask_pixel in zip(image_data, mask_data):
        # If the mask pixel is transparent, set the corresponding image pixel to transparent
        if mask_pixel[3] == 0:  # Alpha channel is 0 (fully transparent)
            new_image_data.append((0, 0, 0, 0))  # Transparent
        else:
            new_image_data.append(img_pixel)  # Keep the original image pixel

    image.putdata(new_image_data)
    return image

def process_jerseys():
    # Load the mask image
    mask_image = create_transparent_mask(mask_path)

    # Get a sorted list of jersey filenames
    jersey_filenames = sorted([f for f in os.listdir(jersey_folder) if f.endswith(".png")])

    # Iterate over all the jersey templates and apply the mask
    for jersey_filename in jersey_filenames:
        jersey_path = os.path.join(jersey_folder, jersey_filename)
        try:
            jersey_image = Image.open(jersey_path).convert("RGBA")
            
            # Apply the mask to the jersey image
            processed_image = apply_mask_to_image(jersey_image, mask_image)
            
            # Save the processed image with the original jersey name
            output_path = os.path.join(output_folder, jersey_filename)
            processed_image.save(output_path)
            print(f"Saved: {output_path}")

        except Exception as e:
            print(f"Error processing {jersey_filename}: {e}")

def zip_output_folder():
    """Zip the NHL Uniforms Skin Pack folder and save it in the user's Downloads folder."""
    # Get the user's home directory
    home_directory = os.path.expanduser("~")
    
    # Construct the path to the Downloads folder
    downloads_folder = os.path.join(home_directory, "Downloads")
    
    # Construct the zip file path in the Downloads folder
    zip_filename = os.path.join(downloads_folder, output_folder + ".zip")
    
    # Remove the previous ZIP file if it exists
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    # Zip the output folder and save it to the Downloads folder
    shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', output_folder)
    
    print(f"Your skin pack has been zipped and saved to {zip_filename}!")

# Process the jerseys and zip the output folder
process_jerseys()
zip_output_folder()
