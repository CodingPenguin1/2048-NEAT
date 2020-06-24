#!/usr/bin/env python
import threading
from multiprocessing import cpu_count
from random import randint
from time import sleep, time

import neat
import numpy as np

from Bot import Bot

# Global Constants
NUM_BOTS = 0 # This gets updated when reading the config file
CPU_COUNT = cpu_count()

# Global Vars
genStart = 0
genNum = 0


def update(dt):
    genStart = time()
    botsRunning = 0
    genTimer = int(time() - genStart)

    for bot in bots:
        bot.useBrain()


def evalGenomes(genomes, config):
    global genStart, genNum

    for i, (genomeID, genome) in enumerate(genomes):
        bot = bots[i]
        genome.fitness = 0
        bot.brain = neat.nn.FeedForwardNetwork.create(genome, config)
        bot.fitness = 0
        bot.genome = genome
        bot.genomeID = genomeID

    botsRunning = len(genomes)

    genStart = time()

    while botsRunning > 1:
        sleep(0.1)

    print('Generation completed')
    genNum += 1

    for bot in bots:
        if bot.genome is not None:
            bot.genome.fitness = bot.fitness
        bot.reset()


if __name__ == '__main__':
    # Load configuration
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')

    # Load some params from config into code
    with open('config', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('pop_size'):
                NUM_BOTS = int(line[line.find('= ') + 2:].strip())
                break
    print(f'Bot count: {NUM_BOTS}')

    # Create the population, which is the top-level object for a NEAT run
    population = neat.Population(config)

    # Add reporter so I can see stuff happen
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Create list of bots
    bots = [Bot() for _ in range(NUM_BOTS)]

    print(bots)

    # Train the population
    winner = population.run(evalGenomes)

    # TODO: add visualization (https://neat-python.readthedocs.io/en/latest/xor_example.html)
