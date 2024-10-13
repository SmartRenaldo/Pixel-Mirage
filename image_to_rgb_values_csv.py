import os
from PIL import Image
import pandas as pd
import argparse

# Setup argument parser
parser = argparse.ArgumentParser(description="Convert an image to a CSV file of RGB values.")
parser.add_argument('--path', type=str, default="images/6(ps).png", help='Path to the image file (optional)')

# Parse arguments
args = parser.parse_args()

# Path to the image file (provided as an argument or default)
image_path = args.path

# Load the image
image = Image.open(image_path)

# Convert the image to RGB mode
rgb_image = image.convert("RGBA")

# Get the size of the image
width, height = rgb_image.size

# Prepare data storage for pixels
data = []

# Loop through each pixel to get its color values
for y in range(height):
    row = []
    for x in range(width):
        # Get the RGB values of the pixel at (x, y)
        r, g, b, a = rgb_image.getpixel((x, y))
        
        # Check if the pixel is fully transparent (empty)
        if a == 0:
            row.append("T")
        # Otherwise, store the RGB values
        else:
            row.append(f"({r}, {g}, {b})")
    data.append(row)

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Create the 'csv' folder if it doesn't exist
csv_folder = "images/csv"
os.makedirs(csv_folder, exist_ok=True)

# Get the file name without the extension
base_name = os.path.basename(image_path)
file_name, _ = os.path.splitext(base_name)

# Define the path for the CSV file
csv_path = os.path.join(csv_folder, f"{file_name}.csv")

# Save to CSV file
df.to_csv(csv_path, index=False, header=False)

print(f"CSV file saved to: {csv_path}")

# Optionally, save to Excel
# df.to_excel("pixel_colors.xlsx", index=False, header=False)
