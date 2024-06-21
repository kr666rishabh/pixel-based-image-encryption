# third, increment key is based on coordinates (concatenation(i, j)+(i*j) mod 256)
from PIL import Image

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

def encrypt_image(image_path):
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

    # save encrypted image
    img.save("encrypted_image.png")

def decrypt_image(encrypted_image_path):
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

    # save decrypted image
    img.save("decrypted_image.png")

if __name__ == "__main__":
    # encrypt_image("red.png")
    # encrypt_image("four.png")
    # encrypt_image("colors.png")
    # encrypt_image("sample HD.jpg")
    encrypt_image("sample 4K.jpg")

    decrypt_image("encrypted_image.png")