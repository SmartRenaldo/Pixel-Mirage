from PIL import Image
import pandas as pd

# Load the image
image = Image.open("your_image.jpg")

# Convert the image to RGB mode
rgb_image = image.convert("RGB")

# Get the size of the image
width, height = rgb_image.size

# Prepare data storage for pixels
data = []

# Loop through each pixel to get its color values
for y in range(height):
    row = []
    for x in range(width):
        # Get the RGB values of the pixel at (x, y)
        r, g, b = rgb_image.getpixel((x, y))
        # Store the RGB values as a string like "(R, G, B)"
        row.append(f"({r}, {g}, {b})")
    data.append(row)

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Save to CSV file
df.to_csv("pixel_colors.csv", index=False, header=False)

# Optionally, save to Excel
# df.to_excel("pixel_colors.xlsx", index=False, header=False)