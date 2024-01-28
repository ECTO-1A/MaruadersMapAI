from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key
from PIL import Image
import os
from prompt import user_input


# Function to load or generate a key
def load_or_generate_key():
    key = os.getenv('SECRET_KEY')
    if not key:
        key = Fernet.generate_key().decode()
        set_key('.env', 'SECRET_KEY', key)
    return key.encode()

# Function to encrypt a message
def encrypt_message(message, key):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode()).decode()
    set_key('.env', 'ENCRYPTED_MESSAGE', encrypted_message)
    return encrypted_message

# Function to encode message in image
def encode_message_in_image(image_path, message, output_path):
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    index = 0

    # Convert message to binary
    binary_message = ''.join([format(ord(char), '08b') for char in message])
    binary_message += '1111111111111110'  # Delimiter to indicate end of message

    for row in range(height):
        for col in range(width):
            if index < len(binary_message):
                pixel = list(img.getpixel((col, row)))
                for n in range(3):  # Iterate through RGB channels
                    if index < len(binary_message):
                        pixel[n] = pixel[n] & ~1 | int(binary_message[index])
                        index += 1
                encoded.putpixel((col, row), tuple(pixel))
            else:
                break

    encoded.save(output_path)

# Function to clear ENCRYPTED_MESSAGE from .env and reset prompt.py
def clear_encrypted_message_and_reset_prompt():
    set_key('.env', 'ENCRYPTED_MESSAGE', '')
    with open('prompt.py', 'w') as file:
        file.write("user_input = ''' Enter information to encrypt here. This will be the prompt for your AI system. It can also be used to store other information, such as a password or a secret message or entire codebase.''' \n")

def main():
    load_dotenv()
    key = load_or_generate_key()
    
    message = user_input
    encrypted_message = encrypt_message(message, key)

    image_path = ('image.png')
    output_path = ("Prompt/output.png")
    encode_message_in_image(image_path, encrypted_message, output_path)

    clear_encrypted_message_and_reset_prompt()
    print("Mischief Managed.")

if __name__ == "__main__":
    main()
