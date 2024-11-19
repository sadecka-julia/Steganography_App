import tkinter as tk
from customtkinter import *
from PIL import Image, ImageTk

class StegoApp(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x600")
        self.title("Image Steganography App")
        self._set_appearance_mode("dark")
        # self.configure(fg_color="#432E54")
        set_default_color_theme("dark-blue")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=0)

        self.image_label = None
        self.loaded_image = None
        self.saved_input = ""

        self.button1 = CTkButton(master=self, 
                                text="Zakoduj wiadomość",
                                width=200, 
                                fg_color="#F18F01", 
                                hover_color="#F0EBD8", 
                                border_color="#F18F01", 
                                bg_color="#242424",
                                border_width=2,
                                text_color="#242424", 
                                command=self.create_encode_view)
        
        self.button2 = CTkButton(master=self, 
                                text="Odczytaj wiadomość",
                                width=200, 
                                fg_color="#F18F01", 
                                hover_color="#F0EBD8", 
                                border_color="#F18F01", 
                                bg_color="#242424",
                                border_width=2,
                                text_color="#242424", 
                                command=self.create_decode_view)
        
        self.button3 = CTkButton(master=self, 
                                text="Wybierz zdjęcie", 
                                fg_color="#748CAB", 
                                hover_color="#F0EBD8", 
                                border_color="#748CBB", 
                                bg_color="#242424",
                                border_width=2,
                                text_color="#242424", 
                                command=self.select_image)

        self.button1.grid(row=0, column=0, padx=0, pady=(0, 0), sticky="nsew")
        self.button2.grid(row=0, column=1, padx=0, pady=(0, 0), sticky="nsew")
        self.button3.grid(row=2, columnspan=2, padx=150, pady=(10, 50), sticky="new")

        self.current_view = None


    def clear_view(self):
        """Usuwa aktualnie wyświetlane widżety."""
        if self.current_view:
            for widget in self.current_view:
                widget.destroy()
            self.current_view = None


    def button_callback(self):
        print("button pressed")


    def create_encode_view(self):
        self.clear_view()
        self.current_view = []

        label = CTkLabel(master=self, 
                         text="Wprowadź wiadomość do ukrycia",
                         fg_color="#748CAB",
                         bg_color="#242424",
                         text_color="#242424")
        
        self.textbox = CTkEntry(master=self, 
                             fg_color="#F0EBD8",
                             bg_color="#242424",
                             border_width=2, 
                             border_color="#748CBB",  
                             height=30)
        
        label2 = CTkLabel(master=self, 
                         text="Wybierz opcję",
                         fg_color="#748CAB",
                         bg_color="#242424",
                         text_color="#242424")
        
        combobox = CTkComboBox(master=self, 
                               values=["LSB", "Random LSB", "LSB+Huffman", "MSB", "Pixel MSB", "DCT", "FFT"], 
                               fg_color="#F0EBD8",
                               bg_color="#242424",
                               border_width=2, 
                               border_color="#748CBB", 
                               dropdown_fg_color="#F4989C")
        
        button4 = CTkButton(master=self, 
                            text="Zakoduj", 
                            fg_color="#F18F01",
                            bg_color="#242424",
                            border_width=2, 
                            border_color="#F18F11",
                            text_color="#242424",
                            hover_color="#F0EBD8",  
                            command=self.save_input)
        
        label.grid(row=3, columnspan=2, padx=50, pady=(0, 10), sticky="nsew")
        self.textbox.grid(row=4, columnspan=2, padx=50, pady=(0, 40), sticky="nsew")
        label2.grid(row=5, columnspan=2, padx=150, pady=(0, 10), sticky="nsew")
        combobox.grid(row=6, columnspan=2, padx=150, pady=(0, 40), sticky="nsew")
        button4.grid(row=7, columnspan=2, padx=150, pady=(0, 50), sticky="senw")

        self.current_view.extend([label, self.textbox, label2, combobox, button4])


    def create_decode_view(self):
        self.clear_view()
        self.current_view = []
        
        label2 = CTkLabel(master=self, 
                         text="Wybierz opcję",
                         fg_color="#748CAB",
                         bg_color="#242424",
                         text_color="#242424")
        
        combobox_dec = CTkComboBox(master=self, 
                                    values=["opc 1", "opc 2", "opc 3"], 
                                    fg_color="#F0EBD8",
                                    bg_color="#242424",
                                    border_width=2, 
                                    border_color="#748CBB", 
                                    dropdown_fg_color="#F4989C")

        button5 = CTkButton(master=self, 
                            text="Odczytaj", 
                            fg_color="#F18F01",
                            bg_color="#242424",
                            border_width=2, 
                            border_color="#F18F11",
                            text_color="#242424",
                            hover_color="#F0EBD8",  
                            command=self.button_callback)
        
        label2.grid(row=3, columnspan=2, padx=150, pady=(0, 10), sticky="nsew")
        combobox_dec.grid(row=4, columnspan=2, padx=150, pady=(0, 40), sticky="sew")
        button5.grid(row=5, columnspan=2, padx=150, pady=(0, 50), sticky="sew")

        self.current_view.extend([label2, combobox_dec, button5])
        
    def select_image(self):
        """Pozwala użytkownikowi wybrać obraz i wyświetla go."""
        filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if filepath:
            self.display_image(filepath)
        

    def display_image(self, filepath):
        """Wyświetla obraz nad przyciskiem."""
        image = Image.open(filepath)
        image = image.resize((200, 200))  # Zmiana rozmiaru obrazu
        self.loaded_image = ImageTk.PhotoImage(image)

        if self.image_label:
            self.image_label.destroy()  # Usuwamy poprzedni obraz, jeśli istnieje

        self.image_label = CTkLabel(master=self, image=self.loaded_image, text="")
        self.image_label.grid(row=1, column=0, columnspan=2, padx=150, pady=10, sticky="nsew")

    def save_input(self):
        """Zapisuje dane z pola wejściowego do zmiennej."""
        self.saved_input = self.textbox.get()
        print(str(self.saved_input))

if __name__ == "__main__":
    # Tworzymy aplikację
    app = StegoApp()
    # Aby aplikacja wyświetlała się cały czas
    app.mainloop()
