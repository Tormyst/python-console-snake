# Genetic program to play python-console-snake

> Fork of python-console-snake by tancredi
> A genetic programing interface designed to play this game of snake.

![Screenshot](https://s23.postimg.org/dj6d3xhi3/2017-04-17_00.17.55.gif)

### Usage

1. `git clone git@github.com:Tormyst/python-console-snake.git`
2. `cd python-console-snake`
3. `pip install --user -r requirements.txt`
4. `./run.sh`

### Options

Run `./run.sh -h` for list of options

```
Genetic Program Trainer to Play Snake

Usage:
  genetic.py [options]
  genetic.py (-h | --help)
  genetic.py --version

Options:
  -h --help                      Show this screen.
  -c --count=<value>             Count of how many runs to preform per fitness evaluation. [default: 1]
  --seed=<seed>                  use a fixed seed
  -p --population=<population>   Population size [default: 100]
  -v --variation=<selection>     Sets the selection-replacement operator (see below for options) [default: sst]
  -r --registers=<count>         Sets the number of registers to be used in the program [default: 8]
  -f --fitness=<kind>            Sets the mode of fitness to use to take multi objective to a single value. [default: add]
  -m --mutation=<probability>    Sets the probability that any child gets mutated [default: 0.05]
  -s --stop=<count>              Sets the stop criterion based on the number of fitness calculations done [default: 5000]
  -i --instruction=<set>         Sets the instruction set to use for the program [default: complex]
  -V --visual                    Sets all runs to be visual

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
```

### Output

The best program will be saved in a file named `bestProgram.dat`.  To run this file use the provided runner: `runprog.sh`.  There are no options, just give it a file, and it will print out the program then continue to play games until stoped with one second pauses between games.

### Licence

Copyright (c) 2017 Raphael Bronfman-Nadas. - Released under the MIT license

Original:

Copyright (c) 2014 Tancredi Trugenberger. - Released under the MIT license
