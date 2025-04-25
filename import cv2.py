import cv2
import os
import numpy as np

# Define input and output folders
input_folder = "A"  # Change to your folder path
output_folder = os.path.join(input_folder, "converted")

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get list of all image files in the folder
image_files = [f for f in os.listdir(input_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

# Process each image
for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # Read with alpha channel support

    if image is None:
        print(f"Skipping {image_file}, unable to read.")
        continue

    # Check if image has an alpha channel (transparency)
    if image.shape[-1] == 4:  
        b, g, r, a = cv2.split(image)  # Split channels (RGBA)
        inverted = cv2.merge([255 - b, 255 - g, 255 - r, a])  # Keep transparency
    else:
        # Invert colors for normal images
        inverted = cv2.bitwise_not(image)

        # Increase brightness for better visibility
        brightness = 50  # Adjust brightness level as needed
        inverted = cv2.add(inverted, np.array([brightness], dtype=np.uint8))

    # Save the converted image
    output_path = os.path.join(output_folder, image_file)
    cv2.imwrite(output_path, inverted)

    print(f"✅ Converted: {image_file} -> {output_path}")

print("🎉 All images processed successfully!")
