from PIL import Image
import piexif

def check_photoshop_edit(image_path):
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Try to get the EXIF metadata
        exif_data = piexif.load(img.info.get("exif", b""))
        
        # Check specific metadata tag for software info
        software_info = exif_data.get("0th", {}).get(piexif.ImageIFD.Software, b"").decode('utf-8', errors='ignore')
        
        # Determine if Photoshop was used for editing
        if "Adobe Photoshop" in software_info:
            print("This image may have been edited with Photoshop.")
        elif software_info:
            print(f"Image editing software: {software_info}")
        else:
            print("No specific Photoshop information found; the image may not have been edited with Photoshop.")
    
    except Exception as e:
        print("Could not read the image metadata, or the image may not contain EXIF information.")
        print("Error message:", e)

# Usage example
image_path = "image.jpg"  # Input image path
check_photoshop_edit(image_path)
