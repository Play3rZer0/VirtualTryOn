import cv2
import numpy as np
import os
#from skimage.transform import warp, PiecewiseAffineTransform, resize
from skimage.transform import warp, AffineTransform, resize

# Define the target dimension (800 x 600 pixels)
TARGET_WIDTH = 800
TARGET_HEIGHT = 600

def resize_image(image, target_width, target_height):
    """
    Resize the input image to the target dimensions.
    """
    return cv2.resize(image, (target_width, target_height))

def create_mask(image):
    # Placeholder for segmentation model to create a mask
    # This should be replaced with actual segmentation logic
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    return mask

def warp_image(src, dst, mask):
    # Placeholder for warping logic (e.g., TPS warping)
    # This should be replaced with actual warping logic
    transform = AffineTransform(scale=(1.1, 1.1), rotation=0.1, translation=(10, 10))
    #transform = PiecewiseAffineTransform()
    warped_image = warp(src, transform.inverse, output_shape=dst.shape[:2])
    warped_mask = warp(mask, transform.inverse, output_shape=dst.shape[:2])
    return (warped_image * 255).astype(np.uint8), (warped_mask * 255).astype(np.uint8)

def blend_images(user_img, cloth_img, mask):
    # Poisson blending for seamless integration
    center = (user_img.shape[1] // 2, user_img.shape[0] // 2)
    blended_img = cv2.seamlessClone(cloth_img, user_img, mask, center, cv2.NORMAL_CLONE)
    return blended_img

def match_histograms(src, dst):
    """
    Match the histograms of the source image to the destination image.
    """
    matched = np.zeros_like(src)
    for i in range(3):  # Loop over channels (BGR)
        src_hist, _ = np.histogram(src[:,:,i], 256, [0,256])
        dst_hist, _ = np.histogram(dst[:,:,i], 256, [0,256])
        src_cdf = np.cumsum(src_hist)
        dst_cdf = np.cumsum(dst_hist)
        lut = np.interp(src_cdf, dst_cdf, np.arange(256))
        matched[:,:,i] = np.uint8(np.interp(src[:,:,i], np.arange(256), lut))
    return matched

def run_vton_pipeline(user_photo_path: str, cloth_photo_path: str) -> str:
    # Load images
    user_img = cv2.imread(user_photo_path)
    cloth_img = cv2.imread(cloth_photo_path)
    
    # Check if images are loaded successfully
    if user_img is None or cloth_img is None:
        raise ValueError("Failed to load one or both images")

    # Create mask for the clothing
    cloth_mask = create_mask(cloth_img)

    # Warp the clothing image to fit the user
    warped_cloth, warped_mask = warp_image(cloth_img, user_img, cloth_mask)

    # Blend the images
    blended_img = blend_images(user_img, warped_cloth, warped_mask)

    # Ensure the output directory exists
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Save the result
    output_path = os.path.join(output_dir, "try_on_result.png")
    cv2.imwrite(output_path, blended_img)

    return output_path
