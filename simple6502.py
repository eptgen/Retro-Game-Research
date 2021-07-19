"""
Simple functions and data related to 6502 machine code.
 - A simple (and untested) disassembler is provided.
 - A map from opcodes to instruction information (name, mode, byte, time, flag).
"""

import sys

# This following data came from the following source (and had one error (see below)).
# https://raw.githubusercontent.com/kpmiller/emulator101/master/6502Disassembler/6502ops.csv

# Default each entry to a no-op.
opcodeInfo = 256*[("NOP","N/A",1,1,"czidbvn")]

# Now manually add all of the other opcode to instruction information.
opcodeInfo[0x69] = ("ADC","IMM",2,2,"CZidbVN")
opcodeInfo[0x65] = ("ADC","ZP",2,3,"CZidbVN")
opcodeInfo[0x75] = ("ADC","ZPX",2,4,"CZidbVN")
opcodeInfo[0x6d] = ("ADC","ABS",3,4,"CZidbVN")
opcodeInfo[0x7d] = ("ADC","ABSX",3,4,"CZidbVN")
opcodeInfo[0x79] = ("ADC","ABSY",3,4,"CZidbVN")
opcodeInfo[0x61] = ("ADC","INDX",2,6,"CZidbVN")
opcodeInfo[0x71] = ("ADC","INDY",2,5,"CZidbVN")
opcodeInfo[0x29] = ("AND","IMM",2,2,"cZidbvN")
opcodeInfo[0x25] = ("AND","ZP",2,3,"cZidbvN")
opcodeInfo[0x35] = ("AND","ZPX",2,4,"cZidbvN")
opcodeInfo[0x2d] = ("AND","ABS",3,4,"cZidbvN")
opcodeInfo[0x3d] = ("AND","ABSX",3,4,"cZidbvN")
opcodeInfo[0x39] = ("AND","ABSY",3,4,"cZidbvN")
opcodeInfo[0x21] = ("AND","INDX",2,6,"cZidbvN")
opcodeInfo[0x31] = ("AND","INDY",2,5,"cZidbvN")
opcodeInfo[0x0a] = ("ASL","ACC",1,2,"CZidbvN")
opcodeInfo[0x06] = ("ASL","ZP",2,5,"CZidbvN")
opcodeInfo[0x16] = ("ASL","ZPX",2,6,"CZidbvN")
opcodeInfo[0x0e] = ("ASL","ABS",3,6,"CZidbvN")
opcodeInfo[0x1e] = ("ASL","ABSX",3,7,"CZidbvN")
opcodeInfo[0x90] = ("BCC","REL",2,(2,3),"czidbvn")
opcodeInfo[0xB0] = ("BCS","REL",2,(2,3),"czidbvn")
opcodeInfo[0xF0] = ("BEQ","REL",2,(2,3),"czidbvn")
opcodeInfo[0x30] = ("BMI","REL",2,(2,3),"czidbvn")
opcodeInfo[0xD0] = ("BNE","REL",2,(2,3),"czidbvn")
opcodeInfo[0x10] = ("BPL","REL",2,(2,3),"czidbvn")
opcodeInfo[0x50] = ("BVC","REL",2,(2,3),"czidbvn")
opcodeInfo[0x70] = ("BVS","REL",2,(2,3),"czidbvn")
opcodeInfo[0x24] = ("BIT","ZP",2,3,"cZidbVN")
opcodeInfo[0x2c] = ("BIT","ABS",3,4,"cZidbVN")
opcodeInfo[0x00] = ("BRK","IMP",1,7,"czidbvn")
opcodeInfo[0x18] = ("CLC","IMP",1,2,"Czidbvn")
opcodeInfo[0xd8] = ("CLD","IMP",1,2,"cziDbvn")
opcodeInfo[0x58] = ("CLI","IMP",1,2,"czIdbvn")
opcodeInfo[0xb8] = ("CLV","IMP",1,2,"czidbVn")
opcodeInfo[0xea] = ("NOP","IMP",1,2,"czidbvn")
opcodeInfo[0x48] = ("PHA","IMP",1,3,"czidbvn")
opcodeInfo[0x68] = ("PLA","IMP",1,4,"cZidbvN")
opcodeInfo[0x08] = ("PHP","IMP",1,3,"czidbvn")
opcodeInfo[0x28] = ("PLP","IMP",1,4,"CZIDBVN")
opcodeInfo[0x40] = ("RTI","IMP",1,6,"czidbvn")
opcodeInfo[0x60] = ("RTS","IMP",1,6,"czidbvn")
opcodeInfo[0x38] = ("SEC","IMP",1,2,"Czidbvn")
opcodeInfo[0xf8] = ("SED","IMP",1,2,"cziDbvn")
opcodeInfo[0x78] = ("SEI","IMP",1,2,"czIdbvn")
opcodeInfo[0xaa] = ("TAX","IMP",1,2,"cZidbvN")
opcodeInfo[0x8a] = ("TXA","IMP",1,2,"cZidbvN")
opcodeInfo[0xa8] = ("TAY","IMP",1,2,"cZidbvN")
opcodeInfo[0x98] = ("TYA","IMP",1,2,"cZidbvN")
opcodeInfo[0xba] = ("TSX","IMP",1,2,"cZidbvN")
opcodeInfo[0x9a] = ("TXS","IMP",1,2,"czidbvn")
opcodeInfo[0xc9] = ("CMP","IMM",2,2,"CZidbvN")
opcodeInfo[0xc5] = ("CMP","ZP",2,3,"CZidbvN")
opcodeInfo[0xd5] = ("CMP","ZPX",2,4,"CZidbvN")
opcodeInfo[0xcd] = ("CMP","ABS",3,4,"CZidbvN")
opcodeInfo[0xdd] = ("CMP","ABSX",3,4,"CZidbvN")
opcodeInfo[0xd9] = ("CMP","ABSY",3,4,"CZidbvN")
opcodeInfo[0xc1] = ("CMP","INDX",2,6,"CZidbvN")
opcodeInfo[0xd1] = ("CMP","INDY",2,5,"CZidbvN")
opcodeInfo[0xe0] = ("CPX","IMM",2,2,"CZidbvN")
opcodeInfo[0xe4] = ("CPX","ZP",2,3,"CZidbvN")
opcodeInfo[0xec] = ("CPX","ABS",3,4,"CZidbvN")
opcodeInfo[0xc0] = ("CPY","IMM",2,2,"CZidbvN")
opcodeInfo[0xc4] = ("CPY","ZP",2,3,"CZidbvN")
opcodeInfo[0xcc] = ("CPY","ABS",3,4,"CZidbvN")
opcodeInfo[0xc6] = ("DEC","ZP",2,5,"cZidbvN")
opcodeInfo[0xd6] = ("DEC","ZPX",2,6,"cZidbvN")
opcodeInfo[0xce] = ("DEC","ABS",3,6,"cZidbvN")
opcodeInfo[0xde] = ("DEC","ABSX",3,7,"cZidbvN")
opcodeInfo[0xca] = ("DEX","IMP",1,2,"cZidbvN")
opcodeInfo[0x88] = ("DEY","IMP",1,2,"cZidbvN")
opcodeInfo[0xe8] = ("INX","IMP",1,2,"cZidbvN")
opcodeInfo[0xc8] = ("INY","IMP",1,2,"cZidbvN")
opcodeInfo[0x49] = ("EOR","IMM",2,2,"cZidbvN")
opcodeInfo[0x45] = ("EOR","ZP",2,3,"cZidbvN")
opcodeInfo[0x55] = ("EOR","ZPX",2,4,"cZidbvN")
opcodeInfo[0x4d] = ("EOR","ABS",3,4,"cZidbvN")
opcodeInfo[0x5d] = ("EOR","ABSX",3,4,"cZidbvN")
opcodeInfo[0x59] = ("EOR","ABSY",3,4,"cZidbvN")
opcodeInfo[0x41] = ("EOR","INDX",2,6,"cZidbvN")
opcodeInfo[0x51] = ("EOR","INDY",2,5,"cZidbvN")
opcodeInfo[0xe6] = ("INC","ZP",2,5,"cZidbvN")
opcodeInfo[0xf6] = ("INC","ZPX",2,6,"cZidbvN")
opcodeInfo[0xee] = ("INC","ABS",3,6,"cZidbvN")
opcodeInfo[0xfe] = ("INC","ABSX",3,7,"cZidbvN")
opcodeInfo[0x4c] = ("JMP","ABS",3,3,"czidbvn")
opcodeInfo[0x6c] = ("JMP","IND",3,5,"czidbvn")
opcodeInfo[0x20] = ("JSR","ABS",3,6,"czidbvn")
opcodeInfo[0xa9] = ("LDA","IMM",2,2,"cZidbvN")
opcodeInfo[0xa5] = ("LDA","ZP",2,3,"cZidbvN")
opcodeInfo[0xb5] = ("LDA","ZPX",2,4,"cZidbvN")
opcodeInfo[0xad] = ("LDA","ABS",3,4,"cZidbvN")
opcodeInfo[0xbd] = ("LDA","ABSX",3,4,"cZidbvN")
opcodeInfo[0xb9] = ("LDA","ABSY",3,4,"cZidbvN")
opcodeInfo[0xa1] = ("LDA","INDX",2,6,"cZidbvN")
opcodeInfo[0xb1] = ("LDA","INDY",2,5,"cZidbvN")
opcodeInfo[0xa2] = ("LDX","IMM",2,2,"cZidbvN")
opcodeInfo[0xa6] = ("LDX","ZP",2,3,"cZidbvN")
opcodeInfo[0xb6] = ("LDX","ZPY",2,4,"cZidbvN")
opcodeInfo[0xae] = ("LDX","ABS",3,4,"cZidbvN")
opcodeInfo[0xbe] = ("LDX","ABSY",3,4,"cZidbvN")
opcodeInfo[0xa0] = ("LDY","IMM",2,2,"cZidbvN")
opcodeInfo[0xa4] = ("LDY","ZP",2,3,"cZidbvN")
opcodeInfo[0xb4] = ("LDY","ZPX",2,4,"cZidbvN")
opcodeInfo[0xac] = ("LDY","ABS",3,4,"cZidbvN")
opcodeInfo[0xbc] = ("LDY","ABSX",3,4,"cZidbvN")
opcodeInfo[0x4a] = ("LSR","ACC",1,2,"CZidbvN")
opcodeInfo[0x46] = ("LSR","ZP",2,5,"CZidbvN")
opcodeInfo[0x56] = ("LSR","ZPX",2,6,"CZidbvN")
opcodeInfo[0x4e] = ("LSR","ABS",3,6,"CZidbvN")
opcodeInfo[0x5e] = ("LSR","ABSX",3,7,"CZidbvN")
opcodeInfo[0x09] = ("ORA","IMM",2,2,"cZidbvN")
opcodeInfo[0x05] = ("ORA","ZP",2,3,"cZidbvN")
opcodeInfo[0x15] = ("ORA","ZPX",2,4,"cZidbvN")
opcodeInfo[0x0d] = ("ORA","ABS",3,4,"cZidbvN")
opcodeInfo[0x1d] = ("ORA","ABSX",3,4,"cZidbvN")
opcodeInfo[0x19] = ("ORA","ABSY",3,4,"cZidbvN")
opcodeInfo[0x01] = ("ORA","INDX",2,6,"cZidbvN")
opcodeInfo[0x11] = ("ORA","INDY",2,5,"cZidbvN")
opcodeInfo[0x2a] = ("ROL","ACC",1,2,"CZidbvN")
opcodeInfo[0x26] = ("ROL","ZP",2,5,"CZidbvN")
opcodeInfo[0x36] = ("ROL","ZPX",2,6,"CZidbvN")
opcodeInfo[0x2e] = ("ROL","ABS",3,6,"CZidbvN")
opcodeInfo[0x3e] = ("ROL","ABSX",3,7,"CZidbvN")
opcodeInfo[0x6a] = ("ROR","ACC",1,2,"CZidbvN")
opcodeInfo[0x66] = ("ROR","ZP",2,5,"CZidbvN")
opcodeInfo[0x76] = ("ROR","ZPX",2,6,"CZidbvN")
opcodeInfo[0x6e] = ("ROR","ABS",3,6,"CZidbvN")  # hahahah this is wrong!  it's absolute,X http://www.6502.org/tutorials/6502opcodes.html#ROR
opcodeInfo[0x7e] = ("ROR","ABSX",3,7,"CZidbvN") # these two opcodes (6e, 7e) are transposed in https://raw.githubusercontent.com/kpmiller/emulator101/master/6502Disassembler/6502ops.csv
opcodeInfo[0xe9] = ("SBC","IMM",2,2,"CZidbVN")
opcodeInfo[0xe5] = ("SBC","ZP",2,3,"CZidbVN")
opcodeInfo[0xf5] = ("SBC","ZPX",2,4,"CZidbVN")
opcodeInfo[0xed] = ("SBC","ABS",3,4,"CZidbVN")
opcodeInfo[0xfd] = ("SBC","ABSX",3,4,"CZidbVN")
opcodeInfo[0xf9] = ("SBC","ABSY",3,4,"CZidbVN")
opcodeInfo[0xe1] = ("SBC","INDX",2,6,"CZidbVN")
opcodeInfo[0xf1] = ("SBC","INDY",2,5,"CZidbVN")
opcodeInfo[0x85] = ("STA","ZP",2,3,"czidbvn")
opcodeInfo[0x95] = ("STA","ZPX",2,4,"czidbvn")
opcodeInfo[0x8d] = ("STA","ABS",3,4,"czidbvn")
opcodeInfo[0x9d] = ("STA","ABSX",3,5,"czidbvn")
opcodeInfo[0x99] = ("STA","ABSY",3,5,"czidbvn")
opcodeInfo[0x81] = ("STA","INDX",2,6,"czidbvn")
opcodeInfo[0x91] = ("STA","INDY",2,6,"czidbvn")
opcodeInfo[0x86] = ("STX","ZP",2,3,"czidbvn")
opcodeInfo[0x96] = ("STX","ZPY",2,4,"czidbvn")
opcodeInfo[0x8e] = ("STX","ABS",3,4,"czidbvn")
opcodeInfo[0x84] = ("STY","ZP",2,3,"czidbvn")
opcodeInfo[0x94] = ("STY","ZPX",2,4,"czidbvn")
opcodeInfo[0x8c] = ("STY","ABS",3,4,"czidbvn")


