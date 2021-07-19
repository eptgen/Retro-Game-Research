# Collects data of where the palettes are in all roms
# in a particular directory.

from romSearch import findPaletteBlocks
from getBytes import getFileHexList
import os
import csv
import sys

if __name__ == "__main__":
    folder = sys.argv[1]

    with open("result.csv", "w") as f:
        paletteData = csv.writer(f, delimiter=",")

        for file in os.listdir(folder):
            path = os.path.join(folder, file)

            # Get the hex values from the file.
            # Note: the hex values are lowercase.
            hexList = getFileHexList(path)

            # Find the palette blocks.
            blocks = findPaletteBlocks(hexList)

            paletteData.writerow([file, str(len(blocks))])
            print(file + ": " + str(len(blocks)) + " palettes found")






























#
