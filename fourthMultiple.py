# NumPy used to efficiently manipulate large arrays of
# image data for encryption and decryption; generate_keys
# function creates encryption keys using np.meshgrid to generate
# coordinate grids, and performs vectorized arithmetic operations
# to produce unique keys for each pixel; Converting images to NumPy
# arrays allows for fast and efficient pixel-wise operations;
# circular addition and subtraction functions leverage NumPy's vectorized
# operations to modify the pixel values based on the keys, ensuring a
# fast encryption and decryption process. Transposing the keys array
# for compatibility with the image array dimensions; overall facilitating
# better time complexity and hence scalability

import os
import numpy as np
from PIL import Image

def generate_keys(width, height):
    # Generate keys for entire image in batch
    i, j = np.meshgrid(np.arange(width), np.arange(height))
    concatenated_keys = i.astype(np.uint16) * 10000 + j.astype(np.uint16)
    keys = (concatenated_keys + (i * j) % 256).astype(np.uint8)
    return keys

def circular_add(value, increment):
    # Vectorized circular addition
    return (value + increment) % 256

def encrypt_image(image_path, output_folder, index):
    # Open image
    img = Image.open(image_path)
    img = img.convert("RGB")
    
    # Convert image to numpy array
    img_array = np.array(img)
    width, height, channels = img_array.shape
    
    # Generate keys for entire image
    keys = generate_keys(width, height)
    
    # Transpose keys to match the shape of img_array
    keys_transposed = keys.T
    
    # Encrypt image using vectorized operations
    encrypted_img_array = circular_add(img_array, keys_transposed[..., None])
    
    # Save encrypted image
    filename = str(index) + ".png"
    encrypted_img_path = os.path.join(output_folder, filename)
    Image.fromarray(encrypted_img_array.astype(np.uint8)).save(encrypted_img_path)

def decrypt_image(encrypted_image_path, output_folder, index):
    # Open encrypted image
    img = Image.open(encrypted_image_path)
    img = img.convert("RGB")
    
    # Convert image to numpy array
    img_array = np.array(img)
    width, height, channels = img_array.shape
    
    # Generate keys for entire image
    keys = generate_keys(width, height)
    
    # Transpose keys to match the shape of img_array
    keys_transposed = keys.T
    
    # Decrypt image using vectorized operations
    decrypted_img_array = circular_add(img_array, -keys_transposed[..., None])
    
    # Save decrypted image
    filename = str(index) + ".png"
    decrypted_img_path = os.path.join(output_folder, filename)
    Image.fromarray(decrypted_img_array.astype(np.uint8)).save(decrypted_img_path)

if __name__ == "__main__":
    # Create folders if they don't exist
    output_encrypted_folder = "encrypted"
    output_decrypted_folder = "decrypted"
    if not os.path.exists(output_encrypted_folder):
        os.makedirs(output_encrypted_folder)
    if not os.path.exists(output_decrypted_folder):
        os.makedirs(output_decrypted_folder)
    
    # Process all images in the 'photos' folder
    photo_folder = "photos"
    index = 1
    for filename in os.listdir(photo_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(photo_folder, filename)
            encrypt_image(image_path, output_encrypted_folder, index)
            decrypt_image(os.path.join(output_encrypted_folder, str(index) + ".png"), output_decrypted_folder, index)
            index += 1
