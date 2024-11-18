import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import randomly_lsb  # Importujemy funkcje z random_LSB.py
import lsb  # Importujemy funkcje z lsb.py
import os

# Funkcja do wyboru obrazu
def load_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        global image_path
        image_path = file_path
        img = Image.open(file_path)
        img.thumbnail((200, 200))  # Skaluje obraz, żeby zmieścił się w oknie
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

# Funkcja do kodowania wiadomości w obrazie
def encode_message():
    global image_path
    message = message_entry.get()  # Pobieramy wiadomość od użytkownika
    method = method_combobox.get()  # Pobieramy metodę wybraną przez użytkownika

    if not image_path or not message:
        messagebox.showerror("Błąd", "Proszę wczytać obraz i wpisać wiadomość.")
        return

    if method == "Klasyczna LSB":
        try:
            _, img = lsb.convertImage(image_path)
            message_in_binary = lsb.convertToBinary(message)
            _, stego_img = lsb.lsbCoding(img, message_in_binary)
            save_stego_image(stego_img, image_path)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zakodować wiadomości: {str(e)}")

    elif method == "Random LSB":
        try:
            _, img = randomly_lsb.convertImage(image_path)
            step = randomly_lsb.calculateStep(len(message), img)
            header_in_binary, message_in_binary = randomly_lsb.convertToBinary(message, step)
            _, stego_img = randomly_lsb.lsbCoding(img, message_in_binary, header_in_binary, step)
            save_stego_image(stego_img, image_path)
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zakodować wiadomości: {str(e)}")
    else:
        messagebox.showerror("Błąd", "Proszę wybrać metodę kodowania.")

# Funkcja do zapisu obrazu z zakodowaną wiadomością
def save_stego_image(stego_img, original_image_path):
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        stego_img.save(save_path)
        messagebox.showinfo("Sukces", f"Stego-obraz zapisany jako: {os.path.basename(save_path)}")
    else:
        messagebox.showerror("Błąd", "Nie udało się zapisać obrazu.")

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Steganografia w obrazach")
root.geometry("400x400")

# Nagłówek aplikacji
header = tk.Label(root, text="Steganografia w obrazach", font=("Helvetica", 16))
header.pack(pady=10)

# Przyciski i pola do wczytania obrazu
image_frame = tk.Frame(root)
image_frame.pack(pady=10)

image_button = tk.Button(image_frame, text="Wczytaj obraz", command=load_image)
image_button.pack(side=tk.LEFT)

image_label = tk.Label(image_frame)
image_label.pack(side=tk.RIGHT)

# Pole tekstowe do wpisania wiadomości
message_label = tk.Label(root, text="Wpisz wiadomość do ukrycia:")
message_label.pack(pady=10)

message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=5)

# Wybór metody kodowania
method_label = tk.Label(root, text="Wybierz metodę kodowania:")
method_label.pack(pady=10)

method_combobox = ttk.Combobox(root, values=["Klasyczna LSB", "Random LSB"])
method_combobox.pack(pady=5)
method_combobox.current(0)

# Przyciski do rozpoczęcia kodowania
encode_button = tk.Button(root, text="Zakoduj wiadomość", command=encode_message)
encode_button.pack(pady=20)

# Uruchomienie aplikacji
root.mainloop()
