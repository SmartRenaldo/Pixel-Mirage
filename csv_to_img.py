import os
import pandas as pd
from PIL import Image

# Path to the CSV file
csv_path = "images/csv/6(ps).csv"  # Replace with your CSV file path

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_path, header=None)

# Get the dimensions of the image from the DataFrame
height, width = df.shape

# Create a new image with the same size (RGB mode)
image = Image.new("RGB", (width, height))

# Loop through each row and column to set pixel values
for y in range(height):
    for x in range(width):
        # Extract the RGB string value from the DataFrame, e.g., "(R, G, B)"
        rgb_string = df.iat[y, x]
        
        # Parse the string to get the individual RGB values
        rgb_tuple = tuple(map(int, rgb_string.strip("()").split(", ")))
        
        # Set the pixel in the image
        image.putpixel((x, y), rgb_tuple)
        
# Create the 'restored_images' folder if it doesn't exist
img_folder = "images/restored_images"
os.makedirs(img_folder, exist_ok=True)

# Get the file name without the extension
base_name = os.path.basename(csv_path)
file_name, _ = os.path.splitext(base_name)

# Define the path for the output image
output_image_path = os.path.join(img_folder, f"{file_name}.jpg")

# Save the image
image.save(output_image_path)

print(f"Image saved to: {output_image_path}")
