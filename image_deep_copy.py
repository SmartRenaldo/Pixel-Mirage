from PIL import Image

def adjust_image(input_path, output_path):
    # Open the image
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    
    # Get image width and height
    width, height = img.size
    
    # Loop through each pixel in the image
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
                
            pixels[x, y] = (r, g, b, a)
    
    # Save the modified image
    img.save(output_path)
    
    # Print image information
    output_img = Image.open(output_path)
    print("New image information:")
    print(f"File path: {output_path}")
    print(f"Image format: {output_img.format}")
    print(f"Image size: {output_img.size} (Width x Height)")
    print(f"Image mode: {output_img.mode}")
    print(f"Sample color information (top-left pixel): {output_img.getpixel((0, 0))}")

# Usage example
input_image_path = "input.png"  # Input image path
output_image_path = "output.png"  # Output image path

adjust_image(input_image_path, output_image_path)
