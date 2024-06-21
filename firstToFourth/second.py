# second, increment key is based on dist from the center

import math
from PIL import Image

def circular_add(value, increment, max_value=255):
    # circular increment(wraps around 256 to 0)
    result = (value + increment) % (max_value + 1)
    return result

def calculate_increment(distance, max_distance, max_increment):
    # increment value acc to distance of pixel from center
    return int(distance / max_distance * max_increment)

def encrypt_image(image_path, max_increment=100):
    # open image
    img = Image.open(image_path)
    
    # convert image to RGB mode
    img = img.convert("RGB")

    width, height = img.size
    center_x = width / 2
    center_y = height / 2

    pixels = img.load()

    # max distance from center
    max_distance = math.sqrt(center_x ** 2 + center_y ** 2)

    # encrypt each pixel using pixel-specific key
    for i in range(width):
        for j in range(height):
            distance = math.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
            increment = calculate_increment(distance, max_distance, max_increment)
            r, g, b = pixels[i, j]
            pixels[i, j] = (
                circular_add(r, increment),
                circular_add(g, increment),
                circular_add(b, increment)
            )

    # save encrypted image
    img.save("encrypted_image.png")

def decrypt_image(encrypted_image_path, max_increment=100):
    # open encrypted image
    img = Image.open(encrypted_image_path)
    
    # convert image to RGB mode
    img = img.convert("RGB")

    width, height = img.size
    center_x = width / 2
    center_y = height / 2

    pixels = img.load()

    # max distance from center
    max_distance = math.sqrt(center_x ** 2 + center_y ** 2)

    # decrypt each pixel using pixel-specific key
    for i in range(width):
        for j in range(height):
            distance = math.sqrt((i - center_x) ** 2 + (j - center_y) ** 2)
            increment = calculate_increment(distance, max_distance, max_increment)
            r, g, b = pixels[i, j]
            pixels[i, j] = (
                circular_add(r, -increment),
                circular_add(g, -increment),
                circular_add(b, -increment)
            )

    # save decrypted image
    img.save("decrypted_image.png")

if __name__ == "__main__":
    encrypt_image("red.png")
    # encrypt_image("four.png")
    # encrypt_image("colors.png")
    # encrypt_image("sample Full HD.jpg")

    decrypt_image("encrypted_image.png")
