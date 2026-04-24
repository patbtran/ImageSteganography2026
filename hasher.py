from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

#Message and key
def user_input(m,k):
    return encrypt(m,k)

def encrypt(I, key):
    iv = get_random_bytes(AES.block_size)  # generate random iv
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = iv + cipher.encrypt(pad(I.encode(), AES.block_size))  # encrypt message
    return b64encode(ciphertext).decode('utf-8')


def decrypt(ciphertext, key):
    ciphertext = b64decode(ciphertext)  # decode the base64 encoded message
    iv = ciphertext[:AES.block_size]  # extract the iv from the beginning
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        plaintext = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
    except ValueError:
        raise ValueError
    else:
        return plaintext.decode('utf-8')