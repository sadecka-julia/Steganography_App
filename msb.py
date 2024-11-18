import math
import sys
import numpy as np
from PIL import Image


'''Zamienia wiadomość tekstową na binarną, aby mogła być zakodowana w pikselach obrazu.
Zwraca:
- Zakodowaną wiadomość w postaci binarnej.
'''
def convertToBinary(message):
    table_of_bin = []
    # Zakodowanie długości wiadomości jako liczba bitów
    len_of_message = (len(message) * 7)  # długość wiadomości w bitach
    len_of_message_bin = bin(len_of_message)[2:].zfill(20)  # konwersja na binarną postać długości z wypełnieniem do 49 bitów

    print(len_of_message, len_of_message_bin)
    # Dołączenie długości binarnej do wiadomości
    message_in_binary = len_of_message_bin

    # Konwersja każdego znaku na 7-bitową reprezentację
    for char in message:
        bin_repr = bin(ord(char))[2:].zfill(7)
        table_of_bin.append(bin_repr)

    for b in table_of_bin:
        message_in_binary += b
    print(message_in_binary)

    return message_in_binary


'''Zamienia binarną wiadomość na tekst.
Zwraca:
- Wiadomość w postaci tekstowej.
'''
def convertToString(message_in_binary):
    table_of_strings = []
    message = ""
    for char in range(0, len(message_in_binary), 7):
        table_of_strings.append(chr(int(message_in_binary[char:char+7], 2)))

    for i in table_of_strings:
        message += i

    return message


# Konwertuje obraz do macierzy numpy w celu manipulacji pikselami
def convertImage(path):
    img = Image.open(path)
    numpy_img = np.array(img)
    return img, numpy_img


def msbCoding(img, message):
    shape = img.shape     # Kształt obrazu
    size = img.size       # Rozmiar obrazu
    resized_img = img.reshape(-1)  # Zmienia macierz obrazu, aby była była jednowymiarowa
    pixel = 0             # Zmienna kontrolująca przesuwanie się po pikselach 
   
    for bit in message:
        data_bit = int(bit)

        # Odczytanie bitów nr 5 i nr 6
        bit_5 = (resized_img[pixel] >> 5) & 1
        bit_6 = (resized_img[pixel] >> 6) & 1
        difference = bit_5 ^ bit_6  # Różnica między bitem nr 5 i nr 6

        # Sprawdzenie różnicy z bitem tajnej informacji
        if difference != data_bit:
            # Jeśli różnica nie odpowiada bitowi danych, zmieniamy bit nr 5
            resized_img[pixel] ^= (1 << 5)  # Przełączenie bitu nr 5
    
        pixel += 1
        if pixel >= len(resized_img):  # Jeśli zabraknie miejsca
            print("Uwaga: Obraz jest za mały, aby zapisać całą wiadomość.")
            break

    new_img = resized_img.reshape(shape)
    pil_image = Image.fromarray(new_img)
    return new_img, pil_image


def msbDecoding(img_path):
    _, img = convertImage(img_path)
    message = ''
    resized_img = img.reshape(-1)
    #size_of_text = ''
    length_bits = ''
    # Odczyt wiadomości z pikseli
    for bit in range(0, 20):      # (2, 149, 3) - jeżeli chcemy zakodować wiadomość tylko w pikselach B (blue), wtedy należy zmeinić też pętlę poniżej (2, (size*3)+2, 3), a rakże w funkcji coding
        bit_5 = (resized_img[bit] >> 5) & 1
        bit_6 = (resized_img[bit] >> 6) & 1
        difference = bit_5 ^ bit_6
        length_bits += str(difference)

    message_length = int(length_bits, 2)

    # Odczyt ukrytej wiadomości
    for bit in range(20, 20 + message_length):
        bit_5 = (resized_img[bit] >> 5) & 1
        bit_6 = (resized_img[bit] >> 6) & 1
        difference = bit_5 ^ bit_6
        message += str(difference)

    return message


