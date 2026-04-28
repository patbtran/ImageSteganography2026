# steganographyproject2026

NEEDS PILLOW AND PYCRYPTODOME:

pip install pillow

pip install pycryptodome

Run main.py then load a .png image. Enter your key(!) and secret message, then click "encode image". You will be prompted to save the file at a location of your choosing. To decode a message in an image, load the encoded image, type the correct key into the key entry box, then press "decode image".

Attack testing:
After encoding an image with a key of your choice (or lack thereof!), run mallory.py and load the image, then enter the maximum time (in seconds) to spend attempting to brute force the key. When the key is found or the time expires, you will be notified.
