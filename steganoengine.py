from PIL import Image
from hashlib import sha256
import hasher

#converts the message text into a list of 8bit strings
def generateData(data):
    return [format(ord(i), "08b") for i in data]

#generator that yields modified 3-pixel chunks, one for each encoded character.
#pix - original image pixel data
#data - ciphertext to hide
def modifyPixels(pix, data):
    datalist = generateData(data) #list of 8 bit binary strings
    lendata = len(datalist)
    imdata = iter(pix) #iterates through original pixels

    for i in range(lendata):
        # each pixel is a tuple (r,g,b)
        # here we flatten the first 3 values of each into a 9 element list
        pixels = [value for value in next(imdata)[:3] + next(imdata)[:3] + next(imdata)[:3]]
        #embed the char's 8 bits into the data via flipping
        #bits [0-7] go into pixels [0-7]
        for j in range(8):
            if datalist[i][j] == '0' and pixels[j] % 2 != 0:
                # if we need zero as least significant bit, make value even
                pixels[j] -= 1
            elif datalist[i][j] == '1' and pixels[j] % 2 == 0:
                # if we need one as least significant bit and the value is zero, increase it instead
                if pixels[j] != 0:
                    pixels[j] -= 1
                else:
                    pixels[j] += 1
        #last channel (pixels[8]) is a continuation flag
        #if it's the last character, set least significant bit to 1
        #otherwise, set it to 0
        if i == lendata - 1:
            pixels[-1] |= 1
        else:
            pixels[-1] &= ~1

        #yields (generates/returns/etc) the three modified pixels
        yield tuple(pixels[:3])
        yield tuple(pixels[3:6])
        yield tuple(pixels[6:9])

#encodes modified pixels into new img
def encode_enc(new_img, data):
    w = new_img.size[0]
    (x, y) = (0, 0)

    #iterate through image pixel left to right row by row and replace it with modifyPixel data
    for p in modifyPixels(new_img.getdata(), data):
        new_img.putpixel((x, y), p)
        if x == w - 1:
            x = 0
        else:
            x += 1

        if x == 0:
            y += 1
        else:
            y = 0

#handles saving/encoding
def encode(filename, msg, key, save_path):
    image = Image.open(filename, 'r')
    key = sha256(key.encode('utf-8')).digest()
    #data = msg
    data = hasher.encrypt(msg, key) #encrypt plaintext msg with AES so the ciphertext goes into the image

    if not data:
        raise ValueError("no data!")

    new_img = image.copy()
    encode_enc(new_img, data)
    new_img_name = save_path
    new_img.save(new_img_name)

#decodes hidden text from image using key
def decode(filename, key):
    key = sha256(key.encode('utf-8')).digest()
    image = Image.open(filename, 'r')
    imgdata = iter(image.getdata())
    encrypted_data = ""

    while True:
        #each next(imgdata)[:3] is a pixel, we need 3 to hold 1 character.
        pixels = [value for value in next(imgdata)[:3] + next(imgdata)[:3] + next(imgdata)[:3]]

        #the least significant bit of first 8 channels gives us one bit of the original char
        binstr = ''.join(['1' if i % 2 else '0' for i in pixels[:8]])
        encrypted_data += chr(int(binstr, 2))
        #if the least significant bit of the 9th value is 1, we should exit
        if pixels[-1] % 2 != 0:
            break
    #return encrypted_data.encode('utf-8')
    return hasher.decrypt(encrypted_data, key)
