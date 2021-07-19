# Use Python 3

import sys
import os

# Input: An integer between 0 and 255.
# Output: A string of length two in hexadecimal.
def int2hex(decimalValue):
    h = hex(decimalValue)
    h = h[2:] # remove 0x
    if len(h) == 1:
        h = "0" + h
    return h


# Read a file into a list of byte values (i.e. integers between 0 and 255).
def getFileBytes(fileName):
    # Process file
    with open(fileName, mode='rb') as file:

        # Build the list of bytes.
        # (There is likely a better way of doing this.)
        byteList = []
        while True:

            # This article helped me:
            # https://stackoverflow.com/questions/2872381/how-to-read-a-file-byte-by-byte-in-python-and-how-to-print-a-bytelist-as-a-binar
            byte_s = file.read(1)
            if not byte_s:
                break
            byte = byte_s[0]
            byteList.append(byte)

    # Return the list of bytes.
    return byteList


# Read a file into a list of byte values in hexadecimal.
# Note: the hex values are returned in lowercase (i.e. "3f" not "3F").
def getFileHexList(fileName):

    # Process file
    with open(fileName, mode='rb') as file:

        # Build the list of bytes.
        # (There is likely a better way of doing this.)
        hexList = []
        while True:

            # This article helped me:
            # https://stackoverflow.com/questions/2872381/how-to-read-a-file-byte-by-byte-in-python-and-how-to-print-a-bytelist-as-a-binar
            byte_s = file.read(1)
            if not byte_s:
                break
            byte = byte_s[0]
            h = int2hex(int(byte))
            hexList.append(h)

    # Return the list of bytes.
    return hexList


if __name__ == "__main__":

    # Get the filenames as provided by the first command-line argument.
    fileName = sys.argv[1]

    hexList = getFileHexList(fileName)
    for hex in hexList:
        print(hex)

    # # Create a list of bytes in the file.
    # fileBytes = getFileBytes(fileName)
    #
    # # Print out the bytes as integers.
    # num = 0
    # for value in fileBytes:
    #     # uggh, this code sucks
    #     h = hex(value)
    #     if len(h) == 3:
    #         print("0", end="")
    #     print(h[2:], sep="", end="")
    #     print(" ", end="")
    #     num += 1
    #     if num == 16:
    #         print("")
    #         num = 0
    # print("")
