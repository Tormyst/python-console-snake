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
        if op == 3:
        #   3 /
            return a / max(b, 0.0001)
        return a
    except OverflowError:
        return a


def do_opc(a, b, opc):
    # Note this returns the inverse, if it should branch
    if opc == 0:
        #   0 <=
        return a > b
    if opc == 1:
        #   1 >
        return a <= b

op_str = ['+', '-', '*', '/']
opc_str = ['<=', '>']
fun_str = ['sin', 'cos', 'sqrt', 'exp', 'log']
op_count = 4
opc_count = 2

def safe_log(x):
    return math.log(max(x, 0.0001))

def safe_sqrt(x):
    return math.sqrt(math.fabs(x))


class Processor:

    def __init__(self, register_count, input_count, output_count):
        """Takes in a program, a set of 32bit integers as described in the instruction set."""
        self.instruction_count = 0
        self.program_count = 0

        self.instructionType = [self.reg_reg_op, self.reg_in_op, self.reg_const_op, self.reg_reg_if, self.reg_in_if, self.reg_const_if, self.reg_fun, self.in_fun]
        self.function_list = [math.sin, math.cos, safe_sqrt, math.exp, safe_log]

        self.program = None
        self.input = None
        self.input_count = input_count
        self.register_count = register_count
        self.r = [0] * register_count
        self.output_count = output_count
        self.mode_count = len(self.instructionType)
        self.function_count = len(self.function_list)
        self.branching = False

        self.mode_info = [
            [op_count, register_count, register_count, register_count],
            [op_count, register_count, register_count, input_count],
            [op_count, register_count, register_count, 256],
            [opc_count, register_count, register_count, 256],
            [opc_count, register_count, input_count, 256],
            [opc_count, register_count, 256, 256],
            [self.function_count, register_count, register_count, 256],
            [self.function_count, register_count, input_count, 256]
        ]

    def set_input(self, input_array):
        self.input = list(input_array)
        self.r = [0] * self.register_count
        self.branching = False

    def set_program(self, program):
        self.program = []
        self.program_count += 1
        for i in range(0, len(program), 4):
            self.program.append(Instruction(program, self.mode_info, i))

    def run(self):
        for instruction in self.program:
            self.do_instruction(instruction)

    def get_value(self):
        max = self.r[0]
        index = 0
        for i in range(1, self.output_count):
            if self.r[i] > max:
                max = self.r[i]
                index = i
        return index

    def do_instruction(self, instruction):
	self.instruction_count += 1
        instruction_fun = self.instructionType[instruction.mode % self.mode_count]
        instruction_fun(instruction.op, instruction.x, instruction.y, instruction.z)

    def print_program(self):
        for instruction in self.program:
            self.print_instruction(instruction)

    def print_instruction(self, instruction):
        m = instruction.mode % self.mode_count
        if m == 0:
            print("r[%d] = r[%d] %s r[%d]" % (instruction.x, instruction.y, op_str[instruction.op % len(op_str)], instruction.z))
        elif m == 1:
            print("r[%d] = r[%d] %s in[%d]" % (instruction.x % self.register_count, instruction.y, op_str[instruction.op % len(op_str)], instruction.z))
        elif m == 2:
            print("r[%d] = r[%d] %s %d" % (instruction.x % self.register_count, instruction.y, op_str[instruction.op % len(op_str)], instruction.z))
        elif m == 3:
            print("if( r[%d] %s r[%d] )" % (instruction.x % self.register_count, opc_str[instruction.op % len(opc_str)], instruction.y))
        elif m == 4:
            print("if( r[%d] %s in[%d] )" % (instruction.x % self.register_count, opc_str[instruction.op % len(opc_str)], instruction.y))
        elif m == 5:
            print("if( r[%d] %s %d )" % (instruction.x % self.register_count, opc_str[instruction.op % len(opc_str)], instruction.y))
        elif m == 6:
            print("r[%d] = %s(r[%d])" % (instruction.x % self.register_count, fun_str[instruction.op % len(fun_str)], instruction.y))
        elif m == 7:
            print("r[%d] = %s(in[%d])" % (instruction.x % self.register_count, fun_str[instruction.op % len(fun_str)], instruction.y))


#   0000 R[x] = R[y] <op> R[z]
    def reg_reg_op(self, op, x, y, z):
        if self.branching:
            self.branching = False
            return
        self.r[x % self.register_count] = do_op(self.r[y], self.r[z], op)

#   0001 R[x] = R[y] <op> in[z]
    def reg_in_op(self, op, x, y, z):
        if self.branching:
            self.branching = False
            return
        self.r[x % self.register_count] = do_op(self.r[y], self.input[z], op)

#   0010 R[x] = R[y] <op> z
    def reg_const_op(self, op, x, y, z):
        if self.branching:
            self.branching = False
            return
        self.r[x % self.register_count] = do_op(self.r[y], z, op)

#   0011 if(R[x] <opc> R[y])
    def reg_reg_if(self, op, x, y, z):
        if self.branching:
            return
        self.branching = do_opc(self.r[x % self.register_count], self.r[y], op)

#   0100 if(R[x] <opc> in[y])
    def reg_in_if(self, op, x, y, z):
        if self.branching:
            return
        self.branching = do_opc(self.r[x % self.register_count], self.input[y], op)

#   0101 if(R[x] <opc> y)
    def reg_const_if(self, op, x, y, z):
        if self.branching:
            return
        self.branching = do_opc(self.r[x % self.register_count], y, op)

#   0110 R[x] = fun(R[y])
    def reg_fun(self, op, x, y, z):
        if self.branching:
            self.branching = False
            return
        try:
            fun = self.function_list[op % self.function_count]
            self.r[x % self.register_count] = fun(self.r[y])
        except OverflowError:
            return
        except ValueError:
            return

#   0111 R[x] = fun(in[y])
    def in_fun(self, op, x, y, z):
        if self.branching:
            self.branching = False
            return
        try:
            fun = self.function_list[op % self.function_count]
            self.r[x % self.register_count] = fun(self.input[y])
        except OverflowError:
            return
        except ValueError:
            return