# Funkcja zakodowująca przykładową wiadomość w obrazie i zapisująca wynik do pliku
def codeExampleMessage(path):
    message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc at arcu lorem. Pellentesque iaculis, odio non volutpat consequat, velit lectus vehicula ipsum, a maximus metus tortor et metus. Donec massa elit, viverra id dignissim in, dignissim at ex. Suspendisse in faucibus nibh. Proin pretium sodales ante ut ultricies. Mauris vel diam iaculis, finibus tellus sit amet, convallis diam. Pellentesque et felis aliquam, finibus dolor at, commodo odio. In fringilla imperdiet lectus, eu rutrum ligula pulvinar nec. Sed malesuada tellus in sapien pellentesque pulvinar. Ut quis metus faucibus elit pretium aliquam. Vestibulum at nulla et risus tristique tincidunt. Nunc porttitor et eros feugiat consectetur. Suspendisse mauris elit, ultrices non risus nec, aliquet pretium purus. Vestibulum dignissim urna eget egestas porta. Aenean eget eros dapibus, fringilla nisi vel, tincidunt ex. Integer vitae vulputate nisi. Cras egestas sem lorem, vel maximus metus ultricies ac. Praesent lobortis egestas dignissim. Etiam porttitor faucibus erat. Curabitur dapibus sem at faucibus facilisis.Maecenas congue odio sed ultricies consectetur. Nullam venenatis orci ac diam maximus, nec elementum erat fermentum. Nullam nisl nibh, luctus id blandit at, luctus eu purus. Duis ultrices, velit eu consequat semper, arcu nisl dapibus elit, commodo egestas ante odio vitae justo. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse libero lectus, condimentum a eleifend pellentesque, ultrices a mi. Nam eu mi vehicula, porttitor eros varius, dictum justo. In fringilla vel purus eu ultrices. Donec imperdiet, nulla eget aliquam aliquet, diam eros iaculis erat, at venenatis nunc magna sollicitudin erat. Donec diam odio, hendrerit nec fermentum eu, fermentum non eros. Suspendisse sit amet augue nibh. Suspendisse eget magna at orci malesuada porttitor id et eros."
    _, message_in_binary = convertToBinary(message)
    _, img = convertImage(path)
    _, stego_img = msbCoding(img, message_in_binary)
    return stego_img

def codeInputMessage():
    message = input("Enter message to code in the image: \n")
    message_in_binary = convertToBinary(message)
    _, img = convertImage(path)
    img_with_info, stego_img = msbCoding(img, message_in_binary)
    return stego_img


if __name__ == '__main__':
    # message1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc at arcu lorem. Pellentesque iaculis, odio non volutpat consequat, velit lectus vehicula ipsum, a maximus metus tortor et metus. Donec massa elit, viverra id dignissim in, dignissim at ex. Suspendisse in faucibus nibh. Proin pretium sodales ante ut ultricies. Mauris vel diam iaculis, finibus tellus sit amet, convallis diam. Pellentesque et felis aliquam, finibus dolor at, commodo odio. In fringilla imperdiet lectus, eu rutrum ligula pulvinar nec. Sed malesuada tellus in sapien pellentesque pulvinar. Ut quis metus faucibus elit pretium aliquam. Vestibulum at nulla et risus tristique tincidunt. Nunc porttitor et eros feugiat consectetur. Suspendisse mauris elit, ultrices non risus nec, aliquet pretium purus. Vestibulum dignissim urna eget egestas porta. Aenean eget eros dapibus, fringilla nisi vel, tincidunt ex. Integer vitae vulputate nisi. Cras egestas sem lorem, vel maximus metus ultricies ac. Praesent lobortis egestas dignissim. Etiam porttitor faucibus erat. Curabitur dapibus sem at faucibus facilisis.Maecenas congue odio sed ultricies consectetur. Nullam venenatis orci ac diam maximus, nec elementum erat fermentum. Nullam nisl nibh, luctus id blandit at, luctus eu purus. Duis ultrices, velit eu consequat semper, arcu nisl dapibus elit, commodo egestas ante odio vitae justo. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse libero lectus, condimentum a eleifend pellentesque, ultrices a mi. Nam eu mi vehicula, porttitor eros varius, dictum justo. In fringilla vel purus eu ultrices. Donec imperdiet, nulla eget aliquam aliquet, diam eros iaculis erat, at venenatis nunc magna sollicitudin erat. Donec diam odio, hendrerit nec fermentum eu, fermentum non eros. Suspendisse sit amet augue nibh. Suspendisse eget magna at orci malesuada porttitor id et eros."
    path = 'D:\STUDIA\Cyberka\Semestr_7\Steganografia\Zdjęcia\PNG_8.png'

    
    # message = 'a a1'
    # message_in_binary = convertToBinary(message)
    # # print(table_of_bin, message_in_binary)
    # # print(convertToString("10010001100101110110011011001101111"))
    # # message_in_binary1 = convertToString(message_in_binary)

    # # print("Przetlumaczona wiadomosc: ", message_in_binary1)
    
    # _, img = convertImage(path)
    # img_with_info, stego_img = msbCoding(img, message_in_binary)
    # stego_img.save("/home/hubert/Documents/StHelloudia/wiadomosc1.png")
    
    codeInputMessage().save("D:\STUDIA\Cyberka\Semestr_7\Steganografia\Zdjęcia\STEGO_PNG_8.png")

    # np.set_printoptions(threshold=sys.maxsize)
    # print("Img with info\n", img_with_info[0:1, 0:15])
    stego_path = 'D:\STUDIA\Cyberka\Semestr_7\Steganografia\Zdjęcia\STEGO_PNG_8.png' # jpg zmienia obraz, że nie da się późneij go odczytać
    _, stego = convertImage(stego_path)
    # stego = np.array(stego_img)
    hide_massage = msbDecoding(stego_path)
    print("Ukryta wiadomość:", convertToString(hide_massage))
