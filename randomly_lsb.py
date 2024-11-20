"""
Ten skrypt implementuje metodę ukrywania wiadomości w obrazach za pomocą zmodyfikowanego algorytmu LSB (Least Significant Bit).
Wiadomość jest zakodowana w najmniej znaczących bitach obrazu. Aby zakodować wiadomość, najpierw konwertuje się ją do postaci
binarnych ciągów, a następnie wstawia do wybranych pikseli obrazu, na podstawie obliczonego kroku. Odkodowanie działa na podobnej zasadzie
odczytując bity ukrytej wiadomości z najmniej znaczących bitów pikseli.

Moduły:
- `convertImage`  Konwertuje obraz na macierz numpy w celu ułatwienia manipulacji.
- `calculateStep`  Oblicza krok, co ile pikseli będzie zakodowany bit wiadomości.
- `lsbCoding`  Koduje wiadomość w obrazie, zmieniając ostatnie bity wybranych pikseli.
- `lsbDecoding`  Odkodowuje wiadomość z obrazu, odczytując najmniej znaczące bity pikseli.
- `codeExampleMessage`  Przykład zakodowania wiadomości w obrazie.
"""

import numpy as np
from PIL import Image
from mess_preparation import *


# Konwertuje obraz na macierz numpy w celu manipulacji pikselami
def convertImage(path):
    img = Image.open(path)
    numpy_img = np.array(img)
    return img, numpy_img


'''Oblicza krok co ile pikseli zostaną zakodowane bity wiadomości.
Jeśli wiadomość jest za długa dla danego obrazu, zwraca błąd.
Zwraca:
- Obliczony krok.
'''
def calculateStep(message_size, img):
    if (message_size*7+34) > (img.size-10):
        raise ValueError("The message is too long to encode in this picture")
    return (img.size - 10) // (message_size*7+34)


'''Koduje wiadomość w obrazie poprzez zmianę najmniej znaczących bitów wybranych pikseli.
Zwraca:
1. Obraz zakodowany w formacie numpy
2. Obraz zakodowany w formacie PIL (do zapisu)
'''
def rlsbCoding(img, message, step):
    shape = img.shape     # Kształt obrazu do przywrócenia po modyfikacji
    size = img.size
    resized_img = img.reshape(1, size)  # Zmiena obrazu na tablicę jednowymiarową
    pixel = 0              # Zmienna kontrolująca przemieszczanie się po pikselach 
    # Kodowanie nagłówka
    for bit in range(0, 10):
        if message[bit] == '0':
            resized_img[0, pixel] = resized_img[0, pixel] & ~1  # Wyzerowanie ostatniego bitu
        elif message[bit] == '1':
            resized_img[0, pixel] = resized_img[0, pixel] | 1   # Ustawia ostatni bit na 1
        else:
            print("Błąd")
        pixel += 1
    
    pixel += 1
    # Kodowanie wiadomości
    for bit in range(10, len(message)):
        if message[bit] == '0':
            resized_img[0, pixel] = resized_img[0, pixel] & ~1  # Wyzerowanie ostatniego bitu
        elif message[bit] == '1':
            resized_img[0, pixel] = resized_img[0, pixel] | 1   # Ustawia ostatni bit na 1
        else:
            print("Błąd")
        pixel += step

    new_img = resized_img.reshape(shape)  # Przywrócenie pierwotnego kształtu obrazu
    pil_image = Image.fromarray(new_img)  # Tworzenie obrazu w formacie PIL
    return new_img, pil_image


# Odkodowuje wiadomość z obrazu, czytając najmniej znaczące bity pikseli
def rlsbDecoding(img_path):
    _, img = convertImage(img_path)
    message = ''
    resized_img = img.reshape(1, img.size)
    step = ''
    size_of_text = ''

    # Read step (10 pierwszych bitów)
    for bit in range(0, 10):
        if resized_img[0, bit] % 2 == 0:
            step += '0'
        elif resized_img[0, bit] % 2 == 1:
            step += '1'
        else:
            print("Błąd")
    step = int(step, 2) # Zmiana z postaci binarnej
        
    # Odczytanie długości wiadomości
    for bit in range(11, (20*step)+11, step):
        if resized_img[0, bit] % 2 == 0:
            size_of_text += '0'
        elif resized_img[0, bit] % 2 == 1:
            size_of_text += '1'
        else:
            print("Błąd")
    size_of_text = int(size_of_text, 2) + 20

    # Odczytanie wiadomości (od miejsca w którym zakończyliśmy czytać długość wiadomości)
    for bit in range((20*step)+11, (size_of_text*step)+11, step):
        if resized_img[0, bit] % 2 == 0:
            message += '0'
        elif resized_img[0, bit] % 2 == 1:
            message += '1'
        else:
            print("Błąd")
    return message 


def codeMessageRandomLSB(path, message):
    _, img = convertImage(path)
    cal_step = calculateStep(len(message), img)
    message_in_binary= convertToBinary(message, cal_step)
    _, stego_img = rlsbCoding(img, message_in_binary, cal_step)
    return stego_img


def decodeMessageRandomLSB(path):
    print("Odczytywanie wiadomości: ")
    mess = convertToString(rlsbDecoding(path))
    if mess[:2] != '**':
        raise ValueError
    print(f"Message: {mess}")
    return mess[2:]


if __name__ == '__main__':
    message = "Hello World"
    path = 'path_to_image'
    stego_path = 'path_to_stego_image'
    stego_img = codeMessageRandomLSB(path, message)
    stego_img.save(stego_path)
    decodeMessageRandomLSB(stego_path)


