# Changes NES palette colors (to greyscale).

import sys
import os
from getBytes import getFileHexList, int2hex

SKIP_SUS = True
# Dictionary for converting to greyscale.
greyscale = {
            "0f":"0f",
            "0e":"0e",
            "0d":"0d",
            "0c":"2d",
            "0b":"2d",
            "0a":"2d",
            "09":"2d",
            "08":"2d",
            "07":"2d",
            "06":"2d",
            "05":"2d",
            "04":"2d",
            "03":"2d",
            "02":"2d",
            "01":"2d",
            "00":"00",
            "1f":"1f",
            "1e":"1e",
            "1d":"1d",
            "1c":"00",
            "1b":"00",
            "1a":"00",
            "19":"00",
            "18":"00",
            "17":"00",
            "16":"00",
            "15":"00",
            "14":"00",
            "13":"00",
            "12":"00",
            "11":"00",
            "10":"00",
            "2f":"2f",
            "2e":"2e",
            "2d":"2d",
            "2c":"10",
            "2b":"10",
            "2a":"10",
            "29":"10",
            "28":"10",
            "27":"10",
            "26":"10",
            "25":"10",
            "24":"10",
            "23":"10",
            "22":"10",
            "21":"10",
            "20":"20",
            "3f":"3f",
            "3e":"3e",
            "3d":"3d",
            "3c":"3d",
            "3b":"3d",
            "3a":"3d",
            "39":"3d",
            "38":"3d",
            "37":"3d",
            "36":"3d",
            "35":"3d",
            "34":"3d",
            "33":"3d",
            "32":"3d",
            "31":"3d",
            "30":"30"
}


# todo: describe what a palette block is (i.e. 3F xx yy colors).
def findPaletteBlocks(hexList):

    # Initialize our list of palette blocks.
    blocks = []

    #find 163037
    spritePalette = [index for index, value in enumerate(hexList) if value == "16"]

    # Find all of the indices in the file that contain 3F.
    threeFs = [index for index, value in enumerate(hexList) if value == "3f"]
#    threeFs = [index for index, value in enumerate(hexList) if value == "16"]
    # Iterate over the 3F indices in the file.
    for threeIndex in threeFs:

        # Edge case: Avoid reading past the end of the file.
        # This would occur below when the 3F is the last or second-last byte.
        if threeIndex+2 >= len(hexList):
            continue

        # Let's assume that this threeIndex is a valid palette block.
        # Get the start index and number of bytes for this palette block.
        startIndex = int(hexList[threeIndex+1], 16)
        numBytes = int(hexList[threeIndex+2], 16)

        # Check if the above values are not valid.
        # This occurs when the start plus the number of bytes goes beyond
        # the address 3F 1F.  Or if the number of bytes is zero.
        if startIndex + numBytes > 32 or numBytes == 0:
            continue

        # Edge case: Avoid reading past the end of the file.
        if threeIndex+3+numBytes > len(hexList):
            continue

        # Get the color indices from the file.
        colorsHex = hexList[threeIndex+3:threeIndex+3+numBytes]
        colors = [int(hex,16) for hex in colorsHex]

        # Check if the colors are not valid.
        # This occurs when one of the colors is greater than 63.
        maxColor = max(colors)
        if maxColor > 63:
            continue

        if SKIP_SUS and numBytes % 4 != 0:
            continue
        # This potential palette block appears to be valid.
        # Add the palette block to the list of blocks.
        index = threeIndex
        blockBytes = hexList[threeIndex:threeIndex+3+numBytes]
        block = [index, blockBytes]
        blocks.append(block)

    # Return the palette blocks that we found.
    #blockA = [0x6b7, hexList[0x6b6:0x6bA]]
    #blocks.append(blockA)
    return blocks


# todo add comments
# note: hexList is modified
def convertPaletteGrey(hexList, paletteBlocks):

    # Iterate over the palette blocks.
    for block in paletteBlocks:

        # Get the index and list of bytes from the block.
        [index, blockBytes] = block

        # Get the list of colors from the block.
        colors = blockBytes[3:]

        # Get the number of colors.
        numColors = len(colors)
        assert(numColors == int(blockBytes[2],16))

        # Convert the colors to greyscale.
        newColors = [greyscale[color] for color in colors]

        # Overwrite the old colors with new colors in the hex list of the file.
        hexList[index+3:index+3+numColors] = newColors

    # Return the modified hex list of the file.
    return hexList


# todo comments
def writeHexListFile(hexList, fileName):
    # Convert the hex list into a single string with spaces between bytes.
    fileString = " ".join(hexList)

    # Write the file string to file.
    with open(fileName, 'wb') as hacked:
        hacked.write(bytes(bytearray.fromhex(fileString)))
        hacked.close()


if __name__ == "__main__":
    fileName = sys.argv[1]

    # Get the hex values from the file.
    # Note: the hex values are lowercase.
    hexList = getFileHexList(fileName)

    # Find the palette blocks.
    blocks = findPaletteBlocks(hexList)

    # Print out the palette blocks.
    for block in blocks:

        [index, blockBytes] = block
        #second block, third block, sixth and seventh block
        #blocks.remove(2, )
        #f SKIP_SUS and numBytes % 4 != 1: continue
#SKIP_SUS = 1
#SKIP_SUS = True
        indexHex = int2hex(index)
        print(indexHex, end=": ")
        print(blockBytes, sep=" ")

    # Modify the hex list using greyscale.
    convertPaletteGrey(hexList, blocks)

    # Write the modified hex list to a new file.
    # Start by splitting the original filename into path and file parts.
    pathPart, filePart = os.path.split(fileName)
    greyFileName = "grey_" + filePart   # pathPart + "grey_" + filePart
    writeHexListFile(hexList, greyFileName)


    # final = romSift(fileName)
    #
    # # Save location and file name:
    # name = "{} Hack.nes".format(fileName[:-4])
    # path = "{}".format(name)
    #
    # # Write file:
    # with open(path, 'wb') as hacked:
    #     hacked.write(bytes(bytearray.fromhex(final)))
    #     hacked.close()
    #
    # print("Success")

# Notes for improvement:
# 1. Should present name of palette no matter what (Bkg0-3, Spr0-3)
