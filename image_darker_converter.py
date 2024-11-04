from PIL import Image
import os
from datetime import datetime
import random

def process_image(input_image_path):
    # Load the image
    img = Image.open(input_image_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size

    # Process each pixel
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]

            # Skip transparent pixels
            if a == 0:
                continue

            # Decrease R, G, B values by 15, with a lower limit of 0
            r = max(r - 15, 0)
            g = max(g - 15, 0)
            b = max(b - 15, 0)

            # If all R, G, B values are zero, apply the probability-based change
            if r == 0 and g == 0 and b == 0:
                chance = random.randint(1, 100)
                if chance <= 3:
                    r, g, b = 1, 1, 1
                elif chance <= 5:
                    r, g, b = 2, 2, 2
                elif chance <= 7:
                    r, g, b = 3, 3, 3

            # Update pixel with new color
            pixels[x, y] = (r, g, b, a)

    # Save the processed image
    output_dir = "./images/restored_images"
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    source_image_name = os.path.basename(input_image_path).split('.')[0]
    output_path = os.path.join(output_dir, f"{timestamp}_{source_image_name}_darker.png")

    # Save the image
    img.save(output_path)
    print(f"Image saved to {output_path}")

# Example usage:
process_image("images/Distinction7.png")
