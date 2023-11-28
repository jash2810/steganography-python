from PIL import Image
from operator import itemgetter
import sys
import base64

def encrypt_key(input_key):
    # Encode the key using base64
    encoded_bytes = base64.b64encode(input_key.encode('utf-8'))
    
    # Convert the bytes to a key
    encrypted_key = encoded_bytes.decode('utf-8')
    
    return encrypted_key

def decrypt_key(encrypted_key):
    # Decode the base64-encoded key
    decoded_bytes = base64.b64decode(encrypted_key.encode('utf-8'))
    
    # Convert the bytes to a key
    decrypted_key = decoded_bytes.decode('utf-8')
    
    return decrypted_key

def message_to_binary(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

def encode_image(image_path, message):
    # message to binary

    input_file = open(message, 'r')
    lines = input_file.readlines()
    lines = ' '.join(x for x in lines)

    binary_message = message_to_binary(lines)

    # get pixels
    img = Image.open(image_path)
    pixels = list(img.getdata())

    if len(binary_message) > len(pixels):
        raise ValueError("Message is too long to be encoded in this image.")
    
    # append bit values to the last elements of each pixel's tuple and at the end of message append normal pixels
    encoded_pixels = []
    for i in range(len(pixels)):
        pixel = list(pixels[i])
        if(i < len(binary_message)):
            pixel[-1] = int(binary_message[i])
        encoded_pixels.append(tuple(pixel))
        
    # save image with new pixel values
    encoded_img = Image.new(img.mode, img.size)
    encoded_img.putdata(encoded_pixels)
    encoded_img.save('encoded.png')
    print("Image encoded successfully as encoded.png.\nKey is: ", encrypt_key(str(len(lines))))
    
def decode_image(key):
    encode_img = Image.open('encoded.png')
    encoded_pixels = list(encode_img.getdata())

    # length of binary values to be extracted from encoded pixels
    bits = key*8
    # bits grouped by 8 (byte) will be stored in this list for each character in the message
    bits_list = []
    # make a list of each character bytes
    for i in range(0, bits, 8):
        bits_list.append(''.join(map(str, list(map(itemgetter(-1), encoded_pixels[i:i+8])))))

    # convert binary values to string
    print(binary_to_string(bits_list))

def binary_to_string(bits):
    return ''.join([chr(int(i, 2)) for i in bits])

message = ''
# key = len(message)

print('Select the following options: \n\n1. Encode the message\n2. Decode the message\n')
x=input()

if(x=='1'):
    print('\nThe file that has been selected is :', sys.argv[1])
    encode_image(sys.argv[1], sys.argv[2])
if(x=='2'):
    print('\nplease enter the key value: \n')
    key = int(decrypt_key(input()))
    decode_image(key)
