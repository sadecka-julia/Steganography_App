import heapq
import numpy as np
from PIL import Image
from collections import defaultdict


def build_huffman_tree(message):
    frequency = defaultdict(int)
    for char in message:
        frequency[char] += 1

    heap = [[weight, [char, ""]] for char, weight in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    huffman_tree = heap[0][1:]
    huffman_codes = {}
    for char, code in huffman_tree:
        huffman_codes[char] = code

    print(huffman_codes)

    return huffman_codes


def compress_message(message, huffman_codes):
    return ''.join([huffman_codes[char] for char in message])


def decompress_message(binary_message, huffman_codes):
    reverse_huffman_codes = {v: k for k, v in huffman_codes.items()}
    current_code = ""
    decoded_message = ""

    for bit in binary_message:
        current_code += bit
        if current_code in reverse_huffman_codes:
            decoded_message += reverse_huffman_codes[current_code]
            current_code = ""

    return decoded_message


def lsbCoding(img, message):
    shape = img.shape
    size = img.size
    resized_img = img.reshape(-1)
    pixel = 0

    # Generowanie kodów Huffmana
    huffman_codes = build_huffman_tree(message)
    compressed_message = compress_message(message, huffman_codes)

    # Kodowanie długości wiadomości
    length_in_binary = bin(len(compressed_message))[2:].zfill(20)
    for bit in length_in_binary:
        resized_img[pixel] = np.uint8(resized_img[pixel] & 254 | int(bit))
        pixel += 1

    # Kodowanie wiadomości
    for bit in compressed_message:
        resized_img[pixel] = np.uint8(resized_img[pixel] & 254 | int(bit))
        pixel += 1

    if pixel > size:
        raise ValueError("Wiadomość jest zbyt długa dla wybranego obrazu.")

    new_img = resized_img.reshape(shape)
    pil_image = Image.fromarray(new_img)
    return new_img, pil_image, huffman_codes


def lsbDecoding(img_path):
    _, img = convertImage(img_path)
    resized_img = img.reshape(-1)
    pixel = 0

    # Odczyt długości wiadomości
    length_in_binary = ""
    for _ in range(20):
        length_in_binary += str(resized_img[pixel] & 1)
        pixel += 1

    message_length = int(length_in_binary, 2)

    # Odczyt samej wiadomości
    compressed_message = ""
    for _ in range(message_length):
        compressed_message += str(resized_img[pixel] & 1)
        pixel += 1

    return compressed_message


def convertImage(path):
    img = Image.open(path)
    numpy_img = np.array(img)
    return img, numpy_img


def codeInputMessage():
    message = input("Wprowadź wiadomość do zakodowania: \n")
    path = '/home/hubert/Documents/Studia/photo.jpg'
    output_path = "/home/hubert/Documents/Studia/wiadomosc_huffman.png"
    
    _, img = convertImage(path)
    img_with_info, stego_img, huffman_codes = lsbCoding(img, message)
    stego_img.save(output_path)
    print(f"Wiadomość zakodowana w obrazie: {output_path}")

    return huffman_codes, output_path


def decodeMessage(huffman_codes, stego_path):
    compressed_message = lsbDecoding(stego_path)
    print(huffman_codes)
    print(compressed_message)
    decoded_message = decompress_message(compressed_message, huffman_codes)
    print(f"Odkodowana wiadomość: {decoded_message}")


if __name__ == '__main__':
    # Kodowanie wiadomości
    huffman_codes, stego_path = codeInputMessage()

    # Dekodowanie wiadomości
    decodeMessage(huffman_codes, stego_path)
