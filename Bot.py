from math import log2
from random import randint

import numpy as np

from Board import Board


class Bot:
    def __init__(self, boardSize=(4, 4)):
        self.board = Board(boardSize[0], boardSize[1])
        self.isRunning = True

        # For learning
        self.fitness = self.board.score
        self.brain = None

    def useBrain(self):
        # 18 inputs: each cell of the board
        #            the count of nonzero cells
        # 1 output: direction to move

        # Run the bot until the game is over
        while not self.board.checkGameOver():
            # Define input vector

            # The board itself
            inputs = []
            for row in range(len(self.board.array)):
                for col in range(len(self.board.array[0])):
                    inputs.append(self.board.array[row][col])

            # The number of nonzero tiles
            nonZeroTileCount = 0
            for row in range(len(self.board.array)):
                for col in range(len(self.board.array[0])):
                    if self.board.array[row][col] != 0:
                        nonZeroTileCount += 1
            inputs.append(nonZeroTileCount)

            # Reference value
            inputs.append(1.0)
            # print(inputs)

            # Do the black magic and get output
            output = self.brain.activate(inputs) if self.brain is not None else [0 for _ in range(18)]

            if output[0] <= 0.25:
                direction = 'left'
            elif output[0] <= 0.5:
                direction = 'right'
            elif output[0] <= 0.75:
                direction = 'up'
            else:
                direction = 'down'

            # Update board
            self.board.move(direction)

        # Update fitness
        self.fitness = self.board.score

        # Update isRunning of game is over
        self.isRunning = self.board.gameOver
