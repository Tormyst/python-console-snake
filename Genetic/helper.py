import os
import sys
import random
import operator

seed = random.randint(0, sys.maxint)
myRand = random.Random(seed)

def init(fitness_function, program_runner, mutation_chance):
    global simulator, runner, mutate_prob
    simulator = fitness_function
    runner = program_runner
    mutate_prob = mutation_chance


# Selection Operators
def steady_state_tournament(population):
    tournament_bracket = myRand.sample(range(0, len(population)), 4)
    fitness = [(i, population[i][1]) for i in tournament_bracket]
    fitness.sort(key=lambda x: x[1])
    kid1, kid2 = crossover(population[fitness[2][0]][0], population[fitness[3][0]][0])
    population[fitness[0][0]] = kid1
    population[fitness[1][0]] = kid2
    return population[fitness[3][0]]


def proportional_selection(population):
    fitness = [0] * len(population)
    kids = []
    max_fitness = 0
    max_program = ''
    for p, i in zip(population, range(len(population))):
        fitness[i] = population[i][1]
        if population[i][1] > max_fitness:
            max_fitness = fitness[i]
            max_program = p
    total_fitness = sum(fitness)
    for _ in range(len(population)//2):
        index1 = proportional_select(fitness, total_fitness)
        index2 = proportional_select(fitness, total_fitness, sample_block=[index1])
        kid1, kid2 = crossover(population[index1][0], population[index2][0])
        kids.append(kid1)
        kids.append(kid2)
    for i in range(len(population)):
        population[i] = kids[i]
    return max_program


def elitist_proportional_selection(population):
    fitness = [0] * len(population)
    kids = []
    for p, i in zip(population, range(len(population))):
        fitness[i] = population[i][1]
    total_fitness = sum(fitness)
    for _ in range((len(population)//2) - 1):
        index1 = proportional_select(fitness, total_fitness)
        index2 = proportional_select(fitness, total_fitness, sample_block=[index1])
        kid1, kid2 = crossover(population[index1][0], population[index2][0])
        kids.append(kid1)
        kids.append(kid2)

    index1, max_fitness = max(enumerate(fitness), key=operator.itemgetter(1))
    kids.append(population[index1])
    max_program = population[index1]
    fitness[index1] = 0
    index2 = max(enumerate(fitness), key=operator.itemgetter(1))[0]
    kids.append(population[index2])

    for i in range(len(population)):
        population[i] = kids[i]
    return max_program


def proportional_select(propotional_population, total, sample_block=[]):
    total -= sum([propotional_population[i] for i in sample_block])
    rand_val = myRand.random() * total
    pop_size = len(propotional_population)
    index = 0
    while rand_val > 0:
        index += 1
        index %= pop_size
        if index not in sample_block:
            rand_val -= propotional_population[index]
    return index


def random_program(program_size):
    return os.urandom(program_size * 4)

def crossover(program1, program2):
    """Takes 2 programs and preforms 2 point cross over on them, creating two children"""
    prog1_points = myRand.sample(range(0, len(program1) + 1, 4), 2)
    prog2_points = myRand.sample(range(0, len(program2) + 1, 4), 2)
    prog1_points.sort()
    prog2_points.sort()
    child1 = program1[:prog1_points[0]] + program2[prog2_points[0]:prog2_points[1]] + program1[prog1_points[1]:]
    child2 = program2[:prog2_points[0]] + program1[prog1_points[0]:prog1_points[1]] + program2[prog2_points[1]:]
    return prob_mutate(child1), prob_mutate(child2)


def prob_mutate(program):
    if myRand.random() < mutate_prob:
        program = mutate(program)
    return (program, simulator(program, runner))

def mutate(program):
    """Takes in a single program and replaces one instruction at random with a new instruction."""
    new_instruction = os.urandom(4)
    position = myRand.randrange(0, len(program), 4)
    return program[:position] + new_instruction + program[position+4:]
