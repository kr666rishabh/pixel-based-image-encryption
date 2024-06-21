from PIL import Image

def circular_add(value, increment, max_value=255):
    # Circularly add the increment to the value
    result = (value + increment) % (max_value + 1)
    return result

def encrypt_image(image_path, increment=10):
    # Open the image
    img = Image.open(image_path)
    
    # Convert to RGB mode if not already in that mode
    img = img.convert("RGB")

    pixels = img.load()

    # Loop through each pixel and circularly add the increment to each RGB component
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (
                circular_add(r, increment),
                circular_add(g, increment),
                circular_add(b, increment)
            )

    # Save the encrypted image
    img.save("encrypted_image.png")

def decrypt_image(encrypted_image_path, increment=10):
    # Open the encrypted image
    img = Image.open(encrypted_image_path)
    
    # Convert to RGB mode if not already in that mode
    img = img.convert("RGB")

    pixels = img.load()

    # Loop through each pixel and revert the circular addition
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (
                circular_add(r, -increment),
                circular_add(g, -increment),
                circular_add(b, -increment)
            )

    # Save the decrypted image
    img.save("decrypted_image.png")

if __name__ == "__main__":
    # Replace 'your_image.jpg' with the path to your image file
    encrypt_image("colors.png")

    # Replace 'encrypted_image.png' with the path to the encrypted image file
    decrypt_image("encrypted_image.png")