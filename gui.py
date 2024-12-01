import tkinter as tk
from customtkinter import *
from PIL import Image, ImageTk
import cv2
import json
import lsb
import randomly_lsb as rlsb
import msb
import pixelmsb
import huffman
import dct
import readDCT
import fmm

class StegoApp(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x700")
        self.title("Image Steganography App")
        self._set_appearance_mode("dark")
        # self.configure(fg_color="#432E54")
        set_default_color_theme("dark-blue")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=0)

        self.image_label = None
        self.loaded_image = None
        self.saved_input = ""
        self.filepath = ""

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
        
        self.help_button = CTkButton(
            master=self,
            text="?",
            width=30,
            fg_color="#748CAB",
            hover_color="#F0EBD8",
            border_color="#748CBB",
            bg_color="#242424",
            text_color="#242424",
            command=self.show_help
        )

        self.button1.grid(row=0, column=0, padx=0, pady=(0, 0), sticky="nsew")
        self.button2.grid(row=0, column=1, padx=0, pady=(0, 0), sticky="nsew")
        self.help_button.grid(row=1, column=0, padx=(0, 10), pady=0, sticky="sw")
        self.button3.grid(row=2, columnspan=2, padx=150, pady=(10, 40), sticky="new")

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
        
        self.combobox = CTkComboBox(master=self, 
                               values=["LSB", "Random LSB", "LSB+Huffman", "MSB", "Pixel MSB", "DCT", "FMM"], 
                               fg_color="#F0EBD8",
                               bg_color="#242424",
                               border_width=2, 
                               border_color="#748CBB", 
                               dropdown_fg_color="#F4989C")
        
        self.button4 = CTkButton(master=self, 
                            text="Zakoduj", 
                            fg_color="#F18F01",
                            bg_color="#242424",
                            border_width=2, 
                            border_color="#F18F11",
                            text_color="#242424",
                            hover_color="#F0EBD8",  
                            command=self.encode)
        
        label.grid(row=3, columnspan=2, padx=50, pady=(0, 10), sticky="nsew")
        self.textbox.grid(row=4, columnspan=2, padx=50, pady=(0, 40), sticky="nsew")
        label2.grid(row=5, columnspan=2, padx=150, pady=(0, 10), sticky="nsew")
        self.combobox.grid(row=6, columnspan=2, padx=150, pady=(0, 40), sticky="nsew")
        self.button4.grid(row=7, columnspan=2, padx=150, pady=(0, 50), sticky="senw")

        self.current_view.extend([label, self.textbox, label2, self.combobox, self.button4])


    def create_decode_view(self):
        self.clear_view()
        self.current_view = []
        
        label2 = CTkLabel(master=self, 
                         text="Wybierz opcję",
                         fg_color="#748CAB",
                         bg_color="#242424",
                         text_color="#242424")
        
        self.combobox_dec = CTkComboBox(master=self, 
                                    values=["LSB", "Random LSB", "LSB+Huffman", "MSB", "Pixel MSB", "DCT", "FMM"], 
                                    fg_color="#F0EBD8",
                                    bg_color="#242424",
                                    border_width=2, 
                                    border_color="#748CBB", 
                                    dropdown_fg_color="#F4989C")

        self.button5 = CTkButton(master=self, 
                            text="Odczytaj", 
                            fg_color="#F18F01",
                            bg_color="#242424",
                            border_width=2, 
                            border_color="#F18F11",
                            text_color="#242424",
                            hover_color="#F0EBD8",  
                            command=self.decode)
        
        label2.grid(row=10, columnspan=2, padx=150, pady=(0, 10), sticky="nsew")
        self.combobox_dec.grid(row=11, columnspan=2, padx=150, pady=(0, 40), sticky="sew")
        self.button5.grid(row=12, columnspan=2, padx=150, pady=(0, 50), sticky="sew")

        self.current_view.extend([label2, self.combobox_dec, self.button5])
        

    def select_image(self):
        # Pozwala użytkownikowi wybrać obraz i wyświetla go.
        self.filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if self.filepath:
            self.display_image(self.filepath)
        

    def display_image(self, filepath):
        # Wyświetla obraz nad przyciskiem.
        image = Image.open(filepath)
        image = image.resize((200, 200))  # Zmiana rozmiaru obrazu
        self.loaded_image = ImageTk.PhotoImage(image)

        if self.image_label:
            self.image_label.destroy()  # Usuwamy poprzedni obraz, jeśli istnieje

        self.image_label = CTkLabel(master=self, image=self.loaded_image, text="")
        self.image_label.grid(row=1, column=0, columnspan=2, padx=150, pady=10, sticky="nsew")


    def encode(self):
        input_message = self.textbox.get()
        input_method = self.combobox.get()

        if not input_message:
            tk.messagebox.showerror("Błąd", "Wprowadź wiadomość do zakodowania.")
            return
        
        if not self.filepath:
            tk.messagebox.showerror("Błąd", "Wprowadź obraz do zakodowania wiadomości.")
            return
        
        if input_method == "LSB":
            try:
                stego_img = lsb.codeMessageLSB(self.filepath, input_message)
                self.saveStegoImage(stego_img)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się zakodować wiadomości {str(e)}")
                return
            
        elif input_method == "Random LSB":
            try:
                stego_img = rlsb.codeMessageRandomLSB(self.filepath, input_message)
                self.saveStegoImage(stego_img)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się zakodować wiadomości {str(e)}")
                return
            
        elif input_method == "MSB":
            try:
                stego_img = msb.codeMessageMSB(self.filepath, input_message)
                self.saveStegoImage(stego_img)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się zakodować wiadomości {str(e)}")
                return
        
        elif input_method == "Pixel MSB":
            try:
                stego_img = pixelmsb.codeMessagePixelMSB(self.filepath, input_message)
                self.saveStegoImage(stego_img)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się zakodować wiadomości {str(e)}")
                
        elif input_method == "DCT":
            try:
                stego_img = dct.codeMessageDCT(self.filepath, input_message)
                self.saveStegoImage(stego_img, dct=True)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się zakodować wiadomości {str(e)}")
                return
            
        elif input_method == "LSB+Huffman":
            try:
                stego_img, huffman_table = huffman.codeMessageHuffman(self.filepath, input_message)
                self.saveStegoImage(stego_img)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się zakodować wiadomości {str(e)}")
                return
            
            path_huffman = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Image Files", "*.txt")])
            if path_huffman:
                # huffman_table.save(path_huffman)
                with open(path_huffman, 'w') as f:
                    f.write(json.dumps(huffman_table))

                tk.messagebox.showinfo("Sukces", f"Udało się zapisać tablicę Huffmana: {os.path.basename(path_huffman)}")
            else:
                tk.messagebox.showerror("Błąd", f"Nie udało się zapisać tablicy Huffmana")

        elif input_method == "FMM":
            self.show_fmm_options(input_message)

            
            

    def decode(self):
        method = self.combobox_dec.get()
        if not self.filepath:
            tk.messagebox.showerror("Błąd", "Wprowadź obraz do odczytania wiadomości")
            return
        
        if method == "LSB":
            try:
                mess = lsb.decodeMessageLSB(self.filepath)
                self.diplayDecodedMessage(mess)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się odczytać wiadomości {str(e)}")
                return
        
        elif method == "Random LSB":
            try:
                mess = rlsb.decodeMessageRandomLSB(self.filepath)
                self.diplayDecodedMessage(mess)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się odczytać wiadomości {str(e)}")
                return
            
        elif method == "MSB":
            try:
                mess = msb.decodeMessageMSB(self.filepath)
                self.diplayDecodedMessage(mess)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się odczytać wiadomości {str(e)}")
                return
            
        elif method == "Pixel MSB":
            try:
                mess = pixelmsb.decodeMessagePixelMSB(self.filepath)
                self.diplayDecodedMessage(mess)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się odczytać wiadomości {str(e)}")
                return
            
        elif method == "DCT":
            try:
                mess = readDCT.decodeMessageDCT(self.filepath)
                self.diplayDecodedMessage(mess)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się odczytać wiadomości {str(e)}")
                return
            
        elif method == "LSB+Huffman":
            try:
                path_huffman = filedialog.askopenfilename(
                    filetypes=[("Text Files", "*.txt")])
                
                with open(path_huffman, 'r') as fi:
                    table = fi.read()
                    try:
                        dir_huffman_table = json.loads(table)
                    except Exception:
                        tk.messagebox.showerror("Błąd", f"Niepoprawny format pliku z tablicą Huffmana! Podaj inny plik.")
                        return

                mess = huffman.decodeMessageHuffman(dir_huffman_table, self.filepath)
                self.diplayDecodedMessage(mess)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się odczytać wiadomości {str(e)}")
                return
        
        elif method == "FMM":
            self.show_fmm_options(decode=True)


    def saveStegoImage(self, steg_img, dct=False):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Image Files", "*.png;*.bmp;*.gif")]
        )
        if save_path:
            if dct:
                cv2.imwrite(save_path, steg_img)
            else:
                steg_img.save(save_path)
            tk.messagebox.showinfo("Sukces", f"Stego-obraz zapisany jako: {os.path.basename(save_path)}")
        else:
            tk.messagebox.showerror("Błąd", f"Nie udało się zapisać obrazu")


    def diplayDecodedMessage(self, message):
        if message:
            tk.messagebox.showinfo("Sukces", f"Odczytana wiadomość: {str(message)}")
        else:
            tk.messagebox.showerror("Błąd", f"Nie udało się odczytać wiadomości")


    def ffmCoding(self, input_message, k, start_index):
        try:
            stego_img = fmm.codeMessageFMM(self.filepath, input_message, k, start_index)
            self.saveStegoImage(stego_img, dct=False)
        except Exception as e:
            tk.messagebox.showerror("Błąd", f"Nie udało się zakodować wiadomości {str(e)}")
            return


    def show_fmm_options(self, input_message="", decode=False):
        self.clear_view()
        self.current_view = []

        image_path = "tab_max.png"  # Ścieżka do Twojego obrazu
        try:
            image = Image.open(image_path)
            image = image.resize((200, 200))  # Dostosowanie rozmiaru obrazu
            fmm_image = ImageTk.PhotoImage(image)
        except Exception as e:
            tk.messagebox.showerror("Błąd", f"Nie udało się wczytać obrazu: {str(e)}")
            return
        
        image_label = CTkLabel(master=self, image=fmm_image, text="")
        image_label.grid(row=7, columnspan=2, padx=150, pady=(0, 10), sticky="nsew")
        self.current_view.append(image_label)

        label = CTkLabel(master=self, text="Wybierz opcję dla FMM", fg_color="#748CAB", bg_color="#242424", text_color="#242424")
        label.grid(row=8, columnspan=2, padx=50, pady=(10, 10), sticky="nsew")
        self.current_view.append(label)

        # Tworzymy RadioButtony
        self.radio_var = tk.StringVar(value="opcja 1")  # Domyślnie opcja 1
 
        radio_button1 = CTkRadioButton(master=self, text="opcja 1 (ze zdjęcia)", variable=self.radio_var, value="opcja 1", text_color="#748CAB", bg_color="#242424", fg_color="#748CAB")
        radio_button1.grid(row=9, columnspan=2, padx=50, pady=(5, 5), sticky="w")
        self.current_view.append(radio_button1)

        radio_button2 = CTkRadioButton(master=self, text="opcja 2 (same cyfry)", variable=self.radio_var, value="opcja 2", text_color="#748CAB", bg_color="#242424", fg_color="#748CAB")
        radio_button2.grid(row=10, columnspan=2, padx=50, pady=(5, 5), sticky="w")
        self.current_view.append(radio_button2)

        radio_button3 = CTkRadioButton(master=self, text="opcja 3 (małe litery)", variable=self.radio_var, value="opcja 3", text_color="#748CAB", bg_color="#242424", fg_color="#748CAB")
        radio_button3.grid(row=11, columnspan=2, padx=50, pady=(5, 5), sticky="w")
        self.current_view.append(radio_button3)

        # Dodajemy przycisk do zakodowania wiadomości
        if decode:
            decode_button = CTkButton(
            master=self,
            text="Zakoduj wiadomość",
            fg_color="#F18F01",
            bg_color="#242424",
            border_width=2,
            border_color="#F18F11",
            text_color="#242424",
            hover_color="#F0EBD8",
            command=lambda: self.en_decode_fmm(decode=True)
            )
            decode_button.grid(row=12, columnspan=2, padx=50, pady=(20, 50), sticky="nsew")
            self.current_view.append(decode_button)

        else:
            encode_button = CTkButton(
                master=self,
                text="Zakoduj wiadomość",
                fg_color="#F18F01",
                bg_color="#242424",
                border_width=2,
                border_color="#F18F11",
                text_color="#242424",
                hover_color="#F0EBD8",
                command=lambda: self.en_decode_fmm(input_message)
            )
            encode_button.grid(row=12, columnspan=2, padx=50, pady=(20, 50), sticky="nsew")
            self.current_view.append(encode_button)


    def en_decode_fmm(self, input_message="", decode=False):
        selected_option = self.radio_var.get()

        # Ustawienia dla FMM w zależności od wybranej opcji
        if selected_option == "opcja 1":
            k, start_index = 5, 32
        elif selected_option == "opcja 2":
            k, start_index = 2, 48
        elif selected_option == "opcja 3":
            k, start_index = 3, 97
        else:
            tk.messagebox.showerror("Błąd", "Nie wybrano poprawnej opcji!")
            return
        
        if decode:
            try:
                mess = fmm.decodeMessageFFM(self.filepath, k, start_index)
                self.diplayDecodedMessage(mess)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się zakodować wiadomości: {str(e)}")
                return
            
        else:
            try:
                stego_img = fmm.codeMessageFMM(self.filepath, input_message, k, start_index)
                self.saveStegoImage(stego_img, dct=False)
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się zakodować wiadomości: {str(e)}")   


    def show_help(self):
        # Funkcja otwiera okno pomocy
        try:
            with open('help_final.txt', 'r', encoding='utf-8') as f:
                help_text = f.read()
            
            help_window = CTkToplevel(self)
            help_window.geometry("600x400")
            help_window.title("Pomoc")

            text_widget = CTkTextbox(help_window, wrap="word")
            text_widget.insert("1.0", help_text)
            text_widget.configure(state="disabled")  # Uniemożliwia edytowanie
            text_widget.pack(expand=True, fill="both", padx=10, pady=10)
        except Exception as e:
            tk.messagebox.showerror("Błąd", f"Nie udało się załadować pliku pomocy: {str(e)}")
    

        

if __name__ == "__main__":
    # Tworzymy aplikację
    app = StegoApp()
    # Aby aplikacja wyświetlała się cały czas
    app.mainloop()
