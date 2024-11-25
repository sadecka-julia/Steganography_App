import numpy as np
from PIL import Image
from mess_preparation import convertToBinary, convertToString

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

        try:
            r, g, b = region[x, y]
        except ValueError:
            raise ValueError("Format obrazu jest niepoprawny, spróbuj inne zdjęcie")
    
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
    
    return message_bits

def codeMessagePixelMSB(path, message):
    message_in_binary = convertToBinary(message)
    _, img = convertImage(path)
    if len(message_in_binary) > (img.size):
        raise Exception("The message is too long to encode in this image")
    _, stego_img = pixelMSBCoding(img, message_in_binary)
    return stego_img

def decodeMessagePixelMSB(path):
    mess = convertToString(pixelMSBDecoding(path))
    print(mess[:2])
    if mess[:2] != '**':
        raise ValueError
    return mess[2:]

if __name__ == '__main__':

    message = 'Hello World!'
    path = '/home/hubert/Documents/Studia/photo.jpg'
    stego_path = '/home/hubert/Documents/Studia/wiadomosc_pixel.png'
    stego_img = codeMessagePixelMSB(path, message)
    stego_img.save(stego_path)

    print("Ukryta wiadomość:", decodeMessagePixelMSB(stego_path))