# operationOpcodes will be a dictionary that maps operation names to opcodes.
operationOpcodes = dict()

# Initialize each operation's list of opcodes to the empty list.
allOperations = set([info[0] for info in opcodeInfo])
for operation in allOperations:
    operationOpcodes[operation] = []

# Add every opcode to the operation's list in the dictionary.
for opcode, info in enumerate(opcodeInfo):
    name = info[0]
    operationOpcodes[name].append(opcode)


# Convert a list of bytes into a list of instructions.
# Each instruction is a tuple of (1, 2, or 3) bytes.
# The partitioning of bytes into instructions is done greedily from the first byte.
# Any incomplete result at the end of the byte list is treated as a no-op.
def getInstructions(bytes):
    # The list of instructions.
    instructions = []

    # n is the number of bytes we are given.
    n = len(bytes)

    # Iterate over all of the bytes.
    # Use the skip value to skip over bytes.
    skip = 0
    for index, byte in enumerate(bytes):

        # Skip over bytes based on last instruction.
        if skip > 0:
            skip -= 1
            continue

        # Get the info for this opcode.
        info = opcodeInfo[byte]
        (name, mode, size, time, flag) = info

        # If the full instruction isn't present, then don't add it, and return.
        if index + size - 1 >= n:
            return instructions

        # Otherwise, build the instruction and add it to the list.
        instruction = tuple(bytes[index:index+size])
        instructions.append(instruction)

        # Skip the remaining bytes in this instruction during the next iterations.
        skip = size - 1

    # Return the list of instructions.
    return instructions


