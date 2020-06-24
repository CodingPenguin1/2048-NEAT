#!/usr/bin/env python
import threading
from multiprocessing import cpu_count
from random import randint
from time import sleep, time

import neat
import numpy as np

from Bot import Bot
from progress.bar import IncrementalBar


# Global Constants
CPU_COUNT = cpu_count()
BOTS_PER_GENOME = 5

# Global Vars
genNum = 0


def runGeneration(genomes, config):
    global genNum

    # Generation timer
    genStart = time()

    # TODO: multiprocess this
    # Create, run, and evalute the genomes
    bar = IncrementalBar('Running Bots', max=len(genomes) * BOTS_PER_GENOME)
    for i, (genomeID, genome) in enumerate(genomes):
        genome.fitness = 0
        for j in range(BOTS_PER_GENOME):
            bot = Bot()
            bot.brain = neat.nn.FeedForwardNetwork.create(genome, config)  # Create
            bot.useBrain()  # Run
            genome.fitness += bot.fitness  # Evaluate
            bar.next()
        # Average bot fitnesses to get overall genome fitness
        genome.fitness /= BOTS_PER_GENOME
    bar.finish()

    # Logging
    genDuration = time() - genStart
    print(f'Generation {genNum} completed in {genDuration}s')
    genNum += 1


if __name__ == '__main__':
    # Load configuration
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config')

    # Create the population, which is the top-level object for a NEAT run
    population = neat.Population(config)

    # Add reporter so I can see stuff happen
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Train the population
    winner = population.run(runGeneration)

    # TODO: add visualization (https://neat-python.readthedocs.io/en/latest/xor_example.html)
