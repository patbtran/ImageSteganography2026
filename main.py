import tkinter as tk
import steganoengine
import hasher
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

root = tk.Tk()

root.title("steganographer | release build")
root.configure(background="black")
root.resizable(width=0, height=0)
root.geometry("400x400")
root.minsize(400, 400)
root.maxsize(400, 400)

img_path = ""
img_size = (0,0)

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


def save_image():
    if len(img_path) == 0:
        status_label.config(text="load an image first!", fg="red")
        return
    msg = msg_text.get("1.0", "end-1c")  # get our hidden message text from the message box
    key = key_value.get()  # get key from key entry

    ##dry run that will generate a similar output to the real encryption,
    ##using this to check if the encrypted message will fit in the image! -asher
    key_hash = steganoengine.sha256(key.encode("utf-8")).digest()
    encrypted_txt = hasher.encrypt(msg, key_hash)

    if len(encrypted_txt) > max_hiding_chars(*img_size):
        messagebox.showerror("FATAL ERROR!", "Image is too small for message!")
        status_label.config(text="message is too big!", fg="red")
        return

    if len(key) == 0:
        choice = messagebox.askquestion("WARNING",
        "you haven't provided a key, are you sure about this?", icon="warning")

        if choice == "no":
            status_label.config(text="no key provided!", fg="red")
            return

    ##open a filedialog where the user can choose the save path
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image files", "*.png *.jpeg")])

    if save_path:
        print("Saving to ", save_path)
        steganoengine.encode(img_path, msg, key, save_path)
        status_label.config(text="secret message saved!", fg="green")
    else:
        status_label.config(text="operation canceled.", fg="red")


def decode_image():
    key = key_value.get()

    if not img_path:
        status_label.config(text="load an image first!", fg="red")
        return

    try:
        decoded_message = steganoengine.decode(img_path, key)
    ##this gets thrown if the key doesn't work!
    except ValueError:
        status_label.config(text="bad key.", fg="red")
        messagebox.showinfo("error", "invalid key or bad image!")
        return
    else:
        status_label.config(text="message decoded!", fg="green")
        ##display decoded message
        messagebox.showinfo("decoded message:", decoded_message, icon="info")
        choice = messagebox.askquestion("", "copy to clipboard?", icon="question")
        if choice == "yes":
            send_to_clipboard(decoded_message)


def send_to_clipboard(msg):
    root.clipboard_clear()
    root.clipboard_append(msg)

def max_hiding_chars(w,h):
    return (w * h) // 3 # 1 character needs 3 pixels. 8 bits for the char, 1 bit for the end flag.

##widgets
load_button = tk.Button(root, text="Load image", command=load_image)
save_button = tk.Button(root, text="Encode image", command=save_image, bg="black", fg="white", activebackground="black",
                        activeforeground="gray40")

key_label = tk.Label(root, text="Key:", bg="black", fg="white")
key_value = tk.Entry(root, bg="gray20", fg="white", insertbackground="white", width=30)
decode_button = tk.Button(root, text="Decode loaded file", command=decode_image, bg="black", fg="white",
                          activebackground="black", activeforeground="gray40")

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

load_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
save_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

decode_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

key_label.grid(row=3, column=0, padx=10, pady=(5, 5), sticky="ew")
key_value.grid(row=3, column=1, padx=10, pady=(10, 5), sticky="ew")

msg_label.grid(row=4, column=0, padx=10, pady=(5, 5), sticky="ew")
msg_text.grid(row=4, column=1, padx=10, pady=(5, 5), sticky="ew")

status_label.grid(row=5, column=0, padx=(5, 0), pady=(0, 15), sticky="ew")

root.mainloop()