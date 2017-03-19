import struct

# INSTRUCTION BIBLE
# Each instruction is a single 32 bit int.
# MODE 4 BIT
# MODE
#   0000 R[x] = R[y] <op> R[z]
#   0001 R[x] = R[y] <op> in[z]
#   0010 R[x] = R[y] <op> z
#   0011 if(R[x] <opc> R[y])
#   0100 if(R[x] <opc> in[y])
#   0101 if(R[x] <opc> y)
#   0110 R[x] = fun(R[y])
#   0111 R[x] = fun(in[y])
# OPCODE 4 BIT
# OP
#   0 +
#   1 -
#   2 *
#   3 /
# OPC
#   0 <=
#   1 >
# FUN
#   0 sin
#   1 cos
#   2 sqrt
#   3 exp
#   4 log
# OUTPUT VALUE X 8 BITS
# INPUT VALUE Y 8 BIT
# INPUT VALUE Z 8 BIT


def decode(instruction, offset=0):
    """Decodes a signle int into its parts"""
    # z = instruction & 0xff
    # y = (instruction >> 8) & 0xff
    # x = (instruction >> 16) & 0xff
    # op = (instruction >> 24) & 0xf
    # mode = (instruction >> 28) & 0xf
    (mode, x, y, z) = struct.unpack_from('bbbb', instruction, offset)

    return mode >> 4, mode & 0xf, x, y, z


class Instruction:
    """Represents an instruction in the instruction set"""

    def __init__(self, instruction, mode_info, offset=0):
        (mode, op, x, y, z) = decode(instruction, offset)
        self.mode = mode % len(mode_info)
        self.op = op % mode_info[self.mode][0]
        self.x = x % mode_info[self.mode][1]
        self.y = y % mode_info[self.mode][2]
        self.z = z % mode_info[self.mode][3]