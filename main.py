#!/usr/bin/env python
import concurrent.futures
from multiprocessing import cpu_count

import neat
from progress.bar import IncrementalBar

import visualize
from Bot import Bot

# Global Constants
BOTS_PER_GENOME = 1

# Global Vars
highScore = 0
highTile = 0


def runGenome(genome, genomeID, config):
    highScore = 0
    highTile = 0
    fitness = 0
    for i in range(BOTS_PER_GENOME):
        bot = Bot()
        bot.brain = neat.nn.FeedForwardNetwork.create(genome, config)
        bot.useBrain()
        fitness += bot.fitness
        if bot.fitness > highScore:
            highScore = bot.fitness
    # Average bot fitnesses to get overall genome fitness
    fitness /= BOTS_PER_GENOME

    # Get high tile
    for row in bot.board.array:
        for cell in row:
            if cell > highTile:
                highTile = cell

    return fitness, genomeID, highScore, highTile


def runGeneration(genomes, config):
    global highScore, highTile

    # Create, run, and evalute the genomes
    with concurrent.futures.ProcessPoolExecutor(cpu_count()) as executor:
        evaluatedGenomes = [executor.submit(runGenome, genome, genomeID, config) for (genomeID, genome) in genomes]

        with IncrementalBar('Running genomes', max=len(genomes)) as bar:
            for completed in concurrent.futures.as_completed(evaluatedGenomes):
                # Update genome fitness
                fitness, ID, bestGenomeScore, bestGenomeTile = completed.result()
                for (genomeID, genome) in genomes:
                    if genomeID == ID:
                        genome.fitness = fitness

                # Update high score and tile
                if bestGenomeScore > highScore:
                    highScore = bestGenomeScore
                if bestGenomeTile > highTile:
                    highTile = bestGenomeTile

                bar.next()

    # Print max score and tile so far
    print(f'High Score: {highScore}')
    print(f'High Tile: {highTile}')


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
