import numpy as np
from PIL import Image

def prepare_image(image_path):
    # Wczytaj obraz w odcieniach szarości
    img = Image.open(image_path).convert('L')
    return np.array(img)

def save_image(image_array, output_path):
    img = Image.fromarray(image_array.astype('uint8'), mode='L')
    img.save(output_path)

def transform_to_multiples_of_5(pixel):
    remainder = pixel % 5
    if remainder == 4:
        return pixel + 1
    elif remainder == 3:
        return pixel + 2
    elif remainder == 2:
        return pixel - 2
    elif remainder == 1:
        return pixel - 1
    return pixel

def encode_message(image_array, message, k=5, starting_index=32):
    # Przekształć piksele obrazu na wielokrotności 5
    transformed_image = np.vectorize(transform_to_multiples_of_5)(image_array)
    
    # Konwertuj wiadomość na wartości ASCII
    starting_point = starting_index - 1
    ascii_values = [ord(char) - starting_point for char in message]
    print(ascii_values)
    
    # Ukryj wiadomość w obrazku
    message_index = 0
    blocks = transformed_image.shape[0] // k, transformed_image.shape[1] // k
    
    for i in range(blocks[0]):
        for j in range(blocks[1]):
            if message_index >= len(ascii_values):
                return transformed_image
            block_start_x, block_start_y = i * k, j * k
            block = transformed_image[block_start_x:block_start_x+k, block_start_y:block_start_y+k]
            
            x = ascii_values[message_index]
            reminder = x // (k * k)
            position = x - (reminder * (k * k))
            position_x, position_y = divmod(position, k)
            
            block[position_x, position_y] += (reminder + 1)
            transformed_image[block_start_x:block_start_x+k, block_start_y:block_start_y+k] = block
            message_index += 1
    
    return transformed_image


def decode_message(encoded_image, k=5, starting_index=32):
    starting_point = starting_index - 1
    blocks = encoded_image.shape[0] // k, encoded_image.shape[1] // k
    decoded_message = []
    
    for i in range(blocks[0]):
        for j in range(blocks[1]):
            block_start_x, block_start_y = i * k, j * k
            block = encoded_image[block_start_x:block_start_x+k, block_start_y:block_start_y+k]
            
            for x in range(k):
                for y in range(k):
                    if block[x, y] % 5 != 0:
                        reminder = (block[x, y] % 5) - 1
                        position = x * k + y
                        ascii_value = position + (reminder * (k * k)) + starting_point
                        decoded_message.append(chr(ascii_value))
                        break
                else:
                    continue
                break
    
    return ''.join(decoded_message)


def codeMessageFMM(path, message, k, start_index):
    image_array = prepare_image(path)
    encoded_image = encode_message(image_array, message, k, start_index)
    img = Image.fromarray(encoded_image.astype('uint8'), mode='L')
    return img


def decodeMessageFFM(path, k, start_index):
    loaded_image = prepare_image(path)
    decoded_message = decode_message(loaded_image, k, start_index)
    return decoded_message


if __name__ == "__main__":
    input_path = "D:\STUDIA\Cyberka\Semestr_7\Steganografia\zdj1.jpg"
    output_path = "D:\STUDIA\Cyberka\Semestr_7\Steganografia\STEGO_zdj1.png"
    message = "Hello World!!!"
    k = 5
    starting_index = 32

    # Kodowanie wiadomości
    image_array = prepare_image(input_path)
    encoded_image = encode_message(image_array, message, k, starting_index)
    save_image(encoded_image, output_path)

    # Dekodowanie wiadomości
    loaded_image = prepare_image(output_path)
    decoded_message = decode_message(loaded_image, k, starting_index)

    print("Original Message:", message)
    print("Decoded Message:", decoded_message)

