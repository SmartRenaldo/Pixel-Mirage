import os
from PIL import Image
import pandas as pd
import random
import argparse
import numpy as np

# Setup argument parser
parser = argparse.ArgumentParser(description="Convert an image to a CSV file of RGB values.")
parser.add_argument('--path', type=str, default="images/6(ps).png", help='Path to the image file (optional)')

# Parse arguments
args = parser.parse_args()

# Path to the image file (provided as an argument or default)
image_path = args.path

# Load the image (supports RGBA mode for transparency)
image = Image.open(image_path).convert("RGBA")

# Get the size of the image
width, height = image.size

# Prepare data storage for pixels by group and for transparent pixels
groups = {i: [] for i in range(1, 11)}  # 10 groups for non-transparent pixels
group_positions = {i: [] for i in range(1, 11)}  # Store original positions of each group
transparent_pixels = []  # Store transparent pixel positions and values

# Group criteria based on r+g+b
group_criteria = [(0, 60), (61, 140), (141, 220), (221, 300), (301, 380), (381, 460), (461, 540), (541, 620), (621, 700), (701, float('inf'))]

# Function to determine which group a pixel belongs to based on its r+g+b sum
def get_group(rgb_sum):
    for i, (low, high) in enumerate(group_criteria, 1):
        if low <= rgb_sum <= high:
            return i
    return None  # This should not happen, but added for safety

# Loop through each pixel to get its color values and group them
for y in range(height):
    for x in range(width):
        r, g, b, a = image.getpixel((x, y))
        
        # Check if the pixel is transparent (alpha less than 255)
        if a < 255:
            transparent_pixels.append(((x, y), (r, g, b, a)))  # Store position and value
            continue  # Skip further processing for this pixel
        
        # Sum the RGB values for grouping
        rgb_sum = r + g + b
        
        # Assign the pixel to the appropriate group based on the RGB sum
        group = get_group(rgb_sum)
        groups[group].append((r, g, b))
        group_positions[group].append((x, y))

# Function to adjust pixel values with 20% chance of +1/-1 change
def adjust_pixel(r, g, b):
    def adjust_value(value):
        chance = random.random()
        if chance < 0.2:  # 20% chance to adjust
            return max(0, min(255, value + random.choice([-1, 1])))
        return value  # 80% chance to remain the same
    
    return adjust_value(r), adjust_value(g), adjust_value(b)

# Shuffle, rearrange, and apply random adjustments to each group
def process_group(group, group_position):
    # Shuffle pixels
    random.shuffle(group)
    
    # Apply adjustments to pixels
    adjusted_group = []
    for r, g, b in group:
        new_r, new_g, new_b = adjust_pixel(r, g, b)
        adjusted_group.append((new_r, new_g, new_b))
    
    # Place the rearranged and adjusted pixels back in their original positions
    for i, (x, y) in enumerate(group_position):
        image.putpixel((x, y), (*adjusted_group[i], 255))  # Add alpha as 255 for opaque pixels

# Process each group
for group_num in range(1, 11):
    process_group(groups[group_num], group_positions[group_num])

# Restore transparent pixels in their original positions
for (x, y), (r, g, b, a) in transparent_pixels:
    image.putpixel((x, y), (r, g, b, a))  # Keep the original transparent pixel as it is

# Save the modified image
output_image_path = f"images/restored_images/{os.path.splitext(os.path.basename(image_path))[0]}_modified.png"
image.save(output_image_path)
print(f"Modified image saved to: {output_image_path}")