# Convert a list of instructions into assembly code.
# The assembly code is a list of strings.
def getAssembly(instructions):
    # The assembly to return is a list of strings.
    assembly = []

    # n is the number instructions to disassemble.
    n = len(instructions)

    # Iterate over all of the instructions.
    for instruction in instructions:

        # Get the opcode.
        opcode = instruction[0]

        # Get the info for this opcode.
        info = opcodeInfo[opcode]
        (name, mode, size, time, flag) = info

        # The line of assembly always begins with the instruction name.
        line = name + " "

        # Add the "#" prefix if were are in immediate or relative mode.
        if mode == "IMM" or mode == "REL":
            line += "#"

        # Add "(" if we are in an indirect mode.
        if mode in ["IND", "INDX", "INDY"]:
            line += "("

        # Add an address: relative, zero page, or full.
        if mode == "REL":
            # Get 2's complement value for the offset.
            # https://stackoverflow.com/a/36338336
            value = instruction[1]
            value = value - int((value << 1) & 2**8)
            line += "$%+03X" % value
        elif size == 2:
            line += "$%02X" % instruction[1]
        elif size == 3:
            line += "$%02X%02X" % (instruction[2], instruction[1])

        # Add ")" if we are in certain indirect modes.
        if mode == "INDY":
            line += ")"

        # Add the ,X or ,Y if necessary.
        if mode in ["ABSX", "INDX", "ZPX"]:
            line += ",X"
        elif mode in ["ABSY", "INDY", "ZPY"]:
            line += ",Y"

        # Add ")" if we are in certain indirect modes.
        if mode in ["IND", "INDX"]:
            line += ")"

        # Add the line to the assembly.
        assembly = assembly + [line]

    # Return the assembly.
    return assembly



