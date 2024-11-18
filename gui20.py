import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2
from lsb import lsbCoding, lsbDecoding, convertToBinary, convertImage, convertToString  # Twoje metody LSB
from dct import codeExampleMessageDCT
from readDCT import dctDecoding  # Twoje metody DCT

class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography App")
        
        # Dodaj tytuł
        title = tk.Label(root, text="Steganography", font=("Helvetica", 16))
        title.pack(pady=10)

        # Dodaj opcję wyboru
        self.choose_option()

    def choose_option(self):
        self.clear_window()

        # Wybór: Kodowanie lub Odkodowanie
        self.option_label = tk.Label(self.root, text="Choose an option:", font=("Helvetica", 12))
        self.option_label.pack(pady=5)

        self.encode_button = tk.Button(self.root, text="Encode Message", command=self.encode_message)
        self.encode_button.pack(pady=5)

        self.decode_button = tk.Button(self.root, text="Decode Message", command=self.decode_message)
        self.decode_button.pack(pady=5)

    def encode_message(self):
        self.clear_window()
        
        # Wybór obrazu
        self.select_image_label = tk.Label(self.root, text="Select an image to encode the message:", font=("Helvetica", 12))
        self.select_image_label.pack(pady=5)

        self.select_image_button = tk.Button(self.root, text="Select Image", command=self.select_image_for_encoding)
        self.select_image_button.pack(pady=5)

    def select_image_for_encoding(self):
        # Wybór obrazu
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if self.image_path:
            self.get_message_to_encode()

    def get_message_to_encode(self):
        # Okno do wprowadzenia wiadomości
        self.clear_window()
        
        self.message_label = tk.Label(self.root, text="Enter the message to encode:", font=("Helvetica", 12))
        self.message_label.pack(pady=5)

        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.pack(pady=5)

        self.encoding_method_label = tk.Label(self.root, text="Choose encoding method:", font=("Helvetica", 12))
        self.encoding_method_label.pack(pady=5)

        self.method_var = tk.StringVar(value="lsb")  # Domyślnie LSB
        lsb_radio = tk.Radiobutton(self.root, text="LSB", variable=self.method_var, value="lsb")
        lsb_radio.pack(pady=5)

        dct_radio = tk.Radiobutton(self.root, text="DCT", variable=self.method_var, value="dct")
        dct_radio.pack(pady=5)

        self.encode_button = tk.Button(self.root, text="Encode", command=self.encode)
        self.encode_button.pack(pady=10)

    def encode(self):
        message = self.message_entry.get()
        if not message:
            messagebox.showerror("Error", "Please enter a message!")
            return
        
        message_in_binary = convertToBinary(message)
        
        if self.method_var.get() == "lsb":
            # Używamy metody LSB
            _, img = convertImage(self.image_path)
            _, stego_image = lsbCoding(img, message_in_binary)
            output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if output_path:
                stego_image.save(output_path)
                messagebox.showinfo("Success", f"Message encoded successfully and saved to {output_path}")
        elif self.method_var.get() == "dct":
            # Używamy metody DCT
            output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if output_path:
                codeExampleMessageDCT(self.image_path, output_path)
                messagebox.showinfo("Success", f"Message encoded successfully and saved to {output_path}")

        # Powrót do głównego okna
        self.choose_option()

    def decode_message(self):
        self.clear_window()

        # Wybór obrazu do odkodowania
        self.select_image_label = tk.Label(self.root, text="Select an image to decode the message:", font=("Helvetica", 12))
        self.select_image_label.pack(pady=5)

        self.select_image_button = tk.Button(self.root, text="Select Image", command=self.select_image_for_decoding)
        self.select_image_button.pack(pady=5)

    def select_image_for_decoding(self):
        self.stego_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if self.stego_image_path:
            self.decode_method_choice()

    def decode_method_choice(self):
        self.clear_window()
        
        self.decode_method_label = tk.Label(self.root, text="Choose decoding method:", font=("Helvetica", 12))
        self.decode_method_label.pack(pady=5)

        self.method_var = tk.StringVar(value="lsb")  # Domyślnie LSB
        lsb_radio = tk.Radiobutton(self.root, text="LSB", variable=self.method_var, value="lsb")
        lsb_radio.pack(pady=5)

        dct_radio = tk.Radiobutton(self.root, text="DCT", variable=self.method_var, value="dct")
        dct_radio.pack(pady=5)

        check_button = tk.Button(self.root, text="Check All Methods", command=self.decode_message_action)
        check_button.pack(pady=10)

    def decode_message_action(self):
        if self.method_var.get() == "lsb":
            # Odczyt za pomocą LSB
            try:
                message = lsbDecoding(self.stego_image_path)
                message = convertToString(message)
                messagebox.showinfo("Decoded Message", f"Decoded message: {message}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decode message: {str(e)}")
        elif self.method_var.get() == "dct":
            # Odczyt za pomocą DCT
            try:
                message = dctDecoding(self.stego_image_path)
                messagebox.showinfo("Decoded Message", f"Decoded message: {message}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decode message: {str(e)}")

        # Powrót do głównego okna
        self.choose_option()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()
