import os
from PIL import Image
import numpy as np
import pandas as pd
import argparse

def analyze_image(image_path):
    # Load the image
    img = Image.open(image_path).convert("RGBA")
    data = np.array(img)

    # Filter out transparent pixels
    non_transparent_pixels = data[data[:, :, 3] != 0]

    # Calculate r+g+b for each pixel
    rgb_sum = np.sum(non_transparent_pixels[:, :3], axis=1)

    # Define group ranges
    groups = {
        "Group 1": rgb_sum <= 60,
        "Group 2": (rgb_sum > 60) & (rgb_sum <= 180),
        "Group 3": (rgb_sum > 180) & (rgb_sum <= 390),
        "Group 4": (rgb_sum > 390) & (rgb_sum <= 600),
        "Group 5": rgb_sum > 600
    }

    # Create a dictionary to store statistics
    stats = {}

    # Initialize data structure
    for group_name in groups:
        stats[group_name] = {'Value': [], 'R': [], 'G': [], 'B': []}

    # Process each group
    for group_name, group_mask in groups.items():
        group_pixels = non_transparent_pixels[group_mask][:, :3]  # R, G, B values
        for i in range(256):  # Ranges from 0 to 255
            r_count = np.sum(group_pixels[:, 0] == i)
            g_count = np.sum(group_pixels[:, 1] == i)
            b_count = np.sum(group_pixels[:, 2] == i)
            if r_count == 0 and g_count == 0 and b_count == 0:
                continue  # Skip row if R == G == B == 0
            stats[group_name]['Value'].append(i)
            stats[group_name]['R'].append(r_count)
            stats[group_name]['G'].append(g_count)
            stats[group_name]['B'].append(b_count)

    # Calculate average R, G, B for each group
    for group_name, group_mask in groups.items():
        group_pixels = non_transparent_pixels[group_mask][:, :3]  # R, G, B values
        avg_r = np.mean(group_pixels[:, 0]) if len(group_pixels) > 0 else 0
        avg_g = np.mean(group_pixels[:, 1]) if len(group_pixels) > 0 else 0
        avg_b = np.mean(group_pixels[:, 2]) if len(group_pixels) > 0 else 0
        stats[group_name]['Value'].append('Avg')
        stats[group_name]['R'].append(round(avg_r, 2))
        stats[group_name]['G'].append(round(avg_g, 2))
        stats[group_name]['B'].append(round(avg_b, 2))

    # Calculate overall average R, G, B for the entire image (excluding transparent pixels)
    avg_r_total = round(np.mean(non_transparent_pixels[:, 0]), 2)
    avg_g_total = round(np.mean(non_transparent_pixels[:, 1]), 2)
    avg_b_total = round(np.mean(non_transparent_pixels[:, 2]), 2)
    
    # Create a dataframe and save to CSV
    df_dict = {}
    for group_name, group_data in stats.items():
        df = pd.DataFrame(group_data)
        df_dict[group_name] = df
    
    # Combine groups into a single DataFrame for the CSV export, with blank columns between groups
    dfs_with_blank_cols = []
    for group in df_dict:
        dfs_with_blank_cols.append(df_dict[group])
        dfs_with_blank_cols.append(pd.DataFrame({"": [""] * len(df_dict[group])}))  # Add blank column
    
    # Remove the last blank column (after the last group)
    dfs_with_blank_cols = dfs_with_blank_cols[:-1]
    
    # Concatenate DataFrames
    combined_df = pd.concat(dfs_with_blank_cols, axis=1)

    # Append the overall average R, G, B
    overall_avg_df = pd.DataFrame({"Value": ["Avg"], "R": [avg_r_total], "G": [avg_g_total], "B": [avg_b_total]})
    combined_df = pd.concat([combined_df, overall_avg_df], axis=1)

    # Create the output directory if it doesn't exist
    output_dir = './images/csv'
    os.makedirs(output_dir, exist_ok=True)

    # Save the DataFrame to a CSV file
    output_filename = os.path.join(output_dir, f"{image_path.split('/')[-1].split('.')[0]}_statistic-dashboard.csv")
    combined_df.to_csv(output_filename, index=False)

# Example usage

# Setup argument parser
parser = argparse.ArgumentParser(description="Convert an image to a CSV file of RGB values statistic.")
parser.add_argument('--path', type=str, default="images/6(ps).png", help='Path to the image file (optional)')

# Parse arguments
args = parser.parse_args()

# Path to the image file (provided as an argument or default)
image_path = args.path

analyze_image(image_path)
