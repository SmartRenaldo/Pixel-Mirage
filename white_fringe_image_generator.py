import os
from PIL import Image
import numpy as np
import random
from datetime import datetime  # Import datetime module

# Step 1: Load the image
def load_image(image_path):
    img = Image.open(image_path)
    return img

# Step 2: Calculate RGB probabilities
def calculate_rgb_probabilities(image):
    # Convert image to RGB and get the pixel data
    image = image.convert("RGB")
    pixels = np.array(image)
    
    # Flatten the pixel array to separate R, G, B channels
    r_values = pixels[:, :, 0].flatten()
    g_values = pixels[:, :, 1].flatten()
    b_values = pixels[:, :, 2].flatten()
    
    # Calculate probabilities for each channel
    total_pixels = len(r_values)
    r_prob = np.bincount(r_values, minlength=256) / total_pixels
    g_prob = np.bincount(g_values, minlength=256) / total_pixels
    b_prob = np.bincount(b_values, minlength=256) / total_pixels
    
    return r_prob, g_prob, b_prob

# Step 3: Generate a new image based on RGB probabilities
def generate_image(r_prob, g_prob, b_prob, size=(500, 500)):
    new_image = Image.new('RGB', size)
    pixels = []

    # Generate each pixel's R, G, B values based on the probabilities
    for _ in range(size[0] * size[1]):
        r = np.random.choice(range(256), p=r_prob)
        g = np.random.choice(range(256), p=g_prob)
        b = np.random.choice(range(256), p=b_prob)
        pixels.append((r, g, b))

    # Set pixel data
    new_image.putdata(pixels)
    return new_image

# Main Function
def main(image_path):
    # Load the image
    img = load_image(image_path)
    
    # Calculate RGB probabilities
    r_prob, g_prob, b_prob = calculate_rgb_probabilities(img)
    
    # Generate a new image based on calculated probabilities
    new_image = generate_image(r_prob, g_prob, b_prob, size=(200, 200))
    
    # Get the current timestamp and format it
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Get the base name of the original file (without the path and extension)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # Create the images directory if it doesn't exist
    output_dir = './images/restored_images'
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct the new file name with the timestamp and "_modified", and save it in the images folder
    filename = f"{timestamp}_{base_name}_modified.png"
    file_path = os.path.join(output_dir, filename)
    
    # Save the generated image
    new_image.save(file_path)
    
    print(f"New image generated and saved as '{file_path}'.")

# Example usage:
main("images/white_fringe.png")
