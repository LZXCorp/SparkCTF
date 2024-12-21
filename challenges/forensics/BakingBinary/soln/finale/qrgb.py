import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from PIL import Image, ImageTk
import qrcode
import os
import cv2

# Function to create a QR code with a superimposed logo
def create_qr_with_logo(data, color, logo_path, qr_version=10, box_size=10):
    qr = qrcode.QRCode(
        version=qr_version,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="white").convert('RGBA')
    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logo file not found: {logo_path}")
    logo = Image.open(logo_path).convert("RGBA")
    basewidth = img.size[0] // 4
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.LANCZOS)
    pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
    img.paste(logo, pos, logo)
    return img

# Combine QR images ensuring they all have the same size
def combine_qr_images(img1, img2, img3, logo_path):
    size = img1.size
    if img2.size != size or img3.size != size:
        raise ValueError("All QR images must be the same size")
    final_image = Image.new("RGBA", size, "black")
    data_red = img1.getdata()
    data_green = img2.getdata()
    data_blue = img3.getdata()
    new_data = []
    for i in range(len(data_red)):
        r1, g1, b1, a1 = data_red[i]
        red_pixel = (r1, g1, b1) != (255, 255, 255)
        r2, g2, b2, a2 = data_green[i]
        green_pixel = (r2, g2, b2) != (255, 255, 255)
        r3, g3, b3, a3 = data_blue[i]
        blue_pixel = (r3, g3, b3) != (255, 255, 255)
        if red_pixel and green_pixel and blue_pixel:
            new_data.append((255, 255, 255, 255))
        elif red_pixel and green_pixel:
            new_data.append((255, 255, 0, 255))
        elif red_pixel and blue_pixel:
            new_data.append((255, 0, 255, 255))
        elif green_pixel and blue_pixel:
            new_data.append((0, 255, 255, 255))
        elif red_pixel:
            new_data.append((255, 0, 0, 255))
        elif green_pixel:
            new_data.append((0, 255, 0, 255))
        elif blue_pixel:
            new_data.append((0, 0, 255, 255))
        else:
            new_data.append((0, 0, 0, 255))
    final_image.putdata(new_data)
    logo = Image.open(logo_path).convert("RGBA")
    basewidth = final_image.size[0] // 4
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.LANCZOS)
    pos = ((final_image.size[0] - logo.size[0]) // 2, (final_image.size[1] - logo.size[1]) // 2)
    final_image.paste(logo, pos, logo)
    return final_image

def show_qrgb_image(img):
    top = tk.Toplevel()
    top.title("QRGB Code")
    img = img.resize((300, 300), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    lbl = tk.Label(top, image=img_tk)
    lbl.image = img_tk
    lbl.pack(pady=20)
    top.mainloop()

# Function to read a QR code from an image
def read_qr(filename):
    img = cv2.imread(filename)
    detector = cv2.QRCodeDetector()
    data, vertices_array, _ = detector.detectAndDecode(img)
    if vertices_array is not None:
        return data
    else:
        return None

# Function to manually decode the superimposed QR
def manual_decode_superposed_qr(filename):
    superposed_img = Image.open(filename)
    superposed_data = superposed_img.getdata()
    size = superposed_img.size
    red_data = [(255, 255, 255, 255)] * len(superposed_data)
    green_data = [(255, 255, 255, 255)] * len(superposed_data)
    blue_data = [(255, 255, 255, 255)] * len(superposed_data)
    for i in range(len(superposed_data)):
        r, g, b, a = superposed_data[i]
        if r != 0:  # Red
            red_data[i] = (0, 0, 0, 255)
        if g != 0:  # Green
            green_data[i] = (0, 0, 0, 255)
        if b != 0:  # Blue
            blue_data[i] = (0, 0, 0, 255)
    print(f"Current working directory: {os.getcwd()}")
    red_img = Image.new("RGBA", size)
    green_img = Image.new("RGBA", size)
    blue_img = Image.new("RGBA", size)
    red_img.putdata(red_data)
    green_img.putdata(green_data)
    blue_img.putdata(blue_data)
    red_img.save("decoded_red.png")
    green_img.save("decoded_green.png")
    blue_img.save("decoded_blue.png")
    data_red = read_qr("decoded_red.png")
    data_green = read_qr("decoded_green.png")
    data_blue = read_qr("decoded_blue.png")
    return data_red, data_green, data_blue

def decode_qr():
    root.withdraw()
    qr_filename = filedialog.askopenfilename(
        title="Select the superimposed QRGB code",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    if qr_filename:
        try:
            data_red, data_green, data_blue = manual_decode_superposed_qr(qr_filename)
            # Show the decoded data in the popup window
            response = messagebox.askokcancel(
                "Decoding successful",
                f"Red layer data: {data_red}\nGreen layer data: {data_green}\nBlue layer data: {data_blue}\n\nDo you want to print this data to the console?"
            )
            if response:
                # Show the decoded data in the console
                print(f"Red layer data: {data_red}")
                print(f"Green layer data: {data_green}")
                print(f"Blue layer data: {data_blue}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("File not selected", "Please select a QR code file.")
    root.deiconify()

# Function to show the main menu
def show_main_menu():
    root.withdraw()
    top = tk.Toplevel()
    top.title("Select option")
    label = tk.Label(top, text="Select an option:", font=("Arial", 14))
    label.pack(pady=10)
    btn_decode = tk.Button(top, text="Decode QRGB", command=open_decode_menu, font=("Arial", 12))
    btn_decode.pack(pady=5)
    top.mainloop()

# Function to open the QRGB decoding window
def open_decode_menu():
    decode_qr()

# GUI configuration
root = tk.Tk()
root.title("QRGB Generator and Decoder")
show_main_menu()  # Show the main menu at startup
root.mainloop()
