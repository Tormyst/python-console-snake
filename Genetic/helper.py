import os
import random
import operator


# Selection Operators
def steady_state_tournament(population, program_runner, mutation_chance, fitness_function):
    tournament_bracket = random.sample(range(0, len(population)), 4)
    fitness = [(i, fitness_function(population[i], program_runner)) for i in tournament_bracket]
    fitness.sort(key=lambda x: x[1])
    kid1, kid2 = crossover(population[fitness[2][0]], population[fitness[3][0]], mutation_chance)
    population[fitness[0][0]] = kid1
    population[fitness[1][0]] = kid2
    return fitness[3][1], population[fitness[3][0]]


def proportional_selection(population, program_runner, mutation_chance, fitness_function):
    fitness = [0] * len(population)
    kids = []
    max_fitness = 0
    max_program = ''
    for p, i in zip(population, range(len(population))):
        fitness[i] = fitness_function(p, program_runner)
        if fitness[i] > max_fitness:
            max_fitness = fitness[i]
            max_program = p
    total_fitness = sum(fitness)
    for _ in range(len(population)//2):
        index1 = proportional_select(fitness, total_fitness)
        index2 = proportional_select(fitness, total_fitness, sample_block=[index1])
        kid1, kid2 = crossover(population[index1], population[index2], mutation_chance)
        kids.append(kid1)
        kids.append(kid2)
    for i in range(len(population)):
        population[i] = kids[i]
    return max_fitness, max_program


def elitist_proportional_selection(population, program_runner, mutation_chance, fitness_function):
    fitness = [0] * len(population)
    kids = []
    for p, i in zip(population, range(len(population))):
        fitness[i] = (fitness_function(p, program_runner))
    total_fitness = sum(fitness)
    for _ in range((len(population)//2) - 1):
        index1 = proportional_select(fitness, total_fitness)
        index2 = proportional_select(fitness, total_fitness, sample_block=[index1])
        kid1, kid2 = crossover(population[index1], population[index2], mutation_chance)
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
    return max_fitness, max_program


def proportional_select(propotional_population, total, sample_block=[]):
    total -= sum([propotional_population[i] for i in sample_block])
    rand_val = random.random() * total
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

def crossover(program1, program2, mutation_chance):
    """Takes 2 programs and preforms 2 point cross over on them, creating two children"""
    prog1_points = random.sample(range(0, len(program1) + 1, 4), 2)
    prog2_points = random.sample(range(0, len(program2) + 1, 4), 2)
    prog1_points.sort()
    prog2_points.sort()
    child1 = program1[:prog1_points[0]] + program2[prog2_points[0]:prog2_points[1]] + program1[prog1_points[1]:]
    child2 = program2[:prog2_points[0]] + program1[prog1_points[0]:prog1_points[1]] + program2[prog2_points[1]:]
    return prob_mutate(child1, mutation_chance), prob_mutate(child2, mutation_chance)


def prob_mutate(program, prob):
    if random.random() < prob:
        return mutate(program)
    else:
        return program

def mutate(program):
    """Takes in a single program and replaces one instruction at random with a new instruction."""
    new_instruction = os.urandom(4)
    position = random.randrange(0, len(program), 4)
    return program[:position] + new_instruction + program[position+4:]
