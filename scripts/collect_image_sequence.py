import os
import time
import cv2
import numpy as np
from picamera2 import Picamera2
from datetime import datetime

# === GLOBAL CONFIGURATION ===
index = 1  # <-- Change this to your desired run index
output_dir = f"/home/pi/ORCA/data/sample_front_camera/run_{index}"
capture_interval = 0.5  # seconds
total_duration = 5      # seconds
frame_count = int(total_duration / capture_interval)

def ensure_dir_exists(path):
    os.makedirs(path, exist_ok=True)

def resize_with_padding(image, target_size=(640, 640)):
    """Resize image while keeping aspect ratio and pad with black."""
    h, w = image.shape[:2]
    scale = min(target_size[0] / h, target_size[1] / w)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Create black background
    padded = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)
    x_offset = (target_size[0] - new_w) // 2
    y_offset = (target_size[1] - new_h) // 2
    padded[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    return padded

def main():
    ensure_dir_exists(output_dir)

    picam2 = Picamera2()
    config = picam2.create_still_configuration()
    picam2.configure(config)

    picam2.set_controls({"AwbEnable": True})
    time.sleep(2) 

    picam2.start()

    metadata = picam2.capture_metadata()
    print("Current ColourGains:", metadata.get("ColourGains"))

    

    print(f"Capturing {frame_count} images to '{output_dir}'...")
    for i in range(frame_count):
        # Capture to numpy array
        image = picam2.capture_array()
        resized = resize_with_padding(image)

        filename = os.path.join(output_dir, f"img_{i:03d}.jpg")
        cv2.imwrite(filename, resized)
        print(f"Saved {filename}")
        time.sleep(capture_interval)

    picam2.close()
    print("Capture complete.")

if __name__ == "__main__":
    main()