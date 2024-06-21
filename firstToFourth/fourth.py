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

def encrypt_image(image_path):
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
    encrypted_img = Image.fromarray(encrypted_img_array.astype(np.uint8))
    encrypted_img.save("encrypted_image.png")

def decrypt_image(encrypted_image_path):
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
    decrypted_img = Image.fromarray(decrypted_img_array.astype(np.uint8))
    decrypted_img.save("decrypted_image.png")

if __name__ == "__main__":
    encrypt_image("sample 4K.jpg")
    decrypt_image("encrypted_image.png")
