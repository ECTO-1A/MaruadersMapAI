from PIL import Image
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import os

def decode_message_from_image(image_path):
    img = Image.open(image_path)
    binary_message = ''
    width, height = img.size

    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            for n in range(3):  # Iterate through RGB channels
                binary_message += str(pixel[n] & 1)

    # Convert binary data to string
    all_bytes = [binary_message[i: i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''
    for byte in all_bytes:
        if byte == '11111110':  # Delimiter indicating end of message
            break
        decoded_message += chr(int(byte, 2))

    return decoded_message

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message.encode()).decode()
    return decrypted_message

def up_to_no_good():
    load_dotenv()
    secret_key = os.getenv('SECRET_KEY')

    if secret_key is None:
        raise ValueError("No 'SECRET_KEY' found in .env file.")

    # Specify the image path
    image_path = 'Prompt/output.png'

    hidden_message = decode_message_from_image(image_path)
    decrypted_message = decrypt_message(hidden_message, secret_key.encode())
    return decrypted_message

# This part allows the script to be run standalone for testing
if __name__ == "__main__":
    try:
        decrypted_msg = up_to_no_good()
        print("Decrypted Message:", decrypted_msg)
    except Exception as e:
        print(e)