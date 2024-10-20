import numpy as np
from PIL import Image
import random
import sys
import os
from datetime import datetime

# Default path to load the image
DEFAULT_IMAGE_PATH = "images/outer_glow.png"

def load_image(image_path=None):
    """Load the image from the provided path or default path."""
    if image_path is None:
        image_path = DEFAULT_IMAGE_PATH
    if not os.path.exists(image_path):
        print(f"Image path '{image_path}' not found!")
        sys.exit(1)
    return Image.open(image_path)

def shuffle_pixels(image):
    """Shuffle the pixels of the image."""
    pixels = np.array(image)
    
    # Check if the image has an alpha channel (RGBA) or just RGB
    if pixels.shape[2] == 4:  # RGBA image
        # Separate the RGB channels from the Alpha channel
        rgb_pixels = pixels[:, :, :3]  # Get only the RGB part
        alpha_channel = pixels[:, :, 3]  # Get the alpha channel
        
        # Flatten and shuffle the RGB pixels
        flattened_rgb = rgb_pixels.reshape(-1, 3)
        np.random.shuffle(flattened_rgb)
        
        # Reshape back to original dimensions and re-attach the alpha channel
        shuffled_rgb = flattened_rgb.reshape(rgb_pixels.shape)
        shuffled_pixels = np.dstack((shuffled_rgb, alpha_channel))
    else:  # RGB image
        # Flatten and shuffle the RGB pixels
        flattened_pixels = pixels.reshape(-1, 3)
        np.random.shuffle(flattened_pixels)
        
        # Reshape back to the original dimensions
        shuffled_pixels = flattened_pixels.reshape(pixels.shape)
    
    return shuffled_pixels

def modify_rgb_values(pixels):
    """Modify RGB values by ±1 for each color channel with 20% probability."""
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            # Modify R, G, B values with 20% chance
            for k in range(3):  # Loop over R, G, B channels
                if random.random() < 0.2:
                    # Convert to int to avoid overflow, then apply the change
                    new_value = int(pixels[i, j, k]) + random.choice([-1, 1])
                    # Clip the result to ensure it stays between 0 and 255
                    pixels[i, j, k] = np.clip(new_value, 0, 255)
    return pixels

def special_modify(pixels):
    """Special modification based on the sum of RGB values."""
    has_alpha = pixels.shape[2] == 4  # Check if the image has an alpha channel

    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            if has_alpha:
                r, g, b, a = pixels[i, j]  # Unpack RGBA values
            else:
                r, g, b = pixels[i, j]  # Unpack RGB values

            # Convert to int to avoid overflow when adding
            r, g, b = int(r), int(g), int(b)
            total_rgb = r + g + b
            
            if total_rgb > 750:
                if random.random() < 0.08:
                    r, g, b = [np.clip(channel + random.choice([-1, 1]), 0, 255) for channel in (r, g, b)]
            elif 735 < total_rgb <= 750:
                chance = random.random()
                if chance < 0.05:
                    r, g, b = [np.clip(channel + random.choice([-1, 1]), 0, 255) for channel in (r, g, b)]
                elif chance < 0.08:
                    r, g, b = [np.clip(channel + random.choice([-2, 2]), 0, 255) for channel in (r, g, b)]
            elif 720 < total_rgb <= 735:
                chance = random.random()
                if chance < 0.05:
                    r, g, b = [np.clip(channel + random.choice([-1, 1]), 0, 255) for channel in (r, g, b)]
                elif chance < 0.08:
                    r, g, b = [np.clip(channel + random.choice([-2, 2]), 0, 255) for channel in (r, g, b)]
                elif chance < 0.10:
                    r, g, b = [np.clip(channel + random.choice([-3, 3]), 0, 255) for channel in (r, g, b)]
            elif total_rgb <= 720:
                chance = random.random()
                if chance < 0.05:
                    r, g, b = [np.clip(channel + random.choice([-1, 1]), 0, 255) for channel in (r, g, b)]
                elif chance < 0.08:
                    r, g, b = [np.clip(channel + random.choice([-2, 2]), 0, 255) for channel in (r, g, b)]
                elif chance < 0.11:
                    r, g, b = [np.clip(channel + random.choice([-3, 3]), 0, 255) for channel in (r, g, b)]

            # Reassign the modified RGB values back to the pixel array
            if has_alpha:
                pixels[i, j] = [r, g, b, a]  # Preserve the alpha channel
            else:
                pixels[i, j] = [r, g, b]

    return pixels

def process_image(image_path=None):
    """Main function to process the image."""
    # Load image
    image = load_image(image_path)
    
    # Shuffle pixels
    pixels = shuffle_pixels(image)
    
    # Modify RGB values
    pixels = modify_rgb_values(pixels)
    
    # Special modifications based on R + G + B values
    pixels = special_modify(pixels)
    
    # Create the output directory if it doesn't exist
    output_dir = "./images/restored_images"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{timestamp}_outer_glow_image.png"
    output_path = os.path.join(output_dir, output_filename)
    
    # Save the modified image
    modified_image = Image.fromarray(pixels.astype('uint8'))
    modified_image.save(output_path)
    print(f"Outer glow image saved as '{output_path}'")

if __name__ == "__main__":
    # If an image path is provided via the terminal, use it; otherwise, use the default path
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    process_image(image_path)