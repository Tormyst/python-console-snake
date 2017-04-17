"""Genetic Box 1.

Usage:
  genetic.py [options]
  genetic.py (-h | --help)
  genetic.py --version

Options:
  -h --help                      Show this screen.
  -c --count=<value>             Count of how many runs to preform per fitness evaluation. [default: 1]
  --seed=<seed>                  use a fixed seed
  -p --population=<population>   Population size [default: 100].
  -v --variation=<selection>     Sets the selection-replacement operator (see below for options) [default: sst]
  -r --registers=<count>         Sets the number of registers to be used in the program [default: 8]
  -f --fitness=<kind>            Sets the mode of fitness to use to take multi objective to a single value. [default: add]
  -m --mutation=<probability>    Sets the probability that any child gets mutated [default: 0.05]
  -s --stop=<count>              Sets the stop criterion based on the number of fitness calculations done [default: 5000]
  -i --instruction=<set>         Sets the instruction set to use for the program [default: complex]
  -V --visual                    Sets all runs to be visual.

Selection-replacement Operators:
  sst   Steady State Tournament
  ps    Proportional Selection
  eps   Elitist Proportional Selection
  
Fitness Calculators:
  add   Add fitness values together.
  rank  Use pareto rank.
  count Use pareto count.

Instruction Sets:
  simple    A set that contains simple instructions.
  complex   A set that includes far more vaired instructions, including branching and functions.
"""

from docopt import docopt
from pickle import dump

import helper
import Processor
import snake
import random

input_count = 6
output_count = 4

def main(args):
    # Valid selection types
    selection = {'sst': helper.steady_state_tournament, 'ps': helper.proportional_selection,
                 'eps': helper.elitist_proportional_selection, 'pm': helper.pure_mutation}
    fitness_kind = {'add': helper.all_add_fitness, 'rank': helper.pareto_rank, 'count': helper.pareto_count}
    instruction_sets = {'simple': Processor.SimpleProcessor, 'complex': Processor.Processor}

    initial_program_size = int(args['--registers']) * 3
    pop = int(args['--population'])

    if args['--variation'] not in selection:
        print('Sorry, I don\'t know how to use the selection operator {}.'.format(args['--variation']))
        exit(-1)
    else:
        sel = selection[args['--variation']]

    if args['--fitness'] not in fitness_kind:
        print('Sorry, I don\'t know how to use the fitness operator {}.'.format(args['--fitness']))
        exit(-1)
    else:
        fit = fitness_kind[args['--fitness']]

    if args['--instruction'] not in instruction_sets:
        print('Sorry, I don\'t know a instruction set named {}.'.format(args['--instruction']))
        exit(-1)
    else:
        Processor_Class = instruction_sets[args['--instruction']]

    print('Making a population of {} programs'.format(pop))

    population = [helper.random_program(initial_program_size) for _ in range(pop)]

    print('creating program runner instance')
    program_runner = Processor_Class(register_count=int(args['--registers']),
                                     input_count=input_count,
                                     output_count=output_count)

    stop_value = int(args['--stop'])
    mutation_chance = float(args['--mutation'])
    best_fit = 0
    best_prog = ''

    snake.gameloop.run_count = int(args['--count'])

    def simulatorFitness(program, program_runner):
        if '--seed' in args:
            random.seed(args['--seed'])
        program_runner.set_program(program)
        return snake.run(args['--visual'], program_runner)

    print('Calculating fitness for entire first population.')
    population = [(prog, simulatorFitness(prog, program_runner)) for prog in population]

    helper.init(simulatorFitness, program_runner, mutation_chance, fit)

    print('Starting genetic evolution')

    print('Average size of program: {}'.format(sum([len(p[0]) for p in population])/float(len(population))))

    while program_runner.program_count <= stop_value:
        (max_prog, max_fit), population = sel(population)
        # if True:
        if helper.add_fitness(max_fit) > best_fit:
            best_fit = helper.add_fitness(max_fit)
            best_prog = max_prog
            if '--seed' in args:
                random.seed(args['--seed'])
            program_runner.set_program(best_prog)
            program_runner.program_count -= 1 # to offset running it again.
            snake.run(True, program_runner)
            print('New best program with fitness of {}, after running {} programs.'.format(best_fit, program_runner.program_count))
    program_runner.set_program(best_prog)
    if '--seed' in args:
        random.seed(args['--seed'])
    print("Final Score: {}".format(snake.run(True, program_runner)))

    print('Average size of program: {}'.format(sum([len(p[0]) for p in population]) / float(len(population))))

    file = open("bestProgram.dat", 'wb')
    dump((best_prog, int(args['--registers']), input_count, args['--instruction']),file)
    file.close()


def run():
    # pr = cProfile.Profile()
    # pr.enable()
    main(docopt(__doc__, argv=None, help=True, version='1.0', options_first=False))
    # pr.disable()
    # pr.print_stats(sort='tottime')

if __name__ == "__main__":
    run()
