# third, increment key is based on coordinates (concatenation(i, j)+(i*j) mod 256)
import os
from PIL import Image
import time

def generate_key(i, j):
    # concatenation
    concatenated_key = int(str(i) + str(j))
    # (concatenation(i, j)+(i*j) mod 256)
    key = (concatenated_key + (i * j)) % 256

    return key

def circular_add(value, increment, max_value=255):
    # circular increment(wraps around 256 to 0)
    result = (value + increment) % (max_value + 1)
    return result

def encrypt_image(image_path, output_folder, index):
    # open image
    img = Image.open(image_path)
    
    # convert image to RGB mode
    img = img.convert("RGB")

    width, height = img.size

    pixels = img.load()

    # encrypt each pixel using pixel-specific key
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            key = generate_key(i, j)
            pixels[i, j] = (
                circular_add(r, key),       # adding cuz encrypting
                circular_add(g, key),
                circular_add(b, key)
            )

    # Save encrypted image
    filename = str(index) + ".png"
    encrypted_img_path = os.path.join(output_folder, filename)
    img.save(encrypted_img_path)
    

def decrypt_image(encrypted_image_path, output_folder, index):
    # open encrypted image
    img = Image.open(encrypted_image_path)
    
    # convert image to RGB mode
    img = img.convert("RGB")

    width, height = img.size

    pixels = img.load()

    # decrypt each pixel using pixel-specific key
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            key = generate_key(i, j)
            pixels[i, j] = (
                circular_add(r, -key),      # subtracting cuz decrypting
                circular_add(g, -key),
                circular_add(b, -key)
            )

    # Save decrypted image
    filename = str(index) + ".png"
    decrypted_img_path = os.path.join(output_folder, filename)
    img.save(decrypted_img_path)

if __name__ == "__main__":
    # Create folders if they don't exist
    output_encrypted_folder = "encrypted"
    output_decrypted_folder = "decrypted"
    if not os.path.exists(output_encrypted_folder):
        os.makedirs(output_encrypted_folder)
    if not os.path.exists(output_decrypted_folder):
        os.makedirs(output_decrypted_folder)
    
    # Start measuring time (milliseconds)
    start_time = time.time() * 1000

    # Process all images in the 'photos' folder
    photo_folder = "photos"
    index = 1
    for filename in os.listdir(photo_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(photo_folder, filename)
            encrypt_image(image_path, output_encrypted_folder, index)
            decrypt_image(os.path.join(output_encrypted_folder, str(index) + ".png"), output_decrypted_folder, index)
            index += 1

     # Calculate and print total runtime (milliseconds)
    end_time = time.time() * 1000
    total_runtime = end_time - start_time
    print("Total actual runtime of the code: {:.2f} milliseconds".format(total_runtime))