import os
import sys
import random
import operator

seed = random.randint(0, sys.maxint)
myRand = random.Random(seed)


def init(fitness_function, program_runner, mutation_chance, multi_to_one_fitness):
    global simulator, runner, mutate_prob, multi_to_one_fitness_function
    simulator = fitness_function
    runner = program_runner
    mutate_prob = mutation_chance
    multi_to_one_fitness_function = multi_to_one_fitness


# Selection Operators
def steady_state_tournament(population):
    tournament_bracket = myRand.sample(range(0, len(population)), 4)
    fitness = [(i, multi_to_one_fitness_function(population[i][1])) for i in tournament_bracket]
    fitness.sort(key=lambda x: x[1])
    kid1, kid2 = crossover(population[fitness[2][0]][0], population[fitness[3][0]][0])
    population[fitness[0][0]] = kid1
    population[fitness[1][0]] = kid2
    return population[fitness[3][0]], population


def proportional_selection(population):
    fitness = [0] * len(population)
    kids = []
    max_fitness = 0
    max_program = ''
    for p, i in zip(population, range(len(population))):
        fitness[i] = multi_to_one_fitness_function(population[i][1])
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
    return max_program, population


def elitist_proportional_selection(population):
    fitness = [0] * len(population)
    kids = []
    for p, i in zip(population, range(len(population))):
        fitness[i] = multi_to_one_fitness_function(population[i][1])
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
    return max_program, population


def pareto_grand_mutation(population):
    pop_size = len(population)
    mutated_pop = [mutate(p[0]) for p in population]
    population.extend([(prog, simulator(prog, runner)) for prog in mutated_pop])
    population = [ y for (x, y) in sorted(zip(pareto_count(population),population))][pop_size:]
    return population[-1], population


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

# Given two scores, is one dominating the other?
def dominating(score1, score2):
    canDom1 = True
    canDom2 = True
    better1 = False
    better2 = False
    for goal1, goal2 in zip(score1, score2):
        if goal1 > goal2:
            better1 = True
            canDom2 = False
        elif goal2 > goal1:
            better2 = True
            canDom1 = False
    if canDom1 and better1:
        return 1
    elif canDom2 and better2:
        return 2
    else:
        return 0


def pareto_rank(population):
    fitness = [0] * len(population)
    for index1, prog1 in enumerate(population):
        score1 = prog1[1]
        for index2, prog2 in enumerate(population[index1:]):
            score2 = prog2[1]
            dom = dominating(score1, score2)
            if dom == 1:
                fitness[index2 + index1] += 1
            elif dom == 2:
                fitness[index1] += 1
    base = max(fitness) + 1
    fitness = [base - s for s in fitness]
    return fitness


def pareto_count(population):
    fitness = [0] * len(population)
    for index1, prog1 in enumerate(population):
        score1 = prog1[1]
        for index2, prog2 in enumerate(population[index1:]):
            score2 = prog2[1]
            dom = dominating(score1, score2)
            if dom == 1:
                fitness[index1] += 1
            elif dom == 2:
                fitness[index2 + index1] += 1
    return fitness

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

def add_fitness(fit):
    return sum(fit)

def prob_mutate(program):
    if myRand.random() < mutate_prob:
        program = mutate(program)
    return (program, simulator(program, runner))

def mutate(program):
    """Takes in a single program and replaces one instruction at random with a new instruction."""
    new_instruction = os.urandom(4)
    position = myRand.randrange(0, len(program), 4)
    return program[:position] + new_instruction + program[position+4:]
