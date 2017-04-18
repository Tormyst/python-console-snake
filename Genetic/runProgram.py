from pickle import load
from sys import argv
from time import sleep

import Processor
import snake

if len(argv) != 2:
    print("Please give me a program to run")
    exit(1)

file = open(argv[1], 'rb')
program, register_count, input_count, instruction_set = load(file)

Processor_Class = {'simple': Processor.SimpleProcessor, 'complex': Processor.Processor}[instruction_set]

program_runner = Processor_Class(register_count=register_count,
                                     input_count=input_count,
                                     output_count=4)
program_runner.set_program(program)

program_runner.print_program()

while True:
    score = snake.run(True, program_runner)
    print("Score: {}".format(score))
    sleep(1)