# This function works, but it can be replaced by getInstructions, getAssembly.

# takes in a list already grouped?  nah
# bytes vs machines?  and is a byte just an int?
# uggh, clarify what a "byte" is in these programs.
def disassemble(bytes):
    # The assembly to return is a list of strings.
    assembly = []

    # n is the number of bytes to disassemble.
    n = len(bytes)

    # Iterate over all of the bytes.
    # Use the skip value to skip over bytes.
    skip = 0
    for index, byte in enumerate(bytes):

        # Skip over bytes based on last instruction.
        if skip > 0:
            skip -= 1
            continue

        # Get the info for this opcode.
        info = opcodeInfo[byte]
        (name, mode, size, time, flag) = info

        # Check if the full instruction cannot be disassembled.
        if index + size - 1 >= n:
            # Add a NOP and then continue.
            assembly = assembly + ["NOP"]
            continue

        # Next time we'll skip over some bytes.
        skip = size - 1

        # The line of assembly always begins with the instruction name.
        line = name + " "

        # Add the "#" prefix if were are in immediate or relative mode.
        if mode == "IMM" or mode == "REL":
            line += "#"

        # Add "(" if we are in an indirect mode.
        if mode in ["IND", "INDX", "INDY"]:
            line += "("

        # Add an address: relative, zero page, or full.
        if mode == "REL":
            # Get 2's complement value for the offset.
            # https://stackoverflow.com/a/36338336
            value = bytes[index+1]
            value = value - int((value << 1) & 2**8)
            line += "$%+03X" % value
        elif size == 2:
            line += "$%02X" % bytes[index+1]
        elif size == 3:
            line += "$%02X%02X" % (bytes[index+2], bytes[index+1])

        # Add ")" if we are in certain indirect modes.
        if mode == "INDY":
            line += ")"

        # Add the ,X or ,Y if necessary.
        if mode in ["ABSX", "INDX", "ZPX"]:
            line += ",X"
        elif mode in ["ABSY", "INDY", "ZPY"]:
            line += ",Y"

        # Add ")" if we are in certain indirect modes.
        if mode in ["IND", "INDX"]:
            line += ")"

        # Add the line to the assembly.
        assembly = assembly + [line]

    # Return the assembly.
    return assembly

