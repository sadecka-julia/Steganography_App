import numpy as np
from PIL import Image

def convertToBinary(message):
    table_of_bin = []
    len_of_message = len(message) * 7  # długość wiadomości w bitach
    len_of_message_bin = bin(len_of_message)[2:].zfill(20)  # konwersja na binarną postać długości z wypełnieniem do 20 bitów

    message_in_binary = len_of_message_bin

    for char in message:
        bin_repr = bin(ord(char))[2:].zfill(7)
        table_of_bin.append(bin_repr)

    for b in table_of_bin:
        message_in_binary += b

    return message_in_binary

def convertToString(message_in_binary):
    message = ""
    for i in range(0, len(message_in_binary), 7):
        message += chr(int(message_in_binary[i:i+7], 2))
    return message

def convertImage(path):
    img = Image.open(path)
    numpy_img = np.array(img)
    return img, numpy_img

def xor_message(message, key='101010'):
    key_repeated = (key * ((len(message) // len(key)) + 1))[:len(message)]
    return ''.join(str(int(m) ^ int(k)) for m, k in zip(message, key_repeated))

def pixelMSBCoding(img, message, key='101010'):
    message = xor_message(message, key)
    height, width, _ = img.shape
    center_h = height // 2
    center_w = width // 2
    half_h = height // 4
    half_w = width // 4
    region = img[center_h - half_h:center_h + half_h, center_w - half_w:center_w + half_w]

    pixel = 0
    for bit in message:
        bit = int(bit)
        x = pixel // (2 * half_w)
        y = pixel % (2 * half_w)
        
        if x >= region.shape[0] or y >= region.shape[1]:
            print("Uwaga: Obraz jest za mały, aby zapisać całą wiadomość.")
            break

        r, g, b = region[x, y]
    
        red_ones_count = bin(r).count('1')

        if red_ones_count % 2 == 0:
            region[x, y, 1] = (g & 0b11011111) | (bit << 5)  # modyfikacja bitu 5
        else:
            region[x, y, 2] = (b & 0b11011111) | (bit << 5)

        pixel += 1

    img[center_h - half_h:center_h + half_h, center_w - half_w:center_w + half_w] = region
    pil_image = Image.fromarray(img)
    return img, pil_image

def pixelMSBDecoding(img_path, key='101010'):
    _, img = convertImage(img_path)
    height, width, _ = img.shape
    center_h = height // 2
    center_w = width // 2
    half_h = height // 4
    half_w = width // 4
    region = img[center_h - half_h:center_h + half_h, center_w - half_w:center_w + half_w]

    decoded_message = ''
    pixel = 0
    for _ in range(region.shape[0] * region.shape[1]):
        x = pixel // (2 * half_w)
        y = pixel % (2 * half_w)

        if x >= region.shape[0] or y >= region.shape[1]:
            break

        r, g, b = region[x, y]
        red_ones_count = bin(r).count('1')

        if red_ones_count % 2 == 0:
            bit = (g >> 5) & 1
        else:
            bit = (b >> 5) & 1

        decoded_message += str(bit)
        pixel += 1

    decoded_message = xor_message(decoded_message, key)
    
    # Usunięcie wypełnienia binarnego
    length_of_message = int(decoded_message[:20], 2)
    message_bits = decoded_message[20:20+length_of_message]
    
    return convertToString(message_bits)

def codeInputMessage():
    message = input("Enter message to code in the image: \n")
    message_in_binary = convertToBinary(message)
    _, img = convertImage(path)
    img_with_info, stego_img = pixelMSBCoding(img, message_in_binary)
    return stego_img

if __name__ == '__main__':
    path = '/home/hubert/Documents/Studia/photo.jpg'
    codeInputMessage().save("/home/hubert/Documents/Studia/wiadomosc1.png")

    stego_path = '/home/hubert/Documents/Studia/wiadomosc1.png'
    hide_message = pixelMSBDecoding(stego_path)
    print("Ukryta wiadomość:", hide_message)
