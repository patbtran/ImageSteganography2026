#Steganography Project

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from hashlib import sha256
from base64 import b64encode, b64decode
import os

def user_input(m):
    return encrypt(m, sha256(os.urandom(16)).digest())

def encrypt(I, key):
    iv = get_random_bytes(AES.block_size)  # generate random iv
    cipher = AES.new(key, AES.MODE_CBC, iv)  
    ciphertext = iv + cipher.encrypt(pad(I.encode(), AES.block_size))  # encrypt message
    return b64encode(ciphertext).decode('utf-8') 
    

def decrypt(ciphertext, key):
    ciphertext = b64decode(ciphertext)  # decode the base64 encoded message
    iv = ciphertext[:AES.block_size]  # extract the iv from the beginning
    cipher = AES.new(key, AES.MODE_CBC, iv) 
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])  # decrypt the message
    return plaintext.rstrip(b'\x00').decode('utf-8')

def main():
    # get message from user
    message = input("Enter message: ")
    encrypted_message = user_input(message)
    print("Encrypted message:", encrypted_message)
    print("Decrypted message:", decrypt(encrypted_message, sha256(os.urandom(16)).digest()))

main()