# When called from the command-line, let's run the simple disassembler.
# Here is an example of how to disassemble a full NES rom file.
#   xxd ~/DLoads/Battle\ of\ Olympus\,\ The\ \(U\).nes | awk '{print $2 $3 $4 $5 $6 $7 $8 $9}' | xargs python3 simple6502.py > olympus.dis
# TODO This should be made into its own script (and this should become a separate git project).
if __name__ == "__main__":

    # If there are no arguments, then exit.
    if len(sys.argv) == 1: exit(0)

    # Smash all of the arguments into a single long string and capitalize it.
    longString = ("".join(sys.argv[1:])).upper()

    # Make sure that the string only contains hex characters.
    if not set(longString) <= set(["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]):
        print("input must consist of an even number of hex characters")
        exit(0)

    # Get the length of the string bail out if it's not even.
    n = len(longString)
    if n % 2 == 1:
        print("input must consist of an even number of hex characters")
        exit(0)

    # Divide the long string into a list of pairs.
    pairs = [longString[i:i+2] for i in range(0,n,2)]

    # Otherwise, assume that each argument is a byte.
    bytes = [int(pair,16) for pair in pairs]

    # Split the bytes into instructions, then get the assembly.
    instructions = getInstructions(bytes)
    assembly = getAssembly(instructions)

    # Pring out the assembly.
    for line in assembly:
        print(line)
