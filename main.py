#!/usr/bin/env python
import concurrent.futures

import neat
from progress.bar import IncrementalBar

from Bot import Bot

# Global Constants
BOTS_PER_GENOME = 5

# Global Vars
highScore = 0


def runGenome(genome, genomeID, config):
    highScore = 0
    genome.fitness = 0
    for i in range(BOTS_PER_GENOME):
        bot = Bot()
        bot.brain = neat.nn.FeedForwardNetwork.create(genome, config)
        bot.useBrain()
        genome.fitness += bot.fitness
        if bot.fitness > highScore:
            highScore = bot.fitness
    # Average bot fitnesses to get overall genome fitness
    genome.fitness /= BOTS_PER_GENOME
    return genome.fitness, genomeID, highScore


def runGeneration(genomes, config):
    global highScore

    # Create, run, and evalute the genomes
    with concurrent.futures.ProcessPoolExecutor() as executor:
        evaluatedGenomes = [executor.submit(runGenome, genome, genomeID, config) for (genomeID, genome) in genomes]

        with IncrementalBar('Running bots', max=len(genomes)) as bar:
            for completed in concurrent.futures.as_completed(evaluatedGenomes):
                # Update genome fitness
                fitness, ID, bestGenomeScore = completed.result()
                for (genomeID, genome) in genomes:
                    if genomeID == ID:
                        genome.fitness = fitness

                # Update high score
                if bestGenomeScore > highScore:
                    highScore = bestGenomeScore
                bar.next()

    # Print max score (fitness) so far
    print(f'High Score: {highScore}')


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
