import math
import sys
import numpy as np
from PIL import Image
from mess_preparation import convertToBinary, convertToString

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

def codeMessageMSB(path, message):
    message_in_binary = convertToBinary(message)
    _, img = convertImage(path)
    if len(message_in_binary) > (img.size):
        raise Exception("The message is too long to encode in this image")
    _, stego_img = msbCoding(img, message_in_binary)
    return stego_img

def decodeMessageMSB(path):
    mess = convertToString(msbDecoding(path))
    print(mess[:2])
    if mess[:2] != '**':
        raise ValueError
    return mess[2:]


if __name__ == '__main__':
    message = 'Hello World!'
    path = '/home/hubert/Documents/Studia/photo.jpg'
    stego_path = '/home/hubert/Documents/Studia/wiadomosc_msb.png' 
    stego_img = codeMessageMSB(path, message)
    stego_img.save(stego_path)
    print("Ukryta wiadomość:", decodeMessageMSB(stego_path))
