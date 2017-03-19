import math

from Instruction import Instruction


def do_op(a, b, op):
    try:
        if op == 0:
        #   0 +
            return a + b
        if op == 1:
        #   1 -
            return a - b
        if op == 2:
        #   2 *
            return a * b
        if op == 3 and b > 0.00001:
        #   3 /
            return a / b
        return a
    except OverflowError:
        print("Overflow ERROR", a, b, op)
        return a

op_str = ['+', '-', '*', '/']
op_count = 4

class SimpleProcessor:

    def __init__(self, register_count, input_count, output_count):
        """Takes in a program, a set of 32bit integers as described in the instruction set."""
        self.instruction_count = 0
        self.program_count = 0

        self.instructionType = [self.reg_reg_op, self.reg_in_op]
        self.function_list = []

        self.program = None
        self.input = None
        self.input_count = input_count
        self.register_count = register_count
        self.r = [0] * register_count
        self.output_count = output_count
        self.mode_count = len(self.instructionType)
        self.function_count = len(self.function_list)

        self.mode_info = [
            [op_count, register_count, register_count, 1],
            [op_count, register_count, input_count, 1]
        ]

    def set_input(self, input_array):
        self.input = list(input_array)
        self.r = [0] * self.register_count

    def set_program(self, program):
        self.program_count += 1
        # you got to love pythons list creation power some times.
        self.program = [Instruction(program, self.mode_info, i) for i in range(0, len(program), 4)]

    def run(self):
        for instruction in self.program:
            self.do_instruction(instruction)

    def get_value(self):
        max_val = self.r[0]
        index = 0
        for i in range(1, self.output_count):
            if self.r[i] > max_val:
                max_val = self.r[i]
                index = i
        return index

    def do_instruction(self, instruction):
        self.instruction_count += 1
	instruction_fun = self.instructionType[instruction.mode]
        instruction_fun(instruction.op, instruction.x, instruction.y, instruction.z)

    def print_program(self):
        for instruction in self.program:
            self.print_instruction(instruction)

    def print_instruction(self, instruction):
        m = instruction.mode % self.mode_count
        if m == 0:
            print("r[%d] = r[%d] %s r[%d]" % (instruction.x, instruction.x, op_str[instruction.op % len(op_str)], instruction.y))
        elif m == 1:
            print("r[%d] = r[%d] %s in[%d]" % (instruction.x, instruction.x, op_str[instruction.op % len(op_str)], instruction.y))

#   0000 R[x] = R[x] <op> R[y]
    def reg_reg_op(self, op, x, y, z):
        self.r[x % self.register_count] = do_op(self.r[x], self.r[y], op)

#   0001 R[x] = R[x] <op> in[y]
    def reg_in_op(self, op, x, y, z):
        self.r[x % self.register_count] = do_op(self.r[x], self.input[y], op)
