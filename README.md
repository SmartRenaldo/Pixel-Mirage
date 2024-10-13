# Pixel-Mirage

Before run .py file, to activate the Virtual Environment, run:
    source myenv/bin/activate

Example Usage for csv_to_img.py (similar to image_to_rgb_values_csv.py):
    Without providing an argument (uses default csv_path):
        python3 csv_to_img.py
        This will use the default csv_path value.
    With providing a custom CSV path:
        python your_script.py --path "path/to/your/other_csv.csv"
        This will override the default and use the provided CSV file path.

When finished, to deactivate the environment, simply run:
    deactivate
