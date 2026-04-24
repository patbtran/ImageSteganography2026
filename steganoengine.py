from PIL import Image
from hashlib import sha256
import hasher


def generateData(data):
    return [format(ord(i), "08b") for i in data]


def modifyPixels(pix, data):
    datalist = generateData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pixels = [value for value in next(imdata)[:3] + next(imdata)[:3] + next(imdata)[:3]]

        for j in range(8):
            if datalist[i][j] == '0' and pixels[j] % 2 != 0:
                pixels[j] -= 1
            elif datalist[i][j] == '1' and pixels[j] % 2 == 0:
                pixels[j] = pixels[j] - 1 if pixels[j] != 0 else pixels[j] + 1

        if i == lendata - 1:
            pixels[-1] |= 1
        else:
            pixels[-1] &= ~1

        yield tuple(pixels[:3])
        yield tuple(pixels[3:6])
        yield tuple(pixels[6:9])


def encode_enc(new_img, data):
    w = new_img.size[0]
    (x, y) = (0, 0)

    for p in modifyPixels(new_img.getdata(), data):
        new_img.putpixel((x, y), p)
        x = 0 if x == w - 1 else x + 1
        y += 1 if x == 0 else 0

def encode(filename, msg, key, save_path):
    image = Image.open(filename, 'r')
    key = sha256(key.encode('utf-8')).digest()
    #data = msg
    data = hasher.encrypt(msg, key)

    if not data:
        raise ValueError("Data is empty")

    new_img = image.copy()
    encode_enc(new_img, data)
    new_img_name = save_path
    new_img.save(new_img_name)


def decode(filename, key):
    key = sha256(key.encode('utf-8')).digest()
    image = Image.open(filename, 'r')
    imgdata = iter(image.getdata())
    encrypted_data = ""

    while True:
        pixels = [value for value in next(imgdata)[:3] + next(imgdata)[:3] + next(imgdata)[:3]]
        binstr = ''.join(['1' if i % 2 else '0' for i in pixels[:8]])
        encrypted_data += chr(int(binstr, 2))

        if pixels[-1] % 2 != 0:
            break
    #return encrypted_data.encode('utf-8')
    return hasher.decrypt(encrypted_data, key)
