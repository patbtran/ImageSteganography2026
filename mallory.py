import itertools
import string
import tkinter as tk
import steganoengine
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time


root = tk.Tk()

root.title("steganocracker | evil build")
root.configure(background="black")
root.resizable(width=0, height=0)
root.geometry("350x350")
root.minsize(350, 350)
root.maxsize(350, 350)

img_path = ""
img_size = (0,0)

start_time = 0

def start_bruteforce():
    if not img_path:
        status_label.config(text="load an image first!", fg="red")
        return TypeError
    max_time = time_range.get()
    if max_time == '':
        status_label.config(text="pick a maximum time!", fg="red")
        return TypeError
    else:
        if not max_time.isdigit():
            status_label.config(text="use a number (sec) for max time!", fg="red")
            return TypeError
        max_time = int(max_time)
        if max_time < 1:
            status_label.config(text="use a positive number for max time!", fg="red")
            return TypeError

    chars = list(string.ascii_letters)
    global start_time
    start_time = time.time()
    print(start_time)
    #check all possible combinations of length 1-50
    for length in range(0, 50):
        if time.time() - start_time > max_time:
            break
        status_label.config(text=f"increasing to length {length}", fg="white")
        print("Starting with length", length)
        #individual length check
        for combo in itertools.product(chars, repeat=length):
            if time.time() - start_time > max_time:
                break
            try_string = ''.join(combo)
            try:
                print("attempt: " + try_string)
                msg = steganoengine.decode(img_path, try_string)
                return try_string
            except ValueError:
                pass
        # we will eventually iterate through all possible combos of that length, so we increment
        print("Exhausted length", length)
    print("couldn't find key in max time")
    return None

def show_results():
    cracked_key = start_bruteforce()
    #returned on invalid max time
    if cracked_key is TypeError:
        return
    if cracked_key is None:
        messagebox.showinfo("ERROR", "couldn't find key in specified time!", icon="info")
        return
    print(f"finished bruteforcing after {round(time.time() - start_time, 2)} seconds")
    messagebox.showinfo("cracked:", cracked_key, icon="info")
    choice = messagebox.askquestion("", "copy to clipboard?", icon="question")
    if choice == "yes":
        send_to_clipboard(cracked_key)

def load_image():
    global img_path
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpeg")])
    if not path:
        status_label.config(text="operation canceled.", fg="red")
        return

    global preview_img
    global img_size

    try:
        new_pil = Image.open(path)
        img_size = new_pil.size
        new_pil = new_pil.resize((128, 128))
    except Exception:
        status_label.config(text="failed to load!", fg="red")
        return
    else:
        img_path = path
        status_label.config(text="image loaded!", fg="green")
        preview_img = ImageTk.PhotoImage(new_pil)
        preview_panel.config(image=preview_img)
        print("Loaded from ", path)

def send_to_clipboard(msg):
    root.clipboard_clear()
    root.clipboard_append(msg)


load_button = tk.Button(root, text="Load image", command=load_image, bg="black", fg="white", activebackground="black",
                        activeforeground="gray40")
brute_button = tk.Button(root, text="Bruteforce key", command=show_results, bg="black", fg="white", activebackground="black",
                        activeforeground="gray40")
#program lags too much for this to work so im just going to remove it
#stop_button = tk.Button(root, text="Stop bruteforce", command=stop_bruteforce, bg="black", fg="white", activebackground="black",
#                        activeforeground="gray40")

time_label = tk.Label(root, text="max attempt time (sec):", bg="black", fg="white")
time_range = tk.Entry(root, bg="gray20", fg="white", insertbackground="white", width=30)

msg_label = tk.Label(root, text="Message:", bg="black", fg="white")
msg_text = tk.Text(root, height=5, width=30, bg="gray20", fg="white", insertbackground="white")

status_label = tk.Label(root, text="No image loaded", bg="black", fg="lightgreen", justify="left")

##if we can't find example.png, just draw a white square -asher
try:
    PIL_input = Image.open("example.png").resize((128, 128))
except FileNotFoundError:
    PIL_input = Image.new("RGB", (128, 128), "white")
preview_img = ImageTk.PhotoImage(PIL_input)

preview_panel = tk.Label(root, image=preview_img, bg="black")
preview_panel.image = preview_img

##widget deployment
preview_panel.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

load_button.grid(row=1, column=0, padx=5, pady=10, sticky="w")
brute_button.grid(row=1, column=1, padx=0, pady=10, sticky="w")
#stop_button.grid(row=1, column=1, padx=5, pady=10, sticky="e")

time_label.grid(row=3, column=0, padx=10, pady=(5, 5), sticky="w")
time_range.grid(row=3, column=1, padx=10, pady=(10, 5), sticky="w")

status_label.grid(row=5, column=0, padx=(5, 0), pady=(0, 15), sticky="w")

root.mainloop()
