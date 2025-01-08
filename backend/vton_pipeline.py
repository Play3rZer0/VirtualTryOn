# vton_pipeline.py
import cv2
import numpy as np
import os

def run_vton_pipeline(user_photo_path: str, cloth_photo_path: str) -> str:
    """
    1. Load user_photo and cloth_photo from the provided paths.
    2. Run them through a simplified VTON pipeline.
    3. Save and return the resulting composited image path.
    """
    # Load images
    user_img = cv2.imread(user_photo_path)
    cloth_img = cv2.imread(cloth_photo_path)
    
    # Check if images are loaded successfully
    if user_img is None or cloth_img is None:
        raise ValueError("Failed to load one or both images")

    # Resize cloth image to match user image size
    cloth_img = cv2.resize(cloth_img, (user_img.shape[1], user_img.shape[0]))

    # Simple blending of images (this is a placeholder for actual VTON processing)
    alpha = 0.5  # Adjust this value to change the blending ratio
    beta = 1.0 - alpha
    blended_img = cv2.addWeighted(user_img, alpha, cloth_img, beta, 0.0)

    # Ensure the output directory exists
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Save the result
    output_path = os.path.join(output_dir, "try_on_result.png")
    cv2.imwrite(output_path, blended_img)

    return output_path
