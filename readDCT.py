from dct import prepareImage, zigZagEncoding, dctTransformation


def convertToStringDCT(message_in_binary):
    table_of_strings = []
    message = ""
    for char in range(0, len(message_in_binary), 7):
        table_of_strings.append(chr(int(message_in_binary[char:char+7], 2)))

    for i in table_of_strings:
        message += i

    # print(message)
    return message


def extractBitsFromImage(image_path, mode=5):
    # Dzieli na bloki 8x8 i odejmuje 128
    blocks = prepareImage(image_path)
    dct_blocks = dctTransformation(blocks)
    bit_index = 0
    extracted_bits = ''
    mess_lenght = 100
    height, width = dct_blocks.shape[:2]

    for i in range(height):
        for j in range(width):
            for channel in range(3):
                if channel in [2]:
                    if bit_index == 49:
                        print(extracted_bits, convertToStringDCT(extracted_bits))
                        mess_lenght = int(convertToStringDCT(extracted_bits))
                    if bit_index >= mess_lenght:
                        print("Finished extracting all bits")
                        return extracted_bits

                    value = int(dct_blocks[i, j, 0, 0, channel])
                    if mode==3:
                        if (value%6) in [4, 5, 0]:
                            bit = 0
                        else:
                            bit = 1
                    if mode==5:
                        if (value%10) in [0, 1, 2, 3, 4]:
                            bit = 0
                        else:
                            bit = 1

                    # idx = 0


                    extracted_bits += str(bit)
                    # print(f"Extracted bit {value % 2} from position ({i}, {j}, {channel}), coefficient {value}")

                    bit_index += 1

    return extracted_bits


def decodeMessageDCT(stego_path):
    bits = extractBitsFromImage(stego_path)
    mess = convertToStringDCT(bits)
    return mess


if __name__ == '__main__':
    path = "stego_path"
    mess = decodeMessageDCT(path)
    print("Decoded message: ", mess)
